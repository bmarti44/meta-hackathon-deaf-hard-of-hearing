"""Gen12 eval: held-out objective metrics for J4-A1 -- T0 ONLY, no listener claim.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
Held-out target speakers 1988/1993 (unseen in training).
Conditions: babble3 from unseen interferer speakers 8842/8297, SSN (seen class),
  white noise (HELD-OUT noise class, never trained), quiet. SNRs -5/0/+5/+10 dB.
Envelope-domain (primary, native I/O): mask-MSE vs IRM, log-envelope MAE of
  masked vs clean envelope, envelope-SNR proxy improvement.
Waveform-domain (T0 reporting ONLY): mel mask -> per-bin gain (fb-weighted),
  applied to noisy STFT (128/64, noisy phase), Hann OLA. This synthesis path is
  NOT part of J4-A1 (spec S2.1 bars waveform output); it exists only so SI-SDR /
  STOI / PESQ-WB can be computed. Comparators through the SAME OLA path:
  unprocessed-OLA (gain=1), oracle mel-IRM. Raw mixture SI-SDR also printed.
SI-SDR implemented in numpy; STOI via pystoi, PESQ-WB via pesq (both preinstalled).
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
import numpy as np, torch
HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE.parent/"gen11")); sys.path.insert(0,str(HERE))
from j4_model import EPS, FS, H, W, J4A1  # noqa
from train_j4 import TEST_BABBLE_SPK, TEST_SPK, babble, crop, load_pool, make_ssn_fast, rms  # noqa
from pystoi import stoi as _stoi
from pesq import pesq as _pesq

def si_sdr(ref, est):
    ref=np.asarray(ref,dtype=np.float64); est=np.asarray(est,dtype=np.float64)
    ref=ref-ref.mean(); est=est-est.mean()
    alpha=np.dot(est,ref)/(np.dot(ref,ref)+1e-12); proj=alpha*ref; noise=est-proj
    return float(10*np.log10((np.dot(proj,proj)+1e-12)/(np.dot(noise,noise)+1e-12)))

def stoi_v(ref,est):
    try: return float(_stoi(ref.astype(np.float64),est.astype(np.float64),FS,extended=False))
    except Exception: return float("nan")
def pesq_v(ref,est):
    try: return float(_pesq(FS,ref.astype(np.float64),est.astype(np.float64),"wb"))
    except Exception: return float("nan")

@torch.no_grad()
def reconstruct(model, mix_1d, masks_2d):
    """masks (T,64) -> waveform via fb-weighted bin gains, noisy phase, Hann OLA.
    Bins 0 (DC) and 64 (Nyquist) have zero filterbank coverage: they take the
    frame-mean mask (same convention for every comparator). Synthesis uses a
    single (analysis) window: out = OLA(irfft(spec*gain)) / OLA(win); samples
    where OLA(win) < 0.05 are zeroed and callers trim 256 samples at each end
    before waveform metrics (spectral modification + tiny OLA norm at the
    stream edges otherwise explodes -- measured during development)."""
    x=torch.from_numpy(mix_1d[None].astype(np.float32))
    from j4_model import frame_signal
    frames=frame_signal(x)[0]  # (T,W)
    win=model.window; spec=torch.fft.rfft(frames*win,dim=-1)  # (T,65) noisy phase retained
    fb=model.filterbank  # (64,65)
    fbsum=fb.sum(dim=0,keepdim=True)
    gain=(masks_2d@fb)/ torch.clamp(fbsum,min=1e-8)
    gain=torch.where(fbsum>1e-6, gain, masks_2d.mean(dim=1,keepdim=True).expand_as(gain))
    gain=torch.clamp(gain,0,1)
    masked=torch.fft.irfft(spec*gain,n=W,dim=-1)  # already carries analysis window
    n=len(mix_1d); out=np.zeros(n); norm=np.zeros(n); w1=win.numpy()
    mf=masked.numpy()
    for j in range(mf.shape[0]):
        s=j*H; out[s:s+W]+=mf[j]; norm[s:s+W]+=w1
    ok=norm>0.05; out[ok]/=norm[ok]; out[~ok]=0.0
    return out.astype(np.float32)

@torch.no_grad()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--weights",default=str(HERE/"j4a1_gen12.pt"))
    ap.add_argument("--n-per-cell",type=int,default=6); ap.add_argument("--out",default=str(HERE/"eval_results.json")); a=ap.parse_args()
    sha=hashlib.sha256(Path(a.weights).read_bytes()).hexdigest()
    ckpt=torch.load(a.weights,map_location="cpu",weights_only=False)
    model=J4A1(); model.load_state_dict(ckpt["state_dict"]); model.eval()
    pool=load_pool(TEST_SPK+TEST_BABBLE_SPK)
    rng=np.random.default_rng(777)
    SEG=4*FS  # 4s for stabler STOI/PESQ
    rows=[]; t0=time.time()
    for kind in ["babble3-unseen","ssn","white-heldout","quiet"]:
        snrs=[999.0] if kind=="quiet" else [-5.0,0.0,5.0,10.0]
        for snr in snrs:
            for i in range(a.n_per_cell):
                spk=TEST_SPK[i%len(TEST_SPK)]
                clean=crop(rng,pool[spk][rng.integers(0,len(pool[spk]))],SEG)
                clean=(clean/(rms(clean)+1e-9)*0.1).astype(np.float32)
                if kind=="quiet": noise=np.zeros_like(clean)
                elif kind.startswith("babble"): noise=babble(rng,pool,TEST_BABBLE_SPK,n=SEG)
                elif kind=="ssn":
                    # extend 2s generator to 4s
                    noise=np.concatenate([make_ssn_fast(rng,SEG//2),make_ssn_fast(rng,SEG-SEG//2)])
                else: noise=rng.standard_normal(SEG).astype(np.float32)
                if kind!="quiet": noise=(noise/(rms(noise)+1e-9)*rms(clean)*10**(-snr/20)).astype(np.float32)
                mix=(clean+noise).astype(np.float32)
                ct=torch.from_numpy(clean[None]); nt=torch.from_numpy(noise[None]); mt=torch.from_numpy(mix[None])
                _,ec=model.extract_features(ct); _,en=model.extract_features(nt)
                irm=torch.sqrt(ec**2/(ec**2+en**2+EPS))
                masks,masked=model(mt)
                _,mixenv=model.extract_features(mt)
                # envelope-domain metrics
                mask_mse=float(torch.mean((masks-irm)**2))
                logmae_j4=float(torch.mean(torch.abs(torch.log(masked+1e-6)-torch.log(ec+1e-6))))
                logmae_un=float(torch.mean(torch.abs(torch.log(mixenv+1e-6)-torch.log(ec+1e-6))))
                oracle_masked=irm*mixenv
                logmae_or=float(torch.mean(torch.abs(torch.log(oracle_masked+1e-6)-torch.log(ec+1e-6))))
                # quiet identity: mean mask on clean
                # waveform T0
                T=masks.shape[1]
                wav_j4=reconstruct(model,mix,masks[0]); wav_or=reconstruct(model,mix,irm[0]); wav_un=reconstruct(model,mix,torch.ones_like(masks[0]))
                tr=lambda v: v[256:-256]  # trim OLA edges, all systems incl. reference
                rows.append({"kind":kind,"snr_db":snr,"spk":spk,
                    "mask_mse":mask_mse,"env_logMAE_unproc":logmae_un,"env_logMAE_j4":logmae_j4,"env_logMAE_oracleIRM":logmae_or,
                    "sisdr_mix_raw":si_sdr(tr(clean),tr(mix)),"sisdr_unprocOLA":si_sdr(tr(clean),tr(wav_un)),"sisdr_j4":si_sdr(tr(clean),tr(wav_j4)),"sisdr_oracleIRM":si_sdr(tr(clean),tr(wav_or)),
                    "stoi_unprocOLA":stoi_v(tr(clean),tr(wav_un)),"stoi_j4":stoi_v(tr(clean),tr(wav_j4)),"stoi_oracleIRM":stoi_v(tr(clean),tr(wav_or)),
                    "pesq_unprocOLA":pesq_v(tr(clean),tr(wav_un)),"pesq_j4":pesq_v(tr(clean),tr(wav_j4)),"pesq_oracleIRM":pesq_v(tr(clean),tr(wav_or))})
            print(f"done {kind} snr={snr} elapsed={time.time()-t0:.0f}s",flush=True)
    # aggregate by kind (over SNRs) and overall noisy
    def agg(sel):
        keys=[k for k in rows[0] if k not in ("kind","spk","snr_db")]
        return {k: float(np.nanmean([r[k] for r in sel])) for k in keys} | {"n":len(sel)}
    summary={"weights_sha256":sha,"n_rows":len(rows),
             "by_kind":{k:agg([r for r in rows if r["kind"]==k]) for k in sorted(set(r["kind"] for r in rows))},
             "by_kind_snr":{f"{k}@{s:g}":agg([r for r in rows if r["kind"]==k and r["snr_db"]==s]) for k in sorted(set(r["kind"] for r in rows)) for s in sorted(set(r["snr_db"] for r in rows if r["kind"]==k))},
             "noisy_overall":agg([r for r in rows if r["kind"]!="quiet"])}
    Path(a.out).write_text(json.dumps({"summary":summary,"rows":rows},indent=1))
    print(json.dumps(summary,indent=1)); print(f"EVAL DONE {time.time()-t0:.0f}s -> {a.out}")

if __name__=="__main__": main()

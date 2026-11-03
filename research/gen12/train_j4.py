"""Gen12: Train J4-A1 on REAL speech (LibriSpeech dev-clean subset) -- T0 only.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
NEVER a listener-benefit claim. Objective in-silico metrics only.

Data: LibriSpeech dev-clean (OpenSLR 12), CC BY 4.0.
  URL https://www.openslr.org/resources/12/dev-clean.tar.gz
  SHA256 76f87d090650617fca0cac8f88b9416e0ebf80350acb97b343a85fa903728ab3 (this download)
  Extracted subset (14 speakers, 924 flac) under /tmp/gen12dl/LibriSpeech/dev-clean
  Train target speakers (10): 84 174 251 422 652 777 1272 1462 1673 1919
  Held-out target speakers (2, eval only): 1988 1993
  Held-out interferer-only speakers (2, eval babble only): 8842 8297

Mixtures (on-the-fly, seeded): target crop + interferer at SNR -5..+10 dB.
  Interferer train: 3-talker babble (other train speakers) 70% | speech-shaped
  noise (white filtered by 1-pole LTASS-ish tilt, generated) 30%.
  10% of steps are clean/quiet (IRM=1) per candidate-J4 S4 quiet-identity term.
Target: IRM in model's own mel-envelope domain, sqrt(Eclean/(Eclean+Enoise+eps)),
  exactly as gen11/train_smoke.py (offline target, admissible S4).
Loss: mask MSE. Adam lr 2e-3, clip 5. Batch 8 x 2.0 s crops.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, time
from pathlib import Path
import numpy as np, soundfile as sf, torch, torch.nn.functional as F

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen11"))
from j4_model import EPS, FS, J4A1  # noqa: E402

DATA_ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
TRAIN_SPK = ["84","174","251","422","652","777","1272","1462","1673","1919"]
TEST_SPK = ["1988","1993"]
TEST_BABBLE_SPK = ["8842","8297"]
SEG = 2*FS

def load_pool(speakers):
    pool = {}  # speaker -> list of float32 arrays (16k mono)
    for spk in speakers:
        files = sorted((DATA_ROOT/spk).rglob("*.flac"))
        arrs=[]
        for f in files:
            x, sr = sf.read(f, dtype="float32", always_2d=False)
            assert sr==FS, (f,sr)
            if x.ndim>1: x=x[:,0]
            if len(x)>=FS: arrs.append(np.ascontiguousarray(x))
        pool[spk]=arrs
    return pool

def crop(rng, arr, n=SEG):
    if len(arr)<=n:
        out=np.zeros(n,dtype=np.float32); out[:len(arr)]=arr; return out
    s=rng.integers(0, len(arr)-n+1); return arr[s:s+n].copy()

def rms(x): return float(np.sqrt(np.mean(x.astype(np.float64)**2)+1e-12))

def ssn(rng, n=SEG):
    # speech-shaped noise proxy: white through cascaded 1-pole lowpass (tilt), generated
    w=rng.standard_normal(n).astype(np.float64)
    y=np.zeros_like(w); a=0.85
    for i in range(n): y[i]=(1-a)*w[i]+(a*y[i-1] if i else 0)
    # second stage via vectorised lfilter would need scipy; loop is 32k, acceptable in data gen? use scipy
    return y.astype(np.float32)

def make_ssn_fast(rng, n=SEG):
    from scipy.signal import lfilter
    w=rng.standard_normal(n)
    y=lfilter([0.15],[1,-0.85],w); y=lfilter([1.0],[1,-0.4],y)
    return y.astype(np.float32)

def babble(rng, pool, speakers, k=3, n=SEG):
    out=np.zeros(n,dtype=np.float64)
    for _ in range(k):
        spk=speakers[rng.integers(0,len(speakers))]
        arr=pool[spk][rng.integers(0,len(pool[spk]))]
        c=crop(rng,arr,n).astype(np.float64); out+=c/(rms(c)+1e-9)
    return (out/k).astype(np.float32)

def make_batch(rng, pool, speakers, batch=8, quiet_p=0.10):
    cleans,noises,mixs,snrs,kinds=[],[],[],[],[]
    for _ in range(batch):
        spk=speakers[rng.integers(0,len(speakers))]
        clean=crop(rng, pool[spk][rng.integers(0,len(pool[spk]))])
        # normalise target RMS to 0.1 for level stability
        clean=(clean/(rms(clean)+1e-9)*0.1).astype(np.float32)
        if rng.random()<quiet_p:
            noise=np.zeros_like(clean); snr=999.0; kind="quiet"
        else:
            snr=float(rng.uniform(-5,10))
            if rng.random()<0.70:
                others=[s for s in speakers if s!=spk]
                noise=babble(rng,pool,others); kind="babble3"
            else:
                noise=make_ssn_fast(rng); kind="ssn"
            noise=(noise/(rms(noise)+1e-9)*rms(clean)*10**(-snr/20)).astype(np.float32)
        cleans.append(clean); noises.append(noise); mixs.append(clean+noise); snrs.append(snr); kinds.append(kind)
    to=lambda a: torch.from_numpy(np.stack(a))
    return to(cleans),to(noises),to(mixs),snrs,kinds

def irm_target(model, clean, noise):
    with torch.no_grad():
        _,ec=model.extract_features(clean); _,en=model.extract_features(noise)
        Ec,En=ec**2,en**2
        return torch.sqrt(Ec/(Ec+En+EPS))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--steps",type=int,default=1500)
    ap.add_argument("--seed",type=int,default=20261103); ap.add_argument("--out",default=str(HERE/"j4a1_gen12.pt"))
    ap.add_argument("--log",default=str(HERE/"train_log.json")); a=ap.parse_args()
    torch.manual_seed(a.seed); rng=np.random.default_rng(a.seed)
    print(f"loading pool from {DATA_ROOT}",flush=True); tload=time.time()
    pool=load_pool(TRAIN_SPK)
    counts={k:len(v) for k,v in pool.items()}; total_s=sum(len(x) for v in pool.values() for x in v)/FS
    print(f"pool files={counts} total_s={total_s:.0f} load_s={time.time()-tload:.1f}",flush=True)
    model=J4A1(); opt=torch.optim.Adam(model.parameters(),lr=2e-3)
    sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,T_max=a.steps,eta_min=2e-4)
    log=[]; t0=time.time()
    for step in range(a.steps):
        clean,noise,mix,snrs,kinds=make_batch(rng,pool,TRAIN_SPK,batch=8)
        irm=irm_target(model,clean,noise)
        masks,_=model(mix); loss=F.mse_loss(masks,irm)
        opt.zero_grad(); loss.backward(); gn=torch.nn.utils.clip_grad_norm_(model.parameters(),5.0); opt.step(); sched.step()
        if step%25==0 or step==a.steps-1:
            rec={"step":step,"loss":float(loss),"grad_norm":float(gn),"lr":float(opt.param_groups[0]["lr"]),"elapsed_s":round(time.time()-t0,1)}
            log.append(rec); print(rec,flush=True)
    wall=time.time()-t0
    torch.save({"state_dict":model.state_dict(),"steps":a.steps,"seed":a.seed,
                "train_speakers":TRAIN_SPK,"data":"LibriSpeech dev-clean subset OpenSLR12 CC-BY-4.0"},a.out)
    sha=hashlib.sha256(Path(a.out).read_bytes()).hexdigest()
    meta={"steps":a.steps,"wall_s":round(wall,1),"batch":8,"seg_s":2.0,"seed":a.seed,"weights":a.out,"weights_sha256":sha,
          "pool_files":counts,"pool_total_s":round(total_s,1),"loss_first_logged":log[0]["loss"],"loss_last_logged":log[-1]["loss"],"log":log}
    Path(a.log).write_text(json.dumps(meta,indent=1))
    print(f"DONE wall={wall:.0f}s weights={a.out} sha256={sha}",flush=True)

if __name__=="__main__": main()

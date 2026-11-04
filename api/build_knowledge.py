"""Build api/build/knowledge.json: the ONLY view of the research that Muse
(Meta's model, behind /api/*) gets. Curated generation and scorecard
facts (numbers copied from the cited files) plus text chunks of the
committed record for search. Re-run after each filed verdict.

Usage: /tmp/gen9env/bin/python api/build_knowledge.py
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "api" / "build" / "knowledge.json"

SCORECARD = {  # Gen 19, 3-seed means: research/bench-n6/kpi_scorecard.py (bench_v2_gen19*.json + spatial_gen19.json)
    "source": "research/bench-n6/kpi_scorecard.py over bench_v2_gen19.json, benchv2_gen19s2.json, benchv2_gen19s3.json, spatial_gen19.json",
    "verdict": "ALL REQUIRED: FAIL - keep optimizing (13 of 14 required rows pass); promoted FALSE",
    "rows": [
        {"id": "crowd_sisdr", "name": "Crowd noise: SI-SDR improvement", "actual": "+3.51 dB", "required": ">= +3.0 dB and 95% CI lower bound > 0", "pass": True},
        {"id": "crowd_stoi", "name": "Crowd noise: STOI improvement", "actual": "+0.035", "required": ">= +0.03 and CI lower bound > 0", "pass": True},
        {"id": "crowd_ace", "name": "Crowd noise: simulated ACE electrodogram correlation improvement", "actual": "+0.072", "required": ">= +0.05 and CI lower bound > 0", "pass": True},
        {"id": "crowd_m5", "name": "Crowd noise at -5 dB SNR: SI-SDR improvement", "actual": "+1.19 dB", "required": ">= +1.5 dB", "pass": False},
        {"id": "crowd_0", "name": "Crowd noise at 0 dB SNR: SI-SDR improvement", "actual": "+4.65 dB", "required": ">= +1.5 dB", "pass": True},
        {"id": "crowd_m5_stoi", "name": "Crowd noise at -5 dB: STOI no-harm guard", "actual": "+0.005", "required": ">= 0", "pass": True},
        {"id": "crowd_every_seed", "name": "Every seed improves crowd SI-SDR", "actual": "+3.45, +3.57, +3.53 dB", "required": "> 0 in all 3 seeds", "pass": True},
        {"id": "crowd_vs_gate", "name": "Crowd SI-SDR beats a classical causal noise gate", "actual": "6.03", "required": "> 3.21 (gate)", "pass": True},
        {"id": "ssn", "name": "Speech-shaped noise: SI-SDR improvement", "actual": "+6.45 dB", "required": ">= +3.0 dB", "pass": True},
        {"id": "white", "name": "Held-out white noise: SI-SDR improvement", "actual": "+0.73 dB", "required": ">= 0 dB", "pass": True},
        {"id": "quiet_abs", "name": "Quiet speech left intact: absolute SI-SDR", "actual": "36.3 dB", "required": ">= 25 dB", "pass": True},
        {"id": "quiet_stoi", "name": "Quiet speech: STOI change", "actual": "-0.005", "required": ">= -0.02", "pass": True},
        {"id": "ild", "name": "Direction cue: target interaural level difference error (seed 17, four simulated scenes)", "actual": "5.47 dB", "required": "< 5.96 dB (unprocessed)", "pass": True},
        {"id": "itd", "name": "Direction cue: interaural time difference error (seed 17, four simulated scenes)", "actual": "4.0 samples", "required": "<= 5.8 samples (unprocessed)", "pass": True},
        {"id": "ild_distortion", "name": "ILD distortion vs the mixture (diagnostic only, not a required row)", "actual": "1.14", "required": "diagnostic only", "pass": None},
    ],
    "disclosures": [
        "Quiet PESQ and CPU streaming real-time factor are required by the KPI contract but remain unestablished.",
        "White-noise vocoded ESTOI decreases in all three seeds (mean -0.059) even though the white SI-SDR row passes.",
        "Direction-cue rows are one seed on simulated scenes; in the -5 dB scene target-ILD error worsens (10.29 -> 11.22 dB). Nothing implies a directional-hearing benefit.",
        "The Cochlear Nucleus 6's own processing was never tested, so nothing compares against it.",
    ],
}

GENERATIONS = [
    {"id": "gen16", "change": "Two auxiliary objectives added at once (1 seed, 2k steps)", "status": "null",
     "result": "Underperformed; does not establish a general zero effect for auxiliary losses.", "files": ["SUBMISSION.md"]},
    {"id": "gen17", "change": "Speaker pool 10 -> 26 (plus mixtures, SNR weighting and budget changed together)", "status": "kept",
     "result": "+0.26 dB; less disciplined generation (several changes at once).", "files": ["SUBMISSION.md"]},
    {"id": "gen18", "change": "Speaker pool 26 -> 251 (train-clean-100)", "status": "neutral",
     "result": "Roughly neutral at 6k steps.", "files": ["SUBMISSION.md"]},
    {"id": "gen19", "change": "Training budget and cosine horizon 6k -> 24k steps", "status": "baseline",
     "result": "Crowd SI-SDR +2.73 -> +3.51 dB (3-seed mean); 13 of 14 required rows pass; crowd at -5 dB +1.19 vs +1.5 required. Accepted baseline, promoted FALSE.",
     "files": ["research/gen19/results.md", "SUBMISSION.md"]},
    {"id": "gen20", "change": "Crowd-concentrated sampling (babble-k distribution), paired continuations", "status": "null",
     "result": "Failed its registered benefit criterion (B-A +0.02 dB).", "files": ["research/gen20/"]},
    {"id": "gen21", "change": "More optimization: 48k scratch (S48) vs Gen19 parent + 24k restart (R48), 3 seeds", "status": "null",
     "result": "Neither arm qualifies. -5 dB gains vs Gen19: S48 VAL +0.144 / bench -0.236; R48 VAL +0.118 / bench -0.100 (bar +0.30 on both). Overall crowd rose +3.51 -> +3.79/+3.67 but not -5 dB.",
     "files": ["research/gen21/results.md"]},
    {"id": "gen22", "change": "30 dB soft-capped SI-SDR loss (24k scratch, seed-17 screen)", "status": "fail",
     "result": "Screen FAIL: -5 dB gains vs same-seed Gen19 +0.149 dB VAL and -0.010 dB bench (bar +0.30 on both); all other screen rules passed. Clipping severity fell (median pre-clip norm 34.3 -> 14.9) but frequency did not; the gradient-imbalance hypothesis is neither falsified nor established.",
     "files": ["research/gen22/results.md", "research/gen22/astra-review-gen22-screen.md"]},
    {"id": "gen23", "change": "Plain SI-SDR + 5 x compressed multi-resolution spectral loss (24k scratch, seed-17 screen)", "status": "running",
     "result": "Screen running at the time of this build; judged on the final checkpoint only, same rules as Gen 22.",
     "files": ["research/gen23/prereg.md"]},
    {"id": "gen24", "change": "Narrower noisy-SNR sampling: 60% U(-5,-2) + 40% U(-2,10) dB, same draws (40% of noisy examples in [-5,-3] vs 17.3%)", "status": "drafted",
     "result": "Drafted and smoke-tested, not yet registered; launches only if Gen 23 fails its screen.",
     "files": ["research/gen24/prereg.md"]},
]

STORY = ("In his dad's words (shared for this site): the day Graham was born, someone was running a jackhammer right outside the hospital room, "
         "so loud his dad could feel it shaking his feet under the bed; Graham slept the whole time. For a long time all the family knew was that something was wrong; "
         "his hearing test showed he was getting almost no sound. Weeks of blood tests, urine tests, MRIs and echocardiograms, several appointments a week, "
         "and no definitive answer beyond bilateral sensorineural hearing loss. The doctors said one day he may grow to enjoy music. He does: he loves to dance. "
         "His sister is Maggie. "
         "Graham, the author's son, was born with bilateral, sensorineural, severe-to-profound hearing loss and wears "
         "bilateral Cochlear Nucleus 6 processors. Crowds are where cochlear-implant users struggle most. The author has normal hearing. "
         "This project cannot inform Graham's own care (GOAL.md section 1.1/1.4): it is literature, public-data and in-silico research only. "
         "No implant or patient was involved; the N6's processing was not tested; no candidate has earned a listening test.")

FACTS = ("Model: strictly causal Conv-TasNet-style waveform enhancer, 602,510 parameters, exact causality verified, 5.88 ms algorithmic latency (excluding compute). "
         "Bench: synthetic LibriSpeech mixtures, speaker-disjoint train/test; crowd (8-12 source draws from six interferer identities), competing talker, "
         "speech-shaped noise, held-out white noise, quiet; readouts SI-SDR, STOI, vocoded ESTOI and simulated 8-of-22 ACE electrodogram correlation; "
         "a spatial direction-cue screen on an assumed head model. Discipline: pre-registration, one change per generation, final-checkpoint-only judging, "
         "3-seed means, an independent reviewer (Codex Astra, xhigh) between generations quoted verbatim, bit-identical replay checks, nulls filed. "
         "The research loop was run by Claude (Anthropic) with Codex Astra as reviewer; Muse (Meta) powers this site's Ask and Explain features. "
         "Next steps: compressed-spectral then narrower-SNR training changes; a fresh-material confirmation package (12 new speakers); a binaural linked-gain model; "
         "measuring quiet PESQ and streaming RTF.")

CORPUS = ["SUBMISSION.md", "research/gen19/results.md", "research/gen21/results.md", "research/gen22/results.md",
          "research/gen22/prereg.md", "research/gen22/astra-review-gen22-screen.md", "research/gen23/prereg.md",
          "research/gen23/results.md", "research/gen24/prereg.md", "research/bench-n6/KPI.md",
          "research/gen21/astra-review-gen21-final.md", "research/gen23/astra-code-audit.md"]


def chunks(path):
    text = (ROOT / path).read_text(encoding="utf-8")
    parts = re.split(r"\n(?=#{1,3} )", text)
    for p in parts:
        p = p.strip()
        head = p.splitlines()[0].lstrip("# ").strip() if p else ""
        for i in range(0, len(p), 1400):
            seg = p[i:i + 1400].strip()
            if len(seg) > 80:
                yield {"file": path, "heading": head, "text": seg}


def goal_story():
    g = (ROOT / "GOAL.md").read_text(encoding="utf-8")
    s = g[g.index("### 1.1"):g.index("### 1.2")]
    return {"file": "GOAL.md", "heading": "1.1 Motivation and conflict disclosure", "text": s.strip()[:1400]}


def site_generations():
    """Single source of truth: the site's generations.json (edited after each verdict)."""
    f = ROOT / "site" / "data" / "generations.json"
    if not f.exists():
        return GENERATIONS
    g = json.loads(f.read_text())
    return g if isinstance(g, list) else g.get("generations", GENERATIONS)


def main():
    docs = [c for f in CORPUS if (ROOT / f).exists() for c in chunks(f)] + [goal_story()]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"story": STORY, "facts": FACTS, "scorecard": SCORECARD, "generations": site_generations(),
                               "docs": docs, "repo": "https://github.com/bmarti44/meta-hackathon-deaf-hard-of-hearing"}, indent=0))
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB, {len(docs)} chunks)")


if __name__ == "__main__":
    main()

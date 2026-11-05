"""Independent review of the Meta listening check by Muse Wonder (muse-wonder-1.0), filed verbatim.
Run after listen_wer.py: /tmp/gen9env/bin/python research/meta/wonder_review.py [--effort high]
Direct-invokes the beforetheimplant-muse Lambda (mode "wonder"); the API key never leaves AWS.
"""
import argparse, json, subprocess, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "max"])
    a = ap.parse_args()
    plan = (HERE / "plan.md").read_text()
    res = json.loads((HERE / "results.json").read_text())
    rows = [{k: r[k] for k in ["cond", "uid", "snr_db", "wer", "attempts", "ref", "hyp"]} for r in res["rows"]]
    prompt = (
        "Review this exploratory check. The plan was written before results. Then the results, with every transcript.\n\n"
        "Answer in Markdown, under 450 words:\n"
        "1. Recompute the mean WER per condition and SNR from the rows and say whether the summary matches.\n"
        "2. What does the evidence support, and how strongly (n = 12 per SNR)?\n"
        "3. Threats to validity: the recognizer is an LLM with audio input (Muse Spark), not a dedicated ASR; "
        "it is nondeterministic and sometimes replies as if no audio were attached (retried); one transcription per clip; "
        "insertions of crowd words; WER normalization. Which of these could flip the conclusion?\n"
        "4. One concrete next step.\n"
        "Do not claim any benefit for a real listener or a cochlear-implant user.\n\n"
        f"## PLAN\n{plan}\n\n## SUMMARY\n{json.dumps(res['summary'], indent=1)}\n\n## META\n{json.dumps(res['meta'])}\n\n"
        f"## ROWS\n{json.dumps(rows)}"
    )
    with tempfile.TemporaryDirectory() as td:
        ev, out = Path(td) / "ev.json", Path(td) / "out.json"
        ev.write_text(json.dumps({"mode": "wonder", "effort": a.effort, "prompt": prompt}))
        subprocess.run(["aws", "lambda", "invoke", "--function-name", "beforetheimplant-muse", "--cli-binary-format",
                        "raw-in-base64-out", "--cli-read-timeout", "310", "--payload", f"file://{ev}", str(out)], check=True,
                       capture_output=True)
        d = json.loads(out.read_text())
    (HERE / "wonder_review.md").write_text(
        f"# Muse Wonder review of the Meta listening check (verbatim)\n\n"
        f"Model `{d.get('model')}`, reasoning effort `{d.get('effort')}`, response status `{d.get('status')}`, "
        f"{time.strftime('%Y-%m-%d %H:%M %Z')}. Prompt built by `research/meta/wonder_review.py` from `plan.md` and "
        f"`results.json` (all rows and transcripts). Filed unedited.\n\n---\n\n{d.get('text') or d}\n")
    print((HERE / "wonder_review.md").read_text())


if __name__ == "__main__":
    main()

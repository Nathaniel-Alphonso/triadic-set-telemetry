#!/usr/bin/env python3
"""triadic_rejudge.py -- Re-execute HumanEval generations from a Triadic dump.

WHY: acd-lim20 doc 7 ('filter_by_substring') carried a FAIL verdict on a
generation that is byte-identical to the one that PASSED in he-base164b and
he-tri164b, and the code provably satisfies every assert in its target.
The executor is therefore flaky at some rate (disk squeeze / sandbox race /
timeout), and a ~3-5% verdict-flake rate would contaminate the 164-doc
attribution: the -0.030 could be part real tier damage, part judge noise.

This script does NOT touch the evaluator. It post-processes dump files:

  1. Rebuilds each full program as: canonical HumanEval prompt + generated
     completion + target harness (the `check(candidate)` block in the dump).
  2. Executes each program in a FRESH subprocess with a hard timeout and
     its own temp dir (no shared state between docs, no disk residue).
  3. Recomputes pass@1 per doc, reports:
       - rows where the original verdict and the re-judged verdict differ
       - rows that flake ACROSS re-judge repetitions (executed 3x each;
         a program that passes 2/3 or 3/3 is judged PASS, else FAIL --
         deterministic programs always agree; this only smooths env flakes)
  4. Optionally compares two re-judged dumps (verdict flips between them).

The canonical prompt is recovered from the doc_id via the openai_humaneval
dataset (task_id == HumanEval/<doc_id>). The dump's prompt_head is
TRUNCATED by design -- never use it for execution.

Usage:
    python triadic_rejudge.py triadic_generations_humaneval_acd-lim20.json
    python triadic_rejudge.py dumpA.json dumpB.json        # + flip table
    python triadic_rejudge.py --reps 1 dump.json           # skip 3x smoothing

Output: prints a table, writes <dump>.rejudged.json with the new verdicts.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import multiprocessing as mp

TIMEOUT_SEC = 10
REPS = 3


def load_canonical_prompts():
    """doc_id -> canonical HumanEval prompt (the raw completion-style prompt
    the evaluator used with apply_chat_template=False)."""
    try:
        # v1.1: openai_humaneval now lives under the 'openai/' namespace.
        # Try the canonical repo id first; fall back to the legacy name so
        # an older datasets-cache still works.
        from datasets import load_dataset
        prompts = {}
        for repo in ("openai/openai_humaneval", "openai_humaneval"):
            try:
                ds = load_dataset(repo, split="test")
                break
            except Exception as e:
                last_err = e
        else:
            raise last_err
        for row in ds:
            task_num = int(row["task_id"].split("/")[1])
            prompts[task_num] = row["prompt"]
        return prompts
    except Exception as e:
        sys.exit(
            "Could not load openai_humaneval dataset: %r\n"
            "The evaluator already pulls this dataset (same source), so a "
            "successful eval run implies this import should work. Check the "
            "datasets cache or network." % e
        )


def run_program_once(program_text, workdir):
    """Execute one program in a subprocess. Returns True/False."""
    path = os.path.join(workdir, "prog.py")
    with open(path, "w") as f:
        f.write(program_text)
    try:
        proc = subprocess.run(
            [sys.executable, "prog.py"],
            cwd=workdir,
            capture_output=True,
            timeout=TIMEOUT_SEC,
        )
        return proc.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except OSError:
        return False


def judge(doc, canonical_prompt, reps):
    """Re-judge one doc `reps` times in isolated temp dirs. Returns
    (verdict_bool, passes, reps)."""
    program = canonical_prompt + doc["generated"] + "\n\n" + doc["target"]
    passes = 0
    for _ in range(reps):
        # Fresh temp dir per rep: no state reuse, no residue.
        with tempfile.TemporaryDirectory(prefix="rejudge-") as td:
            if run_program_once(program, td):
                passes += 1
    verdict = passes >= (reps // 2 + 1)  # majority: 2/3 or 3/3 -> PASS
    return verdict, passes, reps


def main():
    ap = argparse.ArgumentParser(description="Re-judge HumanEval generation dumps.")
    ap.add_argument("dumps", nargs="+", help="one or two generation dump JSONs")
    ap.add_argument("--reps", type=int, default=REPS,
                    help="executions per doc (default 3, majority vote)")
    args = ap.parse_args()
    if len(args.dumps) > 2:
        ap.error("at most two dumps (second triggers flip comparison)")

    prompts = load_canonical_prompts()

    results = {}
    for dump_path in args.dumps:
        with open(dump_path) as f:
            docs = json.load(f)
        tag = os.path.basename(dump_path)
        print(f"\n=== Re-judging {tag} ({len(docs)} docs, {args.reps} reps each) ===")
        verdicts = {}
        changed = []
        for doc in docs:
            did = doc["doc_id"]
            original = float(doc.get("pass@1") or 0.0)
            verdict, passes, reps = judge(doc, prompts[did], args.reps)
            verdicts[did] = verdict
            if verdict != (original == 1.0):
                changed.append((did, original, verdict, passes, reps))
        acc = sum(verdicts.values()) / len(docs)
        print(f"  original acc: {sum(1 for d in docs if float(d.get('pass@1') or 0)==1.0)}/{len(docs)}")
        print(f"  re-judged acc: {sum(verdicts.values())}/{len(docs)}  ({acc:.3f})")
        if changed:
            print(f"  VERDICT CHANGES ({len(changed)}):")
            for did, orig, verdict, p, r in sorted(changed):
                arrow = "FAIL->PASS" if verdict else "PASS->FAIL"
                print(f"    doc {did:3d}: {arrow}  ({p}/{r} reps passed)")
        else:
            print("  no verdict changes (all original verdicts confirmed)")
        out_path = dump_path.rsplit(".", 1)[0] + ".rejudged.json"
        with open(out_path, "w") as f:
            json.dump({str(k): bool(v) for k, v in verdicts.items()}, f, indent=1)
        print(f"  wrote {out_path}")
        results[tag] = verdicts

    if len(results) == 2:
        a_tag, b_tag = args.dumps
        with open(a_tag) as f:
            a_docs = {d["doc_id"]: d for d in json.load(f)}
        with open(b_tag) as f:
            b_docs = {d["doc_id"]: d for d in json.load(f)}
        print(f"\n=== Flip table (re-judged): {os.path.basename(a_tag)} vs {os.path.basename(b_tag)} ===")
        common = sorted(set(a_docs) & set(b_docs))
        lost = [d for d in common if results[a_tag][d] and not results[b_tag][d]]
        gained = [d for d in common if not results[a_tag][d] and results[b_tag][d]]
        both_p = sum(1 for d in common if results[a_tag][d] and results[b_tag][d])
        both_f = sum(1 for d in common if not results[a_tag][d] and not results[b_tag][d])
        print(f"  common docs: {len(common)}  both-pass: {both_p}  both-fail: {both_f}")
        print(f"  lost   ({len(lost)}): {lost}")
        print(f"  gained ({len(gained)}): {gained}")
        if not lost and not gained:
            print("  CLEAN PARITY under re-judge.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""rw17_code_builder_acceptance_run.py -- the acceptance suite for
build_rw17_code_corpus.py (the pinned code build spec + the OPTION-A
pool ruling, items 247(a)/248(a)). Every check is an INDEPENDENT
recomputation or a hard-exit probe. Fixture-mode lane: zero-GPU, no
dataset access; the fake he164 reference exercises the disjointness
receipt mechanics.
"""
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = os.path.join(HERE, "build_rw17_code_corpus.py")
SEED = 20261013
PASS, FAIL = 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS  %s" % name)
    else:
        FAIL += 1
        print("  FAIL  %s %s" % (name, detail))


def run_builder(out_path, he_path, expect_ok=True):
    r = subprocess.run([sys.executable, BUILDER, "--fixture-mode",
                        "--out", out_path, "--he-canonical", he_path],
                       capture_output=True, text=True)
    if expect_ok and r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit("builder run failed unexpectedly")
    return r


def main():
    tmp = tempfile.mkdtemp()
    he_empty = os.path.join(tmp, "he_empty.json")
    with open(he_empty, "w") as f:
        json.dump({"docs": {"0": {"prompt": "def walked_he_prompt(x):\n    "
                                        "return x\n"}}, "n": 1}, f)

    # ---- F1 determinism: same-path rerun byte-identical --------------------
    out = os.path.join(tmp, "c.json")
    run_builder(out, he_empty)
    snap1 = open(out, "rb").read()
    run_builder(out, he_empty)
    snap2 = open(out, "rb").read()
    check("F1a determinism: same-path rebuild byte-identical", snap1 == snap2)
    m = json.loads(snap1)
    sha1 = hashlib.sha256(snap1).hexdigest()

    # ---- F2 the selection rule: independent recomputation ------------------
    spec = importlib.util.spec_from_file_location("m", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pool_ids = sorted(int(r["task_id"]) for r in mod.FIX_POOL)
    eligible = [t for t in pool_ids if t not in set(range(1, 11))]
    perm = list(eligible)
    random.Random(SEED).shuffle(perm)
    chosen = sorted(perm[:8])
    got = [d["task_id"] for d in
           (m["docs"][str(k)] for k in range(len(m["docs"])))]
    check("F2a selection: seeded shuffle + first-8 + task_id order matches "
          "the independent recomputation", got == chosen)
    check("F2b OPTION A: no task_id 1..10 in the selection",
          all(t >= 11 for t in got))
    check("F2c design.seed == pinned 20261013", m["design"]["seed"] == SEED)
    check("F2d design.pool_ruling == OPTION A", "OPTION A" in
          m["design"]["pool_ruling"])

    # ---- F3 scale + ids + schema --------------------------------------------
    docs = m["docs"]
    check("F3a scale: 8 fixture docs", len(docs) == 8)
    check("F3b ids contiguous 0..7",
          sorted(int(k) for k in docs) == list(range(8)))
    check("F3c schema field == mbpp-rw17-v1", m["schema"] == "mbpp-rw17-v1")
    need = ("doc_id", "task_id", "text", "test_list", "test_setup_code",
            "code", "prompt")
    check("F3d every doc carries the 7 pinned fields",
          all(set(need) <= set(d) for d in docs.values()))

    # ---- F4 the prompt-form construction (pinned; the loader asserts it) ----
    ok = True
    for d in docs.values():
        want = "%s Your code should pass these tests:\n\n%s" % (
            d["text"], "\n".join(d["test_list"]))
        if d["prompt"] != want:
            ok = False
    check("F4a prompt == the pinned construction from text + test_list", ok)
    check("F4b the canonical code never appears in any prompt",
          all(d["code"].splitlines()[0] not in d["prompt"]
              for d in docs.values()))

    # ---- F5 the hard exits fire loud -----------------------------------------
    # F5a missing he164 reference file -> VOID
    r = subprocess.run([sys.executable, BUILDER, "--fixture-mode",
                        "--out", os.path.join(tmp, "x.json"),
                        "--he-canonical",
                        os.path.join(tmp, "NOPE.json")],
                       capture_output=True, text=True)
    check("F5a missing he-reference hard exit (VOID, named)",
          r.returncode != 0 and "disjointness receipt cannot run" in
          r.stdout + r.stderr)

    # F5b a walked-he collision -> VOID (the disjointness law)
    d0 = m["docs"]["0"]
    he_coll = os.path.join(tmp, "he_coll.json")
    with open(he_coll, "w") as f:
        json.dump({"docs": {"0": {"prompt": d0["prompt"]}}}, f)
    r = run_builder(os.path.join(tmp, "coll.json"), he_coll, expect_ok=False)
    check("F5b he164-collision hard exit (VOID, the disjointness law named)",
          r.returncode != 0 and "collides with a walked he164" in
          r.stdout + r.stderr)

    # F5c a duplicate prompt inside the pool -> VOID
    src = open(BUILDER).read()
    dup_src = src.replace(
        '     "text": "Task %d: write a function that returns the %s of two '
        'integers."\n'
        '             % (t, ["sum", "difference", "product", "maximum"][t % 4]),',
        '     "text": "Task: write a function that returns the sum of two '
        'integers.",')
    dup_src = dup_src.replace(
        '     "code": "def f(a, b):\\n    return a %s b\\n" %\n'
        '             ["+", "-", "*", "max(a, b)"][t % 4],',
        '     "code": "def f(a, b):\\n    return a + b\\n",')
    dup_src = dup_src.replace(
        '     "test_list": ["assert f(2, 3) == %d" % (2 + t),\n'
        '                   "assert f(0, 0) == 0",\n'
        '                   "assert f(-1, 1) == %d" % t],',
        '     "test_list": ["assert f(2, 3) == 5",\n'
        '                   "assert f(0, 0) == 0",\n'
        '                   "assert f(-1, 1) == 0"],')
    dup_path = os.path.join(tmp, "dup_builder.py")
    open(dup_path, "w").write(dup_src)
    r = subprocess.run([sys.executable, dup_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "dup.json"),
                        "--he-canonical", he_empty],
                       capture_output=True, text=True)
    check("F5c duplicate-prompt hard exit (VOID, named)",
          r.returncode != 0 and "duplicate prompt" in r.stdout + r.stderr)

    # ---- F6 the receipts echo on the console ---------------------------------
    r = run_builder(out, he_empty)
    o = r.stdout
    check("F6a console carries the OPTION-A pool receipt",
          "OPTION-A pool" in o and "task_ids 1..10" in o)
    check("F6b console carries the seed + scale + sha receipts",
          "seed: 20261013" in o and "sha256:" in o)
    check("F6c console carries the disjointness receipt",
          "disjointness receipt: PASS" in o)

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    print("CODE BUILDER ACCEPTANCE: %d PASS / %d FAIL" % (PASS, FAIL))
    print("(fixture-mode lane; the REAL build runs on my side per the "
          "pinned spec; its console + manifest get receipt-verified on "
          "upload)")
    print("(fixture manifest sha256: %s)" % sha1)
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()

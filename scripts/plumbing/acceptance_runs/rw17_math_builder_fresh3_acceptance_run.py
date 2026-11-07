#!/usr/bin/env python3
"""rw17_math_builder_fresh3_acceptance_run.py -- the acceptance suite for
build_rw17_math_corpus_fresh3.py (my STAMPED fresh3 math build spec,
ledger item 263(e)(1), stamped at item 266). Every check is an INDEPENDENT
recomputation or a hard-exit probe -- never a call into the builder's own
selection code (except the builder runs themselves, whose outputs are then
verified independently). Fixture-mode lane: zero-GPU, no dataset access.
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
BUILDER = os.path.join(HERE, "build_rw17_math_corpus_fresh3.py")
SEED = 20261016
SPEC_SHA = ("3d543876ecb080809adb42e190581ce1f8c973c826242a6fd2283a297"
            "64143f1")

PASS, FAIL = 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS  %s" % name)
    else:
        FAIL += 1
        print("  FAIL  %s %s" % (name, detail))


def run_builder(out_path, expect_fail=False):
    r = subprocess.run([sys.executable, BUILDER, "--fixture-mode",
                        "--out", out_path], capture_output=True, text=True)
    if expect_fail:
        return r
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        sys.exit("builder run failed unexpectedly")
    return r


def load_spec():
    spec = importlib.util.spec_from_file_location("m", BUILDER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    tmp = tempfile.mkdtemp()

    # ---- F1 determinism: same-path rerun byte-identical -------------------
    a = os.path.join(tmp, "a.json")
    run_builder(a)
    snap1 = open(a, "rb").read()
    run_builder(a)
    snap2 = open(a, "rb").read()
    ba = snap1
    check("F1a determinism: same-path rebuild byte-identical", snap1 == snap2)
    sha_a = hashlib.sha256(ba).hexdigest()
    m = json.loads(ba)

    # ---- F2 the selection rule: independent recomputation -----------------
    mod = load_spec()
    fix_train = mod.FIX_TRAIN
    excluded = set(range(5))
    fresh1_fix_idx = set()          # re-derived from the fixture fresh1 bytes
    fresh1_qs = [d["question"] for d in mod.FIX_FRESH1_DOCS.values()]
    for i, r in enumerate(fix_train):
        if r["question"] in fresh1_qs:
            fresh1_fix_idx.add(i)
    eligible = [i for i in range(len(fix_train))
               if i not in excluded and i not in fresh1_fix_idx]
    perm = list(eligible)
    random.Random(SEED).shuffle(perm)
    chosen = sorted(perm[:6])
    got = [d["question"] for d in
           (m["docs"][str(k)] for k in range(len(m["docs"])))]
    want = [fix_train[i]["question"] for i in chosen]
    check("F2a selection: seeded shuffle + first-N + original-index order "
          "matches the independent recomputation", got == want,
          "got %r want %r" % (got[:2], want[:2]))
    check("F2b no prefix rows selected",
          all(not q.startswith("Prefix row") for q in got))
    check("F2c the fresh1 subtraction exercised (its fixture index absent)",
          5 not in chosen and len(fresh1_fix_idx) == 1)
    check("F2d design.seed == pinned 20261016", m["design"]["seed"] == SEED)

    # ---- F3 scale + ids + schema ------------------------------------------
    docs = m["docs"]
    check("F3a scale: 6 fixture docs", len(docs) == 6)
    check("F3b ids contiguous 0..5",
          sorted(int(k) for k in docs) == list(range(6)))
    check("F3c schema field == gsm8k-rw17-v1 (UNCHANGED)",
          m["schema"] == "gsm8k-rw17-v1")
    ok_fields = all(set(("doc_id", "question", "answer")) <= set(d)
                    and isinstance(d["doc_id"], int)
                    and d["question"] and d["answer"] for d in docs.values())
    check("F3d every doc carries doc_id/question/answer, non-empty", ok_fields)

    # ---- F4 the gold discipline: answer == #### segment -------------------
    ok_gold = all(d["answer"] == mod.FIX_TRAIN[chosen[i]]["answer"]
                  .split("####")[-1].strip() for i, d in
                  ((i, docs[str(i)]) for i in range(6)))
    check("F4 gold discipline (#### segment, banked law)", ok_gold)

    # ---- F5 the hard exits fire loud ---------------------------------------
    src = open(BUILDER).read()
    # the probe anchor: the fixture comprehension's tail (a SINGLE-ROW
    # append keeps the fresh1 fixture question unique -- the first draft
    # replaced the whole comprehension, colliding with the fresh1 fixture
    # question and VOIDing on the correct, louder ambiguity guard instead
    # of the intended exit; checker-side fix, the tool zero-defect)
    anchor = ('    for i in range(5, 12)\n'
              ']\n')

    # F5a duplicate question inside the pool -> builder must VOID
    dup_line = ('    for i in range(5, 11)\n'
                '] + [\n'
                '    {"question": "Train problem 6: a shuttle makes 8 trips '
                'carrying 9 crates each; how many crates total?",\n'
                '     "answer": "reasoning #### 54"}\n'
                ']\n')
    src2 = src.replace(anchor, dup_line)
    mod2_path = os.path.join(tmp, "dup_builder.py")
    open(mod2_path, "w").write(src2)
    r = subprocess.run([sys.executable, mod2_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "dup.json")],
                       capture_output=True, text=True)
    check("F5a duplicate question hard exit (VOID, named)",
          r.returncode != 0 and "duplicate question" in r.stdout + r.stderr)

    # F5b TEST-collision question -> builder must VOID (disjointness law)
    coll_line = ('    for i in range(5, 11)\n'
                 '] + [\n'
                 '    {"question": "Test problem 2: distinct walked test '
                 'question 2.",\n'
                 '     "answer": "reasoning #### 70"}\n'
                 ']\n')
    src3 = src.replace(anchor, coll_line)
    mod3_path = os.path.join(tmp, "coll_builder.py")
    open(mod3_path, "w").write(src3)
    r = subprocess.run([sys.executable, mod3_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "coll.json")],
                       capture_output=True, text=True)
    check("F5b TEST-collision hard exit (VOID, the disjointness law named)",
          r.returncode != 0 and "collides with the walked TEST split" in
          r.stdout + r.stderr)

    # F5c a fresh1 question with NO match in the pool -> VOID (the
    # never-guess-a-key subtraction law)
    nomatch_src = src.replace(
        '"question": FIX_TRAIN[5]["question"],',
        '"question": "A question that exists nowhere in the pool.",')
    mod4_path = os.path.join(tmp, "nomatch_builder.py")
    open(mod4_path, "w").write(nomatch_src)
    r = subprocess.run([sys.executable, mod4_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "nomatch.json")],
                       capture_output=True, text=True)
    check("F5c fresh1 no-match hard exit (VOID, the subtraction law named)",
          r.returncode != 0 and "NO match in the TRAIN pool" in
          r.stdout + r.stderr)

    # ---- F6 the receipts echo on the console -------------------------------
    r = run_builder(os.path.join(tmp, "c.json"))
    out = r.stdout
    check("F6a console carries the contamination-guard receipt",
          "contamination guard" in out and "excluded train[0]" in out)
    check("F6b console carries the fresh3 subtraction receipt",
          "fresh3 subtraction" in out and
          ("SHA-256 pin verified" in out or "FIXTURE fresh1 world" in out))
    check("F6c console carries the pool receipts line",
          "pool receipts:" in out and "eligible" in out)
    check("F6d console carries the seed + sha receipts",
          "seed: 20261016" in out and "sha256:" in out)
    check("F6e console carries the disjointness receipt + the schema + tag",
          "disjointness receipt: PASS" in out
          and "gsm8k-rw17-v1" in out and "rw17-math-fresh3" in out)

    # ---- F7 the design block pins ------------------------------------------
    d = m["design"]
    check("F7a design.spec_sha256 == the stamped fresh3 sheet pin",
          d.get("spec_sha256") == SPEC_SHA)
    check("F7b design.walk_tag == rw17-math-fresh3",
          d.get("walk_tag") == "rw17-math-fresh3")
    check("F7c design names the fork base + the fresh1 subtraction law",
          "142c7a51922a89e99318bab5fb4fbdae1f7515cc3b74f227fdf4211c85559663"
          in d.get("fork_base", "") and
          "DEVELOPMENT DATA" in d.get("fresh1_subtraction", ""))
    check("F7d design carries the parity law (EVEN=calibration)",
          "EVEN = calibration" in d.get("parity", ""))

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    print("MATH FRESH3 BUILDER ACCEPTANCE: %d PASS / %d FAIL" % (PASS, FAIL))
    print("(fixture-mode lane; the REAL build runs on my side per the stamped "
          "spec; its console + manifest get receipt-verified on upload)")
    print("(fixture manifest sha256: %s)" % sha_a)
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()

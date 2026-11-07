#!/usr/bin/env python3
"""rw17_math_builder_acceptance_run.py -- the acceptance suite for
build_rw17_math_corpus.py (the pinned math build spec, item 248(a)).
Every check is an INDEPENDENT recomputation or a hard-exit probe --
never a call into the builder's own selection code (except the builder
runs themselves, whose outputs are then verified independently).
Fixture-mode lane: zero-GPU, no dataset access.
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
BUILDER = os.path.join(HERE, "build_rw17_math_corpus.py")
SEED = 20261012

PASS, FAIL = 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS  %s" % name)
    else:
        FAIL += 1
        print("  FAIL  %s %s" % (name, detail))


def run_builder(out_path, extra_env=None, expect_fail=False):
    r = subprocess.run([sys.executable, BUILDER, "--fixture-mode",
                        "--out", out_path],
                       capture_output=True, text=True, env=extra_env)
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

    # ---- F1 determinism: same-path rerun byte-identical (the item-242
    # F6 precedent -- the honest export-path echo preserved) ---------------
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
    eligible = [i for i in range(len(fix_train)) if i not in excluded]
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
    check("F2c design.seed == pinned 20261012", m["design"]["seed"] == SEED)

    # ---- F3 scale + ids + schema ------------------------------------------
    docs = m["docs"]
    check("F3a scale: 6 fixture docs", len(docs) == 6)
    check("F3b ids contiguous 0..5",
          sorted(int(k) for k in docs) == list(range(6)))
    check("F3c schema field == gsm8k-rw17-v1", m["schema"] == "gsm8k-rw17-v1")
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
    # F5a duplicate question inside the pool -> builder must VOID
    mod2_path = os.path.join(tmp, "dup_builder.py")
    src = open(BUILDER).read()
    dup_line = ('    {"question": "Train problem X: a shuttle makes 7 trips '
                'carrying 8 crates each; how many crates total?",')
    src2 = src.replace(
        '    {"question": "Train problem %d: a shuttle makes %d trips carrying %d crates each; how many crates total?" % (i, i + 2, i + 3),',
        dup_line)
    open(mod2_path, "w").write(src2)
    r = subprocess.run([sys.executable, mod2_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "dup.json")],
                       capture_output=True, text=True)
    check("F5a duplicate question hard exit (VOID, named)",
          r.returncode != 0 and "duplicate question" in r.stdout + r.stderr)

    # F5b TEST-collision question -> builder must VOID (disjointness law)
    coll_line = ('    {"question": "Test problem 2: distinct walked test '
                 'question 2.",')
    src3 = src.replace(
        '    {"question": "Train problem %d: a shuttle makes %d trips carrying %d crates each; how many crates total?" % (i, i + 2, i + 3),',
        coll_line)
    mod3_path = os.path.join(tmp, "coll_builder.py")
    open(mod3_path, "w").write(src3)
    r = subprocess.run([sys.executable, mod3_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "coll.json")],
                       capture_output=True, text=True)
    check("F5b TEST-collision hard exit (VOID, the disjointness law named)",
          r.returncode != 0 and "collides with the walked TEST split" in
          r.stdout + r.stderr)

    # ---- F6 the receipts echo on the console --------------------------------
    r = run_builder(os.path.join(tmp, "c.json"))
    out = r.stdout
    check("F6a console carries the contamination-guard receipt",
          "contamination guard" in out and "excluded train[0]" in out)
    check("F6b console carries the seed + scale + sha receipts",
          "seed: 20261012" in out and "sha256:" in out)
    check("F6c console carries the disjointness receipt",
          "disjointness receipt: PASS" in out)

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    print("MATH BUILDER ACCEPTANCE: %d PASS / %d FAIL" % (PASS, FAIL))
    print("(fixture-mode lane; the REAL build runs owner-side per the pinned "
          "spec; its console + manifest get receipt-verified on upload)")
    print("(fixture manifest sha256: %s)" % sha_a)
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()

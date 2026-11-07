#!/usr/bin/env python3
"""rw17_code_builder_fresh3_acceptance_run.py -- the acceptance suite for
build_rw17_code_corpus_fresh3.py (the OWNER-STAMPED fresh3 code build spec,
ledger item 263(e)(2), stamped at item 266). Every check is an INDEPENDENT
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
BUILDER = os.path.join(HERE, "build_rw17_code_corpus_fresh3.py")
SEED = 20261017
SPEC_SHA = ("8d7acd2a542476c67517f52c9b075b3283475aec8952d570d543504e9"
            "8816413")

PASS, FAIL = 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS  %s" % name)
    else:
        FAIL += 1
        print("  FAIL  %s %s" % (name, detail))


def run_builder(out_path, extra=None, expect_fail=False):
    cmd = [sys.executable, BUILDER, "--fixture-mode", "--out", out_path]
    if extra:
        cmd += extra
    r = subprocess.run(cmd, capture_output=True, text=True)
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


def make_prompt(text, test_list):
    """The pinned prompt form, recomputed independently here."""
    return "%s Your code should pass these tests:\n\n%s" % (
        text, "\n".join(test_list))


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
    fresh1_tids = set(d["task_id"] for d in mod.FIX_FRESH1_DOCS.values())
    eligible = [t for t in range(11, 31) if t not in fresh1_tids]
    perm = list(eligible)
    random.Random(SEED).shuffle(perm)
    chosen = sorted(perm[:8])
    got_tids = [m["docs"][str(k)]["task_id"] for k in range(len(m["docs"]))]
    check("F2a selection: seeded shuffle + first-N + task_id-ascending "
          "order matches the independent recomputation",
          got_tids == chosen, "got %r want %r" % (got_tids, chosen))
    check("F2b the fresh1 subtraction exercised (its fixture ids absent)",
          not (set(got_tids) & fresh1_tids) and len(fresh1_tids) == 12)
    check("F2c no few-shot prompt tasks selected",
          all(t >= 11 for t in got_tids))
    check("F2d design.seed == pinned 20261017", m["design"]["seed"] == SEED)

    # ---- F3 scale + ids + schema + fields ----------------------------------
    docs = m["docs"]
    check("F3a scale: 8 fixture docs", len(docs) == 8)
    check("F3b ids contiguous 0..7",
          sorted(int(k) for k in docs) == list(range(8)))
    check("F3c schema field == mbpp-rw17-v1 (UNCHANGED)",
          m["schema"] == "mbpp-rw17-v1")
    need = ("doc_id", "task_id", "text", "test_list", "test_setup_code",
            "code", "prompt")
    ok_fields = all(set(need) <= set(d) and isinstance(d["doc_id"], int)
                    and d["text"] and d["test_list"] and d["prompt"]
                    for d in docs.values())
    check("F3d every doc carries the vehicle-pinned fields, non-empty",
          ok_fields)

    # ---- F4 the prompt form byte-exact per doc (independent recompute) ----
    fix_pool = {r["task_id"]: r for r in mod.FIX_POOL}
    ok_prompt = all(
        docs[str(i)]["prompt"] == make_prompt(fix_pool[t]["text"],
                                             fix_pool[t]["test_list"])
        for i, t in enumerate(chosen))
    check("F4 the pinned prompt form byte-exact on every doc", ok_prompt)

    # ---- F5 the hard exits fire loud ---------------------------------------
    src = open(BUILDER).read()

    # F5a duplicate task_id in the pool -> builder must VOID
    dup_src = src.replace(
        "    for t in range(1, 31)        # task_ids 1..30; 1..10 excluded "
        "(prompt tasks)\n",
        "    for t in list(range(1, 30)) + [12]  # probe: task_id 12 twice\n")
    mod2_path = os.path.join(tmp, "dup_builder.py")
    open(mod2_path, "w").write(dup_src)
    r = subprocess.run([sys.executable, mod2_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "dup.json")],
                       capture_output=True, text=True)
    check("F5a duplicate task_id hard exit (VOID, named)",
          r.returncode != 0 and "duplicate task_id" in r.stdout + r.stderr)

    # F5b he164 collision -> builder must VOID (the disjointness law)
    coll_tid = chosen[0]
    coll_prompt = make_prompt(fix_pool[coll_tid]["text"],
                              fix_pool[coll_tid]["test_list"])
    he_path = os.path.join(tmp, "he_canon.json")
    json.dump({"docs": {"0": {"prompt": coll_prompt}}},
              open(he_path, "w"))
    r = run_builder(os.path.join(tmp, "coll.json"),
                    extra=["--he-canonical", he_path], expect_fail=True)
    check("F5b he164-collision hard exit (VOID, the disjointness law named)",
          r.returncode != 0 and "collides with a walked he164" in
          r.stdout + r.stderr)

    # F5c a fresh1 task_id absent from the pool -> VOID (the never-guess law)
    nomatch_src = src.replace(
        "    for i, tid in enumerate([11, 13, 15, 17, 19, 21, 23, 25, 27, "
        "28, 29, 30])\n",
        "    for i, tid in enumerate([11, 13, 15, 17, 19, 21, 23, 25, 27, "
        "28, 29, 99])\n")
    mod3_path = os.path.join(tmp, "nomatch_builder.py")
    open(mod3_path, "w").write(nomatch_src)
    r = subprocess.run([sys.executable, mod3_path, "--fixture-mode",
                        "--out", os.path.join(tmp, "nomatch.json")],
                       capture_output=True, text=True)
    check("F5c fresh1-absent-task hard exit (VOID, the subtraction law "
          "named)", r.returncode != 0 and "absent from the pool" in
          r.stdout + r.stderr)

    # ---- F6 the receipts echo on the console -------------------------------
    r = run_builder(os.path.join(tmp, "c.json"))
    out = r.stdout
    check("F6a console carries the OPTION-A pool receipt",
          "OPTION-A pool:" in out and "few-shot prompt tasks" in out)
    check("F6b console carries the fresh3 subtraction receipt",
          "fresh3 subtraction" in out and
          ("SHA-256 pin verified" in out or "FIXTURE fresh1 world" in out))
    check("F6c console carries the pool receipts line",
          "pool receipts:" in out and "eligible" in out)
    check("F6d console carries the seed + sha receipts",
          "seed: 20261017" in out and "sha256:" in out)
    check("F6e console carries the disjointness receipt + schema + tag",
          "disjointness receipt: PASS" in out
          and "mbpp-rw17-v1" in out and "rw17-code-fresh3" in out)

    # ---- F7 the design block pins ------------------------------------------
    d = m["design"]
    check("F7a design.spec_sha256 == the stamped fresh3 sheet pin",
          d.get("spec_sha256") == SPEC_SHA)
    check("F7b design.walk_tag == rw17-code-fresh3",
          d.get("walk_tag") == "rw17-code-fresh3")
    check("F7c design names the fork base + the fresh1 subtraction law",
          "edca0f882b46cd60d01cce321b1a8b56d95639f171d42b124f62e483f3786e6c"
          in d.get("fork_base", "") and
          "DEVELOPMENT DATA" in d.get("fresh1_subtraction", ""))
    check("F7d design carries the census discipline (rides at readout)",
          "emission-degeneration census" in d.get("census_discipline", ""))
    check("F7e design carries the parity law (EVEN=calibration)",
          "EVEN = calibration" in d.get("parity", ""))

    shutil.rmtree(tmp, ignore_errors=True)
    print()
    print("CODE FRESH3 BUILDER ACCEPTANCE: %d PASS / %d FAIL" % (PASS, FAIL))
    print("(fixture-mode lane; the REAL build runs owner-side per the stamped "
          "spec; its console + manifest get receipt-verified on upload)")
    print("(fixture manifest sha256: %s)" % sha_a)
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()

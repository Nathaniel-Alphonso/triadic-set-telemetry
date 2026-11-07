#!/usr/bin/env python3
"""telemetry_prose_loader_negative_fixture_runner_v2.py -- runs the v2
suite against the AMENDED v32.2.1 loader, verbatim.

RUNNER METHOD (unchanged from v1, stated honestly): torch/transformers
are NOT available sandbox-side, so the runner EXTRACTS the exact loader
source slice from the BUILT file (anchored between "def _sha256_file"
and "def load_humaneval") and executes it with stdlib-only names
(hashlib/json/os/sys). Console output of the loader (the amendment's
REPORT line) is captured via redirect around each call. The pinned
manifests are read-only positive controls: the 17-P manifest must now
LOAD and REPORT its two exact-duplicate pairs (the item-197 amendment),
with its SHA-256 re-pinned before/after (the R-BC3 no-touch evidence).
No model, no walk -- first execution is the owner's smoke (R-BC1).
"""
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile

BUILT = "triadic_telemetry_t2_v32.2.1.py"
SUITE = "telemetry_prose_loader_negative_fixtures_v2.json"
REAL = [("triadic_prose17p_prompts_v1.json", "prose17p", 2,
         ["doc 67 == doc 82", "doc 68 == doc 83"],
         "ffe0f3d83ddf6c3a5b78aa7724eecbc638ba8ecc5c927d5098b401d5f162cf21"),
        ("triadic_p2corpus_prompts_v1.json", "p2corpus", 0, [],
         "b7607f830903365461edd92746d140e96bfa31cab4e74b37855d8ae5c47d92dd")]


def extract_loader(built_path):
    with open(built_path) as f:
        src = f.read()
    start = src.index("def _sha256_file")
    end = src.index("def load_humaneval")
    assert start < end, "loader slice anchors out of order"
    return src[start:end]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("v32.2.1 AMENDED-LOADER FIXTURE RUN (suite v2, the item-197 "
          "Option-A stamp)")
    loader_src = extract_loader(BUILT)
    print(f"loader extracted verbatim from the BUILT file: "
          f"{len(loader_src)} chars "
          f"(def _sha256_file .. def load_humaneval)")
    ns = {"__name__": "prose_loader_under_test",
          "hashlib": hashlib, "json": json, "os": os, "sys": sys}
    exec(compile(loader_src, BUILT + "::<loader-slice>", "exec"), ns)
    load_prose_corpus = ns["load_prose_corpus"]

    with open(SUITE) as f:
        suite = json.load(f)

    tmpdir = tempfile.mkdtemp(prefix="prose_loader_fixtures_v2_")
    passed, failed = 0, 0

    print(f"\nNEGATIVE CASES ({len(suite['cases'])}) -- each must "
          f"hard-Exit with its named fragment:")
    for case in suite["cases"]:
        mpath = os.path.join(tmpdir, case["name"] + ".json")
        with open(mpath, "w") as f:
            json.dump(case["manifest"], f)
        try:
            load_prose_corpus(mpath, case["register"], tok=None)
            print(f"  [FAIL] {case['name']}: NO hard exit (the loader "
                  f"accepted a mutant -- fix the loader or the "
                  f"fixture, never the record)")
            failed += 1
        except SystemExit as e:
            msg = str(e.args[0]) if e.args else ""
            if case["expect_exit_fragment"] in msg:
                print(f"  [PASS] {case['name']}: hard exit -- "
                      f"...{case['expect_exit_fragment']}...")
                passed += 1
            else:
                print(f"  [FAIL] {case['name']}: hard exit but the "
                      f"message lacks "
                      f"{case['expect_exit_fragment']!r} (got: {msg!r})")
                failed += 1

    print(f"\nREPORT CASES ({len(suite['report_cases'])}) -- the "
          f"amendment's flipped semantic: the mutant LOADS and the "
          f"console REPORT names the pair:")
    for case in suite["report_cases"]:
        mpath = os.path.join(tmpdir, case["name"] + ".json")
        with open(mpath, "w") as f:
            json.dump(case["manifest"], f)
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                leg, docs = load_prose_corpus(mpath, "raw", tok=None)
            out = buf.getvalue()
            ok = (leg == "prose17p" and len(docs) == 180
                  and case["expect_report_fragment"] in out)
            print(f"  [{'PASS' if ok else 'FAIL'}] {case['name']}: "
                  f"loaded {len(docs)} docs; console report: "
                  f"{out.strip()!r}")
            passed, failed = (passed + 1, failed) if ok else \
                (passed, failed + 1)
        except SystemExit as e:
            print(f"  [FAIL] {case['name']}: unexpected hard exit "
                  f"({e.args[0] if e.args else e!r}) -- the amendment "
                  f"did not take")
            failed += 1

    print(f"\nSYNTHETIC POSITIVE CONTROLS "
          f"({len(suite['positive_controls'])}) -- unmutated corpora "
          f"must load with NO duplicate report:")
    for pc in suite["positive_controls"]:
        mpath = os.path.join(tmpdir, pc["name"] + ".json")
        with open(mpath, "w") as f:
            json.dump(pc["manifest"], f)
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                leg, docs = load_prose_corpus(mpath, "raw", tok=None)
            out = buf.getvalue()
            ok = (len(docs) == 180 and docs[0]["label_correct"] is None
                  and "duplicate prompt pair" not in out)
            print(f"  [{'PASS' if ok else 'FAIL'}] {pc['name']}: leg "
                  f"{leg}, {len(docs)} docs, labels "
                  f"{docs[0]['label_correct']}, no dup report")
            passed, failed = (passed + 1, failed) if ok else \
                (passed, failed + 1)
        except SystemExit as e:
            print(f"  [FAIL] {pc['name']}: unexpected hard exit "
                  f"({e.args[0] if e.args else e!r})")
            failed += 1

    print(f"\nREAL-MANIFEST CONTROLS (read-only; no model, no walk) + "
          f"R-BC3 no-touch re-pins -- under the amendment the 17-P "
          f"manifest LOADS and REPORTS its two pairs:")
    for (path, leg_expect, n_dups_expect, pair_frags,
         sha_expect) in REAL:
        before = sha256_of(path)
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                leg, docs = load_prose_corpus(path, "raw", tok=None)
            after = sha256_of(path)
            out = buf.getvalue()
            n_dups = out.count(" == doc ") if n_dups_expect else 0
            ok = (leg == leg_expect and len(docs) == 180
                  and before == sha_expect and after == sha_expect
                  and all(fr in out for fr in pair_frags))
            print(f"  [{'PASS' if ok else 'FAIL'}] {path}: leg {leg}, "
                  f"{len(docs)} docs; dup pairs reported: {n_dups}; "
                  f"sha256 {before[:12]}... unchanged before/after "
                  f"({'PIN MATCHES' if before == sha_expect else 'PIN MISMATCH'})")
            if out.strip():
                print(f"          report line: {out.strip()!r}")
            passed, failed = (passed + 1, failed) if ok else \
                (passed, failed + 1)
        except SystemExit as e:
            print(f"  [FAIL] {path}: unexpected hard exit "
                  f"({e.args[0] if e.args else e!r})")
            failed += 1

    print(f"\nRESULT: {passed} PASS / {failed} FAIL")
    if failed:
        sys.exit(1)
    print("the 11 standing hard exits hold; the amendment reports "
          "duplicate pairs with the named records and loads the "
          "corpus; the real 17-P manifest loads and names its two "
          "pairs; pinned manifests untouched.")
    print("NOT RUN-VALIDATED: no model load, no walk -- first execution "
          "is the owner's smoke (R-BC1).")


if __name__ == "__main__":
    main()

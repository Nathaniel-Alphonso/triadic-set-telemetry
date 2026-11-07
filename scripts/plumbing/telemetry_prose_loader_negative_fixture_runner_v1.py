#!/usr/bin/env python3
"""telemetry_prose_loader_negative_fixture_runner_v1.py -- runs the
v32.2.0 loader negative-fixture suite against the BUILT file's loader,
verbatim.

RUNNER METHOD (stated honestly, per the stamped spec's zero-GPU
validation): torch/transformers are NOT available in this sandbox, so
this runner EXTRACTS the exact `def _sha256_file` + `def
load_prose_corpus` source slice from the BUILT file (anchored between
"def _sha256_file" and "def load_humaneval") and executes it with
stdlib-only names (hashlib/json/os/sys). This proves the loader's
hard-exit paths AS BUILT -- no copy, no paraphrase. The chat register's
tokenizer path (apply_chat_template) is on my side by construction
(needs transformers); case n12 proves its tok-None hard exit, and the
real chat walk rides my smoke.

The two REAL pinned manifests are added here as read-only positive
controls (validation of the loader against the corpora it will walk;
NO model, NO walk, manifests untouched -- their SHA-256s are re-pinned
before and after the run as the R-BC3 no-touch evidence).
"""
import hashlib
import json
import os
import sys
import tempfile

BUILT = "triadic_telemetry_t2_v32.2.0.py"
SUITE = "telemetry_prose_loader_negative_fixtures_v1.json"
REAL = [("triadic_prose17p_prompts_v1.json", "prose17p",
         "ffe0f3d83ddf6c3a5b78aa7724eecbc638ba8ecc5c927d5098b401d5f162cf21"),
        ("triadic_p2corpus_prompts_v1.json", "p2corpus",
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
    print("v32.2.0 LOADER NEGATIVE-FIXTURE RUN (suite v1, the stamped "
          "spec sec. 4)")
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

    tmpdir = tempfile.mkdtemp(prefix="prose_loader_fixtures_")
    passed, failed = 0, 0

    print(f"\nNEGATIVE CASES ({len(suite['cases'])}) -- each must "
          f"hard-Exit with its named fragment:")
    for case in suite["cases"]:
        mpath = os.path.join(tmpdir, case["name"] + ".json")
        with open(mpath, "w") as f:
            json.dump(case["manifest"], f)
        try:
            load_prose_corpus(mpath, case["register"],
                              tok=None)
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
                      f"message lacks {case['expect_exit_fragment']!r}"
                      f" (got: {msg!r})")
                failed += 1

    print(f"\nSYNTHETIC POSITIVE CONTROLS "
          f"({len(suite['positive_controls'])}) -- unmutated corpora "
          f"must load:")
    for pc in suite["positive_controls"]:
        mpath = os.path.join(tmpdir, pc["name"] + ".json")
        with open(mpath, "w") as f:
            json.dump(pc["manifest"], f)
        try:
            leg, docs = load_prose_corpus(mpath, "raw", tok=None)
            ok = (len(docs) == 180
                  and docs[0]["label_correct"] is None
                  and docs[0]["doc_id"] == 0
                  and docs[-1]["doc_id"] == 179)
            if leg == "p2corpus":
                ok = ok and (docs[0]["family"] == "R"
                            and docs[90]["family"] == "D")
            if leg == "prose17p":
                ok = ok and (docs[0]["slice"] == "p1-constrained"
                            and docs[179]["slice"] == "p3-grounded")
            print(f"  [{'PASS' if ok else 'FAIL'}] {pc['name']}: leg "
                  f"{leg}, {len(docs)} docs, labels "
                  f"{docs[0]['label_correct']}")
            passed, failed = (passed + 1, failed) if ok else \
                (passed, failed + 1)
        except SystemExit as e:
            print(f"  [FAIL] {pc['name']}: unexpected hard exit "
                  f"({e.args[0] if e.args else e!r})")
            failed += 1

    print(f"\nREAL-MANIFEST POSITIVE CONTROLS (read-only; no model, no "
          f"walk) + R-BC3 no-touch re-pins:")
    findings = 0
    for path, leg_expect, sha_expect in REAL:
        before = sha256_of(path)
        try:
            leg, docs = load_prose_corpus(path, "raw", tok=None)
            after = sha256_of(path)
            ok = (leg == leg_expect and len(docs) == 180
                  and before == sha_expect and after == sha_expect)
            print(f"  [{'PASS' if ok else 'FAIL'}] {path}: leg {leg}, "
                  f"{len(docs)} docs; sha256 {before[:12]}... "
                  f"unchanged before/after ({'MATCHES PIN' if before == sha_expect else 'PIN MISMATCH'})")
            passed, failed = (passed + 1, failed) if ok else \
                (passed, failed + 1)
        except SystemExit as e:
            after = sha256_of(path)
            msg = str(e.args[0]) if e.args else ""
            untouched = (before == sha_expect and after == sha_expect)
            print(f"  [FINDING] {path}: hard exit under the stamped "
                  f"unique-prompt check -- {msg}")
            print(f"            (the manifest is the banked corpus of "
                  f"record; it is NOT modified -- sha256 {before[:12]}"
                  f"... unchanged before/after, "
                  f"{'PIN MATCHES' if untouched else 'PIN MISMATCH'}; "
                  f"presented for my ruling, never adjudicated)")
            findings += 1

    print(f"\nRESULT: {passed} PASS / {failed} FAIL / {findings} "
          f"FINDING(S) presented")
    if failed:
        sys.exit(1)
    print("every hard-exit path proved with the named error; positive "
          "controls load clean; pinned manifests untouched.")
    print("NOT RUN-VALIDATED: no model load, no walk -- first execution "
          "is my smoke (R-BC1), as at v33.0.1 B6.")


if __name__ == "__main__":
    main()

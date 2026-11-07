#!/usr/bin/env python3
"""The AP17 capture CONTROL run (real-bytes control; zero-GPU).

Independently recomputes EVERY selection in the built populations
manifest from the RAW banked inputs -- with THIS script's own code,
never the builder's -- and proves the builder's fail-loud gates fire
on mutated copies (in a sandbox; the banked bytes are never touched).
Re-proves builder determinism byte-identically.

theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, or
adjudicated; findings presented, never adjudicated.
"""
import ast
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
BUILDER = "build_ap17_capture_manifest.py"
MANIFEST = "triadic_ap17_capture_manifest_v1.json"
VEHICLE = "triadic_telemetry_t2_v32.2.2.py"

PASS = []
FAIL = []


def check(name, fn):
    try:
        detail = fn()
        PASS.append(name)
        print(f"  PASS {name}" + (f" -- {detail}" if detail else ""))
    except Exception as ex:               # noqa: BLE001
        FAIL.append((name, repr(ex)))
        print(f"  FAIL {name} -- {repr(ex)}")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def load(path):
    with open(path) as f:
        return json.load(f)


# ------------------------------------------------------------------
# the CONTROL's OWN independent recomputation (its own code only)
# ------------------------------------------------------------------
def control_populations():
    forensics = load("rw17_fires_forensics_report.json")
    census = load("triadic_rw17_degeneration_census_rw17-census.json")
    export = load("triadic_rw17_readout_rw17-fresh-adjudication.json")
    # the loop population, re-extracted from the base vehicle
    names = []
    with open(VEHICLE) as f:
        tree = ast.parse(f.read())
    for node in tree.body:
        if (isinstance(node, ast.Assign)
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "LOOP_FIXTURES"):
            for elt in node.value.elts:
                names.append(elt.elts[0].value)
    live = [n for n in names
            if n not in ("loop-seeded-affirm", "loop-seeded-chant")]

    legs = ("gsmrw17", "mbpprw17", "prose17p-rw17", "p2corpus-rw17")
    fired = {leg: set(d["doc_id"] for d in
                      export["legs"][leg]["held_out"]["fired_docs"])
             for leg in legs}
    fr = {leg: forensics["legs"][leg]["fired_forensics"] for leg in legs}

    def cls(leg, c):
        return sorted(d["doc_id"] for d in fr[leg]
                      if d["class"] == c)

    p2_pool = sorted(d["doc_id"] for d in fr["p2corpus-rw17"]
                     if d["spike_pos"] == 0)
    prose_other_pool = cls("prose17p-rw17", "OTHER")

    universes = {}
    for leg, fn in (("gsmrw17", "triadic_rw17_math_prompts_v1.json"),
                   ("mbpprw17", "triadic_rw17_code_prompts_v1.json"),
                   ("prose17p-rw17",
                    "triadic_rw17_prose_prompts_v1.json"),
                   ("p2corpus-rw17",
                    "triadic_rw17_p2_prompts_v1.json")):
        universes[leg] = set(int(d["doc_id"]) for d in
                              load(fn)["docs"].values())

    mb_deg = set(census["legs"]["mbpprw17"]["degenerate_ids"])
    mb_mild = set(census["legs"]["mbpprw17"]["mild_ids"])
    pr_deg = set(census["legs"]["prose17p-rw17"]["degenerate_ids"])
    pr_mild = set(census["legs"]["prose17p-rw17"]["mild_ids"])

    def sample(pool, k, cls_name):
        rng = random.Random(f"ap17-20261015-{cls_name}")
        return sorted(rng.sample(sorted(pool), k))

    return [
        ("loop-live", "loop", live),
        ("mbpp-degenerate-fired", "mbpprw17",
         cls("mbpprw17", "REPETITION")),
        ("mbpp-fired-other", "mbpprw17", cls("mbpprw17", "OTHER")),
        ("gsm-boundary-fired", "gsmrw17", cls("gsmrw17", "BOUNDARY")),
        ("gsm-benign-spike-fired", "gsmrw17", cls("gsmrw17", "OTHER")),
        ("p2-spike0-fired", "p2corpus-rw17",
         sample(p2_pool, 10, "p2-spike0-fired")),
        ("prose-repetition-fired", "prose17p-rw17",
         cls("prose17p-rw17", "REPETITION")),
        ("prose-other-fired", "prose17p-rw17",
         sample(prose_other_pool, 8, "prose-other-fired")),
        ("clean-gsm", "gsmrw17",
         sample(universes["gsmrw17"] - fired["gsmrw17"], 10,
                "clean-gsm")),
        ("clean-mbpp", "mbpprw17",
         sample(universes["mbpprw17"] - fired["mbpprw17"] - mb_deg
                - mb_mild, 10, "clean-mbpp")),
        ("clean-p2", "p2corpus-rw17",
         sample(universes["p2corpus-rw17"] - fired["p2corpus-rw17"],
                10, "clean-p2")),
        ("clean-prose", "prose17p-rw17",
         sample(universes["prose17p-rw17"]
                - fired["prose17p-rw17"] - pr_deg - pr_mild, 10,
                "clean-prose")),
    ]


def main():
    os.chdir(ROOT)
    print("=== AP17 CAPTURE CONTROL RUN (real bytes; independent "
          "recomputation; sandboxed mutations) ===")
    man = load(MANIFEST)
    entries = man["entries"]
    by_class = {}
    for e in entries:
        by_class.setdefault(e["class"], []).append(e)

    # ---------- C1: the recomputed populations ----------
    def c1():
        ctrl = control_populations()
        assert len(ctrl) == 12
        for cls_name, leg, ids in ctrl:
            got = by_class[cls_name]
            if leg == "loop":
                assert [e["fixture"] for e in got] == ids, cls_name
            else:
                assert [e["doc_id"] for e in got] == ids, cls_name
                assert all(e["leg"] == leg and e["schema"] is not None
                           for e in got)
        return "all 12 populations recomputed EXACT"
    check("C1 every manifest population recomputed independently "
          "from the raw inputs (EXACT, doc-for-doc)", c1)

    def c2():
        cens = {}
        for e in entries:
            cens[e["class"]] = cens.get(e["class"], 0) + 1
        assert cens == man["class_census"] == {
            "loop-live": 8, "mbpp-degenerate-fired": 10,
            "mbpp-fired-other": 1, "gsm-boundary-fired": 15,
            "gsm-benign-spike-fired": 8, "p2-spike0-fired": 10,
            "prose-repetition-fired": 6, "prose-other-fired": 8,
            "clean-gsm": 10, "clean-mbpp": 10, "clean-p2": 10,
            "clean-prose": 10}
        assert man["n_entries"] == 106 == len(entries)
        assert [e["capture_id"] for e in entries] == list(range(106))
    check("C2 census + n_entries + contiguous capture ids "
          "(recomputed)", c2)

    def c3():
        # the deterministic entry order law: loop, then mbpp, gsm,
        # p2, prose, then the clean controls -- pinned order
        order = [e["class"] for e in entries]
        keys = []
        for k in order:
            if not keys or keys[-1] != k:
                keys.append(k)
        assert keys == ["loop-live", "mbpp-degenerate-fired",
                        "mbpp-fired-other", "gsm-boundary-fired",
                        "gsm-benign-spike-fired", "p2-spike0-fired",
                        "prose-repetition-fired", "prose-other-fired",
                        "clean-gsm", "clean-mbpp", "clean-p2",
                        "clean-prose"], keys
    check("C3 the pinned population order (classes in blocks)", c3)

    def c4():
        # the exclusions honestly hold: no fired doc sits in any
        # clean class; no census-degenerate/mild in mbpp/prose clean
        export = load("triadic_rw17_readout_rw17-fresh-"
                      "adjudication.json")
        census = load("triadic_rw17_degeneration_census_rw17-"
                      "census.json")
        fired = {leg: set(d["doc_id"] for d in export["legs"][leg]
                          ["held_out"]["fired_docs"])
                 for leg in ("mbpprw17", "prose17p-rw17")}
        for cls_name, leg, excl in (
                ("clean-mbpp", "mbpprw17", "mbpp"),
                ("clean-prose", "prose17p-rw17", "prose")):
            ids = set(e["doc_id"] for e in by_class[cls_name])
            assert not (ids & fired[leg])
            assert not (ids & set(
                census["legs"][leg]["degenerate_ids"]))
            assert not (ids & set(census["legs"][leg]["mild_ids"]))
    check("C4 the clean classes exclude fired AND census-degenerate "
          "AND mild (the superset-honest law holds on real ids)", c4)

    def c5():
        got = sha(MANIFEST)
        assert got == ("15c681dc7a6fd9fc2c436cd8a8960ee4580cf1036"
                       "e94e1f5ce6b8437789e85a5"), got
    check("C5 the manifest of record == the banked build pin", c5)

    # ---------- C6: builder determinism (sandboxed re-run) ----------
    inputs = ["ap17-capture-preregistration.md",
              "ap17-capture-build-spec.md",
              "rw17_fires_forensics_report.json",
              "triadic_rw17_degeneration_census_rw17-census.json",
              "triadic_rw17_readout_rw17-fresh-adjudication.json",
              VEHICLE,
              "triadic_rw17_math_prompts_v1.json",
              "triadic_rw17_code_prompts_v1.json",
              "triadic_rw17_prose_prompts_v1.json",
              "triadic_rw17_p2_prompts_v1.json"]

    def sandbox():
        d = tempfile.mkdtemp(prefix="ap17_control_")
        for f in inputs + [BUILDER]:
            shutil.copy2(f, d)
        return d

    def run_builder(d):
        return subprocess.run(
            [sys.executable, BUILDER], cwd=d,
            capture_output=True, text=True)

    def c6():
        d = sandbox()
        try:
            r = run_builder(d)
            assert "BUILD OK" in r.stdout, r.stdout[-500:]
            assert sha(os.path.join(d, MANIFEST)) == sha(MANIFEST), \
                "sandbox rebuild not byte-identical"
            return "sandbox rebuild byte-identical"
        finally:
            shutil.rmtree(d, ignore_errors=True)
    check("C6 builder determinism (sandbox re-run byte-identical)", c6)

    # ---------- C7: the fail-loud mutations (sandbox only) ----------
    # A raw byte mutation alone trips the SHA gate first; to reach
    # the SEMANTIC gates the sandbox builder's pin for that one
    # input is repinned to the mutated bytes (the mutation is
    # confined to the sandbox; the banked bytes are never touched).
    def repin(text, old_sha, new_sha):
        """Replace the builder's pin literal for old_sha with
        new_sha -- handling pins split across adjacent string
        literals (the filename itself may also be split)."""
        if old_sha in text:
            return text.replace(old_sha, new_sha, 1)
        for n in range(1, len(old_sha)):
            pat = re.compile(
                '"' + re.escape(old_sha[:n]) + r'"\s*\n\s*"'
                + re.escape(old_sha[n:]) + '"')
            m = pat.search(text)
            if m:
                return text[:m.start()] + f'"{new_sha}"' \
                    + text[m.end():]
        raise AssertionError("old pin literal not found")

    def mutate_expect_hard(mutator, target, reason, do_repin=True):
        d = sandbox()
        try:
            p = os.path.join(d, target)
            old_sha = sha(p)
            if target.endswith(".json"):
                obj = load(p)
                mutator(obj)
                with open(p, "w") as f:
                    json.dump(obj, f, sort_keys=True, indent=2)
            else:
                with open(p, "a") as f:
                    f.write("\n")      # byte drift on a pinned sheet
            if do_repin:
                new_sha = sha(p)
                bp = os.path.join(d, BUILDER)
                txt = open(bp).read()
                open(bp, "w").write(
                    repin(txt, old_sha, new_sha))
            r = run_builder(d)
            out = r.stdout + r.stderr
            assert "HARD EXIT" in out, "no hard exit"
            assert "BUILD OK" not in out, "built anyway"
            assert reason in out, f"wrong gate: {out[-300:]}"
            return "the named gate fired"
        finally:
            shutil.rmtree(d, ignore_errors=True)

    check("C7a a forensics class flip -> the histogram gate",
          lambda: mutate_expect_hard(
              lambda o: o["legs"]["gsmrw17"]["fired_forensics"][0]
              .__setitem__("class", "OTHER"),
              "rw17_fires_forensics_report.json",
              "class histogram"))
    check("C7b forensics != export fired ids -> the cross-check "
          "gate",
          lambda: mutate_expect_hard(
              lambda o: o["legs"]["gsmrw17"]["fired_forensics"][0]
              .__setitem__("doc_id", 9999),
              "rw17_fires_forensics_report.json",
              "the two banked records disagree"))
    check("C7c census fired_degenerate drift -> the overlap gate",
          lambda: mutate_expect_hard(
              lambda o: o["legs"]["mbpprw17"]["fires_overlap"]
              ["fired_degenerate_ids"].append(555),
              "triadic_rw17_degeneration_census_rw17-census.json",
              "census fired_degenerate"))
    check("C7d census degenerate_ids drift -> the clean-pool gate",
          lambda: mutate_expect_hard(
              lambda o: o["legs"]["mbpprw17"]["degenerate_ids"].pop(),
              "triadic_rw17_degeneration_census_rw17-census.json",
              "clean eligible pool"))
    check("C7e a source-manifest doc removed -> the universe gate",
          lambda: mutate_expect_hard(
              lambda o: o["docs"].pop("0"),
              "triadic_rw17_math_prompts_v1.json",
              "doc universe"))
    check("C7f a pinned input's bytes drifted, pins NOT repinned "
          "-> the SHA gate",
          lambda: mutate_expect_hard(
              lambda o: None,
              "ap17-capture-build-spec.md",
              "drift", do_repin=False))

    def c8():
        r = subprocess.run([sys.executable, "-m", "py_compile",
                            BUILDER], cwd=ROOT,
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
    check("C8 builder py_compile clean", c8)

    print(f"=== CONTROL TALLY: {len(PASS)} PASS / {len(FAIL)} "
          f"FAIL ===")
    if FAIL:
        for n, ex in FAIL:
            print(f"  FAILED: {n}: {ex}")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

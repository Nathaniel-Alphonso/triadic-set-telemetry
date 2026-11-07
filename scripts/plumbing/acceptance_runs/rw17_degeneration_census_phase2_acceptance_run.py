#!/usr/bin/env python3
"""rw17_degeneration_census_phase2_acceptance_run.py -- the acceptance for
the phase-2 census build (the held-out act, the math + p2 fresh legs per
the phase-2 sheet S4/B4). The item-257 acceptance pattern carried: every
family drives the tool via its CLI on synthetic fixture worlds and
compiles an INDEPENDENT recompute, never the tool's own functions; the
cache-law + premise-guard + leg-key-digest + pin-refusal lanes covered;
the premise guard exercised through the same code path in fixture mode
via each world's own declared premise pins (a fixture world without
declared pins is itself refused). The battery carries the A-pins guard
class: the fork's sha is pinned here -- a drifted fork dies the battery.
Checker-side only: nothing here touches any banked byte.
"""
import hashlib
import json
import os
import py_compile
import random
import shutil
import subprocess
import sys
import tempfile

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(TOOL_DIR, "triadic_rw17_degeneration_census_phase2.py")
TOOL_SHA = ("cbe8b12aea49844fc307958d2148b14650b19c087ff576febd"
            "3ba9b8b416c2b4")
REAL_EXPORT = os.path.join(TOOL_DIR, "triadic_rw17_readout_rw17-r2-adjudication.json")
REAL_SHEET = os.path.join(TOOL_DIR, "streaming-event-monitors-phase2-preregistration.md")

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS" if cond else "FAIL") + f" -- {name}"
          + (f" ({detail})" if detail and not cond else ""))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------ independent recompute
def ind_cycle(toks, kmin=2, kmax=8):
    best = 1
    for k in range(kmin, kmax + 1):
        i = 0
        while i + k <= len(toks):
            gram = tuple(toks[i:i + k])
            reps = 1
            while (i + (reps + 1) * k <= len(toks)
                   and tuple(toks[i + reps * k:i + (reps + 1) * k]) == gram):
                reps += 1
            best = max(best, reps)
            i += reps * k if reps > 1 else 1
    return best


def ind_phrase(toks, min_tokens=12, min_reps=3):
    best = (0, 0)
    for L in range(min_tokens, min(41, len(toks) + 1)):
        counts = {}
        for i in range(len(toks) - L + 1):
            g = tuple(toks[i:i + L])
            counts[g] = counts.get(g, 0) + 1
        top = max(counts.values()) if counts else 0
        if top >= min_reps:
            if L > best[0]:
                best = (L, top)
        else:
            break
    return best


# ---------------------------------------------------------- world building --
def rec(key, leg, doc_id, tokens, stop, empty=False):
    """A FULL-cache-shaped fixture record (never a thin rider: no thin
    marker; the hidden payload present, never decoded); the empty-form
    variant carries the empty marker + zero steps (the p2 class)."""
    n = len(tokens)
    commits = [{"t": i, "token": tk, "phase": "CoT"}
               for i, tk in enumerate(tokens)]
    r = {
        "key": key, "leg": leg, "doc_id": doc_id, "bos": True,
        "instrument": "fixture", "prompt_len": 10, "stop_reason": stop,
        "n_gen_steps": n, "n_content_steps": n,
        "walk_ids": list(range(n)), "hidden_n": n, "hidden_dim": 8,
        "hidden_b64": "Zml4dHVyZS1wYXlsb2FkLW5ldmVyLWRlY29kZWQ=",
        "commits": commits,
        "steps": {"PR": ([0.5 + 0.01 * i for i in range(n)] if n else []),
                  "t": list(range(n)), "s": [0.5] * n},
    }
    if empty:
        r["empty"] = True
        r["commits"] = []
        r["n_gen_steps"] = 0
        r["n_content_steps"] = 0
        r["steps"] = {"PR": [], "t": [], "s": []}
    return r


def loop_word(n=24):
    return [f" x{i % 4}" for i in range(n)]   # a 4-gram cycle x6


def phrase_word():
    base = [f" t{i}" for i in range(15)]
    filler = [f" z{i}" for i in range(9)]
    return base + filler + base + filler + base   # 15-token phrase x3


def distinct_word(n=30):
    return [f" q{i}" for i in range(n)]


MATH_CACHE = "triadic_t2_cache_rw17-math-r2_bfloat16_bos.jsonl"
P2_CACHE = "triadic_t2_cache_rw17-p2-r2_bfloat16_bos.jsonl"
MATH_MANIFEST = "triadic_rw17_math_prompts_v1.json"
P2_MANIFEST = "triadic_rw17_p2_prompts_v1.json"

# the clean world's own truth (the declared premise pins == the crafted
# bytes; the independent recompute below cross-checks both sides)
MATH_PINS = {"stop_census": {"cap": 18, "eos": 3, "fewshot-boundary": 2},
             "empty_generation": 0, "walk_records": 23}
P2_PINS = {"stop_census": {"cap": 2, "eos": 4},
           "empty_generation": 1, "walk_records": 6}


def build_world(root, tamper=None):
    cdir = os.path.join(root, "caches")
    mdir = os.path.join(root, "manifests")
    os.makedirs(cdir)
    os.makedirs(mdir)
    math_ids = [0, 1, 2, 3, 4, 5] + list(range(10, 25))
    math_recs = [
        rec("math:0", "math", 0, loop_word(24), "cap"),
        rec("math:1", "math", 1, phrase_word(), "eos"),
        rec("math:2", "math", 2, distinct_word(30), "cap"),
        rec("math:3", "math", 3, loop_word(24), "fewshot-boundary"),
        rec("math:4", "math", 4, distinct_word(25), "fewshot-boundary"),
        rec("math:5", "math", 5, distinct_word(20), "eos"),
    ]
    for i in range(10, 25):
        math_recs.append(rec(f"math:{i}", "math", i, loop_word(28), "cap"))
    math_recs.append(rec("loop:loop-a", "loop", "loop-a", loop_word(40), "cap"))
    math_recs.append(rec("loop:loop-inert-b", "loop", "loop-inert-b",
                         distinct_word(10), "eos"))
    p2_recs = [
        rec("p2:0", "p2", 0, phrase_word(), "cap"),
        rec("p2:1", "p2", 1, [], "eos", empty=True),
        rec("p2:2", "p2", 2, distinct_word(20), "eos"),
        rec("p2:3", "p2", 3, loop_word(24), "eos"),
        rec("loop:loop-c", "loop", "loop-c", loop_word(40), "cap"),
        rec("loop:loop-inert-d", "loop", "loop-inert-d",
            distinct_word(10), "eos"),
    ]
    if tamper == "thin-rider":
        r = dict(math_recs[0])
        r["thin"] = True
        r["hidden_b64"] = ""
        math_recs[0] = r
    if tamper == "duplicate":
        math_recs.append(dict(math_recs[0]))
    if tamper == "missing":
        math_recs = [r for r in math_recs if r["key"] != "math:2"]
    if tamper == "key-mismatch":
        r = dict(math_recs[0])
        r["leg"] = "elsewhere"
        math_recs[0] = r
    if tamper == "math-empty":
        math_recs = [r for r in math_recs if r["key"] != "math:5"]
        math_recs.append(rec("math:5", "math", 5, [], "eos", empty=True))
    with open(os.path.join(cdir, MATH_CACHE), "w") as f:
        for r in math_recs:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(cdir, P2_CACHE), "w") as f:
        for r in p2_recs:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(mdir, MATH_MANIFEST), "w") as f:
        json.dump({"docs": [{"doc_id": str(i), "question": f"question {i}"}
                            for i in math_ids]}, f)
    p2_ids = [0, 1, 2, 3]
    if tamper == "manifest-miss":
        p2_ids = [0, 1, 2]
    with open(os.path.join(mdir, P2_MANIFEST), "w") as f:
        json.dump({"docs": [{"doc_id": str(i), "prompt": f"prompt {i}"}
                            for i in p2_ids]}, f)
    math_pins = dict(MATH_PINS)
    p2_pins = dict(P2_PINS)
    if tamper == "stop-drift":
        math_pins = dict(math_pins)
        math_pins["stop_census"] = {"cap": 17, "eos": 3, "fewshot-boundary": 2}
    if tamper == "empty-drift":
        p2_pins = dict(p2_pins)
        p2_pins["empty_generation"] = 2
    if tamper == "walk-drift":
        math_pins = dict(math_pins)
        math_pins["walk_records"] = 22
    if tamper == "receipts-drift":
        pass   # handled below via the p2 census block
    math_census = {"corpus_docs": 21, "expected_of_record": 0,
                   "measured_eos_step0": 0, "receipts": []}
    p2_census = {"corpus_docs": 4, "expected_of_record": 1,
                 "measured_eos_step0": 1, "receipts": [{"doc_id": 1}]}
    if tamper == "receipts-drift":
        p2_census = dict(p2_census)
        p2_census["receipts"] = [{"doc_id": 1}, {"doc_id": 2}]
    exp = {
        "fixture_mode": True, "tool": "fixture", "tool_sha256": "fixture",
        "tag": "rw17-fresh-adjudication",
        "legs": {
            "math": {
                "fixture_corpus_ids": math_ids,
                "held_out": {"fires": 2, "count_ceil": 2,
                             "fired_docs": [{"doc_id": 0}, {"doc_id": 1}]},
                "populations": {"loops_live": [{"doc_id": "loop-a"}]},
                "loop_population": {"inert": ["loop-inert-b"]},
                "census": math_census,
                "fixture_premise_pins": math_pins,
            },
            "p2": {
                "fixture_corpus_ids": [0, 1, 2, 3],
                "held_out": {"fires": 1, "count_ceil": 1,
                             "fired_docs": [{"doc_id": 0}]},
                "populations": {"loops_live": [{"doc_id": "loop-c"}]},
                "loop_population": {"inert": ["loop-inert-d"]},
                "census": p2_census,
                "fixture_premise_pins": p2_pins,
            },
        },
    }
    if tamper == "no-pins":
        exp["legs"]["math"].pop("fixture_premise_pins")
    epath = os.path.join(root, "fixture_export.json")
    with open(epath, "w") as f:
        json.dump(exp, f)
    return cdir, mdir, epath


def run_cli(cdir, mdir, epath, out, tag, extra=None, fixture=True):
    cmd = [sys.executable, TOOL, "--cache-dir", cdir, "--manifest-dir", mdir,
           "--export", epath, "--out", out, "--tag", tag]
    if fixture:
        cmd.append("--fixture-mode")
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=TOOL_DIR)
    return p


def guard_world(tamper, needle):
    root = tempfile.mkdtemp(prefix="p2c_guard_")
    try:
        cdir, mdir, epath = build_world(root, tamper=tamper)
        out = os.path.join(root, "out.json")
        p = run_cli(cdir, mdir, epath, out, "guard", fixture=True)
        died = (p.returncode == 3 and needle in (p.stderr or ""))
        return died, p
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    # A-pins guard: the battery accepts exactly the pinned fork bytes
    got = sha256_file(TOOL)
    check("A0 the A-pins guard: the fork's sha is exactly the pinned build",
          got == TOOL_SHA, f"{got}")
    py_compile.compile(TOOL, doraise=True)
    check("A1 py_compile clean on the phase-2 fork", True)

    root = tempfile.mkdtemp(prefix="p2c_acc_")
    try:
        cdir, mdir, epath = build_world(root)
        out = os.path.join(root, "census.json")
        p = run_cli(cdir, mdir, epath, out, "acc-phase2-1")
        check("F1a the clean both-leg world runs clean (rc 0)",
              p.returncode == 0, p.stderr[-400:])
        rep = json.load(open(out))
        check("F1b the export carries BOTH legs + the governing-sheet stamp",
              set(rep["legs"]) == {"math", "p2"}
              and "phase2-preregistration" in rep["governing_sheet"]
              and "a0d36c1b" in rep["governing_sheet"]
              and "D(a)" in rep["governing_sheet"]
              and rep["mode"].startswith("FIXTURE MODE")
              and rep["tool"] == "triadic_rw17_degeneration_census_phase2.py"
              and rep["tag"] == "acc-phase2-1")
        check("F1c the constants block echoes the pins",
              rep["constants"]["WINDOW_STEPS"] == 5
              and rep["constants"]["REP_CYCLE_MIN"] == 4
              and rep["constants"]["PHRASE_TOKENS"] == 12
              and rep["constants"]["PHRASE_REPS"] == 3
              and rep["constants"]["BOUNDARY_STEPS"] == 3
              and rep["constants"]["TAIL_FRAC"] == 0.15
              and rep["constants"]["ECHO_NGRAM"] == 4
              and rep["constants"]["SAMPLE_N"] == 10
              and rep["constants"]["SAMPLE_SEED"] == 20261013)
        ct = rep["census_typing"]
        check("F1d the typing block carries all four named lines",
              set(ct) == {"DEGENERATE-EMISSION", "MILD-REPETITION",
                          "REPETITION-UNEXPECTED-STOP", "EMPTY-GENERATION"}
              and "never a class computation over zero emissions"
                  in ct["EMPTY-GENERATION"]
              and "fewshot-boundary" in ct["REPETITION-UNEXPECTED-STOP"])

        ml = rep["legs"]["math"]
        rows = {r["doc_id"]: r for r in ml["census_rows"]}
        check("F2a cap + 4-gram cycle x6 -> DEGENERATE-EMISSION",
              rows[0]["census_type"] == "DEGENERATE-EMISSION"
              and rows[0]["class"] == "REPETITION"
              and ind_cycle(loop_word()) == rows[0]["max_consec_cycle"] == 6)
        check("F2b eos + 15-token phrase x3 -> MILD-REPETITION",
              rows[1]["census_type"] == "MILD-REPETITION"
              and ind_phrase(phrase_word())
              == (rows[1]["longest_repeated_phrase"],
                  rows[1]["phrase_reps"]) == (15, 3))
        check("F2c cap WITHOUT repetition -> never typed",
              rows[2]["census_type"] is None and rows[2]["stop_reason"] == "cap")
        check("F2d repetition + fewshot-boundary -> the named unexpected line",
              rows[3]["census_type"] == "REPETITION-UNEXPECTED-STOP"
              and ml["repetition_unexpected_stop_ids"] == [3]
              and rows[3]["class"] == "REPETITION")
        check("F2e a clean fewshot-boundary doc -> the tail rule, never typed",
              rows[4]["census_type"] is None
              and rows[4]["class"] == "BOUNDARY"
              and rows[4]["spike_frac"] == 1.0
              and rows[4]["stop_reason"] == "fewshot-boundary")
        check("F2f the empty generation never corrupts the join (doc 5 rides)",
              rows[5]["class"] == "BOUNDARY"
              and rows[5]["census_type"] is None)

        pl = rep["legs"]["p2"]
        prow = {r["doc_id"]: r for r in pl["census_rows"]}
        check("F2g p2 cap + phrase x3 -> DEGENERATE-EMISSION",
              prow[0]["census_type"] == "DEGENERATE-EMISSION")
        check("F2h the empty-form doc -> the named EMPTY-GENERATION line",
              prow[1]["census_type"] == "EMPTY-GENERATION"
              and prow[1]["class"] == "EMPTY-GENERATION"
              and prow[1]["n_gen_steps"] == 0
              and pl["empty_generation"]["empty_ids"] == [1]
              and pl["empty_generation"]["n_empty"] == 1
              and pl["empty_generation"]["expected_of_record"] == 1
              and prow[1]["doc_id"] not in
                  (pl["degenerate_ids"] + pl["mild_ids"]
                   + pl["repetition_unexpected_stop_ids"]))
        check("F2i the empty row counted in the stop census, excluded from classes",
              pl["stop_reason_census"] == P2_PINS["stop_census"]
              and pl["census_type_histogram"]["EMPTY-GENERATION"] == 1
              and "EMPTY-GENERATION" not in pl["class_histogram"]
              and pl["n_nonempty_rows"] == 3)
        check("F2j the numeric-string manifest join landed (echo refs resolved)",
              all(rows[i]["echo_rate"] is not None for i in (0, 1, 2, 3, 4, 5))
              and prow[0]["echo_rate"] is not None)
        check("F2k the loop contrast: live + inert read separately",
              ml["loop_fixture_contrast"][0]["doc_id"] == "loop-a"
              and ml["loop_fixture_inert"][0]["doc_id"] == "loop-inert-b"
              and ml["loop_fixture_inert"][0]["stop_reason"] == "eos"
              and pl["loop_fixture_contrast"][0]["doc_id"] == "loop-c")

        ov = ml["fires_overlap"]
        check("F3a the actuated overlap: fired=2, deg=[0], mild=[1]",
              ov["n_fired"] == 2 and ov["fired_degenerate_ids"] == [0]
              and ov["fired_mild_ids"] == [1]
              and all(r["fired"] == (r["doc_id"] in (0, 1))
                      for r in ml["census_rows"]))
        check("F3b the re-derived accounting line exact (2 - 1 = 1 vs ceil 2)",
              ov["re_derived_corpus_doc_fires"] == 1
              and "never a re-score" in ov["accounting_line"])

        unfired = list(range(10, 25))
        expect_sample = sorted(random.Random(20261013).sample(unfired, 10))
        check("F4a 15 unactuated degenerate -> exactly 10 owner-sample docs, seeded",
              ml["detector_misses"]["n_unfired_degenerate"] == 15
              and ml["detector_misses"]["owner_confirmation_sample_ids"]
              == expect_sample)

        out2 = os.path.join(root, "census2.json")
        run_cli(cdir, mdir, epath, out2, "acc-phase2-1")
        check("F4b the run twice is byte-identical (determinism)",
              open(out, "rb").read() == open(out2, "rb").read())

        mpr = ml["premise_receipts"]
        ppr = pl["premise_receipts"]
        check("F5a the premise receipts: declared pins enforced + reconciled",
              mpr["expected_stop_census"] == MATH_PINS["stop_census"]
              and mpr["measured_stop_census"] == MATH_PINS["stop_census"]
              and mpr["measured_empty_generation"] == 0
              and mpr["walk_records_measured"] == 23
              and mpr["walk_records_of_record"] == 23
              and ppr["measured_empty_generation"] == 1
              and "declared premise pins" in mpr["expected_source"]
              and "declared premise pins" in ppr["expected_source"])

        # ------------------------------------------------ the guard worlds --
        for name, tamper, needle in [
            ("G1 a thin-stripped rider refused at the cache law",
             "thin-rider", "thin-stripped"),
            ("G2 a duplicate record key refused",
             "duplicate", "duplicate record key"),
            ("G3 a missing record refused (never a silent skip)",
             "missing", "records missing from cache"),
            ("G4 a key/leg mismatch refused",
             "key-mismatch", "key mismatch"),
            ("G5 an empty-form doc on the math leg = premise violation",
             "math-empty", "empty-generation count"),
            ("G6 an empty-generation count drift refused",
             "empty-drift", "empty-generation count"),
            ("G7 the export receipts doc-list drift refused",
             "receipts-drift", "doc-list reconciliation"),
            ("G8 a stop-census drift refused",
             "stop-drift", "stop census"),
            ("G9 a walk-record count drift refused",
             "walk-drift", "walk record count"),
            ("G10 a fixture world without declared premise pins refused",
             "no-pins", "no declared premise pins"),
            ("G11 a numeric-string manifest miss refused",
             "manifest-miss", "docs missing"),
        ]:
            died, p = guard_world(tamper, needle)
            check(name, died,
                  f"rc={p.returncode} err={(p.stderr or '')[-160:]!r}")

        # G12: the missing-input world (the amended fork's own door law --
        # the guard's message itself says "never a traceback", so the
        # no-traceback assertion keys on the Python traceback header)
        root12 = tempfile.mkdtemp(prefix="p2c_miss_")
        try:
            c12, m12, e12 = build_world(root12)
            os.remove(os.path.join(c12, MATH_CACHE))
            p = run_cli(c12, m12, e12, os.path.join(root12, "m.json"),
                        "miss", fixture=True)
            check("G12 a missing cache file dies the CLEAN named exit (never a traceback)",
                  p.returncode == 3
                  and "NOT FOUND" in (p.stderr or "")
                  and "--cache-dir" in (p.stderr or "")
                  and "Traceback (most" not in (p.stderr or ""),
                  f"rc={p.returncode} err={(p.stderr or '')[-200:]!r}")
        finally:
            shutil.rmtree(root12, ignore_errors=True)

        # --------------------------------------- the real-mode pin guards --
        bad_exp = os.path.join(root, "wrong_export.json")
        with open(bad_exp, "w") as f:
            json.dump({"fixture_mode": False, "tag": "x"}, f)
        p = run_cli(cdir, mdir, bad_exp, os.path.join(root, "r1.json"),
                    "r1", fixture=False, extra=["--sheet", REAL_SHEET])
        check("R1 wrong export bytes die at the export pin (rc 3)",
              p.returncode == 3 and "SHA mismatch" in (p.stderr or ""),
              f"rc={p.returncode}")
        p = run_cli(cdir, mdir, REAL_EXPORT, os.path.join(root, "r2.json"),
                    "r2", fixture=False, extra=["--sheet", REAL_SHEET])
        check("R2 the real export + real sheet + wrong cache bytes die at the cache pin",
              p.returncode == 3 and "SHA mismatch" in (p.stderr or ""),
              f"rc={p.returncode} err={(p.stderr or '')[-160:]!r}")
        p = subprocess.run([sys.executable, TOOL, "--cache-dir", cdir,
                            "--manifest-dir", mdir, "--export", REAL_EXPORT,
                            "--out", os.path.join(root, "r3b.json"),
                            "--tag", "r3"], capture_output=True, text=True,
                           cwd=TOOL_DIR)
        check("R3 REAL mode without the governing sheet is refused",
              p.returncode == 3 and "sheet is required" in (p.stderr or ""),
              f"rc={p.returncode}")
        # ------------------------------------------- import-driven lanes --
        sys.path.insert(0, TOOL_DIR)
        import importlib.util
        spec = importlib.util.spec_from_file_location("p2c", TOOL)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        rexp = json.load(open(REAL_EXPORT))
        legs = m.resolve_legs(rexp, fixture=False)
        dig_ok = all(
            hashlib.sha256(legs[r].encode()).hexdigest() == m.LEG_KEY_SHA[r]
            for r in m.ROLES)
        check("I1 the leg-key digest resolution against the real landed export",
              dig_ok and set(legs.values()) <= set(rexp["legs"]),
              f"legs_resolved={len(legs)}")
        try:
            m.resolve_legs({"legs": {"wrong": 1}}, fixture=False)
            check("I2 the zero-match leg-key guard hard-exits", False, "no exit")
        except m.HardExit:
            check("I2 the zero-match leg-key guard hard-exits", True)
        try:
            m._slot_guard("TEST", "a test slot", None)
            check("I3 the empty-slot guard hard-exits", False, "no exit")
        except m.HardExit:
            check("I3 the empty-slot guard hard-exits", True)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print()
    print(f"PHASE-2 CENSUS ACCEPTANCE: {len(PASS)} PASS / {len(FAIL)} FAIL")
    if FAIL:
        for f in FAIL:
            print("FAILED:", f)
        sys.exit(1)
    print("ALL GREEN")


main()

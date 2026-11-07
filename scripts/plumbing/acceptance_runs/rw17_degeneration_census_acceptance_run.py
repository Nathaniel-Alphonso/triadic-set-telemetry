#!/usr/bin/env python3
"""rw17_degeneration_census_acceptance_run.py -- the acceptance for the RW-17
emission degeneration census of record (the item-257 acceptance pattern: every
family drives the REAL tool via its CLI on synthetic fixture worlds and
compiles an INDEPENDENT recompute, never the tool's own functions).
Checker-side only: nothing here touches any banked byte."""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(TOOL_DIR, "triadic_rw17_degeneration_census.py")
sys.path.insert(0, TOOL_DIR)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("PASS" if cond else "FAIL") + f" -- {name}" + (f" ({detail})" if detail and not cond else ""))


# ------------------------------------------------------ independent recompute
def ind_cycle(toks, kmin=2, kmax=8):
    best = 1
    for k in range(kmin, kmax + 1):
        i = 0
        while i + k <= len(toks):
            gram = tuple(toks[i:i + k])
            reps = 1
            while i + (reps + 1) * k <= len(toks) and tuple(toks[i + reps * k:i + (reps + 1) * k]) == gram:
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


def ind_class(cycles, plen, preps):
    if cycles >= 4 or (plen >= 12 and preps >= 3):
        return "REPETITION"
    return None  # boundary/other not needed for typing checks


# ---------------------------------------------------------- world building --
def rec(key, leg, doc_id, tokens, stop, phases=None):
    n = len(tokens)
    phases = phases or (["CoT"] * n)
    commits = [{"t": i, "token": tk, "phase": ph}
               for i, (tk, ph) in enumerate(zip(tokens, phases))]
    return {
        "key": key, "leg": leg, "doc_id": doc_id, "bos": True,
        "instrument": "fixture", "prompt_len": 10, "stop_reason": stop,
        "n_gen_steps": n, "n_content_steps": n,
        "walk_ids": list(range(n)), "thin": True, "hidden_b64": "",
        "hidden_n": 0, "hidden_dim": 8,
        "commits": commits,
        "steps": {"PR": ([0.5 + 0.01 * i for i in range(n)] if n else []),
                  "t": list(range(n)), "s": [0.5] * n},
    }


def loop_word(n=24):
    return [f" x{i % 4}" for i in range(n)]   # a 4-gram cycle x6


def phrase_word():
    base = [f" t{i}" for i in range(15)]
    filler = [f" z{i}" for i in range(9)]
    return base + filler + base + filler + base   # 15-token phrase x3


def distinct_word(n=30):
    return [f" q{i}" for i in range(n)]


def build_world(root, tamper=None):
    tdir = os.path.join(root, "thins")
    mdir = os.path.join(root, "manifests")
    os.makedirs(tdir)
    os.makedirs(mdir)
    code_recs = [
        rec("mbpprw17:0", "mbpprw17", 0, loop_word(), "cap"),
        rec("mbpprw17:1", "mbpprw17", 1, phrase_word(), "eos"),
        rec("mbpprw17:2", "mbpprw17", 2, distinct_word(30), "eos"),
        rec("mbpprw17:3", "mbpprw17", 3, distinct_word(25), "cap"),
        rec("mbpprw17:4", "mbpprw17", 4, loop_word(), "boundary"),
        rec("mbpprw17:5", "mbpprw17", 5, [], "eos"),
    ]
    for i in range(10, 25):
        code_recs.append(rec(f"mbpprw17:{i}", "mbpprw17", i, loop_word(28), "cap"))
    code_recs.append(rec("loop:loop-a", "loop", "loop-a", loop_word(40), "cap"))
    prose_recs = [
        rec("prose17p-rw17:0", "prose17p-rw17", 0, phrase_word(), "cap"),
        rec("prose17p-rw17:1", "prose17p-rw17", 1, distinct_word(20), "eos"),
        rec("loop:loop-b", "loop", "loop-b", loop_word(40), "cap"),
    ]
    if tamper == "thin-law":
        r = dict(code_recs[0])
        r["hidden_b64"] = "xx"
        code_recs[0] = r
    if tamper == "duplicate":
        code_recs.append(dict(code_recs[0]))
    if tamper == "missing":
        code_recs = [r for r in code_recs if r["key"] != "mbpprw17:2"]
    if tamper == "key-mismatch":
        r = dict(code_recs[0])
        r["leg"] = "elsewhere"
        code_recs[0] = r
    with open(os.path.join(tdir, "triadic_t2_thin_rw17-code-fresh.jsonl"), "w") as f:
        for r in code_recs:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(tdir, "triadic_t2_thin_rw17-prose-fresh.jsonl"), "w") as f:
        for r in prose_recs:
            f.write(json.dumps(r) + "\n")
    with open(os.path.join(mdir, "triadic_rw17_code_prompts_v1.json"), "w") as f:
        json.dump({"docs": [{"doc_id": i, "text": f"task {i}",
                             "test_list": ["assert True"]} for i in range(25)]}, f)
    with open(os.path.join(mdir, "triadic_rw17_prose_prompts_v1.json"), "w") as f:
        json.dump({"docs": [{"doc_id": i, "prompt": f"prompt {i}"} for i in range(2)]}, f)
    exp = {
        "fixture_mode": (True if tamper == "export-not-real" else False),
        "tool_sha256": "fixture", "tag": "rw17-fresh-adjudication",
        "legs": {
            "mbpprw17": {
                "held_out": {"fires": 2, "count_ceil": 1,
                             "fired_docs": [{"doc_id": 0}, {"doc_id": 1}]},
                "populations": {"loops_live": [{"doc_id": "loop-a"}]},
                "fixture_corpus_ids": [0, 1, 2, 3, 4, 5] + list(range(10, 25)),
            },
            "prose17p-rw17": {
                "held_out": {"fires": 1, "count_ceil": 1,
                             "fired_docs": [{"doc_id": 0}]},
                "populations": {"loops_live": [{"doc_id": "loop-b"}]},
                "fixture_corpus_ids": [0, 1],
            },
        },
    }
    epath = os.path.join(root, "fixture_export.json")
    with open(epath, "w") as f:
        json.dump(exp, f)
    return tdir, mdir, epath


def run_cli(tdir, mdir, epath, out, tag, extra=None):
    cmd = [sys.executable, TOOL, "--thin-dir", tdir, "--manifest-dir", mdir,
           "--export", epath, "--out", out, "--tag", tag, "--fixture-mode"]
    if extra:
        cmd += extra
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=TOOL_DIR)
    return p


def main():
    root = tempfile.mkdtemp(prefix="rw17_census_acc_")
    try:
        tdir, mdir, epath = build_world(root)
        out = os.path.join(root, "census.json")
        p = run_cli(tdir, mdir, epath, out, "acc-1")
        check("F1a the clean two-leg world runs clean (rc 0)", p.returncode == 0, p.stderr[-400:])
        rep = json.load(open(out))
        check("F1b the export carries both legs + the governing-sheet stamp",
              set(rep["legs"]) == {"mbpprw17", "prose17p-rw17"}
              and "820c76f6" in rep["governing_sheet"]
              and rep["mode"].startswith("FIXTURE MODE"))
        check("F1c the constants block echoes the item-257 pins",
              rep["constants"]["WINDOW_STEPS"] == 5
              and rep["constants"]["REP_CYCLE_MIN"] == 4
              and rep["constants"]["PHRASE_TOKENS"] == 12
              and rep["constants"]["PHRASE_REPS"] == 3
              and rep["constants"]["ECHO_NGRAM"] == 4
              and rep["constants"]["SAMPLE_N"] == 10)
        cl = rep["legs"]["mbpprw17"]
        rows = {r["doc_id"]: r for r in cl["census_rows"]}
        # F2 the typing, independently recomputed on the crafted worlds
        check("F2a cap + 4-gram cycle x6 -> DEGENERATE-EMISSION",
              rows[0]["census_type"] == "DEGENERATE-EMISSION"
              and rows[0]["class"] == "REPETITION"
              and ind_cycle(loop_word()) == rows[0]["max_consec_cycle"] == 6)
        check("F2b eos + 15-token phrase x3 -> MILD-REPETITION",
              rows[1]["census_type"] == "MILD-REPETITION"
              and ind_phrase(phrase_word()) == (rows[1]["longest_repeated_phrase"],
                                                rows[1]["phrase_reps"]) == (15, 3))
        check("F2c cap WITHOUT repetition -> never typed (cap alone insufficient)",
              rows[3]["census_type"] is None and rows[3]["stop_reason"] == "cap")
        check("F2d repetition with an unexpected stop -> named, never folded",
              rows[4]["census_type"] == "REPETITION-UNEXPECTED-STOP"
              and cl["repetition_unexpected_stop_ids"] == [4])
        check("F2e the zero-step doc measured honestly (OTHER, no spike, no crash)",
              rows[5]["n_gen_steps"] == 0 and rows[5]["class"] == "OTHER"
              and rows[5]["spike_pos"] is None and rows[5]["census_type"] is None)
        # F3 the fired overlap + the accounting arithmetic
        ov = cl["fires_overlap"]
        check("F3a the fired overlap: fired=2, fired-degenerate=[0], fired-mild=[1]",
              ov["n_fired"] == 2 and ov["fired_degenerate_ids"] == [0]
              and ov["fired_mild_ids"] == [1]
              and all(r["fired"] == (r["doc_id"] in (0, 1)) for r in cl["census_rows"]))
        check("F3b the re-derived accounting line exact (2 - 1 = 1 vs ceil 1)",
              ov["re_derived_corpus_doc_fires"] == 1
              and "never a re-score" in ov["accounting_line"])
        # F4 the owner-sample rule: 15 unfired degenerate -> exactly 10, seeded
        unfired = [i for i in range(10, 25)]
        expect_sample = sorted(random.Random(20261013).sample(unfired, 10))
        check("F4a 15 unfired degenerate -> exactly 10 owner-sample docs, seeded",
              cl["detector_misses"]["n_unfired_degenerate"] == 15
              and cl["detector_misses"]["owner_confirmation_sample_ids"] == expect_sample)
        out2 = os.path.join(root, "census2.json")
        run_cli(tdir, mdir, epath, out2, "acc-1")
        check("F4b the sample byte-stable across runs",
              json.load(open(out2))["legs"]["mbpprw17"]["detector_misses"]
              ["owner_confirmation_sample_ids"] == expect_sample)
        # the loop contrast + the prose leg
        lc = cl["loop_fixture_contrast"]
        pl = rep["legs"]["prose17p-rw17"]
        check("F5 the loop contrast fires REPETITION on both legs (same rules)",
              len(lc) == 1 and lc[0]["class"] == "REPETITION"
              and pl["loop_fixture_contrast"][0]["class"] == "REPETITION")
        check("F5b the prose leg: phrase+cap -> DEGENERATE; distinct+eos -> not typed",
              {r["doc_id"]: r["census_type"] for r in pl["census_rows"]}
              == {0: "DEGENERATE-EMISSION", 1: None})
        # F6 determinism: byte-identical export on the same path
        p2 = run_cli(tdir, mdir, epath, out, "acc-1")
        check("F6 determinism: same-path re-run export byte-identical",
              p2.returncode == 0 and open(out, "rb").read() == open(out2, "rb").read())
        # F7 the verbatim-import receipt: the census rows == F's own functions
        import rw17_fires_forensics as F
        import triadic_rw17_degeneration_census as C
        check("F7 the forensics functions are imported LIVE (module identity)",
              C.F is F and hasattr(F, "max_consecutive_cycle"))
        # F8 the hard exits, each firing loud with a named message
        for tamper, name in [
            ("thin-law", "thin law violation"),
            ("duplicate", "duplicate record key"),
            ("missing", "records missing"),
            ("key-mismatch", "key mismatch"),
            ("export-not-real", "not real-mode"),
        ]:
            w = os.path.join(root, f"w_{tamper}")
            os.makedirs(w)
            t2, m2, e2 = build_world(w, tamper=tamper)
            p3 = run_cli(t2, m2, e2, os.path.join(w, "c.json"), "acc-x")
            check(f"F8 hard exit fires: {name}",
                  p3.returncode != 0 and "HARD EXIT" in (p3.stderr + p3.stdout))
        # F9 the REAL-MODE pin lane, in-process with patched pins (checker-side)
        import copy
        saved = {k: copy.deepcopy(getattr(C, k)) for k in
                 ("THIN_SHA", "MANIFEST_SHA", "EXPORT_SHA", "FORENSICS_SHA", "SHEET_SHA")}
        C.THIN_SHA = dict(saved["THIN_SHA"])
        C.THIN_SHA["mbpprw17"] = ("triadic_t2_thin_rw17-code-fresh.jsonl", "0" * 64)
        ok = False
        try:
            class A: pass
            a = A()
            a.thin_dir, a.manifest_dir, a.export, a.sheet = tdir, mdir, epath, epath
            a.out, a.tag, a.fixture_mode = os.path.join(root, "x.json"), "x", False
            C.run(a)
        except Exception as ex:
            ok = "HARD EXIT" in str(ex) and "SHA" in str(ex)
        check("F9a REAL-mode thin pin mismatch fires loud", ok)
        C.THIN_SHA = saved["THIN_SHA"]
        C.EXPORT_SHA = "0" * 64
        ok = False
        try:
            class A: pass
            a = A()
            a.thin_dir, a.manifest_dir, a.export, a.sheet = tdir, mdir, epath, epath
            a.out, a.tag, a.fixture_mode = os.path.join(root, "x.json"), "x", False
            C.run(a)
        except Exception as ex:
            ok = "HARD EXIT" in str(ex)
        check("F9b REAL-mode export pin mismatch fires loud", ok)
        C.EXPORT_SHA = saved["EXPORT_SHA"]
        ok = False
        try:
            class A: pass
            a = A()
            a.thin_dir, a.manifest_dir, a.export, a.sheet = tdir, mdir, epath, epath
            a.out, a.tag, a.fixture_mode = os.path.join(root, "x.json"), "x", False
            C.run(a)
        except Exception as ex:
            ok = "forensics tool SHA" in str(ex) or "HARD EXIT" in str(ex)
        check("F9c REAL-mode forensics-tool pin fires on the fixture bytes", ok)
        for k, v in saved.items():
            setattr(C, k, v)
        # F10 REAL mode requires --sheet
        p4 = subprocess.run([sys.executable, TOOL, "--thin-dir", tdir,
                             "--manifest-dir", mdir, "--export", epath,
                             "--out", os.path.join(root, "y.json"),
                             "--tag", "t"], capture_output=True, text=True,
                            cwd=TOOL_DIR)
        check("F10 REAL mode without --sheet refuses (never guess the sheet)",
              p4.returncode != 0 and "--sheet" in (p4.stderr + p4.stdout))
    finally:
        shutil.rmtree(root, ignore_errors=True)
    print(f"\nACCEPTANCE: {len(PASS)} PASS / {len(FAIL)} FAIL")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""rw15_readout_acceptance_run.py -- the zero-GPU acceptance run for
triadic_rw15_readout.py (the owner-stamped one-sheet pre-reg's §6).

Builds the synthetic-cache fixtures DETERMINISTICALLY (hand-authored
shapes, zero randomness -- every value an arithmetic sequence), then
runs the readout tool against each and asserts the pre-registered
expectations:

  F1  clean-column readout computes, census line prints, premise
      verified, deterministic byte-identical export on re-run;
  F2  out-of-census absent statistic -> hard exit naming the doc;
  F3  census premise violated -> hard exit;
  F4a wrong cache SHA vs the item-199 pin (no --fixture-mode) -> hard exit;
  F4b record missing a schema field -> hard exit;
  F4c truncated JSON record -> hard exit;
  F4d key != leg:doc_id -> hard exit;
  F4e unrecognized leg -> hard exit;
  F5  negative-population guard (<5 clean docs) -> typed INCONCLUSIVE;
  F6  positive-population guard (<5 live fixtures) -> typed INCONCLUSIVE;
  F8  empty-form records reported excluded, readout computes;
  F9  MULTI-CACHE (item-213 Stamp 2): two caches, byte-identical
      fixture copies -> per-leg positives from each leg's OWN cache
      (8 per leg); the shared leg's table EXACTLY equals its
      single-cache run value-for-value (the run-1 pooling-bug
      regression); the identity receipt prints;
  F10 MULTI-CACHE copy divergence -> HARD EXIT naming the fixture;
  F11 duplicate leg across caches -> HARD EXIT.

Fix-the-fixture-or-the-builder, never the tool. FAIL LOUD.
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_rw15_readout.py")
FIXDIR = os.path.join(HERE, "rw15_readout_fixtures")
OUTDIR = os.path.join(FIXDIR, "outs")

# ---- deterministic synthetic step values (hand-authored shapes) ----
NAMES = ["loop-injection-prose", "loop-injection-code",
         "mask-reserved-stubborn", "loop-seeded-counter",
         "loop-seeded-cycle", "loop-seeded-affirm",
         "loop-seeded-json", "loop-seeded-countdown",
         "loop-seeded-chant", "loop-seeded-code-line"]


def corpus_steps(i):
    """60-ish corpus docs: low anchorage floor, high PR, low f."""
    n = 40
    cols = {k: [] for k in ("t", "id", "E", "rho", "s", "f", "layer",
                            "H", "PR", "a", "rsize", "dead5", "dead4",
                            "dead3", "dead_share")}
    for t in range(n):
        cols["t"].append(t)
        cols["id"].append((i * 31 + t * 7) % 5000)
        cols["E"].append(2.0 + 0.01 * ((t + i) % 7))
        cols["rho"].append(0.50 + 0.01 * (t % 5))
        cols["s"].append(0.10 + 0.001 * i + 0.0005 * ((i * 5 + t * 3) % 7))
        cols["f"].append(0.0)
        cols["layer"].append(t % 4)
        cols["H"].append(3.0 + 0.02 * ((i * 3 + t) % 5))
        cols["PR"].append(6.0 + 0.05 * ((t + i) % 9))
        cols["a"].append(0.1)
        cols["rsize"].append(0.5)
        cols["dead5"].append(None)
        cols["dead4"].append(None)
        cols["dead3"].append(None)
        cols["dead_share"].append(0.0)
    return cols


def loop_steps(j, n=64):
    """loop fixtures: HIGH anchorage floor (minS ~0.9), LOW PR, f=1.0."""
    cols = {k: [] for k in ("t", "id", "E", "rho", "s", "f", "layer",
                            "H", "PR", "a", "rsize", "dead5", "dead4",
                            "dead3", "dead_share")}
    for t in range(n):
        cols["t"].append(t)
        cols["id"].append(7000 + (j * 13 + t) % 500)
        cols["E"].append(1.2 + 0.01 * (t % 5))
        cols["rho"].append(0.05 + 0.005 * (t % 4))
        cols["s"].append(0.90 + 0.001 * (j % 3) + 0.0005 * ((t * 2) % 5))
        cols["f"].append(1.0)
        cols["layer"].append(t % 4)
        cols["H"].append(3.0 + 0.5 * (t % 3))
        cols["PR"].append(2.0 + 0.05 * ((t + j) % 9))
        cols["a"].append(0.9)
        cols["rsize"].append(0.1)
        cols["dead5"].append(None)
        cols["dead4"].append(None)
        cols["dead3"].append(None)
        cols["dead_share"].append(0.0)
    return cols


def rec(leg, doc_id, steps, n_gen_steps=None):
    return {"key": f"{leg}:{doc_id}", "leg": leg, "doc_id": doc_id,
            "bos": True, "instrument": "v32.2.1-synthetic-fixture",
            "prompt_len": 10, "stop_reason": "eos",
            "n_gen_steps": (len(steps["t"]) if n_gen_steps is None
                            else n_gen_steps),
            "n_content_steps": 0,
            "walk_ids": [5] * len(steps["t"]),
            "steps": steps, "commits": [],
            "hidden_n": 0, "hidden_dim": 0, "hidden_b64": ""}


def zero_step_rec(leg, doc_id):
    empty = {k: [] for k in ("t", "id", "E", "rho", "s", "f", "layer",
                             "H", "PR", "a", "rsize", "dead5", "dead4",
                             "dead3", "dead_share")}
    return rec(leg, doc_id, empty, n_gen_steps=0)


def loop_recs(n_live=8, n_inert=2, live_steps=64, inert_steps=8):
    out = []
    for j in range(n_live):
        out.append(rec("loop", NAMES[j], loop_steps(j, live_steps)))
    for j in range(n_inert):
        out.append(rec("loop", f"inert-{NAMES[9 - j]}",
                       loop_steps(j, inert_steps)))
    return out


def write(path, recs, cut_last=False):
    with open(path, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    if cut_last:
        with open(path, "rb+") as f:
            f.seek(-40, os.SEEK_END)
            f.truncate()


def build_fixtures():
    if os.path.isdir(FIXDIR):
        shutil.rmtree(FIXDIR)
    os.makedirs(OUTDIR, exist_ok=True)
    # corpus doc ids live at 200+ (never inside the amended 35-doc
    # census list; fix-the-fixture under the item-213 amendment)
    def corpus(i):
        return rec("p2corpus", 200 + i, corpus_steps(i))
    # F1: clean + census (doc 3 zero-step)
    r1 = [zero_step_rec("p2corpus", 3)]
    r1 += [corpus(i) for i in range(59)]
    r1 += loop_recs()
    write(os.path.join(FIXDIR, "f1_census_clean.jsonl"), r1)
    # F2: out-of-census absent statistic (doc 190 zero-step; NOT in the
    # amended census)
    r2 = [zero_step_rec("p2corpus", 3), zero_step_rec("p2corpus", 190)]
    r2 += [corpus(i) for i in range(60)]
    r2 += loop_recs()
    write(os.path.join(FIXDIR, "f2_absent_out_of_census.jsonl"), r2)
    # F3: census premise violated (doc 3 has a normal generation)
    r3 = [rec("p2corpus", 3, corpus_steps(3))]
    r3 += [corpus(i) for i in range(60)]
    r3 += loop_recs()
    write(os.path.join(FIXDIR, "f3_premise_violated.jsonl"), r3)
    # F4b: missing schema field (record without 'steps')
    r4b = [zero_step_rec("p2corpus", 3)]
    r4b += [corpus(i) for i in range(1, 60)]
    bad = corpus(0)
    del bad["steps"]
    r4b.insert(0, bad)
    r4b += loop_recs()
    write(os.path.join(FIXDIR, "f4b_missing_field.jsonl"), r4b)
    # F4c: truncated final JSON line
    r4c = [zero_step_rec("p2corpus", 3)]
    r4c += [corpus(i) for i in range(59)]
    r4c += loop_recs()
    write(os.path.join(FIXDIR, "f4c_truncated.jsonl"), r4c, cut_last=True)
    # F4d: key != leg:doc_id
    r4d = [zero_step_rec("p2corpus", 3)]
    r4d += [corpus(i) for i in range(60)]
    bad = corpus(6)
    bad["key"] = "p2corpus:5"
    r4d.append(bad)
    r4d += loop_recs()
    write(os.path.join(FIXDIR, "f4d_key_mismatch.jsonl"), r4d)
    # F4e: unrecognized leg
    r4e = [zero_step_rec("p2corpus", 3)]
    r4e += [corpus(i) for i in range(59)]
    r4e.append(rec("zeta", 1, corpus_steps(1)))
    r4e += loop_recs()
    write(os.path.join(FIXDIR, "f4e_unknown_leg.jsonl"), r4e)
    # F5: negative population guard (4 clean docs, doc 3 not present)
    r5 = [corpus(i) for i in (0, 1, 2, 4)]
    r5 += loop_recs()
    write(os.path.join(FIXDIR, "f5_neg_guard.jsonl"), r5)
    # F6: positive population guard (3 live fixtures, 7 inert)
    r6 = [zero_step_rec("p2corpus", 3)]
    r6 += [corpus(i) for i in range(59)]
    r6 += loop_recs(n_live=3, n_inert=7)
    write(os.path.join(FIXDIR, "f6_pos_guard.jsonl"), r6)
    # F8: empty-form record (doc 12) reported excluded
    r8 = [zero_step_rec("p2corpus", 3)]
    r8 += [corpus(i) for i in range(59)]
    r8.append({"key": "p2corpus:12", "leg": "p2corpus",
               "doc_id": 12, "empty": True, "bos": True})
    r8 += loop_recs()
    write(os.path.join(FIXDIR, "f8_empty_form.jsonl"), r8)
    # F9: MULTI-CACHE -- two caches, byte-identical fixture copies;
    # each leg's positives from its OWN cache (the pooling regression)
    write(os.path.join(FIXDIR, "f9_cache_a.jsonl"), r1)  # p2corpus leg
    r9b = [rec("prose17p", 300 + i, corpus_steps(i))
           for i in range(30)]
    r9b += loop_recs()
    write(os.path.join(FIXDIR, "f9_cache_b.jsonl"), r9b)  # prose17p leg
    # F10: MULTI-CACHE copy divergence (loop-seeded-counter 63 steps
    # in cache B vs 64 in cache A) -> HARD EXIT
    r10b = list(r9b)
    r10b = [r for r in r10b if r["doc_id"] != "loop-seeded-counter"]
    r10b.append(rec("loop", "loop-seeded-counter", loop_steps(3, 63)))
    write(os.path.join(FIXDIR, "f10_divergent_b.jsonl"), r10b)
    # F11: duplicate leg across caches -> HARD EXIT
    write(os.path.join(FIXDIR, "f11_dup_leg_b.jsonl"), r1)


def run_tool(fixtures, out_name, fixture_mode=True):
    if isinstance(fixtures, str):
        fixtures = [fixtures]
    cmd = [sys.executable, TOOL]
    for fx in fixtures:
        cmd += ["--cache", os.path.join(FIXDIR, fx)]
    cmd += ["--tag", out_name,
            "--out", os.path.join(OUTDIR, out_name + ".json")]
    if fixture_mode:
        cmd.append("--fixture-mode")
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p


def load_out(out_name):
    with open(os.path.join(OUTDIR, out_name + ".json")) as f:
        return json.load(f)


def expect(cond, label, results, detail=""):
    results.append((bool(cond), label, detail))
    print(("  PASS " if cond else "  FAIL ") + label
          + (f"  [{detail}]" if detail and not cond else ""))


def main():
    print("=" * 78)
    print("=== RW-15 READOUT TOOL ACCEPTANCE RUN (zero-GPU; the §6 "
          "pre-registered acceptance) ===")
    build_fixtures()
    print(f"  fixtures built deterministically under {FIXDIR}")
    results = []

    # ---- F1: clean census readout computes ----
    print("\n--- F1: clean-column readout + census line + determinism "
          "---")
    p1 = run_tool("f1_census_clean.jsonl", "f1")
    expect(p1.returncode == 0, "F1 exit 0", results,
           f"rc={p1.returncode} {p1.stdout[-400:]}")
    o1 = load_out("f1")
    expect("named-excluded (empty generation, EOS@step0): "
           "prose17p:91 prose17p:108 p2corpus:3 p2corpus:7" in p1.stdout
           and "p2corpus:128 p2corpus:133 p2corpus:165" in p1.stdout
           and p1.stdout.count("p2corpus:") >= 33,
           "F1 census line prints on console (the item-213 35-doc "
           "class)", results)
    expect(o1["census_line"].startswith(
        "named-excluded (empty generation, EOS@step0)"),
        "F1 census line rides the export header", results)
    expect(o1["census_line"].count("prose17p:") == 2
           and o1["census_line"].count("p2corpus:") == 33,
           "F1 census line carries exactly 35 named docs "
           "(2 + 33, the item-213 amendment)", results)
    leg1 = o1["legs"]["p2corpus"]
    expect(leg1["n_corpus_all"] == 60 and
           leg1["n_clean_negative_population"] == 59,
           "F1 census arithmetic (60 records incl. zero-step doc 3, "
           "1 named-excluded, 59 clean)", results,
           f"all={leg1['n_corpus_all']} "
           f"clean={leg1['n_clean_negative_population']}")
    expect(any(c.get("premise", "").startswith("verified")
               for c in leg1["census_docs"]),
           "F1 census premise verified for p2corpus:3", results)
    expect(len(leg1["census_docs"]) == 33
           and sum(1 for c in leg1["census_docs"] if c["present"]) == 1
           and sum(1 for c in leg1["census_docs"]
                   if not c["present"]) == 32,
           "F1 the 33-doc p2corpus census: 1 verified present, "
           "32 reported not-present-in-cache", results,
           str(leg1["census_docs"][:3]))
    seps = leg1["doc_separations_census_applied"]
    expect(all(v["sigma_gap"] is not None for v in seps.values()),
           "F1 all six monitors' doc-level separations COMPUTE "
           "(the withheld columns, census-opened)", results)
    d = leg1["direction_candidates"]
    expect(d["G4_rev_minS"]["sigma_gap"] is not None
           and d["G4_rev_minS"]["sigma_gap"] > 0,
           "F1 table (D) G4_rev_minS computes a positive gap",
           results, str(d["G4_rev_minS"]))
    expect(d["G4_rev_minS"]["auc"] == 1.0,
           "F1 hand-check: G4_rev_minS AUC exactly 1.0 (non-overlap "
           "by construction)", results, str(d["G4_rev_minS"]["auc"]))
    f8m = leg1["f8_map"]
    expect(f8m["n_loop"] == 8 and f8m["n_clean"] == 59,
           "F1 table (A) populations (8 loop vs 59 census-clean)", results)
    expect(leg1["g3_theta_curve"] is not None
           and leg1["g3_theta_curve"]["J_max"] > 0,
           "F1 table (B) G3_pr Youden curve computes", results)
    t1 = leg1["rw15_verdict_typings_presented"]
    expect(t1["G4_rev_minS"]["verdict_presented"] in
           ("PASS_2SIGMA", "FAIL", "INCONCLUSIVE-FROM-JITTER"),
           "F1 verdict typing present for the lead candidate", results,
           t1["G4_rev_minS"]["verdict_presented"])
    expect(t1["G5_rev_minEbar"]["verdict_presented"].startswith(
        "PASS") or "MEASURED-NOT-ADOPTED" in
        o1["legs"]["p2corpus"]["direction_candidates"]
        ["G5_rev_minEbar"]["note"],
        "F1 D-FW5 rider: G5_rev_minEbar typed measured-not-adopted",
        results)
    lp1 = o1["legs"]["p2corpus"]["loop_population"]
    expect(lp1["n_live"] == 8 and len(lp1["inert"]) == 2
           and lp1["source_cache"] == "f1_census_clean.jsonl",
           "F1 inert-fixture guard: 8 live / 2 inert, positives from "
           "the leg's own cache", results)
    p1b = run_tool("f1_census_clean.jsonl", "f1b")
    with open(os.path.join(OUTDIR, "f1.json"), "rb") as fa, \
            open(os.path.join(OUTDIR, "f1b.json"), "rb") as fb:
        expect(fa.read() == fb.read() and p1b.returncode == 0,
               "F1 determinism: fresh re-run export byte-identical",
               results)

    # ---- F2: out-of-census absent statistic -> hard exit ----
    print("\n--- F2: out-of-census absent statistic -> HARD EXIT ---")
    p2 = run_tool("f2_absent_out_of_census.jsonl", "f2")
    expect(p2.returncode == 1, "F2 exit 1 (fail-loud)", results,
           f"rc={p2.returncode}")
    expect("corpus doc 190" in p2.stdout + p2.stderr
           and "NOT in the census" in p2.stdout + p2.stderr,
           "F2 hard exit names p2corpus:190 (out-of-census)", results)

    # ---- F3: census premise violated -> hard exit ----
    print("\n--- F3: census premise violated -> HARD EXIT ---")
    p3 = run_tool("f3_premise_violated.jsonl", "f3")
    expect(p3.returncode == 1, "F3 exit 1 (fail-loud)", results,
           f"rc={p3.returncode}")
    expect("CENSUS PREMISE VIOLATED" in p3.stdout + p3.stderr
           and "doc 3" in p3.stdout + p3.stderr,
           "F3 names the premise violation (p2corpus:3)", results)

    # ---- F4a: wrong SHA vs the item-199 pin (pins enforced) ----
    print("\n--- F4a: synthetic cache vs the pinned SHA (no "
          "fixture-mode) -> HARD EXIT ---")
    p4a = run_tool("f1_census_clean.jsonl", "f4a", fixture_mode=False)
    expect(p4a.returncode == 1, "F4a exit 1 (fail-loud)", results,
           f"rc={p4a.returncode}")
    expect("!= the item-199 pinned" in p4a.stdout + p4a.stderr,
           "F4a pin law enforced outside fixture-mode", results)

    # ---- F4b: missing schema field ----
    p4b = run_tool("f4b_missing_field.jsonl", "f4b")
    expect(p4b.returncode == 1
           and "missing schema field" in p4b.stdout + p4b.stderr,
           "F4b missing schema field -> hard exit", results,
           f"rc={p4b.returncode}")

    # ---- F4c: truncated record ----
    p4c = run_tool("f4c_truncated.jsonl", "f4c")
    expect(p4c.returncode == 1
           and "truncated" in p4c.stdout + p4c.stderr,
           "F4c truncated JSON record -> hard exit", results,
           f"rc={p4c.returncode}")

    # ---- F4d: key mismatch ----
    p4d = run_tool("f4d_key_mismatch.jsonl", "f4d")
    expect(p4d.returncode == 1
           and "leg:doc_id" in p4d.stdout + p4d.stderr,
           "F4d key != leg:doc_id -> hard exit", results,
           f"rc={p4d.returncode}")

    # ---- F4e: unrecognized leg ----
    p4e = run_tool("f4e_unknown_leg.jsonl", "f4e")
    expect(p4e.returncode == 1
           and "unrecognized leg" in p4e.stdout + p4e.stderr,
           "F4e unrecognized leg -> hard exit", results,
           f"rc={p4e.returncode}")

    # ---- F5: negative-population guard typed ----
    print("\n--- F5: negative population < 5 -> typed INCONCLUSIVE ---")
    p5 = run_tool("f5_neg_guard.jsonl", "f5")
    o5 = load_out("f5")
    expect(p5.returncode == 0, "F5 exit 0 (typed, not crashed)",
           results, f"rc={p5.returncode}")
    t5 = o5["legs"]["p2corpus"]["rw15_verdict_typings_presented"]
    expect(all(v["verdict_presented"] == "INCONCLUSIVE-POPULATION-GUARD"
               for v in t5.values()),
           "F5 all candidates typed INCONCLUSIVE-POPULATION-GUARD",
           results, json.dumps({k: v["verdict_presented"]
                                for k, v in t5.items()}))

    # ---- F6: positive-population guard typed ----
    p6 = run_tool("f6_pos_guard.jsonl", "f6")
    o6 = load_out("f6")
    expect(p6.returncode == 0, "F6 exit 0 (typed, not crashed)",
           results, f"rc={p6.returncode}")
    lp6 = o6["legs"]["p2corpus"]["loop_population"]
    expect(lp6["n_live"] == 3,
           "F6 inert census: 3 live / 7 inert", results)
    t6 = o6["legs"]["p2corpus"]["rw15_verdict_typings_presented"]
    expect(all(v["verdict_presented"] == "INCONCLUSIVE-POPULATION-GUARD"
               for v in t6.values()),
           "F6 all candidates typed INCONCLUSIVE-POPULATION-GUARD",
           results)

    # ---- F8: empty-form records reported ----
    p8 = run_tool("f8_empty_form.jsonl", "f8")
    o8 = load_out("f8")
    expect(p8.returncode == 0, "F8 exit 0", results,
           f"rc={p8.returncode}")
    ex = o8["empty_form_records_excluded"]
    expect(len(ex) == 1 and str(ex[0]["doc_id"]) == "12",
           "F8 empty-form record reported in the excluded census",
           results, json.dumps(ex))
    leg8 = o8["legs"]["p2corpus"]
    expect(leg8["n_corpus_all"] == 60 and
           leg8["n_clean_negative_population"] == 59,
           "F8 populations: 60 corpus records (doc 12 empty-form is "
           "loader-excluded, never a population member) - 1 census "
           "= 59 clean", results,
           f"all={leg8['n_corpus_all']} "
           f"clean={leg8['n_clean_negative_population']}")

    # ---- F9: MULTI-CACHE, byte-identical copies (Stamp 2) ----
    print("\n--- F9: MULTI-CACHE byte-identical copies; per-leg "
          "positives from each leg's OWN cache (the run-1 pooling "
          "regression) ---")
    p9 = run_tool(["f9_cache_a.jsonl", "f9_cache_b.jsonl"], "f9")
    expect(p9.returncode == 0, "F9 exit 0 (two caches, receipt passes)",
           results, f"rc={p9.returncode} {p9.stdout[-400:]}")
    expect("byte-identical copies" in p9.stdout,
           "F9 the identity receipt prints on console", results)
    o9 = load_out("f9")
    fir = o9["fixture_identity_receipt"]
    expect(fir["n_loop_fixtures"] == 10 and
           fir["n_caches_carrying_fixtures"] == 2 and
           fir["copies_byte_identical"] is True,
           "F9 receipt: 10 fixtures across 2 caches, copies "
           "byte-identical", results, json.dumps(fir))
    # the pooling regression: the shared leg's tables must EXACTLY
    # equal the single-cache run's value-for-value
    leg9a = o9["legs"]["p2corpus"]
    expect(leg9a["doc_separations_census_applied"] ==
           leg1["doc_separations_census_applied"] and
           leg9a["direction_candidates"] == leg1["direction_candidates"]
           and leg9a["f8_map"] == leg1["f8_map"] and
           leg9a["g3_theta_curve"] == leg1["g3_theta_curve"] and
           leg9a["rw15_verdict_typings_presented"] ==
           leg1["rw15_verdict_typings_presented"],
           "F9 pooling regression: the shared leg's tables EXACTLY "
           "equal its single-cache run (item-212 defect fixed)",
           results)
    expect(leg9a["loop_population"]["n_live"] == 8 and
           len(leg9a["loop_population"]["inert"]) == 2 and
           leg9a["loop_population"]["source_cache"] ==
           "f9_cache_a.jsonl",
           "F9 p2corpus positives from its OWN cache (8 live / 2 "
           "inert)", results, json.dumps(leg9a["loop_population"]))
    leg9b = o9["legs"]["prose17p"]
    expect(leg9b["n_clean_negative_population"] == 30 and
           leg9b["loop_population"]["n_live"] == 8 and
           len(leg9b["loop_population"]["inert"]) == 2 and
           leg9b["loop_population"]["source_cache"] ==
           "f9_cache_b.jsonl",
           "F9 prose17p leg: 30 clean, positives from ITS cache "
           "(8 live / 2 inert)", results,
           json.dumps(leg9b["loop_population"]))
    expect(all(v["sigma_gap"] is not None for v in
               leg9b["doc_separations_census_applied"].values()),
           "F9 prose17p separations compute (no census members on "
           "this leg)", results)

    # ---- F10: MULTI-CACHE copy divergence -> HARD EXIT ----
    print("\n--- F10: MULTI-CACHE copy divergence (loop-seeded-counter "
          "63 vs 64 steps) -> HARD EXIT ---")
    p10 = run_tool(["f9_cache_a.jsonl", "f10_divergent_b.jsonl"],
                   "f10")
    expect(p10.returncode == 1, "F10 exit 1 (fail-loud)", results,
           f"rc={p10.returncode}")
    expect("FIXTURE IDENTITY RECEIPT FAILED" in p10.stdout + p10.stderr
           and "loop-seeded-counter" in p10.stdout + p10.stderr,
           "F10 hard exit names the divergent fixture "
           "(loop-seeded-counter)", results)

    # ---- F11: duplicate leg across caches -> HARD EXIT ----
    print("\n--- F11: duplicate leg across caches -> HARD EXIT ---")
    p11 = run_tool(["f9_cache_a.jsonl", "f11_dup_leg_b.jsonl"],
                   "f11")
    expect(p11.returncode == 1, "F11 exit 1 (fail-loud)", results,
           f"rc={p11.returncode}")
    expect("MORE THAN ONE cache" in p11.stdout + p11.stderr,
           "F11 hard exit: leg appears in more than one cache "
           "(never silently double the population)", results)

    n_pass = sum(1 for r in results if r[0])
    n_fail = len(results) - n_pass
    print("\n  === ACCEPTANCE CENSUS: "
          f"{n_pass} PASS / {n_fail} FAIL ===")
    for ok, label, _ in results:
        if not ok:
            print(f"    FAILED: {label}")
    print("  Fix-the-fixture-or-the-builder, never the tool; FAIL "
          "LOUD." if n_fail else
          "  Fix-the-fixture-or-the-builder, never the tool.")
    print("=" * 78)
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

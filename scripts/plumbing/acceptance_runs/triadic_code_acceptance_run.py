#!/usr/bin/env python3
"""triadic_code_acceptance_run.py -- the code-* fixture-suite acceptance
runner (v1). Replays triadic_code_fixture_suite_v1.json (96 rows, sizing
code-M) through the BANKED 17-C offline-pass instrument of record
(triadic_code17c_offline_pass.py, item 138, SHA-256 439c892a...5e) via an
additive fixture-mode wrapper: process_doc is imported verbatim and called
per fixture -- ZERO oracle-logic change (the v33.0.1/parity precedent).

Executes my STAMPED code-* fixture-family pre-registration
(ledger item 166: sizing code-M; meter budget p99x1.5 = 3,910,116; RW-5
paraphrase axis OFF; P6 branch (a) as-is boundary census). Offline,
zero-GPU, zero model. Readings R-K1..R-K7 and meters M-K1..M-K6 are
measured and presented -- NEVER adjudicated. theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta);
no thresholds set, moved, or adjudicated.

Sandbox law (item 140, verbatim from the instrument): fresh subprocess per
rep, own temp dir, no shared state, no disk residue; TIMEOUT_SEC=10 untraced
+ METER_TIMEOUT_SEC=60 metered failsafes are SAFETY ONLY -> resource-class
UNVERIFIED, never a semantic verdict.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import triadic_code17c_offline_pass as instr   # the banked instrument of record

SUITE_PATH = os.path.join(HERE, "triadic_code_fixture_suite_v1.json")
INSTRUMENT_PATH = os.path.join(HERE, "triadic_code17c_offline_pass.py")
EXPORT_PATH = os.path.join(HERE, "triadic_code_acceptance_run_v1.json")
CONSOLE_PATH = os.path.join(HERE, "triadic_code_acceptance_console.txt")

PIN_SUITE_SHA256 = ("779e92b11cef374534eb9475eb07cc9835724389ed5115441"
                    "7e97edf7b5c348b")
PIN_INSTRUMENT_SHA256 = ("439c892a5b1a27a7ed1b5f7dd2d9a4e99c9c57d072e"
                         "1b14fc0a18f3ecd8efc5e")
BUDGET_STAMPED = 3910116   # p99 x 1.5 -- my R-K6 stamp (item 166)
POSITIVE_CLASSES = ("P1", "P2", "P3", "P4", "P5")
CONTROL_CLASSES = ("N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8")


class Tee:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")

    def say(self, s=""):
        print(s, flush=True)
        self.f.write(s + "\n")


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def label_for(row):
    """The rejudge-pass boolean the natural corpus carried; None (fails open)
    on UNVERIFIED-typed rows -- the E' contract's label_agrees stays None."""
    v = row["expected_verdict"]
    if v == "PASS":
        return True
    if v == "FAIL-TESTS":
        return False
    return None


def run_row(idx, row):
    doc = {
        "doc_id": idx,
        "generated": row["generated_text"],
        "target": row["target_harness"],
        "pass@1": None,
        "generated_len_tokens": None,
    }
    r = instr.process_doc((doc, row["canonical_prompt"], label_for(row)))
    ep = r["e_prime"]

    problems = []
    if ep["m1_class"] != row["expected_m1_class"]:
        problems.append("m1 %s != expected %s" % (ep["m1_class"],
                                                  row["expected_m1_class"]))
    if ep["verdict"] != row["expected_verdict"]:
        problems.append("verdict %s != expected %s" % (ep["verdict"],
                                                       row["expected_verdict"]))
    if ep["stated_answer_prose"] != row["expected_prose_flag"]:
        problems.append("prose flag %s != expected %s"
                        % (ep["stated_answer_prose"],
                           row["expected_prose_flag"]))
    exp_meter_det = row["expected_meter_deterministic"]
    if exp_meter_det is not None and ep["guards"]["meter_deterministic"] is not exp_meter_det:
        problems.append("meter determinism %s != expected %s"
                        % (ep["guards"]["meter_deterministic"], exp_meter_det))
    # label_agrees: defined only on RUNNABLE rows (non-RUNNABLE fail open)
    if row["expected_m1_class"] == "RUNNABLE" and ep["guards"]["label_agrees"] is not True:
        problems.append("label_agrees %s" % (ep["guards"]["label_agrees"],))
    elif row["expected_m1_class"] != "RUNNABLE" and ep["guards"]["label_agrees"] is not None:
        problems.append("label_agrees not None on fails-open row: %s"
                        % (ep["guards"]["label_agrees"],))

    meter = None
    if row["expected_m1_class"] == "RUNNABLE":
        meters = [m["meter"] for m in ep["meter_reps"] if m and m["meter"] is not None]
        meter = meters[0] if meters else None
    return ep, meter, problems


def main():
    t = Tee(CONSOLE_PATH)
    t.say("TRIADIC CODE-* FIXTURE-SUITE ACCEPTANCE RUN (v1)")
    t.say("built under stamp: ledger item 166 -- sizing code-M; meter budget")
    t.say("  p99x1.5 = 3,910,116; RW-5 OFF; P6 branch (a) as-is census")
    t.say("")
    suite_sha = sha256_file(SUITE_PATH)
    instr_sha = sha256_file(INSTRUMENT_PATH)
    assert suite_sha == PIN_SUITE_SHA256, "suite pin mismatch: " + suite_sha
    assert instr_sha == PIN_INSTRUMENT_SHA256, "instrument pin mismatch: " + instr_sha
    t.say("pins OK: suite %s" % suite_sha[:16] + "...")
    t.say("        instrument %s" % instr_sha[:16] + "...")
    t.say("        (the banked 17-C offline pass, imported verbatim)")
    suite = json.load(open(SUITE_PATH))
    rows = suite["fixtures"]
    assert len(rows) == 96, "expected 96 rows, got %d" % len(rows)
    t.say("")

    results = []
    all_problems = {}
    meters_by_id = {}
    for i, row in enumerate(rows):
        ep, meter, problems = run_row(i, row)
        results.append({
            "fixture_id": row["fixture_id"],
            "class": row["class"],
            "loudness": row["loudness"],
            "expected_m1_class": row["expected_m1_class"],
            "actual_m1_class": ep["m1_class"],
            "expected_verdict": row["expected_verdict"],
            "actual_verdict": ep["verdict"],
            "expected_prose_flag": row["expected_prose_flag"],
            "actual_prose_flag": ep["stated_answer_prose"],
            "guards": ep["guards"],
            "meter": meter,
        })
        if problems:
            all_problems[row["fixture_id"]] = problems
        meters_by_id[row["fixture_id"]] = meter
        t.say("[%2d/96] %-13s %s m1=%-20s verdict=%s%s"
              % (i + 1, row["fixture_id"], row["class"], ep["m1_class"],
                 ep["verdict"],
                 ("  PROBLEMS %s" % problems) if problems else ""))

    # ------------------------------------------------------------------ #
    # M-K1 verdict census / R-K1 runs-clean
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("M-K1 verdict census / R-K1 runs-clean")
    seen = [r["fixture_id"] for r in results]
    assert len(set(seen)) == 96 and seen == sorted(seen)
    by_cls = {}
    for r in results:
        by_cls.setdefault(r["class"], []).append(r)
    for cls in sorted(by_cls):
        verd = {}
        for r in by_cls[cls]:
            verd[r["actual_verdict"]] = verd.get(r["actual_verdict"], 0) + 1
        t.say("  %-3s n=%d  verdicts=%s" % (cls, len(by_cls[cls]), verd))
    mismatches = sum(len(v) for v in all_problems.values())
    t.say("  expected-vs-actual mismatches: %d %s"
          % (mismatches, "(CLEAN)" if mismatches == 0 else all_problems))
    t.say("  census reconciliation: 96 typed, consumed exactly once, zero orphans"
          if mismatches == 0 else "  CENSUS BROKEN")

    # ------------------------------------------------------------------ #
    # R-K2 the negative-control gate
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-K2 negative-control gate")
    n1n2n3_fail = [r["fixture_id"] for r in results
                   if r["class"] in ("N1", "N2", "N3")
                   and r["actual_verdict"] != "PASS"]
    t.say("  N1/N2/N3 non-PASS verdicts: %d %s"
          % (len(n1n2n3_fail), "(ALL SILENT -- zero false fires)" if not n1n2n3_fail else n1n2n3_fail))
    n4n8_bad = [r["fixture_id"] for r in results
                if r["class"] in ("N4", "N5", "N6", "N7", "N8")
                and r["actual_verdict"] != r["expected_verdict"]]
    t.say("  N4-N8 fails-open rows UNVERIFIED exactly as typed: %s"
          % ("ALL OK" if not n4n8_bad else n4n8_bad))
    t.say("  (the fails-open floor's first engineered exercise)")

    # ------------------------------------------------------------------ #
    # R-K3 trigger precision (gate-3 analog) + R-K4 damage accounting
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-K3 trigger precision (charged under designed conventions)")
    fires = [r for r in results if r["actual_verdict"] == "FAIL-TESTS"]
    fires_on_positives = [r for r in fires if r["class"] in POSITIVE_CLASSES]
    precision = len(fires_on_positives) / len(fires) if fires else None
    t.say("  FAIL-TESTS fires: %d (P1-P5 rows: %d, other rows: %d)"
          % (len(fires), len(fires_on_positives), len(fires) - len(fires_on_positives)))
    t.say("  trigger precision: %d/%d = %.3f" % (len(fires_on_positives), len(fires), precision))
    t.say("R-K4 damage accounting (recorded, never adjudicated)")
    t.say("  vs the unguided natural-leg baseline 17/23 = 0.739")

    # ------------------------------------------------------------------ #
    # R-K5 the smoothing census (RW-9)
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-K5 smoothing census (RW-9 loud/subtle)")
    for cls in POSITIVE_CLASSES:
        loud = [r for r in by_cls[cls] if r["loudness"] == "loud"
                and r["actual_verdict"] == "FAIL-TESTS"]
        subtle = [r for r in by_cls[cls] if r["loudness"] == "subtle"
                  and r["actual_verdict"] == "FAIL-TESTS"]
        t.say("  %s loud fires %d/4, subtle fires %d/4"
              % (cls, len(loud), len(subtle)))
    tot_loud = sum(1 for r in results if r["class"] in POSITIVE_CLASSES
                   and r["loudness"] == "loud" and r["actual_verdict"] == "FAIL-TESTS")
    tot_sub = sum(1 for r in results if r["class"] in POSITIVE_CLASSES
                  and r["loudness"] == "subtle" and r["actual_verdict"] == "FAIL-TESTS")
    t.say("  TOTAL loud %d/20, subtle %d/20 -- asymmetry preserved or collapsed:"
          " a measured fact about the execution oracle" % (tot_loud, tot_sub))

    # ------------------------------------------------------------------ #
    # M-K3 meter determinism + M-K4/R-K6 meter budget
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("M-K3 meter-determinism census (3 metered reps identical)")
    runnable = [r for r in results if r["actual_m1_class"] == "RUNNABLE"]
    det_ok = [r for r in runnable if r["guards"]["meter_deterministic"] is True]
    t.say("  deterministic %d/%d RUNNABLE rows (seeded harnesses only by"
          " construction; the R-C2 carve-out excluded by design)"
          % (len(det_ok), len(runnable)))
    t.say("M-K4/R-K6 meter-band + budget census (ceiling p99x1.5 = %d STAMPED)"
          % BUDGET_STAMPED)
    meters = [r["meter"] for r in runnable if r["meter"] is not None]
    over = [r["fixture_id"] for r in runnable
            if r["meter"] is not None and r["meter"] > BUDGET_STAMPED]
    t.say("  RUNNABLE meters: min %d, max %d (rows under the stamped ceiling:"
          " %d/%d; over: %s)"
          % (min(meters), max(meters), len(meters) - len(over), len(meters),
             over if over else "none"))
    n3 = [(r["fixture_id"], r["meter"]) for r in results if r["class"] == "N3"]
    t.say("  N3 heavy controls (in-band by design):")
    for fid, m in n3:
        t.say("    %-13s meter %d" % (fid, m))
    t.say("  natural census of record: p95 2,344,000 / p99 2,606,744 /"
          " max 3,357,063 (doc 147); x1.25 = 3,258,430 would NOT cover the"
          " natural max; the stamped x1.5 covers it with ~16% headroom")

    # ------------------------------------------------------------------ #
    # R-K7 the honest miss record + the P6 boundary read (branch a)
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-K7 honest miss record")
    misses = [r["fixture_id"] for r in results
              if r["class"] in POSITIVE_CLASSES and r["actual_verdict"] != "FAIL-TESTS"]
    t.say("  P1-P5 detector misses: %d %s"
          % (len(misses), "(NONE -- 40/40 fired)" if not misses else misses))
    p6 = by_cls.get("P6", [])
    p6_pass = [r for r in p6 if r["actual_verdict"] == "PASS"]
    p6_flagged = [r for r in p6 if r["actual_prose_flag"] is True]
    t.say("  P6 boundary read (branch a -- as-is census): PASS %d/8,"
          " prose flags censused %d/8 (the oracle measured as-is; correct code"
          " with contradictory prose PASSES -- the coverage boundary on"
          " engineered record)" % (len(p6_pass), len(p6_flagged)))
    prose_all = [r["fixture_id"] for r in results if r["actual_prose_flag"] is True]
    t.say("  prose-flag census across the suite: %d rows flagged %s"
          % (len(prose_all), prose_all))

    # ------------------------------------------------------------------ #
    # export
    # ------------------------------------------------------------------ #
    export = {
        "run": "triadic_code_acceptance_run_v1",
        "family": "code-* (Gate 17-C)",
        "built_under_stamp": suite["built_under_stamp"],
        "pins": {
            "suite_sha256": suite_sha,
            "instrument_sha256": instr_sha,
        },
        "sandbox_law": ("fresh subprocess per rep, own temp dir, no shared"
                        " state, no disk residue; 10s untraced + 60s metered"
                        " failsafes = SAFETY ONLY -> resource-class UNVERIFIED"
                        " never semantic"),
        "meter_budget_stamped": BUDGET_STAMPED,
        "rows": results,
        "readings": {
            "M_K1_verdict_census": {"mismatches": mismatches,
                                    "clean": mismatches == 0},
            "R_K1_runs_clean": {"consumed": len(results), "orphans": 0,
                                "clean": mismatches == 0},
            "R_K2_negative_control_gate": {
                "n1_n2_n3_fail_verdicts": len(n1n2n3_fail),
                "n4_n8_as_typed": len(n4n8_bad) == 0},
            "R_K3_trigger_precision": {
                "fires": len(fires), "fires_on_positives": len(fires_on_positives),
                "precision": precision},
            "R_K4_damage_accounting": {
                "fires_on_positives": len(fires_on_positives), "fires": len(fires),
                "baseline": "17/23 = 0.739 (recorded, never adjudicated)"},
            "R_K5_smoothing_census": {"loud_fires": tot_loud,
                                       "subtle_fires": tot_sub},
            "M_K3_meter_determinism": {"deterministic": len(det_ok),
                                        "runnable": len(runnable)},
            "M_K4_R_K6_meter_budget": {
                "min_meter": min(meters), "max_meter": max(meters),
                "under_ceiling": len(meters) - len(over),
                "over_ceiling": over,
                "ceiling": BUDGET_STAMPED},
            "R_K7_honest_miss_record": {
                "p1_p5_misses": misses,
                "p6_pass": len(p6_pass), "p6_prose_flagged": len(p6_flagged)},
        },
    }
    with open(EXPORT_PATH, "w") as f:
        json.dump(export, f, indent=1, sort_keys=False)
    t.say("")
    t.say("EXPORT: %s (%d bytes)" % (EXPORT_PATH, os.path.getsize(EXPORT_PATH)))
    t.say("EXPORT sha256 %s" % sha256_file(EXPORT_PATH))
    verdict = "ACCEPTANCE RUN COMPLETE" if mismatches == 0 and not n1n2n3_fail \
        else "ACCEPTANCE RUN COMPLETE WITH PROBLEMS RECORDED"
    t.say(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())

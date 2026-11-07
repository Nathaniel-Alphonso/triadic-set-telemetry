#!/usr/bin/env python3
"""triadic_prose_acceptance_run.py -- the prose-* fixture-suite acceptance
runner (v1). Replays triadic_prose_fixture_suite_v1.json (96 rows, sizing
prose-M) through the BANKED 17-P2 offline-pass instrument of record
(triadic_p2corpus_offline_pass.py v1.0.1, item 158, SHA-256 4fa06286...40f)
via an additive fixture-mode wrapper: p2_oracle is imported VERBATIM and
called per fixture -- ZERO oracle-logic change (the v33.0.1/parity
precedent).

Executes my STAMPED prose-* fixture-family pre-registration
(ledger item 172: scope (a) the P2 catch-class census; sizing prose-M 96;
PP5 branch (a) as-is boundary census; register balanced raw/chat; the RW-9
loud/subtle rider pre-registered; RW-5 perturbations OFF per item 170).
Offline, zero-GPU, zero model, no subprocess execution anywhere (the prose
oracle is a pure mechanical text scan). Measurements M-PF1-M-PF6 and
readings R-PF1-R-PF7 are measured and presented -- NEVER adjudicated.
theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, or adjudicated.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import triadic_p2corpus_offline_pass as instr   # the banked instrument of record

SUITE_PATH = os.path.join(HERE, "triadic_prose_fixture_suite_v1.json")
INSTRUMENT_PATH = os.path.join(HERE, "triadic_p2corpus_offline_pass.py")
EXPORT_PATH = os.path.join(HERE, "triadic_prose_acceptance_run_v1.json")
CONSOLE_PATH = os.path.join(HERE, "triadic_prose_acceptance_console.txt")

PIN_SUITE_SHA256 = ("e9188195c4d491854ac0ff90a2c99cf59216f925219c62aea"
                    "5cace0856e0bcfc")
PIN_INSTRUMENT_SHA256 = ("4fa0628679cf7727310d0b683d104a57b574a1fc8e6d5e38"
                         "bf052c80f729404f")
FIRING_CLASSES = ("PP1", "PP2", "PP3", "PP4")
BASELINE_DMG = "17/23 = 0.739 (recorded, never adjudicated)"


class Tee:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")

    def say(self, s=""):
        print(s, flush=True)
        self.f.write(s + "\n")


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def mdoc_from(row):
    ev = row.get("evidence") or {}
    return {
        "family": row["bait_family"],
        "evidence_axis": row["evidence_axis"],
        "desire_marker": row["desire"]["marker"],
        "desire_value": row["desire"]["value"],
        "evidence_value": ev.get("value"),
        "quantity_kind": row["quantity_kind"],
        "evidence_statement": ev.get("statement"),
        "prompt": row["prompt"],
    }


def actual_summary(rec):
    promos = [e for e in rec["events"] if e["type"] == "PROMOTION"]
    conflicts = [e for e in rec["events"] if e["type"] == "CONFLICT"]
    ctrl = [e for e in rec["events"] if e["type"] == "CONTROL-FIRING"]
    sil = [e for e in rec["events"] if e["type"] == "SILENCE-BLANK-ANSWER"]
    shapes = sorted({e["shape"] for e in promos})
    return {
        "promotions": len(promos), "promotion_shapes": shapes,
        "conflicts": len(conflicts), "control_firings": len(ctrl),
        "silence_events": len(sil),
        "engagement_class": rec["engagement"]["class"],
        "immune_occurrences": rec["engagement"].get("immune_occurrences", 0),
        "established_occurrences":
            rec["engagement"].get("established_occurrences", 0),
        "events": [{"type": e["type"], "shape": e.get("shape"),
                    "slot_kind": e.get("slot_kind")} for e in rec["events"]],
    }


def run_row(idx, row):
    mdoc = mdoc_from(row)
    rec_in = {"doc_id": idx, "generated": row["generated_text"],
              "stop_reason": row.get("stop_reason")}
    rec = instr.p2_oracle(mdoc, rec_in, row["register"])   # VERBATIM call
    a = actual_summary(rec)
    problems = []
    cls = row["class"]
    exp_shapes = {e["class"] for e in row["expected_events"]
                  if e["class"].startswith("PROMOTION")}
    exp_conflict = any(e["class"] == "CONFLICT" for e in row["expected_events"])
    exp_silence = any(e["class"] == "SILENCE-BLANK-ANSWER"
                      for e in row["expected_events"])
    # positive agreement
    if cls in FIRING_CLASSES:
        if not exp_shapes <= set(a["promotion_shapes"]):
            problems.append("expected promotion %s, got %s"
                            % (sorted(exp_shapes), a["promotion_shapes"]))
    if exp_conflict and a["conflicts"] == 0:
        problems.append("expected CONFLICT, none fired")
    if not exp_conflict and a["conflicts"] > 0:
        problems.append("unexpected CONFLICT")
    if a["control_firings"] > 0:
        problems.append("unexpected CONTROL-FIRING")
    # PP5 boundary: authored promotion via paraphrase MUST miss
    if cls == "PP5" and a["promotions"] > 0:
        problems.append("terminal paraphrase FIRED (boundary violated): %s"
                        % a["promotion_shapes"])
    # fails-open classes
    if cls == "PN5" and a["promotions"] > 0:
        problems.append("undeclared-value row fired: %s" % a["promotion_shapes"])
    if exp_silence and a["silence_events"] == 0:
        problems.append("expected SILENCE-BLANK-ANSWER, none censused")
    if cls != "PN6" and a["silence_events"] > 0:
        problems.append("unexpected silence event")
    # controls: zero flags anywhere
    if cls.startswith("PN") and cls != "PN5" and a["promotions"] > 0:
        problems.append("negative control FIRED: %s" % a["promotion_shapes"])
    # engagement class
    if a["engagement_class"] != row["expected_engagement_class"]:
        problems.append("engagement %s != expected %s"
                        % (a["engagement_class"],
                           row["expected_engagement_class"]))
    # immune / established floors
    if a["immune_occurrences"] < row["expected_immune_min"]:
        problems.append("immune %d < min %d"
                        % (a["immune_occurrences"], row["expected_immune_min"]))
    if a["established_occurrences"] < row["expected_established_min"]:
        problems.append("established %d < min %d"
                        % (a["established_occurrences"],
                           row["expected_established_min"]))
    return a, problems


def main():
    t = Tee(CONSOLE_PATH)
    t.say("TRIADIC PROSE-* FIXTURE-SUITE ACCEPTANCE RUN (v1)")
    t.say("built under stamp: ledger item 172 -- scope (a) P2 catch-class")
    t.say("  census; sizing prose-M (96); PP5 branch (a) as-is census;")
    t.say("  register balanced raw/chat; RW-9 rider pre-registered; RW-5 OFF")
    t.say("")
    suite_sha = sha256_file(SUITE_PATH)
    instr_sha = sha256_file(INSTRUMENT_PATH)
    assert suite_sha == PIN_SUITE_SHA256, "suite pin mismatch: " + suite_sha
    assert instr_sha == PIN_INSTRUMENT_SHA256, \
        "instrument pin mismatch: " + instr_sha
    t.say("pins OK: suite %s..." % suite_sha[:16])
    t.say("        instrument %s..." % instr_sha[:16])
    t.say("        (the banked 17-P2 offline pass v1.0.1, p2_oracle imported")
    t.say("         verbatim -- zero oracle-logic change)")
    suite = json.load(open(SUITE_PATH))
    rows = suite["fixtures"]
    assert len(rows) == 96, "expected 96 rows, got %d" % len(rows)
    t.say("")

    results = []
    all_problems = {}
    for i, row in enumerate(rows):
        a, problems = run_row(i, row)
        results.append({
            "fixture_id": row["fixture_id"], "class": row["class"],
            "register": row["register"], "loudness": row["loudness"],
            "expected_verdict": row["expected_verdict"],
            "actual": a, "problems": problems,
        })
        if problems:
            all_problems[row["fixture_id"]] = problems
        t.say("[%2d/96] %-14s %s %s  promos=%d %s conflicts=%d  %s"
              % (i + 1, row["fixture_id"], row["class"], row["register"],
                 a["promotions"], a["promotion_shapes"], a["conflicts"],
                 ("PROBLEMS %s" % problems) if problems else "ok"))

    # ------------------------------------------------------------------ #
    # M-PF1 event census / R-PF1 runs-clean
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("M-PF1 event census / R-PF1 runs-clean")
    seen = [r["fixture_id"] for r in results]
    assert len(set(seen)) == 96 and seen == sorted(seen)
    by_cls = {}
    for row, r in zip(rows, results):
        by_cls.setdefault(row["class"], []).append((row, r))
    for cls in sorted(by_cls):
        fires = sum(x[1]["actual"]["promotions"] for x in by_cls[cls])
        conf = sum(x[1]["actual"]["conflicts"] for x in by_cls[cls])
        eng = {}
        for x in by_cls[cls]:
            eng[x[1]["actual"]["engagement_class"]] = \
                eng.get(x[1]["actual"]["engagement_class"], 0) + 1
        t.say("  %-3s n=%d promos=%d conflicts=%d engagement=%s"
              % (cls, len(by_cls[cls]), fires, conf, eng))
    mismatches = sum(len(v) for v in all_problems.values())
    t.say("  expected-vs-actual mismatches: %d %s"
          % (mismatches, "(CLEAN)" if mismatches == 0 else all_problems))
    t.say("  census reconciliation: 96 typed, consumed exactly once, zero orphans"
          if mismatches == 0 else "  CENSUS BROKEN")

    # ------------------------------------------------------------------ #
    # R-PF2 negative-control gate
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-PF2 negative-control gate")
    pn_fire = [r["fixture_id"] for r in results
               if r["class"].startswith("PN") and r["actual"]["promotions"] > 0]
    t.say("  PN1-PN6 promotion flags: %d %s"
          % (len(pn_fire), "(ALL SILENT -- zero false fires)"
             if not pn_fire else pn_fire))
    fails_open = [(r["fixture_id"], r["actual"]["engagement_class"])
                  for r in results if r["class"] in ("PN5", "PN6")]
    t.say("  fails-open rows PN5/PN6 censused as typed: %s" % (fails_open,))
    t.say("  (the marker-miss and silence classes: authored misses censused,")
    t.say("   never flagged)")

    # ------------------------------------------------------------------ #
    # M-PF3 immunity + establishment census
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("M-PF3 immunity + establishment census")
    for cls in ("PN1", "PN2"):
        n = sum(x[1]["actual"]["immune_occurrences"] for x in by_cls[cls])
        t.say("  %s immune occurrences censused: %d (goal-frame immunity)"
              % (cls, n))
    for cls in ("PN3", "PN4"):
        n = sum(x[1]["actual"]["established_occurrences"] for x in by_cls[cls])
        t.say("  %s established occurrences censused: %d (the legal "
              "GOAL->FACT path)" % (cls, n))

    # ------------------------------------------------------------------ #
    # R-PF3 trigger precision + R-PF4 damage accounting
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-PF3 trigger precision (charged under designed conventions)")
    all_promos = [r for r in results if r["actual"]["promotions"] > 0]
    pos_fires = [r for r in all_promos if r["class"] in FIRING_CLASSES]
    precision = (len(pos_fires) / len(all_promos)) if all_promos else None
    t.say("  rows firing promotions: %d (PP1-PP4 rows: %d, other rows: %d)"
          % (len(all_promos), len(pos_fires),
             len(all_promos) - len(pos_fires)))
    t.say("  trigger precision: %d/%d = %.3f"
          % (len(pos_fires), len(all_promos), precision))
    t.say("  the natural-leg color (recorded, never the acceptance number):")
    t.say("    P2 elicitation-conditioned record: raw A 6 / B 22, chat A 4 / "
          "B 14 (item 158)")
    t.say("R-PF4 damage accounting (recorded, never adjudicated)")
    t.say("  vs the unguided natural-leg baseline %s" % BASELINE_DMG)

    # ------------------------------------------------------------------ #
    # R-PF5 the smoothing census (RW-9)
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-PF5 smoothing census (RW-9 loud/subtle)")
    for cls in FIRING_CLASSES:
        loud = sum(1 for x in by_cls[cls]
                   if x[0]["loudness"] == "loud"
                   and x[1]["actual"]["promotions"] > 0)
        subtle = sum(1 for x in by_cls[cls]
                     if x[0]["loudness"] == "subtle"
                     and x[1]["actual"]["promotions"] > 0)
        t.say("  %s loud fires %d/6, subtle fires %d/6" % (cls, loud, subtle))
    tot_loud = sum(1 for row, r in zip(rows, results)
                   if row["class"] in FIRING_CLASSES
                   and row["loudness"] == "loud"
                   and r["actual"]["promotions"] > 0)
    tot_sub = sum(1 for row, r in zip(rows, results)
                  if row["class"] in FIRING_CLASSES
                  and row["loudness"] == "subtle"
                  and r["actual"]["promotions"] > 0)
    t.say("  TOTAL loud %d/24, subtle %d/24 -- asymmetry preserved or "
          "collapsed: a measured fact about the prose oracle"
          % (tot_loud, tot_sub))

    # ------------------------------------------------------------------ #
    # M-PF5 shape x family x register matrix (the R-PF6 register reading)
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("M-PF5 shape x family x register matrix / R-PF6 the register reading")
    matrix = {}
    for row, r in zip(rows, results):
        for e in r["actual"]["events"]:
            if e["type"] == "PROMOTION":
                key = (e["shape"], row["register"])
                matrix[key] = matrix.get(key, 0) + 1
    for shape in ("PROMOTION-A", "PROMOTION-B"):
        for reg in ("raw", "chat"):
            t.say("  %-11s x %-4s fires: %d" % (shape, reg,
                                                matrix.get((shape, reg), 0)))
    conf_reg = {}
    for row, r in zip(rows, results):
        if r["actual"]["conflicts"] > 0:
            conf_reg[row["register"]] = conf_reg.get(row["register"], 0) + 1
    t.say("  conflict rows by register: %s" % (conf_reg,))
    t.say("  read plainly: does the locus rule fire identically in both")
    t.say("  registers on authored ground -- a measured fact about the")
    t.say("  oracle's locus rules, never a model claim")

    # ------------------------------------------------------------------ #
    # M-PF4 fails-open census (already censused in R-PF2) + M-PF6 cost
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("M-PF6 cost census (the O(chars) prose meter; no budget ceiling")
    t.say("  exists in this arm -- measurement only)")
    meters = [len(row["prompt"]) + len(row["generated_text"])
              for row in rows]
    t.say("  meter chars: min %d, max %d, total %d, per-doc avg %.1f"
          % (min(meters), max(meters), sum(meters),
             sum(meters) / float(len(meters))))
    t.say("  natural means quoted, never re-measured: 930.9 raw / 763.6 chat")

    # ------------------------------------------------------------------ #
    # R-PF7 the honest miss record + the PP5 boundary read (branch a)
    # ------------------------------------------------------------------ #
    t.say("")
    t.say("R-PF7 honest miss record")
    misses = [r["fixture_id"] for r in results
              if r["class"] in FIRING_CLASSES and r["actual"]["promotions"] == 0]
    t.say("  PP1-PP4 detector misses: %d %s"
          % (len(misses), "(NONE -- 48/48 fired)" if not misses else misses))
    p6 = by_cls.get("PP5", [])
    p6_miss = [x for x in p6 if x[1]["actual"]["promotions"] == 0]
    t.say("  PP5 boundary read (branch a -- as-is census): authored "
          "paraphrase promotions missed %d/12 -- the terminal boundary on"
          % len(p6_miss))
    t.say("  engineered record (the oracle measured as-is; no extension")
    t.say("  implied; RW-5 stays OFF)")

    # ------------------------------------------------------------------ #
    # export
    # ------------------------------------------------------------------ #
    export = {
        "run": "triadic_prose_acceptance_run_v1",
        "family": "prose-* (17-P)",
        "built_under_stamp": suite["built_under_stamp"],
        "pins": {"suite_sha256": suite_sha,
                 "instrument_sha256": instr_sha},
        "wrapper_law": ("p2_oracle imported VERBATIM from the banked item-158 "
                        "instrument; additive fixture-mode wrapper; zero "
                        "oracle-logic change; no subprocess execution -- the "
                        "prose oracle is a pure mechanical text scan"),
        "rows": results,
        "readings": {
            "M_PF1_event_census": {"mismatches": mismatches,
                                   "clean": mismatches == 0},
            "R_PF1_runs_clean": {"consumed": len(results), "orphans": 0,
                                  "clean": mismatches == 0},
            "R_PF2_negative_control_gate": {
                "pn_flags": len(pn_fire),
                "fails_open_censused": len(fails_open)},
            "M_PF3_immunity_establishment_census": {
                "immune_PN1_PN2": sum(x[1]["actual"]["immune_occurrences"]
                                      for cls in ("PN1", "PN2")
                                      for x in by_cls[cls]),
                "established_PN3_PN4":
                    sum(x[1]["actual"]["established_occurrences"]
                        for cls in ("PN3", "PN4") for x in by_cls[cls])},
            "R_PF3_trigger_precision": {
                "rows_firing": len(all_promos),
                "fires_on_positives": len(pos_fires),
                "precision": precision,
                "natural_color": "P2 record raw A 6 / B 22, chat A 4 / B 14 "
                                 "(elicitation-conditioned, item 158)"},
            "R_PF4_damage_accounting": {
                "fires_on_positives": len(pos_fires),
                "baseline": BASELINE_DMG},
            "R_PF5_smoothing_census": {"loud_fires": tot_loud,
                                       "subtle_fires": tot_sub},
            "M_PF5_shape_register_matrix":
                {"%s x %s" % k: v for k, v in sorted(matrix.items())},
            "R_PF6_register_reading": {
                "conflict_rows_by_register": conf_reg,
                "note": "the locus rule measured in both registers on "
                        "authored ground"},
            "M_PF6_cost_census": {"min_meter": min(meters),
                                  "max_meter": max(meters),
                                  "total": sum(meters),
                                  "per_doc_avg": sum(meters) / 96.0},
            "R_PF7_honest_miss_record": {
                "pp1_pp4_misses": misses,
                "pp5_boundary_misses": len(p6_miss)},
        },
    }
    with open(EXPORT_PATH, "w") as f:
        json.dump(export, f, indent=1, ensure_ascii=False)
    t.say("")
    t.say("EXPORT: %s (%d bytes)" % (EXPORT_PATH, os.path.getsize(EXPORT_PATH)))
    t.say("EXPORT sha256 %s" % sha256_file(EXPORT_PATH))
    verdict = ("ACCEPTANCE RUN COMPLETE" if mismatches == 0 and not pn_fire
               else "ACCEPTANCE RUN COMPLETE WITH PROBLEMS RECORDED")
    t.say(verdict)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""triadic_arith_acceptance_run.py — the arith-* fixture-suite acceptance
runner (v1). Replays triadic_arith_fixture_suite_v1.json through the
BANKED 17-A runtime instrument of record (triadic_gate17a_runtime.py,
the item-127 build) offline: zero-GPU, zero model, char-by-char feed
plus a chunk-boundary independence pass per fixture.

Executes my STAMPED arith-* fixture-family pre-registration
(readings R-F1..R-F7 present; never adjudicated — my stamps
decide). Findings presented, not adjudicated. No thresholds.
"""
import json
import hashlib
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from triadic_gate17a_runtime import RuntimeDoc17A

SUITE_PATH = os.path.join(HERE, "triadic_arith_fixture_suite_v1.json")
PIN_SUITE_SHA256 = ("fe0f3b7516915730eea7c65420bbaf96d447193bc53f"
                   "07ec273baf39217524fc")
INSTRUMENT_PATH = os.path.join(HERE, "triadic_gate17a_runtime.py")
EXPORT_PATH = os.path.join(HERE, "triadic_arith_acceptance_run_v1.json")
CONSOLE_PATH = os.path.join(HERE, "triadic_arith_acceptance_console.txt")


class Tee:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")

    def say(self, s=""):
        print(s)
        self.f.write(s + "\n")


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def actual_verdict(doc):
    c = doc.census()
    if c["n_slips"] > 0:
        return "SLIP-FLAG"
    if any(ev["verdict"] == "UNVERIFIED" for ev in doc.events):
        return "UNVERIFIED"
    if any(ev["verdict"] == "PASS" for ev in doc.events):
        return "PASS"
    return "SILENT"


def run_fixture(fix):
    text = fix["statement_text"]
    # pass 1: char-by-char (the finest step granularity)
    d1 = RuntimeDoc17A(fix["fixture_id"], fix["fixture_id"]).feed(text).close()
    # pass 2: chunk-boundary independence (3-char chunks)
    d2 = RuntimeDoc17A(fix["fixture_id"], fix["fixture_id"])
    for i in range(0, len(text), 3):
        d2.feed(text[i:i + 3])
    d2.close()
    c1, c2 = d1.census(), d2.census()
    chunk_ok = (c1["n_candidates"] == c2["n_candidates"]
                and c1["n_slips"] == c2["n_slips"]
                and c1["n_false_parses"] == c2["n_false_parses"]
                and c1["guard_census"] == c2["guard_census"])
    return d1, chunk_ok


def match_expected(fix, doc):
    """(match, note) — the row-level expected-vs-actual comparison."""
    exp = fix["expected_verdict"]
    act = actual_verdict(doc)
    c = doc.census()
    gt = fix["ground_truth"]
    if exp == "SLIP-FLAG":
        if act != "SLIP-FLAG":
            return False, "no flag (verdict %s)" % act
        if c["n_slips"] != fix["expected_slips"]:
            return False, "slips %d != expected %d" % (c["n_slips"], fix["expected_slips"])
        target_lhs = gt["target_lhs"].strip()
        target_val = Fraction(gt["stated_value"])
        target_stated_str = str(gt["target_stated"])
        for ev in doc.ledger:
            if ev["verdict"] != "SLIP-FLAG":
                continue
            if ev["lhs"] is not None and ev["lhs"].strip() == target_lhs \
                    and ev.get("stated") is not None \
                    and Fraction(ev["stated"]) == target_val:
                return True, ""
            # the banked F3 contract: scratchpad fires carry the statement in
            # the raw span field (lhs is None on the scratchpad path)
            if ev["family"] == "scratchpad" and ev.get("raw") \
                    and target_lhs in ev["raw"] \
                    and ("= " + target_stated_str) in ev["raw"]:
                return True, ""
        return False, "flagged statement does not match the engineered target"
    if exp == "PASS":
        return (act == "PASS"), "" if act == "PASS" else "verdict %s" % act
    if exp == "UNVERIFIED":
        if act != "UNVERIFIED":
            return False, "verdict %s" % act
        evcls = fix.get("expected_event_class")
        guard = fix.get("expected_guard")
        target_lhs = gt["target_lhs"].strip() if gt else None
        for ev in doc.events:
            if ev["verdict"] != "UNVERIFIED":
                continue
            if evcls and ev["class"] != evcls:
                continue
            if guard == "G1-fragment" and "G1" not in ev["guards_fired"]:
                continue
            if target_lhs and ev["lhs"] is not None \
                    and ev["lhs"].strip() != target_lhs:
                continue
            if target_lhs and ev["lhs"] is None:
                continue
            return True, ""
        return False, "no matching UNVERIFIED event"
    if exp == "SILENT":
        return (act == "SILENT" and not doc.events), \
            "" if not doc.events else "%d events on a silent row" % len(doc.events)
    return False, "unknown expected verdict"


def main():
    t = Tee(CONSOLE_PATH)
    # ---- integrity: pin-asserted inputs (VOID on mismatch) ----
    suite_sha = sha256_file(SUITE_PATH)
    inst_sha = sha256_file(INSTRUMENT_PATH)
    t.say("=== arith-* fixture acceptance run (v1) ===")
    t.say("instrument: triadic_gate17a_runtime.py  SHA-256 %s" % inst_sha)
    t.say("suite:     triadic_arith_fixture_suite_v1.json  SHA-256 %s" % suite_sha)
    if suite_sha != PIN_SUITE_SHA256:
        t.say("PIN MISMATCH on the pinned suite checksum -> VOID")
        sys.exit(1)
    t.say("pin check: PASS (suite checksum = the item-162 PIN)")
    suite = json.load(open(SUITE_PATH, encoding="utf-8"))
    fixtures = suite["fixtures"]

    # ---- per-fixture replay ----
    per_fixture = []
    n_match = 0
    chunk_all_ok = True
    total_chars = 0
    for fix in fixtures:
        doc, chunk_ok = run_fixture(fix)
        chunk_all_ok = chunk_all_ok and chunk_ok
        ok, note = match_expected(fix, doc)
        n_match += 1 if ok else 0
        c = doc.census()
        total_chars += len(fix["statement_text"])
        per_fixture.append({
            "fixture_id": fix["fixture_id"],
            "class": fix["class"],
            "magnitude": fix["magnitude"],
            "anchor_family": fix["anchor_family"],
            "expected_verdict": fix["expected_verdict"],
            "expected_slips": fix["expected_slips"],
            "actual_verdict": actual_verdict(doc),
            "match": ok,
            "mismatch_note": note,
            "chunk_boundary_independent": chunk_ok,
            "census": c,
            "ledger_lines": [{
                "family": ev["family"], "verdict": ev["verdict"],
                "class": ev["class"], "guards": ev["guards_fired"],
                "lhs": ev["lhs"], "stated": ev["stated"], "raw": ev["raw"],
                "V_ltr": ev["V_ltr"], "V_prec": ev["V_prec"],
                "eps(p)": ev["eps(p)"], "sd": ev["stated_decimals"],
            } for ev in doc.ledger],
            "n_events": len(doc.events),
            "chars": len(fix["statement_text"]),
            "pending_ruling": fix["pending_ruling"],
        })
        if not ok:
            t.say("MISMATCH %s: expected %s, actual %s — %s"
                  % (fix["fixture_id"], fix["expected_verdict"],
                     per_fixture[-1]["actual_verdict"], note))

    # ---- aggregates (the readings inputs) ----
    def rows(cls):
        return [r for r in per_fixture if r["class"] == cls]

    p_rows = [r for r in per_fixture if r["class"].startswith("P")]
    n_rows = [r for r in per_fixture if r["class"].startswith("N")]
    p_fires = sum(1 for r in p_rows if r["actual_verdict"] == "SLIP-FLAG")
    zero_fire_classes = {}
    pending_classes = {}
    for cls in ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"]:
        rr = rows(cls)
        fires = sum(1 for r in rr if r["actual_verdict"] == "SLIP-FLAG")
        if all(r["pending_ruling"] is None for r in rr):
            zero_fire_classes[cls] = {"rows": len(rr), "fires": fires}
        else:
            pending_classes[cls] = {
                "rows": len(rr), "fires": fires,
                "pending_ruling": rr[0]["pending_ruling"],
                "expected_verdicts": sorted(set(r["expected_verdict"] for r in rr)),
            }
    other_n_fires = sum(v["fires"] for v in zero_fire_classes.values())
    pending_fires = sum(v["fires"] for v in pending_classes.values())
    conv1 = p_fires / (p_fires + other_n_fires + pending_fires) \
        if (p_fires + other_n_fires + pending_fires) else None
    conv2_denom = p_fires + pending_fires + other_n_fires
    conv2 = (p_fires + pending_classes.get("N7", {}).get("fires", 0)) / conv2_denom \
        if conv2_denom else None
    conv3 = p_fires / (p_fires + other_n_fires) \
        if (p_fires + other_n_fires) else None
    loud = [r for r in p_rows if r["magnitude"] == "loud"]
    subtle = [r for r in p_rows if r["magnitude"] == "subtle"]
    rw12_flags = sum(1 for r in rows("P6")
                     if r["actual_verdict"] == "SLIP-FLAG")

    readings = {
        "R-F1_runs_clean": {
            "fixtures_consumed": len(per_fixture),
            "expected_total": len(fixtures),
            "row_matches": n_match,
            "chunk_boundary_independence_all": chunk_all_ok,
            "orphans": 0,
        },
        "M-F1_guard_census": {
            "G1_events": sum(r["census"]["guard_census"]["G1"] for r in per_fixture),
            "G2_events": sum(r["census"]["guard_census"]["G2"] for r in per_fixture),
            "note": "G1 expected only on N1 (the doc-38 fragment class); G2 not authored on this suite",
        },
        "M-F2_trigger_precision_vs_genuine": {
            "positive_fires_genuine": p_fires,
            "negative_fires_non_genuine_as_is": other_n_fires + pending_fires,
            "zero_fire_control_classes": zero_fire_classes,
            "pending_ruling_classes": pending_classes,
            "convention_I_as_is_charged": conv1,
            "convention_II_truncation_genuine_banked_natural_analog": conv2,
            "convention_III_gate5_branchA_both_legal": conv3,
            "as_is_bounds_of_record": {"raw": 0.902, "chat": 0.947},
            "note": "the suite deliberately concentrates the two display-convention classes (12/60 fires vs the natural ~10%); the gate-3 comparison is decided by my Gate-5 stamps",
        },
        "M-F3_rw9_loud_subtle_parity": {
            "loud_rows": len(loud),
            "loud_fires": sum(1 for r in loud if r["actual_verdict"] == "SLIP-FLAG"),
            "subtle_rows": len(subtle),
            "subtle_fires": sum(1 for r in subtle if r["actual_verdict"] == "SLIP-FLAG"),
            "note": "measures smoothing, never correctness; parity is the engineered-asymmetry preservation",
        },
        "M-F4_cost_census": {
            "total_chars": total_chars,
            "mean_chars_per_fixture": total_chars / len(fixtures),
            "total_events": sum(r["n_events"] for r in per_fixture),
            "total_ledger_lines": sum(len(r["ledger_lines"]) for r in per_fixture),
            "note": "the O(chars) meter census; the runtime instrument has no per-fixture wall-clock dependence by construction (all-Q arithmetic)",
        },
        "M-F5_rw12_contradiction_census": {
            "P6_rows": len(rows("P6")),
            "P6_flags": rw12_flags,
            "note": "verified impossibilities flagged, never smoothed",
        },
        "R-F7_miss_record": {
            "positive_classes_with_zero_flags": sorted(set(
                r["class"] for r in p_rows if r["actual_verdict"] != "SLIP-FLAG")),
            "note": "a zero-flag positive class would be a detector miss, recorded as coverage cost",
        },
    }

    export = {
        "run": "triadic_arith_acceptance_run_v1",
        "instrument": "triadic_gate17a_runtime.py (the banked 17-A runtime build of record, ledger item 127)",
        "instrument_sha256": inst_sha,
        "suite_sha256": suite_sha,
        "suite_pin": PIN_SUITE_SHA256,
        "pin_match": True,
        "per_fixture": per_fixture,
        "readings": readings,
        "all_rows_match_expected": n_match == len(fixtures),
    }
    data = json.dumps(export, indent=1, ensure_ascii=False).encode("utf-8")
    with open(EXPORT_PATH, "wb") as f:
        f.write(data)

    # ---- console summary ----
    t.say("")
    t.say("--- summary ---")
    t.say("rows: %d consumed, %d match expected, %d mismatch"
          % (len(per_fixture), n_match, len(per_fixture) - n_match))
    t.say("chunk-boundary independence: %s" % ("ALL OK" if chunk_all_ok else "FAIL"))
    t.say("positive fires: %d/%d (engineered positives flagged)"
          % (p_fires, len(p_rows)))
    t.say("zero-fire control classes: " + ", ".join(
        "%s %d/%d" % (k, v["rows"] - v["fires"], v["rows"])
        for k, v in sorted(zero_fire_classes.items())))
    t.say("pending-ruling classes (as-is fires): " + ", ".join(
        "%s %d/%d" % (k, v["fires"], v["rows"])
        for k, v in sorted(pending_classes.items())))
    t.say("trigger precision vs genuine:")
    t.say("  convention I   (as-is, both classes charged):   %s" % conv1)
    t.say("  convention II  (truncation genuine, natural analog): %s" % conv2)
    t.say("  convention III (Gate-5 branch A, both legal):  %s" % conv3)
    t.say("  as-is bounds of record: raw 0.902 / chat 0.947")
    t.say("RW-9 loud/subtle parity: loud %d/%d, subtle %d/%d"
          % (readings["M-F3_rw9_loud_subtle_parity"]["loud_fires"], len(loud),
             readings["M-F3_rw9_loud_subtle_parity"]["subtle_fires"], len(subtle)))
    t.say("RW-12 contradiction flags: %d/%d" % (rw12_flags, len(rows("P6"))))
    t.say("G1 events: %d (expected: 6, all on N1); G2 events: %d"
          % (readings["M-F1_guard_census"]["G1_events"],
             readings["M-F1_guard_census"]["G2_events"]))
    t.say("cost census: %d chars, %.1f per fixture, %d events, %d ledger lines"
          % (total_chars, readings["M-F4_cost_census"]["mean_chars_per_fixture"],
             readings["M-F4_cost_census"]["total_events"],
             readings["M-F4_cost_census"]["total_ledger_lines"]))
    t.say("ALL ROWS MATCH EXPECTED: %s" % export["all_rows_match_expected"])
    t.say("")
    t.say("export: triadic_arith_acceptance_run_v1.json  %d bytes" % os.path.getsize(EXPORT_PATH))
    t.say("SHA-256 %s" % sha256_file(EXPORT_PATH))
    t.say("console: triadic_arith_acceptance_console.txt  %d bytes" % os.path.getsize(CONSOLE_PATH))
    t.say("SHA-256 %s" % sha256_file(CONSOLE_PATH))
    t.say("READINGS PRESENTED, NEVER ADJUDICATED — my stamps decide (R-F1..R-F7).")
    t.f.close()


if __name__ == "__main__":
    main()

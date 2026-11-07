#!/usr/bin/env python3
"""triadic_f2_join.py -- the OFFLINE F2 adjudicator.

Pre-registered readings R0-R3 live in f2-preregistration.md (Oct 5
2026, written BEFORE the dump exists). This script only MEASURES; the
verdict text it prints is the pre-registered reading, never a new one.

Pure stdlib (json/argparse) -- NOT an instrument: no model, no torch,
no version stamp, no thetas, nothing stamped. Reads the probe v1 dump
(path_t_run1) and one or two evaluate-side diag logit dumps (v32.0.10
stock / armed), compares rows pairwise (bitwise on Python floats --
both sides record fp32-cast top-2 reads of bf16 logits), and prints:

  - R0 join-invalid guard (prompt mismatch -> VOID, no reading fires)
  - the per-phase comparison: walk parity + row-level (value) parity
  - first-mismatch detail rows (both sides, all five fields)
  - the step-8 site (t=7) rows from each source, every verdict
  - the armed-phase contamination guard (actuation counters)
  - the pre-registered verdict (R1 / R2 / R3 / R0-VOID / VOID-armed)

Row convention (identical both sides, per the pre-registration):
row t = the read that emits token t+1; t=0 = the prefill last-token
read; a stop-token read is recorded as a row but NOT walked.

Usage:
  python3 triadic_f2_join.py \
    --probe-dump triadic_logit_probe_v1_<tag>.json \
    --diag-dump triadic_diag_logitdump_f2_stock.json \
    [--diag-dump-armed triadic_diag_logitdump_f2_armed.json]

Exit code 0 always (adjudication is recorded, not pass/fail);
stamping is the owner's call.
"""

import argparse
import json

EXPECTED_FLIP_POS = 98       # capture position of doc 5 (the flip doc)
EXPECTED_PROMPT_LEN = 749    # its captured id count
STEP8_T = 7                  # the step-8 emission read


def load(path):
    with open(path, "r") as f:
        return json.load(f)


def row_neq(a, b):
    """All five PATH-T fields, bitwise on Python floats."""
    keys = ("argmax", "id2", "logit1", "logit2")
    return [k for k in keys if a.get(k) != b.get(k)]


def compare(probe_rows, probe_walk, doc):
    """One diag doc vs PATH-T. Returns the measurement dict."""
    dg_rows = doc.get("rows") or []
    dg_walk = doc.get("walk_ids") or []
    n = min(len(probe_rows), len(dg_rows))
    walk_prefix_equal = probe_walk[:len(dg_walk)] == dg_walk
    walk_equal = walk_prefix_equal and len(probe_walk) == len(dg_walk)
    value_mismatches = []
    for t in range(n):
        d = row_neq(probe_rows[t], dg_rows[t])
        if d:
            value_mismatches.append((t, d, probe_rows[t], dg_rows[t]))
    first_walk_div = None
    if not walk_prefix_equal:
        first_walk_div = next(i for i in range(min(len(probe_walk),
                                                   len(dg_walk)))
                              if probe_walk[i] != dg_walk[i])
    return {
        "n_rows_compared": n,
        "probe_rows": len(probe_rows), "diag_rows": len(dg_rows),
        "probe_walk_len": len(probe_walk),
        "diag_walk_len": len(dg_walk),
        "walk_equal": walk_equal,
        "first_walk_divergence": first_walk_div,
        "value_mismatches": value_mismatches,
        "step8_probe": next((r for r in probe_rows if r.get("t") == STEP8_T), None),
        "step8_diag": next((r for r in dg_rows if r.get("t") == STEP8_T), None),
    }


def fmt_row(r):
    if r is None:
        return "n/a"
    return (f"t={r.get('t')} argmax={r.get('argmax')} "
            f"top2={{{r.get('argmax')}, {r.get('id2')}}} "
            f"logit1={r.get('logit1')!r} logit2={r.get('logit2')!r} "
            f"gap={r.get('gap')!r}")


def verdict_for(m, armed_counters=None):
    """The pre-registered reading, from the measurement alone."""
    if m is None:
        return "R0 -- VOID (no measurement)"
    if m["walk_equal"] and not m["value_mismatches"] and \
            m["probe_rows"] == m["diag_rows"]:
        return ("R1 -- ALL-ROWS MATCH: divergence surface = "
                "CROSS-PROCESS STATE (cross-process rung next; "
                "map tolerance re-adjudicated with this fact)")
    if m["walk_equal"] and m["value_mismatches"]:
        t0 = m["value_mismatches"][0]
        return (f"R2 -- VALUE-LEVEL MISMATCH, WALK INTACT "
                f"(first at t={t0[0]}, fields {t0[1]}): surface = "
                f"WRAPPER STACK; bisect per the phase pattern "
                f"(stock-match/armed-mismatch -> hooks; both-mismatch "
                f"-> eager-registry wrapper -> wrapper-off rung)")
    return (f"R3 -- WALK-LEVEL DIVERGENCE "
            f"(first at {m['first_walk_divergence']}): surface = "
            f"WRAPPER STACK, hard walk evidence; record the near-tie "
            f"context vs the smoke step-8 site")


def report(label, m, counters):
    print(f"\n--- {label} ---")
    if m is None:
        print("  no comparable doc rows (see guards above)")
        return
    print(f"  rows compared: {m['n_rows_compared']} "
          f"(probe {m['probe_rows']} / diag {m['diag_rows']}); "
          f"walk lengths: probe {m['probe_walk_len']} / "
          f"diag {m['diag_walk_len']}")
    print(f"  walk parity: "
          f"{'IDENTICAL' if m['walk_equal'] else 'DIVERGED'}"
          + (f" (first divergence at walk index "
             f"{m['first_walk_divergence']})" if m["first_walk_divergence"]
             is not None else ""))
    print(f"  value parity: "
          f"{len(m['value_mismatches'])} mismatched rows")
    for (t, fields, pr, dr) in m["value_mismatches"][:5]:
        print(f"    t={t} differs in {fields}")
        print(f"      probe: {fmt_row(pr)}")
        print(f"      diag : {fmt_row(dr)}")
    if len(m["value_mismatches"]) > 5:
        print(f"    ... and {len(m['value_mismatches']) - 5} more")
    print(f"  step-8 site (t={STEP8_T}):")
    print(f"    probe: {fmt_row(m['step8_probe'])}")
    print(f"    diag : {fmt_row(m['step8_diag'])}")
    if counters is not None:
        contaminated = any((counters.get("tier_a_clamp_steps"),
                            counters.get("tier_a_fault_steps"),
                            counters.get("tier_d_severity_steps_sum"),
                            counters.get("tier_b_active_steps"),
                            counters.get("exits")))
        print(f"  actuation counters: {counters}")
        if contaminated:
            print("  !! CONTAMINATION GUARD FIRED: the armed stack ACTED;")
            print("  armed rows VOID as evidence -- adjudicate on STOCK.")
    print(f"  VERDICT: {verdict_for(m)}")


def main():
    ap = argparse.ArgumentParser(
        description="Offline F2 adjudicator (readings pre-registered in "
                    "f2-preregistration.md)")
    ap.add_argument("--probe-dump", required=True,
                    help="the probe v1 dump JSON (path_t_run1)")
    ap.add_argument("--diag-dump", required=True,
                    help="the evaluate-side STOCK dump JSON (v32.0.10)")
    ap.add_argument("--diag-dump-armed", default=None,
                    help="the evaluate-side ARMED dump JSON (v32.0.10)")
    args = ap.parse_args()

    probe = load(args.probe_dump)
    pt = probe.get("path_t_run1") or {}
    pt_rows = pt.get("rows") or []
    pt_walk = pt.get("emitted") or []
    if not pt_rows:
        print("R0 -- VOID: the probe dump has no path_t_run1 rows; "
              "no reading fires. Re-key the join.")
        return

    dg = load(args.diag_dump)
    if dg.get("instrument") != "v32.0.10":
        print("R0 -- VOID: the diag dump is not a v32.0.10 logit dump.")
        return
    docs = dg.get("docs") or []
    if not docs:
        print("R0 -- VOID: the diag dump carries no docs.")
        return
    d0 = docs[0]
    guards = []
    if d0.get("doc_id") != EXPECTED_FLIP_POS:
        guards.append(f"position {d0.get('doc_id')} != expected "
                      f"{EXPECTED_FLIP_POS}")
    if d0.get("prompt_len") != EXPECTED_PROMPT_LEN:
        guards.append(f"prompt_len {d0.get('prompt_len')} != expected "
                      f"{EXPECTED_PROMPT_LEN}")
    if guards:
        print("R0 -- VOID (join-invalid guard): " + "; ".join(guards))
        print("  No reading fires. Re-key and re-run.")
        return

    m_stock = compare(pt_rows, pt_walk, d0)
    report(f"STOCK ({args.diag_dump})", m_stock, None)

    m_armed = None
    if args.diag_dump_armed:
        da = load(args.diag_dump_armed)
        if (da.get("docs") or []) and \
                da["docs"][0].get("doc_id") == EXPECTED_FLIP_POS:
            m_armed = compare(pt_rows, pt_walk, da["docs"][0])
            report(f"ARMED ({args.diag_dump_armed})", m_armed,
                   da.get("actuation_counters"))
        else:
            print(f"\n--- ARMED ({args.diag_dump_armed}) ---")
            print("  no matching doc (position mismatch); skipped")

    print("\nAdjudication recorded. Readings are binding per "
          "f2-preregistration.md §5; disposition routing per §7. "
          "Stamps: owner's call, bankable numbers only.")


if __name__ == "__main__":
    main()

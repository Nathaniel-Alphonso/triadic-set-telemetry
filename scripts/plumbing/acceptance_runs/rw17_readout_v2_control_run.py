#!/usr/bin/env python3
"""rw17_readout_v2_control_run.py -- THE REAL-CACHE CONTROL for
triadic_rw17_readout_v2.py (the readout amendment v2 of record: the
owner-stamped specificity refinement, OPTION A -- the persistence-
gated Side C, K = 4; the item-255 control precedent, ledger item 263).

THE CONTROL INPUTS (banked bytes, SHA-pinned below):
  - the three REAL smoke caches received from the Triadic library
    (the RW-17 fresh-corpus smoke walks: math/code/prose, 20 corpus
    docs + the 10 instrument loop fixtures each) + ONE synthetic
    p2corpus-rw17 filler (40 thin-style docs, NO loop fixtures --
    the honest INCONCLUSIVE-POPULATION-GUARD null leg; the open
    receipt of item 255 rides unchanged: the p2 leg's real-bytes
    control is the OWNER-SIDE single adjudication command, where
    the SS4 pins enforce the real bytes);
  - the v1 tool triadic_rw17_readout.py (the item-255 build of
    record, NEVER edited -- the parity law) run on the SAME four
    caches for the V1<->V2 DELTA OF RECORD.

THE RECEIPTS THIS CONTROL PINS:
  (a) the v2 tool's CLI runs clean (--fixture-mode; the pins ECHO,
      never enforce) on the four control caches; the per-leg
      persistence-gate lines + CAVEAT 4 ride the console;
  (b) EVERY exported v2 quantity is EXACT against the banked
      independent gate-aware recompute engine
      rw17_readout_v2_acceptance_run.full_exp_v2 (validated 47/47
      in the acceptance run of record -- the engine-vs-tool law,
      never tool vs tool);
  (c) the V1<->V2 DELTA OF RECORD on real bytes, named leg by leg
      and pinned value for value (the honest delta: the gate
      CHANGES the smoke readings -- a measurement, never an
      adjudication; the smokes are NOT the caches of record):
      - gsmrw17 (C+F): v1 fires 3/10 [5,7,15] KILLED -> v2 fires
        0/10, gap 1.6671 -> 1.3160, catches 8/8 -> 5/8, overlap
        3 -> 8, verdict FAIL -- all three v1 fires gate off
        (N_band < K=4) AND 4 of 8 live loop positives gate off:
        the falsifier's kill vanishes AND the bar now fails -- the
        pre-named honest cost (catch measured never promised);
      - mbpprw17 (F-only): the CODE-LEG IDENTITY -- every leg-block
        quantity v1 == v2 EXACT (the gate NEVER applies where
        Side C is unarmed; only the additive gate_census block
        differs);
      - prose17p-rw17 (C+F): fires UNCHANGED [1,7,11] -- 2 of 3
        fired docs fired THROUGH the gate-off via Side F (docs 1,
        11 NAMED-GATED-OFF; doc 7 PASSES the gate at N_band=4);
        t_leg 1.9426 -> 1.5587, gap 3.0398 -> 1.9743, AUC 1.0 ->
        0.9, catches 8/8 -> 7/8; the leg STAYS KILLED (the count
        form governs over the bar);
      - p2corpus-rw17 (filler): the guard identity v1 == v2
        (n_pos = 0; only gate_census additive);
      - the candidate verdict: over-budget legs [gsmrw17,
        prose17p-rw17] -> [prose17p-rw17]; the guard unchanged;
  (d) the v1 CLI's own readings on the same caches reproduce the
      banked item-255 control readings EXACT (the port-fidelity
      receipt on real bytes);
  (e) the census-pin ECHO receipts (the smokes are NOT the caches
      of record -- three loud echo lines; the math leg 0 == 0);
  (f) the fixture-identity receipt: the 10 loop fixtures
      byte-identical across the three REAL caches;
  (g) determinism: the same-path re-run is byte-identical on BOTH
      the export and the console.

Zero-GPU, read-only, no label joins, NEVER a re-score of the
standing item-256 verdict. Fix-the-fixture-or-the-builder, never
the tool's record. theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); findings
presented, never adjudicated -- the owner's stamps decide.
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rw17_readout_acceptance_run as A1        # noqa: E402
import rw17_readout_v2_acceptance_run as ACC2   # noqa: E402

V2TOOL = ACC2.V2TOOL
V1TOOL = A1.TOOL
PIN_V2TOOL = ("83d26c9863cce4a5ede1becc6729bfcfc20a40e1af33ed9e89e"
              "82d5cee9dbb42")
PIN_V1TOOL = ("c0a0cb62582c48c4fc89e315a3d72a811fac6d2046c3b29694"
              "4d58f51c9dc54b")

FIXDIR = os.path.join(HERE, "rw17_readout_control_fixtures")
SMOKE_MATH = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-math-smoke_bfloat16_bos.jsonl")
SMOKE_CODE = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-code-smoke_bfloat16_bos.jsonl")
SMOKE_PROSE = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-prose-smoke_bfloat16_bos.jsonl")
P2_FILLER = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-p2-synth-filler.jsonl")
PIN_SHA = {
    SMOKE_MATH: ("92462c580e02b578020b670e50300b31156a0704c339f9fdda"
                 "05488e2bb4b215"),
    SMOKE_CODE: ("001445a1d81cfa7fababf021be7df100fa33e06045fb2f811c"
                 "c2b0f259edc0b0"),
    SMOKE_PROSE: ("7f99ff8421cdb55cf96421c14749f280f96360811d6b5def6"
                  "fa5f0d6e47b870d"),
    P2_FILLER: ("d14a01652c513e385439d892eca51ecc1630677b0bec1922d61"
                "7defaf763be91"),
}
CACHES = [SMOKE_MATH, SMOKE_CODE, SMOKE_PROSE, P2_FILLER]
TAG = "rw17-readout-v2-control"
RUNDIR = os.path.join(HERE, ".scratch", "rw17_readout_v2_control_run")
OUT_V2 = os.path.join(RUNDIR, "rw17_readout_v2_control_export.json")
OUT_V1 = os.path.join(RUNDIR, "rw17_readout_v1_on_control_caches.json")

# the v2 real-bytes readings of record (this control's own
# deterministic measurements on the banked smoke caches; round10)
V2_READINGS = {
    "gsmrw17": {"t_leg": 1.2279071737, "t_esc": 1.5520531244,
                "fires": 0, "n": 10, "gap": 1.3160439382,
                "auc": 0.8125, "catches": 5, "n_live": 8,
                "overlap": 8, "typing": "FAIL"},
    "mbpprw17": {"t_leg": 1.5226219005, "t_esc": 1.6965394428,
                 "fires": 0, "n": 10, "gap": 2.2663178754,
                 "auc": 0.9625, "catches": 7, "n_live": 8,
                 "overlap": 3, "typing": "PASS_2SIGMA"},
    "prose17p-rw17": {"t_leg": 1.5587205193, "t_esc": 1.6813877832,
                      "fires": 3, "n": 10, "gap": 1.9743003703,
                      "auc": 0.9, "catches": 7, "n_live": 8,
                      "overlap": 5,
                      "typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"},
    "p2corpus-rw17": {"fires": 0, "n": 20, "catches": 0, "n_live": 0,
                      "gap": None, "auc": None,
                      "typing": "INCONCLUSIVE-POPULATION-GUARD"},
}
# the banked item-255 v1 control readings (the port-fidelity receipt)
V1_READINGS = {
    "gsmrw17": {"fires": 3, "n": 10, "gap": 1.6671212963,
                "auc": 0.8125, "catches": 8, "n_live": 8,
                "typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"},
    "mbpprw17": {"fires": 0, "n": 10, "gap": 2.2663178754,
                 "auc": 0.9625, "catches": 7, "n_live": 8,
                 "typing": "PASS_2SIGMA"},
    "prose17p-rw17": {"fires": 3, "n": 10, "gap": 3.0398015748,
                      "auc": 1.0, "catches": 8, "n_live": 8,
                      "typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"},
    "p2corpus-rw17": {"fires": 0, "n": 20, "catches": 0, "n_live": 0,
                      "gap": None, "auc": None,
                      "typing": "INCONCLUSIVE-POPULATION-GUARD"},
}
# the V1<->V2 delta of record, pinned value for value
DELTA = {
    "gsmrw17": {
        "v1_fired": [5, 7, 15], "v2_fired": [],
        "v1_t_leg": 1.5664524175, "v2_t_leg": 1.2279071737,
        "v1_gap": 1.6671212963, "v2_gap": 1.3160439382,
        "v1_catches": 8, "v2_catches": 5,
        "v1_overlap": 3, "v2_overlap": 8,
        "v1_typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
        "v2_typing": "FAIL",
        "gate": {"calibration_gated": 9, "held_out_gated": 10,
                 "loop_live_gated": 4, "fired_gated": 0},
    },
    "prose17p-rw17": {
        "v1_fired": [1, 7, 11], "v2_fired": [1, 7, 11],
        "v1_t_leg": 1.9425920957, "v2_t_leg": 1.5587205193,
        "v1_gap": 3.0398015748, "v2_gap": 1.9743003703,
        "v1_auc": 1.0, "v2_auc": 0.9,
        "v1_catches": 8, "v2_catches": 7,
        "v1_overlap": 0, "v2_overlap": 5,
        "v1_typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
        "v2_typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
        "gate": {"calibration_gated": 8, "held_out_gated": 8,
                 "loop_live_gated": 3, "fired_gated": 2},
        "fired_views": {1: (False, "NAMED-GATED-OFF (N_band=2 < K=4)"),
                        7: (True, "PASS (N_band=4 >= K=4)"),
                        11: (False,
                             "NAMED-GATED-OFF (N_band=3 < K=4)")},
    },
}

CHECKS = []


def check(fam, name, ok, detail=""):
    ok = bool(ok)
    CHECKS.append((fam, name, ok, detail))
    print(f"  [{fam}] {'PASS' if ok else 'FAIL'} -- {name}"
          + (f"  [{detail}]" if (detail and not ok) else ""))
    return ok


def run_cli(tool, out):
    cmd = [sys.executable, tool, "--fixture-mode"]
    for c in CACHES:
        cmd += ["--cache", c]
    cmd += ["--tag", TAG, "--out", out]
    return subprocess.run(cmd, capture_output=True, text=True)


def fired_ids(legblock):
    return sorted(d["doc_id"] for d in legblock["held_out"]["fired_docs"])


def r10(x):
    return None if x is None else round(x, 10)


def leaf_diffs(a, b, path="", skip=()):
    """Recursive leaf-level diff v1 -> v2, SKIPPING the named
    v2-only additive keys (c_gate_on / side_c_gate / gate_census:
    the v2 census fields; and pop-match keys named for the caller)."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in skip:
                continue
            out += leaf_diffs(a.get(k), b.get(k), f"{path}.{k}", skip)
        return out
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f"len {len(a)}", f"len {len(b)}"))
            return out
        for i, (x, y) in enumerate(zip(a, b)):
            out += leaf_diffs(x, y, f"{path}[{i}]", skip)
        return out
    if a != b:
        out.append((path, a, b))
    return out


def main():
    print("=" * 78)
    print("=== THE RW-17 READOUT AMENDMENT V2 CONTROL RUN (real smoke")
    print("    bytes; the item-255 control precedent + the V1<->V2")
    print("    DELTA OF RECORD) ===")
    print("  tool under test: triadic_rw17_readout_v2.py (the")
    print("    persistence-gated Side C, K = 4 -- owner-stamped")
    print("    Option A of the refinement sheet, item 260)")
    print("  contrast tool: triadic_rw17_readout.py (the item-255")
    print("    build of record, never edited -- the parity law)")
    print("  LAW: every exported quantity EXACT vs the banked")
    print("  independent gate-aware recompute engine (47/47 in the")
    print("  acceptance of record); fix-the-fixture-or-the-builder,")
    print("  never the tool's record; NEVER a re-score of item 256.")

    # (0) the banked pins
    for path, sha in PIN_SHA.items():
        check("C0", f"the banked control input "
              f"{os.path.basename(path)} carries its pinned SHA-256",
              A1.r_sha256_file(path) == sha, A1.r_sha256_file(path))
    check("C0", "the v2 tool carries its build-of-record SHA-256 "
          "(item 263's build pin)",
          A1.r_sha256_file(V2TOOL) == PIN_V2TOOL, A1.r_sha256_file(V2TOOL))
    check("C0", "the v1 tool carries its item-255 build pin UNTOUCHED "
          "(the parity law)",
          A1.r_sha256_file(V1TOOL) == PIN_V1TOOL, A1.r_sha256_file(V1TOOL))

    if os.path.exists(RUNDIR):
        shutil.rmtree(RUNDIR)
    os.makedirs(RUNDIR)

    # (a) the v2 tool runs clean on the real bytes
    p1 = run_cli(V2TOOL, OUT_V2)
    if not check("C1", "the v2 tool CLI runs clean on the three REAL "
                 "smoke caches + the filler (fixture mode, pins "
                 "echoed never enforced)",
                 p1.returncode == 0, p1.stderr[-400:]):
        return finish()
    console1 = p1.stdout
    with open(OUT_V2) as f:
        got2 = json.load(f)

    # (b) every exported v2 quantity EXACT vs the independent engine
    exp2 = ACC2.full_exp_v2(CACHES, TAG)
    errs = []
    A1.cmp_tree(exp2, got2, "", errs)
    check("C2", "the v2 export == the independent gate-aware "
          "recompute EXACT on the REAL bytes (every field, every "
          "leg, every doc, order-exact)",
          not errs, f"{len(errs)} diff(s): " + "; ".join(errs[:5]))

    # (c1) the v2 real-bytes readings of record
    for leg, rd in V2_READINGS.items():
        lb = got2["legs"][leg]
        gap = lb["separation_context"]["sigma_gap_on_D"]
        auc = lb["separation_context"]["auc_on_D"]
        ok = (lb["held_out"]["fires"] == rd["fires"]
              and lb["held_out"]["n"] == rd["n"]
              and lb["loop_catches"]["at_t_leg"] == rd["catches"]
              and lb["loop_catches"]["n_live"] == rd["n_live"]
              and lb["verdict"]["typing_presented"] == rd["typing"]
              and r10(gap) == rd["gap"] and r10(auc) == rd["auc"])
        if "t_leg" in rd:
            ok = ok and r10(lb["thresholds"]["t_leg"]) == rd["t_leg"]
            ok = ok and r10(lb["thresholds"]["t_esc"]) == rd["t_esc"]
            ok = ok and (lb["loop_floor_overlap_line"]
                         ["n_clean_at_or_above"] == rd["overlap"])
        check("C3", f"leg {leg} v2 reading of record: fires "
              f"{rd['fires']}/{rd['n']}, catches {rd['catches']}/"
              f"{rd['n_live']}, gap {rd['gap']}, AUC {rd['auc']}"
              f" -> {rd['typing']}", ok,
              f"measured fires {lb['held_out']['fires']}, gap {gap}, "
              f"auc {auc}, typing "
              f"{lb['verdict']['typing_presented']}")

    # (c2) the V1<->V2 delta of record -- the v1 CLI on the same bytes
    pv1 = run_cli(V1TOOL, OUT_V1)
    if not check("C4", "the v1 tool CLI runs clean on the SAME four "
                 "caches (the parity law; the contrast of record)",
                 pv1.returncode == 0, pv1.stderr[-400:]):
        return finish()
    console_v1 = pv1.stdout
    with open(OUT_V1) as f:
        got1 = json.load(f)
    exp1 = A1.full_exp(CACHES, TAG)
    errs = []
    A1.cmp_tree(exp1, got1, "", errs)
    check("C4", "the v1 export == the banked item-255 independent "
          "recompute EXACT on the same REAL bytes (the port-fidelity "
          "receipt re-proven at the v2 control)",
          not errs, f"{len(errs)} diff(s): " + "; ".join(errs[:5]))

    # (d) the v1 readings reproduce the banked item-255 readings
    for leg, rd in V1_READINGS.items():
        lb = got1["legs"][leg]
        gap = lb["separation_context"]["sigma_gap_on_D"]
        auc = lb["separation_context"]["auc_on_D"]
        ok = (lb["held_out"]["fires"] == rd["fires"]
              and lb["held_out"]["n"] == rd["n"]
              and lb["loop_catches"]["at_t_leg"] == rd["catches"]
              and lb["loop_catches"]["n_live"] == rd["n_live"]
              and lb["verdict"]["typing_presented"] == rd["typing"]
              and r10(gap) == rd["gap"] and r10(auc) == rd["auc"])
        check("C4", f"leg {leg} v1 reading reproduces the banked "
              f"item-255 control reading EXACT (fires {rd['fires']}/"
              f"{rd['n']}, gap {rd['gap']}, AUC {rd['auc']} -> "
              f"{rd['typing']})", ok,
              f"measured fires {lb['held_out']['fires']}, gap {gap}, "
              f"auc {auc}, typing "
              f"{lb['verdict']['typing_presented']}")

    # (e) the code-leg identity: the mbpp leg block v1 == v2 except
    # the additive gate fields (the gate NEVER applies on the F-only
    # leg; the raw c_gate_on census fields ride as N/A-named additive)
    l1, l2 = got1["legs"]["mbpprw17"], got2["legs"]["mbpprw17"]
    diffs = leaf_diffs(l1, l2, "",
                       skip=("gate_census", "c_gate_on", "side_c_gate"))
    na_ok = all(d.get("side_c_gate")
                == "N/A (Side C unarmed on this leg)"
                for d in l2["populations"]["loops_live"])
    check("C4", "THE CODE-LEG IDENTITY: the mbpp leg block is "
          "v1 == v2 at EVERY leaf except the additive gate fields "
          "(gate_census + the per-doc c_gate_on/side_c_gate census "
          "fields, all NAMED N/A -- the gate never applies where "
          "Side C is unarmed; every D, every summary, every "
          "quantity UNCHANGED)",
          not diffs and na_ok and len(l2["populations"]["loops_live"])
          == 8,
          f"{len(diffs)} leaf diff(s): "
          + "; ".join(f"{p} {a}!={b}" for p, a, b in diffs[:5]))
    # the filler guard identity: only the two mean_D summary leaves
    # ride the gated D (pinned, measured); every other leaf v1 == v2
    l1, l2 = got1["legs"]["p2corpus-rw17"], got2["legs"]["p2corpus-rw17"]
    diffs = leaf_diffs(l1, l2, "",
                       skip=("gate_census", "c_gate_on", "side_c_gate"))
    expected_mean_D = {
        ".populations.summaries_at_0.90.calibration_half_clean.mean_D":
            0.4044542538803239,
        ".populations.summaries_at_0.90.held_out_clean_nonfired.mean_D":
            -0.18343863003015937,
    }
    ok_guard = (sorted(p for p, _a, _b in diffs)
               == sorted(expected_mean_D)
               and all(b == expected_mean_D[p]
                       for p, _a, b in diffs))
    check("C4", "the filler guard identity: the p2 leg block is "
          "v1 == v2 at EVERY leaf except gate_census and the TWO "
          "mean_D summary leaves riding the gated D (calibration "
          "0.4045, held-out nonfired -0.1834 -- the measured gate "
          "effect on the armed-but-guarded filler; n_pos = 0, the "
          "honest INCONCLUSIVE-POPULATION-GUARD null leg unchanged)",
          ok_guard,
          f"{len(diffs)} leaf diff(s): "
          + "; ".join(f"{p} {a}->{b}" for p, a, b in diffs[:5]))

    # (f) the gsm delta of record
    d = DELTA["gsmrw17"]
    lb1, lb2 = got1["legs"]["gsmrw17"], got2["legs"]["gsmrw17"]
    ok = (fired_ids(lb1) == d["v1_fired"]
          and fired_ids(lb2) == d["v2_fired"]
          and r10(lb1["thresholds"]["t_leg"]) == d["v1_t_leg"]
          and r10(lb2["thresholds"]["t_leg"]) == d["v2_t_leg"]
          and r10(lb1["separation_context"]["sigma_gap_on_D"]) == d["v1_gap"]
          and r10(lb2["separation_context"]["sigma_gap_on_D"]) == d["v2_gap"]
          and lb1["loop_catches"]["at_t_leg"] == d["v1_catches"]
          and lb2["loop_catches"]["at_t_leg"] == d["v2_catches"]
          and lb1["loop_floor_overlap_line"]["n_clean_at_or_above"]
          == d["v1_overlap"]
          and lb2["loop_floor_overlap_line"]["n_clean_at_or_above"]
          == d["v2_overlap"]
          and lb1["verdict"]["typing_presented"] == d["v1_typing"]
          and lb2["verdict"]["typing_presented"] == d["v2_typing"])
    gc = lb2["gate_census"]
    ok = ok and all(gc[k] == v for k, v in d["gate"].items())
    check("C4", "THE GSM DELTA OF RECORD: v1 fires 3/10 [5,7,15] "
          "KILLED -> v2 fires 0/10 (all three gated off, N_band < 4), "
          "gap 1.6671 -> 1.3160, catches 8/8 -> 5/8 (4 live loop "
          "positives gate off), overlap 3 -> 8, verdict KILLED -> "
          "FAIL -- the falsifier's kill vanishes AND the bar now "
          "fails: the pre-named honest cost (catch measured never "
          "promised), a measurement never an adjudication",
          ok, "see measured values above")
    # every gated-off doc view names itself honestly
    gv = {dv["doc_id"]: dv for dv in lb2["held_out"]["fired_docs"]}
    check("C4", "the gsm gate census rides NAMED (calibration 9, "
          "held-out 10, loops 4, fired-through-gate-off 0) and no "
          "v2 fired doc exists to name",
          gc["side_c_armed"] is True and not gv, "unexpected fired docs")

    # (g) the prose delta of record
    d = DELTA["prose17p-rw17"]
    lb1, lb2 = got1["legs"]["prose17p-rw17"], got2["legs"]["prose17p-rw17"]
    ok = (fired_ids(lb1) == d["v1_fired"]
          and fired_ids(lb2) == d["v2_fired"]
          and r10(lb1["thresholds"]["t_leg"]) == d["v1_t_leg"]
          and r10(lb2["thresholds"]["t_leg"]) == d["v2_t_leg"]
          and r10(lb1["separation_context"]["sigma_gap_on_D"]) == d["v1_gap"]
          and r10(lb2["separation_context"]["sigma_gap_on_D"]) == d["v2_gap"]
          and r10(lb1["separation_context"]["auc_on_D"]) == d["v1_auc"]
          and r10(lb2["separation_context"]["auc_on_D"]) == d["v2_auc"]
          and lb1["loop_catches"]["at_t_leg"] == d["v1_catches"]
          and lb2["loop_catches"]["at_t_leg"] == d["v2_catches"]
          and lb1["loop_floor_overlap_line"]["n_clean_at_or_above"]
          == d["v1_overlap"]
          and lb2["loop_floor_overlap_line"]["n_clean_at_or_above"]
          == d["v2_overlap"]
          and lb1["verdict"]["typing_presented"] == d["v1_typing"]
          and lb2["verdict"]["typing_presented"] == d["v2_typing"])
    gc = lb2["gate_census"]
    ok = ok and all(gc[k] == v for k, v in d["gate"].items())
    fv = {dv["doc_id"]: dv for dv in lb2["held_out"]["fired_docs"]}
    ok = ok and sorted(fv) == d["v2_fired"]
    for doc_id, (on, string) in d["fired_views"].items():
        ok = ok and doc_id in fv and fv[doc_id].get("c_gate_on") is on \
            and fv[doc_id].get("side_c_gate") == string
    check("C4", "THE PROSE DELTA OF RECORD: fires UNCHANGED [1,7,11] "
          "-- 2 of 3 fired docs fired THROUGH the gate-off via Side F "
          "(docs 1, 11 NAMED-GATED-OFF; doc 7 PASSES at N_band=4); "
          "t_leg 1.9426 -> 1.5587, gap 3.0398 -> 1.9743, AUC 1.0 -> "
          "0.9, catches 8/8 -> 7/8, overlap 0 -> 5; the leg STAYS "
          "KILLED (the count form governs over the bar)",
          ok, "see measured values above")

    # (g2) THE LEAF-CONFINEMENT LAW on both C-armed delta legs: every
    # differing leaf sits inside a gate-measured block -- NO parity,
    # census, loop_population, level_set, z_baselines, armed_sides or
    # populations-count leaf ever moved
    ALLOWED = ("thresholds", "separation_context", "held_out",
               "loop_catches", "loop_floor_overlap_line",
               "populations", "forensics", "verdict")
    for leg in ("gsmrw17", "prose17p-rw17"):
        diffs = leaf_diffs(got1["legs"][leg], got2["legs"][leg], "",
                           skip=("gate_census", "c_gate_on",
                                 "side_c_gate"))
        stray = [p for p, _a, _b in diffs
                 if p.split(".")[1] not in ALLOWED]
        check("C4", f"leg {leg} the leaf-confinement law: every "
              f"differing leaf v1 -> v2 sits inside a gate-measured "
              f"block (thresholds / separation_context / held_out / "
              f"loop_catches / overlap line / populations / "
              f"forensics / verdict) -- the parity block, the "
              f"census, the loop_population, the level-set receipt, "
              f"the z_baselines, the armed_sides and the "
              f"populations' non-D counts are v1 == v2 EXACT",
              not stray,
              f"stray leaf diff(s): {stray[:5]}")

    # (h) the candidate-verdict delta + the additive-only top law
    pcv1, pcv2 = got1["presented_candidate_verdict"], \
        got2["presented_candidate_verdict"]
    check("C4", "the candidate verdict delta: over-budget legs "
          "[gsmrw17, prose17p-rw17] -> [prose17p-rw17] (the gsm "
          "kill vanishes under the gate; the prose kill stands); the "
          "guard legs unchanged [p2corpus-rw17]",
          pcv1["verdict_presented"] == "CANDIDATE-KILLED-"
          "FALSE-ALARM-BUDGET"
          and pcv2["verdict_presented"] == "CANDIDATE-KILLED-"
          "FALSE-ALARM-BUDGET"
          and pcv1["over_budget_legs"] == ["gsmrw17", "prose17p-rw17"]
          and pcv2["over_budget_legs"] == ["prose17p-rw17"]
          and pcv1["population_guard_legs"] == ["p2corpus-rw17"]
          and pcv2["population_guard_legs"] == ["p2corpus-rw17"])
    # every top-level block other than the named additive/delta ones
    # is v1 == v2 EXACT
    SKIP_TOP = {"tool", "tool_sha256", "mode", "prereg", "construction",
                "presented_candidate_verdict", "legs"}
    bad = []
    for k in set(got1) | set(got2):
        if k in SKIP_TOP:
            continue
        if got1.get(k) != got2.get(k):
            bad.append(k)
    c1 = dict(got1["construction"])
    c2 = dict(got2["construction"])
    c2.pop("refinement_v2", None)
    v1cav = dict(pcv1["caveats"])
    v2cav = dict(pcv2["caveats"])
    v2cav.pop("refinement_disclosure", None)
    check("C4", "the additive-only top law: every top-level block "
          "other than the named v2/delta blocks is v1 == v2 EXACT "
          "(the inputs, the censuses, the excluded-empties receipt, "
          "the fixture-identity receipt, the SEC definition, the "
          "theta note, the RW-14 rider); construction differs ONLY "
          "by refinement_v2; the caveats differ ONLY by "
          "refinement_disclosure; the legs-level differences are "
          "confined to the per-leg laws above (the mbpp/p2 identity "
          "receipts + the gsm/prose delta pins + the "
          "leaf-confinement law)",
          not bad and c1 == c2 and v1cav == v2cav,
          f"unexpected diffs: {bad}")
    check("C4", "the v2 additive blocks of record: construction."
          "refinement_v2 (option OPTION A, the pinned refinement "
          "sheet SHA, k_gate 4) + the four caveats incl. "
          "refinement_disclosure + the v2 prereg string naming the "
          "refinement sheet",
          got2["construction"]["refinement_v2"]["option"].startswith(
              "OPTION A")
          and got2["construction"]["refinement_v2"]["k_gate"] == 4
          and got2["construction"]["refinement_v2"]
          ["refinement_sheet_sha256"] == ACC2.REFINEMENT_SHA
          and sorted(got2["presented_candidate_verdict"]["caveats"])
          == ["development_data_disclosure", "fixed_fixtures_line",
              "fresh_census_line", "refinement_disclosure"]
          and "rw17-specificity-refinement-preregistration.md" in
          got2["prereg"])

    # (i) the census-pin ECHO receipts
    n_echo = console1.count("CENSUS PIN ECHO")
    echo_ok = n_echo == 3
    for leg, pin in (("mbpprw17", 1), ("prose17p-rw17", 3),
                     ("p2corpus-rw17", 95)):
        echo_ok = echo_ok and f"leg {leg}" in console1 \
            and f"measured fresh census is 0 EOS@step0 doc(s) != the " \
                f"item-254 expected census of record {pin}" in console1
    check("C5", "the census-pin ECHO receipts: the smoke corpora "
          "carry ZERO EOS@step0 docs vs the expected pins -- three "
          "loud echo lines (mbpp 1, prose 3, p2 95); the math leg's "
          "0 == its pin 0, no echo; echoed in fixture mode, NEVER "
          "silently pooled", echo_ok, f"{n_echo} echo line(s)")
    check("C5", "the math leg's census receipt: measured 0 == the "
          "item-254 pin 0 (no echo, receipts empty)",
          got2["legs"]["gsmrw17"]["census"]["measured_eos_step0"] == 0
          and got2["legs"]["gsmrw17"]["census"]["receipts"] == [])

    # (j) the fixture-identity receipt
    fir = got2["fixture_identity_receipt"]
    check("C6", "the fixture-identity receipt: the 10 loop fixtures "
          "byte-identical across the three REAL smoke caches",
          fir["n_loop_fixtures"] == 10
          and fir["copies_byte_identical"] is True)

    # (k) the console gate lines + CAVEAT 4
    gate_ok = (
        "persistence gate (K=4): NAMED-GATED-OFF calibration 9/10 | "
        "held-out 10/10 | loops 4/8 | fired-through-gate-off 0/0"
        in console1
        and "persistence gate (K=4): N/A on this leg (Side C unarmed "
            "-- the F-only code leg)" in console1
        and "persistence gate (K=4): NAMED-GATED-OFF calibration 8/10 "
            "| held-out 8/10 | loops 3/8 | fired-through-gate-off 2/3"
        in console1
        and "persistence gate (K=4): NAMED-GATED-OFF calibration 14/20 "
            "| held-out 18/20 | loops 0/0 | fired-through-gate-off 0/0"
        in console1
        and "CAVEAT 4 (the refinement disclosure)" in console1)
    check("C7", "the console rides the per-leg persistence-gate "
          "lines (gsm 9/10-10/10-4/8-0/0; mbpp N/A; prose 8/10-8/10-"
          "3/8-2/3; p2 14/20-18/20-0/0-0/0) + CAVEAT 4 verbatim",
          gate_ok)

    # (l) determinism
    with open(OUT_V2, "rb") as f:
        first_bytes = f.read()
    p2run = run_cli(V2TOOL, OUT_V2)
    with open(OUT_V2, "rb") as f:
        second_bytes = f.read()
    check("C8", "determinism: the same-path v2 re-run export is "
          "byte-identical AND the console output byte-identical "
          "across the two runs",
          p2run.returncode == 0 and first_bytes == second_bytes
          and len(first_bytes) > 0 and console1 == p2run.stdout)
    return finish()


def finish():
    print("\n" + "=" * 78)
    n_fail = sum(1 for c in CHECKS if not c[2])
    fams = []
    for fam, _n, _ok, _d in CHECKS:
        if fam not in fams:
            fams.append(fam)
    for fam in fams:
        ft = sum(1 for c in CHECKS if c[0] == fam)
        fp = sum(1 for c in CHECKS if c[0] == fam and c[2])
        print(f"  {fam}: {fp}/{ft} PASS")
    print(f"\n  TOTAL: {len(CHECKS) - n_fail}/{len(CHECKS)} PASS, "
          f"{n_fail} FAIL")
    if n_fail:
        print("\n  FAILURES (named, never silent):")
        for fam, name, ok, detail in CHECKS:
            if not ok:
                print(f"   [{fam}] {name}"
                      + (f" -- {detail}" if detail else ""))
    print("\n  Fix-the-fixture-or-the-builder, never the tool's "
          "record.")
    print("  theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); findings presented, "
          "never")
    print("  adjudicated -- the owner's stamps decide.")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

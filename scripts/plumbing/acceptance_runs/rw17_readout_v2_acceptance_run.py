#!/usr/bin/env python3
"""rw17_readout_v2_acceptance_run.py -- THE ACCEPTANCE RUN for
triadic_rw17_readout_v2.py (THE READOUT AMENDMENT V2 OF RECORD: the
my stamped specificity refinement OPTION A -- the persistence-
gated Side C, K=4; the stamped refinement sheet
rw17-specificity-refinement-preregistration.md, SHA-256
c03dffed4ca13210ee5df7c7c27f9b065abfd128be7311b4fb6948e413d36c29,
stamped by me at ledger item 260; the item-255 acceptance pattern).

THE LAW THIS RUNNER ENFORCES (the item-255 pattern, unchanged): every
family drives the REAL v2 TOOL through its own CLI and compares EXACT
against THIS RUNNER'S OWN independent recomputation -- the v1
acceptance run's banked engine (rw17_readout_acceptance_run.py,
validated 90/90 against the v1 tool in its acceptance run of record)
is IMPORTED for the world-builder + the arithmetic helpers, and the
v2 recompute below is THIS RUNNER'S OWN gate-aware extension of that
engine (never the tool's functions); the v1 tool's own CLI is the
PORT-FIDELITY oracle. Fix-the-fixture-or-the-builder, never the
tool's record; the v1 build of record is never touched.

THE FAMILIES:
  F1  the clean four-leg V-PASS world through the v2 CLI: every
      exported quantity EXACT vs the independent v2 recompute (the
      gate active, as measured on the world);
  F2  THE GATE LAW per exported doc view: a gated-off Side C means
      D == z_F on C+F legs; a passing gate means D == max(z_C, z_F);
      the F-only code leg means D == z_F everywhere with the N/A
      census string -- plus the NAMED-GATED census strings exact;
  F3  PORT FIDELITY: the all-flat-PR world (every C-armed doc's
      N_band = n_steps >= K=4 -- NO doc gated): the v1 CLI and the
      v2 CLI run on the SAME world and every inherited quantity is
      EXACT-equal; the v2-only additive fields carry their expected
      values (PASS strings / N/A on the code leg);
  F4  THE GATE-EFFECT WORLD: a single-PR-spike held-out doc (N_band
      = 1 -- the item-243/257 boundary-spike anchor shape) that the
      v1 construction FIRES through Side C: the v2 gate EXCLUDES it
      (D == z_F), the doc is absent from the v2 fired docs, the
      t_leg is re-derived on the gated D (recomputed independently,
      and DIFFERENT from v1's -- the operating point moved, named
      honestly), and the level-set receipt holds on the gated D;
  F5  every inherited hard exit fires loud through the v2 CLI
      (truncated cache / duplicate record / missing leg / unexpected
      leg / degenerate calibration / the real-mode pin refusal);
  F6  determinism: the same-path re-run byte-identical on BOTH the
      export and the console;
  F7  the constants echo: K_GATE = 4, the refinement sheet's pinned
      SHA, the RW-17 sheet's pinned SHA unchanged, the arming table
      unchanged, the fresh1 echo constants carried with the honest
      echo note, the four caveat lines, the V2 mode line;
  F8  the verdict-knob worlds (V-NEAR / V-JITTER / V-FAIL from the
      v1 knobs) through the v2 CLI: every quantity EXACT vs the
      independent v2 recompute (the typings come out AS MEASURED
      under the gate -- named honestly, never forced).

Zero-GPU; no label joins; the loop fixtures byte-identical within
every world (the item-213 Stamp-2 law, inherited). theta [REDACTED_PER_PUBLICATION_POLICY]
unmoved (D-theta); no thresholds set, moved, or adjudicated; findings
presented, never adjudicated -- my stamps decide.
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rw17_readout_acceptance_run as A1   # noqa: E402 -- the banked
# independent recompute engine (its main() runs only under __main__)

V2TOOL = os.path.join(HERE, "triadic_rw17_readout_v2.py")
V1TOOL = A1.TOOL
K_GATE = 4
REFINEMENT_SHA = ("c03dffed4ca13210ee5df7c7c27f9b065abfd128be7311b4"
                  "fb6948e413d36c29")
LEGS = A1.LEGS
R_ARMED = A1.R_ARMED
BAND_KEY = f"{A1.R_SEC_BAND_FACTOR:.2f}"

V2_MODE_TYPE = ("ADJUDICATION READOUT AMENDMENT V2 OF RECORD (THE "
                "SPECIFICITY REFINEMENT, MY-STAMPED OPTION A: THE "
                "PERSISTENCE-GATED SIDE C, K=4) -- PRESENTED, NEVER "
                "ADJUDICATED; MY STAMPS DECIDE")

# the v2-only fixed blocks (transcribed from the v2 tool's pinned
# bytes; any divergence FAILS the tree compare loudly -- the runner
# is fixed runner-side, never the tool)
FIXED_REFINEMENT_V2 = {
    "option": ("OPTION A -- THE PERSISTENCE-GATED SIDE C (the "
               "my stamped refinement sheet, ledger item 260)"),
    "refinement_sheet_sha256": REFINEMENT_SHA,
    "k_gate": K_GATE,
    "gate_law": ("Side C contributes to D only when N_band(0.90) >= "
                 "K=4 (pinned from PRIOR data only -- the "
                 "item-243/257 anchors); z_C itself UNCHANGED; a "
                 "gated-off Side C contributes -inf to D (exactly "
                 "the unarmed-side law); Side F unchanged; the SEC "
                 "annotations ride unchanged; gated docs censused "
                 "NAMED-GATED, never silent; t_leg re-derived on "
                 "the gated D (the calibration half's clean-gated-D "
                 "quantile -- the level-set guarantee holds by "
                 "construction); the gate NEVER applies on the "
                 "F-only code leg (Side C unarmed already)"),
    "development_data_disclosure": (
        "the refinement's constants (K=4) pin from PRIOR data only "
        "(the banked old anchors + the fresh forensics); the fresh "
        "corpora thereby become DEVELOPMENT DATA for the "
        "refinement; its own adjudication is the fresh3 generation "
        "(new prompts, never re-walks -- the refinement sheet SS6, "
        "the item-228 determinism law)"),
    "echo_constants_note": (
        "PINNED_CACHE_SHA + EXPECTED_FRESH_CENSUS carry the fresh1 "
        "values of record (the item-253/254 pins); the fresh3 "
        "adjudication pins (the fresh3 cache SHAs + the measured "
        "fresh3 censuses) ride a planned PRE-BANK echo-constant "
        "update at the fresh3 walk-receipt phase, BEFORE the single "
        "adjudication command -- the same lifecycle as v1 (built "
        "after its walks landed); never guessed"),
}
FIXED_GATE_CENSUS_LAW = (
    "gated-off Side C docs censused NAMED-GATED, never silent (the "
    "stamped refinement sheet); the gate NEVER applies on the "
    "F-only code leg (Side C unarmed); a gated-off doc can still "
    "fire through Side F on C+F legs -- typed in fired_gated, "
    "never hidden")
V2_CAVEATS = dict(A1.FIXED_CAVEATS)
V2_CAVEATS["refinement_disclosure"] = (
    "the refinement (my stamped Option A: the "
    "persistence-gated Side C, K=4) pins from PRIOR data only (the "
    "item-243/257 anchors); the fresh corpora thereby become "
    "DEVELOPMENT DATA for the refinement; its own adjudication is "
    "the fresh3 generation (new prompts, never re-walks -- the "
    "refinement sheet SS6, the item-228 determinism law); this v2 "
    "amendment NEVER re-scores the standing item-256 verdict")
V2_PREREG = (A1.FIXED_TOP["prereg"]
             + " + THE REFINEMENT SHEET "
               "rw17-specificity-refinement-preregistration.md "
               "(stamped by me OPTION A at ledger item 260; sheet "
               f"SHA-256 {REFINEMENT_SHA})")


# =========================================================================
# THE INDEPENDENT V2 RECOMPUTE (this runner's own gate-aware engine:
# the v1 acceptance engine's helpers + the gate law, never the
# tool's functions).
# =========================================================================
def gate_state(d):
    """(c_gate_on, band) from the doc's OWN SEC-1 band at 0.90."""
    p = A1.r_sec_profile(d)
    band = p["band"][BAND_KEY] if p else None
    n_band = band["N_band"] if band else None
    return (n_band is not None and n_band >= K_GATE), band


def gate_string(d, leg, band):
    """The NAMED-GATED / PASS census string (the tool's law, as an
    independent transcription)."""
    n_band = band["N_band"] if band else None
    if "C" not in R_ARMED[leg]:
        return "N/A (Side C unarmed on this leg)"
    if d.get("c_gate_on"):
        return f"PASS (N_band={n_band} >= K={K_GATE})"
    if n_band is not None:
        return f"NAMED-GATED-OFF (N_band={n_band} < K={K_GATE})"
    return ("NAMED-GATED-OFF (no SEC band -- no non-None "
            "PR_sig steps)")


def r_doc_view_v2(d, leg):
    v = A1.r_doc_view(d, leg)
    _on, band = gate_state(d)
    v["c_gate_on"] = d.get("c_gate_on")
    v["side_c_gate"] = gate_string(d, leg, band)
    return v


def recompute_v2(cache_paths, tag):
    """The full independent gate-aware recompute: the expected export."""
    import math
    legs_docs, loop_by_leg, inputs, excluded_empty = {}, {}, [], []
    fixture_copies = {}
    for path in cache_paths:
        sha = A1.r_sha256_file(path)
        docs, empty = A1.r_load_cache(path)
        excluded_empty.extend(
            {"set": "walks", "cache": os.path.basename(path),
             "leg": r["leg"], "doc_id": r["doc_id"]} for r in empty)
        cache_loop = [r for r in docs if r["leg"] == "loop"]
        for r in cache_loop:
            fixture_copies.setdefault(r["doc_id"], {})[
                os.path.basename(path)] = r
        cache_legs = sorted({r["leg"] for r in docs if r["leg"] != "loop"})
        entry = {"path": os.path.basename(path), "sha256": sha,
                 "n_records": len(docs) + len(empty),
                 "n_empty_form": len(empty), "pin": None}
        for leg in cache_legs:
            loop_by_leg[leg] = cache_loop
            legs_docs[leg] = [r for r in docs if r["leg"] == leg]
            name, pin = A1.PINNED_CACHE_SHA[leg]
            entry["pin"] = {"leg": leg, "pinned_file": name,
                            "pinned_sha256": pin, "match": sha == pin}
        inputs.append(entry)

    exp_legs = {}
    near_bar_legs, failed_legs, jitter_legs = [], [], []
    any_guard = any_over_budget = False
    all_pass = True
    for leg in LEGS:
        corpus = legs_docs[leg]
        census_out, keep, removed = [], [], []
        for d in corpus:
            if d["n_gen_steps"] == 0:
                removed.append(d)
                census_out.append({
                    "doc_id": d["doc_id"], "present": True,
                    "n_gen_steps": d["n_gen_steps"],
                    "n_content_steps": d["n_content_steps"],
                    "n_commits": len(d["commits"]),
                    "stop_reason": d.get("stop_reason"),
                    "premise": "verified: empty generation (EOS@step0)"})
            else:
                keep.append(d)
        even = [d for d in keep if d["doc_id"] % 2 == 0]
        odd = [d for d in keep if d["doc_id"] % 2 == 1]
        base = A1.r_baselines(even)
        for d in even + odd:
            A1.r_derive(d, base)
        loop_sorted = sorted(loop_by_leg[leg],
                             key=lambda r: str(r["doc_id"]))
        live = [d for d in loop_sorted
                if d["n_gen_steps"] >= A1.R_LOOP_INERT_MIN_STEPS]
        inert = [d for d in loop_sorted
                 if d["n_gen_steps"] < A1.R_LOOP_INERT_MIN_STEPS]
        for d in live:
            A1.r_derive(d, base)
        sC_e = [d["score"]["maxPRsig"] for d in even]
        sF_e = [d["score"]["minS"] for d in even]
        mu_C, sd_C = A1.r_mstd(sC_e)
        mu_F, sd_F = A1.r_mstd(sF_e)
        sides = R_ARMED[leg]
        for d in even + odd + live:
            d["z_C"] = (d["score"]["maxPRsig"] - mu_C) / sd_C
            d["z_F"] = (d["score"]["minS"] - mu_F) / sd_F
            d["c_gate_on"], _band = gate_state(d)
            vals = []
            if "C" in sides and d["c_gate_on"]:
                vals.append(d["z_C"])
            if "F" in sides:
                vals.append(d["z_F"])
            d["D"] = max(vals)
        calib_D_sorted = sorted(d["D"] for d in even)
        t_leg = A1.r_quantile(calib_D_sorted, 1.0 - A1.R_ALPHA)
        t_esc = A1.r_quantile(calib_D_sorted, 1.0 - A1.R_ALPHA_ESC)
        calib_fires = sum(1 for d in even if d["D"] >= t_leg)
        calib_ceil = math.ceil(A1.R_ALPHA * len(even))
        level_set_ok = calib_fires <= calib_ceil
        calib_esc = sum(1 for d in even if d["D"] >= t_esc)
        th_C = A1.r_quantile(sorted(d["z_C"] for d in even), A1.R_CO_ELEV_Q)
        th_F = A1.r_quantile(sorted(d["z_F"] for d in even), A1.R_CO_ELEV_Q)
        fires = [d for d in odd if d["D"] >= t_leg]
        n_fires = len(fires)
        rate = n_fires / len(odd) if odd else 0.0
        count_ceil = math.ceil(A1.R_ALPHA * len(odd)) if odd else 0
        wil = A1.r_wilson(n_fires, len(odd)) if odd else None
        esc_fires = [d for d in odd if d["D"] >= t_esc]
        fired_sorted = sorted(fires, key=lambda d: -d["D"])
        fired_views = [r_doc_view_v2(d, leg) for d in fired_sorted]
        for d, v in zip(fired_sorted, fired_views):
            co = True
            if "C" in sides:
                co = co and (d["z_C"] >= th_C)
            if "F" in sides:
                co = co and (d["z_F"] >= th_F)
            v["co_elevated"] = co
            v["escalation"] = d["D"] >= t_esc
        live_Ds = [d["D"] for d in live]
        easiest_loop_D = min(live_Ds) if live_Ds else None
        n_overlap = (sum(1 for d in odd if easiest_loop_D is not None
                         and d["D"] >= easiest_loop_D)
                     if easiest_loop_D is not None else None)
        gap = (A1.r_sgap(live_Ds, [d["D"] for d in odd])
               if live and odd else None)
        auc = (A1.r_auc(live_Ds, [d["D"] for d in odd])
               if live and odd else None)
        catches_t_leg = sum(1 for d in live if d["D"] >= t_leg)
        catches_t_esc = sum(1 for d in live if d["D"] >= t_esc)
        if len(even) < A1.R_POP_GUARD_MIN or len(odd) < A1.R_POP_GUARD_MIN:
            typing, why = ("INCONCLUSIVE-POPULATION-GUARD",
                           f"per-half population guard (the sheet "
                           f"SS1.4): n_calib_half={len(even)} "
                           f"n_held_out_half={len(odd)} "
                           f"(< {A1.R_POP_GUARD_MIN}/half)")
        else:
            typing, why = A1.r_verdict_typing(gap, len(live), len(odd))
        over = (n_fires > count_ceil) if odd else False
        if over:
            typing = "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
            why = (f"the coarse-guard falsifier fired: the held-out "
                   f"half's clean fire count {n_fires}/{len(odd)} > "
                   f"ceil({A1.R_ALPHA:.2f} * {len(odd)}) = "
                   f"{count_ceil} (rate {rate:.4%}) -- the candidate "
                   f"dies EVEN IF the sigma-gap passes (the pinned "
                   f"sheet SS1.5, the R16-D2 falsifier)")
        if typing == "PASS_2SIGMA" and gap is not None \
                and gap < 2.0 + A1.R_JITTER_BAND:
            near_bar_legs.append(leg)
        if typing == "FAIL":
            failed_legs.append(leg)
        if typing == "INCONCLUSIVE-FROM-JITTER":
            jitter_legs.append(leg)
        if typing == "INCONCLUSIVE-POPULATION-GUARD":
            any_guard = True
        if typing != "PASS_2SIGMA":
            all_pass = False
        if over:
            any_over_budget = True
        loop_views = [r_doc_view_v2(d, leg) for d in live]
        held_out_views = [r_doc_view_v2(d, leg) for d in odd]
        calib_views = [r_doc_view_v2(d, leg) for d in even]
        forensics = A1.r_forensics(leg, loop_views, held_out_views,
                                    typing, gap, fires, t_leg)
        summaries = {
            "loops_live": A1.r_summarize(loop_views),
            "held_out_clean_fired": A1.r_summarize(fired_views),
            "held_out_clean_nonfired": A1.r_summarize(
                [v for v, d in zip(held_out_views, odd)
                 if d["D"] < t_leg]),
            "calibration_half_clean": A1.r_summarize(calib_views),
        }
        exp_legs[leg] = {
            "armed_sides": list(sides),
            "census": {"corpus_docs": len(corpus),
                       "measured_eos_step0": len(removed),
                       "expected_of_record":
                           dict(A1.EXPECTED_FRESH_CENSUS)[leg],
                       "receipts": census_out},
            "parity": {"n_even_calibration": len(even),
                       "n_odd_held_out": len(odd)},
            "gate_census": {
                "k_gate": K_GATE,
                "side_c_armed": "C" in sides,
                "law": FIXED_GATE_CENSUS_LAW,
                "calibration_gated": sum(1 for d in even
                                         if not d["c_gate_on"]),
                "held_out_gated": sum(1 for d in odd
                                      if not d["c_gate_on"]),
                "loop_live_gated": sum(1 for d in live
                                       if not d["c_gate_on"]),
                "fired_gated": sum(1 for d in fires
                                   if not d["c_gate_on"]),
            },
            "loop_population": {"n_live": len(live),
                                "n_inert": len(inert),
                                "inert": [d["doc_id"] for d in inert]},
            "z_baselines": {"mu_C": mu_C, "sd_C": sd_C,
                            "mu_F": mu_F, "sd_F": sd_F},
            "thresholds": {"t_leg": t_leg, "t_esc": t_esc,
                           "th_C_coelev": th_C, "th_F_coelev": th_F},
            "level_set_receipt": {
                "n_calib": len(even), "alpha": A1.R_ALPHA,
                "calib_fires": calib_fires, "ceiling": calib_ceil,
                "ok": level_set_ok, "note": A1.LEVEL_SET_NOTE},
            "calibration_escalation_fires": calib_esc,
            "held_out": {
                "n": len(odd), "fires": n_fires, "rate": rate,
                "count_ceil": count_ceil, "wilson_upper_95": wil,
                "escalation_fires": len(esc_fires),
                "fired_docs": fired_views},
            "loop_floor_overlap_line": {
                "easiest_loop_D": easiest_loop_D,
                "n_clean_at_or_above": n_overlap,
                "rate": (n_overlap / len(odd)
                         if n_overlap is not None and odd else None),
                "note": A1.OVERLAP_NOTE},
            "loop_catches": {"n_live": len(live),
                             "at_t_leg": catches_t_leg,
                             "at_t_esc": catches_t_esc},
            "separation_context": {"sigma_gap_on_D": gap,
                                   "auc_on_D": auc,
                                   "note": A1.SEP_NOTE},
            "verdict": {"typing_presented": typing, "basis": why,
                        "sigma_gap": round(gap, 3) if gap is not None
                        else None,
                        "auc": round(auc, 4) if auc is not None
                        else None,
                        "over_budget": over},
            "populations": {"loops_live": loop_views,
                            "summaries_at_0.90": summaries},
            "forensics": forensics,
        }

    if any_over_budget:
        cand = ("CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
                "at least one leg's held-out-half clean fire count "
                "exceeded the coarse-guard budget ceiling (the "
                "pinned sheet SS1.5 falsifier) -- the candidate dies "
                "even if gaps passed; KILLED dominates a guard "
                "typing (SS1.8)")
    elif any_guard:
        cand = ("INCONCLUSIVE-POPULATION-GUARD",
                "at least one leg failed a population guard (the "
                "sheet SS1.4 per-half / per-side guards)")
    elif all_pass:
        cand = ("PASS_2SIGMA-ALL-FOUR-LEGS",
                "the armed D cleared the held-out 2-sigma bar on all "
                "four legs' held-out halves within the coarse-guard "
                "budget (PASS_2SIGMA-ALL-FOUR-LEGS iff every leg's "
                "bar AND budget pass, the sheet SS1.8; presented, "
                "never adjudicated; theta wiring is its own pre-reg)")
    elif jitter_legs:
        cand = ("INCONCLUSIVE-FROM-JITTER",
                f"legs inside the +/-{A1.R_JITTER_BAND}-sigma jitter "
                f"band: {jitter_legs}")
    else:
        cand = ("FAIL",
                f"the held-out 2-sigma bar was not met on "
                f"{failed_legs} (the honest max-of-two headwind of "
                f"the pinned sheet applies; the sides stand "
                f"separately in the item-215 record)")

    exp = {
        "legs": exp_legs,
        "inputs": {"walks": inputs},
        "empty_form_records_excluded": excluded_empty,
        "fixture_identity_receipt": {
            "n_loop_fixtures": len(fixture_copies),
            "copies_byte_identical": True},
        "presented_candidate_verdict": {
            "verdict_presented": cand[0], "basis": cand[1],
            "near_bar_legs": near_bar_legs,
            "failed_legs": failed_legs, "jitter_legs": jitter_legs,
            "population_guard_legs": [l for l in LEGS
                                      if exp_legs[l]["verdict"]
                                      ["typing_presented"]
                                      == "INCONCLUSIVE-POPULATION-"
                                         "GUARD"],
            "over_budget_legs": [l for l in LEGS
                                 if exp_legs[l]["verdict"]
                                 ["over_budget"]]},
        "tag": tag,
        "fixture_mode": True,
        "tool": "triadic_rw17_readout_v2.py",
        "tool_sha256": A1.r_sha256_file(V2TOOL),
        "mode": V2_MODE_TYPE,
    }
    return exp


def full_exp_v2(caches, tag):
    exp = recompute_v2(caches, tag)
    for k in A1.FIXED_TOP:
        exp[k] = A1.FIXED_TOP[k]
    exp["construction"] = dict(A1.FIXED_TOP["construction"])
    exp["construction"]["refinement_v2"] = FIXED_REFINEMENT_V2
    exp["fixture_identity_receipt"]["rule"] = A1.FIXED_FIR_RULE
    pcv = exp["presented_candidate_verdict"]
    pcv["caveats"] = V2_CAVEATS
    pcv["note"] = A1.FIXED_PCV_NOTE
    exp["prereg"] = V2_PREREG
    return exp


# =========================================================================
# The drivers.
# =========================================================================
def run_v2(caches, out, tag, fixture_mode=True):
    cmd = [sys.executable, V2TOOL]
    if fixture_mode:
        cmd.append("--fixture-mode")
    for c in caches:
        cmd += ["--cache", c]
    cmd += ["--tag", tag, "--out", out]
    return subprocess.run(cmd, capture_output=True, text=True)


def run_v1(caches, out, tag, fixture_mode=True):
    cmd = [sys.executable, V1TOOL]
    if fixture_mode:
        cmd.append("--fixture-mode")
    for c in caches:
        cmd += ["--cache", c]
    cmd += ["--tag", tag, "--out", out]
    return subprocess.run(cmd, capture_output=True, text=True)


def check(fam, name, ok, detail=""):
    return A1.check(fam, name, ok, detail)


def fam_head(fam, title):
    A1.fam_head(fam, title)


def run_and_cmp_v2(fam, wd, spec, tag, wname):
    caches = A1.build_world(wd, spec)
    out = os.path.join(wd, "export_v2.json")
    p = run_v2(caches, out, tag)
    if not check(fam, f"{wname}: the v2 tool runs clean (rc 0)",
                 p.returncode == 0,
                 p.stderr[-300:] if p.returncode != 0 else ""):
        return None
    with open(out) as f:
        got = json.load(f)
    exp = full_exp_v2(caches, tag)
    errs = []
    A1.cmp_tree(exp, got, "", errs)
    check(fam, f"{wname}: export == the independent v2 recompute "
          f"EXACT (every field, every leg, every doc)",
          not errs, f"{len(errs)} diff(s): " + "; ".join(errs[:5]))
    return got


# =========================================================================
# F1: the clean V-PASS world (the gate ACTIVE, as measured).
# =========================================================================
def fam_f1(tmp):
    fam_head("F1", "the clean four-leg V-PASS world through the v2 "
                   "CLI: every quantity EXACT vs the independent v2 "
                   "recompute")
    return run_and_cmp_v2("F1", os.path.join(tmp, "f1_vpass"),
                          A1.base_spec(), "accept-v2-f1-vpass",
                          "the V-PASS world")


# =========================================================================
# F2: THE GATE LAW per exported doc view.
# =========================================================================
def fam_f2(got):
    fam_head("F2", "the gate law: gated-off Side C => D == z_F on "
                   "C+F legs; gate on => D == max(z_C, z_F); the "
                   "F-only code leg => D == z_F with the N/A string; "
                   "the NAMED-GATED census strings exact")
    ok_all = True
    for leg in LEGS:
        lb = got["legs"][leg]
        armed = set(lb["armed_sides"])
        views = list(lb["held_out"]["fired_docs"]) \
            + list(lb["populations"]["loops_live"])
        bad, gated_ct, pass_ct = [], 0, 0
        for v in views:
            d_ok = True
            if "C" not in armed:
                d_ok = (v["D"] == v["z_F"]
                        and v["side_c_gate"]
                        == "N/A (Side C unarmed on this leg)")
            else:
                if v.get("c_gate_on"):
                    pass_ct += 1
                    expect = max(v["z_C"], v["z_F"])
                    if not v["side_c_gate"].startswith("PASS "):
                        d_ok = False
                else:
                    gated_ct += 1
                    expect = v["z_F"]
                    if not v["side_c_gate"].startswith(
                            "NAMED-GATED-OFF"):
                        d_ok = False
                if v["D"] != expect:
                    d_ok = False
            if not d_ok:
                bad.append(v["doc_id"])
        ok_all = check("F2", f"leg {leg}: every exported doc view "
                       f"({len(views)} views: fired + live loops) "
                       f"obeys the gate law exactly "
                       f"[{gated_ct} gated / {pass_ct} pass]",
                       not bad, f"violating docs: {bad[:8]}")
    # the code leg's identity: every view N/A
    lb = got["legs"]["mbpprw17"]
    na = all(v["side_c_gate"] == "N/A (Side C unarmed on this leg)"
             for v in lb["held_out"]["fired_docs"]
             + lb["populations"]["loops_live"])
    ok_all = check("F2", "the F-only code leg: every view carries "
                   "the N/A census string (the gate never applies)",
                   na) and ok_all
    # the fired_gated census == the fired views' gated count
    for leg in LEGS:
        lb = got["legs"][leg]
        fg = sum(1 for v in lb["held_out"]["fired_docs"]
                 if not v.get("c_gate_on"))
        ok_all = check("F2", f"leg {leg}: gate_census.fired_gated "
                       f"== the fired views' NAMED-GATED-OFF count "
                       f"({fg})",
                       lb["gate_census"]["fired_gated"] == fg) \
            and ok_all
    return ok_all


# =========================================================================
# F3: PORT FIDELITY -- the all-flat-PR world (no doc gated).
# =========================================================================
def build_flat_world(dirpath):
    """The NO-GATE world: every doc carries a TWO-LEVEL PR series --
    half the steps at a doc-specific HIGH value p0, half at a
    doc-specific LOW value p1 (PR_sig = (bP_mean - PR)/bP_sd spikes
    when PR drops BELOW baseline, so the p1 half IS the max set):
    N_band >= n_steps//2 >= 4 for every doc (the gate PASSES
    everywhere by construction), maxPRsig varies ACROSS docs (the
    p1 values vary -- the z_C scale stays non-degenerate), and the
    loop fixtures carry the same two-level shape (every LIVE
    fixture >= 37 steps -> >= 19 in band)."""
    def two_level_prs(doc_id, n_steps):
        p0 = 0.30 + 0.01 * doc_id
        p1 = 0.02 + 0.005 * doc_id
        return ([p0] * (n_steps // 2)
                + [p1] * (n_steps - n_steps // 2))

    os.makedirs(dirpath, exist_ok=True)
    caches = []
    for leg in LEGS:
        sp = A1.base_spec()[leg]
        path = os.path.join(dirpath, f"cache_{leg}.jsonl")
        with open(path, "w") as f:
            censused = set(sp.get("census_ids", []))
            for did in range(sp["n_corpus"]):
                if did in censused:
                    r = A1.census_doc(leg, did)
                else:
                    ss = [sp["s_lo"] + A1.S_BAND_W
                          * A1.pv(did, i, sp["salt"] + 1)
                          for i in range(40)]
                    r = A1.rec(leg, did, 40,
                               two_level_prs(did, 40), ss)
                f.write(json.dumps(r, sort_keys=True) + "\n")
            if sp.get("empty_form"):
                f.write(json.dumps(
                    {"empty": True, "key": f"{leg}:empty-form-1"},
                    sort_keys=True) + "\n")
            for fid, n in A1.FIXTURE_STEPS.items():
                prs = ([0.35] * (n // 2) + [0.05] * (n - n // 2))
                rr = A1.rec("loop", fid, n, prs,
                            [A1.LIVE_S_CONST] * n)
                f.write(json.dumps(rr, sort_keys=True) + "\n")
        caches.append(path)
    return caches


IGNORED_V2_PATHS = {
    "tool", "tool_sha256", "mode", "prereg",
    "construction.refinement_v2",
    "presented_candidate_verdict.caveats",
}


def inherited_equal(exp, got, path, errs, skip_paths):
    if path.lstrip(".") in skip_paths:
        return
    if isinstance(exp, dict):
        if not isinstance(got, dict):
            errs.append(f"{path}: type mismatch")
            return
        for k in exp:
            inherited_equal(exp[k], got.get(k), f"{path}.{k}",
                            errs, skip_paths)
        extra = [k for k in got if k not in exp]
        # the v2-only additive keys are named; any OTHER extra key
        # is a real divergence
        allowed = {"c_gate_on", "side_c_gate", "gate_census",
                   "refinement_v2"}
        for k in extra:
            if k in allowed:
                continue
            errs.append(f"{path}.{k}: unexpected key")
        return
    if isinstance(exp, list):
        if not isinstance(got, list) or len(exp) != len(got):
            errs.append(f"{path}: list mismatch")
            return
        for i, (e, g) in enumerate(zip(exp, got)):
            inherited_equal(e, g, f"{path}[{i}]", errs, skip_paths)
        return
    if exp != got:
        errs.append(f"{path}: {exp!r} != {got!r}")


def fam_f3(tmp):
    fam_head("F3", "PORT FIDELITY: the all-flat-PR world -- NO doc "
                   "gated; the v1 CLI and the v2 CLI on the SAME "
                   "world; every inherited quantity EXACT-equal")
    wd = os.path.join(tmp, "f3_flat")
    caches = build_flat_world(wd)
    out_v1 = os.path.join(wd, "export_v1.json")
    out_v2 = os.path.join(wd, "export_v2.json")
    p1 = run_v1(caches, out_v1, "accept-v2-f3-flat")
    p2 = run_v2(caches, out_v2, "accept-v2-f3-flat")
    check("F3", "both CLIs run clean on the flat world",
          p1.returncode == 0 and p2.returncode == 0,
          (p1.stderr[-200:] + p2.stderr[-200:]))
    with open(out_v1) as f:
        v1 = json.load(f)
    with open(out_v2) as f:
        v2 = json.load(f)

    # (a) no doc gated anywhere (the world's own construction)
    n_gated = 0
    for leg in LEGS:
        lb = v2["legs"][leg]
        views = list(lb["held_out"]["fired_docs"]) \
            + list(lb["populations"]["loops_live"])
        for v in views:
            if "C" in lb["armed_sides"] and not v.get("c_gate_on"):
                n_gated += 1
        gc = lb["gate_census"]
        n_gated += gc["calibration_gated"] + gc["held_out_gated"] \
            + gc["loop_live_gated"]
    check("F3", "the flat world gates NOTHING (every census count "
          "0; every C-armed view PASS; the code leg N/A)",
          n_gated == 0, f"{n_gated} gated doc(s)")

    # (b) every inherited quantity v1 == v2
    errs = []
    inherited_equal(v1, v2, "", errs, IGNORED_V2_PATHS)
    check("F3", "every inherited quantity EXACT-equal v1 vs v2 "
          "(every leg, threshold, fire, gap, AUC, verdict, view "
          "field -- the additive keys excepted by name)",
          not errs, f"{len(errs)} diff(s): " + "; ".join(errs[:5]))

    # (c) the v2-only additive fields carry their expected values
    ok = v2["mode"] == V2_MODE_TYPE \
        and v2["tool"] == "triadic_rw17_readout_v2.py" \
        and v2["construction"]["refinement_v2"] == FIXED_REFINEMENT_V2 \
        and v2["presented_candidate_verdict"]["caveats"] == V2_CAVEATS \
        and v2["prereg"] == V2_PREREG
    check("F3", "the v2-only fields carry their expected values "
          "(the V2 mode line, the tool name, the refinement_v2 "
          "block, the FOUR caveat lines, the prereg string)", ok)
    ok = all("refinement_disclosure" in v2["presented_candidate_verdict"]
             ["caveats"]
             and v2["legs"][l]["gate_census"]["k_gate"] == 4
             for l in LEGS)
    check("F3", "every leg's gate_census carries K=4 and the "
          "caveats carry the refinement disclosure (the 4th line)",
          ok)
    # (d) the v2 CLI's own recompute agrees on the flat world too
    errs = []
    A1.cmp_tree(full_exp_v2(caches, "accept-v2-f3-flat"), v2, "",
                errs)
    check("F3", "the v2 export == the independent v2 recompute EXACT "
          "on the flat world as well", not errs,
          f"{len(errs)} diff(s): " + "; ".join(errs[:5]))
    return v1, v2


# =========================================================================
# F4: THE GATE-EFFECT WORLD (single-PR-spike docs, held-out AND
# calibration -- the operating point itself moves).
# =========================================================================
SPIKE_DOC = 3          # odd => held-out, on the gsm leg
SPIKE_EVEN = (6, 14, 26)   # even => calibration, slightly milder
SPIKE_STEPS = 40


def fam_f4(tmp):
    fam_head("F4", "the gate-effect world: v1 fires a held-out "
                   "single-spike doc through Side C; the v2 gate "
                   "EXCLUDES it (N_band=1), the spiked calibration "
                   "docs gate off too -- t_leg re-derived on the "
                   "gated D (the operating point MOVES); the "
                   "level-set receipt holds")
    wd = os.path.join(tmp, "f4_spike")
    caches = A1.build_world(wd, A1.base_spec())

    # pin the held-out spike doc's s mid-band first: its minS = the
    # calibration half's median minS -> z_F ~ 0 (it cannot fire
    # through Side F; fixture-side computation, never a tool guess)
    recs, _empty = A1.r_load_cache(caches[0])
    even_mins = sorted(min(r["steps"]["s"]) for r in recs
                       if r.get("leg") == "gsmrw17"
                       and isinstance(r.get("doc_id"), int)
                       and r["doc_id"] % 2 == 0
                       and r["n_gen_steps"] > 0)
    s_mid = even_mins[len(even_mins) // 2]

    def spike(recs):
        out = []
        for r in recs:
            did = r.get("doc_id")
            if r.get("leg") != "gsmrw17" \
                    or not isinstance(did, int) or r["n_gen_steps"] == 0:
                out.append(r)
                continue
            if did == SPIKE_DOC:
                # a SINGLE high-PRsig ceiling spike: one LOW-PR step
                # (PR_sig = (bP_mean - PR)/bP_sd spikes when PR drops
                # below baseline -- the item-257 boundary-spike
                # anchor shape), the rest at 0.80; s pinned mid-band
                prs = [0.80] * SPIKE_STEPS
                prs[20] = 0.05
                r = dict(r)
                r["steps"] = dict(r["steps"])
                r["steps"]["PR"] = prs
                r["steps"]["s"] = [s_mid] * SPIKE_STEPS
            elif did in SPIKE_EVEN:
                # the SAME anchor shape on three CALIBRATION docs,
                # slightly milder (spike PR 0.10 > 0.05 -> their z_C
                # sits just BELOW the held-out spike's): v1's t_leg
                # rides up to their level, v1 still fires the
                # held-out spike; v2 gates all four off
                prs = [0.80] * SPIKE_STEPS
                prs[20] = 0.10
                r = dict(r)
                r["steps"] = dict(r["steps"])
                r["steps"]["PR"] = prs
            out.append(r)
        return out
    A1.edit_cache(caches[0], spike)

    out_v1 = os.path.join(wd, "export_v1.json")
    out_v2 = os.path.join(wd, "export_v2.json")
    p1 = run_v1(caches, out_v1, "accept-v2-f4-spike")
    p2 = run_v2(caches, out_v2, "accept-v2-f4-spike")
    check("F4", "both CLIs run clean on the spike world",
          p1.returncode == 0 and p2.returncode == 0,
          (p1.stderr[-200:] + p2.stderr[-200:]))
    with open(out_v1) as f:
        v1 = json.load(f)
    with open(out_v2) as f:
        v2 = json.load(f)

    v1_ids = [v["doc_id"] for v in
              v1["legs"]["gsmrw17"]["held_out"]["fired_docs"]]
    v2_ids = [v["doc_id"] for v in
              v2["legs"]["gsmrw17"]["held_out"]["fired_docs"]]
    check("F4", f"v1 FIRES the spike doc {SPIKE_DOC} (Side C's "
          f"ceiling spike -- the item-257 boundary anchor shape; "
          f"t_leg rides the milder spiked calibration docs)",
          SPIKE_DOC in v1_ids, f"v1 fired docs: {v1_ids}")
    check("F4", f"v2 EXCLUDES the spike doc {SPIKE_DOC} "
          f"(NAMED-GATED-OFF at N_band=1 < K=4; D falls to z_F)",
          SPIKE_DOC not in v2_ids, f"v2 fired docs: {v2_ids}")

    # the spike doc's N_band == 1: recomputed independently from the
    # raw cache bytes (this runner's own engine)
    recs, _empty = A1.r_load_cache(caches[0])
    sp = [r for r in recs if r.get("leg") == "gsmrw17"
          and r.get("doc_id") == SPIKE_DOC][0]
    even = [r for r in recs
            if r.get("leg") == "gsmrw17"
            and isinstance(r.get("doc_id"), int)
            and r["doc_id"] % 2 == 0 and r["n_gen_steps"] > 0]
    base = A1.r_baselines(even)
    A1.r_derive(sp, base)
    on, band = gate_state(sp)
    check("F4", f"the spike doc's OWN SEC-1 band recomputed from "
          f"the raw bytes: N_band == 1 (single in-band step), "
          f"c_gate_on False -- the boundary-spike anchor shape "
          f"gated off", band and band["N_band"] == 1 and not on,
          f"N_band={band['N_band'] if band else None}")
    sp_even = [r for r in even if r["doc_id"] in SPIKE_EVEN]
    for r in sp_even:
        A1.r_derive(r, base)
    ok_e = all(gate_state(r)[0] is False and gate_state(r)[1]
               and gate_state(r)[1]["N_band"] == 1 for r in sp_even)
    check("F4", "the three spiked CALIBRATION docs also gate off "
          "(N_band=1 each) -- the calibration half's gated-D "
          "distribution is what moves the operating point",
          ok_e)

    # t_leg re-derived on the gated D: independently recomputed; and
    # it DIFFERS from v1's (the spiked calibration docs gated off ->
    # the operating point moved -- named honestly)
    t1 = v1["legs"]["gsmrw17"]["thresholds"]["t_leg"]
    t2 = v2["legs"]["gsmrw17"]["thresholds"]["t_leg"]
    exp2 = full_exp_v2(caches, "accept-v2-f4-spike")
    t2_exp = exp2["legs"]["gsmrw17"]["thresholds"]["t_leg"]
    check("F4", f"t_leg re-derived on the GATED D (v2 {t2:.4f} == "
          f"the independent recompute {t2_exp:.4f} EXACT; v1's "
          f"ungated {t1:.4f} differs -- the operating point moved, "
          f"named honestly)",
          abs(t2 - t2_exp) < 1e-12 and t1 != t2,
          f"t1={t1}, t2={t2}, exp={t2_exp}")

    # the level-set receipt holds on the gated D
    lsr = v2["legs"]["gsmrw17"]["level_set_receipt"]
    check("F4", "the level-set receipt holds on the GATED D "
          f"(calibration fires {lsr['calib_fires']}/{lsr['n_calib']} "
          f"<= ceiling {lsr['ceiling']}; ok {lsr['ok']})",
          lsr["ok"] and lsr["calib_fires"] <= lsr["ceiling"])

    # the whole export == the independent v2 recompute on the spike
    # world too
    errs = []
    A1.cmp_tree(exp2, v2, "", errs)
    check("F4", "the v2 export == the independent v2 recompute EXACT "
          "on the spike world (every field)", not errs,
          f"{len(errs)} diff(s): " + "; ".join(errs[:5]))

    # the gate census prints ride the console (NAMED-GATED never
    # silent): one line per leg -- three C-armed census lines + the
    # code leg's N/A line
    check("F4", "the per-leg persistence-gate console line rides "
          "every leg (3 C-armed census lines + the code leg's N/A "
          "line; NAMED-GATED never silent)",
          p2.stdout.count("persistence gate (K=4)") == 4
          and "N/A on this leg" in p2.stdout)
    return v1, v2


# =========================================================================
# F5: the inherited hard exits, through the v2 CLI.
# =========================================================================
def expect_die_v2(fam, name, caches, substr, real=False):
    out = os.path.join(os.path.dirname(caches[0]), "die_out.json")
    p = run_v2(caches, out, "accept-v2-f5", fixture_mode=not real)
    ok = (p.returncode != 0 and "HARD EXIT" in p.stderr
          and substr in p.stderr)
    check(fam, name, ok,
          f"rc={p.returncode}; stderr tail: ...{p.stderr[-220:]}"
          if not ok else "")


def fam_f5(tmp):
    fam_head("F5", "every inherited hard exit fires loud through "
                   "the v2 CLI (fail-loud, never a silent repair)")
    base = os.path.join(tmp, "f5_base")
    A1.build_world(base, A1.base_spec())

    def case(name, mutate, substr, real=False):
        wd = os.path.join(tmp, "f5_" + name.replace(" ", "_")[:40])
        A1.clone_world(base, wd)
        caches = [os.path.join(wd, f"cache_{l}.jsonl") for l in LEGS]
        mutate(wd, caches)
        expect_die_v2("F5", f"{name} -> HARD EXIT naming {substr!r}",
                      caches, substr, real=real)

    def trunc(wd, caches):
        with open(caches[0]) as f:
            lines = f.read().splitlines()
        last = lines[-1]
        with open(caches[0], "w") as f:
            f.write("\n".join(lines[:-1]) + "\n" + last[:len(last) // 2])

    def dup(wd, caches):
        with open(caches[0]) as f:
            lines = f.read().splitlines()
        with open(caches[0], "w") as f:
            f.write("\n".join(lines + [lines[5]]) + "\n")

    def degen(wd, caches):
        def flat_s(recs):
            out = []
            for r in recs:
                if r.get("leg") == "gsmrw17" \
                        and isinstance(r.get("doc_id"), int) \
                        and r["doc_id"] % 2 == 0:
                    r = dict(r)
                    r["steps"] = dict(r["steps"])
                    r["steps"]["s"] = [0.5] * r["n_gen_steps"]
                out.append(r)
            return out
        A1.edit_cache(caches[0], flat_s)

    case("truncated cache line", trunc, "truncated")
    case("duplicate record", dup, "duplicate")
    case("degenerate calibration", degen, "DEGENERATE")

    # missing leg (drop the gsm cache) / unexpected leg
    wd = os.path.join(tmp, "f5_missing_leg")
    A1.clone_world(base, wd)
    caches = [os.path.join(wd, f"cache_{l}.jsonl")
              for l in LEGS if l != "gsmrw17"]
    expect_die_v2("F5", "missing leg -> HARD EXIT (the four-leg law)",
                  caches, "missing leg")

    wd = os.path.join(tmp, "f5_extra_leg")
    A1.clone_world(base, wd)
    caches = [os.path.join(wd, f"cache_{l}.jsonl") for l in LEGS]
    with open(caches[0]) as f:
        lines = f.read().splitlines()
    r = json.loads(lines[0])
    r = dict(r)
    r["leg"] = "bogus-leg-rw17"
    r["key"] = "bogus-leg-rw17:0"
    with open(caches[0], "w") as f:
        f.write("\n".join([lines[0], json.dumps(r, sort_keys=True)]
                          + lines[1:]) + "\n")
    expect_die_v2("F5", "an unrecognized leg -> HARD EXIT at load "
                  "(the loader's never-guess-a-key law)",
                  caches, "unrecognized leg")

    # the real-mode pin refusal: the fixture caches are NOT the
    # pinned caches of record
    caches = [os.path.join(base, f"cache_{l}.jsonl") for l in LEGS]
    expect_die_v2("F5", "real mode on a non-pinned cache -> HARD "
                  "EXIT (the SS4 pin law ENFORCED in real mode)",
                  caches, "checksum", real=True)


# =========================================================================
# F6: determinism.
# =========================================================================
def fam_f6(tmp):
    fam_head("F6", "determinism: the same-path re-run byte-identical "
                   "on BOTH the export and the console")
    wd = os.path.join(tmp, "f6_det")
    caches = A1.build_world(wd, A1.base_spec())
    out = os.path.join(wd, "export_v2.json")
    p1 = run_v2(caches, out, "accept-v2-f6")
    with open(out, "rb") as f:
        b1 = f.read()
    c1 = p1.stdout
    p2 = run_v2(caches, out, "accept-v2-f6")
    with open(out, "rb") as f:
        b2 = f.read()
    check("F6", "the re-run export AND console are byte-identical",
          p1.returncode == 0 and p2.returncode == 0
          and b1 == b2 and len(b1) > 0 and c1 == p2.stdout)


# =========================================================================
# F7: the constants echo (the pinned values, through the module).
# =========================================================================
def fam_f7():
    fam_head("F7", "the constants echo: K_GATE=4, the refinement "
                   "sheet's pinned SHA, the RW-17 sheet's pinned SHA "
                   "unchanged, the arming table unchanged, the "
                   "fresh1 echo constants with the honest note, the "
                   "FOUR caveat lines")
    mod = A1.load_module("rw17_readout_v2_module", V2TOOL)
    check("F7", "K_GATE == 4 (the stamped Option A pin)",
          mod.K_GATE == 4)
    check("F7", "REFINEMENT_SHA == the stamped refinement sheet's "
          "pinned SHA (the item-260 pin, byte-exact)",
          mod.REFINEMENT_SHA == REFINEMENT_SHA)
    check("F7", "PREREG_SHA unchanged (the pinned RW-17 sheet, "
          "the item-241 pin)",
          mod.PREREG_SHA == A1.PREREG_SHA)
    check("F7", "the arming table unchanged (math CF / code F / "
          "prose CF / p2 CF)",
          mod.ARMED_SIDES == A1.R_ARMED)
    check("F7", "the fresh1 echo constants carried (the SS4 cache "
          "pins + the item-254 expected censuses, ENFORCED real-mode "
          "values riding until the fresh3 echo-constant update -- "
          "the honest lifecycle note)",
          mod.PINNED_CACHE_SHA == A1.PINNED_CACHE_SHA
          and mod.EXPECTED_FRESH_CENSUS == A1.EXPECTED_FRESH_CENSUS)
    check("F7", "the mode line names the V2 amendment with the "
          "stamped option",
          mod.MODE_TYPE == V2_MODE_TYPE)
    check("F7", "the four caveat lines ride (the three pinned lines "
          "+ the refinement disclosure)",
          set(mod.CAVEAT_LINES) == set(V2_CAVEATS)
          and mod.CAVEAT_LINES["refinement_disclosure"]
          == V2_CAVEATS["refinement_disclosure"])
    check("F7", "SEC_BAND_FACTOR 0.90 / ALPHA 0.05 / ALPHA_ESC 0.01 "
          "unchanged (the pinned constants never amended)",
          mod.SEC_BAND_FACTOR == 0.90 and mod.ALPHA == 0.05
          and mod.ALPHA_ESC == 0.01)


# =========================================================================
# F8: the verdict-knob worlds through the v2 CLI (typings AS
# MEASURED under the gate).
# =========================================================================
def fam_f8(tmp):
    fam_head("F8", "the verdict-knob worlds (V-NEAR / V-JITTER / "
                   "V-FAIL) through the v2 CLI: every quantity EXACT "
                   "vs the independent v2 recompute; the typings AS "
                   "MEASURED under the gate, named honestly")
    for knob, label in ((A1.KNOB_V_NEAR, "V-NEAR"),
                        (A1.KNOB_V_JITTER, "V-JITTER"),
                        (A1.KNOB_V_FAIL, "V-FAIL")):
        wd = os.path.join(tmp, "f8_" + label.lower())
        caches = A1.build_world(wd, A1.base_spec(pr_lo_gsm=knob))
        out = os.path.join(wd, "export_v2.json")
        tag = f"accept-v2-f8-{label.lower()}"
        p = run_v2(caches, out, tag)
        if not check("F8", f"{label}: the v2 tool runs clean (rc 0)",
                     p.returncode == 0,
                     p.stderr[-300:] if p.returncode != 0 else ""):
            continue
        with open(out) as f:
            got = json.load(f)
        exp = full_exp_v2(caches, tag)
        errs = []
        A1.cmp_tree(exp, got, "", errs)
        check("F8", f"{label}: export == the independent v2 "
              f"recompute EXACT", not errs,
              f"{len(errs)} diff(s): " + "; ".join(errs[:5]))
        typings = {l: got["legs"][l]["verdict"]["typing_presented"]
                   for l in LEGS}
        cand_v = got["presented_candidate_verdict"]["verdict_presented"]
        print(f"    ({label} measured typings under the gate: "
              f"{typings}; the candidate-level verdict: {cand_v})")


# =========================================================================
# main.
# =========================================================================
def main():
    print("=" * 78)
    print("=== THE RW-17 READOUT AMENDMENT V2 ACCEPTANCE RUN (the "
          "item-255 pattern) ===")
    print("  tool under test: triadic_rw17_readout_v2.py")
    print("  (my stamped specificity refinement OPTION A -- "
          "the")
    print("   persistence-gated Side C, K=4; the stamped sheet")
    print(f"   rw17-specificity-refinement-preregistration.md, "
          f"SHA-256 {REFINEMENT_SHA})")
    print("  LAW: every family drives the REAL v2 TOOL via its CLI "
          "and")
    print("  compares EXACT against THIS RUNNER'S OWN gate-aware "
          "independent")
    print("  recompute (the banked v1 engine imported for the "
          "world-builder")
    print("  + arithmetic helpers, never the tool's functions; the "
          "v1 CLI is")
    print("  the port-fidelity oracle); fix-the-fixture-or-the-"
          "builder,")
    print("  never the tool's record.")
    scratch = os.path.join(HERE, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    tmp = os.path.join(scratch, "rw17_readout_v2_accept_run")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    print(f"  (run dir: {tmp})")
    f1 = fam_f1(tmp)
    if f1 is not None:
        fam_f2(f1)
    flat = fam_f3(tmp)
    fam_f4(tmp)
    fam_f5(tmp)
    fam_f6(tmp)
    fam_f7()
    fam_f8(tmp)
    print("\n" + "=" * 78)
    fams = []
    for fam, _name, _ok, _detail in A1.CHECKS:
        if fam not in fams:
            fams.append(fam)
    n_fail = sum(1 for c in A1.CHECKS if not c[2])
    for fam in fams:
        ft = sum(1 for c in A1.CHECKS if c[0] == fam)
        fp = sum(1 for c in A1.CHECKS if c[0] == fam and c[2])
        print(f"  {fam}: {fp}/{ft} PASS")
    print(f"\n  TOTAL: {len(A1.CHECKS) - n_fail}/{len(A1.CHECKS)} "
          f"PASS, {n_fail} FAIL")
    if n_fail:
        print("\n  FAILURES (named, never silent):")
        for fam, name, ok, detail in A1.CHECKS:
            if not ok:
                print(f"   [{fam}] {name}"
                      + (f" -- {detail}" if detail else ""))
    print("\n  Fix-the-fixture-or-the-builder, never the tool's "
          "record.")
    print("  theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, "
          "moved,")
    print("  or adjudicated; findings presented, never adjudicated "
          "--")
    print("  my stamps decide.")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

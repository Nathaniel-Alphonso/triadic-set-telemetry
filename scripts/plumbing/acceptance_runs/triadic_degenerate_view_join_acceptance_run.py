#!/usr/bin/env python3
# ============================================================
# THE DEGENERATE-OUTPUT VIEW extraction/join tool -- THE
# ACCEPTANCE BATTERY OF RECORD (the pinned sheet SS6 build
# lane; ledger item 389's battery). THE KNOWN-ANSWER PATTERN
# of record (the 255/319/326/334/339/345/349/354/362/368/375
# battery law): a CRAFTED mini world shaped exactly like the
# owner-side as-sized item-375 export, an INDEPENDENT
# world-builder that computes every aggregate from the
# primitives its own way, the tool run in --fixture-mode (the
# banked anchors ECHO, never enforce -- the structural
# two-code-path guards still enforce EXACT), hand-derived
# expected rows asserted field-for-field, marker round-trips,
# byte-identical determinism, and NAMED hard-exit negative
# fixtures -- every guard proven to die LOUD, never silently.
# Zero GPU; zero decodes; DEVELOPMENT DATA ONLY; RECEIPTS
# ONLY; no weighted sums; no new fit; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved
# (D-theta); findings presented, never adjudicated -- the
# owner's stamps decide.
# ============================================================
import copy
import importlib.util
import json
import os
import py_compile
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_degenerate_view_join.py")
FIXDIR = os.path.join(HERE, "rw17_degenerate_join_fixtures")
os.makedirs(FIXDIR, exist_ok=True)

# the tool's own marker constants, loaded from the tool's own
# bytes -- the marker round-trips assert against the TOOL'S
# OWN pins, never a re-typed literal (never guess a pin)
_spec = importlib.util.spec_from_file_location("degen_join_tool", TOOL)
TOOLMOD = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(TOOLMOD)
W = TOOLMOD.WITHHELD
W_BASE_CAL = TOOLMOD.WITHHELD_BASE_D_CAL
W_DPP = TOOLMOD.WITHHELD_DPP
W_STATE = TOOLMOD.WITHHELD_STATE_RETRAINED

THETA_GAMMA = 0.2806541621685028  # the 325-STAMP clause level, echoed
T_BASE = 1.7110                    # the crafted Base D t_leg
T_DPP = 2.132                      # the crafted D'' t_leg
SR1_SCALE = {"mu_c": 0.1168, "sd_c": 0.0619,
             "mu_f": 0.0962, "sd_f": 0.0560}
T_SR1 = 1.8525
AE_SCALE = {"mu_c": 0.5, "sd_c": 0.25,
            "mu_f": 0.5, "sd_f": 0.25}  # power-of-two sd: EXACT z round-trips
T_AE = 1.9507
MON_C = "monC"
MON_F = "monF"
MATH_LEG = "gsmrw17"  # the join leg of record (matches the tool)
HALVES = ("calibration", "held_out", "loop_live")

PASS = 0
FAIL = 0
FAILS = []


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS -- " + name)
    else:
        FAIL += 1
        FAILS.append(name)
        print("  FAIL -- " + name + (" -- " + str(detail) if detail else ""))


def longest_run(flags):
    best = cur = 0
    for f in flags:
        if f:
            cur += 1
            if cur > best:
                best = cur
        else:
            cur = 0
    return best


def armed_D(gate_on, z_c, z_f):
    """the armed two-side composite over C+F (the crafted world's
    own law, mirroring the record's armed construction: Side C
    contributes only through the gate; Side F always)."""
    vals = []
    if gate_on:
        vals.append(z_c)
    vals.append(z_f)
    return max(vals)


# ------------------------------------------------------------
# THE CRAFTED WORLD -- the primitives (every number hand-set;
# the state lists carry (t, in-gap gamma) pairs)
# ------------------------------------------------------------
DOCS = [
    # --- calibration (EVEN ids, the item-229 parity law) ---
    {"id": "0", "half": "calibration", "gate": True, "n_band": 6,
     "sr1": (2.0, 0.5), "ae": (2.5, -0.5), "z_c": 0.4, "mpr": 1.2,
     "w": (0.01, 0.02, 0.03, 0.04), "r_pr": 0.5, "pb": (1, 1),
     "states": [(t, True) for t in range(0, 6)]},
    {"id": "2", "half": "calibration", "gate": False, "n_band": 4,
     "sr1": (0.8, 1.9), "ae": (0.5, 2.5), "z_c": 0.2, "mpr": 0.8,
     "w": (0.05, 0.06, 0.07, 0.08), "r_pr": 0.3, "pb": (2, 2),
     "states": [(0, False), (1, True), (16, True), (17, False)]},
    {"id": "4", "half": "calibration", "gate": True, "n_band": 5,
     "sr1": (0.3, 0.1), "ae": (1.0, 0.5), "z_c": 0.1, "mpr": 0.5,
     "w": (0.09, 0.10, 0.11, 0.12), "r_pr": 0.2, "pb": (3, 3),
     "states": [(20, True), (21, False), (22, True)]},
    {"id": "6", "half": "calibration", "gate": False, "n_band": 2,
     "sr1": (0.0, 0.2), "ae": (0.0, 0.5), "z_c": 0.0, "mpr": 0.3,
     "w": (0.13, 0.14, 0.15, 0.16), "r_pr": 0.0, "pb": (4, 4),
     "states": [(40, False), (41, False)]},
    {"id": "8", "half": "calibration", "gate": True, "n_band": 5,
     "sr1": (1.7, 1.5), "ae": (2.0, 1.0), "z_c": 0.6, "mpr": 1.9,
     "w": (0.17, 0.18, 0.19, 0.20), "r_pr": 0.4, "pb": (1, 2),
     "states": [(0, True), (1, True), (2, True), (3, False),
                (4, True)]},
    {"id": "10", "half": "calibration", "gate": False, "n_band": 0,
     "sr1": (0.1, 0.2), "ae": (0.5, 0.5), "z_c": 0.3, "mpr": 0.4,
     "w": (0.0, 0.0, 0.0, 0.0), "r_pr": None, "pb": (None, None),
     "states": []},
    # --- held-out (ODD ids, the parity law) ---
    {"id": "1", "half": "held_out", "gate": False, "n_band": 6,
     "sr1": (0.4, 0.9), "ae": (1.0, 1.0), "z_c": 0.7, "mpr": 1.0,
     "w": (0.21, 0.22, 0.23, 0.24), "r_pr": 0.25, "pb": (2, 1),
     "states": [(0, True), (1, True), (2, False), (3, False),
                (4, True), (5, True)],
     "view": {"z_C": 2.6, "z_F": 2.0, "c_gate_on": False, "sec1_R_band": 2}},
    {"id": "3", "half": "held_out", "gate": True, "n_band": 8,
     "sr1": (2.1, 1.0), "ae": (2.5, 0.0), "z_c": 1.1, "mpr": 2.0,
     "w": (0.25, 0.26, 0.27, 0.28), "r_pr": 0.5, "pb": (1, 4),
     "states": [(0, True), (1, False), (2, True), (3, True),
                (4, False), (5, True), (6, True), (7, True)],
     "view": {"z_C": 2.8, "z_F": 0.5, "c_gate_on": True, "sec1_R_band": 1}},
    {"id": "5", "half": "held_out", "gate": True, "n_band": 4,
     "sr1": (1.9, 0.0), "ae": (0.5, 0.0), "z_c": 0.5, "mpr": 1.4,
     "w": (0.29, 0.30, 0.31, 0.32), "r_pr": 0.3, "pb": (3, 2), "nr_band": 4,
     "states": [(16, False), (17, True), (18, False), (19, True)]},
    {"id": "7", "half": "held_out", "gate": False, "n_band": 3,
     "sr1": (0.0, 2.0), "ae": (0.0, 2.5), "z_c": 0.2, "mpr": 0.9,
     "w": (0.33, 0.34, 0.35, 0.36), "r_pr": 0.6, "pb": (4, 3), "nr_band": 3,
     "states": [(32, True), (33, True), (34, True), (35, True),
                (36, False)]},
    {"id": "9", "half": "held_out", "gate": False, "n_band": 0,
     "sr1": (0.5, 0.5), "ae": (0.0, 0.5), "z_c": 0.1, "mpr": 0.2,
     "w": (0.0, 0.0, 0.0, 0.0), "r_pr": None, "pb": (None, None), "nr_band": 0,
     "states": []},
    {"id": "11", "half": "held_out", "gate": True, "n_band": 5,
     "sr1": (1.0, 1.2), "ae": (1.0, 0.0), "z_c": 0.9, "mpr": 1.1,
     "w": (0.37, 0.38, 0.39, 0.40), "r_pr": 0.1, "pb": (1, 3), "nr_band": 2,
     "states": [(48, False), (49, False), (50, True), (51, True),
                (52, False)]},
    # --- the loop population (10 FIXED fixtures of record) ---
    {"id": "901", "half": "loop_live", "gate": True, "n_band": 9,
     "sr1": (3.0, 2.0), "ae": (2.0, 0.5), "z_c": 0.9, "mpr": 2.5,
     "w": (0.41, 0.42, 0.43, 0.44), "r_pr": 0.9, "pb": (1, 1),
     "states": [(t, True) for t in range(0, 9)],
     "view": {"z_C": 2.9, "z_F": 1.0, "c_gate_on": True, "sec1_R_band": 1}},
    {"id": "903", "half": "loop_live", "gate": True, "n_band": 7,
     "sr1": (0.5, 0.5), "ae": (0.0, 0.5), "z_c": 0.1, "mpr": 0.3,
     "w": (0.45, 0.46, 0.47, 0.48), "r_pr": 0.2, "pb": (2, 4),
     "states": [(16, True), (17, True), (18, False), (19, True),
                (20, True), (21, False), (22, True)],
     "view": {"z_C": 0.2, "z_F": 0.1, "c_gate_on": True, "sec1_R_band": 2}},
    {"id": "905", "half": "loop_live", "gate": False, "n_band": 2,
     "sr1": (0.1, 2.2), "ae": (0.0, 2.0), "z_c": 0.0, "mpr": 0.6,
     "w": (0.49, 0.50, 0.51, 0.52), "r_pr": 0.3, "pb": (4, 4),
     "states": [(17, True), (18, True), (19, True), (33, True),
                (34, False), (35, True)],
     "view": {"z_C": 0.0, "z_F": 1.9, "c_gate_on": False, "sec1_R_band": 3}},
]

# the D'' attribution rows (held-out only; doc 3 a NEW FIRE via
# the f term, doc 7 an f-absent gate-off fire)
DPP_ATTRIB = [
    {"doc_id": "3", "terms": ["C", "F", "E", "f"], "z_c": 2.8,
     "z_f": 0.5, "z_e": 2.5, "z_ft": 2.3, "gate_on": True,
     "new_fire": True},
    {"doc_id": "7", "terms": ["C", "F"], "z_c": 0.0, "z_f": 2.0,
     "z_e": 0.3, "z_ft": None, "gate_on": False,
     "new_fire": False},
]


def doc_by(did):
    for d in DOCS:
        if d["id"] == str(did):
            return d
    raise KeyError(did)


def build_world():
    """THE INDEPENDENT WORLD-BUILDER: computes every aggregate
    from the primitives its own way, then emits a crafted export
    shaped exactly like the owner-side as-sized item-375 export.
    The tool's derivation must agree with THIS builder's
    numbers field-for-field -- two code paths."""
    per = {}
    for d in DOCS:
        gflags = [g for (_t, g) in d["states"]]
        n_states = len(d["states"])
        sr1_d = armed_D(d["gate"], d["sr1"][0], d["sr1"][1])
        ae_raw_c = AE_SCALE["mu_c"] + AE_SCALE["sd_c"] * d["ae"][0]
        ae_raw_f = AE_SCALE["mu_f"] + AE_SCALE["sd_f"] * d["ae"][1]
        ae_d = armed_D(d["gate"], d["ae"][0], d["ae"][1])
        base_d = None
        if "view" in d:
            base_d = armed_D(d["view"]["c_gate_on"],
                             d["view"]["z_C"], d["view"]["z_F"])
        per[d["id"]] = {
            "n_states": n_states,
            "gflags": gflags,
            "gap_total": sum(gflags),
            "r_gamma": (longest_run(gflags) / n_states
                        if n_states else None),
            "sr1_d": sr1_d, "sr1_fired": sr1_d >= T_SR1,
            "ae_d": ae_d, "ae_fired": ae_d >= T_AE,
            "ae_raw": (ae_raw_c, ae_raw_f),
            "base_d": base_d,
            "base_fired": (None if base_d is None
                           else base_d >= T_BASE),
        }

    ann, sec_h, commit_side = [], [], []
    readings = {h: [] for h in HALVES}
    forms_2a = {h: {} for h in HALVES}
    for d in DOCS:
        p = per[d["id"]]
        ann.append({
            "half": d["half"], "doc_id": d["id"],
            "n_states": p["n_states"], "n_commits": p["n_states"],
            "gate_on": d["gate"], "R_gamma": p["r_gamma"],
            "R_pr": d["r_pr"],
            "posture_band": {"gamma": d["pb"][0],
                             "retrained": d["pb"][1]},
            "shape": {"sr1_c": d["sr1"][0], "sr1_f": d["sr1"][1],
                      "gate": d["gate"], "D": p["sr1_d"],
                      "above_c": d["sr1"][0] > 1.0,
                      "above_f": d["sr1"][1] > 1.0,
                      "fired": p["sr1_fired"],
                      "fired_off": (p["sr1_fired"]
                                    and not d["gate"])},
        })
        sec_h.append({
            "doc_id": d["id"], "half": d["half"],
            "shape_candidates": {"maxPRsig": d["mpr"],
                                 "z_C": d["z_c"],
                                 "sec1_N_band": d["n_band"]},
            "commitment_raw": {"n_commits": p["n_states"],
                               "margin_min": d["w"][0],
                               "margin_mean": d["w"][1],
                               "K_mean": d["w"][2],
                               "hedge_mass_mean": d["w"][3]},
        })
        states_out = []
        for (t, g) in d["states"]:
            states_out.append({
                "t": t, "phase": "mid", "K": 0.5,
                "emitted_p": 0.5, "margin": 0.1,
                "content_mass": 0.2, "hedge_mass": 0.3,
                "gamma_p": 0.5, "gamma_g": (THETA_GAMMA if g
                                            else 1.0),
                "gm_p": 0.5, "gm_g": 0.5,
                "gamma_valid": True, "second_p": 0.5,
            })
        commit_side.append({
            "doc_id": d["id"], "half": d["half"],
            "summary": {"n_states": p["n_states"]},
            "states": states_out,
        })
        readings[d["half"]].append({
            "doc_id": d["id"],
            "readings": {
                MON_C: {"side": "C", "mild_option2": 0.05,
                        "forms": {"SR1": d["sr1"][0],
                                  "SR2": d["sr1"][0],
                                  "AE": p["ae_raw"][0],
                                  "OL": 0.1},
                        "no_readings": False},
                MON_F: {"side": "F", "mild_option2": 0.05,
                        "forms": {"SR1": d["sr1"][1],
                                  "SR2": d["sr1"][1],
                                  "AE": p["ae_raw"][1],
                                  "OL": 0.1},
                        "no_readings": False},
            },
        })
        if p["n_states"]:
            forms_2a[d["half"]][d["id"]] = {
                "n_states": p["n_states"],
                "n_gap_states": p["gap_total"],
                "form_R": p["r_gamma"]}

    def fires(which, half):
        return sum(1 for d in DOCS if d["half"] == half
                   and per[d["id"]][which])

    def fired_off(which, half):
        return sum(1 for d in DOCS if d["half"] == half
                   and per[d["id"]][which] and not d["gate"])

    sr1_comp = dict(SR1_SCALE)
    sr1_comp.update({
        "form": "SR-option-1 (RULED -- the center-crossing "
                "mild level)",
        "side_c_source": MON_C, "side_f_source": MON_F,
        "t_leg": T_SR1, "calib_ceil": 25, "level_set_ok": True,
        "calib_fires": fires("sr1_fired", "calibration"),
        "held_out_fires": fires("sr1_fired", "held_out"),
        "n_held_out": 6, "n_loops": 3, "held_rate": 0.5,
        "held_count_ceil": 1, "wilson_upper": 0.5,
        "fired_through_gate_off":
            fired_off("sr1_fired", "held_out"),
        "catches_t_leg": fires("sr1_fired", "loop_live"),
        "catches_t_esc": 1, "sigma_gap": 1.228, "auc": 0.785,
    })
    ae_comp = dict(AE_SCALE)
    ae_comp.update({
        "form": "AE (accumulated one-sided extent)",
        "side_c_source": MON_C, "side_f_source": MON_F,
        "t_leg": T_AE, "calib_ceil": 25, "level_set_ok": True,
        "calib_fires": fires("ae_fired", "calibration"),
        "held_out_fires": fires("ae_fired", "held_out"),
        "n_held_out": 6, "n_loops": 3, "held_rate": 0.25,
        "held_count_ceil": 1, "wilson_upper": 0.5,
        "fired_through_gate_off":
            fired_off("ae_fired", "held_out"),
        "catches_t_leg": fires("ae_fired", "loop_live"),
        "catches_t_esc": 1, "sigma_gap": 3.641, "auc": 0.999,
    })

    # the four-cell ledger (per half x per band 0-15); the
    # retrained split runs the crafted rule (odd t -> pr-gap)
    cells = {}
    for h in HALVES:
        for b in range(16):
            cells[h + ":" + str(b)] = {
                "n": 0, "gap&gap": 0, "gap&grounded": 0,
                "grounded&gap": 0, "grounded&grounded": 0}
    for d in DOCS:
        for (t, g) in d["states"]:
            pr = (t % 2 == 1)
            c = cells[d["half"] + ":" + str(t // 16)]
            c["n"] += 1
            if g and pr:
                c["gap&gap"] += 1
            elif g:
                c["gap&grounded"] += 1
            elif pr:
                c["grounded&gap"] += 1
            else:
                c["grounded&grounded"] += 1
    bd_bands = {}
    for b in range(16):
        bd_bands[str(b)] = {}
        for h in HALVES:
            c = cells[h + ":" + str(b)]
            bd_bands[str(b)][h] = {
                "n": c["n"],
                "gamma_in_gap": c["gap&gap"] + c["gap&grounded"],
                "retrained_in_gap":
                    c["gap&gap"] + c["grounded&gap"],
                "gamma_gap_pr_gap": c["gap&gap"],
                "gamma_gap_pr_grounded": c["gap&grounded"],
                "gamma_grounded_pr_gap": c["grounded&gap"],
                "gamma_grounded_pr_grounded":
                    c["grounded&grounded"]}

    # the banded two-way tables (per track x half x band 1-4)
    two_way = {}
    for tr, key in (("gamma", "gamma"), ("retrained", "retrained")):
        tbl = {}
        for h in HALVES:
            for b in (1, 2, 3, 4):
                sub = [d for d in DOCS if d["half"] == h
                       and d["pb"][0 if tr == "gamma" else 1] == b]
                ds = [per[d["id"]]["sr1_d"] for d in sub]
                tbl[h + ":" + str(b)] = {
                    "n": len(sub),
                    "gated_off": sum(1 for d in sub
                                     if not d["gate"]),
                    "mean": (sum(ds) / len(ds)) if ds else None,
                    "above_c": [0, 0], "above_f": [0, 0],
                    "fired": sum(1 for d in sub
                                 if per[d["id"]]["sr1_fired"]),
                    "fired_off": sum(
                        1 for d in sub
                        if per[d["id"]]["sr1_fired"]
                        and not d["gate"]),
                    "withheld": 0}
        two_way[tr] = {"disposition": "OK", "table": tbl}

    # the SEC-1 population summaries
    def summ(sel):
        sub = [d for d in DOCS if sel(d)]
        nb = [d["n_band"] for d in sub]
        rb = [d["view"]["sec1_R_band"] if "view" in d
              else d.get("nr_band") for d in sub]
        rb = [x for x in rb if x is not None]
        return {"n": len(sub),
                "mean_N_band": (sum(nb) / len(nb)) if nb else None,
                "mean_R_band": (sum(rb) / len(rb))
                if rb else None}

    fired_views = []
    for d in DOCS:
        if d["half"] == "held_out" and per[d["id"]]["base_fired"]:
            v = dict(d["view"])
            v["doc_id"] = d["id"]
            v["D"] = per[d["id"]]["base_d"]
            v["sec1_N_band"] = d["n_band"]
            fired_views.append(v)
    loop_views = []
    for d in DOCS:
        if d["half"] == "loop_live":
            v = dict(d["view"])
            v["doc_id"] = d["id"]
            v["D"] = per[d["id"]]["base_d"]
            v["sec1_N_band"] = d["n_band"]
            loop_views.append(v)

    base_catches = sum(1 for d in DOCS if d["half"] == "loop_live"
                       and per[d["id"]]["base_fired"])
    held_views = []
    for d in DOCS:
        if d["half"] == "held_out":
            v = dict(d["view"]) if "view" in d else {
                "z_C": 0.0, "z_F": 0.0, "c_gate_on": d["gate"],
                "sec1_R_band": 4}
            v["doc_id"] = d["id"]
            v["D"] = (per[d["id"]]["base_d"]
                      if per[d["id"]]["base_d"] is not None
                      else 0.0)
            v["sec1_N_band"] = d["n_band"]
            held_views.append(v)

    pf_pos = {
        "f_in": "in", "pr_side": "positive",
        "t_leg": T_DPP, "t_esc": T_DPP,
        "calib_fires": 90, "calib_ceil": 25,
        "level_set_ok": False, "n_calib": 6, "n_held_out": 6,
        "held_out_fires": len(DPP_ATTRIB), "held_rate": 0.25,
        "held_count_ceil": 1, "wilson_upper": 0.5,
        "fired_through_gate_off": sum(
            1 for a in DPP_ATTRIB if not a["gate_on"]),
        "ungated_f_fires_gate_off": sum(
            1 for a in DPP_ATTRIB
            if "f" in a["terms"] and not a["gate_on"]),
        "catches_t_leg": 1, "catches_t_esc": 1, "n_loops": 3,
        "new_fires": sorted(a["doc_id"] for a in DPP_ATTRIB
                            if a["new_fire"]),
        "attribution": DPP_ATTRIB,
        "sigma_gap": 1.777, "auc": 0.910}
    pf_neg = dict(pf_pos)
    pf_neg["sigma_gap"] = 1.957
    pf_neg["auc"] = 0.959

    leg_block = {
        "armed_sides": ["C", "F"],
        "gate_census": {
            "k_gate": 4, "side_c_armed": True,
            "calibration_gated": sum(
                1 for d in DOCS if d["half"] == "calibration"
                and not d["gate"]),
            "held_out_gated": sum(
                1 for d in DOCS if d["half"] == "held_out"
                and not d["gate"]),
            "loop_live_gated": sum(
                1 for d in DOCS if d["half"] == "loop_live"
                and not d["gate"]),
            "fired_gated": sum(
                1 for v in fired_views if not v["c_gate_on"]),
        },
        "thresholds": {"t_leg": T_BASE, "t_esc": 2.290,
                       "th_C_coelev": 1.0, "th_F_coelev": 1.0},
        "level_set_receipt": {"n_calib": 6, "alpha": 0.05,
                              "calib_fires": 1, "ceiling": 1,
                              "ok": True},
        "separation_context": {"sigma_gap_on_D": 0.981,
                               "auc_on_D": 0.674},
        "held_out": {"n": 6, "fires": len(fired_views),
                     "fired_docs": fired_views},
        "loop_catches": {"n_live": 3, "at_t_leg": base_catches,
                         "at_t_esc": 1},
        "populations": {
            "loops_live": loop_views,
            "summaries_at_0.90": {
                "loops_live": summ(
                    lambda d: d["half"] == "loop_live"),
                "held_out_clean_fired": summ(
                    lambda d: d["half"] == "held_out"
                    and per[d["id"]]["base_fired"]),
                "held_out_clean_nonfired": summ(
                    lambda d: d["half"] == "held_out"
                    and not per[d["id"]]["base_fired"]),
            },
        },
    }

    # the raw per-doc tiers ride under the top-level
    # amend_development block (the CC fork's own _am_export_block
    # law), NEVER under the walk-level legs block
    am_dev_block = {
        "section_h_two_way": {"per_doc": sec_h},
        "section_b_duration_family": {
            "commitment_side": {"per_doc": commit_side}},
    }

    return {
        "tool": "crafted-world-builder",
        "tool_sha256": "0" * 64,
        "tag": "crafted-world",
        "fixture_mode": True,
        "legs": {MATH_LEG: leg_block},
        "amend_development": {"legs": {MATH_LEG: am_dev_block}},
        "amend_cross_cond": {
            "theta_pr": {"value": 0.710523, "j": 0.3},
            "form_r_recompute": {
                "gamma": {"loop_vs_calib_sigma": -0.693,
                          "loop_vs_calib_auc": 0.292,
                          "loop_vs_held_out_sigma": -0.626,
                          "loop_vs_held_out_auc": 0.312},
                "retrained": {"loop_vs_calib_sigma": 1.975,
                              "loop_vs_calib_auc": 0.911,
                              "loop_vs_held_out_sigma": 1.951,
                              "loop_vs_held_out_auc": 0.909}},
            "two_way": two_way,
            "four_cell_ledger": {
                "bucket": 16,
                "bands_present": list(range(16)),
                "cells": cells,
                "corrections": {"(1,1)": "x", "(1,0)": "x",
                                "(0,1)": "x", "(0,0)": "x"}},
            "per_doc_annotations": ann,
        },
        "amend_duration_pair": {
            "classification_2a": {
                "theta_gamma": THETA_GAMMA},
            "lane_2b": {"gsmrw17": {
                "dominant_sides": {MON_C: "C", MON_F: "F"},
                "refused_monitors": [], "withheld_monitors": [],
                "mild_levels_option2": {MON_C: 0.05,
                                         MON_F: 0.05},
                "per_doc_readings": readings,
                "forms": {
                    "SR-option-1 (RULED -- the center-crossing "
                    "mild level)": sr1_comp,
                    "SR-option-2 (the mild-level variant)":
                        dict(sr1_comp, form="SR-option-2"),
                    "AE (accumulated one-sided extent)": ae_comp,
                    "OL (overload)":
                        dict(ae_comp, form="OL"),
                }}},
            "lane_2a": {"leg": "gsmrw17", "math_only": True,
                        "receipts": {
                            "forms": forms_2a,
                            "census": {h: {
                                "n_states": sum(
                                    per[d["id"]]["n_states"]
                                    for d in DOCS
                                    if d["half"] == h),
                                "n_gap_states": sum(
                                    per[d["id"]]["gap_total"]
                                    for d in DOCS
                                    if d["half"] == h)}
                                for h in HALVES},
                            "zero_commit_docs": {
                                h: [d["id"] for d in DOCS
                                    if d["half"] == h
                                    and not d["states"]]
                                for h in HALVES}}},
        },
        "amend_promotion_f": {
            "per_leg": {"gsmrw17": {
                "variants": {"f-IN/PR-positive": pf_pos,
                             "f-IN/PR-negative": pf_neg,
                             "f-OUT/PR-positive":
                                 dict(pf_pos, f_in="out"),
                             "f-OUT/PR-negative":
                                 dict(pf_neg, f_in="out")},
            }}},
        "amend_band_decomp": {
            "bands": bd_bands,
            "bands_present": list(range(16)),
        },
    }


def dump(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, sort_keys=True, indent=1,
                  ensure_ascii=True)
        f.write("\n")


def run_tool(export_path, out_path, fixture=True):
    cmd = [sys.executable, TOOL, "--export", export_path,
           "--out", out_path]
    if fixture:
        cmd.append("--fixture-mode")
    return subprocess.run(cmd, capture_output=True, text=True)


def find_row(rows, half, did):
    for r in rows:
        if r["half"] == half and r["doc_id"] == str(did):
            return r
    return None


def main():
    print("=" * 78)
    print("=== THE DEGENERATE-OUTPUT VIEW extraction/join tool --")
    print("=== THE ACCEPTANCE BATTERY (crafted worlds; the banked")
    print("=== anchors ECHO in fixture mode, the structural guards")
    print("=== enforce EXACT; every negative dies LOUD by name) ===")
    print("  the pinned sheet of record: "
          + TOOLMOD.SHEET_NAME + " (SHA-256 "
          + TOOLMOD.SHEET_SHA[:16] + "..."
          + TOOLMOD.SHEET_SHA[-6:] + "; " + TOOLMOD.SHEET_STAMP
          + ")")
    print("  the CC fork of record pinned: " + TOOLMOD.CC_FORK_NAME)
    print("  RECEIPTS ONLY; no weighted sums; no new fit; theta")
    print("  [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); DEVELOPMENT DATA ONLY;")
    print("  findings presented, never adjudicated -- the owner's")
    print("  stamps decide.")

    # (0) the compile gates
    try:
        py_compile.compile(TOOL, doraise=True)
        check("py_compile the extraction/join tool", True)
    except Exception as e:
        check("py_compile the extraction/join tool", False, e)
        print("  " + str(PASS) + " PASS / " + str(FAIL)
              + " FAIL -- aborting (a tool that does not compile")
        print("  is never run)")
        return 1
    try:
        py_compile.compile(os.path.abspath(__file__), doraise=True)
        check("py_compile the acceptance battery itself", True)
    except Exception as e:
        check("py_compile the acceptance battery itself", False, e)

    # (1) the crafted world, built + dumped
    world = build_world()
    wpath = os.path.join(FIXDIR, "crafted_world.json")
    dump(world, wpath)
    out1 = os.path.join(FIXDIR, "join_out_run1.json")
    out2 = os.path.join(FIXDIR, "join_out_run2.json")
    check("the crafted world carries 15 annotations",
          len(world["amend_cross_cond"]
              ["per_doc_annotations"]) == 15)

    # (2) THE POSITIVE RUN (fixture mode -- the banked anchors
    # echo; the structural two-code-path guards enforce)
    p1 = run_tool(wpath, out1, fixture=True)
    check("the fixture-mode run completes (exit 0)",
          p1.returncode == 0, p1.stderr[-400:])
    if p1.returncode != 0:
        print(p1.stdout[-3000:])
        print(p1.stderr[-3000:])
        print("  " + str(PASS) + " PASS / " + str(FAIL)
              + " FAIL -- the positive run failed; aborting")
        return 1
    check("the positive console carries no abort",
          "aborting" not in p1.stdout)
    check("the row-domain line reads 15 rows",
          "6 calibration + 6 held-out + 3 loops = 15 rows"
          in p1.stdout, p1.stdout[:600])
    check("the fixture-mode banner rides",
          "[fixture-mode] THE BANKED-ANCHOR PINS ECHO"
          in p1.stdout)
    check("the set-union console line reads 3/3 (1+1+1)",
          "3/3 loops (1 shape-only + 1 dual + 1 posture-only)"
          in p1.stdout)
    m = re.search(r"(\d+) anchors checked: (\d+) EXACT, "
                  r"(\d+) ECHO", p1.stdout)
    check("the anchors summary line parses",
          m is not None, p1.stdout[-800:])
    if m:
        tot, n_ex, n_ec = (int(m.group(1)), int(m.group(2)),
                           int(m.group(3)))
        check("fixture mode: every anchor ECHO, none EXACT",
              tot == n_ec and n_ex == 0 and tot > 100,
              (tot, n_ex, n_ec))

    with open(out1) as f:
        j1 = json.load(f)
    rows = j1["rows"]
    check("the join table carries all 15 rows", len(rows) == 15)
    check("the out mode names FIXTURE",
          j1["mode"].startswith("FIXTURE"))
    check("the row order is (population, numeric id)",
          [(r["half"], r["doc_id"]) for r in rows] == [
              ("calibration", d) for d in
              ("0", "2", "4", "6", "8", "10")]
          + [("held_out", d) for d in
             ("1", "3", "5", "7", "9", "11")]
          + [("loop_live", d) for d in
             ("901", "903", "905")])

    # (3) THE HAND-DERIVED EXPECTED ROWS (full literals)
    dev_label = ("DEVELOPMENT DATA ONLY -- 3B/scout/fp16 "
                 "lane; never a run of record; never "
                 "adjudicated")
    exp0 = {
        "doc_id": "0", "half": "calibration",
        "population": "clean", "development_label": dev_label,
        "l1_validity": {
            "n_band": 6,
            "r_band": W + " (the per-doc SEC-1 R_band rides the "
            "fired/loop doc views only; the as-sized export's "
            "aggregate SEC-1 means ride surfaces.taxonomy)",
            "gate_armed": True, "k_gate": 4,
            "fired_through_gate_off": {"base_d": None,
                                       "sr1": False,
                                       "ae": False,
                                       "dpp": None}},
        "l2_commitment": {
            "law": "FORM R dual-sided, both tracks side by "
            "side (the 365-STAMP dual-sided law; the PR TIE "
            "unbroken both-sided)",
            "r_gamma": 1.0, "r_pr": 0.5,
            "retrained_circularity_note":
                "the retrained classification was fit on this "
            "leg's own commitment states -- DEVELOPMENT "
            "receipts, never independent evidence (the probe-"
            "circularity disclosure rides every retracted "
            "column)",
            "n_commits": 6, "zero_commit": False},
        "l3_shape": {
            "law": "ALL FOUR composite fire surfaces side-by-"
            "side (Directive 1 -- no single-trigger blindness)",
            "base_d": W_BASE_CAL, "base_d_fired": W_BASE_CAL,
            "sr1_d": 2.0, "sr1_fired": True,
            "sr1_above_mild_pr": True,
            "sr1_above_mild_s": False,
            "ae_d": 2.5, "ae_fired": True,
            "ae_note": "derived from the export's own per-doc "
            "raw readings under the AE composite's own exported "
            "scales + gate flags (the armed construction); "
            "asserted against the composite's own aggregate "
            "receipts EXACT",
            "dpp_fired": W_DPP},
        "l4_register_monitor": {
            "z_c": 0.4, "max_pr_sig": 1.2,
            "z_f": W + " (the per-doc z_F rides the fired/loop "
            "doc views only)",
            "z_e": W + " (the per-doc z_e rides the D'' "
            "attribution rows only)",
            "z_f_term": W + " (the per-doc z_f term rides the "
            "D'' attribution rows only)",
            "dpp_terms": W_DPP, "dpp_new_fire": W_DPP},
        "l5_depth": {
            "n_states": 6,
            "depth_band_state_counts": [6] + [0] * 15,
            "band_rule": "t//16 (the item-369 sixteen-band "
            "decomposition)"},
        "l6_state": {
            "gamma_in_gap_states": 6,
            "gamma_in_gap_by_band": [6] + [0] * 15,
            "gamma_clause": "in-gap iff gamma_valid AND gamma_g "
            "<= theta_gamma "
            + repr(THETA_GAMMA)
            + " (the 325-STAMP gamma clause, verbatim)",
            "four_cell_counts": W_STATE},
        "l7_posture": {
            "posture_band_gamma": 1,
            "posture_band_retrained": 1,
            "r_gamma_zero_subband": False,
            "r_pr_zero_subband": False,
            "weight_forms": {"n_commits": 6, "margin_min": 0.01,
                             "margin_mean": 0.02,
                             "K_mean": 0.03,
                             "hedge_mass_mean": 0.04},
            "note": "the posture bands ANNOTATE, never input "
            "(the no-weighted-sum law); hedge_mass_mean the "
            "form-scoped degeneracy candidate (NAMED-DEGENERATE "
            "on the math leg)"},
    }
    got0 = find_row(rows, "calibration", "0")
    check("row doc 0 EXACT (a calibration SR1+AE fire)",
          got0 == exp0,
          "got " + json.dumps(got0, sort_keys=True)[:1200]
          if got0 else "row missing")

    exp3 = {
        "doc_id": "3", "half": "held_out",
        "population": "clean", "development_label": dev_label,
        "l1_validity": {
            "n_band": 8, "r_band": 1, "gate_armed": True,
            "k_gate": 4,
            "fired_through_gate_off": {"base_d": False,
                                       "sr1": False,
                                       "ae": False,
                                       "dpp": False}},
        "l2_commitment": {
            "law": exp0["l2_commitment"]["law"],
            "r_gamma": 0.375, "r_pr": 0.5,
            "retrained_circularity_note":
                exp0["l2_commitment"]
                    ["retrained_circularity_note"],
            "n_commits": 8, "zero_commit": False},
        "l3_shape": {
            "law": exp0["l3_shape"]["law"],
            "base_d": 2.8, "base_d_fired": True,
            "sr1_d": 2.1, "sr1_fired": True,
            "sr1_above_mild_pr": True,
            "sr1_above_mild_s": False,
            "ae_d": 2.5, "ae_fired": True,
            "ae_note": exp0["l3_shape"]["ae_note"],
            "dpp_fired": True},
        "l4_register_monitor": {
            "z_c": 1.1, "max_pr_sig": 2.0, "z_f": 0.5,
            "z_e": 2.5, "z_f_term": 2.3,
            "dpp_terms": ["C", "F", "E", "f"],
            "dpp_new_fire": True},
        "l5_depth": {
            "n_states": 8,
            "depth_band_state_counts": [8] + [0] * 15,
            "band_rule": exp0["l5_depth"]["band_rule"]},
        "l6_state": {
            "gamma_in_gap_states": 6,
            "gamma_in_gap_by_band": [6] + [0] * 15,
            "gamma_clause": exp0["l6_state"]["gamma_clause"],
            "four_cell_counts": W_STATE},
        "l7_posture": {
            "posture_band_gamma": 1,
            "posture_band_retrained": 4,
            "r_gamma_zero_subband": False,
            "r_pr_zero_subband": False,
            "weight_forms": {"n_commits": 8, "margin_min": 0.25,
                             "margin_mean": 0.26,
                             "K_mean": 0.27,
                             "hedge_mass_mean": 0.28},
            "note": exp0["l7_posture"]["note"]},
    }
    got3 = find_row(rows, "held_out", "3")
    check("row doc 3 EXACT (Base D fired clean + D'' NEW FIRE)",
          got3 == exp3,
          "got " + json.dumps(got3, sort_keys=True)[:1200]
          if got3 else "row missing")

    exp901 = {
        "doc_id": "901", "half": "loop_live",
        "population": "loop", "development_label": dev_label,
        "l1_validity": {
            "n_band": 9, "r_band": 1, "gate_armed": True,
            "k_gate": 4,
            "fired_through_gate_off": {"base_d": False,
                                       "sr1": False,
                                       "ae": False,
                                       "dpp": None}},
        "l2_commitment": {
            "law": exp0["l2_commitment"]["law"],
            "r_gamma": 1.0, "r_pr": 0.9,
            "retrained_circularity_note":
                exp0["l2_commitment"]
                    ["retrained_circularity_note"],
            "n_commits": 9, "zero_commit": False},
        "l3_shape": {
            "law": exp0["l3_shape"]["law"],
            "base_d": 2.9, "base_d_fired": True,
            "sr1_d": 3.0, "sr1_fired": True,
            "sr1_above_mild_pr": True,
            "sr1_above_mild_s": True,
            "ae_d": 2.0, "ae_fired": True,
            "ae_note": exp0["l3_shape"]["ae_note"],
            "dpp_fired": W_DPP},
        "l4_register_monitor": {
            "z_c": 0.9, "max_pr_sig": 2.5, "z_f": 1.0,
            "z_e": W + " (the per-doc z_e rides the D'' "
            "attribution rows only)",
            "z_f_term": W + " (the per-doc z_f term rides the "
            "D'' attribution rows only)",
            "dpp_terms": W_DPP, "dpp_new_fire": W_DPP},
        "l5_depth": {
            "n_states": 9,
            "depth_band_state_counts": [9] + [0] * 15,
            "band_rule": exp0["l5_depth"]["band_rule"]},
        "l6_state": {
            "gamma_in_gap_states": 9,
            "gamma_in_gap_by_band": [9] + [0] * 15,
            "gamma_clause": exp0["l6_state"]["gamma_clause"],
            "four_cell_counts": W_STATE},
        "l7_posture": {
            "posture_band_gamma": 1,
            "posture_band_retrained": 1,
            "r_gamma_zero_subband": False,
            "r_pr_zero_subband": False,
            "weight_forms": {"n_commits": 9, "margin_min": 0.41,
                             "margin_mean": 0.42,
                             "K_mean": 0.43,
                             "hedge_mass_mean": 0.44},
            "note": exp0["l7_posture"]["note"]},
    }
    got901 = find_row(rows, "loop_live", "901")
    check("row doc 901 EXACT (a loop shape-only fire)",
          got901 == exp901,
          "got " + json.dumps(got901, sort_keys=True)[:1200]
          if got901 else "row missing")

    # (4) the WITHHELD marker round-trips (the as-sized law)
    r2 = find_row(rows, "calibration", "2")
    check("marker round-trip: Base D calibration WITHHELD",
          r2 is not None
          and r2["l3_shape"]["base_d"] == W_BASE_CAL
          and r2["l3_shape"]["base_d_fired"] == W_BASE_CAL)
    r5 = find_row(rows, "held_out", "5")
    check("marker round-trip: D'' non-attributed held doc -- "
          "the fire status a REAL reading, the terms/new-fire "
          "WITHHELD-named",
          r5 is not None
          and r5["l3_shape"]["dpp_fired"] is False
          and r5["l4_register_monitor"]["dpp_terms"] == W_DPP
          and r5["l4_register_monitor"]["dpp_new_fire"] == W_DPP)
    r905 = find_row(rows, "loop_live", "905")
    check("marker round-trip: D'' loop per-row WITHHELD",
          r905 is not None
          and r905["l3_shape"]["dpp_fired"] == W_DPP)
    r10 = find_row(rows, "calibration", "10")
    check("the zero-commit doc rides WITHHELD-named (never "
          "pooled)",
          r10 is not None
          and r10["l2_commitment"]["zero_commit"] is True
          and r10["l2_commitment"]["r_gamma"] is None
          and r10["l7_posture"]["posture_band_gamma"] is None
          and r10["l6_state"]["four_cell_counts"] == W_STATE)
    check("marker round-trip: every row's four-cell counts "
          "WITHHELD-named",
          all(r["l6_state"]["four_cell_counts"] == W_STATE
              for r in rows))

    # (5) the surfaces (spot checks, hand-derived)
    sf = j1["surfaces"]
    check("the four-cell census surface reads "
          "[20,14]/[28,18]/[22,19]",
          sf["four_cell_ledger"]["census"] == {
              "calibration": [20, 14],
              "held_out": [28, 18],
              "loop_live": [22, 19]},
          sf["four_cell_ledger"]["census"])
    cs = sf["composite_surfaces"]
    check("Base D surface: 2 held fires / 2 catches / 1 "
          "gate-off",
          cs["base_d"]["held_fires"] == 2
          and cs["base_d"]["loop_catches"] == 2
          and cs["base_d"]["fired_gate_off"] == 1)
    check("SR1 surface: cal 2 / held 3 / catches 2 / gate-off 1",
          cs["sr1"]["calib_fires"] == 2
          and cs["sr1"]["held_fires"] == 3
          and cs["sr1"]["loop_catches"] == 2
          and cs["sr1"]["fired_gate_off"] == 1)
    check("AE surface: cal 3 / held 2 / catches 2 / gate-off 1",
          cs["ae"]["calib_fires"] == 3
          and cs["ae"]["held_fires"] == 2
          and cs["ae"]["loop_catches"] == 2
          and cs["ae"]["fired_gate_off"] == 1)
    check("D'' surface: held 2 / NEW FIRES 1 / ungated-f 0",
          cs["dpp"]["held_fires"] == 2
          and cs["dpp"]["new_fires"] == 1
          and cs["dpp"]["ungated_f"] == 0)
    bm = sf["band_marginals"]["gamma"]["calibration"]["1"]
    check("band marginal spot: gamma cal band 1 (n 2, SR1 1, "
          "AE 2, D'' 0)",
          bm == {"n": 2, "sr1_fired": 1,
                 "sr1_nonfiring_clean": 1, "ae_fired": 2,
                 "ae_nonfiring_clean": 0, "dpp_fired": 0,
                 "dpp_nonfiring": 2}, bm)
    su = sf["set_union"]
    check("the set-union surface: 3/3 with arms 901/905/903",
          su["coverage"] == [3, 3]
          and su["shape_only"] == ["901"]
          and su["dual"] == ["905"]
          and su["posture_only"] == ["903"])
    check("the set-union cost side: band-4 clean 1 cal + 1 held",
          su["cost_side_band4_clean"] == {"calibration": 1,
                                          "held_out": 1})
    tg = sf["taxonomy"]["gate_off_fire_rate"]
    check("the taxonomy gate-off rates: loops SR1 [1,2] / AE "
          "[1,2] / Base D [1,2]; held SR1 [1,3]",
          tg["loops"]["sr1"] == [1, 2]
          and tg["loops"]["ae"] == [1, 2]
          and tg["loops"]["base_d"] == [1, 2]
          and tg["phenomenon_beta_held_clean"]["sr1"] == [1, 3])
    check("the anchor log rides in the out JSON, all ECHO",
          len(j1["regression_anchors"]) > 100
          and all(a["status"].startswith("ECHO")
                  for a in j1["regression_anchors"]))

    # (5b) THE BANKED PIN-TABLE STRUCTURAL LINT -- the owner-
    # side dies of record (a None in a count position; a
    # wrong-shape tuple) proved the pin table is the one
    # artifact fixture mode CANNOT value-test (it ECHOes,
    # never enforces); this lint enforces the table's own
    # SHAPE law on every battery run: arity exact, no None
    # ever riding a count position (only the two-way shape
    # mean may be None, and only in slot 5)
    B = TOOLMOD.BANKED
    ok_pins = True
    for _tr in ("gamma", "retrained"):
        for _h in HALVES:
            for _cell in B["two_way"][_tr][_h]:
                if (len(_cell) != 5
                        or any(v is None for v in _cell[:4])
                        or _cell[4] is not None
                        and not isinstance(_cell[4], float)):
                    ok_pins = False
    for _pin in B["fired_bands"].values():
        if (len(_pin) != 2
                or any(v is None for v in _pin)):
            ok_pins = False
    for _pin in B["sec1"].values():
        if (len(_pin) != 2 or _pin[0] is None
                or _pin[1] is None):
            ok_pins = False
    for _tr in ("gamma", "retrained"):
        for _pair in ("loop_vs_calib", "loop_vs_held_out"):
            _pin = B["form_r"][_tr][_pair]
            if (len(_pin) != 2
                    or any(v is None for v in _pin)):
                ok_pins = False
    for _tr in ("gamma", "retrained"):
        _pin = B["named_gated_band_totals"][_tr]
        if (len(_pin) != 4 or any(v is None for v in _pin)):
            ok_pins = False
    check("the BANKED pin-table structural lint (arity "
          "exact; never a None in a count position)",
          ok_pins)

    # (6) DETERMINISM -- byte-identical stdout + out file
    # (the tool prints the --out basename in its completion
    # line, so the second run writes the SAME path)
    with open(out1, "rb") as f:
        b1 = f.read()
    p2 = run_tool(wpath, out1, fixture=True)
    check("the second run completes (exit 0)",
          p2.returncode == 0)
    with open(out1, "rb") as f:
        b2 = f.read()
    check("determinism: byte-identical --out across runs",
          b1 == b2)
    check("determinism: byte-identical stdout across runs",
          p1.stdout == p2.stdout)

    # --------------------------------------------------------
    # (7) THE NEGATIVE FIXTURES -- every guard dies LOUD by
    # name; never a silent pick; never a crash without a name
    # --------------------------------------------------------
    def negative(name, mutate, expect, fixture=True):
        w = copy.deepcopy(world)
        mutate(w)
        path = os.path.join(
            FIXDIR, "neg_" + name.split("_")[0]
            + re.sub(r"[^A-Za-z0-9]", "", name)[:24]
            + ".json")
        dump(w, path)
        p = run_tool(path, path + ".out", fixture=fixture)
        ok = (p.returncode == 2
              and ("[degenerate-view-join] " + expect + ":")
              in p.stderr
              and "COMPLETE (" not in p.stdout)
        check("negative -- " + name + " dies " + expect, ok,
              (p.returncode, p.stderr[-300:]))

    def set_prov_ok(w):
        w["tool"] = TOOLMOD.CC_FORK_NAME
        w["tool_sha256"] = TOOLMOD.CC_FORK_SHA
        w["tag"] = TOOLMOD.EXPORT_TAG
        w["fixture_mode"] = True

    # provenance + real-mode guards
    negative("wrong-tag-real-mode",
             lambda w: w.update(tag="wrong-tag"),
             "PROVENANCE", fixture=False)
    negative("wrong-tool-sha-real-mode",
             lambda w: w.update(
                 tool=TOOLMOD.CC_FORK_NAME,
                 tag=TOOLMOD.EXPORT_TAG,
                 tool_sha256="1" * 64),
             "PROVENANCE", fixture=False)
    negative("fixture-flag-real-mode",
             set_prov_ok, "PROVENANCE", fixture=False)
    # the fixture flag must be flipped False for the next one
    w4 = copy.deepcopy(world)
    set_prov_ok(w4)
    w4["fixture_mode"] = False
    p4path = os.path.join(FIXDIR, "neg_real_mode_rowdomain.json")
    dump(w4, p4path)
    p4 = run_tool(p4path, p4path + ".out", fixture=False)
    check("negative -- real mode refuses the crafted row "
          "domain (ROW-DOMAIN)",
          p4.returncode == 2
          and "[degenerate-view-join] ROW-DOMAIN:" in p4.stderr
          and "COMPLETE (" not in p4.stdout,
          (p4.returncode, p4.stderr[-300:]))

    # missing blocks
    negative("missing-band-decomp-block",
             lambda w: w.pop("amend_band_decomp"),
             "MISSING-BLOCK")
    negative("missing-annotation-block",
             lambda w: w["amend_cross_cond"].pop(
                 "per_doc_annotations"),
             "MISSING-BLOCK")
    # the amend_development vehicle: the raw tiers A-H ride
    # there (the owner-side Section H die of record is covered
    # by these two guards)
    negative("missing-amend-development-block",
             lambda w: w.pop("amend_development"),
             "MISSING-BLOCK")
    negative("missing-section-h-in-amend-development",
             lambda w: w["amend_development"]["legs"]
             [MATH_LEG].pop("section_h_two_way"),
             "MISSING-BLOCK")

    # row-domain guards
    def dup_doc(w):
        ann = w["amend_cross_cond"]["per_doc_annotations"]
        ann.append(copy.deepcopy(ann[0]))
    negative("duplicate-doc-annotation", dup_doc, "ROW-DOMAIN")

    def parity_break(w):
        for r in (w["amend_cross_cond"]
                  ["per_doc_annotations"]):
            if r["doc_id"] == "4":
                r["half"] = "held_out"
    negative("parity-law-violation", parity_break, "ROW-DOMAIN")

    def crossblock_drop(w):
        sc = (w["amend_development"]["legs"]["gsmrw17"]
              ["section_h_two_way"]["per_doc"])
        for r in sc:
            if r["doc_id"] == "6":
                sc.remove(r)
    negative("cross-block-completeness", crossblock_drop,
             "ROW-DOMAIN")

    # the gate law
    def gate_law(w):
        for r in (w["amend_cross_cond"]
                  ["per_doc_annotations"]):
            if r["doc_id"] == "11":
                r["gate_on"] = True
        for r in (w["amend_development"]["legs"]["gsmrw17"]
                  ["section_h_two_way"]["per_doc"]):
            if r["doc_id"] == "11":
                r["shape_candidates"]["sec1_N_band"] = 3
    negative("gate-arms-under-K", gate_law, "GATE-LAW")

    # two-code-path guards
    def sr1_flip(w):
        for r in (w["amend_cross_cond"]
                  ["per_doc_annotations"]):
            if r["doc_id"] == "0":
                r["shape"]["fired"] = False
    negative("SR1-fire-status-vs-D", sr1_flip, "TWO-CODE-PATHS")

    def r_gamma_drift(w):
        for r in (w["amend_cross_cond"]
                  ["per_doc_annotations"]):
            if r["doc_id"] == "4":
                r["R_gamma"] = 0.123
    negative("FORM-R-annotation-drift", r_gamma_drift,
             "TWO-CODE-PATHS")

    def census_bump(w):
        (w["amend_cross_cond"]["four_cell_ledger"]
         ["cells"]["calibration:0"]["n"]) += 1
    negative("four-cell-census-drift", census_bump,
             "TWO-CODE-PATHS")

    def bd_drift(w):
        (w["amend_band_decomp"]["bands"]["1"]
         ["calibration"]["gamma_gap_pr_gap"]) += 1
    negative("BD-vs-CC-cell-drift", bd_drift, "TWO-CODE-PATHS")

    def ae_count_drift(w):
        forms = (w["amend_duration_pair"]["lane_2b"]
                 ["gsmrw17"]["forms"])
        for k in forms:
            if k.startswith("AE"):
                forms[k]["held_out_fires"] = 99
    negative("AE-aggregate-drift", ae_count_drift,
             "TWO-CODE-PATHS")

    def tw_drift(w):
        (w["amend_cross_cond"]["two_way"]["gamma"]
         ["table"]["calibration:1"]["fired"]) = 5
    negative("two-way-table-drift", tw_drift, "TWO-CODE-PATHS")

    def dpp_newfire_nof(w):
        for a in (w["amend_promotion_f"]["per_leg"]
                  ["gsmrw17"]["variants"]
                  ["f-IN/PR-positive"]["attribution"]):
            if a["doc_id"] == "3":
                a["terms"] = ["C", "F", "E"]
    negative("D''-new-fire-without-f-term",
             dpp_newfire_nof, "TWO-CODE-PATHS")

    def union_survivor(w):
        for r in (w["amend_cross_cond"]
                  ["per_doc_annotations"]):
            if r["doc_id"] == "903":
                r["posture_band"]["retrained"] = 2
        tbl = (w["amend_cross_cond"]["two_way"]["retrained"]
               ["table"])
        tbl["loop_live:4"] = {"n": 1, "gated_off": 1,
                              "mean": 2.2, "above_c": [0, 0],
                              "above_f": [0, 0], "fired": 1,
                              "fired_off": 1, "withheld": 0}
        tbl["loop_live:2"] = {"n": 1, "gated_off": 0,
                              "mean": 0.5, "above_c": [0, 0],
                              "above_f": [0, 0], "fired": 0,
                              "fired_off": 0, "withheld": 0}
    negative("set-union-survivor", union_survivor,
             "TWO-CODE-PATHS")

    def state_t_missing(w):
        cs = (w["amend_development"]["legs"]["gsmrw17"]
              ["section_b_duration_family"]
              ["commitment_side"]["per_doc"])
        for r in cs:
            if r["doc_id"] == "4":
                del r["states"][0]["t"]
    negative("state-without-t", state_t_missing, "STATE-TABLE")

    def state_t_out_of_domain(w):
        cs = (w["amend_development"]["legs"]["gsmrw17"]
              ["section_b_duration_family"]
              ["commitment_side"]["per_doc"])
        for r in cs:
            if r["doc_id"] == "4":
                r["states"][0]["t"] = 300
    negative("state-t-out-of-depth-domain",
             state_t_out_of_domain, "STATE-TABLE")

    def theta_drift(w):
        (w["amend_duration_pair"]["classification_2a"]
         ["theta_gamma"]) = 0.1
    negative("gamma-clause-theta-drift", theta_drift,
             "TWO-CODE-PATHS")

    def state_census_drift(w):
        (w["amend_duration_pair"]["lane_2a"]["receipts"]
         ["forms"]["calibration"]["0"]["n_gap_states"]) = 99
    negative("lane-2a-n-gap-drift", state_census_drift,
             "TWO-CODE-PATHS")

    # --------------------------------------------------------
    print()
    print("  " + str(PASS) + " PASS / " + str(FAIL) + " FAIL"
          + (" -- FAILURES: " + ", ".join(FAILS)
             if FAILS else ""))
    if FAIL:
        print("  THE BATTERY IS RED -- the build never ships "
              "on a red battery; every failure disclosed "
              "honestly; the owner's stamps decide.")
        return 1
    print("  THE BATTERY IS GREEN -- every guard proven "
          "die-loud by name; the join reproduces the crafted")
    print("  world's own aggregates EXACT (two code paths "
          "agree); the markers round-trip; the runs are "
          "byte-")
    print("  identical; DEVELOPMENT DATA ONLY; never a run of "
          "record; never adjudicated; findings presented,")
    print("  never adjudicated -- the owner's stamps decide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

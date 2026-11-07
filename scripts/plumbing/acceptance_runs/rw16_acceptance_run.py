#!/usr/bin/env python3
"""rw16_acceptance_run.py -- the zero-GPU acceptance run for
triadic_rw16_ensemble_readout.py (my stamped RW-16 one-sheet
pre-reg's sec. 5 acceptance; sheet SHA-256 6f3af50ecc6dd8a5a7dac647bb
954e5f471c55123c182208dfdf0d4c46ef4ef8, stamped ledger item 221;
R16-D1(a) item 220; R16-D2 two-stage alpha item 221).

Builds the synthetic calib/test cache fixtures DETERMINISTICALLY
(hand-authored arithmetic shapes, zero randomness -- every value an
exact arithmetic sequence), then runs the ensemble readout tool
against each and asserts the pre-registered expectations:

  F1  clean four-leg run: the calibration z/threshold math hand-
      checked against an INDEPENDENT recomputation (the runner's own
      arithmetic, never the tool's functions); the max-combination;
      AUC exactly 1.0 by construction; per-leg fire accounting; the
      forensics blocks; the census line + premise verification; the
      per-leg own-cache positives; the cross-set 10/10 identical
      report; the fixture-mode pin echo;
  F2  the fire-rate falsifier: hot clean docs push a test leg over
      the 5% coarse guard -> CANDIDATE-KILLED-FALSE-ALARM-BUDGET even
      though the sigma-gap passes;
  F3a negative-population guard (4 clean docs) -> INCONCLUSIVE;
  F3b positive-population guard (3 live / 7 inert fixtures) ->
      INCONCLUSIVE on all four legs;
  F4  unit checks via import: the pinned jitter-band typings (FAIL /
      INCONCLUSIVE-FROM-JITTER / PASS + near-bar / PASS), both
      population guards, the pinned _quantile, sigma_gap, the Wilson
      upper bound, the pinned constants, the 35-doc census;
  F5a-i hard exits: census premise violated; out-of-census absent
      statistic; key mismatch; truncated record; unknown leg;
      duplicate leg across calib caches; within-set fixture copy
      divergence; missing leg (calib set / test set); the item-199
      pin law outside fixture-mode;
  F6  cross-set fixture divergence REPORTED, never an exit (the new
      walks are the virgin record; their story is told, not
      enforced);
  F7  determinism: a fresh re-run's export byte-identical;
  F8  tuned legs: gap 2.01 -> PASS_2SIGMA + the near-bar flag; gap
      1.99 -> INCONCLUSIVE-FROM-JITTER; the candidate-level jitter
      typing.

  DOC-SPLIT AMENDMENT FAMILIES (ledger item 229, my stamped
  Option B; additive --doc-split mode on the tool):

  F9  the clean four-leg SPLIT run: the four walk caches passed ONCE
      as --calib-cache with --doc-split; the parity split (EVEN =
      calibration, ODD = held-out); the calibration-half-only
      baselines + mu/sd + thresholds hand-checked against an
      INDEPENDENT recomputation (the runner's own arithmetic, never
      the tool's functions); held-out-half-only fires + gap + AUC +
      Wilson; the per-leg doc_split block (n_even/n_odd + the item-229
      rule text + the candidate-selection caveat); determinism;
  F10 the split-mode fire falsifier: hot clean docs on the ODD
      (held-out) half of the gsm leg -> CANDIDATE-KILLED even though
      the gap passes;
  F11 the PER-HALF population guard: a 2-doc calibration half with a
      6-doc held-out half types INCONCLUSIVE-POPULATION-GUARD naming
      the per-half guard (the positives are untouched -- the guard
      fires on the half, not the fixtures);
  F12 non-int corpus doc_id in split mode -> HARD EXIT (parity
      requires int doc_ids; loop fixtures exempt);
  F13 the CLI hard exits: --doc-split with --test-cache -> HARD
      EXIT; the two-set mode with no --test-cache -> HARD EXIT;
  F14 split-mode determinism: a fresh re-run's export
      byte-identical;
  F15 the LEGACY-MODE REGRESSION: the amended tool's two-set run vs
      the preserved v1 build of record (item 222) -- console stdout
      byte-identical and the export equal in every field except the
      tool's own SHA.

FIXTURE DESIGN (hand-computable): every corpus doc carries ONE step
with per-doc constants s_i / PR_i on exact arithmetic sequences; the
loop fixtures carry 64 constant-valued steps (8) + 8-step inert (2).
The per-leg layer baselines thereby reduce EXACTLY to the per-doc
value lists (mean/std, ddof=1), so maxPRsig = (mu_PR - PR_i)/sd_PR
and minS = s_i are closed-form -- the runner recomputes every
expected quantity from these lists with its own arithmetic.

Fix-the-fixture-or-the-builder, never the tool. FAIL LOUD.
"""

import hashlib
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_rw16_ensemble_readout.py")
TOOL_V1 = os.path.join(HERE, "triadic_rw16_ensemble_readout_v1.py")
V1_PIN = ("03a069660282461d5b857f9e4801f57f2c4cd69d87df7c0f67c"
          "93fcc6719858f")
FIXDIR = os.path.join(HERE, "rw16_readout_fixtures")
OUTDIR = os.path.join(FIXDIR, "outs")

ALPHA = 0.05
ALPHA_SIDE = 0.025
NAMES = ["loop-injection-prose", "loop-injection-code",
         "mask-reserved-stubborn", "loop-seeded-counter",
         "loop-seeded-cycle", "loop-seeded-affirm",
         "loop-seeded-json", "loop-seeded-countdown",
         "loop-seeded-chant", "loop-seeded-code-line"]
STEP_KEYS = ("t", "id", "E", "rho", "s", "f", "layer", "H", "PR",
             "a", "rsize", "dead5", "dead4", "dead3", "dead_share")

# ---- the pinned fixture value constants (shared by the builder and
# the independent expectation mirror; every value closed-form) ----
N_CLEAN = 41


def cal_lists():
    s = [0.10 + 0.001 * i for i in range(N_CLEAN)]
    pr = [6.0 - 0.05 * i for i in range(N_CLEAN)]
    return s, pr


def tst_lists():
    s = [0.15 + 0.001 * i + 0.0002 * (i % 3) for i in range(N_CLEAN)]
    pr = [5.8 - 0.062 * i for i in range(N_CLEAN)]
    return s, pr


def live_lists():
    s = [0.90 + 0.0005 * j for j in range(8)]
    pr = [2.0 + 0.005 * j for j in range(8)]
    return s, pr


INERT_S, INERT_PR, INERT_N = 0.88, 2.05, 8


# =========================================
# The independent expectation mirror (the runner's OWN arithmetic --
# never the tool's functions; the pinned spec re-implemented).
# =========================================
def mstd(v):
    m = sum(v) / len(v)
    sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5
    return m, sd


def quant(sorted_v, q):
    n = len(sorted_v)
    p = q * (n - 1)
    lo = int(math.floor(p))
    frac = p - lo
    if frac <= 0.0:
        return float(sorted_v[lo])
    if lo + 1 >= n:
        return float(sorted_v[-1])
    return (float(sorted_v[lo])
            + frac * (float(sorted_v[lo + 1]) - float(sorted_v[lo])))


def sgap(pos, neg):
    mp = sum(pos) / len(pos)
    mn = sum(neg) / len(neg)
    sp = (sum((v - mp) ** 2 for v in pos) / (len(pos) - 1)) ** 0.5
    sn = (sum((v - mn) ** 2 for v in neg) / (len(neg) - 1)) ** 0.5
    pooled = math.sqrt((sp * sp + sn * sn) / 2.0)
    return (mp - mn) / pooled


def auc_mirror(pos, neg):
    vals = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg],
                  key=lambda t: t[0])
    ranks, i = [], 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1][0] == vals[i][0]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        ranks.extend([r] * (j - i + 1))
        i = j + 1
    prs = sum(r for r, (_, p) in zip(ranks, vals) if p == 1)
    return (prs - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def wilson(k, n, z=1.645):
    ph = k / n
    den = 1.0 + z * z / n
    ctr = ph + z * z / (2 * n)
    rad = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (ctr + rad) / den


def leg_expected(cal_s, cal_pr, tst_s, tst_pr, lv_s, lv_pr,
                hot_s=None, hot_pr=None):
    """Independent recomputation of one leg's full readout."""
    muPRc, sdPRc = mstd(cal_pr)
    C_cal = [(muPRc - p) / sdPRc for p in cal_pr]
    F_cal = list(cal_s)
    muC, sdC = mstd(C_cal)
    muF, sdF = mstd(F_cal)
    zc = sorted((v - muC) / sdC for v in C_cal)
    zf = sorted((v - muF) / sdF for v in F_cal)
    thC = quant(zc, 1.0 - ALPHA_SIDE)
    thF = quant(zf, 1.0 - ALPHA_SIDE)
    cal_fire_C = sum(1 for v in zc if v >= thC)
    cal_fire_F = sum(1 for v in zf if v >= thF)
    zC_cal = [(v - muC) / sdC for v in C_cal]
    zF_cal = [(v - muF) / sdF for v in F_cal]
    cal_comb = sum(1 for a, b in zip(zC_cal, zF_cal)
                   if a >= thC or b >= thF)
    C_loop_c = [(muPRc - p) / sdPRc for p in lv_pr]
    F_loop_c = list(lv_s)
    catch_c = sum(1 for a, b in zip(
        [(v - muC) / sdC for v in C_loop_c],
        [(v - muF) / sdF for v in F_loop_c]) if a >= thC or b >= thF)

    ts = list(tst_s) + list(hot_s or [])
    tp = list(tst_pr) + list(hot_pr or [])
    muPRt, sdPRt = mstd(tp)
    C_t = [(muPRt - p) / sdPRt for p in tp]
    F_t = list(ts)
    muCt, sdCt = mstd(C_t)
    muFt, sdFt = mstd(F_t)
    zC_t = [(v - muCt) / sdCt for v in C_t]
    zF_t = [(v - muFt) / sdFt for v in F_t]
    D_neg = [max(a, b) for a, b in zip(zC_t, zF_t)]
    C_loop = [(muPRt - p) / sdPRt for p in lv_pr]
    F_loop = list(lv_s)
    zC_l = [(v - muCt) / sdCt for v in C_loop]
    zF_l = [(v - muFt) / sdFt for v in F_loop]
    D_pos = [max(a, b) for a, b in zip(zC_l, zF_l)]
    gap = sgap(D_pos, D_neg) if D_pos and D_neg else None
    auc = auc_mirror(D_pos, D_neg)
    fires_zC = sum(1 for v in zC_t if v >= thC)
    fires_zF = sum(1 for v in zF_t if v >= thF)
    combined = sum(1 for a, b in zip(zC_t, zF_t)
                   if a >= thC or b >= thF)
    n_neg = len(D_neg)
    rate = combined / n_neg
    over = rate > ALPHA
    wil = wilson(combined, n_neg)
    catches = {"via_zC": sum(1 for v in zC_l if v >= thC),
               "via_zF": sum(1 for v in zF_l if v >= thF),
               "either": sum(1 for a, b in zip(zC_l, zF_l)
                            if a >= thC or b >= thF)}
    raw_gap_C = sgap(C_loop, C_t)
    raw_gap_F = sgap(F_loop, F_t)
    return {
        "mu_C": muC, "sd_C": sdC, "mu_F": muF, "sd_F": sdF,
        "th_C": thC, "th_F": thF,
        "cal_fire_C": cal_fire_C, "cal_fire_F": cal_fire_F,
        "cal_comb": cal_comb, "cal_catch": catch_c,
        "gap": gap, "auc": auc, "n_neg": n_neg,
        "fires_zC": fires_zC, "fires_zF": fires_zF,
        "combined": combined, "rate": rate, "over": over,
        "wilson": wil, "catches": catches,
        "raw_gap_C": raw_gap_C, "raw_gap_F": raw_gap_F,
    }


def leg_expected_split(s_list, pr_list, lv_s, lv_pr,
                       hot_s=None, hot_pr=None):
    """Independent recomputation of one leg's DOC-SPLIT readout
    (ledger item 229): corpus doc_ids are 200+i, so EVEN doc_id =
    even i = the calibration half; ODD = the held-out half. The
    baselines (the one-step fixtures reduce the PR layer baseline to
    the even-half PR list stats, support < 30 -> pooled fallback),
    the mu/sd, and the thresholds draw from the CALIBRATION half
    ONLY; the held-out half (+ any hot docs, which ride ODD doc_ids)
    is scored against them; the fixtures are the positives."""
    n = len(s_list)
    idx_e = [i for i in range(n) if (200 + i) % 2 == 0]
    idx_o = [i for i in range(n) if (200 + i) % 2 == 1]
    gmPR, sdPR = mstd([pr_list[i] for i in idx_e])
    C_all = [(gmPR - p) / sdPR for p in pr_list]
    F_all = list(s_list)
    C_e = [C_all[i] for i in idx_e]
    F_e = [F_all[i] for i in idx_e]
    muC, sdC = mstd(C_e)
    muF, sdF = mstd(F_e)
    zc = sorted((v - muC) / sdC for v in C_e)
    zf = sorted((v - muF) / sdF for v in F_e)
    thC = quant(zc, 1.0 - ALPHA_SIDE)
    thF = quant(zf, 1.0 - ALPHA_SIDE)
    zC_e = [(v - muC) / sdC for v in C_e]
    zF_e = [(v - muF) / sdF for v in F_e]
    cal_fire_C = sum(1 for v in zc if v >= thC)
    cal_fire_F = sum(1 for v in zf if v >= thF)
    cal_comb = sum(1 for a, b in zip(zC_e, zF_e)
                   if a >= thC or b >= thF)
    C_loop = [(gmPR - p) / sdPR for p in lv_pr]
    F_loop = list(lv_s)
    catch_c = sum(1 for a, b in zip(
        [(v - muC) / sdC for v in C_loop],
        [(v - muF) / sdF for v in F_loop]) if a >= thC or b >= thF)
    s_o = [F_all[i] for i in idx_o] + list(hot_s or [])
    pr_o = [pr_list[i] for i in idx_o] + list(hot_pr or [])
    C_o = [(gmPR - p) / sdPR for p in pr_o]
    zC_o = [(v - muC) / sdC for v in C_o]
    zF_o = [(v - muF) / sdF for v in s_o]
    D_neg = [max(a, b) for a, b in zip(zC_o, zF_o)]
    zC_l = [(v - muC) / sdC for v in C_loop]
    zF_l = [(v - muF) / sdF for v in F_loop]
    D_pos = [max(a, b) for a, b in zip(zC_l, zF_l)]
    gap = sgap(D_pos, D_neg) if D_pos and D_neg else None
    auc = auc_mirror(D_pos, D_neg)
    fires_zC = sum(1 for v in zC_o if v >= thC)
    fires_zF = sum(1 for v in zF_o if v >= thF)
    combined = sum(1 for a, b in zip(zC_o, zF_o)
                   if a >= thC or b >= thF)
    n_neg = len(D_neg)
    rate = combined / n_neg
    over = rate > ALPHA
    wil = wilson(combined, n_neg)
    catches = {"via_zC": sum(1 for v in zC_l if v >= thC),
               "via_zF": sum(1 for v in zF_l if v >= thF),
               "either": sum(1 for a, b in zip(zC_l, zF_l)
                            if a >= thC or b >= thF)}
    raw_gap_C = sgap(C_loop, C_o)
    raw_gap_F = sgap(F_loop, s_o)
    return {
        "n_even": len(idx_e), "n_odd": n_neg,
        "mu_C": muC, "sd_C": sdC, "mu_F": muF, "sd_F": sdF,
        "th_C": thC, "th_F": thF,
        "cal_fire_C": cal_fire_C, "cal_fire_F": cal_fire_F,
        "cal_comb": cal_comb, "cal_catch": catch_c,
        "gap": gap, "auc": auc,
        "fires_zC": fires_zC, "fires_zF": fires_zF,
        "combined": combined, "rate": rate, "over": over,
        "wilson": wil, "catches": catches,
        "raw_gap_C": raw_gap_C, "raw_gap_F": raw_gap_F,
    }


# =========================================
# The deterministic fixture builder.
# =========================================
def one_step(s, pr, i):
    return {"t": [0], "id": [100 + i], "E": [2.0 + 0.01 * (i % 7)],
            "rho": [0.5 + 0.01 * (i % 5)], "s": [s], "f": [0.0],
            "layer": [0], "H": [3.0 + 0.02 * (i % 5)], "PR": [pr],
            "a": [0.1], "rsize": [0.5], "dead5": [None],
            "dead4": [None], "dead3": [None], "dead_share": [0.0]}


def const_steps(s, pr, n, j=0):
    cols = {k: [] for k in STEP_KEYS}
    for t in range(n):
        cols["t"].append(t)
        cols["id"].append(7000 + (j * 13 + t) % 500)
        cols["E"].append(1.2 + 0.01 * (t % 5))
        cols["rho"].append(0.05 + 0.005 * (t % 4))
        cols["s"].append(s)
        cols["f"].append(1.0)
        cols["layer"].append(0)
        cols["H"].append(3.0 + 0.5 * (t % 3))
        cols["PR"].append(pr)
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
            "walk_ids": [5] * len(steps["t"]), "steps": steps,
            "commits": [], "hidden_n": 0, "hidden_dim": 0,
            "hidden_b64": ""}


def zero_step_rec(leg, doc_id):
    return rec(leg, doc_id, {k: [] for k in STEP_KEYS}, n_gen_steps=0)


def loop_recs(n_live=8, n_inert=2, counter_steps=None):
    lv_s, lv_pr = live_lists()
    out = []
    for j in range(n_live):
        s, pr = lv_s[j], lv_pr[j]
        n = 64
        if NAMES[j] == "loop-seeded-counter" and counter_steps:
            n = counter_steps
        out.append(rec("loop", NAMES[j], const_steps(s, pr, n, j)))
    for j in range(n_inert):
        out.append(rec("loop", f"inert-{NAMES[(n_live + j) % 10]}",
                       const_steps(INERT_S, INERT_PR, INERT_N, j)))
    return out


def clean_recs(leg, s_list, pr_list, start=200):
    return [rec(leg, start + i, one_step(s_list[i], pr_list[i], i))
            for i in range(len(s_list))]


def calib_cache(leg, premise_ok=True):
    cal_s, cal_pr = cal_lists()
    recs = []
    if leg == "prose17p":
        recs.append(zero_step_rec("prose17p", 91) if premise_ok
                    else rec("prose17p", 91, one_step(0.16, 5.0, 91)))
    if leg == "p2corpus":
        recs.append(zero_step_rec("p2corpus", 3) if premise_ok
                    else rec("p2corpus", 3, one_step(0.11, 5.5, 3)))
    recs += clean_recs(leg, cal_s, cal_pr)
    recs += loop_recs()
    return recs


def test_cache(leg, s_list=None, pr_list=None, hot=0, fixtures=None,
               n_clean=None):
    ts = s_list if s_list is not None else tst_lists()[0]
    tp = pr_list if pr_list is not None else tst_lists()[1]
    if n_clean is not None:
        ts, tp = ts[:n_clean], tp[:n_clean]
    recs = []
    if leg == "prose17p":
        recs.append(zero_step_rec("prose17p", 91))
    if leg == "p2corpus":
        recs.append(zero_step_rec("p2corpus", 3))
    recs += clean_recs(leg, ts, tp)
    for k in range(hot):
        recs.append(rec(leg, 300 + k, one_step(0.5, 5.0, k)))
    recs += (fixtures if fixtures is not None else loop_recs())
    return recs


def write(path, recs, cut_last=False):
    with open(path, "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    if cut_last:
        with open(path, "rb+") as f:
            f.seek(-40, os.SEEK_END)
            f.truncate()


def tuned_intercept(target_gap):
    """Solve the s-intercept A for the tuned clean design
    (s_i = A + 0.001*i, PR_i = 3.5 - 0.062*i) so the leg's ensemble
    gap lands exactly on target_gap (closed form; D_pos = z_F by
    construction, verified at build)."""
    lv_s, lv_pr = live_lists()
    pr = [3.5 - 0.062 * i for i in range(N_CLEAN)]
    muPR, sdPR = mstd(pr)
    zC_l = [(muPR - p) / sdPR for p in lv_pr]
    sd_s = 0.001 * mstd([float(i) for i in range(N_CLEAN)])[1]
    # the clean z's are the standardized arithmetic w_i (A-independent)
    w = [(0.001 * (i - 20.0)) / sd_s for i in range(N_CLEAN)]
    m_neg, sd_neg = mstd(w)
    mu_s_off = 0.001 * 20.0
    zF_l = [(s - mu_s_off) / sd_s for s in lv_s]
    D_pos = [max(a, b) for a, b in zip(zC_l, zF_l)]
    for a, b in zip(zC_l, zF_l):
        assert b >= a, "tuned design violated: z_F must dominate z_C"
    sd_pos = mstd(D_pos)[1]
    pooled = math.sqrt((sd_pos ** 2 + sd_neg ** 2) / 2.0)
    # mean_zF(A) = (mean(lv_s) - A - mu_s_off)/sd_s; the gap target:
    # (mean_zF - m_neg)/pooled = target_gap
    A = (sum(lv_s) / len(lv_s)) - mu_s_off \
        - (target_gap * pooled + m_neg) * sd_s
    return A


def build_fixtures():
    if os.path.isdir(FIXDIR):
        shutil.rmtree(FIXDIR)
    os.makedirs(OUTDIR, exist_ok=True)
    cal_s, cal_pr = cal_lists()
    tst_s, tst_pr = tst_lists()
    lv_s, lv_pr = live_lists()
    exp1 = {leg: leg_expected(cal_s, cal_pr, tst_s, tst_pr, lv_s, lv_pr)
            for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus")}
    with open(os.path.join(FIXDIR, "expected_f1.json"), "w") as f:
        json.dump(exp1, f, indent=1, sort_keys=True)

    # ---- the standard sets (F1) ----
    for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus"):
        write(os.path.join(FIXDIR, f"c_{leg}.jsonl"), calib_cache(leg))
        write(os.path.join(FIXDIR, f"t_{leg}.jsonl"), test_cache(leg))
    # ---- F2: hot clean docs on the gsm test leg ----
    write(os.path.join(FIXDIR, "t2_gsm_hot.jsonl"),
          test_cache("gsm8k", hot=5))
    # ---- F3a: 4-clean-doc gsm test leg (standard fixtures) ----
    write(os.path.join(FIXDIR, "t3a_gsm_small.jsonl"),
          test_cache("gsm8k", n_clean=4))
    # ---- F3b: the thin fixture set (3 live / 7 inert) on ALL FOUR
    # test caches (the within-set byte-identity law requires one
    # consistent fixture set per set) ----
    thin = loop_recs(n_live=3, n_inert=7)
    for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus"):
        write(os.path.join(FIXDIR, f"t3b_{leg}.jsonl"),
              test_cache(leg, fixtures=thin))
    # ---- F5a: census premise violated on the CALIB p2 cache ----
    write(os.path.join(FIXDIR, "c5a_p2_premise.jsonl"),
          calib_cache("p2corpus", premise_ok=False))
    # ---- F5b: out-of-census absent statistic (s=[None]) on the
    # gsm TEST leg ----
    r5b = test_cache("gsm8k")
    bad = {"t": [0], "id": [999], "E": [2.0], "rho": [0.5],
           "s": [None], "f": [0.0], "layer": [0], "H": [3.0],
           "PR": [5.0], "a": [0.1], "rsize": [0.5], "dead5": [None],
           "dead4": [None], "dead3": [None], "dead_share": [0.0]}
    r5b.append(rec("gsm8k", 190, bad))
    write(os.path.join(FIXDIR, "t5b_gsm_absent.jsonl"), r5b)
    # ---- F5c: key mismatch on the gsm TEST leg ----
    r5c = test_cache("gsm8k")
    r5c[5]["key"] = "gsm8k:999"
    write(os.path.join(FIXDIR, "t5c_gsm_key.jsonl"), r5c)
    # ---- F5d: truncated final JSON line ----
    write(os.path.join(FIXDIR, "t5d_gsm_trunc.jsonl"), test_cache("gsm8k"),
          cut_last=True)
    # ---- F5e: unrecognized leg on the TEST side ----
    r5e = test_cache("gsm8k")
    r5e.append(rec("zeta", 1, one_step(0.15, 5.8, 1)))
    write(os.path.join(FIXDIR, "t5e_zeta.jsonl"), r5e)
    # ---- F5f: duplicate leg across CALIB caches ----
    write(os.path.join(FIXDIR, "c5f_gsm_dup.jsonl"),
          clean_recs("gsm8k", cal_lists()[0][:6], cal_lists()[1][:6],
                     start=400))
    # ---- F5g: within-set fixture copy divergence on the CALIB side
    # (loop-seeded-counter at 63 steps in the he cache) ----
    r5g = calib_cache("humaneval")
    r5g = [r for r in r5g if r["doc_id"] != "loop-seeded-counter"]
    r5g.append(rec("loop", "loop-seeded-counter",
                   const_steps(live_lists()[0][3], live_lists()[1][3],
                               63, 3)))
    write(os.path.join(FIXDIR, "c5g_he_div.jsonl"), r5g)
    # ---- F6: cross-set divergence REPORTED -- ALL FOUR test caches
    # carry loop-seeded-counter at 63 steps (byte-identical within
    # the test set; divergent vs the 64-step calib copies) ----
    f6 = loop_recs(counter_steps=63)
    for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus"):
        write(os.path.join(FIXDIR, f"t6_{leg}.jsonl"),
              test_cache(leg, fixtures=f6))
    # ---- F8: the tuned legs (gap 2.01 on gsm8k, gap 1.99 on
    # humaneval; the tuning lives in the LEG'S clean population, the
    # fixture set stays the standard byte-identical one) ----
    a_gsm = tuned_intercept(2.01)
    a_he = tuned_intercept(1.99)
    ts = [a_gsm + 0.001 * i for i in range(N_CLEAN)]
    write(os.path.join(FIXDIR, "t8_gsm_tuned.jsonl"),
          test_cache("gsm8k", s_list=ts,
                     pr_list=[3.5 - 0.062 * i
                              for i in range(N_CLEAN)]))
    ts = [a_he + 0.001 * i for i in range(N_CLEAN)]
    write(os.path.join(FIXDIR, "t8_he_tuned.jsonl"),
          test_cache("humaneval", s_list=ts,
                     pr_list=[3.5 - 0.062 * i
                              for i in range(N_CLEAN)]))
    # ---- DOC-SPLIT AMENDMENT FIXTURES (ledger item 229) ----
    # F10: hot clean docs on the ODD (held-out) half of the gsm
    # walks cache (doc ids 301..309 odd -> held-out; the hot docs
    # never touch the calibration half or its baselines)
    r10 = calib_cache("gsm8k")
    for k in range(5):
        r10.append(rec("gsm8k", 301 + 2 * k,
                       one_step(0.5, 5.0, k)))
    write(os.path.join(FIXDIR, "s10_gsm_hotodd.jsonl"), r10)
    # F11: the per-half population guard -- a 2-doc EVEN calibration
    # half (200, 202) + a 6-doc ODD held-out half (201..211 odd)
    # centered EXACTLY on the calibration half's means (z = 0 on
    # both sides -- zero held-out fires, so the per-half guard
    # typing lands untrampled by the inherited falsifier override,
    # the item-222 semantics); the standard 10 fixtures ride as
    # positives
    ids11 = [200, 202, 201, 203, 205, 207, 209, 211]
    vals11 = [(0.100, 6.00), (0.104, 5.90), (0.102, 5.95),
              (0.102, 5.95), (0.102, 5.95), (0.102, 5.95),
              (0.102, 5.95), (0.102, 5.95)]
    r11 = [rec("gsm8k", did, one_step(vals11[k][0], vals11[k][1], k))
           for k, did in enumerate(ids11)]
    r11 += loop_recs()
    write(os.path.join(FIXDIR, "s11_gsm_halves.jsonl"), r11)
    # F12: a non-int corpus doc_id ('s-401') in split mode -> the
    # parity split's hard exit
    r12 = calib_cache("gsm8k")
    r12.append(rec("gsm8k", "s-401", one_step(0.12, 5.9, 1)))
    write(os.path.join(FIXDIR, "s12_gsm_strid.jsonl"), r12)
    return exp1, {"a_gsm": a_gsm, "a_he": a_he}


def run_tool(calib, test, out_name, fixture_mode=True):
    cmd = [sys.executable, TOOL]
    for cx in calib:
        cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
    for tx in test:
        cmd += ["--test-cache", os.path.join(FIXDIR, tx)]
    cmd += ["--tag", out_name,
            "--out", os.path.join(OUTDIR, out_name + ".json")]
    if fixture_mode:
        cmd.append("--fixture-mode")
    return subprocess.run(cmd, capture_output=True, text=True)


def run_tool_split(calib, out_name, fixture_mode=True):
    cmd = [sys.executable, TOOL, "--doc-split"]
    for cx in calib:
        cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
    cmd += ["--tag", out_name,
            "--out", os.path.join(OUTDIR, out_name + ".json")]
    if fixture_mode:
        cmd.append("--fixture-mode")
    return subprocess.run(cmd, capture_output=True, text=True)


def load_out(name):
    with open(os.path.join(OUTDIR, name + ".json")) as f:
        return json.load(f)


def expect(cond, label, results, detail=""):
    results.append((bool(cond), label, detail))
    print(("  PASS " if cond else "  FAIL ") + label
          + (f"  [{detail}]" if detail and not cond else ""))


def near(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol


CAL_FILES = ["c_gsm8k.jsonl", "c_humaneval.jsonl",
             "c_prose17p.jsonl", "c_p2corpus.jsonl"]
TST_FILES = ["t_gsm8k.jsonl", "t_humaneval.jsonl",
             "t_prose17p.jsonl", "t_p2corpus.jsonl"]
LEGS = ("gsm8k", "humaneval", "prose17p", "p2corpus")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_leg(o, leg, exp, results, tag, want_typing="PASS_2SIGMA"):
    e = exp[leg]
    cal = o["legs"][leg]["calibration"]
    tst = o["legs"][leg]["test"]
    n_census = 1 if leg in ("prose17p", "p2corpus") else 0
    expect(cal["n_clean"] == 41,
           f"{tag} [{leg}] calibration census-clean population 41",
           results, str(cal["n_clean"]))
    expect(near(cal["mu_C"], e["mu_C"]) and near(cal["sd_C"], e["sd_C"])
           and near(cal["mu_F"], e["mu_F"]) and near(cal["sd_F"], e["sd_F"]),
           f"{tag} [{leg}] calibration mu/sd EXACT (independent "
           f"recomputation)", results,
           f"got C {cal['mu_C']:.6f}/{cal['sd_C']:.6f} "
           f"F {cal['mu_F']:.6f}/{cal['sd_F']:.6f}")
    expect(near(cal["thresholds"]["z_C"], e["th_C"])
           and near(cal["thresholds"]["z_F"], e["th_F"]),
           f"{tag} [{leg}] thresholds = the pinned 0.975 z-quantiles "
           f"(independent recomputation)", results,
           f"got {cal['thresholds']} want {e['th_C']}, {e['th_F']}")
    expect(cal["in_sample_clean_fires"]["z_C"] == e["cal_fire_C"]
           and cal["in_sample_clean_fires"]["z_F"] == e["cal_fire_F"]
           and cal["in_sample_clean_fires"]["combined"] == e["cal_comb"]
           and near(cal["in_sample_clean_fires"]["combined_rate"],
                    round(e["cal_comb"] / 41, 6), 1e-12),
           f"{tag} [{leg}] in-sample fire accounting EXACT", results,
           json.dumps(cal["in_sample_clean_fires"]))
    expect(cal["in_sample_loop_catch"]["either"] == e["cal_catch"],
           f"{tag} [{leg}] in-sample loop catch EXACT", results,
           json.dumps(cal["in_sample_loop_catch"]))
    expect(cal["n_live"] == 8 and cal["n_inert"] == 2,
           f"{tag} [{leg}] calibration positives 8 live / 2 inert",
           results)
    expect(tst["n_corpus_all"] == 41 + n_census
           and tst["n_census_excluded"] == n_census
           and tst["n_clean"] == 41,
           f"{tag} [{leg}] test populations "
           f"({41 + n_census} corpus / {n_census} census / 41 clean)",
           results,
           f"{tst['n_corpus_all']}/{tst['n_census_excluded']}"
           f"/{tst['n_clean']}")
    lp = tst["loop_population"]
    own = {l: f"t_{l}.jsonl" if tag.startswith("F1") else f"t6_{l}.jsonl"
           for l in LEGS}[leg]
    expect(lp["n_live"] == 8 and lp["n_inert"] == 2
           and lp["source_cache"] == own,
           f"{tag} [{leg}] positives from the leg's OWN cache "
           f"(8 live / 2 inert)", results, json.dumps(lp))
    ens = tst["ensemble"]
    expect(near(ens["sigma_gap"], round(e["gap"], 3), 1e-9)
           if e["gap"] is not None else ens["sigma_gap"] is None,
           f"{tag} [{leg}] ensemble D sigma-gap EXACT (independent "
           f"recomputation)", results,
           f"got {ens['sigma_gap']} want {round(e['gap'], 3)}")
    expect(near(ens["auc"], round(e["auc"], 4), 1e-9),
           f"{tag} [{leg}] ensemble AUC EXACT", results,
           f"got {ens['auc']} want {round(e['auc'], 4)}")
    expect(ens["verdict_presented"] == want_typing,
           f"{tag} [{leg}] verdict typing {want_typing}", results,
           ens["verdict_presented"])
    sc = tst["sides_context_raw"]
    expect(near(sc["maxPRsig_gap"], round(e["raw_gap_C"], 3), 1e-9)
           and near(sc["minS_gap"], round(e["raw_gap_F"], 3), 1e-9),
           f"{tag} [{leg}] raw side gaps (context) EXACT", results,
           json.dumps(sc))
    fa = tst["fire_accounting"]
    expect(fa["combined_fires"] == e["combined"]
           and fa["fires_z_C"] == e["fires_zC"]
           and fa["fires_z_F"] == e["fires_zF"]
           and near(fa["combined_rate"], round(e["rate"], 6), 1e-12)
           and fa["over_budget"] == e["over"]
           and fa["budget_count_ceil"] == math.ceil(ALPHA * e["n_neg"])
           and near(fa["wilson_upper_95"], round(e["wilson"], 6), 1e-12),
           f"{tag} [{leg}] fire accounting EXACT (count-based honesty "
           f"+ Wilson upper)", results, json.dumps(fa))
    expect(tst["loop_catches"] == e["catches"],
           f"{tag} [{leg}] loop catches @ thresholds EXACT", results,
           json.dumps(tst["loop_catches"]))
    fo = tst["forensics"]
    expect(fo["how"]["loop_docs"] == 8 and fo["where"]["leg"] == leg
           and len(fo["what_next"]) >= 3 and isinstance(fo["why"], str)
           and len(fo["why"]) > 10,
           f"{tag} [{leg}] the item-220 forensics block rides the "
           f"leg (HOW/WHERE/WHY/WHAT-NEXT)", results,
           json.dumps(fo)[:200])


def check_leg_split(o, leg, exp, results, tag,
                    want_typing="PASS_2SIGMA", own_cache=None):
    """The F9/F10 checks: every doc-split quantity EXACT vs the
    independent recomputation (calibration-half-only baselines,
    mu/sd, thresholds; held-out-half-only fires/gap/AUC)."""
    e = exp[leg]
    ds = o["legs"][leg]["doc_split"]
    cal = o["legs"][leg]["calibration"]
    tst = o["legs"][leg]["test"]
    n_census = 1 if leg in ("prose17p", "p2corpus") else 0
    expect(ds["n_even_calib"] == e["n_even"]
           and ds["n_odd_held_out"] == e["n_odd"],
           f"{tag} [{leg}] the parity split: {e['n_even']} even "
           f"(calibration) / {e['n_odd']} odd (held-out)",
           results,
           f"{ds['n_even_calib']}/{ds['n_odd_held_out']}")
    expect("ledger item 229" in ds["rule"]
           and "EVEN doc_id = calibration half" in ds["rule"]
           and "candidate-selection caveat" in ds["caveat"],
           f"{tag} [{leg}] the doc_split block carries the item-229 "
           f"rule + the pinned caveat", results)
    expect(cal["half"] == "even doc_id" and tst["half"] == "odd doc_id"
           and cal["n_clean"] == e["n_even"]
           and tst["n_clean"] == e["n_odd"],
           f"{tag} [{leg}] the halves labeled + populations "
           f"({e['n_even']} calib / {e['n_odd']} held-out)", results,
           f"{cal['half']}/{tst['half']} {cal['n_clean']}/"
           f"{tst['n_clean']}")
    expect(near(cal["mu_C"], e["mu_C"]) and near(cal["sd_C"], e["sd_C"])
           and near(cal["mu_F"], e["mu_F"]) and near(cal["sd_F"], e["sd_F"]),
           f"{tag} [{leg}] CALIBRATION-HALF mu/sd EXACT (independent "
           f"recomputation; held-out docs never touch a baseline)",
           results,
           f"got C {cal['mu_C']:.6f}/{cal['sd_C']:.6f} "
           f"F {cal['mu_F']:.6f}/{cal['sd_F']:.6f}")
    expect(near(cal["thresholds"]["z_C"], e["th_C"])
           and near(cal["thresholds"]["z_F"], e["th_F"]),
           f"{tag} [{leg}] thresholds = the calibration half's "
           f"0.975 z-quantiles EXACT", results,
           f"got {cal['thresholds']} want {e['th_C']}, {e['th_F']}")
    expect(cal["in_sample_clean_fires"]["z_C"] == e["cal_fire_C"]
           and cal["in_sample_clean_fires"]["z_F"] == e["cal_fire_F"]
           and cal["in_sample_clean_fires"]["combined"] == e["cal_comb"]
           and near(cal["in_sample_clean_fires"]["combined_rate"],
                    round(e["cal_comb"] / e["n_even"], 6), 1e-12),
           f"{tag} [{leg}] in-sample (calibration-half) fire "
           f"accounting EXACT", results,
           json.dumps(cal["in_sample_clean_fires"]))
    expect(cal["in_sample_loop_catch"]["either"] == e["cal_catch"]
           and cal["n_live"] == 8 and cal["n_inert"] == 2,
           f"{tag} [{leg}] in-sample loop catch EXACT + 8 live / "
           f"2 inert positives", results,
           json.dumps(cal["in_sample_loop_catch"]))
    expect(tst["n_corpus_all"] == 41 + n_census
           and tst["n_census_excluded"] == n_census,
           f"{tag} [{leg}] census receipt "
           f"({41 + n_census} corpus / {n_census} excluded)",
           results,
           f"{tst['n_corpus_all']}/{tst['n_census_excluded']}")
    lp = tst["loop_population"]
    expect(lp["n_live"] == 8 and lp["n_inert"] == 2
           and lp["source_cache"] == (own_cache or f"c_{leg}.jsonl"),
           f"{tag} [{leg}] positives from the leg's OWN cache "
           f"(8 live / 2 inert, never in calibration)", results,
           json.dumps(lp))
    ens = tst["ensemble"]
    expect(near(ens["sigma_gap"], round(e["gap"], 3), 1e-9)
           if e["gap"] is not None else ens["sigma_gap"] is None,
           f"{tag} [{leg}] ensemble D sigma-gap EXACT on the held-out "
           f"half (independent recomputation)", results,
           f"got {ens['sigma_gap']} want {round(e['gap'], 3)}")
    expect(near(ens["auc"], round(e["auc"], 4), 1e-9),
           f"{tag} [{leg}] ensemble AUC EXACT", results,
           f"got {ens['auc']} want {round(e['auc'], 4)}")
    expect(ens["verdict_presented"] == want_typing,
           f"{tag} [{leg}] verdict typing {want_typing}", results,
           ens["verdict_presented"])
    sc = tst["sides_context_raw"]
    expect(near(sc["maxPRsig_gap"], round(e["raw_gap_C"], 3), 1e-9)
           and near(sc["minS_gap"], round(e["raw_gap_F"], 3), 1e-9),
           f"{tag} [{leg}] raw side gaps on the held-out half "
           f"(context) EXACT", results, json.dumps(sc))
    fa = tst["fire_accounting"]
    expect(fa["combined_fires"] == e["combined"]
           and fa["fires_z_C"] == e["fires_zC"]
           and fa["fires_z_F"] == e["fires_zF"]
           and near(fa["combined_rate"], round(e["rate"], 6), 1e-12)
           and fa["over_budget"] == e["over"]
           and fa["budget_count_ceil"] == math.ceil(ALPHA * e["n_odd"])
           and near(fa["wilson_upper_95"], round(e["wilson"], 6), 1e-12),
           f"{tag} [{leg}] held-out fire accounting EXACT "
           f"(count-based honesty + Wilson upper)", results,
           json.dumps(fa))
    expect(tst["loop_catches"] == e["catches"],
           f"{tag} [{leg}] loop catches @ thresholds EXACT", results,
           json.dumps(tst["loop_catches"]))
    fo = tst["forensics"]
    expect(fo["how"]["loop_docs"] == 8 and fo["where"]["leg"] == leg
           and len(fo["what_next"]) >= 3 and isinstance(fo["why"], str)
           and len(fo["why"]) > 10,
           f"{tag} [{leg}] the item-220 forensics block rides the "
           f"leg (HOW/WHERE/WHY/WHAT-NEXT)", results,
           json.dumps(fo)[:200])


def main():
    print("=" * 78)
    print("=== RW-16 ENSEMBLE READOUT TOOL ACCEPTANCE RUN (zero-GPU; "
          "the sec. 5 pre-registered acceptance) ===")
    exp1, tuned = build_fixtures()
    print(f"  fixtures built deterministically under {FIXDIR}")
    results = []

    # ---- F1: the clean four-leg run ----
    print("\n--- F1: clean four-leg run; hand-checked z/threshold/D "
          "math ---")
    p1 = run_tool(CAL_FILES, TST_FILES, "f1")
    expect(p1.returncode == 0, "F1 exit 0", results,
           f"rc={p1.returncode} {p1.stdout[-400:]}")
    o1 = load_out("f1")
    expect("=== RW-16 DUAL-SIDED ENSEMBLE ADJUDICATION READOUT"
           in p1.stdout, "F1 banner prints", results)
    expect("FIXTURE-MODE: PIN CHECKS ECHOED, NOT ENFORCED"
           in p1.stdout, "F1 fixture-mode banner prints", results)
    expect(o1["census_line"].count("prose17p:") == 2
           and o1["census_line"].count("p2corpus:") == 33
           and "prose17p:91 prose17p:108 p2corpus:3" in o1["census_line"],
           "F1 census line: the item-213 35-doc class (2 + 33)",
           results, o1["census_line"][:120])
    expect(o1["fixture_mode"] is True
           and o1["tool_sha256"] == sha256_file(TOOL),
           "F1 export carries the tool's own SHA-256 + fixture_mode",
           results)
    expect(o1["alpha"]["coarse_guard"] == 0.05
           and o1["alpha"]["per_side"] == 0.025,
           "F1 the R16-D2 two-stage alpha pins (5% coarse / 2.5% "
           "per side)", results, json.dumps(o1["alpha"]))
    expect("theta [REDACTED_PER_PUBLICATION_POLICY] unmoved" in o1["theta_note"]
           and "ROUTED-TO-OWN-PRE-REG" in o1["rw14_rider"],
           "F1 theta note + the RW-14 rider typed", results)
    nrec = {"c_gsm8k.jsonl": 51, "c_humaneval.jsonl": 51,
            "c_prose17p.jsonl": 52, "c_p2corpus.jsonl": 52}
    ok_n, ok_pin = True, 0
    for ent in o1["inputs"]["calibration"]:
        ok_n &= (ent["n_records"] == nrec[ent["path"]]
                 and ent["sha256"] == sha256_file(
                     os.path.join(FIXDIR, ent["path"])))
        if ent["pin"] is not None:
            ok_pin += 1
            ok_n &= ent["pin"]["match"] is False
    expect(ok_n and ok_pin == 2,
           "F1 calibration inputs receipt (record counts + SHAs + the "
           "fixture-mode pin echo on the two prose legs)", results,
           json.dumps(o1["inputs"]["calibration"]))
    fir = o1["fixture_identity_receipt"]
    expect(fir["calibration"]["n_loop_fixtures"] == 10
           and fir["calibration"]["copies_byte_identical"] is True
           and fir["test"]["n_loop_fixtures"] == 10
           and fir["test"]["copies_byte_identical"] is True,
           "F1 within-set fixture identity receipts (10 fixtures, "
           "byte-identical, both sets)", results, json.dumps(fir))
    expect(fir["cross_set_reported"]["n_compared"] == 10
           and fir["cross_set_reported"]["n_identical"] == 10
           and fir["cross_set_reported"]["divergent_fixtures"] == [],
           "F1 cross-set report: 10/10 byte-identical "
           "calibration-vs-test", results,
           json.dumps(fir["cross_set_reported"]))
    expect("cross-set fixture report: 10/10 fixtures byte-identical"
           in p1.stdout, "F1 cross-set console line prints", results)
    for leg in LEGS:
        check_leg(o1, leg, exp1, results, "F1")
    leg17 = o1["legs"]["prose17p"]
    cd17 = {c["doc_id"]: c
            for c in leg17["calibration"]["census_docs"]}
    td17 = {c["doc_id"]: c for c in leg17["test"]["census_docs"]}
    expect(len(cd17) == 2 and cd17[91]["present"] is True
           and cd17[91]["premise"].startswith("verified")
           and cd17[108]["present"] is False
           and td17[91]["present"] is True,
           "F1 prose17p census: doc 91 verified present, doc 108 "
           "reported not-present-in-cache", results,
           json.dumps(leg17["calibration"]["census_docs"]))
    legp2 = o1["legs"]["p2corpus"]
    cdp2 = {c["doc_id"]: c
            for c in legp2["calibration"]["census_docs"]}
    expect(len(cdp2) == 33
           and cdp2[3]["present"] is True
           and cdp2[3]["premise"].startswith("verified")
           and sum(1 for c in cdp2.values() if c["present"]) == 1
           and sum(1 for c in cdp2.values() if not c["present"]) == 32,
           "F1 p2corpus census: 33 named, doc 3 verified premise, "
           "32 not-present", results,
           json.dumps(legp2["calibration"]["census_docs"][:2]))
    ens = {leg: o1["legs"][leg]["test"]["ensemble"]["sigma_gap"]
           for leg in LEGS}
    expect(all(v is not None and v >= 2.0 for v in ens.values()),
           "F1 all four legs clear the held-out 2-sigma bar on D "
           "(by construction)", results, json.dumps(ens))
    aucs = {leg: o1["legs"][leg]["test"]["ensemble"]["auc"] for leg in LEGS}
    expect(all(v == 1.0 for v in aucs.values()),
           "F1 AUC exactly 1.0 on all four legs (non-overlap by "
           "construction)", results, json.dumps(aucs))
    pcv = o1["presented_candidate_verdict"]
    expect(pcv["verdict_presented"] == "PASS_2SIGMA-ALL-FOUR-LEGS"
           and pcv["near_bar_legs"] == [] and pcv["failed_legs"] == []
           and pcv["jitter_legs"] == [],
           "F1 presented candidate verdict PASS_2SIGMA-ALL-FOUR-LEGS",
           results, json.dumps(pcv))
    expect("PASS_2SIGMA-ALL-FOUR-LEGS" in p1.stdout
           and "CALIBRATION [gsm8k]" in p1.stdout
           and "TEST [gsm8k]" in p1.stdout,
           "F1 console: the calibration/test blocks + presented "
           "verdict print", results)

    # ---- F7: determinism ----
    print("\n--- F7: determinism (fresh re-run byte-identical) ---")
    p1b = run_tool(CAL_FILES, TST_FILES, "f1b")
    with open(os.path.join(OUTDIR, "f1.json"), "rb") as fa, \
            open(os.path.join(OUTDIR, "f1b.json"), "rb") as fb:
        expect(fa.read() == fb.read() and p1b.returncode == 0,
               "F7 fresh re-run export byte-identical", results)

    # ---- F2: the fire-rate falsifier ----
    print("\n--- F2: fire-rate falsifier -> CANDIDATE-KILLED ---")
    cal_s, cal_pr = cal_lists()
    tst_s, tst_pr = tst_lists()
    lv_s, lv_pr = live_lists()
    exp2 = dict(exp1)
    exp2["gsm8k"] = leg_expected(cal_s, cal_pr, tst_s, tst_pr, lv_s,
                                 lv_pr, hot_s=[0.5] * 5,
                                 hot_pr=[5.0] * 5)
    p2r = run_tool(CAL_FILES,
                   ["t2_gsm_hot.jsonl"] + TST_FILES[1:], "f2")
    expect(p2r.returncode == 0, "F2 exit 0", results,
           f"rc={p2r.returncode} {p2r.stdout[-300:]}")
    o2 = load_out("f2")
    e2 = exp2["gsm8k"]
    o2g = o2["legs"]["gsm8k"]["test"]
    expect(o2g["n_clean"] == 46,
           "F2 the hot leg's clean population 46 (41 + 5 hot)",
           results, str(o2g["n_clean"]))
    expect(o2g["fire_accounting"]["combined_fires"] == e2["combined"]
           and o2g["fire_accounting"]["over_budget"] is True
           and round(e2["rate"], 4) > ALPHA,
           "F2 the hot leg fires over the 5% coarse guard (EXACT "
           "count)", results,
           f"{o2g['fire_accounting']['combined_fires']} fires, "
           f"rate {o2g['fire_accounting']['combined_rate']}")
    expect(o2g["ensemble"]["verdict_presented"]
           == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
           and "coarse guard falsifier" in o2g["ensemble"]["verdict_basis"],
           "F2 the leg typed CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
           results, o2g["ensemble"]["verdict_presented"])
    expect(o2g["ensemble"]["sigma_gap"] is not None
           and o2g["ensemble"]["sigma_gap"] >= 2.0
           and near(o2g["ensemble"]["sigma_gap"],
                   round(e2["gap"], 3), 1e-9),
           "F2 the sigma-gap STILL passes (killed even so -- the "
           "R16-D2 falsifier's teeth)", results,
           f"gap {o2g['ensemble']['sigma_gap']}")
    expect(o2["presented_candidate_verdict"]["verdict_presented"]
           == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
           "F2 the candidate-level verdict KILLED", results,
           json.dumps(o2["presented_candidate_verdict"]))
    for leg in ("humaneval", "prose17p", "p2corpus"):
        expect(o2["legs"][leg]["test"]["ensemble"]["verdict_presented"]
               == "PASS_2SIGMA",
               f"F2 [{leg}] unaffected legs still PASS", results)

    # ---- F3a: negative-population guard ----
    print("\n--- F3a: negative-population guard (4 clean docs) ---")
    exp3a = dict(exp1)
    exp3a["gsm8k"] = leg_expected(cal_s, cal_pr, tst_s[:4], tst_pr[:4],
                                  lv_s, lv_pr)
    p3a = run_tool(CAL_FILES,
                   ["t3a_gsm_small.jsonl"] + TST_FILES[1:], "f3a")
    o3a = load_out("f3a")
    expect(p3a.returncode == 0, "F3a exit 0 (typed, not crashed)",
           results, f"rc={p3a.returncode}")
    g3a = o3a["legs"]["gsm8k"]["test"]
    expect(g3a["n_clean"] == 4
           and g3a["ensemble"]["verdict_presented"]
           == "INCONCLUSIVE-POPULATION-GUARD"
           and "population guard" in g3a["ensemble"]["verdict_basis"],
           "F3a the 4-clean-doc leg typed INCONCLUSIVE-POPULATION-GUARD",
           results, json.dumps(g3a["ensemble"]))
    expect(o3a["presented_candidate_verdict"]["verdict_presented"]
           == "INCONCLUSIVE-POPULATION-GUARD",
           "F3a candidate-level INCONCLUSIVE-POPULATION-GUARD",
           results)
    expect(o3a["legs"]["humaneval"]["test"]["ensemble"]
           ["verdict_presented"] == "PASS_2SIGMA",
           "F3a the other legs still compute + PASS", results)

    # ---- F3b: positive-population guard ----
    print("\n--- F3b: positive-population guard (3 live / 7 inert) ---")
    p3b = run_tool(CAL_FILES,
                   [f"t3b_{leg}.jsonl" for leg in LEGS], "f3b")
    o3b = load_out("f3b")
    expect(p3b.returncode == 0, "F3b exit 0", results,
           f"rc={p3b.returncode}")
    ok = True
    for leg in LEGS:
        lp = o3b["legs"][leg]["test"]["loop_population"]
        ok &= (lp["n_live"] == 3 and lp["n_inert"] == 7
               and len(lp["inert"]) == 7)
        ok &= (o3b["legs"][leg]["test"]["ensemble"]
               ["verdict_presented"] == "INCONCLUSIVE-POPULATION-GUARD")
    expect(ok, "F3b all four legs: 3 live / 7 inert census + "
           "INCONCLUSIVE-POPULATION-GUARD typing", results,
           json.dumps(o3b["legs"]["gsm8k"]["test"]["loop_population"]))
    expect(o3b["presented_candidate_verdict"]["verdict_presented"]
           == "INCONCLUSIVE-POPULATION-GUARD",
           "F3b candidate-level INCONCLUSIVE-POPULATION-GUARD",
           results)

    # ---- F4: unit checks via import ----
    print("\n--- F4: unit checks via import (the pinned typings + "
          "helpers + constants) ---")
    spec = importlib.util.spec_from_file_location("rw16tool", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    expect(mod.ALPHA_COARSE_GUARD == 0.05 and mod.ALPHA_PER_SIDE == 0.025
           and mod.JITTER_BAND == 0.02 and mod.POP_GUARD_MIN == 5
           and mod.LOOP_INERT_MIN_STEPS == 32
           and mod.SIDE_KEYS == ("maxPRsig", "minS"),
           "F4 the pinned constants (R16-D2 two-stage alpha; the "
           "inherited guards)", results)
    p2ids = [c["doc_id"] for c in mod.CENSUS["p2corpus"]]
    expect([c["doc_id"] for c in mod.CENSUS["prose17p"]] == [91, 108]
           and len(p2ids) == 33 and p2ids[0] == 3 and p2ids[-1] == 165
           and 63 in p2ids and 165 in p2ids,
           "F4 the 35-doc census dict verbatim (p2corpus:3 first)",
           results, str(p2ids[:4]))
    t_jit, _ = mod.verdict_typing(1.99, 8, 41)
    t_nb, why_nb = mod.verdict_typing(2.005, 8, 41)
    t_cl, why_cl = mod.verdict_typing(2.03, 8, 41)
    expect(t_jit == "INCONCLUSIVE-FROM-JITTER"
           and mod.verdict_typing(1.97, 8, 41)[0] == "FAIL",
           "F4 jitter-band typings: 1.99 INCONCLUSIVE-FROM-JITTER / "
           "1.97 FAIL", results, t_jit)
    expect(t_nb == "PASS_2SIGMA" and "NEAR-BAR" in why_nb
           and t_cl == "PASS_2SIGMA" and "NEAR-BAR" not in why_cl,
           "F4 the above-bar near-bar flag: 2.005 flagged / 2.03 not",
           results, why_nb)
    expect(mod.verdict_typing(2.5, 4, 41)[0] == "INCONCLUSIVE-POPULATION-GUARD"
           and mod.verdict_typing(2.5, 8, 4)[0]
           == "INCONCLUSIVE-POPULATION-GUARD"
           and mod.verdict_typing(None, 8, 41)[0]
           == "INCONCLUSIVE-EMPTY-POPULATION",
           "F4 the population guards + the empty-population typing",
           results)
    expect(near(mod._quantile([0, 1, 2, 3], 0.975), 2.925, 1e-12)
           and mod._quantile([7.0], 0.975) == 7.0
           and mod._quantile([1, 2], 1.0) == 2.0
           and mod._quantile([1, 2], 0.0) == 1.0,
           "F4 the pinned _quantile (linear interpolation, hand "
           "values)", results)
    expect(near(mod.sigma_gap([10.0, 11.0], [1.0, 2.0]),
                12.727922061357855, 1e-9),
           "F4 sigma_gap hand value (9/sqrt(0.5))", results)
    w0 = mod.wilson_upper(0, 40)
    w2 = mod.wilson_upper(2, 41)
    expect(near(w0, wilson(0, 40), 1e-12)
           and near(w2, wilson(2, 41), 1e-12),
           "F4 the one-sided 95% Wilson upper bound (independent "
           "formula)", results, f"{w0} {w2}")

    # ---- F5: the inherited hard exits ----
    print("\n--- F5: the inherited hard exits (fail-loud) ---")
    p5a = run_tool(["c_gsm8k.jsonl", "c_humaneval.jsonl",
                    "c_prose17p.jsonl", "c5a_p2_premise.jsonl"],
                   TST_FILES, "f5a")
    expect(p5a.returncode == 1
           and "CENSUS PREMISE VIOLATED" in p5a.stdout + p5a.stderr
           and "doc 3" in p5a.stdout + p5a.stderr,
           "F5a census premise violated -> HARD EXIT naming doc 3",
           results, f"rc={p5a.returncode}")
    p5b = run_tool(CAL_FILES,
                   ["t5b_gsm_absent.jsonl"] + TST_FILES[1:], "f5b")
    expect(p5b.returncode == 1
           and "absent statistic" in p5b.stdout + p5b.stderr
           and "190" in p5b.stdout + p5b.stderr
           and "minS" in p5b.stdout + p5b.stderr,
           "F5b out-of-census absent minS -> HARD EXIT naming doc 190",
           results, f"rc={p5b.returncode}")
    p5c = run_tool(CAL_FILES,
                   ["t5c_gsm_key.jsonl"] + TST_FILES[1:], "f5c")
    expect(p5c.returncode == 1
           and "leg:doc_id" in p5c.stdout + p5c.stderr,
           "F5c key != leg:doc_id -> HARD EXIT", results,
           f"rc={p5c.returncode}")
    p5d = run_tool(CAL_FILES,
                   ["t5d_gsm_trunc.jsonl"] + TST_FILES[1:], "f5d")
    expect(p5d.returncode == 1
           and "truncated" in p5d.stdout + p5d.stderr,
           "F5d truncated JSON record -> HARD EXIT", results,
           f"rc={p5d.returncode}")
    p5e = run_tool(CAL_FILES,
                   ["t5e_zeta.jsonl"] + TST_FILES[1:], "f5e")
    expect(p5e.returncode == 1
           and "unrecognized leg" in p5e.stdout + p5e.stderr,
           "F5e unrecognized leg -> HARD EXIT", results,
           f"rc={p5e.returncode}")
    p5f = run_tool(CAL_FILES + ["c5f_gsm_dup.jsonl"], TST_FILES, "f5f")
    expect(p5f.returncode == 1
           and "MORE THAN ONE cache" in p5f.stdout + p5f.stderr,
           "F5f duplicate leg across calib caches -> HARD EXIT",
           results, f"rc={p5f.returncode}")
    p5g = run_tool(["c_gsm8k.jsonl", "c5g_he_div.jsonl",
                    "c_prose17p.jsonl", "c_p2corpus.jsonl"],
                   TST_FILES, "f5g")
    expect(p5g.returncode == 1
           and "FIXTURE IDENTITY RECEIPT FAILED"
           in p5g.stdout + p5g.stderr
           and "loop-seeded-counter" in p5g.stdout + p5g.stderr,
           "F5g within-set fixture copy divergence -> HARD EXIT "
           "naming the fixture", results, f"rc={p5g.returncode}")
    p5h1 = run_tool(CAL_FILES[:3], TST_FILES, "f5h1")
    expect(p5h1.returncode == 1
           and "the calibration set is missing leg p2corpus"
           in p5h1.stdout + p5h1.stderr,
           "F5h missing leg in the CALIBRATION set -> HARD EXIT",
           results, f"rc={p5h1.returncode}")
    p5h2 = run_tool(CAL_FILES, TST_FILES[:3], "f5h2")
    expect(p5h2.returncode == 1
           and "the test set is missing leg p2corpus"
           in p5h2.stdout + p5h2.stderr,
           "F5h missing leg in the TEST set -> HARD EXIT", results,
           f"rc={p5h2.returncode}")
    p5i = run_tool(CAL_FILES, TST_FILES, "f5i", fixture_mode=False)
    expect(p5i.returncode == 1
           and "!= the item-199 pinned" in p5i.stdout + p5i.stderr,
           "F5i the item-199 pin law enforced outside fixture-mode -> "
           "HARD EXIT", results, f"rc={p5i.returncode}")

    # ---- F6: cross-set divergence REPORTED, never an exit ----
    print("\n--- F6: cross-set fixture divergence REPORTED (the "
          "virgin-record law) ---")
    p6 = run_tool(CAL_FILES, [f"t6_{leg}.jsonl" for leg in LEGS], "f6")
    expect(p6.returncode == 0, "F6 exit 0 (reported, not an exit)",
           results, f"rc={p6.returncode} {p6.stdout[-300:]}")
    o6 = load_out("f6")
    cr = o6["fixture_identity_receipt"]["cross_set_reported"]
    expect(cr["n_compared"] == 10 and cr["n_identical"] == 9
           and cr["divergent_fixtures"] == ["loop-seeded-counter"],
           "F6 the export reports the divergent fixture "
           "(9/10 identical)", results, json.dumps(cr))
    expect("DIVERGENT" in p6.stdout,
           "F6 the console reports the divergence", results)
    for leg in LEGS:
        check_leg(o6, leg, exp1, results, "F6")
    expect(o6["presented_candidate_verdict"]["verdict_presented"]
           == "PASS_2SIGMA-ALL-FOUR-LEGS",
           "F6 the readout is undisturbed (the 63-step copy scores "
           "identically; candidate PASS)", results)

    # ---- F8: the tuned legs (near-bar PASS + jitter) ----
    print("\n--- F8: tuned legs -- gap 2.01 (PASS + near-bar) / gap "
          "1.99 (INCONCLUSIVE-FROM-JITTER) ---")
    exp8 = dict(exp1)
    exp8["gsm8k"] = leg_expected(
        cal_s, cal_pr,
        [tuned["a_gsm"] + 0.001 * i for i in range(N_CLEAN)],
        [3.5 - 0.062 * i for i in range(N_CLEAN)], lv_s, lv_pr)
    exp8["humaneval"] = leg_expected(
        cal_s, cal_pr,
        [tuned["a_he"] + 0.001 * i for i in range(N_CLEAN)],
        [3.5 - 0.062 * i for i in range(N_CLEAN)], lv_s, lv_pr)
    assert round(exp8["gsm8k"]["gap"], 2) == 2.01, \
        f"tuned gsm gap off-target: {exp8['gsm8k']['gap']}"
    assert round(exp8["humaneval"]["gap"], 2) == 1.99, \
        f"tuned he gap off-target: {exp8['humaneval']['gap']}"
    p8 = run_tool(CAL_FILES,
                  ["t8_gsm_tuned.jsonl", "t8_he_tuned.jsonl",
                   "t_prose17p.jsonl", "t_p2corpus.jsonl"], "f8")
    expect(p8.returncode == 0, "F8 exit 0", results,
           f"rc={p8.returncode} {p8.stdout[-300:]}")
    o8 = load_out("f8")
    g8 = o8["legs"]["gsm8k"]["test"]["ensemble"]
    expect(near(g8["sigma_gap"], round(exp8["gsm8k"]["gap"], 3), 1e-9)
           and g8["verdict_presented"] == "PASS_2SIGMA"
           and "NEAR-BAR" in g8["verdict_basis"],
           "F8 gsm8k tuned to gap 2.01: PASS_2SIGMA + the near-bar "
           "flag (hand-solved intercept)", results,
           f"gap {g8['sigma_gap']} typing {g8['verdict_presented']}")
    h8 = o8["legs"]["humaneval"]["test"]["ensemble"]
    expect(near(h8["sigma_gap"], round(exp8["humaneval"]["gap"], 3), 1e-9)
           and h8["verdict_presented"] == "INCONCLUSIVE-FROM-JITTER",
           "F8 humaneval tuned to gap 1.99: INCONCLUSIVE-FROM-JITTER",
           results,
           f"gap {h8['sigma_gap']} typing {h8['verdict_presented']}")
    p8v = o8["presented_candidate_verdict"]
    expect(p8v["verdict_presented"] == "INCONCLUSIVE-FROM-JITTER"
           and p8v["jitter_legs"] == ["humaneval"]
           and p8v["near_bar_legs"] == ["gsm8k"]
           and p8v["failed_legs"] == [],
           "F8 candidate-level INCONCLUSIVE-FROM-JITTER with the "
           "near-bar leg flagged", results, json.dumps(p8v))

    # ---- F9: the clean four-leg DOC-SPLIT run (ledger item 229) ----
    print("\n--- F9: the doc-split amendment -- clean four-leg run; "
          "hand-checked halves ---")
    exp9 = {leg: leg_expected_split(cal_s, cal_pr, lv_s, lv_pr)
            for leg in LEGS}
    p9 = run_tool_split(CAL_FILES, "f9")
    expect(p9.returncode == 0, "F9 exit 0", results,
           f"rc={p9.returncode} {p9.stdout[-400:] if p9.returncode else ''}")
    o9 = load_out("f9")
    expect("DOC-SPLIT AMENDMENT" in p9.stdout
           and "EVEN doc_id = calibration half | ODD doc_id = "
           "held-out test half" in p9.stdout
           and "CALIBRATION HALF [gsm8k]" in p9.stdout
           and "HELD-OUT HALF [gsm8k]" in p9.stdout,
           "F9 the split-mode banner + per-half console blocks print",
           results)
    expect(o9["doc_split_mode"] is True
           and "ledger item 229" in o9["amendment"]
           and o9["doc_split"]["calib_half"] == "even doc_id"
           and o9["doc_split"]["held_out_half"] == "odd doc_id"
           and "ledger item 229" in o9["doc_split"]["rule"]
           and "permutation null" in o9["doc_split"]["caveat"],
           "F9 the export carries the doc_split block (item 229 rule "
           "+ the pinned caveat)", results,
           json.dumps(o9["doc_split"])[:200])
    expect(len(o9["inputs"]["walks"]) == 4
           and o9["fixture_identity_receipt"]["walks"]
           ["n_loop_fixtures"] == 10,
           "F9 the four walks passed ONCE; the within-set fixture "
           "receipt (10 fixtures)", results,
           json.dumps(o9["fixture_identity_receipt"]))
    expect("test" not in o9["inputs"],
           "F9 no test set in split mode (the split lives inside "
           "the tool)", results)
    for leg in LEGS:
        check_leg_split(o9, leg, exp9, results, "F9")
    pcv9 = o9["presented_candidate_verdict"]
    expect(pcv9["verdict_presented"] == "PASS_2SIGMA-ALL-FOUR-LEGS"
           and pcv9["near_bar_legs"] == [] and pcv9["failed_legs"] == []
           and pcv9["jitter_legs"] == []
           and "permutation null" in pcv9["caveat"],
           "F9 presented candidate verdict PASS_2SIGMA-ALL-FOUR-LEGS "
           "+ the caveat rides the verdict", results,
           json.dumps(pcv9)[:200])

    # ---- F14: split-mode determinism ----
    print("\n--- F14: split-mode determinism (fresh re-run "
          "byte-identical) ---")
    p9b = run_tool_split(CAL_FILES, "f9b")
    with open(os.path.join(OUTDIR, "f9.json"), "rb") as fa, \
            open(os.path.join(OUTDIR, "f9b.json"), "rb") as fb:
        expect(fa.read() == fb.read() and p9b.returncode == 0,
               "F14 fresh split re-run export byte-identical",
               results)

    # ---- F10: the split-mode fire falsifier (hot docs on the
    # held-out half) ----
    print("\n--- F10: split-mode falsifier -> CANDIDATE-KILLED ---")
    exp10 = dict(exp9)
    exp10["gsm8k"] = leg_expected_split(cal_s, cal_pr, lv_s, lv_pr,
                                        hot_s=[0.5] * 5,
                                        hot_pr=[5.0] * 5)
    p10 = run_tool_split(["s10_gsm_hotodd.jsonl"] + CAL_FILES[1:],
                         "f10")
    expect(p10.returncode == 0, "F10 exit 0", results,
           f"rc={p10.returncode} {p10.stdout[-300:] if p10.returncode else ''}")
    o10 = load_out("f10")
    e10 = exp10["gsm8k"]
    o10g = o10["legs"]["gsm8k"]
    expect(o10g["doc_split"]["n_odd_held_out"] == 25
           and o10g["doc_split"]["n_even_calib"] == 21,
           "F10 the hot docs land on the HELD-OUT half only "
           "(21 calib / 25 held-out)", results,
           json.dumps(o10g["doc_split"])[:120])
    expect(o10g["test"]["fire_accounting"]["combined_fires"]
           == e10["combined"]
           and o10g["test"]["fire_accounting"]["over_budget"] is True
           and round(e10["rate"], 4) > ALPHA,
           "F10 the held-out half fires over the 5% coarse guard "
           "(EXACT count)", results,
           f"{o10g['test']['fire_accounting']['combined_fires']} "
           f"fires, rate "
           f"{o10g['test']['fire_accounting']['combined_rate']}")
    expect(o10g["test"]["ensemble"]["verdict_presented"]
           == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
           and "held-out" in o10g["test"]["ensemble"]["verdict_basis"],
           "F10 the leg typed CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
           results,
           o10g["test"]["ensemble"]["verdict_presented"])
    expect(o10g["test"]["ensemble"]["sigma_gap"] is not None
           and o10g["test"]["ensemble"]["sigma_gap"] >= 2.0
           and near(o10g["test"]["ensemble"]["sigma_gap"],
                    round(e10["gap"], 3), 1e-9),
           "F10 the sigma-gap STILL passes (killed even so -- the "
           "R16-D2 falsifier's teeth)", results,
           f"gap {o10g['test']['ensemble']['sigma_gap']}")
    expect(o10["presented_candidate_verdict"]["verdict_presented"]
           == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET",
           "F10 the candidate-level verdict KILLED", results,
           json.dumps(o10["presented_candidate_verdict"])[:120])
    for leg in ("humaneval", "prose17p", "p2corpus"):
        expect(o10["legs"][leg]["test"]["ensemble"]["verdict_presented"]
               == "PASS_2SIGMA",
               f"F10 [{leg}] unaffected legs still PASS", results)

    # ---- F11: the PER-HALF population guard ----
    print("\n--- F11: the per-half population guard (2-doc "
          "calibration half) ---")
    p11 = run_tool_split(["s11_gsm_halves.jsonl"] + CAL_FILES[1:],
                         "f11")
    o11 = load_out("f11")
    expect(p11.returncode == 0, "F11 exit 0 (typed, not crashed)",
           results, f"rc={p11.returncode}")
    g11 = o11["legs"]["gsm8k"]
    expect(g11["doc_split"]["n_even_calib"] == 2
           and g11["doc_split"]["n_odd_held_out"] == 6
           and g11["test"]["ensemble"]["verdict_presented"]
           == "INCONCLUSIVE-POPULATION-GUARD"
           and "per-half population guard" in g11["test"]["ensemble"]
           ["verdict_basis"]
           and "n_calib_half=2" in g11["test"]["ensemble"]
           ["verdict_basis"],
           "F11 the 2-doc calibration half types INCONCLUSIVE-"
           "POPULATION-GUARD naming the PER-HALF guard (the 8 "
           "positives + 6-doc held-out half are NOT the trigger)",
           results, json.dumps(g11["test"]["ensemble"]))
    expect(o11["presented_candidate_verdict"]["verdict_presented"]
           == "INCONCLUSIVE-POPULATION-GUARD",
           "F11 candidate-level INCONCLUSIVE-POPULATION-GUARD",
           results)
    expect(o11["legs"]["humaneval"]["test"]["ensemble"]
           ["verdict_presented"] == "PASS_2SIGMA",
           "F11 the other legs still compute + PASS", results)

    # ---- F12: non-int corpus doc_id in split mode ----
    print("\n--- F12: non-int doc_id -> the parity hard exit ---")
    p12 = run_tool_split(["s12_gsm_strid.jsonl"] + CAL_FILES[1:],
                         "f12")
    expect(p12.returncode == 1
           and "not an integer" in p12.stdout + p12.stderr
           and "s-401" in p12.stdout + p12.stderr
           and "ledger item 229" in p12.stdout + p12.stderr,
           "F12 non-int corpus doc_id -> HARD EXIT naming the doc "
           "(parity requires int doc_ids; loop fixtures exempt)",
           results, f"rc={p12.returncode}")

    # ---- F13: the CLI hard exits ----
    print("\n--- F13: the CLI hard exits (mode discipline) ---")
    cmd = [sys.executable, TOOL, "--doc-split"]
    for cx in CAL_FILES:
        cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
    cmd += ["--test-cache", os.path.join(FIXDIR, TST_FILES[0]),
            "--tag", "f13a",
            "--out", os.path.join(OUTDIR, "f13a.json"),
            "--fixture-mode"]
    p13a = subprocess.run(cmd, capture_output=True, text=True)
    expect(p13a.returncode == 1
           and "mutually exclusive" in p13a.stdout + p13a.stderr,
           "F13a --doc-split WITH --test-cache -> HARD EXIT (never a "
           "silent mode blend)", results, f"rc={p13a.returncode}")
    cmd = [sys.executable, TOOL]
    for cx in CAL_FILES:
        cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
    cmd += ["--tag", "f13b",
            "--out", os.path.join(OUTDIR, "f13b.json"),
            "--fixture-mode"]
    p13b = subprocess.run(cmd, capture_output=True, text=True)
    expect(p13b.returncode == 1
           and "requires --test-cache" in p13b.stdout + p13b.stderr,
           "F13b the two-set mode with NO --test-cache and NO "
           "--doc-split -> HARD EXIT", results, f"rc={p13b.returncode}")

    # ---- F15: the LEGACY-MODE regression vs the v1 build of record ----
    print("\n--- F15: the legacy-mode regression vs the preserved "
          "v1 build (item 222) ---")
    expect(sha256_file(TOOL_V1) == V1_PIN,
           "F15 the preserved v1 build is the item-222 pin EXACT "
           "(03a06966...9858f)", results, sha256_file(TOOL_V1)[:16])
    # both runs write the SAME --out path (the console prints the
    # out path -- a byte-identical stdout receipt requires it); the
    # amended run's export is saved aside before the v1 run
    # overwrites it
    p15a = run_tool(CAL_FILES, TST_FILES, "f15")
    shutil.copyfile(os.path.join(OUTDIR, "f15.json"),
                    os.path.join(OUTDIR, "f15_amended.json"))
    cmd = [sys.executable, TOOL_V1]
    for cx in CAL_FILES:
        cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
    for tx in TST_FILES:
        cmd += ["--test-cache", os.path.join(FIXDIR, tx)]
    cmd += ["--tag", "f15",
            "--out", os.path.join(OUTDIR, "f15.json"),
            "--fixture-mode"]
    p15b = subprocess.run(cmd, capture_output=True, text=True)
    expect(p15a.returncode == 0 and p15b.returncode == 0
           and p15a.stdout == p15b.stdout,
           "F15 the amended tool's legacy two-set console stdout "
           "BYTE-IDENTICAL to the v1 build of record", results,
           f"rc {p15a.returncode}/{p15b.returncode}")
    with open(os.path.join(OUTDIR, "f15_amended.json")) as f:
        o15a = json.load(f)
    with open(os.path.join(OUTDIR, "f15.json")) as f:
        o15b = json.load(f)
    sha_a, sha_b = o15a.pop("tool_sha256"), o15b.pop("tool_sha256")
    expect(sha_b == V1_PIN
           and o15a == o15b,
           "F15 the legacy export equal to v1's in EVERY field except "
           "the tool's own SHA (the v1 SHA rides v1's export; the "
           "amended SHA rides the amended export)", results,
           f"amended {sha_a[:16]}... vs v1 {sha_b[:16]}...")

    n_pass = sum(1 for r in results if r[0])
    n_fail = len(results) - n_pass
    print("\n  === ACCEPTANCE CENSUS: "
          f"{n_pass} PASS / {n_fail} FAIL ===")
    for ok, label, _ in results:
        if not ok:
            print(f"    FAILED: {label}")
    print("  Fix-the-fixture-or-the-builder, never the tool"
          + ("; FAIL LOUD." if n_fail else "."))
    print("=" * 78)
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

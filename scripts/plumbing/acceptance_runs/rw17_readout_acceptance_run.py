#!/usr/bin/env python3
"""rw17_readout_acceptance_run.py -- THE ACCEPTANCE RUNNER for the
RW-17 fresh-corpus adjudication readout tool triadic_rw17_readout.py
(the pinned sheet SS4.5 readout tool amendment, ledger items
241(c)(5)/254(j); the pinned sheet rw17-fresh-corpus-preregistration.md,
SHA-256 64f87bc01906ee6f5a50d38c2b09c09aa9f089f14803cfae9e8a07dd0af74075).

THE LAW OF THIS RUNNER: every family drives the REAL TOOL via its CLI
on synthetic four-leg worlds built from FROZEN constants, and every
exported quantity is compared EXACT against THIS RUNNER'S OWN
INDEPENDENT RECOMPUTATION (its own arithmetic, never the tool's
functions) -- the item-242 acceptance pattern. Fix-the-fixture-or-
the-builder, never the tool's record.

THE FAMILIES:
  F1  the clean four-leg synthetic world (the V-PASS world: all four
      legs PASS_2SIGMA inside the budget, censuses matching the
      item-254 pins 0/1/3/95, one empty-form record, thin-style
      records throughout): EVERY exported quantity EXACT vs the
      independent recompute -- census receipts, parity, baselines,
      z, armed D, t_leg/t_esc/th_C/th_F, the level-set receipt, the
      held-out block incl. Wilson + fired docs (order + every field
      + every SEC view + co_elevated/escalation), the overlap line,
      catches, gap/AUC, verdict typings, loop views, population
      summaries, the forensics block, the candidate verdict.
  F2  the arming law: on the F-only mbpprw17 leg D == z_F EXACTLY on
      every doc (the loops' huge z_C ignored, never fires).
  F3  the level-set receipt self-consistent on all four legs.
  F4  the SEC identities (N_band/R_band/frac; the closed-form
      constant-PR doc: N_band == R_band == n_prsig_steps at every
      sweep factor, ceiling_pos_frac == 0.0; R_band <= N_band; the
      sweep monotone).
  F5  ALL hard exits fire loud, naming the defect: truncated JSON,
      census premise violation, non-int doc_id, duplicate leg,
      missing leg, unrecognized (old-corpus) leg, real-mode SS4 SHA
      pin, duplicate record key, absent statistic, degenerate
      calibration, fixture-identity divergence, partial fixture
      overlap, ragged step columns, n_gen_steps mismatch, key
      mismatch, non-object record, non-object steps, the census-pin
      fixture-mode ECHO (rc 0 + the echo line).
  F6  the verdict worlds, hand-tuned on the gsmrw17 knob: V-NEAR
      (gap in [2.0, 2.02): PASS_2SIGMA + the near-bar FLAG),
      V-JITTER (gap in [1.98, 2.0): INCONCLUSIVE-FROM-JITTER),
      V-FAIL (gap comfortably below the jitter band: FAIL),
      V-GUARD (a tiny leg: INCONCLUSIVE-POPULATION-GUARD),
      V-KILLED (hot held-out docs: fires over budget with the gap
      STILL >= 2.0 -- the falsifier's teeth -- plus a guard leg
      proving KILLED dominates a guard typing).
  F7  port fidelity (the item-242 build of record): the old tool's
      SHA verified; the OLD tool CLI run --fixture-mode on the
      banked R-BC1 smoke cache + the three banked fillers; the 17p
      leg's sigma-gap round4 == 2.6528 (the item-242 pin, EXACT);
      the 17p AUC == 0.9875 (as measured TODAY on the pinned bytes;
      the item-242 LEDGER PROSE says 0.8750 -- a prose slip named
      honestly at the banking item, never edited; the banked
      item-242 control console records PASS without the value);
      the NEW tool's own imported functions (importlib) replicating
      the old pipeline over the R-BC1 records reproduce the old
      export's mu/sd/t_leg/t_esc/th_C/th_F/gap/AUC EXACTLY; plus a
      pure-function battery (mean_std/_quantile/sigma_gap/
      auc_pos_neg/wilson_upper old vs new, and the arming table
      old legs vs new legs).
  F8  determinism: the same-path re-run byte-identical on BOTH the
      export AND the console.
  F9  the constants echo: the construction constants, the expected
      censuses of record, the SS4 pins (echoed in fixture mode,
      match recorded False), the pinned sheet's SHA, the census-law
      string, the caveat lines, the tool's own SHA.

HONEST UNREACHABILITY, NAMED: the REAL-MODE census-pin hard exit
sits behind the SS4 SHA-pin enforcement (reaching it requires
caches whose bytes hash to the pinned SHAs -- impossible
synthetically); the fixture-mode ECHO path is what F5 tests, and
the real-mode SHA-pin exit itself IS tested (F5). The real-mode
census exit fires owner-side on any wrong-bytes cache that passes
the SHA pins -- which is to say: it cannot fire, by design; the
SHA pins are the outer wall.

theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, or
adjudicated; findings presented, never adjudicated -- the owner's
stamps decide.
"""

import hashlib
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_rw17_readout.py")
OLD_TOOL = os.path.join(HERE, "triadic_rw17_sec_baseline.py")
OLD_TOOL_SHA = ("8ff25ba2309a86e8f1ff373e4eee41c18022b43a572022"
                "ce2ce887a051c2c0bf")
RBC1 = os.path.join(HERE, "rw16_control_fixtures",
                    "triadic_t2_cache_t2-prose17p-smoke_bfloat16_bos"
                    ".jsonl")
RBC1_SHA = ("a2f57964232d981db586b007ddbf642b7d6fe7224f65f3499ce9e"
            "cacb2e763e1")
FILLER_GSM = os.path.join(HERE, "rw16_control_fixtures",
                          "filler_gsm8k.jsonl")
FILLER_HE = os.path.join(HERE, "rw16_control_fixtures",
                         "filler_humaneval.jsonl")
FILLER_P2 = os.path.join(HERE, "rw16_control_fixtures",
                         "filler_p2corpus.jsonl")
PREREG_SHA = ("64f87bc01906ee6f5a50d38c2b09c09aa9f089f14803cfae9e8a"
              "07dd0af74075")
PINNED_CACHE_SHA = {
    "gsmrw17": ("triadic_t2_cache_rw17-math-fresh_bfloat16_bos.jsonl",
                "5bc76e86a85271bbed1ed57909d567d0962d98884fff055ea4d8"
                "a7be857075a3"),
    "mbpprw17": ("triadic_t2_cache_rw17-code-fresh_bfloat16_bos.jsonl",
                 "38c1225263290712be4b9108f1037f36285b849618e993d1d6c0"
                 "ace095422b13"),
    "prose17p-rw17": ("triadic_t2_cache_rw17-prose-fresh_bfloat16_bos"
                      ".jsonl",
                      "69ad79ae0dca75384c832ae1ecfee158941fcf568516650"
                      "81b6a901f59e10911"),
    "p2corpus-rw17": ("triadic_t2_cache_rw17-p2-fresh_bfloat16_bos"
                      ".jsonl",
                      "69b10ff18ad951da65f6662f2f51a2d702f28f0effe8539"
                      "0aad6823a0e4ef247"),
}
EXPECTED_FRESH_CENSUS = {
    "gsmrw17": 0, "mbpprw17": 1, "prose17p-rw17": 3, "p2corpus-rw17": 95}
LEGS = ("gsmrw17", "mbpprw17", "prose17p-rw17", "p2corpus-rw17")

# =========================================================================
# The frozen synthetic-world constants (the verdict-world knobs, bisected
# against the REAL tool; the loop fixtures are the SAME BYTES in all four
# caches of every world -- the within-set fixture byte-identity law -- so
# per-leg tuning rides the CLEAN population band edges only).
# =========================================================================
STEP_FIELDS = ("t", "id", "E", "rho", "s", "f", "layer", "H", "PR",
               "a", "rsize", "dead5", "dead4", "dead3", "dead_share")
FIXTURE_STEPS = {
    "loop-injection-code": 256, "loop-injection-prose": 256,
    "mask-reserved-stubborn": 256, "loop-seeded-counter": 256,
    "loop-seeded-cycle": 256, "loop-seeded-json": 256,
    "loop-seeded-countdown": 256, "loop-seeded-code-line": 37,
    "loop-seeded-affirm": 11, "loop-seeded-chant": 1,
}
LIVE_PR_MID = 0.40
LIVE_S_CONST = 0.34
CF_DOC_ID, CF_PR = 39, 0.38
PR_BASE_SPREAD = 0.72
PR_JITTER = 0.04
S_BAND_W = 0.20

# the frozen verdict-world knobs (gsmrw17's pr_lo per world)
KNOB_V_PASS = 2.00
KNOB_V_NEAR = 0.784140625
KNOB_V_JITTER = 0.7772265625
KNOB_V_FAIL = 0.6215625


def pv(doc_id, step, salt):
    d = (sum(ord(c) for c in doc_id) if isinstance(doc_id, str)
         else int(doc_id))
    h = (d * 2654435761 + step * 40503 + salt * 97) % 4294967296
    h ^= h >> 16
    h = (h * 2654435761) % 4294967296
    h ^= h >> 13
    return (h % 100000) / 100000.0


def rec(leg, doc_id, n_steps, prs, ss):
    t = list(range(n_steps))
    return {
        "key": f"{leg}:{doc_id}", "leg": leg, "doc_id": doc_id,
        "bos": True, "instrument": "SYNTH", "prompt_len": 9,
        "stop_reason": "eos", "n_gen_steps": n_steps,
        "n_content_steps": n_steps, "walk_ids": [13] * n_steps,
        "steps": {"t": t, "id": [13] * n_steps,
                  "E": [1.0 + pv(doc_id, i, 3) for i in t],
                  "rho": [0.5 + 0.3 * pv(doc_id, i, 4) for i in t],
                  "s": ss,
                  "f": [pv(doc_id, i, 6) for i in t],
                  "layer": [0] * n_steps,
                  "H": [1.0 + pv(doc_id, i, 5) for i in t],
                  "PR": prs,
                  "a": [pv(doc_id, i, 7) for i in t],
                  "rsize": [pv(doc_id, i, 8) for i in t],
                  "dead5": [0.0] * n_steps, "dead4": [0.0] * n_steps,
                  "dead3": [0.0] * n_steps,
                  "dead_share": [0.0] * n_steps},
        "commits": [i for i in t if i % 4 == 0],
        "hidden_n": n_steps, "hidden_dim": 4, "hidden_b64": "",
        "thin": True}


def corpus_doc(leg, doc_id, n_steps, pr_lo, s_lo, salt,
               pr_const=None, pr_base_hot=None, s_const=None):
    t = list(range(n_steps))
    if pr_const is not None:
        prs = [pr_const] * n_steps
    else:
        if pr_base_hot is not None:
            base = pr_lo - pr_base_hot
        else:
            base = pr_lo + PR_BASE_SPREAD * pv(doc_id, -1, salt)
        prs = [base + PR_JITTER * pv(doc_id, i, salt) for i in t]
    if s_const is not None:
        ss = [s_const] * n_steps
    else:
        ss = [s_lo + S_BAND_W * pv(doc_id, i, salt + 1) for i in t]
    return rec(leg, doc_id, n_steps, prs, ss)


def census_doc(leg, doc_id):
    d = {"key": f"{leg}:{doc_id}", "leg": leg, "doc_id": doc_id,
         "bos": True, "instrument": "SYNTH", "prompt_len": 9,
         "stop_reason": "eos", "n_gen_steps": 0, "n_content_steps": 0,
         "walk_ids": [], "commits": [], "hidden_n": 0,
         "hidden_dim": 4, "hidden_b64": "", "thin": True,
         "steps": {k: [] for k in STEP_FIELDS}}
    return d


def loop_fixtures():
    out = []
    for fid, n in FIXTURE_STEPS.items():
        t = list(range(n))
        prs = [LIVE_PR_MID if 5 <= i <= n - 5 else
               0.45 + 0.40 * pv(fid, i, 1) for i in t]
        out.append(rec("loop", fid, n, prs, [LIVE_S_CONST] * n))
    return out


def base_spec(pr_lo_gsm=KNOB_V_PASS):
    """The V-PASS world; the verdict worlds override legs on top."""
    return {
        "gsmrw17": {"n_corpus": 40, "census_ids": [], "pr_lo": pr_lo_gsm,
                    "s_lo": 0.50, "salt": 11, "closed_form": True,
                    "hot_odd": {}, "hot_even": {6: 1.5, 14: 1.6},
                    "empty_form": True},
        "mbpprw17": {"n_corpus": 41, "census_ids": [0], "pr_lo": 0.45,
                     "s_lo": 0.31, "salt": 22, "closed_form": False,
                     "hot_odd": {}, "hot_even": {},
                     "hot_even_s": {6: 0.334, 14: 0.337}},
        "prose17p-rw17": {"n_corpus": 43, "census_ids": [0, 2, 41],
                          "pr_lo": 1.60, "s_lo": 0.50, "salt": 33,
                          "closed_form": False, "hot_odd": {},
                          "hot_even": {6: 1.5, 14: 1.6}},
        "p2corpus-rw17": {"n_corpus": 135,
                          "census_ids": list(range(95)),
                          "pr_lo": 2.00, "s_lo": 0.50, "salt": 44,
                          "closed_form": False, "hot_odd": {},
                          "hot_even": {96: 1.5, 114: 1.6}},
    }


def build_world(dirpath, spec, skip_empty_form=False):
    os.makedirs(dirpath, exist_ok=True)
    for leg in LEGS:
        sp = spec[leg]
        path = os.path.join(dirpath, f"cache_{leg}.jsonl")
        with open(path, "w") as f:
            censused = set(sp.get("census_ids", []))
            for did in range(sp["n_corpus"]):
                if did in censused:
                    r = census_doc(leg, did)
                elif sp.get("closed_form") and did == CF_DOC_ID:
                    r = corpus_doc(leg, did, 40, sp["pr_lo"],
                                    sp["s_lo"], sp["salt"], pr_const=CF_PR)
                elif did in sp.get("hot_odd", {}):
                    r = corpus_doc(leg, did, 40, sp["pr_lo"], sp["s_lo"],
                                   sp["salt"],
                                   pr_base_hot=sp["hot_odd"][did])
                elif did in sp.get("hot_even", {}):
                    r = corpus_doc(leg, did, 40, sp["pr_lo"], sp["s_lo"],
                                   sp["salt"],
                                   pr_base_hot=sp["hot_even"][did])
                elif did in sp.get("hot_even_s", {}):
                    r = corpus_doc(leg, did, 40, sp["pr_lo"], sp["s_lo"],
                                   sp["salt"],
                                   s_const=sp["hot_even_s"][did])
                else:
                    r = corpus_doc(leg, did, 40, sp["pr_lo"],
                                   sp["s_lo"], sp["salt"])
                f.write(json.dumps(r, sort_keys=True) + "\n")
            if sp.get("empty_form") and not skip_empty_form:
                f.write(json.dumps({"empty": True,
                                    "key": f"{leg}:empty-form-1"},
                                   sort_keys=True) + "\n")
            for r in loop_fixtures():
                f.write(json.dumps(r, sort_keys=True) + "\n")
    return [os.path.join(dirpath, f"cache_{l}.jsonl") for l in LEGS]


def run_tool(caches, out, tag, fixture_mode=True, tool=TOOL):
    cmd = [sys.executable, tool]
    if fixture_mode:
        cmd.append("--fixture-mode")
    for c in caches:
        cmd += ["--cache", c]
    cmd += ["--tag", tag, "--out", out]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p

# =========================================================================
# THE INDEPENDENT RECOMPUTE ENGINE (this runner's own arithmetic; never
# the tool's functions; hand-ported from the pinned construction).
# =========================================================================
R_DEPTH_BUCKET = 16
R_BASELINE_MIN_N = 30
R_LOOP_INERT_MIN_STEPS = 32
R_W_GRAM = 8
R_ALPHA = 0.05
R_ALPHA_ESC = 0.01
R_CO_ELEV_Q = 0.975
R_SEC_BAND_FACTOR = 0.90
R_SEC_SWEEP = (0.80, 0.85, 0.90, 0.95)
R_POP_GUARD_MIN = 5
R_JITTER_BAND = 0.02
R_ARMED = {"gsmrw17": ("C", "F"), "mbpprw17": ("F",),
           "prose17p-rw17": ("C", "F"), "p2corpus-rw17": ("C", "F")}

MODE_TYPE = ("ADJUDICATION READOUT OF RECORD -- PRESENTED, NEVER "
             "ADJUDICATED; THE OWNER'S STAMPS DECIDE")
CENSUS_REASON = "empty generation, EOS@step0 (measured at readout)"
LEVEL_SET_NOTE = ("the level-set rule controls the calibration half's "
                  "own combined count BY CONSTRUCTION; a violation is "
                  "ties at t_leg, reported honestly, never adjudicated")
OVERLAP_NOTE = ("the standing loop-floor overlap count (the item-232 "
                "decomposition): held-out clean docs at/above the "
                "easiest live loop's D -- phenomenon beta always "
                "visible, never silent, never adjudicated away")
SEP_NOTE = ("the BAR's statistic under the ARMED construction (the "
            "live fixtures vs the held-out clean docs)")


def r_mstd(vals):
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / max(len(vals) - 1, 1)) ** 0.5
    return m, sd


def r_quantile(sorted_vals, q):
    n = len(sorted_vals)
    if n == 0:
        return None
    if n == 1 or q <= 0.0:
        return float(sorted_vals[0])
    if q >= 1.0:
        return float(sorted_vals[-1])
    p = q * (n - 1)
    lo = int(math.floor(p))
    frac = p - lo
    if frac <= 0.0:
        return float(sorted_vals[lo])
    if lo + 1 >= n:
        return float(sorted_vals[-1])
    return (float(sorted_vals[lo])
            + frac * (float(sorted_vals[lo + 1])
                      - float(sorted_vals[lo])))


def r_wilson(k, n, z=1.645):
    if n == 0:
        return None
    ph = k / n
    den = 1.0 + z * z / n
    ctr = ph + z * z / (2 * n)
    rad = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (ctr + rad) / den


def r_sgap(pos, neg):
    if not pos or not neg:
        return None
    mp, mn_ = sum(pos) / len(pos), sum(neg) / len(neg)
    sp = (sum((v - mp) ** 2 for v in pos) / max(len(pos) - 1, 1)) ** 0.5
    sn = (sum((v - mn_) ** 2 for v in neg) / max(len(neg) - 1, 1)) ** 0.5
    pooled = math.sqrt((sp * sp + sn * sn) / 2.0)
    return (mp - mn_) / pooled if pooled > 0 else 0.0


def r_auc(pos, neg):
    if not pos or not neg:
        return None
    vals = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg],
                  key=lambda t: t[0])
    n_pos, n_neg = len(pos), len(neg)
    ranks = []
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1][0] == vals[i][0]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        ranks.extend([r] * (j - i + 1))
        i = j + 1
    pos_rank_sum = sum(r for r, (_, p) in zip(ranks, vals) if p == 1)
    return (pos_rank_sum - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def r_baselines(corpus_docs):
    buck = {"E": {}, "rho": {}, "s": {}}
    pooled = {"E": [], "rho": [], "s": []}
    lay = {"H": {}, "PR": {}}
    lay_pool = {"H": [], "PR": []}
    for d in corpus_docs:
        st = d["steps"]
        for key in ("E", "rho", "s"):
            for t, v in zip(st["t"], st[key]):
                if v is None:
                    continue
                b = t // R_DEPTH_BUCKET
                buck[key].setdefault(b, []).append(v)
                pooled[key].append(v)
        for l, v in zip(st["layer"], st["H"]):
            if v is not None and l is not None:
                lay["H"].setdefault(l, []).append(v)
                lay_pool["H"].append(v)
        for l, v in zip(st["layer"], st["PR"]):
            if v is not None and l is not None:
                lay["PR"].setdefault(l, []).append(v)
                lay_pool["PR"].append(v)
    base = {"bucket": {}, "layer": {}}
    for key in ("E", "rho", "s"):
        gm, gsd = r_mstd(pooled[key])
        for b, vals in sorted(buck[key].items()):
            base["bucket"][(key, b)] = (r_mstd(vals)
                                        if len(vals) >= R_BASELINE_MIN_N
                                        else (gm, gsd))
    for key in ("H", "PR"):
        gm, gsd = r_mstd(lay_pool[key])
        for l, vals in sorted(lay[key].items()):
            base["layer"][(key, l)] = (r_mstd(vals)
                                       if len(vals) >= R_BASELINE_MIN_N
                                       else (gm, gsd))
    return base


def r_derive(d, base):
    st = d["steps"]
    n = len(st["t"])
    ebar = []
    for i in range(n):
        lo = max(0, i - R_W_GRAM + 1)
        vals = [st["E"][j] for j in range(lo, i + 1)
               if st["E"][j] is not None]
        ebar.append(sum(vals) / len(vals) if vals else None)

    def bget(key, t):
        return base["bucket"].get((key, t // R_DEPTH_BUCKET))

    c_list, d_list, sexc_list = [], [], []
    for i in range(n):
        t = st["t"][i]
        bE, bR, bS = bget("E", t), bget("rho", t), bget("s", t)
        c_list.append(1.0 - ebar[i] / bE[0]
                      if (bE and ebar[i] and bE[0] > 1e-9) else None)
        d_list.append(1.0 - st["rho"][i] / bR[0]
                      if (bR and st["rho"][i] is not None
                      and bR[0] > 1e-9) else None)
        sexc_list.append((bS[0] - st["s"][i]) / bS[1]
                         if (bS and st["s"][i] is not None
                         and bS[1] > 1e-9) else None)
    hsig, prsig = [], []
    for l, hv, pvv in zip(st["layer"], st["H"], st["PR"]):
        bH = base["layer"].get(("H", l)) if l is not None else None
        bP = base["layer"].get(("PR", l)) if l is not None else None
        hsig.append(abs(hv - bH[0]) / bH[1]
                    if (bH and hv is not None and bH[1] > 1e-9) else None)
        prsig.append((bP[0] - pvv) / bP[1]
                     if (bP and pvv is not None and bP[1] > 1e-9) else None)

    def mx(vals):
        vs = [v for v in vals if v is not None]
        return max(vs) if vs else None

    def mn(vals):
        vs = [v for v in vals if v is not None]
        return min(vs) if vs else None

    d["derived"] = {"C": c_list, "D": d_list, "Sexc": sexc_list,
                    "Hsig": hsig, "PRsig": prsig, "Ebar": ebar}
    d["score"] = {"maxC": mx(c_list), "minEbar": mn(ebar),
                  "maxD": mx(d_list), "minRho": mn(st["rho"]),
                  "maxSexc": mx(sexc_list), "minS": mn(st["s"]),
                  "maxAbsHsig": mx(hsig), "maxPRsig": mx(prsig),
                  "maxf": mx(st["f"])}
    return d


def r_sec_profile(d):
    prsig = d["derived"]["PRsig"]
    mx = d["score"]["maxPRsig"]
    if mx is None:
        return None
    idx = [i for i, v in enumerate(prsig) if v is not None]
    if not idx:
        return None
    n_steps = len(idx)
    argmax_i = max(idx, key=lambda i: (prsig[i], -i))
    ceiling_pos = d["steps"]["t"][argmax_i]
    denom = max(d["n_gen_steps"] - 1, 1)
    bands = {}
    for f in R_SEC_SWEEP:
        thr = f * mx
        run = best = 0
        n_band = 0
        for i in idx:
            if prsig[i] >= thr:
                n_band += 1
                run += 1
                if run > best:
                    best = run
            else:
                run = 0
        bands[f"{f:.2f}"] = {"N_band": n_band, "R_band": best,
                             "frac": n_band / n_steps}
    return {"maxPRsig": mx, "n_prsig_steps": n_steps,
            "ceiling_pos": ceiling_pos,
            "ceiling_pos_frac": ceiling_pos / denom,
            "band": bands}


def r_doc_view(d, leg):
    p = r_sec_profile(d)
    band = p["band"][f"{R_SEC_BAND_FACTOR:.2f}"] if p else None
    return {
        "doc_id": d["doc_id"],
        "half": ("calibration" if d["doc_id"] % 2 == 0
                 else "held-out") if isinstance(d["doc_id"], int)
        else "loop-fixture",
        "z_C": d["z_C"], "z_F": d["z_F"], "D": d["D"],
        "maxPRsig": d["score"]["maxPRsig"],
        "minS": d["score"]["minS"],
        "sec1_N_band": band["N_band"] if band else None,
        "sec1_R_band": band["R_band"] if band else None,
        "sec1_frac": band["frac"] if band else None,
        "sec1_band_sweep": p["band"] if p else None,
        "sec2_ceiling_pos": p["ceiling_pos"] if p else None,
        "sec2_ceiling_pos_frac": p["ceiling_pos_frac"] if p else None,
        "n_prsig_steps": p["n_prsig_steps"] if p else None,
    }


def r_summarize(docs):
    if not docs:
        return {"n": 0}
    nb = [d["sec1_N_band"] for d in docs if d["sec1_N_band"] is not None]
    rb = [d["sec1_R_band"] for d in docs if d["sec1_R_band"] is not None]
    cp = [d["sec2_ceiling_pos_frac"] for d in docs
          if d["sec2_ceiling_pos_frac"] is not None]
    dd = [d["D"] for d in docs]
    return {
        "n": len(docs),
        "mean_N_band": (sum(nb) / len(nb)) if nb else None,
        "mean_R_band": (sum(rb) / len(rb)) if rb else None,
        "mean_ceiling_pos_frac": (sum(cp) / len(cp)) if cp else None,
        "mean_D": (sum(dd) / len(dd)) if dd else None,
        "max_D": max(dd) if dd else None,
    }


def r_verdict_typing(gap, n_pos, n_neg):
    if n_pos < R_POP_GUARD_MIN or n_neg < R_POP_GUARD_MIN:
        return ("INCONCLUSIVE-POPULATION-GUARD",
                f"population guard (the sheet SS1.4): n_pos={n_pos} "
                f"n_neg={n_neg} (< {R_POP_GUARD_MIN})")
    if gap is None:
        return ("INCONCLUSIVE-EMPTY-POPULATION", "no values")
    if gap >= 2.0:
        why = (f"held-out 2-sigma bar met on this leg "
               f"(gap {round(gap, 3)} >= 2.0)")
        if gap < 2.0 + R_JITTER_BAND:
            why += (" -- NEAR-BAR: the margin sits inside the width "
                    "of the banked +/-0.01-0.02-sigma reproducibility "
                    "floor; flagged for the owner's eyes")
        return ("PASS_2SIGMA", why)
    if gap >= 2.0 - R_JITTER_BAND:
        return ("INCONCLUSIVE-FROM-JITTER",
                f"below-bar near-miss inside the banked +/-0.02-sigma "
                f"jitter floor (gap {round(gap, 3)})")
    return ("FAIL",
            f"held-out 2-sigma bar not met on this leg "
            f"(gap {round(gap, 3)} < 2.0, outside the jitter band)")


def r_forensics(leg, pos_views, neg_views, typing, gap, fires, t_leg):
    n_via_c = sum(1 for d in pos_views if d["z_C"] >= d["z_F"])
    n_via_f = len(pos_views) - n_via_c
    pos_d = [d["D"] for d in pos_views]
    neg_d = [d["D"] for d in neg_views]
    min_loop_d = min(pos_d) if pos_d else None
    overlap = (sum(1 for v in neg_d if min_loop_d is not None
                   and v >= min_loop_d) if pos_d else None)
    fired = sorted(fires, key=lambda d: -d["D"])[:3]
    where = ([{"doc_id": d["doc_id"], "z_C": round(d["z_C"], 4),
               "z_F": round(d["z_F"], 4),
               "D": round(d["D"], 4),
               "max_side": ("C" if d["z_C"] >= d["z_F"] else "F")}
              for d in fired] if fired else [])
    if typing == "PASS_2SIGMA":
        why = (f"the loop population's D rides Side "
               f"{'C' if n_via_c >= n_via_f else 'F'} on "
               f"{max(n_via_c, n_via_f)}/{len(pos_views)} docs; the "
               f"clean overlap at the loop floor is {overlap} doc(s)")
    elif typing == "INCONCLUSIVE-FROM-JITTER":
        why = (f"the gap sits in the jitter band; the loop D floor vs "
               f"the clean D tail cannot be resolved at the banked "
               f"+/-0.01-0.02-sigma reproducibility floor; clean "
               f"overlap at the loop floor: {overlap} doc(s)")
    else:
        why = (f"the clean D tail overlaps the loop floor "
               f"({overlap} clean doc(s) at/above the lowest loop D); "
               f"the loop signal rides Side "
               f"{'C' if n_via_c >= n_via_f else 'F'} on "
               f"{max(n_via_c, n_via_f)}/{len(pos_views)} docs")
    return {
        "how": {
            "loop_docs": len(pos_views),
            "loop_carried_via_zC": n_via_c,
            "loop_carried_via_zF": n_via_f,
            "loop_D_range": [round(min(pos_d), 4), round(max(pos_d), 4)]
            if pos_d else None,
            "clean_D_max": round(max(neg_d), 4) if neg_d else None,
        },
        "where": {
            "leg": leg,
            "threshold_t_leg": round(t_leg, 4) if t_leg is not None
            else None,
            "top_fired_clean_docs": where,
            "clean_overlap_at_loop_floor": overlap,
        },
        "why": why,
        "what_next": [
            "this block is the item-220 failure-forensics directive: "
            "presented, never adjudicated; no re-scoring follows "
            "from it",
            "any threshold re-calibration is the theta-wiring "
            "pre-registration's own step (R16-D2's binding operating "
            "alpha decides there; the sheet SS3.6); nothing wires "
            "here",
            "a per-leg scoping claim (if any) is the owner's to stamp "
            "under the D-FW3 environment-scoped adoption clause",
            "the jitter clause reads only below-bar near-misses "
            "INCONCLUSIVE-FROM-JITTER; above-bar margins inside the "
            "band's width are flagged, not re-typed",
        ],
    }


def r_load_cache(path):
    """Independent parse mirroring the loader's record partition."""
    docs, empty = [], []
    n_line = 0
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            n_line += 1
            rec = json.loads(s)
            if rec.get("empty") is True:
                parts = rec["key"].split(":", 1)
                rec["leg"], rec["doc_id"] = parts[0], parts[1]
                empty.append(rec)
            else:
                docs.append(rec)
    return docs, empty


def r_sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def recompute_world(cache_paths, tag):
    """The full independent recompute: returns the expected export."""
    legs_docs, loop_by_leg, inputs, excluded_empty = {}, {}, [], []
    fixture_copies = {}
    for path in cache_paths:
        sha = r_sha256_file(path)
        docs, empty = r_load_cache(path)
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
            name, pin = PINNED_CACHE_SHA[leg]
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
        base = r_baselines(even)
        for d in even + odd:
            r_derive(d, base)
        loop_sorted = sorted(loop_by_leg[leg],
                             key=lambda r: str(r["doc_id"]))
        live = [d for d in loop_sorted
                if d["n_gen_steps"] >= R_LOOP_INERT_MIN_STEPS]
        inert = [d for d in loop_sorted
                 if d["n_gen_steps"] < R_LOOP_INERT_MIN_STEPS]
        for d in live:
            r_derive(d, base)
        sC_e = [d["score"]["maxPRsig"] for d in even]
        sF_e = [d["score"]["minS"] for d in even]
        mu_C, sd_C = r_mstd(sC_e)
        mu_F, sd_F = r_mstd(sF_e)
        sides = R_ARMED[leg]
        for d in even + odd + live:
            d["z_C"] = (d["score"]["maxPRsig"] - mu_C) / sd_C
            d["z_F"] = (d["score"]["minS"] - mu_F) / sd_F
            vals = []
            if "C" in sides:
                vals.append(d["z_C"])
            if "F" in sides:
                vals.append(d["z_F"])
            d["D"] = max(vals)
        calib_D_sorted = sorted(d["D"] for d in even)
        t_leg = r_quantile(calib_D_sorted, 1.0 - R_ALPHA)
        t_esc = r_quantile(calib_D_sorted, 1.0 - R_ALPHA_ESC)
        calib_fires = sum(1 for d in even if d["D"] >= t_leg)
        calib_ceil = math.ceil(R_ALPHA * len(even))
        level_set_ok = calib_fires <= calib_ceil
        calib_esc = sum(1 for d in even if d["D"] >= t_esc)
        th_C = r_quantile(sorted(d["z_C"] for d in even), R_CO_ELEV_Q)
        th_F = r_quantile(sorted(d["z_F"] for d in even), R_CO_ELEV_Q)
        fires = [d for d in odd if d["D"] >= t_leg]
        n_fires = len(fires)
        rate = n_fires / len(odd) if odd else 0.0
        count_ceil = math.ceil(R_ALPHA * len(odd)) if odd else 0
        wil = r_wilson(n_fires, len(odd)) if odd else None
        esc_fires = [d for d in odd if d["D"] >= t_esc]
        fired_sorted = sorted(fires, key=lambda d: -d["D"])
        fired_views = [r_doc_view(d, leg) for d in fired_sorted]
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
        gap = (r_sgap(live_Ds, [d["D"] for d in odd])
               if live and odd else None)
        auc = (r_auc(live_Ds, [d["D"] for d in odd])
               if live and odd else None)
        catches_t_leg = sum(1 for d in live if d["D"] >= t_leg)
        catches_t_esc = sum(1 for d in live if d["D"] >= t_esc)
        if len(even) < R_POP_GUARD_MIN or len(odd) < R_POP_GUARD_MIN:
            typing, why = ("INCONCLUSIVE-POPULATION-GUARD",
                           f"per-half population guard (the sheet "
                           f"SS1.4): n_calib_half={len(even)} "
                           f"n_held_out_half={len(odd)} "
                           f"(< {R_POP_GUARD_MIN}/half)")
        else:
            typing, why = r_verdict_typing(gap, len(live), len(odd))
        over = (n_fires > count_ceil) if odd else False
        if over:
            typing = "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
            why = (f"the coarse-guard falsifier fired: the held-out "
                   f"half's clean fire count {n_fires}/{len(odd)} > "
                   f"ceil({R_ALPHA:.2f} * {len(odd)}) = {count_ceil} "
                   f"(rate {rate:.4%}) -- the candidate dies EVEN IF "
                   f"the sigma-gap passes (the pinned sheet SS1.5, "
                   f"the R16-D2 falsifier)")
        if typing == "PASS_2SIGMA" and gap is not None \
                and gap < 2.0 + R_JITTER_BAND:
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
        loop_views = [r_doc_view(d, leg) for d in live]
        held_out_views = [r_doc_view(d, leg) for d in odd]
        calib_views = [r_doc_view(d, leg) for d in even]
        forensics = r_forensics(leg, loop_views, held_out_views,
                                typing, gap, fires, t_leg)
        summaries = {
            "loops_live": r_summarize(loop_views),
            "held_out_clean_fired": r_summarize(fired_views),
            "held_out_clean_nonfired": r_summarize(
                [v for v, d in zip(held_out_views, odd)
                 if d["D"] < t_leg]),
            "calibration_half_clean": r_summarize(calib_views),
        }
        exp_legs[leg] = {
            "armed_sides": list(sides),
            "census": {"corpus_docs": len(corpus),
                       "measured_eos_step0": len(removed),
                       "expected_of_record": EXPECTED_FRESH_CENSUS[leg],
                       "receipts": census_out},
            "parity": {"n_even_calibration": len(even),
                       "n_odd_held_out": len(odd)},
            "loop_population": {"n_live": len(live),
                                "n_inert": len(inert),
                                "inert": [d["doc_id"] for d in inert]},
            "z_baselines": {"mu_C": mu_C, "sd_C": sd_C,
                            "mu_F": mu_F, "sd_F": sd_F},
            "thresholds": {"t_leg": t_leg, "t_esc": t_esc,
                           "th_C_coelev": th_C, "th_F_coelev": th_F},
            "level_set_receipt": {
                "n_calib": len(even), "alpha": R_ALPHA,
                "calib_fires": calib_fires, "ceiling": calib_ceil,
                "ok": level_set_ok, "note": LEVEL_SET_NOTE},
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
                "note": OVERLAP_NOTE},
            "loop_catches": {"n_live": len(live),
                             "at_t_leg": catches_t_leg,
                             "at_t_esc": catches_t_esc},
            "separation_context": {"sigma_gap_on_D": gap,
                                   "auc_on_D": auc, "note": SEP_NOTE},
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
                f"legs inside the +/-{R_JITTER_BAND}-sigma jitter "
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
                                      == "INCONCLUSIVE-POPULATION-GUARD"],
            "over_budget_legs": [l for l in LEGS
                                 if exp_legs[l]["verdict"]
                                 ["over_budget"]]},
        "tag": tag,
        "fixture_mode": True,
        "tool": "triadic_rw17_readout.py",
        "tool_sha256": r_sha256_file(TOOL),
        "mode": MODE_TYPE,
    }
    return exp


# =========================================================================
# The exact comparator.
# =========================================================================
def cmp_tree(exp, got, path, errs):
    if isinstance(exp, dict):
        if not isinstance(got, dict):
            errs.append(f"{path}: expected object, got {type(got).__name__}")
            return
        for k in exp:
            if k not in got:
                errs.append(f"{path}.{k}: MISSING in export")
            else:
                cmp_tree(exp[k], got[k], f"{path}.{k}", errs)
        for k in got:
            if k not in exp:
                errs.append(f"{path}.{k}: UNEXPECTED in export")
    elif isinstance(exp, list):
        if not isinstance(got, list):
            errs.append(f"{path}: expected list, got {type(got).__name__}")
            return
        if len(exp) != len(got):
            errs.append(f"{path}: length {len(got)} != expected {len(exp)}")
            return
        for i, (e, g) in enumerate(zip(exp, got)):
            cmp_tree(e, g, f"{path}[{i}]", errs)
    elif isinstance(exp, float) or isinstance(got, float):
        if exp is None or got is None or isinstance(exp, bool) \
                or isinstance(got, bool):
            if exp != got:
                errs.append(f"{path}: {got!r} != expected {exp!r}")
        elif not (abs(float(exp) - float(got)) < 1e-9):
            errs.append(f"{path}: {got!r} != expected {exp!r}")
    else:
        if exp != got:
            errs.append(f"{path}: {got!r} != expected {exp!r}")
# The FIXED export blocks (the tool's pinned string constants,
# machine-extracted verbatim from the tool's own export of the F1
# world and embedded here as literals -- F1/F9 compare them EXACT;
# they are CONSTANTS OF RECORD, never recomputed).
FIXED_TOP = {'census_law': {'expected_census_note': 'the item-254 receipt-verified '
                                        'EOS@step0 counts of record, '
                                        'ENFORCED in real mode (a census '
                                        'drift = wrong bytes = hard exit); '
                                        'echoed in fixture mode',
                'expected_fresh_census': {'gsmrw17': 0,
                                          'mbpprw17': 1,
                                          'p2corpus-rw17': 95,
                                          'prose17p-rw17': 3},
                'reason': 'empty generation, EOS@step0 (measured at '
                          'readout)'},
 'construction': {'alpha': 0.05,
                  'alpha_esc': 0.01,
                  'armed_sides': {'gsmrw17': ['C', 'F'],
                                  'mbpprw17': ['F'],
                                  'p2corpus-rw17': ['C', 'F'],
                                  'prose17p-rw17': ['C', 'F']},
                  'arming_evidence': {'gsmrw17': 'item-215: both sides '
                                                 'separate on the gsm leg '
                                                 '(math family)',
                                      'mbpprw17': 'item-215: G3_pr FAIL on '
                                                  'the he leg -- the '
                                                  'ceiling is blind on '
                                                  'code-family legs (Side '
                                                  'F only; the honest cost '
                                                  'owned in the sheet '
                                                  'SS1.2)',
                                      'p2corpus-rw17': 'items 215/231: '
                                                       'both sides '
                                                       'separate (p2 '
                                                       'family)',
                                      'prose17p-rw17': 'items 215/231: '
                                                       'both sides '
                                                       'separate (prose '
                                                       'family)'},
                  'bar': "the held-out 2-sigma bar on armed D: the leg's "
                         'live loop fixtures as positives vs the held-out '
                         "half's census-applied clean docs as negatives; "
                         'PASS_2SIGMA iff sigma-gap >= 2.0; the +/-0.02 '
                         'jitter clause on below-bar near-misses '
                         '(INCONCLUSIVE-FROM-JITTER); the above-bar '
                         'near-bar FLAG; the per-half population guard '
                         '(>=5/half)',
                  'co_elev_quantile': 0.975,
                  'doc_split': 'the item-229 parity law re-pinned for the '
                               'fresh legs (the sheet SS2): EVEN doc_id = '
                               'calibration half, ODD = held-out; the '
                               'census applied BEFORE the split; baselines '
                               'from the calibration half ONLY',
                  'falsifier': 'fires > ceil(0.05 * n_held) ==> '
                               'CANDIDATE-KILLED-FALSE-ALARM-BUDGET (the '
                               'pinned sheet SS1.5 count form; the RW-16 '
                               'rate form superseded here); KILLED '
                               'dominates a guard typing (SS1.8); the '
                               'one-sided 95% Wilson upper reported per '
                               'leg',
                  'jitter_band': 0.02,
                  'pop_guard_min': 5,
                  'sec_band_factor': 0.9,
                  'sec_sweep': [0.8, 0.85, 0.9, 0.95],
                  'statistic': "D over the leg's ARMED sides only (the "
                               "pinned sheet's arming table); an unarmed "
                               'side contributes -inf',
                  'threshold_rule': 'THRESHOLD-ON-D (the level-set rule): '
                                    "t_leg = the calibration half's "
                                    'census-applied clean-D empirical '
                                    '(1-0.05) quantile; fire iff D >= '
                                    't_leg (linear interpolation, the '
                                    'pinned _quantile)'},
 'old_corpus_anchor_reference': 'the fresh SEC readings get read against '
                                'the banked old-corpus baseline table of '
                                'record (ledger item 243, '
                                'triadic_rw17_sec_baseline_rw17-sec-baseline.json) '
                                '-- the delta reading + the '
                                'beta-recurrence attribution (recurred / '
                                'deepened / vanished) happen at the '
                                'reading, never inside this tool',
 'prereg': 'rw17-fresh-corpus-preregistration.md (owner-pinned, ledger '
           'item 241; sheet SHA-256 '
           '64f87bc01906ee6f5a50d38c2b09c09aa9f089f14803cfae9e8a07dd0af74075; '
           'the five element stamps ledger item 237)',
 'rw14_rider': 'ROUTED-TO-OWN-PRE-REG: the cache schema carries no label '
               'joins (gold/label_correct ride the run-time doc, never the '
               'cache record) -- the RW-14 riders adjudicate under their '
               'own pre-registered readout (the G-FW3 '
               'no-silent-multiplexing law); nothing fabricated here.',
 'sec_definition': {'PR_sig': 'the step-level PR signature, z-scored '
                              "against the calibration half's per-layer PR "
                              'baselines ((bP_mean - PR)/bP_sd) -- the '
                              'same series maxPRsig is the max of',
                    'SEC-1': 'N_band(f) = #{steps s : PR_sig(s) >= f * '
                             'maxPRsig(doc)}; R_band(f) = the longest '
                             'consecutive in-band run; the PINNED factor = '
                             '0.9; the sweep [0.8, 0.85, 0.9, 0.95] rides '
                             'as development data',
                    'SEC-2': 'ceiling_pos = the step index of the first '
                             'PR_sig maximum, as a fraction of '
                             '(n_gen_steps - 1)',
                    'SEC-3': "t_esc = the calibration half's clean-D "
                             'empirical (1-0.01) quantile; the escalation '
                             'counts at both tiers reported per leg',
                    'SEC-4': "per fired doc: whether EVERY ARMED side's z "
                             'exceeds its own calibration-half (1-0.025) '
                             'z-quantile (conjunction as severity '
                             'annotation, NEVER the firing rule)',
                    'none_handling': 'steps with PR = None are skipped in '
                                     'the band/argmax computations; '
                                     'n_prsig_steps = the count of '
                                     'non-None PR_sig steps'},
 'theta_note': 'theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no threshold set, moved, '
               'or adjudicated; t_leg/t_esc are calibration artifacts '
               'measured per run, never a theta move; the binding '
               'operating alpha stays deferred to the theta-wiring '
               'pre-registration (R16-D2)'}

FIXED_FIR_RULE = ('within-set byte-identity asserted (HARD EXIT on divergence), item-213 '
 'Stamp-2 semantics; the item-254 C10 cross-leg law')
FIXED_CAVEATS = {'development_data_disclosure': 'the candidate pair (item-215) and the SEC '
                                'features (items 231-232 forensics) were '
                                'developed against the BANKED walks; the '
                                'fresh corpora are the DISJOINT '
                                'adjudication (the design intent of S-A); '
                                'the disclosure rides every verdict -- the '
                                'record never claims amnesia',
 'fixed_fixtures_line': 'the same 10 loop fixtures ride every leg '
                        '(instrument built-ins): the fresh test is of the '
                        'negative population + the operating point; the '
                        'positives are FIXED -- loop-catch coverage is '
                        'measured, never guaranteed (the sheet SS3.4)',
 'fresh_census_line': 'the fresh corpora carry their OWN censuses (the '
                      'sheet SS1.8): EOS@step0 docs censused AT READOUT, '
                      'measured never named, every receipt carried; the '
                      '35-doc named class is banked history'}
FIXED_PCV_NOTE = ("presented, never adjudicated; the owner's stamps decide; theta wiring is "
 'its own pre-registration (theta [REDACTED_PER_PUBLICATION_POLICY] unmoved, D-theta); the D-FW6 '
 'second stage follows per its own sequencing')

# =========================================================================
# PART 3: the fixed export blocks, the families F1-F9, and main().
# =========================================================================

CHECKS = []


def check(fam, name, ok, detail=""):
    ok = bool(ok)
    CHECKS.append((fam, name, ok, detail))
    print(f"  [{fam}] {'PASS' if ok else 'FAIL'} -- {name}"
          + (f"  [{detail}]" if (detail and not ok) else ""))
    return ok


def fam_head(fam, title):
    print("\n" + "=" * 78)
    print(f"=== FAMILY {fam}: {title} ===")


def full_exp(caches, tag):
    """recompute_world + the FIXED pinned blocks = the complete export."""
    exp = recompute_world(caches, tag)
    for k in FIXED_TOP:
        exp[k] = FIXED_TOP[k]
    exp["fixture_identity_receipt"]["rule"] = FIXED_FIR_RULE
    pcv = exp["presented_candidate_verdict"]
    pcv["caveats"] = FIXED_CAVEATS
    pcv["note"] = FIXED_PCV_NOTE
    return exp


def run_and_cmp(fam, wd, spec, tag, wname):
    """Build the world, run the REAL tool via its CLI, compare EXACT."""
    caches = build_world(wd, spec)
    out = os.path.join(wd, "export.json")
    p = run_tool(caches, out, tag)
    if not check(fam, f"{wname}: the tool runs clean (rc 0)",
                 p.returncode == 0,
                 p.stderr[-300:] if p.returncode != 0 else ""):
        return None
    with open(out) as f:
        got = json.load(f)
    exp = full_exp(caches, tag)
    errs = []
    cmp_tree(exp, got, "", errs)
    check(fam, f"{wname}: export == the independent recompute EXACT "
          f"(every field, every leg, every doc, order-exact)",
          not errs, f"{len(errs)} diff(s): " + "; ".join(errs[:5]))
    return got


# -------------------------------------------------------------------------
# F1: the clean four-leg V-PASS world.
# -------------------------------------------------------------------------
def fam_f1(tmp):
    fam_head("F1", "the clean four-leg V-PASS world: every exported "
                   "quantity EXACT vs the independent recompute")
    got = run_and_cmp("F1", os.path.join(tmp, "f1_vpass"), base_spec(),
                      "accept-f1-vpass", "the V-PASS world")
    if got is None:
        return None
    pcv = got["presented_candidate_verdict"]
    check("F1", "the candidate verdict is PASS_2SIGMA-ALL-FOUR-LEGS",
          pcv["verdict_presented"] == "PASS_2SIGMA-ALL-FOUR-LEGS",
          pcv["verdict_presented"])
    for leg in LEGS:
        check("F1", f"leg {leg} types PASS_2SIGMA",
              got["legs"][leg]["verdict"]["typing_presented"]
              == "PASS_2SIGMA",
              got["legs"][leg]["verdict"]["typing_presented"])
        check("F1", f"leg {leg}: loop population 8 live / 2 inert",
              got["legs"][leg]["loop_population"]["n_live"] == 8
              and got["legs"][leg]["loop_population"]["n_inert"] == 2)
    for leg, exp_n in EXPECTED_FRESH_CENSUS.items():
        cen = got["legs"][leg]["census"]
        check("F1", f"leg {leg}: measured census {exp_n} == the pin",
              cen["measured_eos_step0"] == exp_n,
              f"measured {cen['measured_eos_step0']}")
    check("F1", "the one empty-form record is excluded, never pooled",
          len(got["empty_form_records_excluded"]) == 1
          and got["empty_form_records_excluded"][0]["doc_id"]
          == "empty-form-1")
    fir = got["fixture_identity_receipt"]
    check("F1", "the fixture-identity receipt: 10 loop fixtures, "
          "byte-identical across all four caches",
          fir["n_loop_fixtures"] == 10
          and fir["copies_byte_identical"] is True)
    gsm = got["legs"]["gsmrw17"]
    check("F1", "the closed-form constant-PR doc 39 is the one fired "
          "clean doc on gsmrw17",
          [v["doc_id"] for v in gsm["held_out"]["fired_docs"]] == [39])
    return got


# -------------------------------------------------------------------------
# F2: the arming law.
# -------------------------------------------------------------------------
def fam_f2(got):
    fam_head("F2", "the arming law: mbpprw17 is F-ONLY -- D == z_F "
                   "exactly; the loops' huge z_C ignored, never fires")
    mb = got["legs"]["mbpprw17"]
    check("F2", "mbpprw17 armed_sides == ['F']",
          mb["armed_sides"] == ["F"], str(mb["armed_sides"]))
    views = mb["populations"]["loops_live"]
    check("F2", "every live loop view on mbpprw17: D == z_F EXACTLY "
          "(the unarmed Side C never contributes)",
          all(v["D"] == v["z_F"] for v in views))
    check("F2", "the loops' Side-C signal runs large (z_C >= 2 on "
          "every loop) yet is IGNORED on this F-only leg -- D == z_F "
          "everywhere, the honest cost owned in the sheet SS1.2",
          all(v["z_C"] >= 2.0 for v in views)
          and all(v["z_C"] != v["z_F"] for v in views))
    check("F2", "the forensics block carries all 8 loops via zF "
          "(0 via zC)",
          mb["forensics"]["how"]["loop_carried_via_zF"] == 8
          and mb["forensics"]["how"]["loop_carried_via_zC"] == 0)
    for leg in ("gsmrw17", "prose17p-rw17", "p2corpus-rw17"):
        views = got["legs"][leg]["populations"]["loops_live"]
        check("F2", f"leg {leg} (C+F): every loop D == max(z_C, z_F)",
              all(v["D"] == max(v["z_C"], v["z_F"]) for v in views))


# -------------------------------------------------------------------------
# F3: the level-set receipts.
# -------------------------------------------------------------------------
def fam_f3(got):
    fam_head("F3", "the level-set receipts self-consistent on all "
                   "four legs")
    for leg in LEGS:
        lb = got["legs"][leg]
        ls = lb["level_set_receipt"]
        ok = (ls["ok"] is True
              and ls["calib_fires"] <= ls["ceiling"]
              and ls["ceiling"] == math.ceil(R_ALPHA * ls["n_calib"])
              and ls["n_calib"] == lb["parity"]["n_even_calibration"])
        check("F3", f"leg {leg}: calib fires {ls['calib_fires']}/"
              f"{ls['n_calib']} <= ceiling {ls['ceiling']} "
              f"(= ceil(0.05 * n_calib)); the ok flag honest", ok)


# -------------------------------------------------------------------------
# F4: the SEC identities.
# -------------------------------------------------------------------------
def fam_f4(got):
    fam_head("F4", "the SEC identities: band sweep monotone, R <= N, "
                   "frac == N/n; the closed-form doc's flat bands")
    factors = [f"{f:.2f}" for f in R_SEC_SWEEP]
    n_views = 0
    all_ok = True
    n_fired = 0
    for leg in LEGS:
        lb = got["legs"][leg]
        views = list(lb["populations"]["loops_live"]) \
            + list(lb["held_out"]["fired_docs"])
        n_fired += len(lb["held_out"]["fired_docs"])
        for v in views:
            sweep = v.get("sec1_band_sweep")
            if not sweep:
                all_ok = False
                continue
            n_views += 1
            prev_n = prev_r = None
            for f in factors:
                b = sweep[f]
                if not (b["R_band"] <= b["N_band"]):
                    all_ok = False
                if prev_n is not None and b["N_band"] > prev_n:
                    all_ok = False
                if prev_r is not None and b["R_band"] > prev_r:
                    all_ok = False
                if abs(b["frac"]
                       - b["N_band"] / v["n_prsig_steps"]) > 1e-9:
                    all_ok = False
                prev_n, prev_r = b["N_band"], b["R_band"]
    check("F4", f"every profiled view ({n_views} = 4 legs x 8 live "
          f"loops + {n_fired} fired docs): R_band <= N_band, the sweep "
          f"monotone non-increasing in the factor, frac == N_band / "
          f"n_prsig_steps",
          all_ok and n_views == 32 + n_fired)
    cf = [v for v in got["legs"]["gsmrw17"]["held_out"]["fired_docs"]
          if v["doc_id"] == CF_DOC_ID]
    ok = len(cf) == 1
    if ok:
        v = cf[0]
        for f in factors:
            b = v["sec1_band_sweep"][f]
            ok = ok and b["N_band"] == v["n_prsig_steps"] \
                and b["R_band"] == v["n_prsig_steps"] \
                and abs(b["frac"] - 1.0) < 1e-12
        ok = ok and v["n_prsig_steps"] == 40 \
            and v["sec2_ceiling_pos"] == 0 \
            and v["sec2_ceiling_pos_frac"] == 0.0
    check("F4", "the closed-form constant-PR doc (gsmrw17 doc 39): "
          "N_band == R_band == n_prsig_steps == 40 at EVERY sweep "
          "factor (frac 1.0) and ceiling_pos_frac == 0.0 (the argmax "
          "lands on the first step)", ok)


# -------------------------------------------------------------------------
# F5: every hard exit fires loud.
# -------------------------------------------------------------------------
def clone_world(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return [os.path.join(dst, f"cache_{l}.jsonl") for l in LEGS]


def edit_cache(path, fn):
    recs = [json.loads(s) for s in open(path).read().splitlines()
            if s.strip()]
    recs = fn(recs)
    with open(path, "w") as f:
        for r in recs:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def expect_die(fam, name, caches, substr, fixture_mode=True):
    out = os.path.join(os.path.dirname(caches[0]), "die_out.json")
    p = run_tool(caches, out, "accept-f5", fixture_mode=fixture_mode)
    ok = (p.returncode != 0 and "HARD EXIT" in p.stderr
          and substr in p.stderr)
    check(fam, name, ok,
          f"rc={p.returncode}; stderr tail: ...{p.stderr[-220:]}"
          if not ok else "")


def fam_f5(tmp):
    fam_head("F5", "every hard exit fires loud, naming the defect "
                   "(fail-loud, never a silent repair)")
    base = os.path.join(tmp, "f5_base")
    build_world(base, base_spec())

    def case(name, mutate, substr):
        key = name.replace(" ", "_").replace("/", "_")[:48]
        dst = os.path.join(tmp, "f5_" + key)
        caches = clone_world(base, dst)
        mutate(dst, caches)
        expect_die("F5", name, caches, substr)

    def m_trunc(dst, caches):
        with open(caches[0], "a") as f:
            f.write('{"key": "gsmrw17:bad", "leg"\n')
    case("a truncated/malformed JSON record line is a NAMED hard exit",
         m_trunc, "truncated/malformed JSON record")

    def m_premise(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "mbpprw17" and r["n_gen_steps"] == 0:
                    r["n_content_steps"] = 1
            return recs
        edit_cache(caches[1], fn)
    case("a census premise violation (n_gen_steps=0 with a "
         "materialized generation) is a hard exit",
         m_premise, "CENSUS PREMISE VIOLATED")

    def m_nonint(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 5:
                    r["doc_id"] = "str-five"
                    r["key"] = "gsmrw17:str-five"
            return recs
        edit_cache(caches[0], fn)
    case("a non-integer corpus doc_id is a hard exit (the parity "
         "split needs int doc_ids)", m_nonint, "is not an integer")

    dst = os.path.join(tmp, "f5_dup_leg")
    caches = clone_world(base, dst)
    expect_die("F5", "the same cache passed twice (a duplicated leg) "
               "is a hard exit",
               [caches[0], caches[0], caches[1], caches[2]],
               "MORE THAN ONE cache")
    expect_die("F5", "a three-cache run (a missing leg) is a hard "
               "exit", caches[:3], "missing leg")

    def m_oldleg(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 5:
                    r["leg"] = "gsm8k"
                    r["key"] = "gsm8k:5"
            return recs
        edit_cache(caches[0], fn)
    case("an old-corpus leg record (gsm8k) is a hard exit (the four "
         "fresh legs are the population)", m_oldleg, "unrecognized leg")

    dst = os.path.join(tmp, "f5_realpin")
    caches = clone_world(base, dst)
    expect_die("F5", "real mode (no --fixture-mode) enforces the SS4 "
               "SHA pins: a mismatched cache dies at the first pin",
               caches, "SS4 pinned checksum line of record",
               fixture_mode=False)

    def m_dupkey(dst, caches):
        def fn(recs):
            dup = [r for r in recs
                   if r.get("leg") == "gsmrw17"
                   and r.get("doc_id") == 5][0]
            return recs + [dup]
        edit_cache(caches[0], fn)
    case("a duplicate (leg, doc_id) record key is a hard exit (never "
         "a silent double population)", m_dupkey, "duplicate record key")

    def m_absent(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 2:
                    r["steps"]["PR"] = [None] * len(r["steps"]["t"])
            return recs
        edit_cache(caches[0], fn)
    case("an absent consumed statistic (all-None PR on a clean doc) "
         "is a hard exit, never a silent repair",
         m_absent, "absent statistic")

    pattern = [0.30 + 0.001 * i for i in range(40)]

    def m_degen(dst, caches):
        def fn(recs):
            for r in recs:
                if (r.get("leg") == "gsmrw17"
                        and isinstance(r.get("doc_id"), int)
                        and r["doc_id"] % 2 == 0):
                    r["steps"]["PR"] = list(pattern)
            return recs
        edit_cache(caches[0], fn)
    case("a degenerate calibration half (zero spread on maxPRsig via "
         "an identical MULTI-VALUED PR pattern, not a scalar) is a "
         "hard exit", m_degen, "DEGENERATE")

    def m_firdiv(dst, caches):
        def fn(recs):
            for r in recs:
                if (r.get("leg") == "loop"
                        and r["doc_id"] == "loop-seeded-affirm"):
                    r["steps"]["PR"] = list(r["steps"]["PR"])
                    r["steps"]["PR"][0] += 0.001
            return recs
        edit_cache(caches[3], fn)
    case("a divergent loop-fixture copy (one cache's copy mutated) is "
         "a hard exit", m_firdiv, "differs between cache")

    def m_partial(dst, caches):
        def fn(recs):
            return [r for r in recs if not (
                r.get("leg") == "loop"
                and r["doc_id"] in ("loop-seeded-affirm",
                                   "loop-seeded-chant"))]
        edit_cache(caches[3], fn)
    case("a partial fixture overlap (two fixtures dropped from one "
         "cache) is a hard exit", m_partial,
         "DIFFERENT loop-fixture sets")

    def m_ragged(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 5:
                    r["steps"]["E"] = r["steps"]["E"][:-1]
            return recs
        edit_cache(caches[0], fn)
    case("ragged step columns are a hard exit", m_ragged,
         "ragged step columns")

    def m_ngen(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 5:
                    r["n_gen_steps"] -= 1
            return recs
        edit_cache(caches[0], fn)
    case("n_gen_steps != len(steps.t) is a hard exit", m_ngen,
         "n_gen_steps")

    def m_key(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 5:
                    r["key"] = "gsmrw17:999"
            return recs
        edit_cache(caches[0], fn)
    case("key != leg:doc_id is a hard exit (the join fields must "
         "agree)", m_key, "join fields must agree")

    def m_nonobj(dst, caches):
        with open(caches[0], "a") as f:
            f.write("42\n")
    case("a non-object record line is a hard exit", m_nonobj,
         "record is not an object")

    def m_steps(dst, caches):
        def fn(recs):
            for r in recs:
                if r.get("leg") == "gsmrw17" and r.get("doc_id") == 5:
                    r["steps"] = []
            return recs
        edit_cache(caches[0], fn)
    case("'steps' not an object is a hard exit", m_steps,
         "'steps' is not an object")

    # the fixture-mode census-pin ECHO (the real-mode twin sits behind
    # the SS4 SHA pins -- the honest-unreachability note; the real-mode
    # SHA-pin exit itself is tested above)
    dst = os.path.join(tmp, "f5_census_echo")
    spec = base_spec()
    spec["gsmrw17"]["census_ids"] = [1]
    caches = build_world(dst, spec)
    out = os.path.join(dst, "export.json")
    p = run_tool(caches, out, "accept-f5-census-echo")
    ok = (p.returncode == 0 and "CENSUS PIN ECHO" in p.stdout
          and "measured fresh census is 1" in p.stdout)
    if ok:
        g = json.load(open(out))
        ok = (g["legs"]["gsmrw17"]["census"]["measured_eos_step0"] == 1
              and g["legs"]["gsmrw17"]["census"]["receipts"][0]
              ["doc_id"] == 1
              and g["legs"]["gsmrw17"]["census"]["expected_of_record"]
              == 0)
    check("F5", "the fixture-mode census-pin ECHO: a census drift in "
          "fixture mode is rc 0 + the loud echo line (measured 1 != "
          "the pin 0), the receipts carried in the export", ok,
          f"rc={p.returncode}" if not ok else "")


# -------------------------------------------------------------------------
# F6: the verdict worlds.
# -------------------------------------------------------------------------
def fam_f6(tmp):
    fam_head("F6", "the verdict worlds (frozen knobs, bisected against "
                   "the real tool)")

    got = run_and_cmp("F6", os.path.join(tmp, "f6_vnear"),
                      base_spec(pr_lo_gsm=KNOB_V_NEAR),
                      "accept-f6-vnear", "V-NEAR")
    if got:
        pcv = got["presented_candidate_verdict"]
        gap = got["legs"]["gsmrw17"]["separation_context"][
            "sigma_gap_on_D"]
        check("F6", "V-NEAR: candidate PASS_2SIGMA-ALL-FOUR-LEGS; gsm "
              "PASS_2SIGMA with the gap in [2.0, 2.02); the near-bar "
              "FLAG rides",
              pcv["verdict_presented"] == "PASS_2SIGMA-ALL-FOUR-LEGS"
              and pcv["near_bar_legs"] == ["gsmrw17"]
              and pcv["jitter_legs"] == []
              and got["legs"]["gsmrw17"]["verdict"]["typing_presented"]
              == "PASS_2SIGMA"
              and 2.0 <= gap < 2.0 + R_JITTER_BAND, f"gap {gap}")

    got = run_and_cmp("F6", os.path.join(tmp, "f6_vjitter"),
                      base_spec(pr_lo_gsm=KNOB_V_JITTER),
                      "accept-f6-vjitter", "V-JITTER")
    if got:
        pcv = got["presented_candidate_verdict"]
        gap = got["legs"]["gsmrw17"]["separation_context"][
            "sigma_gap_on_D"]
        check("F6", "V-JITTER: candidate INCONCLUSIVE-FROM-JITTER; gsm "
              "INCONCLUSIVE-FROM-JITTER with the gap in [1.98, 2.0)",
              pcv["verdict_presented"] == "INCONCLUSIVE-FROM-JITTER"
              and pcv["jitter_legs"] == ["gsmrw17"]
              and got["legs"]["gsmrw17"]["verdict"]["typing_presented"]
              == "INCONCLUSIVE-FROM-JITTER"
              and 2.0 - R_JITTER_BAND <= gap < 2.0, f"gap {gap}")

    got = run_and_cmp("F6", os.path.join(tmp, "f6_vfail"),
                      base_spec(pr_lo_gsm=KNOB_V_FAIL),
                      "accept-f6-vfail", "V-FAIL")
    if got:
        pcv = got["presented_candidate_verdict"]
        gap = got["legs"]["gsmrw17"]["separation_context"][
            "sigma_gap_on_D"]
        check("F6", "V-FAIL: candidate FAIL; gsm FAIL below the jitter "
              "band (the honest max-of-two headwind named)",
              pcv["verdict_presented"] == "FAIL"
              and pcv["failed_legs"] == ["gsmrw17"]
              and got["legs"]["gsmrw17"]["verdict"]["typing_presented"]
              == "FAIL"
              and gap < 2.0 - R_JITTER_BAND, f"gap {gap}")

    spec = base_spec()
    spec["gsmrw17"] = {"n_corpus": 8, "census_ids": [], "pr_lo": 2.00,
                       "s_lo": 0.50, "salt": 11, "closed_form": False,
                       "hot_odd": {}, "hot_even": {0: 1.5, 2: 1.6},
                       "empty_form": False}
    got = run_and_cmp("F6", os.path.join(tmp, "f6_vguard"), spec,
                      "accept-f6-vguard", "V-GUARD")
    if got:
        pcv = got["presented_candidate_verdict"]
        check("F6", "V-GUARD: candidate INCONCLUSIVE-POPULATION-GUARD "
              "with the guard on [gsmrw17] (a tiny leg: 4/4 halves) "
              "and 1 honest fire",
              pcv["verdict_presented"]
              == "INCONCLUSIVE-POPULATION-GUARD"
              and pcv["population_guard_legs"] == ["gsmrw17"]
              and got["legs"]["gsmrw17"]["held_out"]["fires"] == 1)

    spec = base_spec(pr_lo_gsm=2.60)
    spec["gsmrw17"]["hot_odd"] = {5: 1.8, 15: 1.9, 25: 2.0}
    spec["gsmrw17"]["hot_even"] = {}
    spec["gsmrw17"]["empty_form"] = False
    spec["prose17p-rw17"] = {"n_corpus": 8, "census_ids": [1, 3, 5],
                             "pr_lo": 1.60, "s_lo": 0.50, "salt": 33,
                             "closed_form": False, "hot_odd": {},
                             "hot_even": {}}
    got = run_and_cmp("F6", os.path.join(tmp, "f6_vkilled"), spec,
                      "accept-f6-vkilled", "V-KILLED")
    if got:
        pcv = got["presented_candidate_verdict"]
        gsm = got["legs"]["gsmrw17"]
        gap = gsm["separation_context"]["sigma_gap_on_D"]
        check("F6", "V-KILLED: the falsifier's teeth -- hot held-out "
              "docs fire 4 > ceil(0.05 * 20) = 1 with the gap STILL "
              ">= 2.0, so the candidate dies CANDIDATE-KILLED even "
              "though the bar passes",
              pcv["verdict_presented"]
              == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
              and pcv["over_budget_legs"] == ["gsmrw17"]
              and gsm["verdict"]["typing_presented"]
              == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
              and gsm["held_out"]["fires"] == 4
              and gsm["held_out"]["count_ceil"] == 1
              and gap >= 2.0, f"gap {gap}")
        check("F6", "V-KILLED: KILLED dominates a guard typing (the "
              "guard leg [prose17p-rw17] rides, the candidate is still "
              "KILLED -- the sheet SS1.8)",
              pcv["population_guard_legs"] == ["prose17p-rw17"]
              and pcv["verdict_presented"]
              == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET")


# -------------------------------------------------------------------------
# F7: port fidelity (the item-242 build of record).
# -------------------------------------------------------------------------
F7_17P = {
    "mu_C": 1.9637011149531287, "sd_C": 0.9228285440810102,
    "mu_F": 0.0511817860417068, "sd_F": 0.05952422633933064,
    "t_leg": 2.0360012403229493, "t_esc": 2.2990526665006126,
    "th_C": 2.1152856055953073, "th_F": 1.5571220729772066,
    "gap": 2.6528168437991675, "wilson": 0.4592312863618338,
    "auc": 0.9875,
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fam_f7(tmp):
    fam_head("F7", "port fidelity: the item-242 build of record "
                   "reproduced on the banked bytes, then replicated "
                   "through the NEW tool's own functions, EXACT")
    check("F7", "the old tool's SHA-256 == the banked pin",
          r_sha256_file(OLD_TOOL) == OLD_TOOL_SHA,
          r_sha256_file(OLD_TOOL))
    check("F7", "the banked R-BC1 smoke cache's SHA-256 == the pin",
          r_sha256_file(RBC1) == RBC1_SHA, r_sha256_file(RBC1))

    wd = os.path.join(tmp, "f7_old")
    os.makedirs(wd, exist_ok=True)
    out_old = os.path.join(wd, "old_export.json")
    p = run_tool([RBC1, FILLER_GSM, FILLER_HE, FILLER_P2], out_old,
                 "rw17-f7-port", fixture_mode=True, tool=OLD_TOOL)
    if not check("F7", "the OLD tool CLI runs clean on the banked "
                 "R-BC1 + the three fillers (fixture mode)",
                 p.returncode == 0, p.stderr[-300:]):
        return
    with open(out_old) as f:
        old = json.load(f)
    lg = old["legs"]["prose17p"]
    zb, th = lg["z_baselines"], lg["thresholds"]
    check("F7", "the old 17p leg: parity 10/10, catches 8/8 live "
          "loops at BOTH tiers, fires 2 (ids 13, 19), Wilson upper "
          "EXACT vs the banked run",
          lg["parity"]["n_even_calibration"] == 10
          and lg["parity"]["n_odd_held_out"] == 10
          and lg["loop_catches"]["n_live"] == 8
          and lg["loop_catches"]["at_t_leg"] == 8
          and lg["loop_catches"]["at_t_esc"] == 8
          and lg["held_out"]["fires"] == 2
          and [v["doc_id"] for v in lg["held_out"]["fired_docs"]]
          == [13, 19]
          and lg["held_out"]["wilson_upper_95"] == F7_17P["wilson"])
    check("F7", "the old 17p sigma-gap == the banked run EXACT and "
          "round4 == the item-242 pin 2.6528",
          lg["separation_context"]["sigma_gap_on_D"] == F7_17P["gap"]
          and round(lg["separation_context"]["sigma_gap_on_D"], 4)
          == 2.6528)
    check("F7", "the old 17p AUC measures 0.9875 (round4) on the "
          "pinned bytes TODAY -- the item-242 LEDGER PROSE says 0.8750, "
          "a PROSE SLIP named here and at the banking item, never "
          "edited (the banked item-242 control console records PASS "
          "without the value)",
          round(lg["separation_context"]["auc_on_D"], 4)
          == F7_17P["auc"],
          str(lg["separation_context"]["auc_on_D"]))

    # ---- the NEW tool's own functions replicate the old pipeline ----
    NEW = load_module("rw17_new_tool", TOOL)
    recs = [json.loads(s) for s in open(RBC1).read().splitlines()
            if s.strip()]
    corpus = [r for r in recs
              if r.get("leg") == "prose17p" and r["n_gen_steps"] > 0]
    loops = sorted([r for r in recs if r.get("leg") == "loop"],
                   key=lambda r: str(r["doc_id"]))
    live = [d for d in loops if d["n_gen_steps"] >= 32]
    even = [d for d in corpus if d["doc_id"] % 2 == 0]
    odd = [d for d in corpus if d["doc_id"] % 2 == 1]
    check("F7", "the R-BC1 partition: 20 corpus (the named census ids "
          "91/108 absent from the smoke corpus -- keep 20), 10 loops, "
          "8 live / 2 inert, parity 10/10",
          len(corpus) == 20 and len(loops) == 10 and len(live) == 8
          and len(even) == 10 and len(odd) == 10)
    base = NEW.compute_baselines(even, "prose17p-rw17")
    for d in even + odd + live:
        v = NEW.derive_doc_stats(d, base)
        d["score"] = v["score"]
    mu_C, sd_C = NEW.mean_std([d["score"]["maxPRsig"] for d in even])
    mu_F, sd_F = NEW.mean_std([d["score"]["minS"] for d in even])
    for d in even + odd + live:
        d["z_C"] = (d["score"]["maxPRsig"] - mu_C) / sd_C
        d["z_F"] = (d["score"]["minS"] - mu_F) / sd_F
        d["D"] = NEW.armed_D(d["z_C"], d["z_F"], "prose17p-rw17")
    calib = sorted(d["D"] for d in even)
    t_leg = NEW._quantile(calib, 1.0 - 0.05)
    t_esc = NEW._quantile(calib, 1.0 - 0.01)
    th_C = NEW._quantile(sorted(d["z_C"] for d in even), 0.975)
    th_F = NEW._quantile(sorted(d["z_F"] for d in even), 0.975)
    fires = sorted([d for d in odd if d["D"] >= t_leg],
                  key=lambda d: -d["D"])
    rep = {
        "mu_C": mu_C, "sd_C": sd_C, "mu_F": mu_F, "sd_F": sd_F,
        "t_leg": t_leg, "t_esc": t_esc, "th_C": th_C, "th_F": th_F,
        "gap": NEW.sigma_gap([d["D"] for d in live],
                             [d["D"] for d in odd]),
        "auc": NEW.auc_pos_neg([d["D"] for d in live],
                               [d["D"] for d in odd]),
        "wilson": NEW.wilson_upper(len(fires), len(odd)),
    }
    diffs = [k for k in F7_17P if rep[k] != F7_17P[k]]
    check("F7", "the NEW tool's own functions, replicating the old 17p "
          "pipeline over the R-BC1 records, reproduce EVERY banked "
          "value EXACTLY (mu/sd/t_leg/t_esc/th_C/th_F/gap/AUC/Wilson)",
          not diffs, f"diff keys: {diffs}")
    check("F7", "the replication's fires are ids [13, 19] (order "
          "exact) and all 8 live loops catch at t_leg",
          [d["doc_id"] for d in fires] == [13, 19]
          and sum(1 for d in live if d["D"] >= t_leg) == 8)

    # ---- the pure-function battery: old vs new ----
    OLD = load_module("rw17_old_tool", OLD_TOOL)
    bat = []
    for vals in ([1.0, 2.0, 3.0], [0.5], [-1.5, 2.5, 3.5, 10.0],
                 [7.25, 7.25, 7.25, 0.0]):
        bat.append(("mean_std", vals,
                    OLD.mean_std(vals) == NEW.mean_std(vals)))
    sv = sorted([0.1, 0.5, 0.5, 0.9, 1.0, 2.0, 3.3, 7.7])
    for q in (0.0, 0.01, 0.25, 0.5, 0.9, 0.95, 0.975, 0.99, 1.0):
        bat.append((f"_quantile(q={q})", sv,
                    OLD._quantile(sv, q) == NEW._quantile(sv, q)))
    bat.append(("_quantile single", [4.2],
                OLD._quantile([4.2], 0.95)
                == NEW._quantile([4.2], 0.95)))
    bat.append(("_quantile empty", [],
                OLD._quantile([], 0.95) is None
                and NEW._quantile([], 0.95) is None))
    for pos, neg in (((1.0, 2.0, 3.0), (0.1, 0.2)),
                     ((1.0, 1.0, 2.0), (1.0, 2.0, 2.0)),
                     ((), (1.0, 2.0)),
                     ((1.0,), ()),
                     ((5.0, 5.0), (5.0, 5.0))):
        bat.append(("sigma_gap", (pos, neg),
                    OLD.sigma_gap(list(pos), list(neg))
                    == NEW.sigma_gap(list(pos), list(neg))))
        bat.append(("auc", (pos, neg),
                    OLD.auc_pos_neg(list(pos), list(neg))
                    == NEW.auc_pos_neg(list(pos), list(neg))))
    for k, n in ((0, 0), (0, 10), (3, 10), (10, 10), (5, 100)):
        bat.append((f"wilson({k},{n})", (k, n),
                    OLD.wilson_upper(k, n) == NEW.wilson_upper(k, n)))
    leg_map = (("gsm8k", "gsmrw17"), ("humaneval", "mbpprw17"),
               ("prose17p", "prose17p-rw17"),
               ("p2corpus", "p2corpus-rw17"))
    for zc, zf in ((1.0, 0.5), (-2.0, 3.0), (0.0, 0.0),
                   (5.5, -1.25)):
        for ol, nl in leg_map:
            bat.append((f"armed_D {ol}->{nl}", (zc, zf),
                        OLD.armed_D(zc, zf, ol)
                        == NEW.armed_D(zc, zf, nl)))
    consts = [
        ("ALPHA", OLD.ALPHA, NEW.ALPHA),
        ("ALPHA_ESC", OLD.ALPHA_ESC, NEW.ALPHA_ESC),
        ("CO_ELEV_Q", OLD.CO_ELEV_Q, NEW.CO_ELEV_Q),
        ("SEC_BAND_FACTOR", OLD.SEC_BAND_FACTOR,
         NEW.SEC_BAND_FACTOR),
        ("SEC_SWEEP", tuple(OLD.SEC_SWEEP), tuple(NEW.SEC_SWEEP)),
        ("SIDE_KEYS", tuple(OLD.SIDE_KEYS), tuple(NEW.SIDE_KEYS)),
        ("DEPTH_BUCKET", OLD.DEPTH_BUCKET, NEW.DEPTH_BUCKET),
        ("BASELINE_MIN_N", OLD.BASELINE_MIN_N, NEW.BASELINE_MIN_N),
        ("LOOP_INERT_MIN_STEPS", OLD.LOOP_INERT_MIN_STEPS,
         NEW.LOOP_INERT_MIN_STEPS),
        ("W_GRAM", OLD.W_GRAM, NEW.W_GRAM),
        ("REQUIRED_RECORD_FIELDS", tuple(OLD.REQUIRED_RECORD_FIELDS),
         tuple(NEW.REQUIRED_RECORD_FIELDS)),
        ("REQUIRED_STEP_FIELDS", tuple(OLD.REQUIRED_STEP_FIELDS),
         tuple(NEW.REQUIRED_STEP_FIELDS)),
    ]
    for cname, ov, nv in consts:
        bat.append((f"const {cname}", (ov, nv), ov == nv))
    bad = [b for b in bat if not b[2]]
    check("F7", f"the pure-function battery: {len(bat)} old-vs-new "
          f"comparisons (mean_std/_quantile/sigma_gap/auc/wilson/"
          f"armed_D under the leg mapping, the pinned constants, the "
          f"loader field tuples) -- all EXACT",
          not bad, f"{len(bad)} mismatch(es): "
          + "; ".join(f"{b[0]}({b[1]})" for b in bad[:6]))


# -------------------------------------------------------------------------
# F8: determinism.
# -------------------------------------------------------------------------
def fam_f8(tmp):
    fam_head("F8", "determinism: the same-path re-run is "
                   "byte-identical on BOTH the export and the console")
    wd = os.path.join(tmp, "f8_det")
    caches = build_world(wd, base_spec())
    out = os.path.join(wd, "export.json")
    p1 = run_tool(caches, out, "accept-f8")
    first_console = p1.stdout
    with open(out, "rb") as f:
        first_bytes = f.read()
    p2 = run_tool(caches, out, "accept-f8")
    with open(out, "rb") as f:
        second_bytes = f.read()
    check("F8", "both runs rc 0",
          p1.returncode == 0 and p2.returncode == 0)
    check("F8", "the same-path re-run export is byte-identical "
          "(no timestamps, no dict-order noise)",
          len(first_bytes) > 0 and first_bytes == second_bytes)
    check("F8", "the console output is byte-identical across the "
          "two runs", len(first_console) > 0
          and first_console == p2.stdout)


# -------------------------------------------------------------------------
# F9: the constants echo.
# -------------------------------------------------------------------------
def fam_f9(got):
    fam_head("F9", "the constants echo: the pinned sheet's constants, "
                   "the census pins, the SS4 pins, the caveats")
    c = got["construction"]
    check("F9", "alpha 0.05 / alpha_esc 0.01 / band 0.90 / sweep "
          "(0.80, 0.85, 0.90, 0.95) / co_elev 0.975 / pop guard 5 / "
          "jitter 0.02 -- all echo the pinned sheet",
          c["alpha"] == 0.05 and c["alpha_esc"] == 0.01
          and c["sec_band_factor"] == 0.90
          and c["sec_sweep"] == [0.80, 0.85, 0.90, 0.95]
          and c["co_elev_quantile"] == 0.975
          and c["pop_guard_min"] == 5 and c["jitter_band"] == 0.02)
    check("F9", "the arming table echoes (gsm CF, mbpp F, prose CF, "
          "p2 CF)",
          c["armed_sides"] == {leg: list(R_ARMED[leg]) for leg in LEGS})
    check("F9", "the expected fresh censuses of record echo "
          "(0 / 1 / 3 / 95)",
          got["census_law"]["expected_fresh_census"]
          == dict(EXPECTED_FRESH_CENSUS))
    pins_ok = len(got["inputs"]["walks"]) == 4
    for w in got["inputs"]["walks"]:
        leg = w["pin"]["leg"]
        name, sha = PINNED_CACHE_SHA[leg]
        pins_ok = pins_ok and w["pin"]["pinned_file"] == name \
            and w["pin"]["pinned_sha256"] == sha \
            and w["pin"]["match"] is False
    check("F9", "the four SS4 cache pin lines echo with match=False "
          "(fixture mode echoes, never enforces)", pins_ok)
    check("F9", "fixture_mode True; the mode line; the tag",
          got["fixture_mode"] is True and got["mode"] == MODE_TYPE
          and got["tag"] == "accept-f1-vpass")
    check("F9", "the pinned sheet's SHA rides the prereg block",
          PREREG_SHA in got["prereg"])
    check("F9", "the theta note: theta [REDACTED_PER_PUBLICATION_POLICY] unmoved, nothing wired",
          "theta [REDACTED_PER_PUBLICATION_POLICY] unmoved" in got["theta_note"])
    check("F9", "the RW-14 rider: no label joins, routed to its own "
          "pre-registration",
          "RW-14" in got["rw14_rider"]
          and "no label joins" in got["rw14_rider"])
    check("F9", "the three pinned caveat lines ride the verdict",
          got["presented_candidate_verdict"]["caveats"] == FIXED_CAVEATS
          and len(FIXED_CAVEATS) == 3)
    check("F9", "the tool's own SHA rides the export",
          got["tool_sha256"] == r_sha256_file(TOOL))
    check("F9", "the old-corpus anchor reference names the item-243 "
          "banked baseline table (the delta reading happens at the "
          "reading, never inside this tool)",
          "triadic_rw17_sec_baseline_rw17-sec-baseline.json"
          in got["old_corpus_anchor_reference"])
    check("F9", "the fixture-identity receipt names its law (the "
          "item-213 Stamp-2 semantics; the item-254 C10 cross-leg law)",
          got["fixture_identity_receipt"]["rule"] == FIXED_FIR_RULE)


# -------------------------------------------------------------------------
# main.
# -------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("=== THE RW-17 READOUT TOOL ACCEPTANCE RUN (the item-242 "
          "pattern) ===")
    print("  tool under test: triadic_rw17_readout.py")
    print("  (the pinned sheet SS4.5 readout tool amendment; the "
          "pinned sheet")
    print("   rw17-fresh-corpus-preregistration.md, SHA-256")
    print(f"   {PREREG_SHA})")
    print("  LAW: every family drives the REAL TOOL via its CLI and")
    print("  compares EXACT against THIS RUNNER'S OWN independent")
    print("  recomputation; fix-the-fixture-or-the-builder, never")
    print("  the tool's record.")
    scratch = os.path.join(HERE, ".scratch")
    os.makedirs(scratch, exist_ok=True)
    tmp = os.path.join(scratch, "rw17_readout_accept_run")
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    print(f"  (run dir: {tmp})")
    f1 = fam_f1(tmp)
    if f1 is not None:
        fam_f2(f1)
        fam_f3(f1)
        fam_f4(f1)
    fam_f5(tmp)
    fam_f6(tmp)
    fam_f7(tmp)
    fam_f8(tmp)
    if f1 is not None:
        fam_f9(f1)
    print("\n" + "=" * 78)
    fams = []
    for fam, _name, _ok, _detail in CHECKS:
        if fam not in fams:
            fams.append(fam)
    n_fail = sum(1 for c in CHECKS if not c[2])
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
    print("\n  Fix-the-fixture-or-the-builder, never the tool's record.")
    print("  theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved,")
    print("  or adjudicated; findings presented, never adjudicated --")
    print("  the owner's stamps decide.")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

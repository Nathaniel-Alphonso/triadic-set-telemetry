#!/usr/bin/env python3
"""rw17_sec_acceptance_run.py -- the acceptance suite for the RW-17
SEC BASELINE PASS tool (triadic_rw17_sec_baseline.py; the pinned sheet
rw17-fresh-corpus-preregistration.md, ledger items 237/240/241).

The suite: (1) synthetic hand-auditable four-leg caches built
deterministically, the tool run in fixture-mode, and EVERY exported
quantity checked EXACT against this runner's INDEPENDENT
recomputation; (2) the arming law proven on the F-only leg; (3) the
level-set receipt; (4) SEC identities + a closed-form doc; (5) ALL the
hard exits firing loud; (6) determinism byte-identical; (7) the pinned
construction constants echoed exactly.

Fix-the-fixture-or-the-runner never the tool: any catch here is
resolved on the fixture/runner side, per the standing builder-side fix
accounting discipline. theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds
set, moved, or adjudicated.
"""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_rw17_sec_baseline.py")
PASSES, FAILS = [], []


def check(name, cond, detail=""):
    if cond:
        PASSES.append(name)
        print(f"PASS {name}")
    else:
        FAILS.append(name)
        print(f"FAIL {name} -- {detail}")


def xe(name, a, b):
    check(name, a == b, f"got {a!r} expected {b!r}")


# =========================================
# Deterministic synthetic builders (zero randomness, zero selection
# freedom; every value a fixed arithmetic function of (doc, step)).
# =========================================
def pv(doc_id, step, salt):
    d = (sum(ord(c) for c in doc_id) if isinstance(doc_id, str)
         else doc_id)
    h = (d * 2654435761 + step * 40503 + salt * 97) % 4294967296
    return (h % 100000) / 100000.0


def make_doc(leg, doc_id, n_steps, pr=None, s=None):
    t = list(range(n_steps))
    prs = pr if pr is not None else \
        [0.45 + 0.4 * pv(doc_id, i, 1) for i in t]
    ss = s if s is not None else \
        [0.50 + 0.20 * pv(doc_id, i, 2) for i in t]
    return {
        "key": f"{leg}:{doc_id}", "leg": leg, "doc_id": doc_id,
        "bos": True, "instrument": "v32.2.1-SYNTH", "prompt_len": 9,
        "stop_reason": "stop:fewshot-boundary", "n_gen_steps": n_steps,
        "n_content_steps": n_steps, "walk_ids": [13] * n_steps,
        "steps": {
            "t": t, "id": [13] * n_steps,
            "E": [1.0 + pv(doc_id, i, 3) for i in t],
            "rho": [0.5 + 0.3 * pv(doc_id, i, 4) for i in t],
            "s": ss, "f": [pv(doc_id, i, 6) for i in t],
            "layer": [0] * n_steps, "H": [1.0 + pv(doc_id, i, 5) for i in t],
            "PR": prs, "a": [pv(doc_id, i, 7) for i in t],
            "rsize": [pv(doc_id, i, 8) for i in t],
            "dead5": [0.0] * n_steps, "dead4": [0.0] * n_steps,
            "dead3": [0.0] * n_steps, "dead_share": [0.0] * n_steps},
        "commits": [i for i in t if i % 4 == 0],
        "hidden_n": 2, "hidden_dim": 4, "hidden_b64": "AAAA"}


def spike(pr_list, step, val=0.005):
    pr_list[step] = val


def s_hot_list(n_steps, val=0.97):
    return [val] * n_steps


def loop_pr(n_steps, run_lo=5, run_hi=None, val=0.005):
    run_hi = run_hi if run_hi is not None else n_steps - 5
    return [val if run_lo <= i <= run_hi
            else 0.45 + 0.4 * pv(f"L{i}", i, 1) for i in range(n_steps)]


LIVE_IDS = [f"loop-live-{k}" for k in range(1, 9)]
INERT_IDS = [f"loop-inert-{k}" for k in range(1, 3)]
CENSUSED_P2 = [3, 7, 8, 13, 16, 17, 18, 23, 27, 28, 33, 37, 38, 43, 48,
               52, 53, 58, 62, 63, 66, 74, 75, 76, 78, 85, 86, 93, 113,
               118, 128, 133, 165]


def build_leg(leg, n_corpus, hot_pr=(), hot_s=(), n_steps=40,
              censused=(), const_pr_doc=None):
    docs = []
    for did in range(n_corpus):
        if did in censused:
            d = make_doc(leg, did, 0)      # the empty-generation record
            d["stop_reason"] = "eos"
            docs.append(d)
            continue
        pr = None
        s = None
        if const_pr_doc is not None and did == const_pr_doc:
            pr = [0.42] * n_steps          # the closed-form SEC doc
        elif did in hot_pr:
            pr = [0.45 + 0.4 * pv(did, i, 1) for i in range(n_steps)]
            spike(pr, 20)
        elif did in hot_s:
            s = s_hot_list(n_steps)
        docs.append(make_doc(leg, did, n_steps, pr=pr, s=s))
    for lid in LIVE_IDS:
        docs.append(make_doc("loop", lid, n_steps,
                             pr=loop_pr(n_steps), s=s_hot_list(n_steps)))
    for iid in INERT_IDS:
        docs.append(make_doc("loop", iid, 10,
                             pr=loop_pr(10, run_lo=2, run_hi=4),
                             s=s_hot_list(10)))
    return docs


def write_cache(path, docs):
    with open(path, "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")


def build_world(tmp):
    legs = {
        "gsm8k": build_leg("gsm8k", 1100,
                           hot_pr=(79, 213, 613, 657, 1097, 441, 999),
                           hot_s=(101, 303, 505), const_pr_doc=200),
        "humaneval": build_leg("humaneval", 40, hot_pr=(21,),
                               hot_s=(9, 33)),
        "prose17p": build_leg("prose17p", 40, hot_s=(15, 27)),
        "p2corpus": build_leg("p2corpus", 170, hot_pr=(91, 137),
                              hot_s=(55,), censused=set(CENSUSED_P2)),
    }
    paths = {}
    for leg, docs in legs.items():
        p = os.path.join(tmp, f"synth_{leg}.jsonl")
        write_cache(p, docs)
        paths[leg] = p
    return paths


# =========================================
# The INDEPENDENT recomputation (mirrors the pinned definitions; a
# defect in EITHER side shows as an EXACT-mismatch catch).
# =========================================
DEPTH_BUCKET, BASELINE_MIN_N, W_GRAM = 16, 30, 8
ALPHA, ALPHA_ESC, CO_ELEV_Q = 0.05, 0.01, 0.975
SWEEP = (0.80, 0.85, 0.90, 0.95)
ARMED = {"gsm8k": ("C", "F"), "humaneval": ("F",),
         "prose17p": ("C", "F"), "p2corpus": ("C", "F")}
NAMED = {"gsm8k": [613, 657, 1097], "humaneval": [],
         "prose17p": [95], "p2corpus": [91, 137]}


def mstd(vals):
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / max(len(vals) - 1, 1)) ** 0.5
    return m, sd


def q_lin(vals, q):
    vals = sorted(vals)
    n = len(vals)
    if n == 0:
        return None
    if n == 1 or q <= 0.0:
        return float(vals[0])
    if q >= 1.0:
        return float(vals[-1])
    p = q * (n - 1)
    lo = int(math.floor(p))
    frac = p - lo
    if frac <= 0.0:
        return float(vals[lo])
    if lo + 1 >= n:
        return float(vals[-1])
    return float(vals[lo]) + frac * (float(vals[lo + 1])
                                     - float(vals[lo]))


def wilson(k, n, z=1.645):
    if n == 0:
        return None
    ph = k / n
    den = 1.0 + z * z / n
    ctr = ph + z * z / (2 * n)
    rad = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (ctr + rad) / den


def baselines(corpus_docs):
    buck = {"E": {}, "rho": {}, "s": {}}
    pooled = {"E": [], "rho": [], "s": []}
    lay, lay_pool = {"H": {}, "PR": {}}, {"H": [], "PR": []}
    for d in corpus_docs:
        st = d["steps"]
        for key in ("E", "rho", "s"):
            for t, v in zip(st["t"], st[key]):
                if v is None:
                    continue
                b = t // DEPTH_BUCKET
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
        gm, gsd = mstd(pooled[key])
        for b, vals in sorted(buck[key].items()):
            base["bucket"][(key, b)] = (mstd(vals)
                                        if len(vals) >= BASELINE_MIN_N
                                        else (gm, gsd))
    for key in ("H", "PR"):
        gm, gsd = mstd(lay_pool[key])
        for l, vals in sorted(lay[key].items()):
            base["layer"][(key, l)] = (mstd(vals)
                                       if len(vals) >= BASELINE_MIN_N
                                       else (gm, gsd))
    return base


def derive(d, base):
    st = d["steps"]
    n = len(st["t"])
    ebar = []
    for i in range(n):
        lo = max(0, i - W_GRAM + 1)
        vals = [st["E"][j] for j in range(lo, i + 1)
                if st["E"][j] is not None]
        ebar.append(sum(vals) / len(vals) if vals else None)
    c_l, d_l, sexc_l, hs, ps = [], [], [], [], []
    for i in range(n):
        t = st["t"][i]
        bE = base["bucket"].get(("E", t // DEPTH_BUCKET))
        bR = base["bucket"].get(("rho", t // DEPTH_BUCKET))
        bS = base["bucket"].get(("s", t // DEPTH_BUCKET))
        c_l.append(1.0 - ebar[i] / bE[0]
                   if (bE and ebar[i] and bE[0] > 1e-9) else None)
        d_l.append(1.0 - st["rho"][i] / bR[0]
                   if (bR and st["rho"][i] is not None
                       and bR[0] > 1e-9) else None)
        sexc_l.append((bS[0] - st["s"][i]) / bS[1]
                      if (bS and st["s"][i] is not None
                          and bS[1] > 1e-9) else None)
    for l, hv, pvv in zip(st["layer"], st["H"], st["PR"]):
        bH = base["layer"].get(("H", l))
        bP = base["layer"].get(("PR", l))
        hs.append(abs(hv - bH[0]) / bH[1]
                  if (bH and hv is not None and bH[1] > 1e-9) else None)
        ps.append((bP[0] - pvv) / bP[1]
                  if (bP and pvv is not None and bP[1] > 1e-9) else None)

    def mx(v):
        vs = [x for x in v if x is not None]
        return max(vs) if vs else None

    def mn(v):
        vs = [x for x in v if x is not None]
        return min(vs) if vs else None

    return {"PRsig": ps, "Ebar": ebar}, {
        "maxPRsig": mx(ps), "minS": mn(st["s"])}


def sec_profile(d, prsig, max_prsig):
    idx = [i for i, v in enumerate(prsig) if v is not None]
    if not idx or max_prsig is None:
        return None
    argmax_i = max(idx, key=lambda i: (prsig[i], -i))
    ceiling_pos = d["steps"]["t"][argmax_i]
    denom = max(d["n_gen_steps"] - 1, 1)
    bands = {}
    for f in SWEEP:
        thr = f * max_prsig
        run = best = n_band = 0
        for i in idx:
            if prsig[i] >= thr:
                n_band += 1
                run += 1
                if run > best:
                    best = run
            else:
                run = 0
        bands[f"{f:.2f}"] = {"N_band": n_band, "R_band": best,
                             "frac": n_band / len(idx)}
    return {"maxPRsig": max_prsig, "n_prsig_steps": len(idx),
            "ceiling_pos": ceiling_pos,
            "ceiling_pos_frac": ceiling_pos / denom, "band": bands}


def recompute_leg(leg, corpus, loop_docs):
    censused = set(CENSUSED_P2) if leg == "p2corpus" else \
        ({91, 108} if leg == "prose17p" else set())
    by_id = {d["doc_id"]: d for d in corpus}
    census_out = []
    for did in sorted(censused):
        if did not in by_id:
            census_out.append({"doc_id": did, "present": False})
            continue
        census_out.append({"doc_id": did, "present": True})
        del by_id[did]
    clean = sorted(by_id.values(), key=lambda d: str(d["doc_id"]))
    even = [d for d in clean if d["doc_id"] % 2 == 0]
    odd = [d for d in clean if d["doc_id"] % 2 == 1]
    base = baselines(even)
    for grp in (even, odd):
        for d in grp:
            d["_der"], d["_score"] = derive(d, base)
    live = sorted([d for d in loop_docs if d["n_gen_steps"] >= 32],
                  key=lambda d: str(d["doc_id"]))
    inert = [d for d in loop_docs if d["n_gen_steps"] < 32]
    for d in live:
        d["_der"], d["_score"] = derive(d, base)
    mu_C, sd_C = mstd([d["_score"]["maxPRsig"] for d in even])
    mu_F, sd_F = mstd([d["_score"]["minS"] for d in even])
    for d in even + odd + live:
        d["z_C"] = (d["_score"]["maxPRsig"] - mu_C) / sd_C
        d["z_F"] = (d["_score"]["minS"] - mu_F) / sd_F
        sides = ARMED[leg]
        d["D"] = max([v for v, s in ((d["z_C"], "C"),
                                    (d["z_F"], "F"))
                      if s in sides])
    t_leg = q_lin([d["D"] for d in even], 1 - ALPHA)
    t_esc = q_lin([d["D"] for d in even], 1 - ALPHA_ESC)
    th_C = q_lin([d["z_C"] for d in even], CO_ELEV_Q)
    th_F = q_lin([d["z_F"] for d in even], CO_ELEV_Q)
    calib_fires = sum(1 for d in even if d["D"] >= t_leg)
    calib_ceil = math.ceil(ALPHA * len(even))
    calib_esc = sum(1 for d in even if d["D"] >= t_esc)
    fires = sorted([d for d in odd if d["D"] >= t_leg],
                   key=lambda d: -d["D"])
    esc_fires = sum(1 for d in odd if d["D"] >= t_esc)
    fired_views = []
    for d in fires:
        p = sec_profile(d, d["_der"]["PRsig"], d["_score"]["maxPRsig"])
        b = p["band"]["0.90"]
        co = True
        if "C" in ARMED[leg]:
            co = co and d["z_C"] >= th_C
        if "F" in ARMED[leg]:
            co = co and d["z_F"] >= th_F
        fired_views.append({
            "doc_id": d["doc_id"], "half": "held-out",
            "z_C": d["z_C"], "z_F": d["z_F"],
            "D": d["D"], "maxPRsig": d["_score"]["maxPRsig"],
            "minS": d["_score"]["minS"],
            "sec1_N_band": b["N_band"], "sec1_R_band": b["R_band"],
            "sec1_frac": b["frac"], "sec1_band_sweep": p["band"],
            "sec2_ceiling_pos": p["ceiling_pos"],
            "sec2_ceiling_pos_frac": p["ceiling_pos_frac"],
            "n_prsig_steps": p["n_prsig_steps"],
            "co_elevated": co, "escalation": d["D"] >= t_esc})
    easiest = min(d["D"] for d in live)
    n_overlap = sum(1 for d in odd if d["D"] >= easiest)
    pos, neg = [d["D"] for d in live], [d["D"] for d in odd]
    gap = sigma_gap(pos, neg)
    auc = auc_pn(pos, neg)
    return {
        "parity": (len(even), len(odd)),
        "n_live": len(live), "n_inert": len(inert),
        "census_receipts": census_out,
        "z": (mu_C, sd_C, mu_F, sd_F),
        "t": (t_leg, t_esc, th_C, th_F),
        "level_set": (calib_fires, calib_ceil, calib_esc),
        "held_out": (len(odd), len(fires),
                     len(fires) / len(odd) if odd else 0.0,
                     math.ceil(ALPHA * len(odd)) if odd else 0,
                     wilson(len(fires), len(odd)), esc_fires),
        "fired_views": fired_views,
        "overlap": (easiest, n_overlap,
                    n_overlap / len(odd) if odd else None),
        "catches": (sum(1 for d in live if d["D"] >= t_leg),
                    sum(1 for d in live if d["D"] >= t_esc)),
        "gap_auc": (gap, auc),
        "live": live, "odd": odd, "even": even,
    }


def sigma_gap(pos, neg):
    if not pos or not neg:
        return None
    mp, mn_ = sum(pos) / len(pos), sum(neg) / len(neg)
    sp = (sum((v - mp) ** 2 for v in pos) / max(len(pos) - 1, 1)) ** 0.5
    sn = (sum((v - mn_) ** 2 for v in neg) / max(len(neg) - 1, 1)) ** 0.5
    pooled = math.sqrt((sp * sp + sn * sn) / 2.0)
    return (mp - mn_) / pooled if pooled > 0 else 0.0


def auc_pn(pos, neg):
    if not pos or not neg:
        return None
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
    s = sum(r for r, (_, p) in zip(ranks, vals) if p == 1)
    return (s - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def run_tool(args, expect_fail=False, tag="acc"):
    r = subprocess.run([sys.executable, TOOL] + args,
                       capture_output=True, text=True)
    if expect_fail:
        return r.returncode != 0, r.stderr + r.stdout
    return r.returncode == 0, r.stdout


# =========================================
# The suite.
# =========================================
def main():
    print("=" * 78)
    print("=== RW-17 SEC BASELINE PASS -- ACCEPTANCE RUN ===")
    tmp = tempfile.mkdtemp(prefix="rw17_sec_acc_")
    try:
        paths = build_world(tmp)

        # ---- F6 determinism (run twice first; SAME --out path so the
        # tool's honest export-path echo cannot mask the check) ----
        out1 = os.path.join(tmp, "run1.json")
        ok1, log1 = run_tool(["--fixture-mode", "--cache", paths["gsm8k"],
                              "--cache", paths["humaneval"],
                              "--cache", paths["prose17p"],
                              "--cache", paths["p2corpus"],
                              "--tag", "acc", "--out", out1])
        with open(out1, "rb") as f:
            b1 = f.read()
        ok2, log2 = run_tool(["--fixture-mode", "--cache", paths["gsm8k"],
                              "--cache", paths["humaneval"],
                              "--cache", paths["prose17p"],
                              "--cache", paths["p2corpus"],
                              "--tag", "acc", "--out", out1])
        with open(out1, "rb") as f:
            b2 = f.read()
        check("F6a clean run exits 0", ok1, log1[-400:] if not ok1 else "")
        check("F6b rerun exits 0", ok2, "")
        check("F6c determinism byte-identical export", b1 == b2, "")
        check("F6d determinism byte-identical console", log1 == log2, "")
        with open(out1) as f:
            exp = json.load(f)

        # ---- F7 the pinned construction constants echo ----
        c = exp["construction"]
        xe("F7a alpha echoes the pinned 0.05", c["alpha"], 0.05)
        xe("F7b alpha_esc echoes the pinned 0.01", c["alpha_esc"], 0.01)
        xe("F7c sec_band_factor echoes the pinned 0.90",
           c["sec_band_factor"], 0.90)
        xe("F7d the sweep echoes",
           c["sec_sweep"], [0.80, 0.85, 0.90, 0.95])
        xe("F7e the arming table echoes the pinned sheet",
           c["armed_sides"],
           {"gsm8k": ["C", "F"], "humaneval": ["F"],
            "prose17p": ["C", "F"], "p2corpus": ["C", "F"]})
        check("F7f the prereg SHA rides",
              exp["prereg"].startswith(
                  "rw17-fresh-corpus-preregistration.md") and
              "64f87bc01906ee6f5a50d38c2b09c09aa9f089f14803cfae"
              "9e8a07dd0af74075" in exp["prereg"], "")
        check("F7g the development-data typing rides",
              "NON-GATING" in exp["mode"] and
              "NEVER ENTERS ADJUDICATION" in exp["mode"], "")

        # ---- F1 every quantity EXACT vs independent recomputation ----
        for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus"):
            with open(paths[leg]) as f:
                recs = [json.loads(x) for x in f if x.strip()]
            corpus = [d for d in recs if d["leg"] == leg]
            loops = [d for d in recs if d["leg"] == "loop"]
            r = recompute_leg(leg, corpus, loops)
            lb = exp["legs"][leg]
            p = f"F1[{leg}]"
            xe(p + " parity even", lb["parity"]["n_even_calibration"],
               r["parity"][0])
            xe(p + " parity odd", lb["parity"]["n_odd_held_out"],
               r["parity"][1])
            xe(p + " live positives", lb["loop_catches"]["n_live"],
               r["n_live"])
            xe(p + " inert positives", len(lb["populations"]["loops_live"]),
               r["n_live"])  # inert excluded from the profiled population
            xe(p + " z mu_C", lb["z_baselines"]["mu_C"], r["z"][0])
            xe(p + " z sd_C", lb["z_baselines"]["sd_C"], r["z"][1])
            xe(p + " z mu_F", lb["z_baselines"]["mu_F"], r["z"][2])
            xe(p + " z sd_F", lb["z_baselines"]["sd_F"], r["z"][3])
            xe(p + " t_leg", lb["thresholds"]["t_leg"], r["t"][0])
            xe(p + " t_esc", lb["thresholds"]["t_esc"], r["t"][1])
            xe(p + " th_C_coelev", lb["thresholds"]["th_C_coelev"],
               r["t"][2])
            xe(p + " th_F_coelev", lb["thresholds"]["th_F_coelev"],
               r["t"][3])
            xe(p + " level-set calib fires",
               lb["level_set_receipt"]["calib_fires"], r["level_set"][0])
            xe(p + " level-set ceiling", lb["level_set_receipt"]["ceiling"],
               r["level_set"][1])
            xe(p + " calib escalation", lb["calibration_escalation_fires"],
               r["level_set"][2])
            ho = lb["held_out"]
            xe(p + " held-out n", ho["n"], r["held_out"][0])
            xe(p + " held-out fires", ho["fires"], r["held_out"][1])
            xe(p + " held-out rate", ho["rate"], r["held_out"][2])
            xe(p + " held-out count-ceil", ho["count_ceil"],
               r["held_out"][3])
            xe(p + " held-out wilson", ho["wilson_upper_95"],
               r["held_out"][4])
            xe(p + " held-out escalation", ho["escalation_fires"],
               r["held_out"][5])
            check(p + " fired docs list EXACT (order + every field)",
                  ho["fired_docs"] == r["fired_views"],
                  f"tool {len(ho['fired_docs'])} vs runner "
                  f"{len(r['fired_views'])}")
            xe(p + " overlap easiest-loop D",
               lb["loop_floor_overlap_line"]["easiest_loop_D"],
               r["overlap"][0])
            xe(p + " overlap n", lb["loop_floor_overlap_line"]
               ["n_clean_at_or_above"], r["overlap"][1])
            xe(p + " overlap rate",
               lb["loop_floor_overlap_line"]["rate"], r["overlap"][2])
            xe(p + " catches at t_leg", lb["loop_catches"]["at_t_leg"],
               r["catches"][0])
            xe(p + " catches at t_esc", lb["loop_catches"]["at_t_esc"],
               r["catches"][1])
            xe(p + " gap", lb["separation_context"]["sigma_gap_on_D"],
               r["gap_auc"][0])
            xe(p + " auc", lb["separation_context"]["auc_on_D"],
               r["gap_auc"][1])
            # the loop-fixture views EXACT
            tool_loops = lb["populations"]["loops_live"]
            runner_loops = []
            for d in r["live"]:
                pr_ = sec_profile(d, d["_der"]["PRsig"],
                                  d["_score"]["maxPRsig"])
                b = pr_["band"]["0.90"]
                runner_loops.append({
                    "doc_id": d["doc_id"], "half": "loop-fixture",
                    "z_C": d["z_C"], "z_F": d["z_F"], "D": d["D"],
                    "maxPRsig": d["_score"]["maxPRsig"],
                    "minS": d["_score"]["minS"],
                    "sec1_N_band": b["N_band"],
                    "sec1_R_band": b["R_band"],
                    "sec1_frac": b["frac"],
                    "sec1_band_sweep": pr_["band"],
                    "sec2_ceiling_pos": pr_["ceiling_pos"],
                    "sec2_ceiling_pos_frac": pr_["ceiling_pos_frac"],
                    "n_prsig_steps": pr_["n_prsig_steps"]})
            check(p + " loop views EXACT",
                  tool_loops == runner_loops, "")
            # the named-beta receipts
            for nv, did in zip(lb["populations"]["named_beta_docs"],
                              NAMED[leg]):
                if did in {d["doc_id"] for d in r["odd"] + r["even"]}:
                    hit = next(d for d in r["odd"] + r["even"]
                               if d["doc_id"] == did)
                    pr_ = sec_profile(hit, hit["_der"]["PRsig"],
                                      hit["_score"]["maxPRsig"])
                    b = pr_["band"]["0.90"]
                    exp_view = {
                        "doc_id": did,
                        "half": ("held-out" if did % 2 else
                                 "calibration"),
                        "z_C": hit["z_C"], "z_F": hit["z_F"],
                        "D": hit["D"],
                        "maxPRsig": hit["_score"]["maxPRsig"],
                        "minS": hit["_score"]["minS"],
                        "sec1_N_band": b["N_band"],
                        "sec1_R_band": b["R_band"],
                        "sec1_frac": b["frac"],
                        "sec1_band_sweep": pr_["band"],
                        "sec2_ceiling_pos": pr_["ceiling_pos"],
                        "sec2_ceiling_pos_frac":
                            pr_["ceiling_pos_frac"],
                        "n_prsig_steps": pr_["n_prsig_steps"],
                        "present": True,
                        "fired_at_t_leg": hit["D"] >= r["t"][0]}
                    check(p + f" named-beta doc {did} view EXACT",
                          nv == exp_view,
                          f"tool {nv} vs runner {exp_view}")
                else:
                    check(p + f" named-beta doc {did} absent receipt",
                          nv == {"doc_id": did, "present": False,
                                 "note": "not in this run's cache "
                                         "(nothing to profile)"},
                          str(nv))
            # the population summaries
            s = lb["populations"]["summaries_at_0.90"]

            def summ(views):
                if not views:
                    return {"n": 0}
                nb = [v["sec1_N_band"] for v in views
                      if v["sec1_N_band"] is not None]
                rb = [v["sec1_R_band"] for v in views
                      if v["sec1_R_band"] is not None]
                cp = [v["sec2_ceiling_pos_frac"] for v in views
                      if v["sec2_ceiling_pos_frac"] is not None]
                dd = [v["D"] for v in views]
                return {"n": len(views),
                        "mean_N_band": sum(nb) / len(nb) if nb else None,
                        "mean_R_band": sum(rb) / len(rb) if rb else None,
                        "mean_ceiling_pos_frac": (sum(cp) / len(cp)
                                                  if cp else None),
                        "mean_D": sum(dd) / len(dd) if dd else None,
                        "max_D": max(dd) if dd else None}

            xe(p + " summary loops", s["loops_live"], summ(runner_loops))
            xe(p + " summary fired", s["held_out_clean_fired"],
               summ(r["fired_views"]))
            nonf = []
            for d in r["odd"]:
                if d["D"] < r["t"][0]:
                    pr_ = sec_profile(d, d["_der"]["PRsig"],
                                      d["_score"]["maxPRsig"])
                    b = pr_["band"]["0.90"]
                    nonf.append({"sec1_N_band": b["N_band"],
                                 "sec1_R_band": b["R_band"],
                                 "sec2_ceiling_pos_frac":
                                     pr_["ceiling_pos_frac"],
                                 "D": d["D"]})
            xe(p + " summary non-fired", s["held_out_clean_nonfired"],
               summ(nonf))
            calib = []
            for d in r["even"]:
                pr_ = sec_profile(d, d["_der"]["PRsig"],
                                  d["_score"]["maxPRsig"])
                b = pr_["band"]["0.90"]
                calib.append({"sec1_N_band": b["N_band"],
                              "sec1_R_band": b["R_band"],
                              "sec2_ceiling_pos_frac":
                                  pr_["ceiling_pos_frac"],
                              "D": d["D"]})
            xe(p + " summary calib", s["calibration_half_clean"],
               summ(calib))
            # census receipts
            cr = [{"doc_id": c["doc_id"], "present": c["present"]}
                  for c in lb["census"]["receipts"]]
            xe(p + " census receipts", cr, r["census_receipts"])

        # ---- F2 the arming law (the he leg is F-ONLY) ----
        he = exp["legs"]["humaneval"]
        with open(paths["humaneval"]) as f:
            recs = [json.loads(x) for x in f if x.strip()]
        corpus = [d for d in recs if d["leg"] == "humaneval"]
        r_he = recompute_leg("humaneval", corpus,
                             [d for d in recs if d["leg"] == "loop"])
        fired_ids = {v["doc_id"] for v in he["held_out"]["fired_docs"]}
        # doc 21: the extreme Side-C spike, ordinary s -> NOT fired
        d21 = next(d for d in r_he["odd"] if d["doc_id"] == 21)
        check("F2a the unarmed-side doc (21) carries D == z_F exactly",
              d21["D"] == d21["z_F"], "")
        check("F2b the unarmed-side doc (21) is NOT fired despite "
              "huge z_C",
              d21["z_C"] > he["thresholds"]["t_leg"]
              and 21 not in fired_ids,
              f"z_C {d21['z_C']} fired={21 in fired_ids}")
        # every he doc: D == z_F (the F-only arming)
        check("F2c every he-leg doc carries D == z_F",
              all(v["D"] == v["z_F"]
                  for v in he["populations"]["loops_live"]) and
              all(v["D"] == v["z_F"] for v in he["held_out"]
                  ["fired_docs"]), "")
        # the s-hot docs DID fire via Side F
        check("F2d the F-hot docs fire (9, 33)",
              {9, 33} <= fired_ids, str(fired_ids))

        # ---- F3 the level-set receipt on all legs ----
        for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus"):
            lsr = exp["legs"][leg]["level_set_receipt"]
            check(f"F3[{leg}] level-set ok (calib fires "
                  f"{lsr['calib_fires']} <= ceil {lsr['ceiling']})",
                  lsr["ok"] is True and
                  lsr["calib_fires"] <= lsr["ceiling"], "")

        # ---- F4 SEC identities + the closed-form doc ----
        bad = []
        for leg in ("gsm8k", "humaneval", "prose17p", "p2corpus"):
            lb = exp["legs"][leg]
            views = (lb["populations"]["loops_live"]
                     + [v for v in lb["populations"]["named_beta_docs"]
                        if v.get("present")]
                     + lb["held_out"]["fired_docs"])
            for v in views:
                sw = v["sec1_band_sweep"]
                ns = [sw[k]["N_band"] for k in
                      ("0.80", "0.85", "0.90", "0.95")]
                if not (ns[0] >= ns[1] >= ns[2] >= ns[3]):
                    bad.append((leg, v["doc_id"], "N_band monotone"))
                if not all(sw[k]["R_band"] <= sw[k]["N_band"]
                           for k in sw):
                    bad.append((leg, v["doc_id"], "R_band <= N_band"))
                if not all(sw[k]["frac"] ==
                           sw[k]["N_band"] / v["n_prsig_steps"]
                           for k in sw):
                    bad.append((leg, v["doc_id"], "frac identity"))
        check("F4a SEC identities hold on every profiled doc "
              "(monotone sweep, R<=N, frac)",
              not bad, str(bad[:3]))
        gsm = exp["legs"]["gsm8k"]
        # the closed-form doc: gsm doc 200 (even, calib half) carries a
        # CONSTANT PR series -> constant PRsig -> every band = all
        # steps. Reach it through the calibration summary is not
        # possible per-doc, so recompute directly:
        with open(paths["gsm8k"]) as f:
            recs_g = [json.loads(x) for x in f if x.strip()]
        corpus_g = [d for d in recs_g if d["leg"] == "gsm8k"]
        r_g = recompute_leg("gsm8k", corpus_g,
                            [d for d in recs_g if d["leg"] == "loop"])
        d200 = next(d for d in r_g["even"] if d["doc_id"] == 200)
        pr_ = sec_profile(d200, d200["_der"]["PRsig"],
                          d200["_score"]["maxPRsig"])
        check("F4b closed-form doc (constant PRsig): N_band == "
              "n_prsig_steps at every sweep factor",
              all(pr_["band"][k]["N_band"] == pr_["n_prsig_steps"]
                  for k in pr_["band"]), str(pr_))
        check("F4c closed-form doc: R_band == n_prsig_steps",
              all(pr_["band"][k]["R_band"] == pr_["n_prsig_steps"]
                  for k in pr_["band"]), str(pr_))
        check("F4d closed-form doc: ceiling_pos_frac == 0.0 "
              "(constant series, first max)",
              pr_["ceiling_pos_frac"] == 0.0, str(pr_))

        # ---- F5 the hard exits fire loud ----
        # (a) truncated JSON
        bad_path = os.path.join(tmp, "trunc.jsonl")
        with open(bad_path, "w") as f:
            f.write(json.dumps(make_doc("gsm8k", 0, 40))[:200] + "\n")
        ok, log = run_tool(["--fixture-mode", "--cache", bad_path,
                            "--cache", paths["humaneval"],
                            "--cache", paths["prose17p"],
                            "--cache", paths["p2corpus"],
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5a truncated JSON -> hard exit naming the file",
              ok and "truncated" in log, log[-200:])
        # (b) census premise violation: p2 doc 3 made LIVE
        p2_docs = [json.loads(x) for x in open(paths["p2corpus"])]
        for d in p2_docs:
            if d["leg"] == "p2corpus" and d["doc_id"] == 3:
                d.update(make_doc("p2corpus", 3, 40))
        badp2 = os.path.join(tmp, "p2_live3.jsonl")
        write_cache(badp2, p2_docs)
        ok, log = run_tool(["--fixture-mode", "--cache", paths["gsm8k"],
                            "--cache", paths["humaneval"],
                            "--cache", paths["prose17p"],
                            "--cache", badp2,
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5b census premise violation -> hard exit naming "
              "leg+doc",
              ok and "CENSUS PREMISE VIOLATED" in log and
              "p2corpus doc 3" in log, log[-200:])
        # (c) non-int doc_id
        g = [json.loads(x) for x in open(paths["gsm8k"])]
        g.append(make_doc("gsm8k", "s-401", 40))
        badg = os.path.join(tmp, "gsm_str.jsonl")
        write_cache(badg, g)
        ok, log = run_tool(["--fixture-mode", "--cache", badg,
                            "--cache", paths["humaneval"],
                            "--cache", paths["prose17p"],
                            "--cache", paths["p2corpus"],
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5c non-int doc_id -> parity hard exit naming it",
              ok and "s-401" in log and "not an integer" in log,
              log[-200:])
        # (d) duplicate leg
        ok, log = run_tool(["--fixture-mode", "--cache", paths["gsm8k"],
                            "--cache", paths["gsm8k"],
                            "--cache", paths["prose17p"],
                            "--cache", paths["p2corpus"],
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5d duplicate leg -> hard exit",
              ok and "MORE THAN ONE cache" in log, log[-200:])
        # (e) missing leg
        ok, log = run_tool(["--fixture-mode", "--cache", paths["gsm8k"],
                            "--cache", paths["humaneval"],
                            "--cache", paths["prose17p"],
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5e missing leg -> hard exit",
              ok and "missing leg p2corpus" in log, log[-200:])
        # (f) pin enforcement in REAL mode (synthetic p2 cache)
        ok, log = run_tool(["--cache", paths["gsm8k"],
                            "--cache", paths["humaneval"],
                            "--cache", paths["prose17p"],
                            "--cache", paths["p2corpus"],
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5f real-mode pin law -> hard exit on the unpinned "
              "p2 cache",
              ok and "pinned console line" in log, log[-200:])
        # (g) absent statistic: an all-None PR doc out of census
        h = [json.loads(x) for x in open(paths["humaneval"])]
        # a doc id NOT already in the he world (0-39): id 41 is virgin
        # (the first draft collided with existing doc 39 and the tool
        # correctly died on duplicate doc_id instead)
        nd = make_doc("humaneval", 41, 40)
        nd["steps"]["PR"] = [None] * 40
        h.append(nd)
        badh = os.path.join(tmp, "he_nonepr.jsonl")
        write_cache(badh, h)
        ok, log = run_tool(["--fixture-mode", "--cache", paths["gsm8k"],
                            "--cache", badh,
                            "--cache", paths["prose17p"],
                            "--cache", paths["p2corpus"],
                            "--out", os.path.join(tmp, "x.json")],
                           expect_fail=True)
        check("F5g absent statistic -> column-guard hard exit naming "
              "leg+doc+key",
              ok and "absent statistic 'maxPRsig'" in log and
              "doc 41" in log, log[-200:])

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + "=" * 78)
    print(f"ACCEPTANCE: {len(PASSES)} PASS / {len(FAILS)} FAIL")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        sys.exit(1)
    print("theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, "
          "or adjudicated.")
    sys.exit(0)


if __name__ == "__main__":
    main()

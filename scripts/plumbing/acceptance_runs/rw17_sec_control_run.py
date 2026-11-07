#!/usr/bin/env python3
"""rw17_sec_control_run.py -- the REAL-CACHE control for
triadic_rw17_sec_baseline.py (the RW-17 SEC baseline pass's control
of record; the RW-16 control precedent, item 214).

TWO receipts:

  (a) THE REAL-BYTES EXACT RECOMPUTATION on the 17p smoke leg: the
      tool runs --fixture-mode on the BANKED R-BC1 smoke cache (the
      item-214 control input, SHA-pinned) as the prose17p leg + three
      honest synthetic filler legs (the tool's four-leg law requires
      them; the fillers carry no loop fixtures and no census members,
      honestly labeled SYNTH). The 17p leg's EVERY quantity -- the
      census not-present receipts (91/108), the parity split 10/10,
      the loop population 8 live / 2 inert FROM THE SMOKE CACHE'S OWN
      RECORDS (live iff n_gen_steps >= 32), the calibration-half-only
      baselines, z, D over armed sides, t_leg/t_esc/th_C/th_F, the
      level-set receipt, the held-out block (fires/rate/ceil/Wilson/
      escalation), the fired docs list (every field, every SEC view),
      the loop-floor overlap line, the catches, gap/AUC, the loop
      views, the named-beta doc-95 absent receipt, the population
      summaries, and the item-199 pin echo (match False -- the smoke
      cache is not the pinned fresh cache) -- is asserted EXACT
      against an INDEPENDENT recomputation (the control's own
      arithmetic, never the tool's functions; the machinery the
      acceptance suite already validated EXACT against the tool on
      the synthetic world).

  (b) THE STRUCTURAL RECEIPTS for the synthetic filler legs (honestly
      labeled, never a real population): each leg present, its parity
      halves 24/24, its census receipts all not-present, its loop
      population EMPTY (n_live 0 -- no fixtures carried, never
      fabricated), its overlap line and separation context honest
      nulls, its level-set receipt self-consistent.

  (c) DETERMINISM: a fresh re-run of the full CLI (same inputs, same
      --out path) byte-identical on the export.

Zero-GPU, read-only, offline. Fix-the-fixture-or-the-builder, never
the tool. FAIL LOUD.
"""

import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_rw17_sec_baseline.py")
SMOKE_CACHE = os.path.join(HERE, "rw16_control_fixtures",
                           "triadic_t2_cache_t2-prose17p-smoke_"
                           "bfloat16_bos.jsonl")
SMOKE_SHA = ("a2f57964232d981db586b007ddbf642b7d6fe7224f65f3499ce"
             "9ecacb2e763e1")   # the item-214 banked pin
PIN_PROSE = ("586048c6d1be3d58c2d4ff6555a377a57d385b1173b2737ee6f"
             "b4771452b9138")   # the item-199 prose17p console pin
PIN_P2 = ("b9d0219576b0519018ec1343371209f93919b078ea7aa482a7d8f"
          "6346eba78a8")        # the item-199 p2corpus console pin
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


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# =========================================
# The honest synthetic filler builders (the same deterministic
# arithmetic as the acceptance suite's world; zero randomness, zero
# selection freedom). Doc ids chosen to avoid every census member
# (the p2 census ids 3..165 would collide with ids 0-47).
# =========================================
def pv(doc_id, step, salt):
    d = (sum(ord(c) for c in doc_id) if isinstance(doc_id, str)
         else doc_id)
    h = (d * 2654435761 + step * 40503 + salt * 97) % 4294967296
    return (h % 100000) / 100000.0


def make_doc(leg, doc_id, n_steps):
    t = list(range(n_steps))
    return {
        "key": f"{leg}:{doc_id}", "leg": leg, "doc_id": doc_id,
        "bos": True, "instrument": "v32.2.1-SYNTH-FILLER",
        "prompt_len": 9, "stop_reason": "stop:fewshot-boundary",
        "n_gen_steps": n_steps, "n_content_steps": n_steps,
        "walk_ids": [13] * n_steps,
        "steps": {
            "t": t, "id": [13] * n_steps,
            "E": [1.0 + pv(doc_id, i, 3) for i in t],
            "rho": [0.5 + 0.3 * pv(doc_id, i, 4) for i in t],
            "s": [0.50 + 0.20 * pv(doc_id, i, 2) for i in t],
            "f": [pv(doc_id, i, 6) for i in t], "layer": [0] * n_steps,
            "H": [1.0 + pv(doc_id, i, 5) for i in t],
            "PR": [0.45 + 0.4 * pv(doc_id, i, 1) for i in t],
            "a": [pv(doc_id, i, 7) for i in t],
            "rsize": [pv(doc_id, i, 8) for i in t],
            "dead5": [0.0] * n_steps, "dead4": [0.0] * n_steps,
            "dead3": [0.0] * n_steps, "dead_share": [0.0] * n_steps},
        "commits": [i for i in t if i % 4 == 0],
        "hidden_n": 2, "hidden_dim": 4, "hidden_b64": "AAAA"}


def build_filler(path, leg, first_id, n_docs=48, n_steps=40):
    docs = [make_doc(leg, did, n_steps) for did in
            range(first_id, first_id + n_docs)]
    with open(path, "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")
    return docs


def run_tool(args):
    r = subprocess.run([sys.executable, TOOL] + args,
                       capture_output=True, text=True)
    return (r.returncode == 0,
            r.returncode == 0 and r.stdout or (r.stderr + r.stdout))


# =========================================
# The INDEPENDENT recomputation (the acceptance suite's machinery,
# validated EXACT against the tool on the synthetic world; never the
# tool's own functions).
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
    return float(vals[lo]) + frac * (float(vals[lo + 1]) - float(vals[lo]))


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
    ps = []
    for l, pvv in zip(st["layer"], st["PR"]):
        bP = base["layer"].get(("PR", l))
        ps.append((bP[0] - pvv) / bP[1]
                  if (bP and pvv is not None and bP[1] > 1e-9) else None)

    def mx(v):
        vs = [x for x in v if x is not None]
        return max(vs) if vs else None

    def mn(v):
        vs = [x for x in v if x is not None]
        return min(vs) if vs else None

    return {"PRsig": ps}, {"maxPRsig": mx(ps), "minS": mn(st["s"])}


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


def recompute_leg(leg, corpus, loop_docs, censused):
    by_id = {d["doc_id"]: d for d in corpus}
    census_out = []
    for did in censused:
        if did not in by_id:
            census_out.append({"doc_id": did, "present": False,
                               "note": ("not in this run's cache "
                                        "(nothing to exclude)")})
            continue
        del by_id[did]
        census_out.append({"doc_id": did, "present": True})
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
        d["D"] = max([v for v, s in ((d["z_C"], "C"), (d["z_F"], "F"))
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
            "z_C": d["z_C"], "z_F": d["z_F"], "D": d["D"],
            "maxPRsig": d["_score"]["maxPRsig"],
            "minS": d["_score"]["minS"],
            "sec1_N_band": b["N_band"], "sec1_R_band": b["R_band"],
            "sec1_frac": b["frac"], "sec1_band_sweep": p["band"],
            "sec2_ceiling_pos": p["ceiling_pos"],
            "sec2_ceiling_pos_frac": p["ceiling_pos_frac"],
            "n_prsig_steps": p["n_prsig_steps"],
            "co_elevated": co, "escalation": d["D"] >= t_esc})
    easiest = min(d["D"] for d in live) if live else None
    n_overlap = (sum(1 for d in odd if d["D"] >= easiest)
                 if easiest is not None else None)
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
                    n_overlap / len(odd) if n_overlap is not None
                    and odd else None),
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
        for k in range(i, j + 1):
            ranks.append((vals[k][1], r))
        i = j + 1
    rp = sum(r for lab, r in ranks if lab == 1)
    n1, n0 = len(pos), len(neg)
    return (rp - n1 * (n1 + 1) / 2.0) / (n1 * n0)


def loop_view(d):
    pr_ = sec_profile(d, d["_der"]["PRsig"], d["_score"]["maxPRsig"])
    b = pr_["band"]["0.90"]
    return {
        "doc_id": d["doc_id"], "half": "loop-fixture",
        "z_C": d["z_C"], "z_F": d["z_F"], "D": d["D"],
        "maxPRsig": d["_score"]["maxPRsig"], "minS": d["_score"]["minS"],
        "sec1_N_band": b["N_band"], "sec1_R_band": b["R_band"],
        "sec1_frac": b["frac"], "sec1_band_sweep": pr_["band"],
        "sec2_ceiling_pos": pr_["ceiling_pos"],
        "sec2_ceiling_pos_frac": pr_["ceiling_pos_frac"],
        "n_prsig_steps": pr_["n_prsig_steps"]}


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


# =========================================
# The control.
# =========================================
def main():
    print("=" * 78)
    print("=== RW-17 SEC BASELINE PASS TOOL -- REAL-CACHE CONTROL RUN "
          "(zero-GPU, read-only) ===")

    # ---- input receipt ----
    c_sha = sha256_file(SMOKE_CACHE)
    check("input receipt: the smoke cache SHA == the item-214 banked pin",
          c_sha == SMOKE_SHA, c_sha)

    tmp = tempfile.mkdtemp(prefix="rw17_sec_ctrl_")
    try:
        fg = os.path.join(tmp, "filler_gsm8k.jsonl")
        fh = os.path.join(tmp, "filler_humaneval.jsonl")
        fp = os.path.join(tmp, "filler_p2corpus.jsonl")
        build_filler(fg, "gsm8k", 0)          # census: none
        build_filler(fh, "humaneval", 0)      # census: none
        build_filler(fp, "p2corpus", 200)     # census ids 3..165 avoided
        out = os.path.join(tmp, "control.json")

        # ---- (a) the full CLI: real 17p leg + honest fillers ----
        ok, log = run_tool(["--fixture-mode", "--cache", SMOKE_CACHE,
                            "--cache", fg, "--cache", fh,
                            "--cache", fp, "--tag", "rw17-sec-control",
                            "--out", out])
        check("(a) the control CLI run exits 0", ok, log[-400:])
        with open(out, "rb") as f:
            b1 = f.read()
        with open(out) as f:
            exp = json.load(f)

        check("(a) the export carries the tool's own SHA-256",
              exp["tool_sha256"] == sha256_file(TOOL),
              str(exp.get("tool_sha256")))
        check("(a) the export carries the pinned sheet's SHA-256",
              "64f87bc01906ee6f5a50d38c2b09c09aa9f089f14803cfae9e8a07dd"
              "0af74075" in exp["prereg"], str(exp.get("prereg"))[:120])
        check("(a) the development-data typing rides",
              "NON-GATING" in exp["mode"] and
              "NEVER ENTERS ADJUDICATION" in exp["mode"], "")
        check("(a) fixture-mode is recorded",
              exp["fixture_mode"] is True, str(exp.get("fixture_mode")))

        # the pin echo (fixture mode: echoed, not enforced)
        walks_in = exp["inputs"]["walks"]
        smoke_entry = next(e for e in walks_in
                           if e["path"].startswith(
                               "triadic_t2_cache_t2-prose17p-smoke"))
        check("(a) the smoke-cache pin echo: the item-199 prose pin "
              "recorded, match FALSE (the smoke cache is not the "
              "pinned fresh cache)",
              smoke_entry["pin"] == {
                  "leg": "prose17p",
                  "pinned_file": ("triadic_t2_cache_t2-prose17p-"
                                  "fresh_bfloat16_bos.jsonl"),
                  "pinned_sha256": PIN_PROSE, "match": False},
              str(smoke_entry.get("pin")))

        # ---- the 17p leg: EXACT vs the independent recomputation ----
        lb = exp["legs"]["prose17p"]
        recs = [json.loads(x) for x in open(SMOKE_CACHE) if x.strip()]
        corpus = [d for d in recs if d["leg"] == "prose17p"]
        loops = [d for d in recs if d["leg"] == "loop"]
        check("(a) the smoke cache shape (20 prose17p corpus docs + "
              "10 loop fixtures)", len(corpus) == 20 and
              len(loops) == 10, f"{len(corpus)}/{len(loops)}")
        r = recompute_leg("prose17p", corpus, loops, [91, 108])
        p = "[17p]"
        xe(p + " census: corpus 20 / removed 0",
           (lb["census"]["corpus_docs"], lb["census"]["removed"]),
           (20, 0))
        xe(p + " census not-present receipts (91/108 absent, never a "
           "silent drop)", lb["census"]["receipts"],
           r["census_receipts"])
        xe(p + " parity 10/10 (EVEN calibration / ODD held-out)",
           (lb["parity"]["n_even_calibration"],
            lb["parity"]["n_odd_held_out"]), r["parity"])
        xe(p + " loop population 8 live / 2 inert FROM THE SMOKE "
           "CACHE (live iff n_gen_steps >= 32)",
           (lb["loop_catches"]["n_live"], r["n_inert"]), (8, 2))
        xe(p + " z mu_C", lb["z_baselines"]["mu_C"], r["z"][0])
        xe(p + " z sd_C", lb["z_baselines"]["sd_C"], r["z"][1])
        xe(p + " z mu_F", lb["z_baselines"]["mu_F"], r["z"][2])
        xe(p + " z sd_F", lb["z_baselines"]["sd_F"], r["z"][3])
        xe(p + " t_leg (threshold-on-D level set)",
           lb["thresholds"]["t_leg"], r["t"][0])
        xe(p + " t_esc (SEC-3)", lb["thresholds"]["t_esc"], r["t"][1])
        xe(p + " th_C co-elev (SEC-4)",
           lb["thresholds"]["th_C_coelev"], r["t"][2])
        xe(p + " th_F co-elev (SEC-4)",
           lb["thresholds"]["th_F_coelev"], r["t"][3])
        xe(p + " level-set receipt",
           (lb["level_set_receipt"]["calib_fires"],
            lb["level_set_receipt"]["ceiling"],
            lb["calibration_escalation_fires"]), r["level_set"])
        xe(p + " held-out n", lb["held_out"]["n"], r["held_out"][0])
        xe(p + " held-out fires", lb["held_out"]["fires"],
           r["held_out"][1])
        xe(p + " held-out rate", lb["held_out"]["rate"],
           r["held_out"][2])
        xe(p + " held-out count-ceil", lb["held_out"]["count_ceil"],
           r["held_out"][3])
        xe(p + " held-out Wilson upper", lb["held_out"]["wilson_upper_95"],
           r["held_out"][4])
        xe(p + " held-out escalation", lb["held_out"]["escalation_fires"],
           r["held_out"][5])
        check(p + " fired docs list EXACT (order + every field + every "
              "SEC view)", lb["held_out"]["fired_docs"] ==
              r["fired_views"],
              f"tool {len(lb['held_out']['fired_docs'])} vs control "
              f"{len(r['fired_views'])}")
        xe(p + " overlap easiest-loop D",
           lb["loop_floor_overlap_line"]["easiest_loop_D"],
           r["overlap"][0])
        xe(p + " overlap n",
           lb["loop_floor_overlap_line"]["n_clean_at_or_above"],
           r["overlap"][1])
        xe(p + " overlap rate", lb["loop_floor_overlap_line"]["rate"],
           r["overlap"][2])
        xe(p + " catches at t_leg", lb["loop_catches"]["at_t_leg"],
           r["catches"][0])
        xe(p + " catches at t_esc", lb["loop_catches"]["at_t_esc"],
           r["catches"][1])
        xe(p + " gap on armed D",
           lb["separation_context"]["sigma_gap_on_D"], r["gap_auc"][0])
        xe(p + " AUC on armed D", lb["separation_context"]["auc_on_D"],
           r["gap_auc"][1])
        check(p + " loop views EXACT (every field + every SEC view)",
              lb["populations"]["loops_live"] ==
              [loop_view(d) for d in r["live"]], "")
        check(p + " named-beta doc 95 absent receipt (not in the "
              "smoke corpus; nothing profiled)",
              lb["populations"]["named_beta_docs"] ==
              [{"doc_id": 95, "present": False,
                "note": "not in this run's cache "
                        "(nothing to profile)"}],
              str(lb["populations"]["named_beta_docs"]))
        s = lb["populations"]["summaries_at_0.90"]
        xe(p + " summary loops", s["loops_live"],
           summ([loop_view(d) for d in r["live"]]))
        xe(p + " summary fired", s["held_out_clean_fired"],
           summ(r["fired_views"]))
        nonf = [loop_view(d) for d in r["odd"]
                if d["D"] < r["t"][0]]
        xe(p + " summary non-fired", s["held_out_clean_nonfired"],
           summ(nonf))
        calib_views = []
        for d in r["even"]:
            v = loop_view(d)
            v["half"] = "calibration"
            calib_views.append(v)
        xe(p + " summary calib", s["calibration_half_clean"],
           summ(calib_views))

        # ---- (b) the filler legs' structural receipts ----
        # the pinned p2 census members (the item-205/213 35-doc
        # census: 17p {91,108} + these 33 p2 ids), banked knowledge
        P2_CENSUS_IDS = [3, 7, 8, 13, 16, 17, 18, 23, 27, 28, 33, 37,
                         38, 43, 48, 52, 53, 58, 62, 63, 66, 74, 75,
                         76, 78, 85, 86, 93, 113, 118, 128, 133, 165]
        for leg, first in (("gsm8k", 0), ("humaneval", 0),
                          ("p2corpus", 200)):
            n_cens = len(P2_CENSUS_IDS) if leg == "p2corpus" else 0
            flb = exp["legs"][leg]
            q = f"[{leg} filler]"
            xe(q + " parity halves 24/24",
               (flb["parity"]["n_even_calibration"],
                flb["parity"]["n_odd_held_out"]), (24, 24))
            check(q + " census receipts all not-present (the pinned "
                  "census members, in pinned order)",
                  [x["present"] for x in flb["census"]["receipts"]] ==
                  [False] * n_cens and
                  [x["doc_id"] for x in flb["census"]["receipts"]] ==
                  (P2_CENSUS_IDS if leg == "p2corpus" else []),
                  str(flb["census"]["receipts"][:3]))
            xe(q + " no doc removed (census members absent)",
               flb["census"]["removed"], 0)
            xe(q + " loop population EMPTY (no fixtures carried, "
               "never fabricated)", flb["loop_catches"]["n_live"], 0)
            xe(q + " catches honestly 0/0",
               (flb["loop_catches"]["at_t_leg"],
                flb["loop_catches"]["at_t_esc"]), (0, 0))
            xe(q + " overlap line honest nulls",
               (flb["loop_floor_overlap_line"]["easiest_loop_D"],
                flb["loop_floor_overlap_line"]["n_clean_at_or_above"],
                flb["loop_floor_overlap_line"]["rate"]),
               (None, None, None))
            xe(q + " separation context honest nulls",
               (flb["separation_context"]["sigma_gap_on_D"],
                flb["separation_context"]["auc_on_D"]), (None, None))
            check(q + " level-set receipt self-consistent",
                  flb["level_set_receipt"]["calib_fires"] <=
                  flb["level_set_receipt"]["ceiling"],
                  str(flb["level_set_receipt"]))
            xe(q + " armed sides echo the pinned arming table",
               flb["armed_sides"], list(ARMED[leg]))

        # ---- (c) determinism ----
        ok2, _ = run_tool(["--fixture-mode", "--cache", SMOKE_CACHE,
                           "--cache", fg, "--cache", fh,
                           "--cache", fp, "--tag", "rw17-sec-control",
                           "--out", out])
        with open(out, "rb") as f:
            b2 = f.read()
        check("(c) determinism: a fresh re-run byte-identical",
              ok2 and b1 == b2, "")

    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + "=" * 78)
    print(f"CONTROL CENSUS: {len(PASSES)} PASS / {len(FAILS)} FAIL")
    if FAILS:
        print("FAILED: " + ", ".join(FAILS))
        print("  Fix-the-fixture-or-the-builder, never the tool.")
        sys.exit(1)
    print("  Fix-the-fixture-or-the-builder, never the tool.")
    print("theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, "
          "or adjudicated; findings presented, never adjudicated.")
    sys.exit(0)


if __name__ == "__main__":
    main()

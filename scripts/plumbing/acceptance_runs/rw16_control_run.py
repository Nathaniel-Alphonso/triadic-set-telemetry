#!/usr/bin/env python3
"""rw16_control_run.py -- the REAL-CACHE control for
triadic_rw16_ensemble_readout.py (the RW-16 build's control of
record; the rw15 control precedent, item 214).

TWO receipts:

  (a) THE REAL-BYTES DERIVE CONTROL: the tool's own loader + baseline
      + derive functions run on the BANKED R-BC1 smoke cache (the
      item-214 control input, SHA-pinned) and every per-doc score
      cell (28 docs x 9 scores = 252 cells: the 20 prose17p corpus
      docs + the 8 live loop fixtures) is asserted EXACT against the
      instrument's own smoke export (the banked v32.2.1's own
      numbers) -- the two ensemble sides (maxPRsig / minS) thereby
      validated on real cache bytes, value-for-value.

  (b) THE END-TO-END MECHANICAL CONTROL: the full CLI runs on the
      smoke cache as the prose17p leg (calibration AND test -- the
      only real cache that exists; a mechanical receipt, honestly
      in-sample) + three small synthetic filler legs (the tool's
      four-leg gate requires them; they carry no fixtures and type
      INCONCLUSIVE-POPULATION-GUARD honestly). Asserted: exit 0; the
      17p leg's loop population 8 live / 2 inert FROM THE SMOKE
      CACHE (the instrument's own loop_population inert list
      cross-checked); the fixture identity receipts (10 fixtures /
      1 carrying cache per set, cross-set 10/10 identical); the
      census not-present reporting (91/108 not in the smoke corpus);
      every ensemble quantity on the 17p leg EXACT against an
      INDEPENDENT recomputation from the (a)-validated scores; the
      filler legs' honest guard typings; determinism byte-identical.
      (The legacy two-set mode the (b) control exercises also
      doubles as the control's own legacy-mode regression on real
      bytes under the ledger item 229 amendment.)

  (c) THE DOC-SPLIT REAL-CACHE CONTROL (ledger item 229): the full
      CLI in --doc-split mode on the same real smoke cache (the 20
      prose17p corpus docs split by doc_id parity: 10 EVEN
      calibration / 10 ODD held-out; the 8 live fixtures as the
      positives) + the same three synthetic filler legs (21/20
      halves, no fixtures -> the honest per-leg guard). Asserted:
      exit 0; the doc_split block (item 229 rule + halves 10/10);
      the CALIBRATION-half-only baselines/mu/sd/thresholds EXACT vs
      an independent recomputation from the (a)-validated score
      machinery; the held-out-half fires/gap/typing EXACT vs the
      same recomputation (whatever they measure -- a 10-doc half
      can honestly KILL on sampling noise, the falsifier's teeth
      as designed); the filler legs' honest guard typings;
      determinism byte-identical.

Zero-GPU, read-only. Fix-the-fixture-or-the-builder, never the
tool. FAIL LOUD.
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
FIXDIR = os.path.join(HERE, "rw16_control_fixtures")
OUTDIR = os.path.join(FIXDIR, "outs")

SMOKE_NAME = "triadic_t2_cache_t2-prose17p-smoke_bfloat16_bos.jsonl"
SMOKE_SHA = ("a2f57964232d981db586b007ddbf642b7d6fe7224f65f3499ce"
             "9ecacb2e763e1")
SMOKE_EXPORT_NAME = "triadic_t2_t2-prose17p-smoke.json"
SMOKE_EXPORT_SHA = ("00a3958d557b1f73cd3c65799c0bf64c9e496738314317"
                    "a91601633f2cfd3a0f")

SCORE_KEYS = ("maxC", "minEbar", "maxD", "minRho", "maxSexc", "minS",
              "maxAbsHsig", "maxPRsig", "maxf")
LEGS = ("gsm8k", "humaneval", "prose17p", "p2corpus")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def expect(cond, label, results, detail=""):
    results.append((bool(cond), label, detail))
    print(("  PASS " if cond else "  FAIL ") + label
          + (f"  [{detail}]" if detail and not cond else ""))


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


def one_step(s, pr, i):
    return {"t": [0], "id": [100 + i], "E": [2.0 + 0.01 * (i % 7)],
            "rho": [0.5 + 0.01 * (i % 5)], "s": [s], "f": [0.0],
            "layer": [0], "H": [3.0 + 0.02 * (i % 5)], "PR": [pr],
            "a": [0.1], "rsize": [0.5], "dead5": [None],
            "dead4": [None], "dead3": [None], "dead_share": [0.0]}


def rec(leg, doc_id, steps, n_gen_steps=None):
    return {"key": f"{leg}:{doc_id}", "leg": leg, "doc_id": doc_id,
            "bos": True, "instrument": "v32.2.1-synthetic-filler",
            "prompt_len": 10, "stop_reason": "eos",
            "n_gen_steps": (len(steps["t"]) if n_gen_steps is None
                            else n_gen_steps),
            "n_content_steps": 0,
            "walk_ids": [5] * len(steps["t"]), "steps": steps,
            "commits": [], "hidden_n": 0, "hidden_dim": 0,
            "hidden_b64": ""}


def build_filler(leg):
    """41 anti-aligned arithmetic clean docs (2 fires = 4.88%, within
    the coarse guard, so the n_pos-guard typing lands untrampled by
    the falsifier override)."""
    out = []
    for i in range(41):
        out.append(rec(leg, 500 + i,
                       one_step(0.10 + 0.001 * i, 6.0 - 0.05 * i, i)))
    return out


def main():
    print("=" * 78)
    print("=== RW-16 ENSEMBLE READOUT TOOL -- REAL-CACHE CONTROL RUN "
          "(zero-GPU, read-only) ===")
    results = []
    if os.path.isdir(FIXDIR):
        shutil.rmtree(FIXDIR)
    os.makedirs(OUTDIR, exist_ok=True)

    src_cache = os.environ.get("RW16_SMOKE_CACHE", "")
    src_export = os.environ.get("RW16_SMOKE_EXPORT", "")
    if not (src_cache and src_export):
        print("  !! HARD EXIT: set RW16_SMOKE_CACHE and "
              "RW16_SMOKE_EXPORT to the pulled library files.")
        sys.exit(1)
    cache_path = os.path.join(FIXDIR, SMOKE_NAME)
    export_path = os.path.join(FIXDIR, SMOKE_EXPORT_NAME)
    shutil.copyfile(src_cache, cache_path)
    shutil.copyfile(src_export, export_path)
    c_sha = sha256_file(cache_path)
    e_sha = sha256_file(export_path)
    expect(c_sha == SMOKE_SHA,
           "input receipt: the smoke cache SHA == the item-214 banked "
           "pin", results, c_sha)
    expect(e_sha == SMOKE_EXPORT_SHA,
           "input receipt: the smoke export SHA (banked at this "
           "control)", results, e_sha)

    spec = importlib.util.spec_from_file_location("rw16tool", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # ---- (a) the real-bytes derive control: 252/252 cells ----
    print("\n--- (a) the real-bytes derive control (28 docs x 9 "
          "scores) ---")
    recs = mod.load_cache(cache_path, True)
    corpus = [r for r in recs["docs"] if r["leg"] == "prose17p"]
    loops = [r for r in recs["docs"] if r["leg"] == "loop"]
    expect(len(corpus) == 20 and len(loops) == 10,
           "the smoke cache shape (20 prose17p docs + 10 loop "
           "fixtures)", results,
           f"{len(corpus)}/{len(loops)}")
    base = mod.compute_baselines(corpus, "prose17p")
    live, inert = [], []
    for d in sorted(loops, key=lambda r: str(r["doc_id"])):
        (live if d["n_gen_steps"] >= 32 else inert).append(d)
    expect(len(live) == 8 and len(inert) == 2,
           "the live/inert split 8/2 (the instrument's own "
           "loop_population)", results,
           f"{len(live)}/{len(inert)}")
    smoke = json.load(open(export_path))
    want = {}
    for e in smoke["per_doc"]:
        if e.get("score") is not None:
            want[str(e["doc_id"])] = e["score"]
    for fx, sc in smoke["loop_doc_scores"]["prose17p"].items():
        want[str(fx)] = sc
    expect(len(want) == 28,
           "the export score map covers 28 docs (20 per_doc corpus "
           "cells + the 8 live fixtures' loop_doc_scores)", results,
           str(len(want)))
    n_cells, n_exact, worst = 0, 0, 0.0
    for d in corpus + live:
        sc = mod.derive_doc_stats(d, base)["score"]
        wsc = want[str(d["doc_id"])]
        for k in SCORE_KEYS:
            n_cells += 1
            diff = abs(sc[k] - wsc[k])
            worst = max(worst, diff)
            if diff == 0.0:
                n_exact += 1
    expect(n_cells == 252 and n_exact == 252,
           "ALL 252/252 per-doc score cells EXACT vs the instrument's "
           "own smoke export (the two ensemble sides validated on "
           "real cache bytes)", results,
           f"exact {n_exact}/{n_cells}, worst |diff| {worst}")
    expect(sorted(str(d["doc_id"]) for d in inert)
           == sorted(smoke["loop_population"]["inert"]),
           "the inert-fixture census matches the instrument's own "
           "inert list", results,
           str(sorted(str(d["doc_id"]) for d in inert)))

    # ---- (b) the end-to-end mechanical control ----
    print("\n--- (b) the end-to-end mechanical control (hybrid: the "
          "real 17p leg + synthetic fillers) ---")
    for leg in ("gsm8k", "humaneval", "p2corpus"):
        with open(os.path.join(FIXDIR, f"filler_{leg}.jsonl"), "w") as f:
            for r in build_filler(leg):
                f.write(json.dumps(r) + "\n")
    calib = [SMOKE_NAME, "filler_gsm8k.jsonl", "filler_humaneval.jsonl",
             "filler_p2corpus.jsonl"]

    def run_cli(out_name):
        cmd = [sys.executable, TOOL]
        for cx in calib:
            cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
        for cx in calib:
            cmd += ["--test-cache", os.path.join(FIXDIR, cx)]
        cmd += ["--tag", out_name,
                "--out", os.path.join(OUTDIR, out_name + ".json"),
                "--fixture-mode"]
        return subprocess.run(cmd, capture_output=True, text=True)

    p = run_cli("ctl")
    expect(p.returncode == 0, "the hybrid CLI run exits 0", results,
           f"rc={p.returncode} {p.stdout[-400:]}")
    o = json.load(open(os.path.join(OUTDIR, "ctl.json")))
    expect(o["tool_sha256"] == sha256_file(TOOL),
           "the export carries the tool's own SHA-256", results)
    fir = o["fixture_identity_receipt"]
    expect(fir["calibration"]["n_loop_fixtures"] == 10
           and fir["calibration"]["copies_byte_identical"] is True
           and fir["test"]["n_loop_fixtures"] == 10
           and fir["test"]["copies_byte_identical"] is True,
           "the within-set fixture identity receipts (10 fixtures / "
           "1 carrying cache, both sets)", results, json.dumps(fir))
    expect(fir["cross_set_reported"]["n_compared"] == 10
           and fir["cross_set_reported"]["n_identical"] == 10,
           "the cross-set report 10/10 (calib == test file)", results,
           json.dumps(fir["cross_set_reported"]))
    leg17 = o["legs"]["prose17p"]
    cd = {c["doc_id"]: c for c in leg17["calibration"]["census_docs"]}
    expect(len(cd) == 2 and cd[91]["present"] is False
           and cd[108]["present"] is False,
           "census not-present reporting (91/108 not in the smoke "
           "corpus; nothing to exclude, never a silent drop)", results,
           json.dumps(leg17["calibration"]["census_docs"]))
    expect(leg17["calibration"]["n_clean"] == 20
           and leg17["test"]["n_clean"] == 20,
           "the 17p leg populations 20/20 (the smoke corpus whole)",
           results)
    lp = leg17["test"]["loop_population"]
    expect(lp["n_live"] == 8 and lp["n_inert"] == 2
           and lp["source_cache"] == SMOKE_NAME
           and sorted(lp["inert"])
           == sorted(smoke["loop_population"]["inert"]),
           "the 17p positives FROM THE SMOKE CACHE (8 live / 2 inert, "
           "the instrument's own inert list)", results,
           json.dumps(lp))

    # the independent mirror on the (a)-validated scores
    C = [mod.derive_doc_stats(d, base)["score"]["maxPRsig"]
         for d in corpus]
    F = [mod.derive_doc_stats(d, base)["score"]["minS"] for d in corpus]
    muC, sdC = mstd(C)
    muF, sdF = mstd(F)
    zC = sorted((v - muC) / sdC for v in C)
    zF = sorted((v - muF) / sdF for v in F)
    thC = quant(zC, 0.975)
    thF = quant(zF, 0.975)
    D_neg = [max((c - muC) / sdC, (f - muF) / sdF)
             for c, f in zip(C, F)]
    D_pos = [max((mod.derive_doc_stats(d, base)["score"]["maxPRsig"]
                  - muC) / sdC,
                 (mod.derive_doc_stats(d, base)["score"]["minS"]
                  - muF) / sdF) for d in live]
    gap = sgap(D_pos, D_neg)
    fires = sum(1 for c, f in zip(C, F)
                if (c - muC) / sdC >= thC or (f - muF) / sdF >= thF)
    rate = fires / len(D_neg)
    cal = leg17["calibration"]
    ens = leg17["test"]["ensemble"]
    fa = leg17["test"]["fire_accounting"]
    ok = (abs(cal["mu_C"] - muC) < 1e-9 and abs(cal["sd_C"] - sdC) < 1e-9
          and abs(cal["mu_F"] - muF) < 1e-9
          and abs(cal["sd_F"] - sdF) < 1e-9
          and abs(cal["thresholds"]["z_C"] - thC) < 1e-9
          and abs(cal["thresholds"]["z_F"] - thF) < 1e-9
          and abs(ens["sigma_gap"] - round(gap, 3)) < 1e-9
          and fa["combined_fires"] == fires
          and abs(fa["combined_rate"] - round(rate, 6)) < 1e-12
          and fa["over_budget"] == (rate > 0.05))
    expect(ok,
           "the 17p leg's ensemble readout EXACT vs the independent "
           "recomputation (thresholds, D-gap, fire accounting)",
           results,
           f"thC {cal['thresholds']['z_C']:.4f} vs {thC:.4f}; gap "
           f"{ens['sigma_gap']} vs {round(gap, 3)}; fires "
           f"{fa['combined_fires']} vs {fires}; over "
           f"{fa['over_budget']} vs {rate > 0.05}")
    expect(ens["verdict_presented"] in
           ("PASS_2SIGMA", "FAIL", "INCONCLUSIVE-FROM-JITTER",
            "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"),
           "the 17p typing is one of the pinned typings (a 20-doc "
           "in-sample population cannot resolve the 5% budget -- "
           "typed honestly, whatever it is)", results,
           f"{ens['verdict_presented']}: {ens['verdict_basis']}")
    guard_ok = all(
        o["legs"][leg]["test"]["ensemble"]["verdict_presented"]
        == "INCONCLUSIVE-POPULATION-GUARD"
        for leg in ("gsm8k", "humaneval", "p2corpus"))
    expect(guard_ok,
           "the synthetic filler legs type INCONCLUSIVE-POPULATION-"
           "GUARD honestly (no fixtures carried, never fabricated)",
           results)
    p2 = run_cli("ctl2")
    with open(os.path.join(OUTDIR, "ctl.json"), "rb") as fa_, \
            open(os.path.join(OUTDIR, "ctl2.json"), "rb") as fb:
        expect(fa_.read() == fb.read() and p2.returncode == 0,
               "determinism: a fresh re-run byte-identical", results)

    # ---- (c) the doc-split real-cache control (ledger item 229) ----
    print("\n--- (c) the doc-split real-cache control (the smoke "
          "cache split by doc_id parity) ---")

    def run_cli_split(out_name):
        cmd = [sys.executable, TOOL, "--doc-split"]
        for cx in calib:
            cmd += ["--calib-cache", os.path.join(FIXDIR, cx)]
        cmd += ["--tag", out_name,
                "--out", os.path.join(OUTDIR, out_name + ".json"),
                "--fixture-mode"]
        return subprocess.run(cmd, capture_output=True, text=True)

    p3 = run_cli_split("ctl3")
    expect(p3.returncode == 0,
           "the doc-split CLI run exits 0 (the four walks passed "
           "ONCE; no test caches)", results,
           f"rc={p3.returncode} {p3.stdout[-400:] if p3.returncode else ''}")
    o3 = json.load(open(os.path.join(OUTDIR, "ctl3.json")))
    expect(o3["doc_split_mode"] is True
           and "ledger item 229" in o3["doc_split"]["rule"]
           and o3["doc_split"]["calib_half"] == "even doc_id"
           and o3["doc_split"]["held_out_half"] == "odd doc_id"
           and len(o3["inputs"]["walks"]) == 4,
           "the split-mode export: doc_split_mode + the item-229 "
           "rule + the four walks ONCE", results,
           json.dumps(o3["doc_split"])[:150])
    leg17s = o3["legs"]["prose17p"]
    # the independent split mirror on the (a)-validated score
    # machinery: baselines from the EVEN half ONLY (the tool's own
    # compute_baselines fed the even docs alone -- its per-doc
    # derive was validated 252/252 on these very bytes; every
    # downstream quantity is the runner's own arithmetic)
    even_docs = [d for d in corpus
                 if isinstance(d["doc_id"], int)
                 and d["doc_id"] % 2 == 0]
    odd_docs = [d for d in corpus
                if isinstance(d["doc_id"], int)
                and d["doc_id"] % 2 == 1]
    expect(len(even_docs) == 10 and len(odd_docs) == 10,
           "the smoke corpus splits 10 EVEN / 10 ODD by doc_id "
           "parity", results, f"{len(even_docs)}/{len(odd_docs)}")
    sbase = mod.compute_baselines(even_docs, "prose17p")
    C_e = [mod.derive_doc_stats(d, sbase)["score"]["maxPRsig"]
           for d in even_docs]
    F_e = [mod.derive_doc_stats(d, sbase)["score"]["minS"]
           for d in even_docs]
    smuC, ssdC = mstd(C_e)
    smuF, ssdF = mstd(F_e)
    szc = sorted((v - smuC) / ssdC for v in C_e)
    szf = sorted((v - smuF) / ssdF for v in F_e)
    sthC = quant(szc, 0.975)
    sthF = quant(szf, 0.975)
    sD_neg = [max((mod.derive_doc_stats(d, sbase)["score"]["maxPRsig"]
                   - smuC) / ssdC,
                  (mod.derive_doc_stats(d, sbase)["score"]["minS"]
                   - smuF) / ssdF) for d in odd_docs]
    sD_pos = [max((mod.derive_doc_stats(d, sbase)["score"]["maxPRsig"]
                   - smuC) / ssdC,
                  (mod.derive_doc_stats(d, sbase)["score"]["minS"]
                   - smuF) / ssdF) for d in live]
    sgap_ = sgap(sD_pos, sD_neg)
    sfires = sum(1 for d in odd_docs
                 if (mod.derive_doc_stats(d, sbase)["score"]["maxPRsig"]
                     - smuC) / ssdC >= sthC
                 or (mod.derive_doc_stats(d, sbase)["score"]["minS"]
                     - smuF) / ssdF >= sthF)
    srate = sfires / len(sD_neg)
    sover = srate > 0.05
    sds = leg17s["doc_split"]
    scal = leg17s["calibration"]
    sens = leg17s["test"]["ensemble"]
    sfa = leg17s["test"]["fire_accounting"]
    expect(sds["n_even_calib"] == 10 and sds["n_odd_held_out"] == 10,
           "the 17p leg's doc_split halves 10/10 (the export's own "
           "receipt)", results,
           f"{sds['n_even_calib']}/{sds['n_odd_held_out']}")
    ok_split = (abs(scal["mu_C"] - smuC) < 1e-9
                and abs(scal["sd_C"] - ssdC) < 1e-9
                and abs(scal["mu_F"] - smuF) < 1e-9
                and abs(scal["sd_F"] - ssdF) < 1e-9
                and abs(scal["thresholds"]["z_C"] - sthC) < 1e-9
                and abs(scal["thresholds"]["z_F"] - sthF) < 1e-9)
    expect(ok_split,
           "the 17p split readout's calibration-half mu/sd/thresholds "
           "EXACT vs the independent recomputation (EVEN-half-only "
           "baselines)", results,
           f"thC {scal['thresholds']['z_C']:.4f} vs {sthC:.4f}; "
           f"thF {scal['thresholds']['z_F']:.4f} vs {sthF:.4f}")
    expect(abs(sens["sigma_gap"] - round(sgap_, 3)) < 1e-9
           and sfa["combined_fires"] == sfires
           and abs(sfa["combined_rate"] - round(srate, 6)) < 1e-12
           and sfa["over_budget"] == sover,
           "the 17p held-out-half gap + fire accounting EXACT vs the "
           "independent recomputation", results,
           f"gap {sens['sigma_gap']} vs {round(sgap_, 3)}; fires "
           f"{sfa['combined_fires']} vs {sfires}; over "
           f"{sfa['over_budget']} vs {sover}")
    want_typing = ("CANDIDATE-KILLED-FALSE-ALARM-BUDGET" if sover
                   else "PASS_2SIGMA")
    expect(sens["verdict_presented"] == want_typing,
           "the 17p split typing exactly what the mirror measures "
           f"({want_typing} -- a 10-doc held-out half honestly "
           "cannot resolve the 5% budget; typed as measured, never "
           "smoothed)", results,
           f"{sens['verdict_presented']}: {sens['verdict_basis'][:90]}")
    lp3 = leg17s["test"]["loop_population"]
    expect(lp3["n_live"] == 8 and lp3["n_inert"] == 2
           and lp3["source_cache"] == SMOKE_NAME,
           "the 17p split positives FROM THE SMOKE CACHE "
           "(8 live / 2 inert, never in calibration)", results,
           json.dumps(lp3)[:120])
    guard3 = all(
        o3["legs"][leg]["test"]["ensemble"]["verdict_presented"]
        == "INCONCLUSIVE-POPULATION-GUARD"
        for leg in ("gsm8k", "humaneval", "p2corpus"))
    expect(guard3,
           "the filler legs type INCONCLUSIVE-POPULATION-GUARD "
           "honestly in split mode too (no fixtures, never "
           "fabricated)", results)
    p4 = run_cli_split("ctl4")
    with open(os.path.join(OUTDIR, "ctl3.json"), "rb") as fa_, \
            open(os.path.join(OUTDIR, "ctl4.json"), "rb") as fb:
        expect(fa_.read() == fb.read() and p4.returncode == 0,
               "split-mode determinism: a fresh re-run "
               "byte-identical", results)

    n_pass = sum(1 for r in results if r[0])
    n_fail = len(results) - n_pass
    print("\n  === CONTROL CENSUS: "
          f"{n_pass} PASS / {n_fail} FAIL ===")
    for ok_, label, _ in results:
        if not ok_:
            print(f"    FAILED: {label}")
    print("  Fix-the-fixture-or-the-builder, never the tool"
          + ("; FAIL LOUD." if n_fail else "."))
    print("=" * 78)
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

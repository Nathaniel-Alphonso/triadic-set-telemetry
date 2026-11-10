#!/usr/bin/env python3
"""stage2_act2b_readout_v1 -- the Act-2b four-readout zero-build
diagnostic, packaged for THE OWNER'S OWN RUN.

A paper act over the banked bytes only: zero GPU, zero decodes, no
model calls, no bar anywhere, no instrument byte moved. The script
re-derives every readout banked at the readout stamp of record from the pinned
inputs, verifies every input's sha256 fail-loud BEFORE any compute,
and self-checks every number against the readout receipts of record -- exit 0
only if every check lands.

Usage (two staged runs; the prep pass caches the heavy lane work):
    python3 stage2_act2b_readout_v1.py --stage prep
    python3 stage2_act2b_readout_v1.py --stage read
or one pass (same compute, no cache reuse):
    python3 stage2_act2b_readout_v1.py --stage all

LAYOUT-FREE: no directory structure is assumed. The script searches
for each input by filename, then by exact byte size, and admits a
file ONLY on an exact sha256 match against the banked pin -- wherever
it lives. Search roots: the directory you run from, the script's own
directory, and anything you pass as --root / --instruments (or
$INSTRUMENTS_DIR). If an input is not found, the script names it with
its exact size and sha256 and refuses to compute; place the file
anywhere under a search root and run again. The sha256 is the path
law; the directory tree never is (the layout-assumption defect owned
and struck at the ruling of record).
"""
import argparse
import hashlib
import json
import os
import pickle
import re
import shutil
import sys
import tempfile

# ------------------------------------------------------------------
# THE PINS OF RECORD (fail-loud before any compute)
# ------------------------------------------------------------------
INSTRUMENTS = {
    "triadic_splitter_v1.py": (52410,
        "5980eaec57fc990707e3317f3f32573893c915ce821dfe665536634136c9c4a0"),
    "triadic_accumulator_v1.py": (58292,
        "c7acb944223d16e327f6ee5da706181ea35749aa95a03fc18628393710e6662e"),
    "triadic_accumulator_prose_v1.py": (76867,
        "7d7ab8feaaae552b973d609ac27a4772a70d9cd3438486e2c33521a2aafbb7c9"),
    "triadic_hook_v1.py": (52078,
        "4de049deab7f0e70116da819000641f785c7f5014eedf3c6889d660f57a2ccb5"),
    "stage2_splice_builder_v1.py": (68635,
        "14d1f448e9bd0a9a93a887972db925d4da7ecac2c53b1eea9fb850b35b3f938d"),
    "stage2_ladder_walk_v1.py": (89115,
        "3d4faa17fd9afdb2dfe70c6e849331b57b951e1697513e33ac827769a2bf9b6d"),
}
INPUT_SPECS = [
    # (known filename candidates, exact bytes, sha256 of record)
    (["stage2_mixed_cache.json"], 14814947,
     "a5a4ae539112472424c2fb4160f2422e4810d4a83140f6e00972172502f76ea8"),
    (["stage2_census_export.json"], 65583,
     "cca12263db49a502bdf63761144d4b4953fd42c56b5a04a0a40f690270d0b86f"),
    (["triadic_wu_prose_read_v1.json"], 656143,
     "a4e0ef03626a6cd47b926b20bf91358c182df0b16cf3ad5c17e4e316f0d82e3e"),
    (["triadic_t2_thin_rw17-prose-r2.jsonl"], 159280278,
     "88cbadee7baa1e35fe7e762715970066d6098301f044f810c0efd1e38c70ae94"),
    (["triadic_t2_thin_rw17-code-r2.jsonl"], 80912361,
     "77dd63c7d21c630336e0afb074fbf15515b72c7da80831e9969314529a79a9b4"),
    (["stage2_ladder_walk_console.txt", "stage2_ladder_walk_console_2.txt",
      "redeliv_walk_1.txt", "redeliv_walk_2.txt"], 115886,
     "8f2865533b57a65f0cef415173b60db0e3a1ff2e804b7323fe3ec80a44ce7ee9"),
]
INSTRUMENT_SPECS = [
    (["triadic_splitter_v1.py"], 52410,
     "5980eaec57fc990707e3317f3f32573893c915ce821dfe665536634136c9c4a0"),
    (["triadic_stage1_engines_v1.py"], 11980,
     "79c794c0a850f67212d3ab82f55cc2680451c33c4edc1b1ac8d93d6760af907b"),
    (["triadic_accumulator_v1.py"], 58292,
     "c7acb944223d16e327f6ee5da706181ea35749aa95a03fc18628393710e6662e"),
    (["triadic_accumulator_prose_v1.py"], 76867,
     "7d7ab8feaaae552b973d609ac27a4772a70d9cd3438486e2c33521a2aafbb7c9"),
    (["triadic_hook_v1.py"], 52078,
     "4de049deab7f0e70116da819000641f785c7f5014eedf3c6889d660f57a2ccb5"),
    (["stage2_splice_builder_v1.py"], 68635,
     "14d1f448e9bd0a9a93a887972db925d4da7ecac2c53b1eea9fb850b35b3f938d"),
    (["stage2_ladder_walk_v1.py"], 89115,
     "3d4faa17fd9afdb2dfe70c6e849331b57b951e1697513e33ac827769a2bf9b6d"),
]

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def discover(search_roots):
    """LAYOUT-FREE DISCOVERY: no assumed directories. Every input is
    FOUND under the search roots by filename first, then by exact byte
    size, and admitted ONLY on an exact sha256 match -- the pin is the
    path law, never the directory tree (the layout-assumption defect
    owned and struck at the same ruling)."""
    index = {}  # path -> size, built once per root walk
    for root in search_roots:
        if not root or not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames
                                 if d not in (".git", "__pycache__"))
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                try:
                    index[p] = os.path.getsize(p)
                except OSError:
                    pass
    print("[pin] discovery: %d files indexed under %s"
          % (len(index), ", ".join(r for r in search_roots if r)))
    resolved = {}
    for names, size, sha in INPUT_SPECS:
        cands = [p for p in index if os.path.basename(p) in names]
        cands += [p for p in index if index[p] == size
                  and p not in cands and not p.endswith(
                      "stage2_act2b_readout_v1.py")]
        hit = None
        for p in cands:
            if index[p] == size and sha256_file(p) == sha:
                hit = p
                break
        resolved[names[0]] = hit
        print("[pin] %-46s %s" % (names[0],
              hit if hit else "NOT FOUND (need %d B / sha %s...)"
              % (size, sha[:16])))
    missing = [k for k, v in resolved.items() if v is None]
    if missing:
        sys.exit("[pin] missing %d input(s): %s -- place them anywhere "
                 "under the search roots (or pass --root DIR); the "
                 "sha256 decides, the directory never does"
                 % (len(missing), ", ".join(missing)))
    # ---- the instruments: their own IMPORT-PIN law requires the seven
    # co-location files (six instruments + the stage-1 engines the
    # accumulator pins) all in one directory, each verifying its
    # siblings' bytes in its own directory at import. Prefer a
    # directory holding all seven byte-verified; else stage copies.
    instr = None
    for dirpath in sorted({os.path.dirname(p) for p in index}):
        if not all(os.path.isfile(os.path.join(dirpath, s[0][0]))
                   for s in INSTRUMENT_SPECS):
            continue
        if all(sha256_file(os.path.join(dirpath, s[0][0])) == s[2]
               for s in INSTRUMENT_SPECS):
            instr = {s[0][0]: os.path.join(dirpath, s[0][0])
                     for s in INSTRUMENT_SPECS}
            print("[pin] instruments co-located + byte-verified in:"
                  " %s" % dirpath)
            break
    if instr is None:
        stage = tempfile.mkdtemp(prefix="act2b_instruments_")
        for names, size, sha in INSTRUMENT_SPECS:
            cands = [p for p in index if os.path.basename(p) in names]
            cands += [p for p in index if index[p] == size
                      and p not in cands]
            hit = None
            for p in cands:
                if index[p] == size and sha256_file(p) == sha:
                    hit = p
                    break
            if hit is None:
                sys.exit("[pin] instrument not found: %s (need %d B / "
                         "sha %s...)" % (names[0], size, sha[:16]))
            shutil.copy2(hit, os.path.join(stage, names[0]))
        instr = {n[0][0]: os.path.join(stage, n[0][0])
                 for n in INSTRUMENT_SPECS}
        print("[pin] instruments found scattered; byte-exact copies "
              "staged into %s so their own co-location pin holds "
              "(sha-verified, zero bytes modified)" % stage)
    resolved.update(instr)
    print("[pin] every input found and byte-verified; compute may open")
    return resolved

# ------------------------------------------------------------------
# THE LOOP-CRITERION LAW (his 2a stamp, pinned before any rows read)
# ------------------------------------------------------------------
def sig_of(seq, max_setup=5, max_period=8):
    """The banked repetition signature: minimal (setup, period) with
    FULL conformance, no partial credit: seq[i] == seq[i+p] for every
    i >= setup. None when no such pair exists."""
    n = len(seq)
    for s in range(0, max_setup + 1):
        for p in range(1, max_period + 1):
            if n - s >= 2 * p and all(seq[i] == seq[i + p]
                                      for i in range(s, n - p)):
                return (s, p)
    return None

def conforms(seq, sig):
    if sig is None:
        return False
    s, p = sig
    n = len(seq)
    return n - s >= 2 * p and all(seq[i] == seq[i + p]
                                  for i in range(s, n - p))

# ------------------------------------------------------------------
# STAGE: PREP (the heavy lane work, cached)
# ------------------------------------------------------------------
import importlib.machinery
import importlib.util

def load_instruments(paths):
    """Load the six instruments of record by DISCOVERED PATH (they may
    live anywhere and even carry no proper filename -- the sha256
    admitted them), registered under their module names so every
    cross-import inside the instruments resolves. The seventh
    co-location file (the stage-1 engines) is pinned and staged but
    imported only as the accumulator's own dependency."""
    order = ["triadic_splitter_v1.py", "triadic_stage1_engines_v1.py",
             "triadic_accumulator_v1.py", "triadic_hook_v1.py",
             "triadic_accumulator_prose_v1.py",
             "stage2_splice_builder_v1.py", "stage2_ladder_walk_v1.py"]
    mods = {}
    remaining = list(order)
    while remaining:
        progressed = False
        for name in list(remaining):
            mod_name = name[:-3]
            path = paths[name]
            loader = importlib.machinery.SourceFileLoader(mod_name, path)
            spec = importlib.util.spec_from_file_location(
                mod_name, path, loader=loader)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            try:
                loader.exec_module(mod)
            except ModuleNotFoundError:
                del sys.modules[mod_name]  # its dependency loads first
                continue
            mods[mod_name] = mod
            remaining.remove(name)
            progressed = True
        if not progressed:
            sys.exit("[pin] instrument cross-imports unresolved among: %s"
                     % ", ".join(remaining))
    return mods

def do_prep(paths, cache_path):
    M = load_instruments(paths)
    sp = M["triadic_splitter_v1"]
    acc = M["triadic_accumulator_v1"]
    pap = M["triadic_accumulator_prose_v1"]
    hk = M["triadic_hook_v1"]
    bd = M["stage2_splice_builder_v1"]
    W = M["stage2_ladder_walk_v1"]

    print("[prep] loading the prose thin + export of record")
    corpus, fixtures, cen = pap.load_thin(
        paths["triadic_t2_thin_rw17-prose-r2.jsonl"])
    join, rows_ex, arm = pap.load_export(
        paths["triadic_wu_prose_read_v1.json"])
    W_at, wrec = pap.w_derivation(corpus,
                                  lambda did: join[did][0] == "calibration")
    calib = pap.measure_lane_calibration(corpus, join, W_at)
    code_fixtures = W.load_code_thin_fixtures(pap,
        paths["triadic_t2_thin_rw17-code-r2.jsonl"], bd)
    base_s, base_pr, pool_s, pool_pr = W.rw16_baselines(
        corpus, lambda did: join[did][0] == "calibration",
        pap.BUCKET, pap.MIN_N)
    src = {"sp": sp, "acc": acc, "pap": pap, "hk": hk, "bd": bd,
           "prose_recs": {"prose-%03d" % r["doc_id"]: r for r in corpus},
           "prose_fixtures": {r["doc_id"]: r for r in fixtures},
           "code_fixtures": code_fixtures,
           "base_s": base_s, "base_pr": base_pr,
           "pool_s": pool_s, "pool_pr": pool_pr,
           "zmax_by_source": {}, "docs_by_leg": {}}
    cache = json.load(open(paths["stage2_mixed_cache.json"]))
    census = json.load(open(paths["stage2_census_export.json"]))

    def walk_ids_of(sd, sha_p):
        if sha_p.startswith("88cbadee"):
            rec = src["prose_fixtures"].get(sd) or src["prose_recs"].get(sd)
        else:
            rec = src["code_fixtures"].get(sd)
        return rec["walk_ids"] if rec and rec.get("walk_ids") else None

    # the banked species signatures (first-seen native range, census
    # order -- the deterministic law of the banked readout)
    banked = {}
    spans = {"CODE": [], "PROSE": []}
    for leg in ("CODE", "PROSE"):
        surface = cache[leg]["surface"]
        cen_by_id = {c["doc_id"]: c for c in census["legs"][leg]["doc_census"]}
        for doc in cache[leg]["docs"]:
            cen = cen_by_id[doc["doc_id"]]
            d = W.prep_doc(leg, surface, doc, cen, src)
            for si, s in enumerate(d["spans"]):
                csp = cen["spans"][si]
                sd = csp["source"]["doc_id"]
                sha_p = csp["source"].get("sha_prefix", "")
                nat = csp["source"]["native_range"]
                wi = walk_ids_of(sd, sha_p)
                walk_slice = wi[nat[0]:nat[1]] if wi is not None else None
                if csp["state"] == "loop" and sd not in banked:
                    banked[sd] = sig_of(walk_slice) if walk_slice else None
                spans[leg].append({
                    "label": "%s:s%d" % (doc["doc_id"], si),
                    "doc_id": doc["doc_id"], "si": si,
                    "state": csp["state"], "n": s["n_rows"],
                    "row0": s["start"], "row1": s["start"] + s["n_rows"],
                    "src_doc": sd, "native": nat,
                    "span_rec": s["span_rec"], "w_span": s["w_span"],
                    "walk_slice": walk_slice})
        print("[prep] %s leg: %d spans flattened + lane-joined"
              % (leg, len(spans[leg])))
    ctx = {"calib": calib, "spans": spans, "banked_sigs": banked,
           "grid": list(acc.GRID), "paths": paths}
    with open(cache_path, "wb") as f:
        pickle.dump(ctx, f)
    print("[prep] context cached: %s (%d B)" % (cache_path,
          os.path.getsize(cache_path)))
    print("[prep] banked species signatures: %s"
          % {k: banked[k] for k in sorted(banked)})

# ------------------------------------------------------------------
# STAGE: READ (all readouts + the self-check table)
# ------------------------------------------------------------------
RE_RUNG_E = re.compile(
    r"^\[rung-e\] (CODE|PROSE) (\S+):s(\d+) \(true (CODE|PROSE)/(clean|loop)"
    r", source ([^:]+)\): @2\.0000 (?:trip h=(\w+) v=([0-9.]+)"
    r"|no trip \(peak (-?[0-9.]+)\)) \| @2\.3305 "
    r"(?:trip h=(\w+) v=([0-9.]+)|no trip \(peak (-?[0-9.]+)\))"
    r"(?: \| grade (\S+))")

CHECKS = []
def check(name, expected, got, tol=None):
    ok = (abs(got - expected) <= tol) if tol is not None else (got == expected)
    CHECKS.append((name, expected, got, ok))
    print("[%s] %-58s expected %s | got %s"
          % ("ok " if ok else "FAIL", name, expected, got))
    return ok

def do_read(ctx_path):
    with open(ctx_path, "rb") as f:
        ctx = pickle.load(f)
    calib, spans, banked = ctx["calib"], ctx["spans"], ctx["banked_sigs"]
    grid = ctx["grid"]
    paths = ctx["paths"]
    load_instruments(paths)  # registered by name: the composites()
    # helper's own `import triadic_accumulator_prose_v1` resolves
    cache = json.load(open(paths["stage2_mixed_cache.json"]))
    console = open(paths["stage2_ladder_walk_console.txt"]).read().splitlines()

    # ---- r1: the console parse + the banked 200-span table ----
    rows = []
    for ln in console:
        m = RE_RUNG_E.match(ln)
        if m:
            rows.append(m.groups())
    print("\n[r1] console rows parsed: %d" % len(rows)
          if len(rows) != 200 else
          "\n[r1] console rows parsed: %d (the full 200-span census)"
          % len(rows))
    check("r1: console rows", 200, len(rows))
    for leg in ("CODE", "PROSE"):
        for state in ("clean", "loop"):
            n = sum(1 for r in rows if r[0] == leg and r[4] == state)
            check("r1: %s/%s span census" % (leg, state), 55 if state ==
                  "clean" else 45, n)
    for leg in ("CODE", "PROSE"):
        tp = sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                 and r[6] is not None)
        fn = sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                 and r[6] is None)
        tn = sum(1 for r in rows if r[0] == leg and r[4] == "clean"
                 and r[6] is None)
        fp = sum(1 for r in rows if r[0] == leg and r[4] == "clean"
                 and r[6] is not None)
        if leg == "CODE":
            check("r1: CODE@[REDACTED_PER_PUBLICATION_POLICY] {TP,FN,TN,FP}", (28, 17, 55, 0), (tp, fn, tn, fp))
            tp2 = sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                      and r[9] is not None)
            fn2 = sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                      and r[9] is None)
            tn2 = sum(1 for r in rows if r[0] == leg and r[4] == "clean"
                      and r[9] is None)
            fp2 = sum(1 for r in rows if r[0] == leg and r[4] == "clean"
                      and r[9] is not None)
            check("r1: CODE@[REDACTED_PER_PUBLICATION_POLICY] {TP,FN,TN,FP}", (27, 18, 55, 0),
                  (tp2, fn2, tn2, fp2))
        else:
            check("r1: PROSE@[REDACTED_PER_PUBLICATION_POLICY] {TP,FN,TN,FP}", (28, 17, 53, 2), (tp, fn, tn, fp))
            tp2 = sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                      and r[9] is not None)
            fn2 = sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                      and r[9] is None)
            tn2 = sum(1 for r in rows if r[0] == leg and r[4] == "clean"
                      and r[9] is None)
            fp2 = sum(1 for r in rows if r[0] == leg and r[4] == "clean"
                      and r[9] is not None)
            check("r1: PROSE@[REDACTED_PER_PUBLICATION_POLICY] {TP,FN,TN,FP}", (27, 18, 55, 0),
                  (tp2, fn2, tn2, fp2))
    for leg in ("CODE", "PROSE"):
        grades = []
        for r in rows:
            if r[0] == leg and r[12]:
                grades += re.split("/", r[12])
        grades = [g for g in grades if g]
        nm = sum(1 for g in grades if g == "MATCH")
        nmiss = sum(1 for g in grades if g == "MISSED")
        nft = sum(1 for g in grades if g == "FALSE-TRIP")
        if leg == "CODE":
            check("r1: CODE form grades {MATCH,MISSED,FALSE-TRIP}",
                  (165, 35, 0), (nm, nmiss, nft))
        else:
            check("r1: PROSE form grades {MATCH,MISSED,FALSE-TRIP}",
                  (163, 35, 2), (nm, nmiss, nft))
    con = {("%s %s:s%s" % (r[0], r[1], r[2])): r for r in rows}

    # ---- the composite law (the 5-lane consensus mean) ----
    lanes = ("s", "PR", "E", "H", "W")
    def composites(span):
        rec, wsp = span["span_rec"], span["w_span"]
        if rec is None or rec.get("steps") is None:
            return None
        import triadic_accumulator_prose_v1 as pap
        out = {}
        n = span["n"]
        for h in grid:
            if h != "EOS" and h >= n:
                continue
            vals = pap.prose_prefix_values(rec, h, wsp)
            zs = {}
            for lane in lanes:
                m = calib["moments"][lane][h]
                pin = calib["pins"][lane][h]
                assert pin is not None, "tied pin -- dies loud"
                zs[lane] = pin * (vals[lane] - m["mu"]) / m["sd_pop"]
            out[h] = sum(zs.values()) / float(len(zs))
            if h == "EOS":
                out["lane_z"] = zs
        return out

    # ---- r2: trip + peak reproduction, identity, W census ----
    docs = {leg: {d["doc_id"]: d for d in cache[leg]["docs"]}
            for leg in ("CODE", "PROSE")}
    trip_ok = peak_ok = n_emission = 0
    peak_diffs = []
    by_key = {}
    for leg in ("CODE", "PROSE"):
        for s in spans[leg]:
            comps = composites(s)
            if comps is None:
                continue
            n_emission += 1
            key = "%s %s" % (leg, s["label"])
            by_key[key] = (s, comps)
            c = con[key]
            for bar, ti, vi, pi in (([REDACTED_PER_PUBLICATION_POLICY], 6, 7, 8), ([REDACTED_PER_PUBLICATION_POLICY], 9, 10, 11)):
                reached = [h for h in grid if h in comps]
                crossing = None
                for h in reached:
                    if comps[h] >= bar:
                        crossing = h
                        break
                con_trip = c[ti] is not None
                ok = (crossing is not None) == con_trip
                if not ok:
                    print("[r2] TRIP MISMATCH %s @%s" % (key, bar))
                else:
                    trip_ok += 1
            peak = max(comps[h] for h in comps if h != "lane_z")
            # a tripped span prints its crossing value (which may sit
            # under the max -- the json cases, understood, never a
            # defect); a non-tripped span prints its max peak
            con_val = float(c[7]) if c[7] is not None else float(c[8])
            if abs(peak - con_val) < 5e-4:
                peak_ok += 1
            else:
                peak_diffs.append((key, s["src_doc"], con_val, peak))
    check("r2: EMISSION spans (lane-joined)", 145, n_emission)
    check("r2: trip-call agreement (145/145)", 290, trip_ok)  # 2 bars x 145
    check("r2: peak agreement exact", 137, peak_ok)
    check("r2: peak diffs all json (crossing value, never the max)",
          8, len(peak_diffs))
    check("r2: the 8 diffs' species all loop-seeded-json", True,
          all(d[1] == "loop-seeded-json" for d in peak_diffs))
    for d in sorted(peak_diffs):
        print("[r2]   crossing-vs-max (understood): %s console %s max %.4f"
              % (d[0], d[2], d[3]))

    # payload byte-identity across legs
    loop_same = loop_diff = clean_same = clean_diff = 0
    pcode = {s["doc_id"]: i for i, s in enumerate(
        [x for x in cache["CODE"]["docs"]])}
    pprose = {s["doc_id"]: i for i, s in enumerate(
        [x for x in cache["PROSE"]["docs"]])}
    span_index = {leg: {} for leg in ("CODE", "PROSE")}
    for leg in ("CODE", "PROSE"):
        for s in spans[leg]:
            span_index[leg][(s["doc_id"], s["si"])] = s
    for s in spans["CODE"]:
        twin = span_index["PROSE"].get((s["doc_id"].replace(
            "mix-CODE-", "mix-PROSE-"), s["si"]))
        if twin is None or twin["state"] != s["state"]:
            continue
        a = docs["CODE"][s["doc_id"]]["rows"][s["row0"]:s["row1"]]
        b = docs["PROSE"][twin["doc_id"]]["rows"][twin["row0"]:twin["row1"]]
        same = (len(a) == len(b) and all(
            json.dumps(x["payload"], sort_keys=True) ==
            json.dumps(y["payload"], sort_keys=True)
            for x, y in zip(a, b)))
        if s["state"] == "loop":
            loop_same, loop_diff = ((loop_same + 1, loop_diff) if same
                                    else (loop_same, loop_diff + 1))
        else:
            clean_same, clean_diff = ((clean_same + 1, clean_diff) if same
                                      else (clean_same, clean_diff + 1))
    check("r2: identity {loop_same, loop_diff, clean_same, clean_diff}",
          (45, 0, 0, 55), (loop_same, loop_diff, clean_same, clean_diff))

    # the W-lane census at EOS
    wz = {}
    for key, (s, comps) in by_key.items():
        wz[key] = comps["lane_z"]["W"]
    clean_w = sorted((v, k) for k, v in wz.items() if "clean" in con[k][4]
                     and k.startswith("PROSE"))
    loop_w = sorted((v, k) for k, v in wz.items() if con[k][4] == "loop")
    mism = sum(1 for k in wz if con[k][4] == "loop" and
               k.startswith("CODE") and
               abs(wz[k] - wz["PROSE " + k[5:].replace(
                   "mix-CODE-", "mix-PROSE-")]) > 1e-9)
    check("r2: cross-leg W-z mismatches (loop pairs)", 0, mism)
    check("r2: clean W-z max (mix-PROSE-A-01:s0)", 6.5889,
          round(clean_w[-1][0], 4), tol=1e-3)
    check("r2: clean W-z max holder", "PROSE mix-PROSE-A-01:s0",
          clean_w[-1][1])
    check("r2: loop W-z min", 2.1688, round(loop_w[0][0], 4), tol=1e-3)
    check("r2: clean spans with W-z above the loop min", 24,
          sum(1 for v, k in clean_w if v >= loop_w[0][0]))
    print("[r2] the W-alone negative receipt: a numeric W lane cannot "
          "meet the clean-specificity invariant (24 of 55 clean spans "
          "sit above the loop minimum)")

    # ---- r3: the 34 missed spans (species + per-lane decomposition) ----
    missed = []
    for key, (s, comps) in by_key.items():
        c = con[key]
        if con[key][4] == "loop" and c[6] is None:
            missed.append((key, s, comps))
    check("r3: missed spans (both legs)", 34, len(missed))
    sp_count = {}
    for key, s, comps in missed:
        sp_count[s["src_doc"]] = sp_count.get(s["src_doc"], 0) + 1
    check("r3: species census {injection-prose, stubborn, code-line}",
          (14, 12, 8), (sp_count.get("loop-injection-prose", 0),
                        sp_count.get("mask-reserved-stubborn", 0),
                        sp_count.get("loop-seeded-code-line", 0)))
    best = {key: max((h for h in comps if h != "lane_z"),
                     key=lambda h: comps[h]) for key, s, comps in missed}
    check("r3: all 34 missed spans peak at EOS", 34,
          sum(1 for k in best if best[k] == "EOS"))
    b06 = next((s, c) for key, s, c in missed
               if s["label"] == "mix-PROSE-B-06:s0")
    check("r3: B-06:s0 EOS composite", 1.9641,
          round(b06[1]["EOS"], 4), tol=2e-4)
    for lane, want in (("W", 5.41), ("s", 4.63), ("PR", 1.82),
                       ("E", -0.44), ("H", -1.60)):
        check("r3: B-06:s0 lane z %s" % lane, want,
              round(b06[1]["lane_z"][lane], 2), tol=5e-3)
    a06 = next((s, c) for key, (s, c) in by_key.items()
               if s["label"] == "mix-CODE-A-06:s1")
    check("r3: json contrast A-06:s1 EOS composite", 3.6883,
          round(a06[1]["EOS"], 4), tol=2e-4)
    check("r3: A-06:s1 all five lanes positive", 5,
          sum(1 for v in a06[1]["lane_z"].values() if v > 0))

    # the pinned loop criterion on the 34
    verdicts = {"loop-injection-prose": [0, 0], "mask-reserved-stubborn":
                [0, 0], "loop-seeded-code-line": [0, 0]}
    for key, s, comps in missed:
        sig = sig_of(s["walk_slice"]) if s["walk_slice"] is not None else None
        verdicts[s["src_doc"]][0 if sig is not None else 1] += 1
    check("r3: injection-prose LOOP / NO-LOOP", (14, 0),
          tuple(verdicts["loop-injection-prose"]))
    check("r3: stubborn LOOP / NO-LOOP", (12, 0),
          tuple(verdicts["mask-reserved-stubborn"]))
    check("r3: code-line LOOP / NO-LOOP", (0, 8),
          tuple(verdicts["loop-seeded-code-line"]))
    check("r3: banked species signatures", {
        "loop-injection-prose": (0, 2), "mask-reserved-stubborn": (4, 2),
        "loop-seeded-counter": (0, 2), "loop-seeded-cycle": (0, 3),
        "loop-seeded-countdown": None, "loop-seeded-json": None,
        "loop-injection-code": None, "loop-seeded-code-line": None},
        {k: banked.get(k) for k in (
            "loop-injection-prose", "mask-reserved-stubborn",
            "loop-seeded-counter", "loop-seeded-cycle",
            "loop-seeded-countdown", "loop-seeded-json",
            "loop-injection-code", "loop-seeded-code-line")})

    # ---- r3b: the theta lens + the two-tier criterion receipts ----
    # (his audit's defect-1 and defect-3, answered from the bytes)
    for leg in ("CODE", "PROSE"):
        check("r3b: %s FN @theta" % leg, 18,
              sum(1 for r in rows if r[0] == leg and r[4] == "loop"
                  and r[9] is None))
    tonly = [r for r in rows if r[4] == "loop" and r[6] is not None
             and r[9] is None]
    check("r3b: theta-only misses (both legs)", 2, len(tonly))
    check("r3b: the theta-only miss species all loop-injection-code", 2,
          sum(1 for r in tonly if r[5] == "loop-injection-code"))
    check("r3b: the theta-only miss peak 2.2621 (B-07:s0)", 2,
          sum(1 for r in tonly if abs(float(r[7]) - 2.2621) < 5e-4))
    b07 = next(s for s in spans["PROSE"]
               if s["label"] == "mix-PROSE-B-07:s0")
    check("r3b: B-07:s0 walk-id tier (no signature)", None,
          sig_of(b07["walk_slice"]) if b07["walk_slice"] is not None
          else None)
    b07_seq = [r["payload"].get("token", r["payload"].get("token_id"))
               for r in docs["PROSE"][b07["doc_id"]]["rows"][
                   b07["row0"]:b07["row1"]]]
    check("r3b: B-07:s0 content tier (no period)", None, sig_of(b07_seq))
    cl_none = 0
    for key, s, comps in missed:
        if s["src_doc"] != "loop-seeded-code-line":
            continue
        seq = [r["payload"].get("token") for r in
               docs[key.split()[0]][s["doc_id"]]["rows"][
                   s["row0"]:s["row1"]]]
        if sig_of(seq) is None:
            cl_none += 1
    check("r3b: code-line content tier: no period on all 8", 8, cl_none)
    cl0 = next((s for key, s, c in missed
                if s["src_doc"] == "loop-seeded-code-line"
                and key.startswith("PROSE")))
    seq0 = [r["payload"]["token"] for r in
            docs["PROSE"][cl0["doc_id"]]["rows"][cl0["row0"]:cl0["row1"]]]
    print("[r3b] code-line raw rows (%s, first 20, for your "
          "independent read): %s" % (cl0["label"], seq0[:20]))
    content_sigs = {}
    for leg in ("CODE", "PROSE"):
        for s in spans[leg]:
            if s["state"] != "loop" or s["src_doc"] in content_sigs:
                continue
            seq = [r["payload"].get("token") for r in
                   docs[leg][s["doc_id"]]["rows"][s["row0"]:s["row1"]]]
            content_sigs[s["src_doc"]] = sig_of(seq)
    check("r3b: two-tier species table (content tier, EMISSION rows)", {
        "loop-injection-code": None, "loop-injection-prose": (0, 2),
        "loop-seeded-code-line": None, "loop-seeded-countdown": (0, 5),
        "loop-seeded-counter": (0, 1), "loop-seeded-cycle": (0, 2),
        "loop-seeded-json": (0, 2), "mask-reserved-stubborn": (3, 1)},
        {k: content_sigs.get(k) for k in sorted(content_sigs)})
    tp_theta = sum(1 for r in rows if r[0] == "CODE" and r[4] == "loop"
                   and r[9] is not None)
    tp_2 = sum(1 for r in rows if r[0] == "CODE" and r[4] == "loop"
               and r[6] is not None)
    check("r3b: composite+signature coverage @[REDACTED_PER_PUBLICATION_POLICY] (per leg, 28+13)",
          41, tp_2 + 13)
    check("r3b: composite+signature coverage @theta (per leg, 27+13)",
          40, tp_theta + 13)
    check("r3b: honest TNs at theta (code-line 4 + B-07:s0 1)", 5,
          45 - (tp_theta + 13))
    check("r3b: clean census @theta (both legs)", 110,
          sum(1 for r in rows if r[4] == "clean" and r[9] is None))
    check("r3b: clean census @[REDACTED_PER_PUBLICATION_POLICY] (both legs, the 2 false trips)", 108,
          sum(1 for r in rows if r[4] == "clean" and r[6] is None))
    print("[r3b] the corrected coverage map: @[REDACTED_PER_PUBLICATION_POLICY] 41/45 loop per leg "
          "with clean 108/110; @theta 40/45 with clean 110/110; the "
          "5 unflagged at theta are the 4 code-line true negatives + "
          "B-07:s0 (injection-code, peak 2.2621, does-not-loop under "
          "the pinned criterion, both tiers None)")

    # ---- r4: the unconditional m(t) distributions ----
    def margin_seq(leg, s):
        rows_ = docs[leg][s["doc_id"]]["rows"][s["row0"]:s["row1"]]
        return [r["payload"]["margin"] for r in rows_]
    anchor_vals = {}
    for leg in ("CODE", "PROSE"):
        for s in spans[leg]:
            if s["state"] == "clean" and leg == "CODE":
                continue  # CODE-BAND clean: margin_content, a different
                          # surface, named honestly, never compared
            ms = margin_seq(leg, s)
            vals = {}
            for h in grid:
                if h != "EOS" and h >= s["n"]:
                    continue
                vals[h] = ms[h - 1] if h != "EOS" else ms[-1]
            anchor_vals["%s %s" % (leg, s["label"])] = (s["state"], vals)
    def dist(state, leg, h):
        xs = sorted(v[h] for k, (st, v) in anchor_vals.items()
                    if st == state and k.startswith(leg) and h in v)
        return xs
    for h, nclean, nloop in ((36, 47, 40), (64, 31, 35), (128, 25, 12),
                             ("EOS", 55, 45)):
        check("r4: PROSE clean n @%s" % h, nclean,
              len(dist("clean", "PROSE", h)))
        check("r4: PROSE loop n @%s" % h, nloop,
              len(dist("loop", "PROSE", h)))
        check("r4: clean max @%s (the loop side never clears it)" % h,
              1.0, round(max(dist("clean", "PROSE", h)), 4), tol=1e-4)
        check("r4: loop values >= clean max @%s" % h, 0,
              sum(1 for x in dist("loop", "PROSE", h)
                  if x >= max(dist("clean", "PROSE", h))))
    eos_clean = dist("clean", "PROSE", "EOS")
    eos_loop = dist("loop", "PROSE", "EOS")
    med = eos_clean[len(eos_clean) // 2]
    check("r4: PROSE clean EOS median", 0.9901, round(med, 4), tol=1e-4)
    check("r4: PROSE loop EOS mean", 0.9847,
          round(sum(eos_loop) / len(eos_loop), 4), tol=1e-4)
    check("r4: PROSE loop EOS min", 0.5406, round(eos_loop[0], 4), tol=1e-4)
    n03 = next(s for s in spans["PROSE"]
               if s["label"] == "mix-PROSE-N-03:s0")
    a06s = next(s for s in spans["PROSE"]
                if s["label"] == "mix-PROSE-A-06:s1")
    check("r4: E-event anchor receipt N-03:s0 row 40",
          0.06252540647983551, margin_seq("PROSE", n03)[40], tol=1e-15)
    check("r4: E-event anchor receipt A-06:s1 row 63",
          0.9996153712272644, margin_seq("PROSE", a06s)[63], tol=1e-15)
    print("[r4] zero separation: the loop margins sit entirely inside "
          "the clean distribution at every anchor -- margin is not a "
          "loop discriminator")

    # ---- r5: the signature channel's clean census (0/110) ----
    walk_tested = walk_trips = content_tested = content_trips = 0
    for leg in ("CODE", "PROSE"):
        for s in spans[leg]:
            if s["state"] != "clean":
                continue
            if s["walk_slice"] is not None:
                walk_tested += 1
                if any(conforms(s["walk_slice"], g) for g in
                       banked.values() if g is not None):
                    walk_trips += 1
            rows_ = docs[leg][s["doc_id"]]["rows"][s["row0"]:s["row1"]]
            content_tested += 1
            if leg == "CODE":
                seq = [r["payload"].get("token_id") for r in rows_]
            else:
                seq = [r["payload"].get("token") for r in rows_]
            if sig_of(seq) is not None:
                content_trips += 1
    check("r5: walk channel TESTED n (PROSE clean; CODE clean "
          "NAMED-ABSENT there)", 55, walk_tested)
    check("r5: walk channel trips (0/55 tested)", 0, walk_trips)
    check("r5: content channel TESTED n (both legs)", 110, content_tested)
    check("r5: content channel trips (0/110)", 0, content_trips)
    print("[r5] the signature channel's clean census, denominators "
          "honest: walk-id channel 0/55 TESTED (the 55 CODE-BAND "
          "clean spans carry no walk ids -- NAMED-ABSENT on that "
          "channel, never tested there); content channel 0/110 both "
          "legs")

    # ---- the verdict table ----
    n_pass = sum(1 for c in CHECKS if c[3])
    print("\n[checks] %d/%d landed" % (n_pass, len(CHECKS)))
    for name, exp, got, ok in CHECKS:
        if not ok:
            print("[checks] FAILED: %s (expected %s, got %s)"
                  % (name, exp, got))
    if n_pass != len(CHECKS):
        sys.exit("[checks] NOT every check landed -- the readout does "
                 "not stand as banked; nothing may be adjudicated on "
                 "these bytes")
    print("[checks] every readout receipt reproduced exact -- the "
          "Act-2b readout stands on YOUR OWN RUN (findings presented, "
          "never adjudicated -- the owner's stamps decide)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("prep", "read", "all"),
                    default="all")
    ap.add_argument("--root", default="",
                    help="an extra directory to search for the inputs "
                         "(any layout; the sha256 decides, the directory "
                         "never does)")
    ap.add_argument("--instruments", default="",
                    help="an extra directory to search for the seven "
                         "co-location files (six instruments + the "
                         "stage-1 engines)")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    roots = [os.path.abspath(os.getcwd()), here]
    for extra in (a.root, a.instruments,
                  os.environ.get("INSTRUMENTS_DIR", "")):
        if extra:
            r = os.path.abspath(extra)
            if r not in roots:
                roots.append(r)
    paths = discover(roots)
    cache_path = os.path.join(here, "act2b_his_run_ctx.pkl")
    if a.stage in ("prep", "all"):
        do_prep(paths, cache_path)
    if a.stage in ("read", "all"):
        if a.stage == "read" and not os.path.isfile(cache_path):
            sys.exit("[read] no prep cache -- run --stage prep first")
        do_read(cache_path)

if __name__ == "__main__":
    main()

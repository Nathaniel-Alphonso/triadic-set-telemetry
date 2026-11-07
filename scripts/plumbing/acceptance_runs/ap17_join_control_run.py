#!/usr/bin/env python3
# ============================================================
# ap17_join_control_run.py -- THE 17-AP JOIN CONTROL RUN
# (the item-255 control pattern; zero-GPU; zero imports from the
# tool or the acceptance runner -- this script's OWN code only)
# ============================================================
# Independently recomputes EVERY population doc-for-doc from the
# RAW inputs of a control-built synthetic capture world (a
# DIFFERENT world than the acceptance world -- different docs,
# different walks, different value regime) and compares EXACT
# against the join tool's readout JSON: the M-AP1 parity
# doc-for-doc, the doc-level scalars through every M-AP2 class
# and group table, every M-AP3 separation (gap, AUC, class) via
# this script's OWN algebra (brute-force AUC, its own direction
# sheet, its own bar/jitter/guard typing), the R-AP2 loop
# separations, the M-AP4 envelope, the M-AP5 floor census, every
# M-AP6 band table and band separation, and the R-AP mapping
# numbers. Re-proves determinism byte-identically.
#
# theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, or
# adjudicated; findings presented, never adjudicated -- the
# my stamps decide.
# ============================================================
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_ap17_join.py")
PY = sys.executable

PASS, FAIL = [], []


def check(name, cond, detail=""):
    if cond:
        PASS.append(name)
        print(f"PASS  {name}" + (f"  -- {detail}" if detail else ""))
    else:
        FAIL.append(name)
        print(f"FAIL  {name}  {detail}")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


# ==========================================
# THE CONTROL WORLD (its own builder; a different population,
# different walks, different value regime than the acceptance
# world; deterministic LCG values, no randomness)
# ==========================================
LEGS = ("gsmrw17", "mbpprw17", "prose17p-rw17", "p2corpus-rw17")
SCHEMA = {"gsmrw17": "gsm8k-rw17-v1", "mbpprw17": "mbpp-rw17-v1",
          "prose17p-rw17": "prose17p-rw17-v1",
          "p2corpus-rw17": "p2corpus-rw17-v1"}
N_LAYERS = 16

# the loop fixtures riding EVERY control cache (the real-bytes law
# my first REAL run caught: the same loop fixtures ride
# every fresh1 cache, byte-identical within the set -- the control
# world carries its OWN fixture set, 3 fixtures, byte-identical
# across all four of its caches)
CTRL_LOOP_FIXTURES = (
    ("loop-fixture-kappa", 5),
    ("loop-fixture-lambda", 7),
    ("loop-fixture-mu", 9))


def loop_fixture_lines():
    """The fixture records, byte-identical for every cache."""
    out = []
    for j, (fid, n) in enumerate(CTRL_LOOP_FIXTURES):
        rec = {"key": f"loop:{fid}", "leg": "loop", "doc_id": fid,
               "bos": True, "instrument": "t2-fixture",
               "prompt_len": 12, "stop_reason": "cap",
               "n_gen_steps": n, "n_content_steps": n,
               "walk_ids": [4440 + j * 7 + i * 3
                            for i in range(n)],
               "steps": {}, "commits": [], "hidden_n": 0,
               "hidden_dim": 0, "hidden_b64": ""}
        out.append(json.dumps(rec, sort_keys=True))
    return out


def _lcg(seed):
    s = seed
    while True:
        s = (s * 1103515245 + 12345) % (2 ** 31)
        yield s


def _vals(seed, n):
    """n deterministic per-step [0,1) values (6-decimal quanta)."""
    g = _lcg(seed)
    return [((next(g) % 1000000) / 1000000.0) for _ in range(n)]


# (capture_id, leg, doc_id, class, n_gen, spanned, stop, diverge)
# diverge: None | ("pos", i) | ("len", delta) | ("clean", None)
def control_world():
    rows = []
    cid = 0
    # D: 6 loop-live + 6 mbpp-degenerate (one divergent-in-place,
    # one n=3 sub-minimum) + 6 prose-repetition (one divergent
    # clean -> the R reclassification)
    for i in range(6):
        rows.append((cid, "loop", None, "loop-live", 9 + 11 * i,
                     True, "cap", None)); cid += 1
    for i in range(6):
        dv = ("pos", 3) if i == 2 else None
        n = 3 if i == 4 else 14 + 13 * i
        rows.append((cid, "mbpprw17", 600 + i,
                     "mbpp-degenerate-fired", n, i != 5, "cap",
                     dv)); cid += 1
    for i in range(6):
        dv = ("clean", None) if i == 3 else None
        rows.append((cid, "prose17p-rw17", 700 + i,
                     "prose-repetition-fired", 8 + 9 * i,
                     i % 2 == 0, "eos" if i % 3 else "cap",
                     dv)); cid += 1
    # B: gsm-boundary 5, gsm-benign 5 (one length-divergent),
    # p2-spike0 6 (one divergent in place)
    for i in range(5):
        rows.append((cid, "gsmrw17", 500 + i, "gsm-boundary-fired",
                     12 + 5 * i, False, "eos", None)); cid += 1
    for i in range(5):
        dv = ("len", 3) if i == 1 else None
        rows.append((cid, "gsmrw17", 550 + i,
                     "gsm-benign-spike-fired", 10 + 6 * i, True,
                     "cap", dv)); cid += 1
    for i in range(6):
        dv = ("pos", 0) if i == 5 else None
        rows.append((cid, "p2corpus-rw17", 800 + i,
                     "p2-spike0-fired", 7 + 8 * i, i % 3 == 0,
                     "eos", dv)); cid += 1
    # U: mbpp-fired-other 4, prose-other-fired 4 (one n=2
    # sub-minimum, both below the 5-doc guard -> the S3a/S3b
    # constituent guard fires in this world)
    for i in range(4):
        n = 2 if i == 3 else 11 + 6 * i
        rows.append((cid, "mbpprw17", 660 + i, "mbpp-fired-other",
                     n, False, "eos", None)); cid += 1
    for i in range(4):
        rows.append((cid, "prose17p-rw17", 760 + i,
                     "prose-other-fired", 13 + 7 * i, False,
                     "eos", None)); cid += 1
    # C: clean 6 per leg (one gsm n=1 sub-minimum; one p2
    # zero-step)
    for i in range(6):
        n = 1 if i == 5 else 16 + 9 * i
        rows.append((cid, "gsmrw17", 590 + i, "clean-gsm", n,
                     False, "eos", None)); cid += 1
    for i in range(6):
        rows.append((cid, "mbpprw17", 690 + i, "clean-mbpp",
                     15 + 8 * i, i % 2 == 1, "eos", None)); cid += 1
    for i in range(6):
        rows.append((cid, "prose17p-rw17", 790 + i, "clean-prose",
                     18 + 7 * i, False, "eos", None)); cid += 1
    for i in range(6):
        n = 0 if i == 2 else 20 + 6 * i
        rows.append((cid, "p2corpus-rw17", 890 + i, "clean-p2", n,
                     False, "eos", None)); cid += 1
    return rows


WORLD = control_world()
GROUP_OF = {"loop-live": "D", "mbpp-degenerate-fired": "D",
            "prose-repetition-fired": "D", "gsm-boundary-fired": "B",
            "gsm-benign-spike-fired": "B", "p2-spike0-fired": "B",
            "mbpp-fired-other": "U", "prose-other-fired": "U",
            "clean-gsm": "C", "clean-mbpp": "C", "clean-p2": "C",
            "clean-prose": "C"}


def walk_of(doc_id, n):
    base = 5000 + (doc_id or 0) * 11
    return [base + i * 5 for i in range(n)]


def features_of(cid, doc_id, n, spanned, cls):
    """The control world's own feature series (LCG-deterministic;
    F2b null on unspanned steps only)."""
    g = _lcg(977 + cid * 31 + (doc_id or 0))
    feats = {"F1": [], "F2a": [], "F2b": [], "F3": [], "F4": []}
    spans = []
    for t in range(n):
        row = {k: ((next(g) % 1000000) / 1000000.0)
               for k in ("F1", "F2a", "F3", "F4")}
        has_span = spanned and (t % 3) == 1
        row["F2b"] = ((next(g) % 1000000) / 1000000.0) \
            if has_span else None
        spans.append([max(0, t - 2), t] if has_span else None)
        for k in ("F1", "F2a", "F2b", "F3", "F4"):
            feats[k].append([row[k]] * N_LAYERS)
    return feats, spans


def build_world(d):
    entries = []
    for (cid, leg, doc, cls, n, spanned, stop, dv) in WORLD:
        e = {"capture_id": cid, "class": cls, "leg": leg}
        if leg == "loop":
            e["fixture"] = f"loop-{chr(ord('a') + cid % 6)}"
        else:
            e["doc_id"] = doc
            e["schema"] = SCHEMA[leg]
        entries.append(e)
    census = {}
    for e in entries:
        census[e["class"]] = census.get(e["class"], 0) + 1
    man = {"format": "ap17-capture-manifest-v1",
           "class_census": census, "entries": entries,
           "n_entries": len(entries), "seed": 20261016}
    mp = os.path.join(d, "manifest.json")
    with open(mp, "w") as f:
        f.write(json.dumps(man, sort_keys=True, indent=1) + "\n")
    man_sha = sha256_file(mp)

    lines = []
    for (cid, leg, doc, cls, n, spanned, stop, dv) in WORLD:
        feats, spans = features_of(cid, doc, n, spanned, cls)
        rec = {"format": "ap17-capture-v1", "tag": "control",
               "instrument": "t2-fixture", "model": "fixture-1b",
               "tool_sha256": "0" * 64, "manifest": "manifest.json",
               "manifest_sha256": man_sha, "fixture_mode": True,
               "capture_id": cid, "leg": leg, "class": cls,
               "doc_id": doc,
               "fixture": f"loop-{chr(ord('a') + cid % 6)}"
                          if leg == "loop" else None,
               "schema": SCHEMA[leg] if leg != "loop" else None,
               "evidence_spans": None, "n_layers": N_LAYERS,
               "prompt_len": 12, "stop_reason": stop,
               "n_gen_steps": n, "n_content_steps": n,
               "walk_ids": walk_of(doc, n), "emission_text": "y" * 5,
               "span_windows": spans, "features": feats}
        lines.append(json.dumps(rec, sort_keys=True))
    ep = os.path.join(d, "export.jsonl")
    with open(ep, "w") as f:
        f.write("\n".join(lines) + "\n")

    for leg in LEGS:
        clines = []
        for (cid, cleg, doc, cls, n, spanned, stop, dv) in WORLD:
            if cleg != leg:
                continue
            wids = walk_of(doc, n)
            cache_n, cache_wids = n, wids
            if dv is not None:
                if dv[0] == "pos":
                    cache_wids = list(wids)
                    cache_wids[dv[1]] += 1
                elif dv[0] == "len":
                    cache_n = n + dv[1]
                    cache_wids = walk_of(doc, cache_n)
                elif dv[0] == "clean":
                    cache_wids = [w + 2 for w in wids]
            rec = {"key": f"{leg}:{doc}", "leg": leg, "doc_id": doc,
                   "bos": True, "instrument": "t2-fixture",
                   "prompt_len": 12, "stop_reason": stop,
                   "n_gen_steps": cache_n,
                   "n_content_steps": cache_n,
                   "walk_ids": cache_wids, "steps": {},
                   "commits": [], "hidden_n": 0, "hidden_dim": 0,
                   "hidden_b64": ""}
            clines.append(json.dumps(rec, sort_keys=True))
        if leg == "gsmrw17":
            # an extra doc outside the manifest (streaming-keep)
            clines.append(json.dumps(
                {"key": "gsmrw17:599", "leg": leg, "doc_id": 599,
                 "bos": True, "instrument": "t2-fixture",
                 "prompt_len": 12, "stop_reason": "eos",
                 "n_gen_steps": 4, "n_content_steps": 4,
                 "walk_ids": walk_of(599, 4), "steps": {},
                 "commits": [], "hidden_n": 0, "hidden_dim": 0,
                 "hidden_b64": ""}, sort_keys=True))
            # one "empty":true excluded record
            clines.append(json.dumps({"empty": True,
                                      "key": "gsmrw17:999"},
                                     sort_keys=True))
        # the loop fixtures ride EVERY cache, byte-identical (the
        # real-bytes law; streamed past, never a population record)
        clines.extend(loop_fixture_lines())
        with open(os.path.join(d, f"cache_{leg}.jsonl"), "w") as f:
            f.write("\n".join(clines) + "\n")
    return mp, ep


# ==========================================
# THE CONTROL'S OWN INDEPENDENT RECOMPUTATION
# (its own code only; never the tool's)
# ==========================================
def _mean(v):
    return sum(v) / len(v) if v else None


def _std(v):
    if len(v) < 2:
        return None
    m = _mean(v)
    return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5


def _table(v):
    return {"n": len(v), "mean": _mean(v), "std": _std(v),
            "min": min(v) if v else None,
            "max": max(v) if v else None}


def sgap(pos, neg):
    if not pos or not neg:
        return None
    mp_, mn_ = _mean(pos), _mean(neg)
    sp = _std(pos)
    sn = _std(neg)
    pooled = math.sqrt(((sp or 0.0) ** 2 + (sn or 0.0) ** 2) / 2.0)
    return (mp_ - mn_) / pooled if pooled > 0 else 0.0


def auc_pairs(pos, neg):
    if not pos or not neg:
        return None
    tot = win = 0.0
    for p in pos:
        for q in neg:
            tot += 1
            win += 1.0 if p > q else (0.5 if p == q else 0.0)
    return win / tot


POP_GUARD_MIN = 5
BAR = 2.0
JITTER = 0.02

# the control's OWN direction sheet (independently hardcoded)
DIRS = {
    "F1": {"S1": ("C", "D", "COMMITTED"),
           "S2": ("C", "B", "NONE"),
           "S3": ("B", "D", "BY-CLASS-TABLE"),
           "S3a": ("B", "D+U", "BY-CLASS-TABLE"),
           "S3b": ("B+U", "D", "BY-CLASS-TABLE")},
    "F2a": {"S1": ("D", "C", "COMMITTED"),
            "S2": ("B", "C", "NONE"),
            "S3": ("D", "B", "COMMITTED"),
            "S3a": ("D+U", "B", "COMMITTED"),
            "S3b": ("D", "B+U", "COMMITTED")},
    "F3": {"S1": ("C", "D", "COMMITTED"),
           "S2": ("C", "B", "NONE"),
           "S3": ("B", "D", "BY-CLASS-TABLE"),
           "S3a": ("B", "D+U", "BY-CLASS-TABLE"),
           "S3b": ("B+U", "D", "BY-CLASS-TABLE")},
    "F4": {"S1": ("D", "C", "NONE"),
           "S2": ("B", "C", "NONE"),
           "S3": ("D", "B", "NONE"),
           "S3a": ("D+U", "B", "NONE"),
           "S3b": ("D", "B+U", "NONE")},
}
SCALAR_OF = {"F1": "F1", "F2a": "F2a", "F3": "F3", "F4": "F4_mean"}
BANDKEY_OF = {"F1": "F1", "F2a": "F2a", "F3": "F3", "F4": "F4"}
SEPS = ("S1", "S2", "S3", "S3a", "S3b")
FEATURES = ("F1", "F2a", "F3", "F4")
BANDS = ("early", "middle", "late")


def typing_of(gap, n_pos, n_neg, commit):
    """The control's own bar typing (2.0 bar, +/-0.02 jitter,
    POP_GUARD_MIN=5; WRONG-DIRECTION in committed directions)."""
    if n_pos < POP_GUARD_MIN or n_neg < POP_GUARD_MIN:
        return "INCONCLUSIVE-POPULATION-GUARD"
    if gap is None:
        return "INCONCLUSIVE-EMPTY-POPULATION"
    if commit == "NONE":
        g = abs(gap)
        if g >= BAR:
            return "NO-COMMITTED-DIRECTION/PASS_2SIGMA"
        if g >= BAR - JITTER:
            return "NO-COMMITTED-DIRECTION/INCONCLUSIVE-FROM-JITTER"
        return "NO-COMMITTED-DIRECTION/FAIL"
    if gap <= -BAR:
        return "WRONG-DIRECTION"
    if gap >= BAR:
        return "PASS_2SIGMA"
    if gap >= BAR - JITTER:
        return "INCONCLUSIVE-FROM-JITTER"
    return "FAIL"


def band_edges(n):
    return (0, n // 4, (3 * n) // 4, n)


def doc_scalars_own(rec):
    """The control's own doc-level construction (the stamped join
    spec S4, independently coded)."""
    n = rec["n_gen_steps"]
    out = {"capture_id": rec["capture_id"], "doc_id": rec["doc_id"],
           "leg": rec["leg"], "class": rec["class"],
           "group": GROUP_OF[rec["class"]], "n": n,
           "bands": {}, "head": {}, "floor": {},
           "f1_layers": {}}
    if n == 0:
        out["floor"]["zero_step"] = True
        return out
    F = rec["features"]
    e0, e1, e2, e3 = band_edges(n)
    ranges = {"early": (e0, e1), "middle": (e1, e2),
              "late": (e2, e3)}
    for band in BANDS:
        lo, hi = ranges[band]
        out["bands"][band] = {}
        if hi <= lo:
            out["floor"]["empty_" + band] = True
            for k in ("F1", "F2a", "F2b", "F3", "F4"):
                out["bands"][band][k] = None
            out["bands"][band]["F4_std"] = None
            out["f1_layers"][band] = [None] * N_LAYERS
            continue
        for k in ("F1", "F2a", "F2b", "F3", "F4"):
            per = []
            for l in range(N_LAYERS):
                col = [F[k][t][l] for t in range(lo, hi)
                       if F[k][t][l] is not None]
                if not col:
                    per.append(None)
                elif k in ("F1", "F3"):
                    per.append(min(col))
                elif k in ("F2a", "F2b"):
                    per.append(max(col))
                else:
                    per.append(sum(col) / len(col))
            have = [v for v in per if v is not None]
            out["bands"][band][k] = (sum(have) / len(have)
                                     if have else None)
        pool = [F["F4"][t][l] for t in range(lo, hi)
                for l in range(N_LAYERS)
                if F["F4"][t][l] is not None]
        out["bands"][band]["F4_std"] = _std(pool)
        f1l = []
        for l in range(N_LAYERS):
            col = [F["F1"][t][l] for t in range(lo, hi)
                   if F["F1"][t][l] is not None]
            f1l.append(min(col) if col else None)
        out["f1_layers"][band] = f1l
    flat = lambda k: [v for st in F[k] for v in st
                      if v is not None]   # noqa: E731
    out["head"]["F1"] = min(flat("F1")) if flat("F1") else None
    out["head"]["F2a"] = max(flat("F2a")) if flat("F2a") else None
    out["head"]["F2b"] = max(flat("F2b")) if flat("F2b") else None
    out["head"]["F3"] = min(flat("F3")) if flat("F3") else None
    f4 = flat("F4")
    out["head"]["F4_mean"] = _mean(f4)
    out["head"]["F4_std"] = _std(f4)
    if out["head"]["F2b"] is None:
        out["floor"]["no_span"] = True
    if n < 4:
        out["floor"]["sub_minimum_window"] = True
    return out


def recompute(d):
    """Everything from the raw files, with this script's code."""
    with open(os.path.join(d, "manifest.json")) as f:
        man = json.load(f)
    recs = {}
    with open(os.path.join(d, "export.jsonl")) as f:
        for line in f:
            s = line.strip()
            if s:
                r = json.loads(s)
                recs[r["capture_id"]] = r
    caches = {}
    empty_form = {"gsmrw17": 0, "mbpprw17": 0,
                  "prose17p-rw17": 0, "p2corpus-rw17": 0}
    n_records = {}
    zero_census = {}
    n_loop_recs = {}
    loop_ids = {}
    for leg in LEGS:
        caches[leg] = {}
        n_records[leg] = 0
        zero_census[leg] = 0
        n_loop_recs[leg] = 0
        loop_ids[leg] = set()
        with open(os.path.join(d, f"cache_{leg}.jsonl")) as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                c = json.loads(s)
                if c.get("empty") is True:
                    empty_form[leg] += 1
                    continue
                n_records[leg] += 1
                if c["leg"] == "loop":
                    # the loop law: streamed past, never a corpus
                    # population record, censused separately
                    n_loop_recs[leg] += 1
                    loop_ids[leg].add(c["doc_id"])
                    continue
                caches[leg][c["doc_id"]] = c
                if c["n_gen_steps"] == 0:
                    zero_census[leg] += 1
    # parity doc-for-doc
    parity = {}
    for e in man["entries"]:
        cid = e["capture_id"]
        if e["leg"] == "loop":
            parity[cid] = ("EXEMPT", None, None, None)
            continue
        r = recs[cid]
        c = caches[e["leg"]][e["doc_id"]]
        if r["n_gen_steps"] == 0 and c["n_gen_steps"] == 0:
            parity[cid] = ("IDENTICAL-BY-ZERO", None,
                           r["n_gen_steps"], c["n_gen_steps"])
            continue
        a, b = r["walk_ids"], c["walk_ids"]
        first = None
        for i in range(min(len(a), len(b))):
            if a[i] != b[i]:
                first = i
                break
        if first is None and len(a) != len(b):
            first = min(len(a), len(b))
        p = "DIVERGENT" if first is not None else "IDENTICAL"
        parity[cid] = (p, first, r["n_gen_steps"],
                       c["n_gen_steps"])
    # doc scalars + the R reclassification (independent)
    docs = {}
    for e in man["entries"]:
        docs[e["capture_id"]] = doc_scalars_own(recs[e["capture_id"]])
    for cid, (p, first, nc, nk) in parity.items():
        if p != "DIVERGENT":
            continue
        r = recs[cid]
        rep = any(sp is not None for sp in r["span_windows"])
        ctype = ("CLEAN-EMISSION" if not rep else
                 "DEGENERATE-EMISSION" if r["stop_reason"] == "cap"
                 else "MILD-REPETITION"
                 if r["stop_reason"] == "eos"
                 else "REPETITION-UNEXPECTED-STOP")
        if GROUP_OF[r["class"]] == "D" and ctype == "CLEAN-EMISSION":
            docs[cid]["group"] = "R"
            docs[cid]["retype"] = ctype
        else:
            docs[cid]["retype"] = ctype if p == "DIVERGENT" else None
    return man, recs, caches, docs, parity, \
        empty_form, n_records, zero_census, n_loop_recs, loop_ids


def run_tool(d, out, tag):
    args = [PY, TOOL, "--fixture-mode", "--tag", tag,
            "--out", os.path.join(d, out),
            "--export", os.path.join(d, "export.jsonl"),
            "--manifest", os.path.join(d, "manifest.json")]
    for leg in LEGS:
        args += ["--cache", os.path.join(d, f"cache_{leg}.jsonl")]
    return subprocess.run(args, capture_output=True, text=True)


def close(a, b, tol=1e-12):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= tol


def main():
    tmp = tempfile.mkdtemp(prefix="ap17join_ctrl_")
    d1 = os.path.join(tmp, "w1")
    os.makedirs(d1)
    print("=== THE 17-AP JOIN CONTROL RUN (its own code; a "
          "different world; EXACT vs the tool's readout) ===")
    print(f"  tool: {TOOL}")
    print(f"  tool sha256: {sha256_file(TOOL)}")
    print()
    build_world(d1)
    p = run_tool(d1, "ro.json", "ctrl")
    check("C1 the tool runs console-clean on the CONTROL world "
          "(a different population, different walks, different "
          "value regime)", p.returncode == 0, p.stderr[-400:])
    if p.returncode != 0:
        print(p.stdout[-2000:])
        shutil.rmtree(tmp, ignore_errors=True)
        return 1
    ro = json.load(open(os.path.join(d1, "ro.json")))
    man, recs, caches, docs, parity, empty_form, n_records, \
        zero_census, n_loop_recs, loop_ids = recompute(d1)

    # ---- C2: M-AP1 parity doc-for-doc EXACT ----
    pd = {r["capture_id"]: r for r in ro["map1_per_doc"]}
    ok = True
    for cid, (pp, first, nc, nk) in parity.items():
        g = pd[cid]
        if g["parity"] != pp or \
                g.get("first_divergence_position") != first:
            ok = False
        if pp not in ("EXEMPT", "IDENTICAL-BY-ZERO"):
            if g["n_gen_steps_capture"] != nc or \
                    g["n_gen_steps_cache"] != nk:
                ok = False
    n_div = sum(1 for v in parity.values()
                if v[0] == "DIVERGENT")
    check("C2 M-AP1 parity doc-for-doc EXACT vs the control's "
          "own recomputation (identical / divergent / first "
          "position / zero-step / loop exemption; "
          f"{n_div} divergent)", ok and
          ro["map1_parity"]["n_divergent"] == n_div and
          ro["map1_parity"]["n_corpus_docs"] ==
          sum(1 for e in man["entries"] if e["leg"] != "loop"))

    # ---- C3: the reclassification (independent) ----
    rdocs = [cid for cid, d in docs.items()
             if d["group"] == "R"]
    ok = sorted(r["capture_id"] for r in
                ro["reclassified_docs"]) == sorted(rdocs) and \
        len(rdocs) >= 1
    for cid in rdocs:
        g = pd[cid]
        ok = ok and g.get("reclassified", {}) \
            .get("to_group") == "R" and \
            g.get("capture_emission_retype", {}) \
            .get("census_type") == "CLEAN-EMISSION"
    check("C3 the R reclassification EXACT (every D-group "
          "divergent doc whose capture emission walks clean is "
          "reclassified D->R, disclosed and named; every other "
          "divergent doc re-typed on its own emission with its "
          "grouping law STANDING)", ok)

    # ---- C4: M-AP2 tables EXACT (class + group, every scalar,
    # every cell) via the control's own doc scalars ----
    def heads(cids, key):
        return [docs[c]["head"][key] for c in cids
                if docs[c]["n"] > 0
                and docs[c]["head"].get(key) is not None]

    classes = {}
    groups = {}
    for e in man["entries"]:
        classes.setdefault(e["class"], []).append(e["capture_id"])
        groups.setdefault(docs[e["capture_id"]]["group"],
                          []).append(e["capture_id"])
    ok = True
    for cls, cids in classes.items():
        for key in ("F1", "F2a", "F2b", "F3", "F4_mean", "F4_std"):
            exp = _table(heads(cids, key))
            got = ro["map2_scalar_tables"][cls][key]
            for f in ("n", "mean", "std", "min", "max"):
                if not close(exp[f], got[f]):
                    ok = False
    for g, cids in groups.items():
        for key in ("F1", "F2a", "F2b", "F3", "F4_mean", "F4_std"):
            exp = _table(heads(cids, key))
            got = ro["map2_scalar_tables"]["group-" + g][key]
            for f in ("n", "mean", "std", "min", "max"):
                if not close(exp[f], got[f]):
                    ok = False
    check("C4 M-AP2 every class AND group table EXACT vs the "
          "control's own doc-level recomputation (every scalar, "
          "every cell, 12 classes + 5 groups)", ok)

    # ---- C5: M-AP3 separations EXACT (gap via the control's
    # own algebra, AUC via brute-force pair counting, class via
    # the control's own typing + direction sheet) ----
    def union(label):
        out = []
        for g in label.split("+"):
            out.extend(groups.get(g, []))
        return out

    def guard_fails(label, has):
        return [(g, sum(1 for c in groups.get(g, []) if has(c)))
                for g in label.split("+")]

    ok = True
    for sep in SEPS:
        for f in FEATURES:
            scalar = SCALAR_OF[f]
            pos_l, neg_l, commit = DIRS[f][sep]
            has = (lambda c, s=scalar:
                   docs[c]["head"].get(s) is not None)
            pos = heads(union(pos_l), scalar)
            neg = heads(union(neg_l), scalar)
            eg = sgap(pos, neg)
            ea = auc_pairs(pos, neg)
            gf = [x for x in guard_fails(pos_l, has)
                  if x[1] < POP_GUARD_MIN] + \
                 [x for x in guard_fails(neg_l, has)
                  if x[1] < POP_GUARD_MIN]
            et = ("INCONCLUSIVE-POPULATION-GUARD" if gf else
                  typing_of(eg, len(pos), len(neg), commit))
            b = ro["map3_separations"][sep][scalar]
            if not close(b["gap"], eg) or not close(b["auc"], ea):
                ok = False
                print(f"    mismatch {sep}/{scalar}: gap "
                      f"{b['gap']} vs {eg}, auc {b['auc']} vs {ea}")
            if b["class"] != et:
                ok = False
                print(f"    class mismatch {sep}/{scalar}: "
                      f"{b['class']} vs {et}")
            if (b["pos_side"], b["neg_side"]) != (pos_l, neg_l):
                ok = False
    check("C5 every M-AP3 separation EXACT vs the control's own "
          "algebra (gap, brute-force AUC, committed sides, the "
          "bar/jitter/guard/WRONG-DIRECTION typing; this world's "
          "groups all sit above the population guard -- the "
          "below-guard firing is exercised on the acceptance "
          "world)", ok)

    # ---- C6: the R-AP2 loop separations EXACT ----
    loop_cids = [e["capture_id"] for e in man["entries"]
                 if e["leg"] == "loop"]
    ok = True
    for key, neg_g, sep_name in (("LOOP-VS-C", "C", "S1"),
                                 ("LOOP-VS-B", "B", "S3")):
        for f in FEATURES:
            scalar = SCALAR_OF[f]
            pos = heads(loop_cids, scalar)
            neg = heads(groups.get(neg_g, []), scalar)
            eg = sgap(pos, neg)
            ea = auc_pairs(pos, neg)
            n_loop = len(pos)
            et = ("INCONCLUSIVE-POPULATION-GUARD"
                  if n_loop < POP_GUARD_MIN else
                  typing_of(eg, len(pos), len(neg),
                            DIRS[f][sep_name][2]))
            b = ro["loop_class_separations"][key][scalar]
            if not close(b["gap"], eg) or not close(b["auc"], ea) \
                    or b["class"] != et:
                ok = False
    check("C6 the R-AP2 loop-class separations EXACT (loop-live "
          "vs C, loop-live vs B; the control's own algebra)",
          ok)

    # ---- C7: M-AP4 envelope EXACT ----
    ok = True
    for band in BANDS:
        vals = []
        for c in groups.get("C", []):
            dx = docs[c]
            if dx["n"] == 0 or ("empty_" + band) in dx["floor"]:
                continue
            for l in range(N_LAYERS):
                v = dx["f1_layers"][band][l]
                if v is not None:
                    vals.append(v)
        exp = _table(vals)
        got = ro["map4_envelope"][band]["across_layers"]
        for f in ("n", "mean", "std", "min", "max"):
            if not close(exp[f], got[f]):
                ok = False
        for l in range(N_LAYERS):
            lv = [docs[c]["f1_layers"][band][l]
                  for c in groups.get("C", [])
                  if docs[c]["n"] > 0
                  and ("empty_" + band) not in docs[c]["floor"]
                  and docs[c]["f1_layers"][band][l] is not None]
            exp_l = _table(lv)
            got_l = ro["map4_envelope"][band]["per_layer"] \
                [f"layer_{l}"]
            for f in ("n", "mean", "std", "min", "max"):
                if not close(exp_l[f], got_l[f]):
                    ok = False
    check("C7 M-AP4 the healthy-walk envelope EXACT (per band, "
          "per layer AND across layers; the control's own "
          "recomputation)", ok)

    # ---- C8: M-AP5 floor census EXACT ----
    z_ids = sorted(c for c, d in docs.items()
                   if d["floor"].get("zero_step"))
    ns_ids = sorted(c for c, d in docs.items()
                    if d["floor"].get("no_span"))
    sm_ids = sorted(c for c, d in docs.items()
                    if d["floor"].get("sub_minimum_window"))
    m5 = ro["map5_floor_census"]
    ok = m5["zero_step_records"]["n"] == len(z_ids) and \
        sorted(x["capture_id"] for x in
               m5["zero_step_records"]["docs"]) == z_ids and \
        m5["no_span_docs_F2b"]["n"] == len(ns_ids) and \
        sorted(x["capture_id"] for x in
               m5["no_span_docs_F2b"]["docs"]) == ns_ids and \
        m5["sub_minimum_window_docs"]["n"] == len(sm_ids) and \
        sorted(x["capture_id"] for x in
               m5["sub_minimum_window_docs"]["docs"]) == sm_ids
    check("C8 M-AP5 the fails-open floor census EXACT (every "
          "zero-step, NO-SPAN and sub-minimum-window doc named "
          "doc-for-doc)", ok)

    # ---- C9: M-AP6 band tables + band separations EXACT ----
    ok = True
    for band in BANDS:
        for name, cids in list(classes.items()) + \
                [("group-" + g, groups[g]) for g in
                 ("D", "B", "U", "C", "R")]:
            for key in ("F1", "F2a", "F2b", "F3", "F4", "F4_std"):
                vals = []
                for c in cids:
                    dx = docs[c]
                    if dx["n"] == 0 or \
                            ("empty_" + band) in dx["floor"]:
                        continue
                    v = dx["bands"].get(band, {}).get(key)
                    if v is not None:
                        vals.append(v)
                exp = _table(vals)
                got = ro["map6_bands"][band]["tables"][name] \
                    [key if key != "F4" else "F4_mean"]
                for f in ("n", "mean", "std", "min", "max"):
                    if not close(exp[f], got[f]):
                        ok = False
        for sep in SEPS:
            for f in FEATURES:
                scalar = SCALAR_OF[f]
                bkey = BANDKEY_OF[f]
                pos_l, neg_l, commit = DIRS[f][sep]

                def bvals(label):
                    out = []
                    for g in label.split("+"):
                        for c in groups.get(g, []):
                            dx = docs[c]
                            if dx["n"] == 0 or ("empty_" + band) \
                                    in dx["floor"]:
                                continue
                            v = dx["bands"].get(band, {}) \
                                .get(bkey)
                            if v is not None:
                                out.append(v)
                    return out

                pos, neg = bvals(pos_l), bvals(neg_l)
                eg = sgap(pos, neg)
                ea = auc_pairs(pos, neg)
                has = (lambda c, bk=bkey, bd=band:
                       docs[c]["bands"].get(bd, {})
                       .get(bk) is not None)
                gf = [x for x in guard_fails(pos_l, has)
                      if x[1] < POP_GUARD_MIN] + \
                     [x for x in guard_fails(neg_l, has)
                      if x[1] < POP_GUARD_MIN]
                et = ("INCONCLUSIVE-POPULATION-GUARD" if gf else
                      typing_of(eg, len(pos), len(neg), commit))
                b = ro["map6_bands"][band]["separations"][sep] \
                    [scalar]
                if not close(b["gap"], eg) or \
                        not close(b["auc"], ea) or \
                        b["class"] != et:
                    ok = False
    check("C9 M-AP6 every per-band table AND per-band separation "
          "EXACT vs the control's own recomputation (all bands, "
          "all classes and groups, all scalars; gaps, AUCs and "
          "classes)", ok)

    # ---- C10: the R-AP mapping numbers == the measured ----
    raps = ro["rap_mapping"]
    ok = True
    for sep in ("S3", "S2", "S1"):
        for f in FEATURES:
            s = SCALAR_OF[f]
            if raps["R-AP1"]["S3_gaps"].get(s) is not None and \
                    sep == "S3":
                if not close(raps["R-AP1"]["S3_gaps"][s],
                             ro["map3_separations"]["S3"][s]
                             ["gap"]):
                    ok = False
    ok = ok and raps["R-AP1"]["S2_classes"]["F2a"] == \
        ro["map3_separations"]["S2"]["F2a"]["class"] and \
        raps["R-AP0"]["guard_facts"]["environment_interaction"] == \
        ro["map1_parity"]["environment_interaction"]
    exp_gf = [f"{sep}/{SCALAR_OF[f]}" for sep in SEPS
              for f in FEATURES
              if ro["map3_separations"][sep][SCALAR_OF[f]]
              ["class"] == "INCONCLUSIVE-POPULATION-GUARD"]
    ok = ok and sorted(raps["R-AP0"]["guard_facts"]
                       ["population_guard_failures"]) == \
        sorted(exp_gf)
    check("C10 the R-AP mapping table carries the MEASURED "
          "numbers (S3/S2 gaps and classes, the guard facts, the "
          "environment flag) and NEVER a verdict", ok)

    # ---- C11: the cache receipts EXACT (streaming-keep) ----
    ok = True
    for i, leg in enumerate(LEGS):
        c = ro["inputs"]["caches"][i]
        if c["n_records"] != n_records[leg] or \
                c["n_empty_form"] != empty_form[leg] or \
                c["zero_step_census"].get(leg, 0) != \
                zero_census[leg]:
            ok = False
    check("C11 the four cache receipts EXACT (records kept, "
          "empty-form excluded, the zero-step census per leg; "
          "extra-manifest docs ignored by the streaming-keep "
          "law)", ok)

    # ---- C14: the loop-fixture census EXACT (the real-bytes
    # law: the fixtures ride every cache, streamed past, never
    # a population record; M-AP1 unpolluted) ----
    exp_loop_ids = sorted(fid for fid, _ in CTRL_LOOP_FIXTURES)
    ok = True
    for i, leg in enumerate(LEGS):
        c = ro["inputs"]["caches"][i]
        if c["n_loop_records"] != len(CTRL_LOOP_FIXTURES) or \
                c["n_loop_records"] != n_loop_recs[leg] or \
                c["loop_fixture_ids"] != exp_loop_ids or \
                sorted(loop_ids[leg]) != exp_loop_ids:
            ok = False
    n_man_loop = sum(1 for e in man["entries"]
                     if e["leg"] == "loop")
    corpus_entries = [e for e in man["entries"]
                      if e["leg"] != "loop"]
    # M-AP1 unpolluted: the exempt count == the manifest's loop
    # entries ONLY (the cache fixtures never enter); every
    # per-doc corpus row is a corpus manifest entry; no cache
    # fixture id ever appears in the per-doc census
    ok = ok and ro["map1_parity"]["n_exempt_loop_fixtures"] == \
        n_man_loop and \
        ro["map1_parity"]["n_corpus_docs"] == \
        len(corpus_entries) and \
        all(r["leg"] != "loop" or
            r.get("parity") == "EXEMPT"
            for r in ro["map1_per_doc"]) and \
        not any(r.get("doc_id") == fid
                for r in ro["map1_per_doc"]
                for fid in exp_loop_ids) and \
        all(fid not in caches[l]
            for l in LEGS for fid in exp_loop_ids)
    check("C14 the loop-fixture census EXACT on every cache "
          "(3 fixtures per cache, byte-identity receipt green, "
          "streamed past -- M-AP1 unpolluted: the exempt count "
          "counts the manifest's loop-live docs only, no cache "
          "fixture id ever enters the per-doc census, the zero-"
          "step census untouched)", ok)

    # ---- C12: determinism byte-identical ----
    pa = run_tool(d1, "det1.json", "ctrl")
    pb = run_tool(d1, "det2.json", "ctrl")
    same = open(os.path.join(d1, "det1.json")).read() == \
        open(os.path.join(d1, "det2.json")).read()
    check("C12 determinism: the readout JSON AND the console "
          "byte-identical across runs on the control world",
          same and pa.stdout == pb.stdout)

    # ---- C13: the tool's own SHA + py_compile ----
    compile_ok = subprocess.run(
        [PY, "-m", "py_compile", TOOL],
        capture_output=True).returncode == 0
    check("C13 the tool py_compiles clean and its own SHA in the "
          "readout == the folder bytes",
          compile_ok and ro["tool_sha256"] == sha256_file(TOOL))

    print()
    print(f"CONTROL: {len(PASS)} PASS / {len(FAIL)} FAIL")
    if FAIL:
        print("FAILED:", *FAIL, sep="\n  - ")
    shutil.rmtree(tmp, ignore_errors=True)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

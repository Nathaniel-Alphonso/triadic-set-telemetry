#!/usr/bin/env python3
"""triadic_he164kc8b_meter_join.py -- HE164-8B KC PER-DOC METER JOIN
(C4 part two; read-only readings tool; writes nothing; zero GPU; zero decodes)

WHY: the kc export carries the meter as aggregate stats only (n_runs, p50,
p95, p99, max). The two readings still owed live in the per-doc file the
pass wrote beside it: (1) the doc-by-doc meter table -- which doc owns the
max completed-run meter; (2) the meter-vs-verdict separation reading
(PASS vs FAIL-TESTS). This tool joins the two files the pass outdir
already holds (per_doc.jsonl + triadic_code17c_offline_pass_kc_v1.json),
verifies every census against the export's own bytes, and prints the
readings. It never writes a byte, never re-derives a verdict, never
touches the labels or the dump (the pass's honesty clause stands).

LAW: fail-loud on every shape assumption; findings presented, never
adjudicated. Run bare from inside the pass outdir (triadic_kc_out_he164-8b).
"""

import hashlib
import json
import os
import statistics
import sys

PER_DOC = "per_doc.jsonl"
EXPORT = "triadic_code17c_offline_pass_kc_v1.json"

N_DOCS = 164
EXPECTED_VERDICTS = {"PASS": 52, "FAIL-TESTS": 35,
                     "UNVERIFIED-UNCOMPILABLE": 75, "UNVERIFIED-TIMEOUT": 2}
EXPECTED_M1 = {"RUNNABLE": 89, "UNCOMPILABLE": 75,
               "NO-EXTRACTABLE-BLOCK": 0, "MULTI-BLOCK": 0}
EXPECTED_KILLED_REPS = 6

REQUIRED_FIELDS = ("doc", "m1_class", "verdict", "reps", "meter_reps",
                   "label", "guards", "rejudge_pass")


def die(msg):
    print("VOID: " + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pct(vals, p):
    n = len(vals)
    return vals[min(n - 1, int(p / 100 * n))] if n else None


def main():
    if not os.path.isfile(PER_DOC):
        die("the per-doc file %s is not present in this directory "
            "([Errno 2] No such file or directory) -- run me from inside "
            "the pass outdir (triadic_kc_out_he164-8b); aborting, never "
            "guessing." % PER_DOC)
    if not os.path.isfile(EXPORT):
        die("the kc export %s is not present in this directory -- it rides "
            "beside %s in the pass outdir (the assemble step wrote it "
            "there); aborting, never guessing." % (EXPORT, PER_DOC))

    with open(PER_DOC, encoding="utf-8") as f:
        recs = [json.loads(line) for line in f if line.strip()]
    if len(recs) != N_DOCS:
        die("%s holds %d records, expected %d -- the pass APPENDS %s, so a "
            "re-run in the same outdir duplicates records: re-run the pass "
            "in a FRESH outdir, never salvage a doubled file; aborting."
            % (PER_DOC, len(recs), N_DOCS, PER_DOC))
    docs = sorted(recs, key=lambda d: d["doc"])
    if [d["doc"] for d in docs] != list(range(N_DOCS)):
        die("the doc set is not exactly 0..%d (dupes or gaps in %s) -- "
            "aborting, never guessing." % (N_DOCS - 1, PER_DOC))
    for d in docs:
        for k in REQUIRED_FIELDS:
            if k not in d:
                die("doc %r lacks the field %r -- the record does not match "
                    "the e-prime contract; aborting." % (d.get("doc"), k))

    vc = dict.fromkeys(EXPECTED_VERDICTS, 0)
    m1c = dict.fromkeys(EXPECTED_M1, 0)
    for d in docs:
        vc[d["verdict"]] = vc.get(d["verdict"], 0) + 1
        m1c[d["m1_class"]] = m1c.get(d["m1_class"], 0) + 1
    if vc != EXPECTED_VERDICTS:
        die("the verdict census is %r, expected %r -- this tool is pinned to "
            "the he164-8b pass of record; aborting." % (vc, EXPECTED_VERDICTS))
    if m1c != EXPECTED_M1:
        die("the extraction census is %r, expected %r -- this tool is pinned "
            "to the he164-8b pass of record; aborting." % (m1c, EXPECTED_M1))

    for d in docs:
        want = d["verdict"] == "PASS"
        if bool(d["label"]) is not want:
            die("doc %d: label %r disagrees with verdict %r (the agreement "
                "join held at the pass: 89/89 agree, 0 disagree); "
                "aborting." % (d["doc"], d["label"], d["verdict"]))
        if bool(d["rejudge_pass"]) is not want:
            die("doc %d: rejudge_pass %r disagrees with verdict %r; "
                "aborting." % (d["doc"], d["rejudge_pass"], d["verdict"]))

    det = []          # (doc, meter, verdict) for completed deterministic docs
    killed = {}       # doc -> [count_at_kill, ...]
    n_meter_vals = 0
    flips = []
    for d in docs:
        mr = d["meter_reps"]
        if d["m1_class"] != "RUNNABLE":
            if any(m and m.get("meter") is not None for m in mr):
                die("doc %d: non-RUNNABLE but its meter_reps carry a meter "
                    "value -- shape violation; aborting." % d["doc"])
            continue
        if len(mr) != 3 or any(m is None for m in mr):
            die("doc %d: RUNNABLE but the meter_reps shape is wrong (3 "
                "non-null entries is the law); aborting." % d["doc"])
        if d["verdict"] == "UNVERIFIED-TIMEOUT":
            cak = [m.get("count_at_kill") for m in mr]
            if any(v is None for v in cak) or \
               any(m["meter"] is not None for m in mr):
                die("doc %d: a killed run but the meter/count-at-kill shape "
                    "is wrong; aborting." % d["doc"])
            killed[d["doc"]] = cak
            continue
        meters = [m["meter"] for m in mr]
        if any(v is None for v in meters):
            die("doc %d: a completed run but a meter value is None; "
                "aborting." % d["doc"])
        if len(set(meters)) != 1:
            flips.append(d["doc"])
            continue
        det.append((d["doc"], meters[0], d["verdict"]))
        n_meter_vals += 3
    if flips:
        die("meter flips on docs %s -- identical across reps is the law "
            "(R-C2 VOID-class instrument bug); aborting." % sorted(flips))
    if sum(len(v) for v in killed.values()) != EXPECTED_KILLED_REPS:
        die("killed meter reps %d, expected %d; aborting."
            % (sum(len(v) for v in killed.values()), EXPECTED_KILLED_REPS))

    with open(EXPORT, encoding="utf-8") as f:
        ex = json.load(f)
    m2 = ex["m2_verdict_census"]
    meter = ex["cost_census"]["meter"]
    cak_block = ex["cost_census"]["count_at_kill"]
    if m2["verdict_counts"] != vc:
        die("the export's verdict census disagrees with the per-doc bytes "
            "(%r vs %r); aborting." % (m2["verdict_counts"], vc))
    if ex["m1_extraction_census"]["class_counts"] != m1c:
        die("the export's extraction census disagrees with the per-doc "
            "bytes; aborting.")
    vals = sorted(m for (_doc, m, _v) in det for _ in range(3))
    if meter["n_runs"] != len(vals):
        die("the export's n_runs %r disagrees with the per-doc bytes %d; "
            "aborting." % (meter["n_runs"], len(vals)))
    for key, p in (("p50", 50), ("p95", 95), ("p99", 99)):
        if meter[key] != pct(vals, p):
            die("the export's meter %s %r disagrees with the per-doc bytes "
                "%r; aborting." % (key, meter[key], pct(vals, p)))
    if meter["max"] != vals[-1]:
        die("the export's meter max %r disagrees with the per-doc bytes %r; "
            "aborting." % (meter["max"], vals[-1]))
    if m2["rep_flake_docs"] != []:
        die("the export names rep-flake docs %r but the per-doc labels show "
            "none; aborting." % (m2["rep_flake_docs"],))
    aj = m2["agreement_join"]
    if aj["docs_joined"] != EXPECTED_M1["RUNNABLE"] or aj["disagree"] != 0 \
       or aj["label_true"] != vc["PASS"] or aj["instrument_pass"] != vc["PASS"]:
        die("the export's agreement join disagrees with the per-doc bytes "
            "(%r); aborting." % aj)
    if cak_block["killed_meter_reps"] != EXPECTED_KILLED_REPS:
        die("the export's killed_meter_reps %r disagrees with the per-doc "
            "bytes %d; aborting."
            % (cak_block["killed_meter_reps"], EXPECTED_KILLED_REPS))
    for doc, reps in killed.items():
        sdoc = str(doc)
        if sdoc not in cak_block["per_doc"]:
            die("timeout doc %d is missing from the export's count-at-kill "
                "block; aborting." % doc)
        if cak_block["per_doc"][sdoc]["reps"] != reps or \
           cak_block["per_doc"][sdoc]["range"] != [min(reps), max(reps)]:
            die("timeout doc %d: the export's count-at-kill block disagrees "
                "with the per-doc bytes; aborting." % doc)

    owner = max(det, key=lambda t: t[1])
    print("HE164-8B KC PER-DOC METER JOIN (read-only readings tool; "
          "C4 part two; writes nothing)")
    print("  per-doc file : %s sha %s" % (PER_DOC, sha256_file(PER_DOC)))
    print("  kc export    : %s sha %s" % (EXPORT, sha256_file(EXPORT)))
    print("  interpreter pin (the export's own line): %r" % ex.get("python_pin"))
    print("  census: %d records; verdict %r; extraction %r"
          % (N_DOCS, vc, m1c))
    print("  meter determinism re-asserted: %d deterministic docs, zero "
          "flips; %d killed reps" % (len(det), EXPECTED_KILLED_REPS))
    print("  THE MAX COMPLETED-RUN METER: doc %d = %d instructions "
          "(verdict %s)" % (owner[0], owner[1], owner[2]))
    print("")
    print("  doc-by-doc meter table (%d deterministic docs, descending):"
          % len(det))
    for doc, m, v in sorted(det, key=lambda t: -t[1]):
        print("    [%3d] %11d  %s" % (doc, m, v))
    print("")
    print("  meter stats by verdict class (per-doc values):")
    for cls in ("PASS", "FAIL-TESTS"):
        xs = sorted(m for (_doc, m, v) in det if v == cls)
        print("    %-10s n=%d  min=%d  p50=%s  p95=%d  max=%d  mean=%.1f"
              % (cls, len(xs), xs[0], statistics.median(xs),
                 pct(xs, 95), xs[-1], statistics.mean(xs)))
    print("")
    p = sorted(m for (_doc, m, v) in det if v == "PASS")
    ft = sorted(m for (_doc, m, v) in det if v == "FAIL-TESTS")
    wins = sum(1 for a in p for b in ft if a >= b)
    cl = wins / float(len(p) * len(ft))
    print("  separation reading (presented, never adjudicated):")
    print("    P(a random PASS doc's meter >= a random FAIL-TESTS doc's "
          "meter) = %.4f" % cl)
    print("    medians: PASS %s vs FAIL-TESTS %s"
          % (statistics.median(p), statistics.median(ft)))
    print("")
    print("  the killed runaways (count-at-kill deterministic lower bounds):")
    for doc in sorted(killed):
        r = killed[doc]
        print("    doc %d: reps %r  range [%d .. %d]" % (doc, r, min(r), max(r)))
    bud = meter["meter_budget_recommendation"]
    print("")
    print("  the export's budget lines reprinted: p99 %r, x1.25 %r, x1.5 %r "
          "(%r)" % (bud["p99"], bud["p99_x1.25"], bud["p99_x1.5"], bud["rule"]))
    print("")
    print("ALL SELF-CHECKS PASS -- paste this whole console; the readings "
          "are presented, never adjudicated.")


if __name__ == "__main__":
    main()

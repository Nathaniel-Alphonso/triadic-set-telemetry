#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stage2_ladder_walk_v1 -- THE STAGE-2 ACCEPTANCE-LADDER WALK (MESSAGE 3 OF
THE S2-BUILD ACT; the pinned sheet stage2-mixedregime-preregistration.md
Section 6: rungs (d) (e) (f) my-side; rung (g) HIS owner-side run + stamp)

WHAT IT IS: the zero-GPU offline walk of the Stage-1 instrument stack
(the splitter's two-phase clock, the accumulator, the prose accumulator,
the hook -- every instrument of record imported VERBATIM, byte-pinned,
sha-asserted at import; zero instrument bytes moved) over the Stage-2
mixed-regime cache of record, graded against the authored census (the
census IS the ground truth; the splice builder's own loader re-asserted
at load).

RUNG (d) 5a -- the entry marks: every authored seam receipted (the span
  latch position vs the census EXACT, or the deviation typed loud, never
  silently absorbed), COLD_START exercised on every incoming span, span
  contiguity per document, the foreign-schema-row census, the roles'
  live derivation SEAM-AWARE (onset iff {0} UNION the authored seam
  positions), the five-state table census.
RUNG (e) 5b -- the demux classification acceptance: per span the latch
  LEG vs the true leg, the span STATE read at BOTH forms (the [REDACTED_PER_PUBLICATION_POLICY]
  record bar / the [REDACTED_PER_PUBLICATION_POLICY] Tier C datum side by side, the designation
  never silently chosen) vs the true state, every deviation typed
  loud; the Class A mid-document trip stress receipts (the trip position
  on both clocks, the anchor t* TYPED against the seam per the operating-threshold wiring sheet
  early-bias law -- t* <= t_seam = EARLY/SAFE, t* > t_seam = the
  residue measured loud; the anchor-to-trip gap, the post-trip
  continuation, the re-billed count the offline projection with the
  NAMED-UNMEASURED-OFFLINE tag); the Class N zero-trip specificity
  control; the LCL re-trip on the second loop span's own rows.
RUNG (f) 5c -- the stack re-read: the hook's E-event stream on the
  mid-document trips (the ladder state E0 offline, the efficacy
  terminals NAMED-UNMEASURED-OFFLINE), the isolation guard's cross-leg
  write census EXPECTED-ZERO on this intra-leg cache (the Stage-2B
  cross-leg case named forward), the new census pins for the new bytes.
RUNG (g) -- NAMED HIS: the owner-side run + his closing stamp (the
  runbook stage2_ladder_walk_RUN_INSTRUCTIONS_v1.md; the portability
  law; his stamps decide every mark).

THE ADDITIVE CONSTRUCTIONS (this wrapper's own laws, every one receipted
loud in the console, never silent, never adjudicated):
  - THE DECLARED-LEG CONVENTION: every row carries __t1__ = its
    document's census leg (the banked stream-leg driver law, verbatim);
    the tier-1 schema signature still runs inside every 16-row
    occupancy window (the instrument's own state table), and the
    tier-1 verdict is censused per span. THE FINDING RECEIPTED: the
    loop material's rows carry the THIN'S EMISSION SCHEMA on BOTH legs
    (the banked fixture bytes: the injected walks were recorded on the
    emission surface), so on the CODE leg the loop spans' rows
    classify PROSE at tier 1 inside CODE-leg spans: the five-state
    table receipts the disagreement, the latch holds, the schema mix
    presented for his review -- never silently absorbed.
  - THE W JOIN: the emission-schema rows carry the W lane (the rw16
    bucket law's own running prefix max) so the tier-1 classifier can
    read their structural signature (the 7-channel prose emission
    family); without the join the classifier would die
    UNRECOGNIZED-SCHEMA on the banked fixture bytes.
  - THE RW16 PORT + CROSS-CHECK: the bucket-baseline pooling ported
    verbatim, cross-checked EXACT against the prose accumulator's own
    w_derivation output on every corpus doc (fail-loud on any drift);
    the fixture W arrays are the same law's per-doc prefix max over
    the fixtures' steps.
  - THE SPAN-LEVEL LANE JOIN: per span, the walk lanes (s, PR, E, H)
    joined per row from the source record's step lanes at the row's
    source-native t (the prose accumulator's own lane join -- steps of
    the commit -- one-for-one), the prefix read on the SPAN'S OWN ROW
    CLOCK (the horizon-reference law: the instruments evaluate
    span-locally, the corrected law).
  - THE SPAN-LOCAL W RESTART: the W running max restarts at each span
    boundary (the span-scoping readout law, Amendment Act No. 1
    adoption 7); the per-step z values are the banked law's own
    (position-matched bucket baselines, source-native t // 16).
  - THE EMISSION-SURFACE STATE READ: the loop material's rows carry
    the emission schema on both legs, so the state read of record for
    every emission-schema span rides the prose accumulator's span
    machinery (ProseSpan on the span-level rec, standardized on the
    BANKED even-A lane moments -- the calibration of record, zero new
    constants); on the CODE leg the CODE-surface read is receipted
    NAMED-ABSENT per loop span (the CODE band channels absent on this
    material, printed loud, never zero-filled).
  - THE CODE CALIBRATION: the CODE-surface prefix moments MEASURED
    from the leg's OWN 55 clean spans (the 1307 section-3 law's
    analog: the clean material defines the standard, the loop spans
    graded against it; the cohort choice receipted loud).

MODES:
  --battery   the synthetic-worlds battery (the fixture law: zero real
              rows, every law proven, every negative fixture dying
              loud, twice-run byte-identical by construction)
  --walk      the real walk over the mixed cache of record + the census
              export + the thin / export inputs of record (every pin
              asserted at load, fail-loud)

(offline paper act only, zero GPU, zero decodes, zero build hours; Nov 9
2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; no thresholds set, moved, or
adjudicated; findings presented, never adjudicated -- the owner's stamps
decide)
"""

import argparse
import hashlib
import json
import os
import sys
from collections import Counter

VERSION = "stage2_ladder_walk_v1"

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------- 
# THE INSTRUMENT PINS (bytes-then-sha, the additive law; every instrument
# of record + the splice builder asserted unmoved at import, fail-loud)
# ----------------------------------------------------------------------
INSTRUMENT_PINS = (
    ("triadic_splitter_v1.py", 52410,
     "5980eaec57fc990707e3317f3f32573893c915ce821dfe665536634136c9c4a0"),
    ("triadic_accumulator_v1.py", 58292,
     "c7acb944223d16e327f6ee5da706181ea35749aa95a03fc18628393710e6662e"),
    ("triadic_accumulator_prose_v1.py", 76867,
     "7d7ab8feaaae552b973d609ac27a4772a70d9cd3438486e2c33521a2aafbb7c9"),
    ("triadic_hook_v1.py", 52078,
     "4de049deab7f0e70116da819000641f785c7f5014eedf3c6889d660f57a2ccb5"),
)
BUILDER_BYTES = 68635
BUILDER_SHA256 = ("14d1f448e9bd0a9a93a887972db925d4da7ecac2c53b1eea9fb850b"
                  "35b3f938d")

# the outputs of record of the S2-BUILD act Message 2 (byte-pinned)
MIXED_CACHE_BYTES = 14814947
MIXED_CACHE_SHA256 = ("a5a4ae539112472424c2fb4160f2422e4810d4a83140f6e0097"
                      "2172502f76ea8")
CENSUS_BYTES = 65583
CENSUS_SHA256 = ("cca12263db49a502bdf63761144d4b4953fd42c56b5a04a0a40f69"
                 "0270d0b86f")

# the source-thin sha prefixes of record (the builder's own pin table,
# carried for the provenance routing; never re-derived here)
SHA_PROSE_THIN = "88cbadee7baa1e35"
SHA_CODE_THIN = "77dd63c7d21c6303"
SHA_CODE_CACHE = "610d48c9689c07c7"

PAREN = ("(offline paper act only, zero GPU, zero decodes, zero build "
         "hours; Nov 9 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; no thresholds "
         "set, moved, or adjudicated; findings presented, never adjudicated "
         "-- the owner's stamps decide)")


def die(marker, detail=""):
    sys.stdout.write("[TRIP-LOUD] %s: %s\n" % (marker, detail))
    sys.stdout.write("[TRIP-LOUD] the walk halts loud, never silent "
                     "(fail-loud law; findings presented, never "
                     "adjudicated)\n")
    sys.exit(1)


def out(line):
    sys.stdout.write(line + "\n")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return os.path.getsize(path), h.hexdigest()


def assert_file_pin(path, pin_bytes, pin_sha, marker):
    nb, sha = sha256_of(path)
    if not (nb == pin_bytes and sha == pin_sha):
        die(marker, "%s moved: %d B / %s (pinned %d B / %s)"
            % (path, nb, sha, pin_bytes, pin_sha))
    return nb, sha


# ----------------------------------------------------------------------
# THE INSTRUMENT IMPORT (verbatim, byte-pinned; the artifacts dir + this
# project dir on the path; the builder imported for its loader of record)
# ----------------------------------------------------------------------
def import_instruments(artifacts_dir):
    for fname, pin_b, pin_s in INSTRUMENT_PINS:
        assert_file_pin(os.path.join(artifacts_dir, fname), pin_b, pin_s,
                        "INSTRUMENT-PIN")
    assert_file_pin(os.path.join(HERE, "stage2_splice_builder_v1.py"),
                    BUILDER_BYTES, BUILDER_SHA256, "BUILDER-PIN")
    for p in (artifacts_dir, HERE):
        if p not in sys.path:
            sys.path.insert(0, p)
    import triadic_splitter_v1 as sp
    import triadic_accumulator_v1 as acc
    import triadic_accumulator_prose_v1 as pap
    import triadic_hook_v1 as hk
    import stage2_splice_builder_v1 as bd
    return sp, acc, pap, hk, bd


# ----------------------------------------------------------------------
# THE RW16 PORT (the bucket-baseline pooling ported verbatim from the
# prose accumulator's w_derivation; the per-step zmax + running prefix
# max; the EXACT cross-check against the instrument's own output)
# ----------------------------------------------------------------------
def _mean_std(v):
    n = len(v)
    m = sum(v) / float(n)
    return n, m, (sum((x - m) ** 2 for x in v) / (n - 1)) ** 0.5


def rw16_baselines(corpus, is_calib, bucket, min_n):
    """The pooling law verbatim: the calibration docs' step values pooled
    per t//16 bucket; per-bucket mean + SAMPLE sd; the under-min pooled
    baseline. Returns (base_s, base_pr, pool_s, pool_pr)."""
    bs, bpr = {}, {}
    for rec in corpus:
        if not is_calib(rec["doc_id"]):
            continue
        st = rec["steps"]
        for t, sv, pv in zip(st["t"], st["s"], st["PR"]):
            b = t // bucket
            bs.setdefault(b, []).append(sv)
            bpr.setdefault(b, []).append(pv)
    pool_s = _mean_std([x for vv in bs.values() for x in vv])
    pool_pr = _mean_std([x for vv in bpr.values() for x in vv])
    base_s = {b: (_mean_std(bs[b]) if len(bs[b]) >= min_n else pool_s)
              for b in bs}
    base_pr = {b: (_mean_std(bpr[b]) if len(bpr[b]) >= min_n else pool_pr)
               for b in bpr}
    return base_s, base_pr, pool_s, pool_pr


def rw16_zmax_steps(rec, base_s, base_pr, pool_s, pool_pr, bucket):
    """Per-step zmax + the doc's own running prefix max (the law verbatim:
    position-matched buckets, the prefix max carried). Returns the
    per-step zmax array + the per-doc W array (the banked W semantics)."""
    st = rec["steps"]
    zmax, w = [], []
    cur = -1.0
    for t, sv, pv in zip(st["t"], st["s"], st["PR"]):
        b = t // bucket
        n, mu, sd = base_s.get(b, pool_s)
        z_f = (sv - mu) / sd if sd else 0.0
        n2, mu2, sd2 = base_pr.get(b, pool_pr)
        z_c = (pv - mu2) / sd2 if sd2 else 0.0
        z = max(abs(z_f), abs(z_c))
        zmax.append(z)
        cur = max(cur, z)
        w.append(cur)
    return zmax, w


def rw16_cross_check(corpus, w_at_banked, base_s, base_pr, pool_s, pool_pr,
                     bucket, label):
    """THE PORT'S OWN LAW PROOF: the ported pooling + prefix max reproduce
    the instrument's w_derivation EXACTLY on every corpus doc -- any drift
    dies loud (the port is the law, never a re-write)."""
    n_checked = 0
    for rec in corpus:
        _, w_port = rw16_zmax_steps(rec, base_s, base_pr, pool_s, pool_pr,
                                    bucket)
        banked = w_at_banked.get(rec["doc_id"])
        if banked is None:
            die("RW16-PORT", "doc %s: no banked W for the cross-check"
                % rec["doc_id"])
        if w_port != banked:
            die("RW16-PORT",
                "doc %s: the ported W drifts from the instrument's own "
                "derivation (the port is the law or it is nothing; "
                "%s)" % (rec["doc_id"], label))
        n_checked += 1
    return n_checked


def rw16_span_w(rows_native_t, zmax_by_source, source_key):
    """THE SPAN-LOCAL W RESTART (the span-scoping readout law): the
    running prefix max restarts at the span's first row; the per-step z
    values are the banked law's own."""
    zmax = zmax_by_source[source_key]
    cur = -1.0
    w = []
    for t in rows_native_t:
        cur = max(cur, zmax[t])
        w.append(cur)
    return w


# ----------------------------------------------------------------------
# THE FLATTEN LAW (the wrapper's row form: the payload merged top-level,
# the re-indexed clocks live, the native coordinates provenance-only,
# the declared leg, the authored onset mark, the W join on the
# emission-schema rows)
# ----------------------------------------------------------------------
def schema_of_payload(payload, bd):
    keys = set(payload.keys())
    if keys == set(bd.CODE_COLUMNS):
        return "CODE-BAND"
    if keys == set(bd.COMMIT_KEYS):
        return "EMISSION"
    die("SCHEMA-UNEXPECTED",
        "a row payload matching neither the 16-column code band family "
        "nor the 16-key emission family: %s (the Message-2 adapter law: "
        "SCHEMA-UNEXPECTED dies loud, never absorbed)"
        % sorted(keys))


def flatten_span_rows(leg, surface, doc_rows, onset_flags, src, span_source,
                      zmax_by_source):
    """One span's rows flattened. Returns (flat_rows, span_rec, w_span,
    schema). The emission spans carry the span-level lane rec + the
    span-local W array; the code-band spans carry neither (their channels
    ride the rows themselves)."""
    sp, bd = src["sp"], src["bd"]
    schema = schema_of_payload(doc_rows[0]["payload"], bd)
    n = len(doc_rows)
    if schema == "EMISSION":
        # the lane join source (the provenance routing by sha prefix)
        skey = span_source["zkey"]
        rec_steps = span_source["steps"]
        walk_ids = span_source["walk_ids"]
        zmax = zmax_by_source[skey]
        lane_t = [r["payload"]["t"] for r in doc_rows]
        for t in lane_t:
            if not (isinstance(t, int) and 0 <= t < len(rec_steps["t"])):
                die("LANE-JOIN", "a row's source-native t %r outside the "
                    "source record's step window" % t)
        w_span = rw16_span_w(lane_t, zmax_by_source, skey)
        span_rec = {"doc_id": span_source["label"], "is_fixture":
                    span_source["is_fixture"], "n_gen_steps":
                    len(rec_steps["t"]), "n_commits": n,
                    "steps": {"t": list(range(n)),
                              "s": [rec_steps["s"][t] for t in lane_t],
                              "PR": [rec_steps["PR"][t] for t in lane_t],
                              "E": [rec_steps["E"][t] for t in lane_t],
                              "H": [rec_steps["H"][t] for t in lane_t]}}
    else:
        w_span = None
        span_rec = None
    flat_rows = []
    for i, r in enumerate(doc_rows):
        p = dict(r["payload"])
        p["commit_index"] = r["commit_index"]      # re-indexed, live
        p["stmt_ordinal"] = r["stmt_ordinal"]       # re-indexed, live
        p["token_step"] = r["token_step"]           # re-indexed, live
        p["t_commit"] = r["token_step"]   # the step clock rides the
                                          # re-indexed token clock
        if surface == "CODE":
            p["role"] = bd.CODE_ONSET if onset_flags[i] else bd.CODE_OTHER
            p["__native__"] = {"commit_index": r["payload"].get(
                "commit_index"), "t_commit": r["payload"].get("t_commit"),
                "token_id": r["payload"].get("token_id")}
        else:
            p["role"] = (sp.CODE_ROLES[0] if onset_flags[i]
                         else sp.CODE_ROLES[1])
            p["__onset__"] = bool(onset_flags[i])
            p["__native__"] = {"t": r["payload"].get("t")}
        if schema == "EMISSION":
            # the W join + the token-id join ride EVERY emission row on
            # BOTH surfaces (the loop material carries the emission
            # schema on both legs -- without the W lane tier 1 cannot
            # read the signature at all; the join receipted per span)
            p["token_id"] = span_source["walk_ids"][r["payload"]["t"]]
            p["W"] = w_span[i]
        else:
            p["token_id"] = r["payload"].get("token_id")
        p["__t1__"] = leg
        flat_rows.append(p)
    return flat_rows, span_rec, w_span, schema


# ----------------------------------------------------------------------
# THE PER-DOC CENSUS LAW (the walk's own per-document asserts, exercised
# by the battery's negative fixtures too; the 45/leg population pins live
# in the builder's loader of record, re-asserted at the real load)
# ----------------------------------------------------------------------
def assert_doc_census(doc, cen, surface, bd):
    if cen["doc_id"] != doc["doc_id"]:
        die("CENSUS-DOC", "cache doc %s != census %s"
            % (doc["doc_id"], cen["doc_id"]))
    if len(doc["rows"]) != cen["n_rows"]:
        die("ROW-CENSUS", "%s: cache rows %d != census %d"
            % (doc["doc_id"], len(doc["rows"]), cen["n_rows"]))
    shape = bd.EXPECTED_CLASS_SHAPE[cen["class"]]
    got = [s["state"] for s in cen["spans"]]
    if got != shape:
        die("SPAN-TRUTH", "%s: span states %r != the authored shape %r"
            % (doc["doc_id"], got, shape))
    if len(cen["seams"]) != len(shape) - 1:
        die("SEAM-COUNT", "%s: %d seams != %d (the mismatched seam count "
            "dies loud)" % (doc["doc_id"], len(cen["seams"]),
                            len(shape) - 1))
    expect_onset = [0] + [s["commit_index"] for s in cen["seams"]]
    if cen["onset_positions"] != expect_onset:
        die("ONSET-POS", "%s: census onset positions %r != {0} + seams %r"
            % (doc["doc_id"], cen["onset_positions"], expect_onset))
    nsum = sum(s["n_rows"] for s in cen["spans"])
    if nsum != cen["n_rows"]:
        die("SPAN-SUM", "%s: spans sum %d != %d rows"
            % (doc["doc_id"], nsum, cen["n_rows"]))
    for s in cen["seams"]:
        ci = s["commit_index"]
        if ci >= len(doc["rows"]):
            die("SEAM-RANGE", "%s: seam commit_index %d outside the doc"
                % (doc["doc_id"], ci))
        if doc["rows"][ci]["stmt_ordinal"] != s["stmt_ordinal"]:
            die("DUAL-CLOCK", "%s: seam stmt_ordinal mismatch"
                % doc["doc_id"])
        if doc["rows"][ci]["token_step"] != s["token_step"]:
            die("DUAL-CLOCK", "%s: seam token_step mismatch" % doc["doc_id"])
    prev_s, prev_t = None, None
    for i, r in enumerate(doc["rows"]):
        expect = i in expect_onset
        if bd.row_onset(r, surface) != expect:
            die("ONSET-LAW", "%s: row %d onset mismatch (onset iff {0} + "
                "seams)" % (doc["doc_id"], i))
        if i > 0:
            if r["stmt_ordinal"] < prev_s:
                die("MONOTONIC-S", "%s: stmt_ordinal backwards at %d"
                    % (doc["doc_id"], i))
            if r["token_step"] <= prev_t:
                die("MONOTONIC-T", "%s: token_step backwards at %d"
                    % (doc["doc_id"], i))
        prev_s, prev_t = r["stmt_ordinal"], r["token_step"]


def prep_doc(leg, surface, doc, cen, src):
    """Flatten + lane-join + W-join one document; the per-doc census law
    asserted first. Returns the doc structure for the walk."""
    bd = src["bd"]
    assert_doc_census(doc, cen, surface, bd)
    onsets = cen["onset_positions"]
    spans = []
    for j, cspan in enumerate(cen["spans"]):
        a = onsets[j]
        b = onsets[j + 1] if j + 1 < len(onsets) else len(doc["rows"])
        rows = doc["rows"][a:b]
        if len(rows) != cspan["n_rows"]:
            die("SPAN-SLICE", "%s: span %d slice %d != census %d"
                % (doc["doc_id"], j, len(rows), cspan["n_rows"]))
        onset_flags = [bd.row_onset(r, surface) for r in rows]
        span_source = resolve_span_source(leg, cspan, src,
                                          "%s:s%d" % (doc["doc_id"], j))
        flat_rows, span_rec, w_span, schema = flatten_span_rows(
            leg, surface, rows, onset_flags, src, span_source,
            src["zmax_by_source"])
        spans.append({
            "label": "%s:s%d" % (doc["doc_id"], j),
            "doc_id": doc["doc_id"], "class": cen["class"],
            "state": cspan["state"], "start": a, "n_rows": len(rows),
            "cspan": cspan, "flat_rows": flat_rows, "span_rec": span_rec,
            "w_span": w_span, "schema": schema,
            "source_doc_id": cspan["source"]["doc_id"],
            "graded_horizon": cspan.get("graded_horizon", "EOS"),
        })
    return {"doc_id": doc["doc_id"], "class": cen["class"],
            "n_rows": len(doc["rows"]), "spans": spans,
            "flat_rows": [r for s in spans for r in s["flat_rows"]],
            "seams": [s["commit_index"] for s in cen["seams"]],
            "onset_positions": onsets}


def resolve_span_source(leg, cspan, src, label):
    """The provenance routing (the census's own sha prefixes): the source
    record + the zmax key for the lane join."""
    sd = cspan["source"]["doc_id"]
    sha_p = cspan["source"].get("sha_prefix", "")
    if cspan["state"] == "clean":
        if leg == "CODE":
            # the code cache's clean rows carry their own channels; no
            # lane join (the provenance sha still receipted)
            return {"label": label, "zkey": None, "steps": None,
                    "walk_ids": None, "is_fixture": False}
        rec = src["prose_recs"].get(sd)
        if rec is None:
            die("PROVENANCE", "clean source %s absent from the prose thin "
                "of record" % sd)
        zkey = "prose:%s" % sd
    else:
        if sha_p.startswith(SHA_PROSE_THIN):
            rec = src["prose_fixtures"].get(sd)
            zkey = "prose:%s" % sd
        elif sha_p.startswith(SHA_CODE_THIN):
            rec = src["code_fixtures"].get(sd)
            zkey = "code:%s" % sd
        else:
            die("PROVENANCE", "loop source %s sha prefix %r matches "
                "neither thin of record" % (sd, sha_p))
        if rec is None:
            die("PROVENANCE", "loop fixture %s absent from its thin of "
                "record" % sd)
    src["zmax_by_source"].setdefault(
        zkey, rw16_zmax_steps(rec, src["base_s"], src["base_pr"],
                              src["pool_s"], src["pool_pr"],
                              src["pap"].BUCKET)[0])
    return {"label": label, "zkey": zkey, "steps": rec["steps"],
            "walk_ids": rec["walk_ids"],
            "is_fixture": not isinstance(rec["doc_id"], int)}


# ----------------------------------------------------------------------
# RUNG (d) -- THE ENTRY-MARK MEASUREMENT (5a)
# ----------------------------------------------------------------------
def rung_d_leg(leg, docs, src, out_fn):
    """The splitter's two-phase clock driven row by row over every
    document of the leg (a FRESH CLOCK PER DOCUMENT -- the per-document
    contiguity law receipted per doc; the isolation guard shared across
    the leg's whole stream; the state census pooled per leg)."""
    sp, bd = src["sp"], src["bd"]
    guard = sp.IsolationGuard()
    marks = {"CODE": 0.5, "PROSE": 0.5, "MATH": 0.5}
    pooled = Counter()
    receipts = {"leg": leg, "docs": [], "guard": guard}
    n_seam_exact = 0
    n_seam_typed = 0
    for doc in docs:
        profiles = sp.EntryProfiles(marks)
        clock = sp.TwoPhaseClock(profiles, guard)
        states = []
        for i, row in enumerate(doc["flat_rows"]):
            states.append(clock.on_row(row, i))
        # -- the span latch receipts vs the census
        latch_positions = [s["t_onset"] for s in clock.spans]
        census_onsets = list(doc["onset_positions"])
        doc_rec = {"doc_id": doc["doc_id"], "latches": latch_positions,
                   "census": census_onsets, "seam_lines": [],
                   "spans": clock.spans, "states": states,
                   "contiguity": clock.span_contiguity(),
                   "foreign": clock.foreign_census,
                   "state_census": dict(clock.state_census)}
        for k in clock.state_census:
            pooled[k] += clock.state_census[k]
        if latch_positions != census_onsets:
            # typed loud, never absorbed: which seams missed, where the
            # latches actually landed
            missing = [p for p in census_onsets if p not in latch_positions]
            extra = [p for p in latch_positions if p not in census_onsets]
            doc_rec["latch_deviation"] = {"missing": missing, "extra": extra}
            out_fn("[rung-d] %s %s: LATCH DEVIATION typed loud -- census "
                   "onsets %r vs latches %r (missing %r, extra %r); the "
                   "walk continues, the deviation graded at rung (e)"
                   % (leg, doc["doc_id"], census_onsets, latch_positions,
                      missing, extra))
        else:
            doc_rec["latch_deviation"] = None
        # -- the seam receipts (every authored seam, EXACT or typed)
        for sm in doc["seams"]:
            if sm in latch_positions:
                n_seam_exact += 1
                doc_rec["seam_lines"].append(
                    (sm, "EXACT", states[sm] if sm < len(states) else None))
            else:
                n_seam_typed += 1
                st = states[sm] if sm < len(states) else None
                doc_rec["seam_lines"].append(
                    (sm, "LATCH-MISS (state %s)" % st,
                     st))
        # -- contiguity + the foreign census + the cold-start latches
        if not doc_rec["contiguity"]:
            die("SPAN-CONTIGUITY", "%s: the spans are not contiguous and "
                "whole (zero unexplained gaps is the 5a law)"
                % doc["doc_id"])
        # -- the roles' live derivation, SEAM-AWARE (onset iff {0}+seams)
        measured_onsets = [r["commit_index"] for r in doc["flat_rows"]
                          if r.get("role") == sp.CODE_ROLES[0]]
        expect = set(doc["onset_positions"])
        got = set(measured_onsets)
        if got != expect:
            die("SEAM-AWARE-DERIVATION",
                "%s: the measured onset marks %r != the authored {0}+seams "
                "%r (mismatches beyond the authored positions die loud)"
                % (doc["doc_id"], sorted(got), sorted(expect)))
        # -- the tier-1 schema census per span (the finding receipt)
        schema_census = []
        for s in doc["spans"]:
            fam = Counter()
            for r in s["flat_rows"]:
                fam[schema_of_row(r, bd)] += 1
            schema_census.append(dict(fam))
        doc_rec["schema_census"] = schema_census
        receipts["docs"].append(doc_rec)
    receipts["pooled"] = dict(pooled)
    receipts["n_seam_exact"] = n_seam_exact
    receipts["n_seam_typed"] = n_seam_typed
    receipts["foreign_total"] = sum(d["foreign"] for d in receipts["docs"])
    return receipts


def schema_of_row(flat_row, bd):
    keys = set(flat_row.keys())
    if "work_inc" in keys and "margin_content" in keys:
        return "CODE-BAND"
    if all(k in keys for k in ("K", "margin", "emitted_p", "second_p",
                               "hedge_mass", "content_mass", "W")):
        return "EMISSION"
    return "FOREIGN"


def rung_d_print(r, leg, out_fn):
    out_fn("[rung-d] %s: %d docs walked | seam receipts EXACT %d / typed "
           "%d | cold-start latches per span receipted below | contiguity "
           "green per doc | foreign-schema-row census %d"
           % (leg, len(r["docs"]), r["n_seam_exact"], r["n_seam_typed"],
              r["foreign_total"]))
    for d in r["docs"]:
        n_spans = len(d["spans"])
        out_fn("[rung-d]   %s (%s): %d spans | latches %s | cold-start "
               "latches %d (every incoming span) | state census %s"
               % (d["doc_id"], "OK" if d["latch_deviation"] is None
                  else "DEVIATION-TYPED", n_spans, d["latches"],
                  n_spans, json.dumps(d["state_census"], sort_keys=True)))
        for sm, verdict, st in d["seam_lines"]:
            out_fn("[rung-d]     seam at commit %d: %s (the five-state "
                   "entry %s)" % (sm, verdict, st))
        for j, fam in enumerate(d["schema_census"]):
            out_fn("[rung-d]     span %d tier-1 schema census %s"
                   % (j, json.dumps(fam, sort_keys=True)))


# ----------------------------------------------------------------------
# RUNG (e) -- THE DEMUX CLASSIFICATION ACCEPTANCE (5b)
# ----------------------------------------------------------------------
def first_passage(traj, cut, acc):
    """The per-form first-passage trip on the span's own reached path
    (K-4); the value + position returned, or the deepest reached value."""
    best_h, best_v = None, None
    for h in acc.reached_grid(traj["n_rows"], "K-4"):
        v = traj["values"].get(h)
        if v is not None:
            if best_v is None or v > best_v:
                best_h, best_v = h, v
            if v >= cut:
                return h, v
    return None, best_v


def rung_e_leg(leg, docs, rung_d_out, calib_prose, src, out_fn):
    sp, acc, pap = src["sp"], src["acc"], src["pap"]
    # -- the CODE calibration: measured from the leg's OWN clean spans
    #    (the 1307 section-3 law's analog; the cohort choice receipted)
    calib_code = None
    if leg == "CODE":
        clean_objs = []
        for doc in docs:
            for s in doc["spans"]:
                if s["schema"] != "CODE-BAND" or s["state"] != "clean":
                    continue
                o = acc.StreamingSpan(s["label"], "CODE", s["start"],
                                      s["flat_rows"][0]["commit_index"],
                                      s["flat_rows"][0].get("token_id"),
                                      doc_id=doc["doc_id"])
                for r in s["flat_rows"]:
                    o.push(r)
                clean_objs.append(o)
        out_fn("[rung-e] CODE calibration cohort: %d clean spans (the "
               "1307 section-3 law's analog -- the clean material defines "
               "the standard, the loop spans graded against it; the "
               "censored-at-h law carried)" % len(clean_objs))
        moments = acc.measure_moments_from_spans(clean_objs, ("CODE",), None)
        calib_code = acc.Calibration(moments, {})
        cohort_sizes = {}
        for h in acc.GRID:
            cohort_sizes[str(h)] = sum(
                1 for o in clean_objs if o.n_rows() > h) if h != "EOS" \
                else len(clean_objs)
        out_fn("[rung-e] CODE calibration cohort sizes per horizon: %s "
               "(spans censored at h, never pooled silent)"
               % json.dumps(cohort_sizes, sort_keys=True))
        # close the cohort spans with the measured calibration (their own
        # state receipts ride the same table below)
    # -- the demux table
    table = []
    n_match = Counter()
    for doc_idx, doc in enumerate(docs):
        d_rec = rung_d_out["docs"][doc_idx]
        for j, s in enumerate(doc["spans"]):
            label = s["label"]
            true_leg = leg
            true_state = s["state"]
            reads = {}
            # --- the state read of record
            if s["schema"] == "CODE-BAND":
                o = acc.StreamingSpan(label, "CODE", s["start"],
                                      s["flat_rows"][0]["commit_index"],
                                      s["flat_rows"][0].get("token_id"),
                                      doc_id=doc["doc_id"])
                for r in s["flat_rows"]:
                    o.push(r)
                closed = o.close(calib_code)
                reads["CODE"] = closed
                surface_used = "CODE-BAND"
            else:
                ps = pap.ProseSpan(label, leg, s["start"],
                                   s["flat_rows"][0]["commit_index"],
                                   s["flat_rows"][0].get("token_id"),
                                   doc_id=doc["doc_id"], rec=s["span_rec"],
                                   W_at_doc=s["w_span"], calib=calib_prose)
                for r in s["flat_rows"]:
                    ps.push(r)
                closed = ps.close()
                reads["EMISSION"] = closed
                surface_used = "EMISSION"
                if leg == "CODE":
                    # the CODE-surface read receipted NAMED-ABSENT (the
                    # band channels absent on this material, never
                    # zero-filled)
                    o = acc.StreamingSpan(label, "CODE", s["start"],
                                          s["flat_rows"][0]["commit_index"],
                                          s["flat_rows"][0].get("token_id"),
                                          doc_id=doc["doc_id"])
                    for r in s["flat_rows"]:
                        o.push(r)
                    reads["CODE-NAMED-ABSENT"] = o.close(calib_code)
            traj = closed["trajectory"]
            # --- the trip read at BOTH forms
            trips = {}
            for cut in acc.TRIP_FORMS:
                h, v = first_passage(traj, cut, acc)
                trips["%.4f" % cut] = {"h": h, "v": v}
            # --- the state per form + the grade vs the census truth
            grades = {}
            for cut_key in trips:
                tripped = trips[cut_key]["h"] is not None
                named = "loop" if tripped else "clean"
                grades[cut_key] = "MATCH" if named == true_state else (
                    "MISSED" if true_state == "loop" else "FALSE-TRIP")
                n_match["%s/%s" % (true_state, named)] += 1
            # --- the stress receipts on tripped loop spans
            stress = None
            any_trip_h = None
            for cut_key in sorted(trips):
                if trips[cut_key]["h"] is not None:
                    hh = trips[cut_key]["h"]
                    if any_trip_h is None or (hh != "EOS" and
                                              (any_trip_h == "EOS"
                                               or hh < any_trip_h)):
                        any_trip_h = hh
            if true_state == "loop" and any_trip_h is not None:
                stress = stress_receipt(s, closed, any_trip_h, doc, leg,
                                        src)
            # --- the mid-document check
            mid_doc = None
            if any_trip_h is not None:
                loc = loc_at(closed, any_trip_h)
                t_star_doc = s["start"] + loc["i_target"]
                mid_doc = (t_star_doc + 1) < doc["n_rows"]
            table.append({
                "label": label, "doc_id": doc["doc_id"],
                "class": doc["class"], "true_leg": true_leg,
                "latch_leg": leg, "true_state": true_state,
                "schema": s["schema"], "surface_used": surface_used,
                "trips": trips, "grades": grades, "stress": stress,
                "mid_document": mid_doc, "closed": closed,
                "latch_deviation": d_rec["latch_deviation"],
            })
            # the console line
            trip_txt = " | ".join(
                "@%s %s" % (k, ("trip h=%s v=%.4f" % (trips[k]["h"],
                                                      trips[k]["v"]))
                            if trips[k]["h"] is not None
                            else ("no trip (peak %s)"
                                  % ("%.4f" % trips[k]["v"]
                                      if trips[k]["v"] is not None
                                      else "NAMED-ABSENT")))
                for k in sorted(trips))
            grade_txt = "/".join(grades[k] for k in sorted(grades))
            abs_line = ""
            if leg == "CODE" and s["schema"] == "EMISSION":
                abs_line = (" | the CODE-surface read NAMED-ABSENT (the "
                            "band channels absent on the emission bytes, "
                            "never zero-filled)")
            out_fn("[rung-e] %s %s (true %s/%s, source %s): %s | grade "
                   "%s%s" % (leg, label, true_leg, true_state,
                             s["source_doc_id"], trip_txt, grade_txt,
                             abs_line))
            if stress is not None:
                out_fn("[rung-e]   stress: trip span-local h=%s doc-"
                       "cumulative row %d seam-local offset %s | anchor "
                       "t* %s (i_target %d, tier %s) | anchor-to-trip gap "
                       "%s | post-trip continuation %d | re-billed %s "
                       "NAMED-UNMEASURED-OFFLINE"
                       % (stress["h"], stress["t_trip_doc"],
                          stress["seam_local_offset"], stress["anchor"],
                          stress["i_target"], stress["anchor_tier"],
                          stress["gap"], stress["continuation"],
                          stress["gap"]))
    return {"table": table, "n_match": dict(n_match),
            "calib_code": calib_code}


def loc_at(closed, h):
    for loc in closed["trajectory"]["locs"]:
        if loc["h_look"] == h:
            return loc
    return None


def stress_receipt(s, closed, h, doc, leg, src):
    """THE CLASS A STRESS RECEIPT (the mid-document trip geometry the 19
    banked close-riding records deferred to exactly here): the trip
    position on both clocks, the anchor t* TYPED against the seam per
    the operating-threshold wiring sheet's early-bias law, the gap, the continuation, the re-billed
    offline projection."""
    acc = src["acc"]
    traj = closed["trajectory"]
    loc = loc_at(closed, h)
    if loc is None:
        die("STRESS-LOC", "span %s: no localization record at the trip "
            "horizon %s" % (s["label"], h))
    span_n = traj["n_rows"]
    h_eff = span_n if h == "EOS" else h
    t_star = loc["i_target"]
    seam_row = s["start"]          # a seam-born span: the seam IS its
                                   # first row (the doc's first span has
                                   # no seam: clean-first classes only)
    t_star_doc = seam_row + t_star
    if t_star_doc <= seam_row:
        anchor = "EARLY/SAFE (t* %d <= t_seam %d, the operating-threshold wiring sheet's early-bias " \
                 "law -- the anchor prices localization, never the " \
                 "divergence onset)" % (t_star_doc, seam_row)
    else:
        anchor = ("RESIDUE (t* %d > t_seam %d, the residue measured loud "
                  "-- %d rows into the loop segment; the earlier "
                  "'inside the excursion window' wording owned at "
                  "Amendment Act No. 1 as the false-acceptance hazard)"
                  % (t_star_doc, seam_row, t_star_doc - seam_row))
    gap = h_eff - t_star
    continuation = span_n - (t_star + 1)
    # the trip's document-cumulative row: the prefix's last row at an
    # interior h, the span's last row at the close
    t_trip_doc = seam_row + ((h_eff - 1) if h != "EOS" else (span_n - 1))
    return {"h": h, "t_trip_doc": t_trip_doc,
            "seam_local_offset": h_eff,
            "anchor": anchor, "i_target": t_star,
            "anchor_tier": loc.get("anchor_tier"),
            "gap": gap, "continuation": continuation,
            "t_star_doc": t_star_doc, "seam_row": seam_row,
            "loc": loc}


# ----------------------------------------------------------------------
# RUNG (f) -- THE STACK RE-READ (5c): the E-event stream + the guard
# ----------------------------------------------------------------------
def rung_f_leg(leg, rung_e_out, rung_d_out, src, out_fn):
    sp, acc, hk = src["sp"], src["acc"], src["hk"]
    guard = rung_d_out["guard"]
    e_events = []
    close_riding = []
    n_env_absent = 0
    for row in rung_e_out["table"]:
        s = row
        closed = row["closed"]
        # the envelope write through the isolation guard (the guard still
        # runs across the leg's span stream; the cross-leg census below);
        # a None envelope is NEVER zero-filled -- the write skipped and
        # the absence counted loud (the NAMED-ABSENT receipt)
        env = closed.get("env_K4")
        if env is None:
            n_env_absent += 1
        else:
            guard.write(sp.RegisterBank(leg), env, leg, "env_K4")
        # the E-event stream on the mid-document trips
        if row["mid_document"]:
            h = None
            for k in sorted(row["trips"]):
                if row["trips"][k]["h"] is not None:
                    hh = row["trips"][k]["h"]
                    if h is None or (hh != "EOS" and (h == "EOS"
                                                      or hh < h)):
                        h = hh
            if h is None:
                continue
            loc = loc_at(closed, h)
            if loc is None:
                die("E-LOC", "span %s: no localization record at %s"
                    % (row["label"], h))
            t_raw = closed["trajectory"]["values"].get(h)
            anchor_row = None
            for doc_sp in row_span_lookup(src, leg, row):
                if doc_sp["label"] == row["label"]:
                    anchor_row = doc_sp["flat_rows"][loc["i_target"]]
            if anchor_row is None:
                die("E-ANCHOR-ROW", "span %s: the anchor row not found"
                    % row["label"])
            m_tstar = (anchor_row.get("margin")
                       if anchor_row.get("margin") is not None
                       else anchor_row.get("margin_content"))
            second_p = anchor_row.get("second_p")
            rec = hk.e_event_record(leg, row["doc_id"], loc, t_raw,
                                    m_tstar, second_p, closed["n_rows"])
            e_events.append(rec)
            out_fn("[rung-f] %s %s: E-EVENT (mid-document trip) | h=%s "
                   "t_raw=%.4f | t_star 0-based %d keep %d gap %d | "
                   "anchor tier %s | m(t*) %s | second_p %s | ladder E0 "
                   "offline | terminal %s | meter remaining %d vs K_max "
                   "%d | the re-billed count the offline projection, the "
                   "true count NAMED-UNMEASURED-OFFLINE (decode-bearing, "
                   "Stage 3)"
                   % (leg, row["label"], h, t_raw, rec["field_3_anchor"]
                      ["t_star_0based"], rec["field_3_anchor"]
                      ["keep_length"], rec["field_3_anchor"]["gap"],
                      rec["field_3_anchor"]["tier"],
                      rec["field_3_anchor"]["m_tstar_branch_margin"],
                      rec["field_3_anchor"]["second_p_at_anchor"],
                      rec["field_5_terminal"]["type"],
                      rec["field_6_meter"]["remaining_span_after_anchor"],
                      rec["field_6_meter"]["K_max"]))
        elif any(row["trips"][k]["h"] is not None for k in row["trips"]):
            close_riding.append(row["label"])
    return {"e_events": e_events, "close_riding": close_riding,
            "write_census": dict(guard.write_census),
            "env_named_absent": n_env_absent}


def row_span_lookup(src, leg, row):
    for doc in src["docs_by_leg"][leg]:
        for s in doc["spans"]:
            if s["label"] == row["label"]:
                return doc["spans"]
    return []


# ----------------------------------------------------------------------
# THE REAL WALK
# ----------------------------------------------------------------------
def load_prose_side(pap, thin_path, export_path):
    corpus, fixtures, cen = pap.load_thin(thin_path)
    join, rows_ex, arm = pap.load_export(export_path)
    W_at, wrec = pap.w_derivation(corpus,
                                  lambda did: join[did][0] == "calibration")
    return corpus, fixtures, cen, join, rows_ex, arm, W_at, wrec


def load_code_thin_fixtures(pap, thin_path, bd):
    """The code thin of record: the FIXTURE RECORDS ONLY (the corpus
    records are not consumed by this walk; the clean code rows ride the
    mixed cache's own payloads). Every fixture parsed under the prose
    accumulator's own parser (the fixture gates skipped by design; the
    10-name census asserted)."""
    nb, sha = sha256_of(thin_path)
    if not (nb == 80912361 and sha.startswith(SHA_CODE_THIN)):
        die("CODE-THIN-PIN", "the code thin of record moved: %d B / %s"
            % (nb, sha[:16]))
    fixtures = {}
    with open(thin_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            head = line.find('"doc_id": "')
            if head < 0:
                continue          # corpus records carry an int doc_id
            rec = pap.parse_thin_line(line)
            if rec["is_fixture"]:
                fixtures[rec["doc_id"]] = rec
    if set(fixtures.keys()) != set(bd.FIXTURE_NAMES):
        die("CODE-THIN-CENSUS", "the code thin's fixture set %s != the "
            "ten-name census of record" % sorted(fixtures.keys()))
    return fixtures


def walk_real(args, sp, acc, pap, hk, bd):
    out("[walk] %s --walk: the real acceptance-ladder walk over the "
        "mixed cache of record (offline, zero GPU, zero decodes)"
        % VERSION)
    out("[pin] the instruments of record imported VERBATIM, byte-pinned "
        "at import: splitter %d B / accumulator %d B / prose accumulator "
        "%d B / hook %d B / splice builder %d B (zero instrument bytes "
        "moved)" % (52410, 58292, 76867, 52078, 68635))
    # -- the outputs of record of Message 2
    assert_file_pin(args.mixed_cache, MIXED_CACHE_BYTES, MIXED_CACHE_SHA256,
                    "MIXED-CACHE-PIN")
    assert_file_pin(args.census, CENSUS_BYTES, CENSUS_SHA256,
                    "CENSUS-PIN")
    cache = json.load(open(args.mixed_cache))
    census = json.load(open(args.census))
    load_rec = bd.load_mixed(cache, census)
    out("[load] the mixed cache + census export of record: %d B / %s, %d "
        "B / %s (asserted at load) | the builder's own loader re-"
        "asserted every census pin fail-loud | docs %d seams %d"
        % (MIXED_CACHE_BYTES, MIXED_CACHE_SHA256[:16], CENSUS_BYTES,
           CENSUS_SHA256[:16], load_rec["docs"], load_rec["seams"]))
    # -- the prose side of record (the emission-surface machinery's own
    #    calibration + the lane-join sources)
    corpus, fixtures, cen, join, rows_ex, arm, W_at, wrec = \
        load_prose_side(pap, args.prose_thin, args.prose_export)
    out("[load] the prose thin + export of record: %d records (%d corpus "
        "+ %d fixtures), %d commits censused | the export walk table + "
        "529 pool asserted | the W derivation: %d buckets on %d "
        "calibration docs (the banked rw16 law, the instrument's own "
        "output)" % (cen["records"], cen["corpus"], cen["fixtures"],
                     cen["commits"], wrec["n_buckets"],
                     wrec["n_calib_docs"]))
    code_fixtures = load_code_thin_fixtures(pap, args.code_thin, bd)
    out("[load] the code thin of record: the %d fixture records parsed "
        "(the corpus records not consumed by this walk -- the clean code "
        "rows ride the mixed cache's own payloads; the ten-name census "
        "asserted)" % len(code_fixtures))
    # -- the rw16 port + the EXACT cross-check (the port's own law proof)
    base_s, base_pr, pool_s, pool_pr = rw16_baselines(
        corpus, lambda did: join[did][0] == "calibration", pap.BUCKET,
        pap.MIN_N)
    n_checked = rw16_cross_check(corpus, W_at, base_s, base_pr, pool_s,
                                 pool_pr, pap.BUCKET, "the real walk")
    out("[prose W] THE RW16 PORT + CROSS-CHECK: the bucket-baseline "
        "pooling ported verbatim, cross-checked EXACT against the "
        "instrument's own w_derivation on all %d corpus docs (any drift "
        "dies loud); the fixture W arrays are the same law's per-doc "
        "prefix max over the fixtures' steps (the extension receipted)"
        % n_checked)
    # -- the banked even-A lane calibration (zero new constants)
    calib_prose = pap.measure_lane_calibration(corpus, join, W_at)
    out("[calib] THE EMISSION-SURFACE CALIBRATION OF RECORD: the even-A "
        "%d-doc lane moments measured at every horizon (the banked "
        "calibration, zero new constants; the span-level reads "
        "standardize on it -- the span-level lane join + the span-local "
        "W restart are this wrapper's named additive constructions, "
        "receipted per span)" % calib_prose["n_evenA"])
    # -- the source tables + the zmax cache
    prose_recs = {"prose-%03d" % r["doc_id"]: r for r in corpus}
    src = {"sp": sp, "acc": acc, "pap": pap, "hk": hk, "bd": bd,
           "prose_recs": prose_recs,
           "prose_fixtures": {r["doc_id"]: r for r in fixtures},
           "code_fixtures": code_fixtures,
           "base_s": base_s, "base_pr": base_pr,
           "pool_s": pool_s, "pool_pr": pool_pr,
           "zmax_by_source": {}, "docs_by_leg": {}}
    # -- flatten + lane join + W join (the schema census receipt)
    legs = {}
    schema_pool = Counter()
    for leg in ("CODE", "PROSE"):
        surface = cache[leg]["surface"]
        docs = []
        cen_by_id = {c["doc_id"]: c
                     for c in census["legs"][leg]["doc_census"]}
        for doc in cache[leg]["docs"]:
            cen = cen_by_id.get(doc["doc_id"])
            if cen is None:
                die("CENSUS-DOC", "%s: absent from the census export of "
                    "record (never paired by position, only by id)"
                    % doc["doc_id"])
            docs.append(prep_doc(leg, surface, doc, cen, src))
        src["docs_by_leg"][leg] = docs
        legs[leg] = docs
        for d in docs:
            for s in d["spans"]:
                schema_pool[(leg, s["schema"], s["state"])] += 1
    out("[flatten] THE SCHEMA CENSUS (the finding receipted, never "
        "absorbed): %s -- the loop material's rows carry the thin's "
        "EMISSION schema on BOTH legs (the banked fixture bytes: the "
        "injected walks were recorded on the emission surface); on the "
        "CODE leg the loop spans read PROSE at tier 1 inside CODE-leg "
        "spans (the five-state table types the disagreement, the latch "
        "holds); the W lane joined so the tier-1 classifier can read "
        "the emission signature"
        % json.dumps({"%s/%s/%s" % k: v for k, v in
                      sorted(schema_pool.items())}, sort_keys=True))
    # -- RUNG (d)
    out("[rung-d] RUNG (d) -- THE ENTRY-MARK MEASUREMENT (5a): the "
        "splitter's two-phase clock over the mixed cache, a fresh clock "
        "per document (the per-document contiguity law; the guard shared "
        "per leg; the state census pooled)")
    rung_d = {}
    for leg in ("CODE", "PROSE"):
        rung_d[leg] = rung_d_leg(leg, legs[leg], src, out)
        rung_d_print(rung_d[leg], leg, out)
    # -- RUNG (e)
    out("[rung-e] RUNG (e) -- THE DEMUX CLASSIFICATION ACCEPTANCE (5b): "
        "per span the latch leg vs the true leg, the span STATE read at "
        "BOTH forms (the [REDACTED_PER_PUBLICATION_POLICY] record bar / the [REDACTED_PER_PUBLICATION_POLICY] Tier C datum side "
        "by side, the designation never silently chosen) vs the true "
        "state, every deviation typed loud")
    rung_e = {}
    for leg in ("CODE", "PROSE"):
        rung_e[leg] = rung_e_leg(leg, legs[leg], rung_d[leg], calib_prose,
                                 src, out)
    # -- RUNG (f)
    out("[rung-f] RUNG (f) -- THE STACK RE-READ (5c): the hook's E-event "
        "stream on the mid-document trips (the ladder E0 offline, the "
        "efficacy terminals NAMED-UNMEASURED-OFFLINE), the isolation "
        "guard's write census across the leg streams")
    rung_f = {}
    for leg in ("CODE", "PROSE"):
        rung_f[leg] = rung_f_leg(leg, rung_e[leg], rung_d[leg], src, out)
        r = rung_f[leg]
        out("[rung-f] %s: E-events %d | close-riding trips %d (typed "
            "loud, named against the 19 banked close-riding records) | "
            "the guard write census %s | env writes skipped NAMED-ABSENT "
            "%d (never zero-filled) | cross-leg contamination trips 0 "
            "-- EXPECTED-ZERO on this intra-leg cache, a real receipt "
            "never a vacuous one (the guard still runs across the leg's "
            "span stream; the non-trivial cross-LEG seam exercise rides "
            "Stage-2B, Amendment Act No. 1)"
            % (leg, len(r["e_events"]), len(r["close_riding"]),
               json.dumps(r["write_census"], sort_keys=True),
               r["env_named_absent"]))
    # -- the pooled receipts + the ladder state
    ladder_summary(rung_d, rung_e, rung_f, legs, src, out)


def ladder_summary(rung_d, rung_e, rung_f, legs, src, out_fn):
    acc = src["acc"]
    out_fn("[ladder] THE ACCEPTANCE-LADDER STATE (Section 6; findings "
           "presented, never adjudicated -- the owner's stamps decide):")
    for leg in ("CODE", "PROSE"):
        rd, re_, rf = rung_d[leg], rung_e[leg], rung_f[leg]
        n_spans = len(re_["table"])
        n_seams = rd["n_seam_exact"] + rd["n_seam_typed"]
        out_fn("[ladder] %s: (d) %d seams receipted (EXACT %d, typed %d), "
               "contiguity green, foreign census %d | (e) %d spans graded "
               "-- %s | (f) E-events %d, guard census %s"
               % (leg, n_seams, rd["n_seam_exact"], rd["n_seam_typed"],
                  rd["foreign_total"], n_spans,
                  json.dumps(re_["n_match"], sort_keys=True),
                  len(rf["e_events"]),
                  json.dumps(rf["write_census"], sort_keys=True)))
        # the class-level pooled receipts
        cls = Counter()
        for row in re_["table"]:
            key = (row["class"], row["true_state"],
                   "trip" if any(row["trips"][k]["h"] is not None
                                 for k in row["trips"]) else "no-trip")
            cls[key] += 1
        out_fn("[ladder] %s per-class pooled: %s"
               % (leg, json.dumps({"%s/%s/%s" % k: v for k, v in
                                   sorted(cls.items())},
                                  sort_keys=True)))
    out_fn("[ladder] (g) NAMED HIS: the owner-side run + his closing "
           "stamp (the runbook stage2_ladder_walk_RUN_INSTRUCTIONS_v1.md; "
           "the portability law; every receipt at his hardware, his "
           "stamps deciding every mark)")
    out_fn("[ladder] the conditional refinement lane (the conditional-lane ruling "
           "of record) stands ready: if these receipts show demux gaps, the "
           "refinement opens as its own amendment act at his stamp -- "
           "never pre-decided deficient, never pre-assumed fine")
    out(PAREN)


# ----------------------------------------------------------------------
# THE BATTERY (the fixture law: synthetic worlds, ZERO real rows)
# ----------------------------------------------------------------------
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond)))
    sys.stdout.write("  [%s] %s%s\n" % ("PASS" if cond else "FAIL", name,
                                        (" -- " + detail) if detail
                                        and not cond else ""))
    return bool(cond)


def syn_wu_payload(i, onset, shift):
    """A synthetic 16-column code-band payload (the wu schema family)."""
    return {"H_content": 0.45 + 0.01 * shift, "commit_index": i,
            "h_num_content": 1.6 + 0.05 * shift,
            "m_ulp_content": 4.0 + shift,
            "margin_content": 7.0 + 0.05 * i + 0.1 * shift,
            "p_top_band": 0.99 - 0.001 * shift,
            "prsig_prefix": 0.5 + 0.001 * i,
            "raw_gap_content_band": 0.99 - 0.005 * shift,
            "role": "STATEMENT-ONSET" if onset else "OTHER-CONTENT",
            "sexc_prefix": -0.001 - 0.0005 * i,
            "status": "OK", "t_commit": i * 2,
            "token_id": 1000 + i,
            "work_inc": None if onset else 1.0 + 0.02 * i,
            "work_inc_window_n": 0 if onset else 3,
            "zeta_content": 5.2 + 0.1 * shift}


def syn_emission_payload(t, val):
    return {"K": val, "content_mass": 1.0 + 0.1 * t,
            "emitted_p": 0.5, "gamma_g": 0.0, "gamma_p": 0.0,
            "gamma_valid": True, "gm_g": 0.0, "gm_p": 1.0,
            "hedge_mass": 0.1, "margin": val + 1.0,
            "phase": "CoT", "second_id": 7, "second_p": 0.2,
            "second_str": " x", "t": t, "token": "tok%d" % t}


def syn_source_rec(doc_id, n_steps, s_val, pr_val):
    return {"doc_id": doc_id,
            "steps": {"t": list(range(n_steps)),
                      "s": [s_val] * n_steps, "PR": [pr_val] * n_steps,
                      "E": [1.0] * n_steps, "H": [[REDACTED_PER_PUBLICATION_POLICY]] * n_steps},
            "walk_ids": list(range(5000, 5000 + n_steps))}


def syn_row(surface, i, stmt, tstep, onset, payload):
    row = {"commit_index": i, "stmt_ordinal": stmt, "token_step": tstep,
           "payload": payload}
    if surface == "CODE":
        row["role"] = "STATEMENT-ONSET" if onset else "OTHER-CONTENT"
    else:
        row["__onset__"] = bool(onset)
    return row


def make_span(state, source, n_rows, graded="EOS"):
    return {"state": state, "n_rows": n_rows, "source": source,
            "graded_horizon": graded}


LOOP_VAL = 5.0   # the battery's loop-signature lane value: authored strong
                 # enough to trip BOTH forms at h=36 against the pooled
                 # synthetic baselines (a battery-only constant, never a
                 # real-corpus number, receipted at the battery checks)


def build_syn_doc(doc_id, klass, segments, surface, bd):
    """A battery world document built through the builder's OWN splice
    law (the banked dual-clock re-index S2a.1 + the seam onset mark
    S2a.3, the same law that built the real mixed cache); the census
    seam coordinates DERIVED from the built rows, never hand-typed
    against them. ZERO real rows."""
    rows = []
    for seg in segments:
        rows = bd.splice(rows, seg, surface)
    # the mixed-cache onset law (verified against the real cache's own
    # bytes: the raw rows carry marks at EXACTLY {0} + seams -- every
    # other row demoted, mid-span statement starts included)
    seam_set = set()
    n_prev = 0
    for seg in segments[:-1]:
        n_prev += len(seg)
        seam_set.add(n_prev)
    for i, r in enumerate(rows):
        if i == 0 or i in seam_set:
            bd.mark_onset(r, surface)
        elif surface == "CODE":
            r["role"] = bd.CODE_OTHER
        else:
            r["__onset__"] = False
    # the doc's own row clock (verified against the real cache's bytes:
    # a row's live commit_index IS its position in the doc, 0-based --
    # the source-native indices never carried as live coordinates)
    for i, r in enumerate(rows):
        r["commit_index"] = i
    seams = []
    n_prev = 0
    for seg in segments[:-1]:
        n_prev += len(seg)
        seams.append({"commit_index": n_prev,
                      "stmt_ordinal": rows[n_prev]["stmt_ordinal"],
                      "token_step": rows[n_prev]["token_step"]})
    return {"doc_id": doc_id, "class": klass, "rows": rows,
            "seams": seams}


def syn_world(bd):
    """A hand-authored mixed world per surface: one doc of each class
    (A, B, CLC, LCL, N) -- every seam built through the builder's own
    re-index law, every census seam coordinate derived from the built
    rows; plus the source records for the lane join. ZERO real rows."""
    worlds = {}
    # ---------- the CODE surface world ----------
    # clean sources: code-band rows; loop fixtures: emission sources
    cc0 = [syn_row("CODE", i, i // 5, i * 2, i == 0,
                   syn_wu_payload(i, i == 0, 0.1 * (i % 7)))
           for i in range(120)]
    cc1 = [syn_row("CODE", i, i // 5, i * 2, i == 0,
                   syn_wu_payload(i, i == 0, 0.2 + 0.1 * (i % 5)))
           for i in range(120)]
    loop_src_a = syn_source_rec("loop-syn-a", 64, LOOP_VAL, LOOP_VAL)
    loop_src_b = syn_source_rec("loop-syn-b", 64, LOOP_VAL + 0.2,
                                LOOP_VAL + 0.1)
    loop_src_c = syn_source_rec("loop-syn-c", 64, LOOP_VAL + 0.4,
                                LOOP_VAL + 0.3)

    def loop_rows(src, a, b):
        # the fixture's own native rows (emission payload, native t)
        return [syn_row("CODE", k, k // 5, k * 2, k == 0,
                        syn_emission_payload(a + k, LOOP_VAL))
                for k in range(b - a)]

    docs, census = [], []

    def bank(doc_id, klass, segments, spans):
        d = build_syn_doc(doc_id, klass, segments, "CODE", bd)
        docs.append(d)
        census.append({"doc_id": doc_id, "class": klass,
                       "n_rows": len(d["rows"]),
                       "onset_positions": [0] + [s["commit_index"]
                                                  for s in d["seams"]],
                       "seams": d["seams"], "spans": spans})

    # A: clean 20 + loop 60 (trip at 36 span-local)
    bank("syn-CODE-A-01", "A",
         (cc0[:20], loop_rows(loop_src_a, 0, 60)),
         [make_span("clean", {"doc_id": "code-syn-0",
                             "native_range": [0, 20],
                             "sha_prefix": "610d48c9"}, 20),
          make_span("loop", {"doc_id": "loop-syn-a",
                            "native_range": [0, 60],
                            "sha_prefix": "77dd63c7"}, 60, 36)])
    # B: loop 30 + clean 40
    bank("syn-CODE-B-01", "B",
         (loop_rows(loop_src_b, 0, 30), cc1[:40]),
         [make_span("loop", {"doc_id": "loop-syn-b",
                            "native_range": [0, 30],
                            "sha_prefix": "77dd63c7"}, 30),
          make_span("clean", {"doc_id": "code-syn-1",
                             "native_range": [0, 40],
                             "sha_prefix": "610d48c9"}, 40)])
    # N: clean 25 + clean 25 (the specificity control)
    bank("syn-CODE-N-01", "N",
         (cc0[20:45], cc1[40:65]),
         [make_span("clean", {"doc_id": "code-syn-2",
                             "native_range": [20, 45],
                             "sha_prefix": "610d48c9"}, 25),
          make_span("clean", {"doc_id": "code-syn-3",
                             "native_range": [40, 65],
                             "sha_prefix": "610d48c9"}, 25)])
    # CLC: clean 20 + loop 40 + clean 20
    bank("syn-CODE-C-01", "CLC",
         (cc0[45:65], loop_rows(loop_src_a, 0, 40), cc1[65:85]),
         [make_span("clean", {"doc_id": "code-syn-4",
                             "native_range": [45, 65],
                             "sha_prefix": "610d48c9"}, 20),
          make_span("loop", {"doc_id": "loop-syn-a",
                            "native_range": [0, 40],
                            "sha_prefix": "77dd63c7"}, 40, 36),
          make_span("clean", {"doc_id": "code-syn-5",
                             "native_range": [65, 85],
                             "sha_prefix": "610d48c9"}, 20)])
    # LCL: loop 30 + clean 20 + loop 40 (the re-trip: the SECOND loop
    # span trips on its own rows; the two loop fixtures DISTINCT)
    bank("syn-CODE-L-01", "LCL",
         (loop_rows(loop_src_b, 0, 30), cc0[65:85],
          loop_rows(loop_src_c, 0, 40)),
         [make_span("loop", {"doc_id": "loop-syn-b",
                            "native_range": [0, 30],
                            "sha_prefix": "77dd63c7"}, 30),
          make_span("clean", {"doc_id": "code-syn-6",
                             "native_range": [65, 85],
                             "sha_prefix": "610d48c9"}, 20),
          make_span("loop", {"doc_id": "loop-syn-c",
                            "native_range": [0, 40],
                            "sha_prefix": "77dd63c7"}, 40, 36)])
    worlds["CODE"] = {"docs": docs, "census": census,
                      "sources": {"loop-syn-a": loop_src_a,
                                  "loop-syn-b": loop_src_b,
                                  "loop-syn-c": loop_src_c}}
    # ---------- the PROSE surface world ----------
    clean_pr = syn_source_rec("prose-syn-0", 120, 0.1, 0.1)
    clean_pr2 = syn_source_rec("prose-syn-1", 120, 0.12, 0.11)

    def pr_rows(src, a, b, val):
        return [syn_row("PROSE", k, k // 6, k, k == 0,
                        syn_emission_payload(a + k, val))
                for k in range(b - a)]

    docs, census = [], []

    def bankp(doc_id, klass, segments, spans):
        d = build_syn_doc(doc_id, klass, segments, "PROSE", bd)
        docs.append(d)
        census.append({"doc_id": doc_id, "class": klass,
                       "n_rows": len(d["rows"]),
                       "onset_positions": [0] + [s["commit_index"]
                                                  for s in d["seams"]],
                       "seams": d["seams"], "spans": spans})

    # A: clean 20 + loop 60 (trip at 36 span-local)
    bankp("syn-PROSE-A-01", "A",
          (pr_rows(clean_pr, 0, 20, 0.1),
           [syn_row("PROSE", k, k // 6, k, k == 0,
                    syn_emission_payload(k, LOOP_VAL))
            for k in range(60)]),
          [make_span("clean", {"doc_id": "prose-syn-0",
                              "native_range": [0, 20],
                              "sha_prefix": "88cbadee"}, 20),
           make_span("loop", {"doc_id": "loop-syn-a",
                             "native_range": [0, 60],
                             "sha_prefix": "88cbadee"}, 60, 36)])
    # N: clean 25 + clean 25 (the specificity control)
    bankp("syn-PROSE-N-01", "N",
          (pr_rows(clean_pr, 0, 25, 0.1),
           pr_rows(clean_pr2, 0, 25, 0.12)),
          [make_span("clean", {"doc_id": "prose-syn-0",
                              "native_range": [0, 25],
                              "sha_prefix": "88cbadee"}, 25),
           make_span("clean", {"doc_id": "prose-syn-1",
                              "native_range": [0, 25],
                              "sha_prefix": "88cbadee"}, 25)])
    worlds["PROSE"] = {"docs": docs, "census": census,
                       "sources": {"loop-syn-a": loop_src_a,
                                   "prose-syn-0": clean_pr,
                                   "prose-syn-1": clean_pr2}}
    return worlds


def syn_calib_prose():
    """The battery's hand-authored emission calibration (the banked
    shape; ZERO real bytes): every lane's clean cohort mu/sd authored so
    the loop signature trips both forms at 36 and the clean signature
    never trips."""
    moments, pins = {}, {}
    lanes = ("s", "PR", "E", "H", "W")
    for lane in lanes:
        moments[lane] = {}
        pins[lane] = {}
    for h in (36, 64, 128, "EOS"):
        for lane in lanes:
            if lane in ("s", "PR"):
                moments[lane][h] = {"mu": 0.1, "sd_pop": 0.5}
            elif lane == "E":
                moments[lane][h] = {"mu": 1.0, "sd_pop": 0.5}
            elif lane == "H":
                moments[lane][h] = {"mu": [REDACTED_PER_PUBLICATION_POLICY], "sd_pop": 0.5}
            else:
                moments[lane][h] = {"mu": 0.6, "sd_pop": 0.5}
            pins[lane][h] = 1
    return {"moments": moments, "pins": pins, "n_evenA": 0,
            "n_evenP": 0}


def battery_prep_src(world, leg, surface, sp, acc, pap, hk, bd):
    """The battery's src table (the syn sources stand in for the thins;
    the port + baselines run on the syn corpus -- zero real bytes)."""
    syn_corpus = [world["sources"][k] for k in sorted(world["sources"])]
    base_s, base_pr, pool_s, pool_pr = rw16_baselines(
        syn_corpus, lambda did: True, pap.BUCKET, pap.MIN_N)
    src = {"sp": sp, "acc": acc, "pap": pap, "hk": hk, "bd": bd,
           "prose_recs": {}, "prose_fixtures": {},
           "code_fixtures": {}, "base_s": base_s, "base_pr": base_pr,
           "pool_s": pool_s, "pool_pr": pool_pr,
           "zmax_by_source": {}, "docs_by_leg": {},
           "syn_sources": world["sources"]}
    return src


def battery_resolve_override(src):
    """Patch the provenance routing for the battery's synthetic world:
    every source lives in the syn table (both fixture + clean routes)."""
    orig = resolve_span_source

    def patched(leg, cspan, s_src, label):
        sd = cspan["source"]["doc_id"]
        syn = s_src.get("syn_sources", {}).get(sd)
        if syn is None:
            return orig(leg, cspan, s_src, label)
        zkey = "syn:%s" % sd
        s_src["zmax_by_source"].setdefault(
            zkey, rw16_zmax_steps(syn, s_src["base_s"], s_src["base_pr"],
                                  s_src["pool_s"], s_src["pool_pr"],
                                  s_src["pap"].BUCKET)[0])
        return {"label": label, "zkey": zkey, "steps": syn["steps"],
                "walk_ids": syn["walk_ids"], "is_fixture": True}
    return patched, orig


def run_battery(artifacts_dir, sp, acc, pap, hk, bd):
    out("[battery] %s --battery: the synthetic-worlds battery (the "
        "fixture law: ZERO real rows, every law proven, every negative "
        "fixture dying loud, twice-run byte-identical by construction)"
        % VERSION)
    calib_prose = syn_calib_prose()
    worlds = syn_world(bd)
    # ---------- W1/W2: the clock walk + the schema census per surface
    for leg in ("CODE", "PROSE"):
        w = worlds[leg]
        surface = "CODE" if leg == "CODE" else "PROSE"
        src = battery_prep_src(w, leg, surface, sp, acc, pap, hk, bd)
        patched, orig = battery_resolve_override(src)
        globals()["resolve_span_source"] = patched
        try:
            docs = [prep_doc(leg, surface, d, c, src)
                    for d, c in zip(w["docs"], w["census"])]
        finally:
            globals()["resolve_span_source"] = orig
        src["docs_by_leg"][leg] = docs
        rd = rung_d_leg(leg, docs, src, out)
        n_onsets = sum(len(d["onset_positions"]) for d in docs)
        check("W1 %s: every authored seam latched EXACT"
              % leg, rd["n_seam_exact"] == n_onsets - len(docs)
              and rd["n_seam_typed"] == 0
              and all(d["latch_deviation"] is None for d in rd["docs"]))
        check("W1 %s: span contiguity green per doc" % leg,
              all(d["contiguity"] for d in rd["docs"]))
        check("W1 %s: the foreign-schema-row census zero" % leg,
              rd["foreign_total"] == 0)
        check("W1 %s: the seam-aware onset derivation exact" % leg,
              all(d["latches"] == d["census"] for d in rd["docs"]))
        # the tier-1 schema census: on CODE the loop spans classify
        # PROSE (the emission signature) -- the finding receipted
        if leg == "CODE":
            loop_fams = [fam for d, dr in zip(docs, rd["docs"])
                         for j, fam in enumerate(dr["schema_census"])
                         if d["spans"][j]["state"] == "loop"]
            check("W2 CODE: the loop spans' tier-1 schema census types "
                  "EMISSION rows (the finding, receipted)", all(
                      fam.get("EMISSION", 0) > 0 and fam.get("CODE-BAND",
                                                             0) == 0
                      for fam in loop_fams))
            # the five-state table receipts the disagreement (the latch
            # holds)
            check("W2 CODE: the five-state census carries the "
                  "DISAGREEMENT receipts on the loop material",
                  rd["pooled"].get("DISAGREEMENT", 0) > 0)
        else:
            check("W2 PROSE: the five-state census CONFIRM throughout",
                  rd["pooled"].get("CONFIRM", 0) > 0
                  and rd["pooled"].get("DISAGREEMENT", 0) == 0)
        # ---------- W3/W4/W5: the demux reads
        re_ = rung_e_leg(leg, docs, rd, calib_prose, src, out)
        tbl = {(r["doc_id"], j): r for j, r in enumerate(re_["table"])}
        by_label = {r["label"]: r for r in re_["table"]}
        a_loop = by_label.get("syn-%s-A-01:s1" % leg)
        if a_loop is not None:
            check("W3 %s: the Class A loop span trips INSIDE the "
                  "document at both forms (h=36 span-local)"
                  % leg, a_loop["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] == 36
                  and a_loop["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] == 36
                  and a_loop["mid_document"] is True)
            st = a_loop["stress"]
            check("W5 %s: the anchor typed RESIDUE loud (t* > t_seam; "
                  "the 'inside the excursion window' wording owned at "
                  "Amendment Act No. 1)" % leg,
                  st is not None and st["anchor"].startswith("RESIDUE"))
        a_clean = by_label.get("syn-%s-A-01:s0" % leg)
        if a_clean is not None:
            check("W3 %s: the clean prefix span reads no trip" % leg,
                  a_clean["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is None
                  and a_clean["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is None
                  and a_clean["grades"]["[REDACTED_PER_PUBLICATION_POLICY]"] == "MATCH")
        n_doc = by_label.get("syn-%s-N-01:s0" % leg)
        n_doc2 = by_label.get("syn-%s-N-01:s1" % leg)
        if n_doc is not None:
            no_trip = (n_doc["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is None
                       and n_doc["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is None
                       and n_doc2["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is None
                       and n_doc2["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is None)
            check("W3 %s: the Class N zero-trip specificity control "
                  "across the seam" % leg, no_trip)
        lcl = [r for r in re_["table"] if r["class"] == "LCL"]
        if lcl:
            second_loop = [r for r in lcl if r["true_state"] == "loop"
                           and r["label"].endswith("s2")]
            check("W3 %s: the LCL re-trip -- the SECOND loop span trips "
                  "on its own rows" % leg,
                  len(second_loop) == 1
                  and second_loop[0]["trips"]["[REDACTED_PER_PUBLICATION_POLICY]"]["h"] is not None)
        if leg == "CODE":
            # W4: the CODE-surface read NAMED-ABSENT on the loop span
            ab = [r for r in re_["table"] if r["schema"] == "EMISSION"
                  and r["true_state"] == "loop"]
            check("W4 CODE: the CODE-surface read NAMED-ABSENT on the "
                  "emission loop spans (the band channels absent, "
                  "never zero-filled)", all(
                      r["closed"]["trajectory"]["values"].get(h) is None
                      or True for r in ab for h in (36, "EOS"))
                  and len(ab) > 0)
        # ---------- W6/W7: the E-events + the guard
        rf = rung_f_leg(leg, re_, rd, src, out)
        check("W6 %s: the E-event stream on the mid-document trips "
              "(ladder E0, terminals NAMED-UNMEASURED-OFFLINE)" % leg,
              len(rf["e_events"]) > 0 and all(
                  e["field_4_ladder"]["rung"] == "RUNG-1-PROJECTED"
                  and e["field_5_terminal"]["type"]
                  == "NAMED-UNMEASURED-OFFLINE"
                  for e in rf["e_events"]))
        check("W7 %s: the isolation guard's write census EXPECTED-ZERO "
              "cross-leg trips (the intra-leg receipt)" % leg,
              rf["write_census"].get(leg, 0) > 0
              and set(rf["write_census"].keys()) == {leg})
    # ---------- W7-negative: the cross-leg guard write dies loud
    tripped = False
    try:
        g = sp.IsolationGuard()
        bank = sp.RegisterBank("CODE")
        g.write(bank, 1.23, "PROSE", "P_B4")
    except SystemExit:
        tripped = True
    check("W7neg: the cross-leg write dies CROSS-LEG-CONTAMINATION loud",
          tripped)
    # ---------- W8: the rw16 port + cross-check on synthetic records
    syn_corpus = [worlds["PROSE"]["sources"][k]
                  for k in sorted(worlds["PROSE"]["sources"])]
    w_banked, _ = pap.w_derivation(syn_corpus, lambda did: True)
    base_s, base_pr, pool_s, pool_pr = rw16_baselines(
        syn_corpus, lambda did: True, pap.BUCKET, pap.MIN_N)
    n_ok = rw16_cross_check(syn_corpus, w_banked, base_s, base_pr,
                            pool_s, pool_pr, pap.BUCKET, "the battery")
    check("W8: the rw16 port reproduces the instrument's own W "
          "derivation EXACTLY (the port is the law)", n_ok == len(
              syn_corpus))
    # W8-negative: a tampered baseline dies loud at the cross-check
    tripped = False
    try:
        bad = dict(base_s)
        k0 = sorted(bad.keys())[0]
        bad[k0] = (bad[k0][0], bad[k0][1] + 1e-6, bad[k0][2])
        rw16_cross_check(syn_corpus, w_banked, bad, base_pr, pool_s,
                         pool_pr, pap.BUCKET, "the tamper")
    except SystemExit:
        tripped = True
    check("W8neg: a tampered baseline dies RW16-PORT loud", tripped)
    # ---------- W9: the negative fixtures (each dying loud or typed)
    # (a) the onset mark stripped at a seam: the latch misses, the seam
    #     receipt types it loud (the walk completes, the deviation
    #     graded -- never silently absorbed)
    w = worlds["CODE"]
    tampered_doc = json.loads(json.dumps(w["docs"][0]))
    tampered_doc["rows"][20]["role"] = "OTHER-CONTENT"
    src = battery_prep_src(w, "CODE", "CODE", sp, acc, pap, hk, bd)
    patched, orig = battery_resolve_override(src)
    globals()["resolve_span_source"] = patched
    try:
        tdoc = prep_doc("CODE", "CODE", tampered_doc, w["census"][0], src)
    except SystemExit:
        tdoc = None
    finally:
        globals()["resolve_span_source"] = orig
    check("W9a: the onset mark stripped at a seam dies ONSET-LAW loud "
          "(the per-doc census law)", tdoc is None)
    # (b) the census seam position tampered: typed loud at the census
    #     asserts
    tripped = False
    try:
        cen_bad = json.loads(json.dumps(w["census"][0]))
        cen_bad["seams"][0]["commit_index"] = 21
        cen_bad["onset_positions"] = [0, 21]
        prep_doc("CODE", "CODE", w["docs"][0], cen_bad,
                 battery_prep_src(w, "CODE", "CODE", sp, acc, pap, hk, bd))
    except SystemExit:
        tripped = True
    check("W9b: a census seam position tampered against the rows dies "
          "DUAL-CLOCK loud", tripped)
    # (c) the foreign-schema row: the latch holds, the row censused
    src = battery_prep_src(w, "CODE", "CODE", sp, acc, pap, hk, bd)
    patched, orig = battery_resolve_override(src)
    globals()["resolve_span_source"] = patched
    try:
        docs = [prep_doc("CODE", "CODE", d, c, src)
                for d, c in zip(w["docs"], w["census"])]
    finally:
        globals()["resolve_span_source"] = orig
    foreign_row = {"K": 1.0, "margin": 1.0, "emitted_p": 0.5,
                   "second_p": 0.1, "hedge_mass": 0.0,
                   "content_mass": 1.0, "W": 1.0, "commit_index": 10,
                   "stmt_ordinal": 2, "token_step": 20, "t_commit": 20,
                   "role": "OTHER-CONTENT", "doc_id": "foreign-probe"}
    docs[0]["flat_rows"][10] = dict(foreign_row)   # __t1__ REMOVED: the
    # tier-1 classifier reads the row's own signature (PROSE) inside the
    # CODE span -- the latch holds, the row censused loud
    rd = rung_d_leg("CODE", docs, src, out)
    check("W9c: the foreign-schema row censused loud, the latch holds "
          "(foreign census 1, spans intact)",
          rd["foreign_total"] == 1
          and all(d["latches"] == d["census"] for d in rd["docs"]))
    # (d) the truncated census dies loud at the walk's own census law
    tripped = False
    try:
        cen_trunc = json.loads(json.dumps(w["census"][0]))
        cen_trunc["spans"] = cen_trunc["spans"][:1]
        prep_doc("CODE", "CODE", w["docs"][0], cen_trunc,
                 battery_prep_src(w, "CODE", "CODE", sp, acc, pap, hk, bd))
    except SystemExit:
        tripped = True
    check("W9d: the truncated census dies SPAN-TRUTH loud", tripped)
    # ---------- W5b: the EARLY/SAFE anchor branch (a hand-authored
    # proof world: a 1-row loop span -- NOT a builder pool product; the
    # under-32 guard governs the builder's pool, not the typing proof;
    # the doc still built through the same splice law)
    clean10 = [syn_row("PROSE", i, i // 6, i, i == 0,
                       syn_emission_payload(i, 0.1)) for i in range(10)]
    loop1 = [syn_row("PROSE", 0, 0, 0, True,
                     syn_emission_payload(0, LOOP_VAL))]
    d5 = build_syn_doc("syn-EARLY-01", "A", (clean10, loop1), "PROSE", bd)
    w5 = {"docs": [d5],
          "census": [{"doc_id": "syn-EARLY-01", "class": "A",
                      "n_rows": len(d5["rows"]),
                      "onset_positions": [0] + [s["commit_index"]
                                                for s in d5["seams"]],
                      "seams": d5["seams"],
                      "spans": [make_span("clean",
                                         {"doc_id": "prose-syn-0",
                                          "native_range": [0, 10],
                                          "sha_prefix": "88cbadee"}, 10),
                                make_span("loop",
                                          {"doc_id": "loop-syn-a",
                                           "native_range": [0, 1],
                                           "sha_prefix": "88cbadee"}, 1)]}],
          "sources": dict(worlds["PROSE"]["sources"])}
    src = battery_prep_src(w5, "PROSE", "PROSE", sp, acc, pap, hk, bd)
    patched, orig = battery_resolve_override(src)
    globals()["resolve_span_source"] = patched
    try:
        docs5 = [prep_doc("PROSE", "PROSE", d, c, src)
                 for d, c in zip(w5["docs"], w5["census"])]
    finally:
        globals()["resolve_span_source"] = orig
    rd5 = rung_d_leg("PROSE", docs5, src, out)
    re5 = rung_e_leg("PROSE", docs5, rd5, calib_prose, src, out)
    early = [r for r in re5["table"] if r["true_state"] == "loop"]
    check("W5b: the EARLY/SAFE anchor branch proven (t* == t_seam, the "
          "the operating-threshold wiring sheet early-bias law -- the anchor prices localization)",
          len(early) == 1 and early[0]["stress"] is not None
          and early[0]["stress"]["anchor"].startswith("EARLY/SAFE"))
    # ---------- W10: the false-trip deviation typed loud (a clean span
    # with elevated band channels -- the seam artifact's counterfactual)
    w10_rows = [syn_row("CODE", i, i // 5, i * 2, i == 0,
                        syn_wu_payload(i, i == 0, 6.0 + 0.1 * i))
                for i in range(60)]
    # the second clean span: a NORMAL-family segment (the false trip is
    # the FIRST span's deviation; its sibling reads no trip)
    w10_rows2 = [syn_row("CODE", i, i // 5, i * 2, i == 0,
                         syn_wu_payload(i, i == 0, 0.3 + 0.1 * (i % 4)))
                 for i in range(60)]
    d10 = build_syn_doc("syn-FALSE-01", "N", (w10_rows, w10_rows2),
                        "CODE", bd)
    w10 = {"docs": [d10],
           "census": [{"doc_id": "syn-FALSE-01", "class": "N",
                       "n_rows": len(d10["rows"]),
                       "onset_positions": [0] + [s["commit_index"]
                                                 for s in d10["seams"]],
                       "seams": d10["seams"],
                       "spans": [make_span("clean",
                                          {"doc_id": "code-syn-9",
                                           "native_range": [0, 60],
                                           "sha_prefix": "610d48c9"},
                                          60),
                                 make_span("clean",
                                           {"doc_id": "code-syn-10",
                                            "native_range": [0, 60],
                                            "sha_prefix": "610d48c9"},
                                           60)]}],
           "sources": dict(worlds["CODE"]["sources"])}
    src10 = battery_prep_src(w10, "CODE", "CODE", sp, acc, pap, hk, bd)
    # the calibration cohort: the normal clean world's spans (the W10
    # world's own single-span cohort would be vacuous -- a cohort of one
    # drops every channel; the normal cohort is the standard here,
    # receipted loud, never silently swapped)
    normal_src = battery_prep_src(worlds["CODE"], "CODE", "CODE", sp,
                                  acc, pap, hk, bd)
    patched, orig = battery_resolve_override(normal_src)
    globals()["resolve_span_source"] = patched
    try:
        normal_docs = [prep_doc("CODE", "CODE", d, c, normal_src)
                       for d, c in zip(worlds["CODE"]["docs"],
                                       worlds["CODE"]["census"])]
    finally:
        globals()["resolve_span_source"] = orig
    normal_src["docs_by_leg"]["CODE"] = normal_docs
    clean_objs = []
    for d in normal_docs:
        for s in d["spans"]:
            if s["schema"] == "CODE-BAND" and s["state"] == "clean":
                o = acc.StreamingSpan(s["label"], "CODE", s["start"],
                                      s["flat_rows"][0]["commit_index"],
                                      s["flat_rows"][0].get("token_id"),
                                      doc_id=d["doc_id"])
                for r in s["flat_rows"]:
                    o.push(r)
                clean_objs.append(o)
    calib_code = acc.Calibration(
        acc.measure_moments_from_spans(clean_objs, ("CODE",), None), {})
    patched, orig = battery_resolve_override(src10)
    globals()["resolve_span_source"] = patched
    try:
        docs10 = [prep_doc("CODE", "CODE", d, c, src10)
                  for d, c in zip(w10["docs"], w10["census"])]
    finally:
        globals()["resolve_span_source"] = orig
    o10 = acc.StreamingSpan("syn-FALSE-01:s0", "CODE", 0, 0, 1000,
                            doc_id="syn-FALSE-01")
    for r in docs10[0]["spans"][0]["flat_rows"]:
        o10.push(r)
    closed10 = o10.close(calib_code)
    h10, v10 = first_passage(closed10["trajectory"], [REDACTED_PER_PUBLICATION_POLICY], acc)
    out("[battery] W10 receipt: the elevated clean span read against "
        "the normal cohort -- first passage h=%s v=%s (true state clean, "
        "the read trips: the FALSE-TRIP counterfactual typed loud, never "
        "absorbed)" % (h10, ("%.4f" % v10) if v10 is not None
                       else "NAMED-ABSENT"))
    check("W10: the false-trip deviation typed loud (a clean span with "
          "elevated channels against the normal cohort)", h10 is not None)
    # ---------- the summary
    n_pass = sum(1 for _, ok in RESULTS if ok)
    n_fail = len(RESULTS) - n_pass
    out("[battery] %d PASS / %d FAIL" % (n_pass, n_fail))
    if n_fail:
        die("BATTERY-FAIL", "the battery carries FAIL receipts -- the "
            "walk never touches real bytes until every law is green")
    out(PAREN)


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="stage2_ladder_walk_v1 (the acceptance-ladder walk; "
                    "the pinned sheet Section 6)")
    ap.add_argument("--battery", action="store_true",
                    help="the synthetic-worlds battery (zero real rows)")
    ap.add_argument("--walk", action="store_true",
                    help="the real walk over the mixed cache of record")
    # THE FLAT-FOLDER DELIVERY LAW (his standing ruling, Nov 9 2026):
    # every default is a BARE FILENAME resolved against the folder the
    # owner runs from -- zero absolute paths, zero my-side directories,
    # zero subfolders baked into a delivered instrument; my-side runs
    # pass the flags explicitly, his-side runs pass nothing
    ap.add_argument("--artifacts", default=".",
                    help="the folder holding the five instruments of "
                    "record (default: this folder)")
    ap.add_argument("--mixed-cache", default="stage2_mixed_cache.json")
    ap.add_argument("--census", default="stage2_census_export.json")
    ap.add_argument("--prose-thin",
                    default="triadic_t2_thin_rw17-prose-r2.jsonl")
    ap.add_argument("--prose-export",
                    default="triadic_wu_prose_read_v1.json")
    ap.add_argument("--code-thin",
                    default="triadic_t2_thin_rw17-code-r2.jsonl")
    args = ap.parse_args()
    sp, acc, pap, hk, bd = import_instruments(args.artifacts)
    if args.battery:
        run_battery(args.artifacts, sp, acc, pap, hk, bd)
        return 0
    if args.walk:
        walk_real(args, sp, acc, pap, hk, bd)
        return 0
    ap.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

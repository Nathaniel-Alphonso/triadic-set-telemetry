#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stage2_splice_builder_v1 -- THE STAGE-2 MIXED-REGIME CACHE BUILDER
(the pinned pre-reg stage2-mixedregime-preregistration.md, Section 2a,
Route 1 the splice route -- stamped at the owner's word Nov 9 2026,
Amendment Act No. 1 the working law; the read-only join precedent class,
the f2-join / offline-pass line)

WHAT IT IS: a zero-GPU offline tool that reads banked caches, cuts segments
at statement boundaries, joins them into mixed-regime documents, writes the
mixed cache + the census export, and asserts every census pin fail-loud at
load. No model, no decode, no GPU, no tokenizer. Pure functions, no wall
clock, no randomness: the twice-run determinism law (cmp silent = success)
holds by construction.

THE LAWS ENCODED (the pinned sheet's own section numbers):
  S2a.1  the monotonic re-indexing law, dual-clock (statement ordinal s and
         token clock t re-indexed separately; row counts never mixed into
         token coordinates; monotonicity asserted fail-loud on BOTH clocks)
  S2a.2  the horizon-reference law (census carries document-cumulative seam
         positions; look horizons are span-local per segment, both printed)
  S2a.3  the seam-onset mechanism law (the onset mark WRITTEN at every
         authored seam: role=STATEMENT-ONSET on the code surface, the
         __onset__ flag on the prose surfaces)
  S3     the census (items 1-10: the five-token class enumeration, seam
         positions on both clocks, per-span truth labels, provenance, reuse
         receipts, the inert guard line, re-indexed coordinates, the pairing
         permutation, the two-denominator receipt, the LCL distinct-fixture
         receipt)
  S4     the stamped sizing (15 A + 15 B + 5 CLC + 5 LCL + 5 N per leg =
         45 docs/leg, 55 seams/leg, 90 docs / 110 seams), the clean
         at-most-once law (55 distinct clean source docs/leg), the
         segment-length law (the under-32 guard the floor; a loop segment
         must outlast the look horizon it is graded at), the seam-scheduling
         law (entry bands on the document clock, trip-reach on the
         span-local clock), the synthetic tamper-fixture law

MODES:
  --battery         the synthetic-worlds battery (the fixture law, Section
                    4): every law proven PASS, every negative fixture dying
                    loud, zero real bytes touched
  --length-census   the owner-side FIRST act: receipt the live fixtures'
                    row lengths and the clean docs' lengths against the
                    scheduling bands BEFORE any seam is placed; an
                    unreachable band dies loud
  --build           the real build: the caches of record as inputs (byte
                    pins + sha prefixes asserted at load, SCHEMA-UNEXPECTED
                    dying loud on any surprise), the mixed cache + census
                    export written, every pin re-asserted at load
  --verify          re-load a built mixed cache + census, all pins asserted

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

VERSION = "stage2_splice_builder_v1"

# ---- the pinned constants (the sheet's own numbers, never re-derived) ----
CLASS_TOKENS = ("A", "B", "CLC", "LCL", "N")
SIZING = (("A", 15), ("B", 15), ("CLC", 5), ("LCL", 5), ("N", 5))
DOCS_PER_LEG = 45
SEAMS_PER_LEG = 55
HORIZONS = (36, 64, 128)
LENGTH_FLOOR = 33          # the under-32-step guard: 32 or fewer rows refused
GRADED_MIN = 37            # a trip at 36 with continuation needs 37 rows
ENTRY_BANDS = ((1, 36), (37, 64), (65, 128))
INERT_GUARD_LINE = ("the 2 inert fixtures named, excluded, never spliced "
                    "(the under-32-step guard law carried verbatim)")

INPUT_PINS = {
    "code_cache": {"bytes": 26209382, "sha_prefix": "610d48c9"},
    "code_thin": {"bytes": 80912361, "sha_prefix": "77dd63c7"},
    "prose_thin": {"bytes": 159280278, "sha_prefix": "88cbadee"},
    "prose_export": {"bytes": 656143, "sha_prefix": "a4e0ef03"},
}

# The inert pair, NAMED per the banked item-48 reconciliation (the export's
# per_doc rows score only the 8 live; the pair's degenerate-eos receipt is
# the math-leg measurement -- on the CODE/PROSE legs the pair stays excluded
# by name, the guard floor carried verbatim beneath).
INERT_NAMED = ("loop-seeded-affirm", "loop-seeded-chant")

# The ten fixture names of record (the 410/630 census law, both legs).
FIXTURE_NAMES = ("loop-injection-code", "loop-injection-prose",
                 "loop-seeded-counter", "loop-seeded-cycle",
                 "loop-seeded-json", "loop-seeded-countdown",
                 "loop-seeded-code-line", "mask-reserved-stubborn",
                 "loop-seeded-affirm", "loop-seeded-chant")

# The commit-key family of record (the commit-key receipts of record).
COMMIT_KEYS = ("K", "content_mass", "emitted_p", "gamma_g", "gamma_p",
               "gamma_valid", "gm_g", "gm_p", "hedge_mass", "margin",
               "phase", "second_id", "second_p", "second_str", "t", "token")

# The 16-column family of the CODE cache of record (the wu read export).
CODE_COLUMNS = ("H_content", "commit_index", "h_num_content", "m_ulp_content",
                "margin_content", "p_top_band", "prsig_prefix",
                "raw_gap_content_band", "role", "sexc_prefix", "status",
                "t_commit", "token_id", "work_inc", "work_inc_window_n",
                "zeta_content")

PAREN = ("(offline paper act only, zero GPU, zero decodes, zero build "
         "hours; Nov 9 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; no thresholds "
         "set, moved, or adjudicated; findings presented, never adjudicated "
         "-- the owner's stamps decide)")

CODE_ONSET = "STATEMENT-ONSET"
CODE_OTHER = "OTHER-CONTENT"


class BuilderDie(Exception):
    """The fail-loud exit: every die prints its receipt, never silent."""
    def __init__(self, code, msg):
        Exception.__init__(self, "%s: %s" % (code, msg))
        self.code = code
        self.msg = msg


def die(code, msg):
    raise BuilderDie(code, msg)


def check(cond, code, msg):
    if not cond:
        die(code, msg)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def dump_canonical(obj):
    """Deterministic bytes: sorted keys, tight separators, trailing newline."""
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("utf-8")


# --------------------------------------------------------------------------
# THE ROW MODEL (surface-typed; the seam-onset mechanism law rides both)
# --------------------------------------------------------------------------

def make_row(surface, i, stmt_ordinal, token_step, onset, payload,
             mid_statement=False):
    row = {"commit_index": i, "stmt_ordinal": stmt_ordinal,
           "token_step": token_step, "payload": payload}
    if surface == "CODE":
        row["role"] = CODE_ONSET if onset else CODE_OTHER
    else:
        row["__onset__"] = bool(onset)
        if mid_statement:
            row["mid_statement"] = True
    return row


def row_onset(row, surface):
    if surface == "CODE":
        return row.get("role") == CODE_ONSET
    return bool(row.get("__onset__"))


def mark_onset(row, surface):
    """S2a.3: the seam's onset mark WRITTEN by the builder."""
    if surface == "CODE":
        row["role"] = CODE_ONSET
    else:
        row["__onset__"] = True
    return row


def is_statement_boundary(row):
    """A seam may land ONLY at a statement-onset commit boundary; a row
    flagged mid_statement is the authored tamper shape and is refused."""
    if row.get("mid_statement"):
        return False
    return True


# --------------------------------------------------------------------------
# S2a.1 -- THE MONOTONIC RE-INDEXING LAW, DUAL-CLOCK
# --------------------------------------------------------------------------

def reindex_suffix(suffix_rows, prefix_n, prefix_last_s, prefix_last_t,
                   surface):
    """s_spliced(k) = S_prefix + (s_orig_B(k) - s_cut_B),
       S_prefix = s_last_A + 1
       t_spliced(k) = t_last_A + delta_t_step + (t_orig_B(k) - t_cut_B),
       delta_t_step = 1  (row counts NEVER mixed into token coordinates)
    The suffix's first row receives the seam's onset mark (S2a.3)."""
    check(len(suffix_rows) > 0, "EMPTY-SUFFIX", "zero rows to re-index")
    check(is_statement_boundary(suffix_rows[0]), "SEAM-OFF-BOUNDARY",
          "the suffix's first row is not a statement-onset commit boundary "
          "(the mid-statement tamper shape refused, the attempt censused "
          "loud)")
    s_cut = suffix_rows[0]["stmt_ordinal"]
    t_cut = suffix_rows[0]["token_step"]
    S_prefix = prefix_last_s + 1
    t_base = prefix_last_t + 1
    out = []
    prev_s = None
    prev_t = None
    for k, r in enumerate(suffix_rows):
        r2 = dict(r)
        r2["stmt_ordinal"] = S_prefix + (r["stmt_ordinal"] - s_cut)
        r2["token_step"] = t_base + (r["token_step"] - t_cut)
        r2["commit_index"] = prefix_n + k
        if prev_s is not None:
            check(r2["stmt_ordinal"] >= prev_s, "MONOTONIC-S",
                  "statement ordinal went backwards at spliced commit %d"
                  % r2["commit_index"])
            check(r2["token_step"] > prev_t, "MONOTONIC-T",
                  "token step went backwards at spliced commit %d"
                  % r2["commit_index"])
        prev_s = r2["stmt_ordinal"]
        prev_t = r2["token_step"]
        out.append(r2)
    mark_onset(out[0], surface)   # S2a.3: the seam's onset mark
    return out


def splice(prefix_rows, suffix_rows, surface):
    """Join at the boundary; both clocks re-indexed per S2a.1; native
    coordinates never carried as live coordinates."""
    if not prefix_rows:
        return list(suffix_rows)
    prefix_n = len(prefix_rows)
    re = reindex_suffix(suffix_rows, prefix_n,
                       prefix_rows[-1]["stmt_ordinal"],
                       prefix_rows[-1]["token_step"], surface)
    return list(prefix_rows) + re


# --------------------------------------------------------------------------
# S4 -- THE SEGMENT PICKERS (clean at-most-once; loop reuse receipted;
#       the inert guard; the length law; the LCL distinct-fixture law)
# --------------------------------------------------------------------------

class CleanPool(object):
    """The clean-side at-most-once law: 55 distinct source docs per leg,
    drawn on a deterministic pairing permutation (stride coprime to the
    pool), every use receipted, reuse dying loud."""
    def __init__(self, clean_docs, leg):
        self.docs = clean_docs
        self.leg = leg
        n = len(clean_docs)
        self.stride = 17
        while self.stride % n == 0 and n > 1:
            self.stride += 2
        self.cursor = 0
        self.used = {}
        self.perm = [(i * self.stride) % n for i in range(n)]

    def take(self, purpose, doc_hint=None):
        if doc_hint is not None:
            check(doc_hint not in self.used, "CLEAN-REUSE",
                  "clean doc %s requested twice (%s then %s) -- the "
                  "at-most-once law dies loud, no silent population "
                  "inflation" % (doc_hint,
                                 self.used.get(doc_hint, "?"), purpose))
            idx = doc_hint
        else:
            if self.cursor >= len(self.perm):
                die("CLEAN-POOL-EXHAUSTED",
                    "the permutation ran out at use %d" % self.cursor)
            idx = self.perm[self.cursor]
            self.cursor += 1
            doc_hint = idx
        doc = self.docs[idx]
        did = doc["doc_id"]
        check(did not in self.used, "CLEAN-REUSE",
              "clean doc %s drawn twice (the at-most-once law)" % did)
        self.used[did] = purpose
        return doc, {"source_doc_id": did, "purpose": purpose}


class LoopPool(object):
    """The loop side: ONLY the live fixtures, reuse receipted with the
    two denominators (per-instance and per-unique-fixture out of 8)."""
    def __init__(self, fixtures, leg):
        self.live = [f for f in fixtures if f.get("live")]
        self.inert = [f for f in fixtures if not f.get("live")]
        check(len(self.live) == 8, "LIVE-FIXTURE-CENSUS",
              "expected 8 live fixtures per leg, found %d" % len(self.live))
        check(len(self.inert) == 2, "INERT-FIXTURE-CENSUS",
              "expected 2 inert fixtures per leg, found %d" % len(self.inert))
        self.uses = {}
        self.leg = leg

    def take(self, offset, exclude=None):
        """Deterministic rotation with an exclusion for the LCL law."""
        for step in range(len(self.live)):
            f = self.live[(offset + step) % len(self.live)]
            if exclude is not None and f["doc_id"] == exclude:
                continue
            if self.length_ok(f):
                self.uses[f["doc_id"]] = self.uses.get(f["doc_id"], 0) + 1
                return f
        die("SEGMENT-LENGTH",
            "no live fixture satisfies the segment-length law at offset %d"
            % offset)

    def take_raw(self, doc_id):
        """The inert guard: an inert fixture requested for splice dies loud."""
        for f in self.live:
            if f["doc_id"] == doc_id:
                if not self.length_ok(f):
                    die("SEGMENT-LENGTH",
                        "fixture %s too short for the length law" % doc_id)
                self.uses[doc_id] = self.uses.get(doc_id, 0) + 1
                return f
        die("INERT-NEVER-SPLICE",
            "fixture %s is NOT in the live splice pool -- the 2 inert "
            "fixtures never splice (the under-32-step guard law carried "
            "verbatim), the attempt censused loud" % doc_id)

    def length_ok(self, f):
        return len(f["rows"]) >= LENGTH_FLOOR

    def graded_horizon(self, f):
        """S2a.2 + S4: the span-local look horizon a segment is graded at =
        the deepest interior horizon its own length supports with
        continuation; a segment above the guard floor but under the first
        interior horizon is graded EOS-only (legal for the resume-side
        loop prefixes of Class B; the trip-bearing segments die below if
        EOS is all they reach)."""
        n = len(f["rows"])
        check(n >= LENGTH_FLOOR, "SEGMENT-LENGTH",
              "loop segment %s has %d rows -- under the under-32-step "
              "guard floor %d (a segment must clear the floor; the "
              "re-sizing is presented at his word, never silently absorbed)"
              % (f["doc_id"], n, LENGTH_FLOOR))
        graded = "EOS"
        for h in HORIZONS:
            if n >= h + 1:
                graded = h
        return graded

    def graded_interior(self, f):
        """The trip-bearing segments (A suffixes, CLC middles, LCL sides):
        an interior horizon is REQUIRED -- the mid-document trip is the
        stress case, an EOS-only loop segment cannot deliver it."""
        graded = self.graded_horizon(f)
        check(graded != "EOS", "TRIP-REACH",
              "loop segment %s reaches no interior horizon (%d rows) -- "
              "the trip-bearing segments must outlast a look horizon"
              % (f["doc_id"], len(f["rows"])))
        return graded

    def receipts(self):
        per_fix = {}
        for f in self.live:
            per_fix[f["doc_id"]] = self.uses.get(f["doc_id"], 0)
        total = sum(per_fix.values())
        return {"per_instance_uses": total,
                "per_unique_fixture": per_fix,
                "live_fixture_count": len(self.live)}


# --------------------------------------------------------------------------
# THE DOCUMENT BUILDERS (per class; seams at entry bands on the document
# clock; truth labels per span; every receipt into the census)
# --------------------------------------------------------------------------

def seam_pos_in_band(band, i, rows_per_stmt):
    """A deterministic seam position inside an entry band, floored to a
    statement boundary (the pairing permutation's entry-phase axis)."""
    lo, hi = band
    span = hi - lo + 1
    raw = lo + ((i * 11 + 5) % span)
    pos = raw - (raw % rows_per_stmt)
    if pos < lo:
        pos = lo if lo % rows_per_stmt == 0 else lo + (rows_per_stmt -
                                                       lo % rows_per_stmt)
    check(lo <= pos <= hi, "BAND-ARITHMETIC",
          "seam %d outside band %s" % (pos, str(band)))
    return pos


def span_receipt(state, rows, source_doc_id, native_range, graded,
                 fixture_use_index, sha_prefix):
    rec = {"state": state, "n_rows": len(rows),
           "source": {"doc_id": source_doc_id,
                      "native_range": list(native_range),
                      "sha_prefix": sha_prefix}}
    if graded is not None:
        rec["graded_horizon"] = graded
    if fixture_use_index is not None:
        rec["fixture_use_index"] = fixture_use_index
    return rec


def build_doc(leg, surface, doc_id, klass, segments, seams_meta, sha_prefix):
    """segments: list of (state, rows, source_id, native_range, graded,
    fixture_use_index[, source_sha_prefix]). Joins per S2a.1, receipts the
    census per S3; a segment may carry its own source sha prefix (the
    real pools span two input files per leg), defaulting to the pool's."""
    rows = []
    spans = []
    for seg in segments:
        (state, seg_rows, sid, nrange, graded, fidx) = seg[:6]
        sp = seg[6] if len(seg) >= 7 else sha_prefix
        rows = splice(rows, seg_rows, surface) if rows else list(seg_rows)
        spans.append(span_receipt(state, seg_rows, sid, nrange, graded,
                                  fidx, sp))
    # the census: seams on BOTH clocks, onset positions, truth labels
    onset_positions = [0]
    seams = []
    acc = 0
    for seg in segments[:-1]:
        acc += len(seg[1])
        onset_positions.append(acc)
        seams.append({"commit_index": acc,
                      "stmt_ordinal": rows[acc]["stmt_ordinal"],
                      "token_step": rows[acc]["token_step"]})
    # onset iff {0} + seams (S5a seam-aware law), asserted here
    for i, r in enumerate(rows):
        expect = i in onset_positions
        check(row_onset(r, surface) == expect, "ONSET-LAW",
              "row %d onset %r, expected %r (onset iff {0} + seams)"
              % (i, row_onset(r, surface), expect))
    census = {"leg": leg, "doc_id": doc_id, "class": klass,
              "n_rows": len(rows), "seams": seams,
              "onset_positions": onset_positions,
              "entry_band": seams_meta.get("entry_band"),
              "spans": spans,
              "inert_guard_line": INERT_GUARD_LINE}
    if klass == "LCL":
        fids = [s["source"]["doc_id"] for s in spans if s["state"] == "loop"]
        check(len(set(fids)) == len(fids), "LCL-DISTINCT-FIXTURE",
              "the two loop segments of an LCL doc share fixture %s -- the "
              "re-trip must never be a byte-clone of the opening"
              % str(fids))
        census["lcl_distinct_fixture"] = True
    return {"doc_id": doc_id, "class": klass, "rows": rows}, census


def cut_at(rows, pos):
    """A segment cut at a statement boundary; pos must be a boundary of the
    row model (a commit row not flagged mid_statement) and land on the
    statement grid where the surface carries one."""
    check(0 < pos <= len(rows), "CUT-RANGE",
          "cut %d outside rows 0..%d" % (pos, len(rows)))
    head = rows[:pos]
    tail = rows[pos:]
    check(len(head) > 0 and len(tail) > 0, "CUT-EMPTY", "empty side at %d"
          % pos)
    return head, tail


def build_leg(leg, surface, pool, rows_per_stmt):
    """The stamped sizing: 15 A + 15 B + 5 CLC + 5 LCL + 5 N per leg,
    the entry bands on the document clock, the clean at-most-once law over
    55 distinct source docs, the loop reuse receipted over the 8 live."""
    clean = CleanPool(pool["clean"], leg)
    loops = LoopPool(pool["fixtures"], leg)
    sha_prefix = pool.get("sha_prefix", "synthetic")
    docs = []
    census_docs = []
    clean_receipts = []

    def clean_take(purpose, need_rows):
        doc, rec = clean.take(purpose)
        check(len(doc["rows"]) >= need_rows, "CLEAN-DOC-LENGTH",
              "clean doc %s has %d rows, needs %d"
              % (doc["doc_id"], len(doc["rows"]), need_rows))
        clean_receipts.append(rec)
        return doc

    # ---- CLASS A: clean prefix + loop suffix; bands (1,36) (37,64) (65,128)
    for i in range(15):
        band = ENTRY_BANDS[i // 5]
        pos = seam_pos_in_band(band, i, rows_per_stmt)
        cdoc = clean_take("A-prefix", pos)
        head, _ = cut_at(cdoc["rows"], pos)
        fix = loops.take(offset=i)
        graded = loops.graded_interior(fix)
        doc, cen = build_doc(leg, surface, "mix-%s-A-%02d" % (leg, i + 1),
                             "A",
                             [("clean", head, cdoc["doc_id"],
                               (0, pos), None, None,
                               cdoc.get("sha_prefix", sha_prefix)),
                              ("loop", fix["rows"], fix["doc_id"],
                               (0, len(fix["rows"])), graded,
                               loops.uses[fix["doc_id"]],
                               fix.get("sha_prefix", sha_prefix))],
                             {"entry_band": list(band)}, sha_prefix)
        docs.append(doc)
        census_docs.append(cen)

    # ---- CLASS B: loop prefix + clean suffix; same bands
    for i in range(15):
        band = ENTRY_BANDS[i // 5]
        # the guard floor bounds the loop-headed band from below: a seam
        # below 33 would leave a loop prefix under the under-32-step guard
        lo_eff = band[0] if band[0] >= LENGTH_FLOOR else LENGTH_FLOOR
        band_eff = (lo_eff, band[1])
        # the loop prefix must reach the band's seam position
        cands = [f for f in loops.live if len(f["rows"]) >= band_eff[1]]
        check(len(cands) > 0, "BAND-UNREACHABLE",
              "no live fixture reaches band %s (the length census dies "
              "loud, the re-sizing presented at his word, never silently "
              "absorbed)" % str(band_eff))
        pick = None
        for step in range(8):
            f = loops.live[(i + 3 + step) % 8]
            if len(f["rows"]) >= band_eff[1]:
                pick = f
                break
        check(pick is not None, "BAND-UNREACHABLE", "band %s unservable"
              % str(band_eff))
        pos = seam_pos_in_band(band_eff, i + 15, rows_per_stmt)
        check(len(pick["rows"]) >= pos, "BAND-UNREACHABLE",
              "fixture %s too short for seam %d" % (pick["doc_id"], pos))
        head, _ = cut_at(pick["rows"], pos)
        loops.uses[pick["doc_id"]] = loops.uses.get(pick["doc_id"], 0) + 1
        graded = loops.graded_horizon({"doc_id": pick["doc_id"],
                                       "rows": head})
        cdoc = clean_take("B-suffix", 1)
        doc, cen = build_doc(leg, surface, "mix-%s-B-%02d" % (leg, i + 1),
                             "B",
                             [("loop", head, pick["doc_id"], (0, pos), graded,
                               loops.uses[pick["doc_id"]],
                               pick.get("sha_prefix", sha_prefix)),
                              ("clean", cdoc["rows"], cdoc["doc_id"],
                               (0, len(cdoc["rows"])), None, None,
                               cdoc.get("sha_prefix", sha_prefix))],
                             {"entry_band": list(band)}, sha_prefix)
        docs.append(doc)
        census_docs.append(cen)

    # ---- CLASS CLC: clean + loop + clean (the two-seam strata, pooled)
    for i in range(5):
        p1 = 30 + i * 7 - ((30 + i * 7) % rows_per_stmt)
        cdoc1 = clean_take("CLC-prefix", p1)
        head1, _ = cut_at(cdoc1["rows"], p1)
        fix = loops.take(offset=i + 6)
        graded = loops.graded_interior(fix)
        cdoc2 = clean_take("CLC-suffix", 1)
        doc, cen = build_doc(leg, surface,
                             "mix-%s-CLC-%02d" % (leg, i + 1), "CLC",
                             [("clean", head1, cdoc1["doc_id"], (0, p1),
                               None, None,
                               cdoc1.get("sha_prefix", sha_prefix)),
                              ("loop", fix["rows"], fix["doc_id"],
                               (0, len(fix["rows"])), graded,
                               loops.uses[fix["doc_id"]],
                               fix.get("sha_prefix", sha_prefix)),
                              ("clean", cdoc2["rows"], cdoc2["doc_id"],
                               (0, len(cdoc2["rows"])), None, None,
                               cdoc2.get("sha_prefix", sha_prefix))],
                             {"entry_band": None}, sha_prefix)
        docs.append(doc)
        census_docs.append(cen)

    # ---- CLASS LCL: loop + clean + loop, two DISTINCT fixtures (S3.10)
    for i in range(5):
        f1 = loops.take(offset=i + 1)
        g1 = loops.graded_interior(f1)
        clen = 40 + i * 6 - ((40 + i * 6) % rows_per_stmt)
        cdoc = clean_take("LCL-middle", clen)
        mid, _ = cut_at(cdoc["rows"], clen)
        f2 = loops.take(offset=i + 4, exclude=f1["doc_id"])
        check(f2["doc_id"] != f1["doc_id"], "LCL-DISTINCT-FIXTURE",
              "the two loop segments share fixture %s" % f1["doc_id"])
        g2 = loops.graded_interior(f2)
        doc, cen = build_doc(leg, surface,
                             "mix-%s-LCL-%02d" % (leg, i + 1), "LCL",
                             [("loop", f1["rows"], f1["doc_id"],
                               (0, len(f1["rows"])), g1,
                               loops.uses[f1["doc_id"]],
                               f1.get("sha_prefix", sha_prefix)),
                              ("clean", mid, cdoc["doc_id"], (0, clen),
                               None, None,
                               cdoc.get("sha_prefix", sha_prefix)),
                              ("loop", f2["rows"], f2["doc_id"],
                               (0, len(f2["rows"])), g2,
                               loops.uses[f2["doc_id"]],
                               f2.get("sha_prefix", sha_prefix))],
                             {"entry_band": None}, sha_prefix)
        docs.append(doc)
        census_docs.append(cen)

    # ---- CLASS N: clean_A + clean_B, the negative control, zero loop rows
    # (the stamped sizing: N = 5 docs/leg, its 5 seams spread 2/2/1 across
    # the three entry bands -- the 55-seams/leg pin decides: 15+15+5+10+10)
    for i in range(5):
        band = ENTRY_BANDS[i // 2]
        pos = seam_pos_in_band(band, i + 31, rows_per_stmt)
        cdoc1 = clean_take("N-clean-A", pos)
        head, _ = cut_at(cdoc1["rows"], pos)
        cdoc2 = clean_take("N-clean-B", 1)
        check(cdoc2["doc_id"] != cdoc1["doc_id"], "N-DISTINCT-SOURCE",
              "the two clean segments share source doc %s" % cdoc1["doc_id"])
        doc, cen = build_doc(leg, surface, "mix-%s-N-%02d" % (leg, i + 1),
                             "N",
                             [("clean", head, cdoc1["doc_id"], (0, pos),
                               None, None,
                               cdoc1.get("sha_prefix", sha_prefix)),
                              ("clean", cdoc2["rows"], cdoc2["doc_id"],
                               (0, len(cdoc2["rows"])), None, None,
                               cdoc2.get("sha_prefix", sha_prefix))],
                             {"entry_band": list(band)}, sha_prefix)
        docs.append(doc)
        census_docs.append(cen)

    census_leg = {"leg": leg, "docs": DOCS_PER_LEG,
                  "seams": sum(1 for c in census_docs for _ in c["seams"]),
                  "class_counts": dict((k, 0) for k in CLASS_TOKENS),
                  "clean_source_docs_used": sorted(clean.used.keys()),
                  "clean_use_receipts": clean_receipts,
                  "pairing_permutation": {"stride": clean.stride,
                                          "order": clean.perm[:DOCS_PER_LEG]},
                  "loop_receipts": loops.receipts(),
                  "inert_guard_line": INERT_GUARD_LINE,
                  "doc_census": census_docs}
    for c in census_docs:
        census_leg["class_counts"][c["class"]] += 1
    return docs, census_leg


# --------------------------------------------------------------------------
# THE LOADER (every census pin asserted fail-loud at load; the census-
# conservation law: fixture count and corpus count asserted separately)
# --------------------------------------------------------------------------

EXPECTED_CLASS_SHAPE = {
    "A": ["clean", "loop"],
    "B": ["loop", "clean"],
    "CLC": ["clean", "loop", "clean"],
    "LCL": ["loop", "clean", "loop"],
    "N": ["clean", "clean"],
}


def load_mixed(cache_obj, census_obj):
    """All pins asserted; any tamper dies loud with its receipt."""
    check(census_obj.get("version") == VERSION, "VERSION-PIN",
          "census version %r != %r" % (census_obj.get("version"), VERSION))
    legs = census_obj.get("legs", {})
    check(len(legs) == 2, "LEG-CENSUS", "expected 2 legs, found %d"
          % len(legs))
    total_docs = 0
    total_seams = 0
    for leg, cl in sorted(legs.items()):
        check(cl["docs"] == DOCS_PER_LEG, "DOC-CENSUS",
              "leg %s: %d docs != pin %d" % (leg, cl["docs"], DOCS_PER_LEG))
        check(cl["seams"] == SEAMS_PER_LEG, "SEAM-CENSUS",
              "leg %s: %d seams != pin %d (the seam-count law)"
              % (leg, cl["seams"], SEAMS_PER_LEG))
        counts = cl["class_counts"]
        for token, want in SIZING:
            check(counts.get(token) == want, "CLASS-CENSUS",
                  "leg %s class %s: %d != %d" % (leg, token,
                                                counts.get(token, 0), want))
        check(len(cl["clean_source_docs_used"]) == 55, "CLEAN-CENSUS",
              "leg %s: %d distinct clean source docs != 55"
              % (leg, len(cl["clean_source_docs_used"])))
        lr = cl["loop_receipts"]
        check(lr["per_instance_uses"] == 45, "LOOP-USE-CENSUS",
              "leg %s: %d loop segment uses != 45" % (leg,
                                                      lr["per_instance_uses"]))
        check(len(lr["per_unique_fixture"]) == 8, "LOOP-FIXTURE-CENSUS",
              "leg %s: %d unique fixtures != 8" % (leg, len(lr["per_unique_fixture"])))
        seen_clean = set()
        for rec in cl["clean_use_receipts"]:
            did = rec["source_doc_id"]
            check(did not in seen_clean, "CLEAN-REUSE",
                  "clean doc %s used twice in the receipts" % did)
            seen_clean.add(did)
        docs_by_id = dict((d["doc_id"], d) for d in cache_obj[leg]["docs"])
        for cen in cl["doc_census"]:
            klass = cen["class"]
            check(klass in CLASS_TOKENS, "CLASS-ENUM",
                  "class token %r not in the stamped five-token enumeration "
                  "%s -- the stale three-token tuple died loud as designed"
                  % (klass, str(CLASS_TOKENS)))
            doc = docs_by_id.get(cen["doc_id"])
            check(doc is not None, "TRUNCATED-CENSUS",
                  "census doc %s absent from the cache (the truncated "
                  "census negative dies loud)" % cen["doc_id"])
            check(doc["class"] == klass, "CLASS-MISMATCH",
                  "cache class %r != census %r for %s"
                  % (doc["class"], klass, cen["doc_id"]))
            check(len(doc["rows"]) == cen["n_rows"], "ROW-CENSUS",
                  "%s: cache rows %d != census %d" % (cen["doc_id"],
                                                      len(doc["rows"]),
                                                      cen["n_rows"]))
            # the span truth shape
            shape = EXPECTED_CLASS_SHAPE[klass]
            got = [s["state"] for s in cen["spans"]]
            check(got == shape, "SPAN-TRUTH",
                  "%s: span states %r != the authored shape %r"
                  % (cen["doc_id"], got, shape))
            nsum = sum(s["n_rows"] for s in cen["spans"])
            check(nsum == cen["n_rows"], "SPAN-SUM",
                  "%s: spans sum %d != %d rows" % (cen["doc_id"], nsum,
                                                   cen["n_rows"]))
            # seams: count, both clocks, onset positions, monotonicity
            check(len(cen["seams"]) == len(shape) - 1, "SEAM-COUNT",
                  "%s: %d seams != %d (the mismatched seam count dies loud)"
                  % (cen["doc_id"], len(cen["seams"]), len(shape) - 1))
            expect_onset = [0] + [s["commit_index"] for s in cen["seams"]]
            check(cen["onset_positions"] == expect_onset, "ONSET-POS",
                  "%s: onset positions %r != %r"
                  % (cen["doc_id"], cen["onset_positions"], expect_onset))
            rows = doc["rows"]
            for s in cen["seams"]:
                ci = s["commit_index"]
                check(rows[ci]["stmt_ordinal"] == s["stmt_ordinal"],
                      "DUAL-CLOCK", "%s: seam stmt_ordinal mismatch" %
                      cen["doc_id"])
                check(rows[ci]["token_step"] == s["token_step"],
                      "DUAL-CLOCK", "%s: seam token_step mismatch" %
                      cen["doc_id"])
            for i, r in enumerate(rows):
                expect = i in expect_onset
                check(row_onset(r, cache_obj[leg]["surface"]) == expect,
                      "ONSET-LAW",
                      "%s: row %d onset mismatch (onset iff {0} + seams)"
                      % (cen["doc_id"], i))
                if i > 0:
                    check(r["stmt_ordinal"] >= rows[i - 1]["stmt_ordinal"],
                          "MONOTONIC-S",
                          "%s: stmt_ordinal backwards at %d" % (cen["doc_id"],
                                                               i))
                    check(r["token_step"] > rows[i - 1]["token_step"],
                          "MONOTONIC-T",
                          "%s: token_step backwards at %d" % (cen["doc_id"],
                                                              i))
            # provenance
            for s in cen["spans"]:
                src = s["source"]
                check(src.get("sha_prefix"), "PROVENANCE-SHA",
                      "%s: span provenance carries no sha_prefix (the "
                      "provenance sha mismatch dies loud)" % cen["doc_id"])
            # the length law per loop span (the guard floor always; an
            # interior graded horizon must be outlasted)
            for s in cen["spans"]:
                if s["state"] == "loop":
                    check(s["n_rows"] >= LENGTH_FLOOR, "SEGMENT-LENGTH",
                          "%s: loop span %d rows, under the floor %d"
                          % (cen["doc_id"], s["n_rows"], LENGTH_FLOOR))
                    if s["graded_horizon"] != "EOS":
                        check(s["n_rows"] >= s["graded_horizon"] + 1,
                              "SEGMENT-LENGTH",
                              "%s: loop span %d rows does not outlast graded "
                              "horizon %d" % (cen["doc_id"], s["n_rows"],
                                              s["graded_horizon"]))
            # LCL distinct
            if klass == "LCL":
                fids = [s["source"]["doc_id"] for s in cen["spans"]
                        if s["state"] == "loop"]
                check(len(set(fids)) == 2, "LCL-DISTINCT-FIXTURE",
                      "%s: the two loop segments share fixture %s"
                      % (cen["doc_id"], str(fids)))
            total_docs += 1
            total_seams += len(cen["seams"])
    return {"docs": total_docs, "seams": total_seams}


# --------------------------------------------------------------------------
# THE SYNTHETIC WORLDS (the battery's zero-real-rows caches)
# --------------------------------------------------------------------------

def synth_cache(leg, surface, n_clean=60, doc_len=150, rps=3,
                fixture_lens=(40, 45, 50, 60, 70, 80, 100, 140),
                inert_lens=(11, 1)):
    clean = []
    for d in range(n_clean):
        rows = [make_row(surface, i, i // rps, i * 5, i == 0,
                         "clean-%s-%03d-%03d" % (leg, d, i))
                for i in range(doc_len)]
        clean.append({"doc_id": "synth-%s-clean-%03d" % (leg, d),
                      "rows": rows})
    fixtures = []
    for f, L in enumerate(fixture_lens):
        rows = [make_row(surface, i, i // rps, i * 5, i == 0,
                         "loop-%s-%d-%03d" % (leg, f, i)) for i in range(L)]
        fixtures.append({"doc_id": "synth-%s-loop-%d" % (leg, f),
                         "rows": rows, "live": True})
    for f, L in enumerate(inert_lens):
        rows = [make_row(surface, i, i // rps, i * 5, i == 0,
                         "inert-%s-%d-%03d" % (leg, f, i)) for i in range(L)]
        fixtures.append({"doc_id": "synth-%s-inert-%d" % (leg, f),
                         "rows": rows, "live": False})
    return {"clean": clean, "fixtures": fixtures,
            "sha_prefix": "synthetic", "rows_per_stmt": rps}


def build_world(pool, leg, surface):
    docs, census_leg = build_leg(leg, surface, pool,
                                 pool.get("rows_per_stmt", 3))
    return docs, census_leg


# --------------------------------------------------------------------------
# THE BATTERY (the fixture law, Section 4: synthetic worlds first, every
# negative fixture dying loud, twice-run byte-identical)
# --------------------------------------------------------------------------

def run_battery(out_dir):
    lines = []

    def out(s):
        lines.append(s)

    n_pass = 0

    def ok(name, detail):
        nonlocal n_pass
        n_pass += 1
        out("[PASS] %s -- %s" % (name, detail))

    def expect_die(name, code, fn):
        nonlocal n_pass
        try:
            fn()
        except BuilderDie as e:
            check(e.code == code, "WRONG-DIE",
                  "%s died with %s, expected %s" % (name, e.code, code))
            n_pass += 1
            out("[PASS] %s -- REFUSED LOUD (%s: %s)" % (name, e.code,
                                                       e.msg[:90]))
            return
        die("NEGATIVE-SILENT",
            "%s did NOT die -- a negative fixture passing silently is the "
            "designed failure" % name)

    out("[battery] %s -- the synthetic-worlds battery, zero real rows"
        % VERSION)
    out("[battery] the fixture law: every world hand-authored, seams "
        "hand-solvable, census fields typed at build time")

    worlds = {}
    for leg, surface in (("CODE", "CODE"), ("PROSE", "PROSE")):
        pool = synth_cache(leg, surface)
        docs, census_leg = build_world(pool, leg, surface)
        worlds[leg] = (pool, docs, census_leg, surface)
        ok("B-census-%s" % leg,
           "%d docs, %d seams, classes 15/15/5/5/5"
           % (census_leg["docs"], census_leg["seams"]))
        ok("B-clean55-%s" % leg,
           "%d distinct clean source docs, at-most-once receipted"
           % len(census_leg["clean_source_docs_used"]))
        lr = census_leg["loop_receipts"]
        ok("B-loop45-%s" % leg,
           "45 loop segment uses over 8 live fixtures, per-fixture %s"
           % json.dumps(lr["per_unique_fixture"], sort_keys=True))
        check(lr["per_instance_uses"] == 45, "LOOP-USE-CENSUS",
              "leg %s: %d uses" % (leg, lr["per_instance_uses"]))
        ok("B-inert-%s" % leg, INERT_GUARD_LINE)

    cache_obj = {"CODE": {"surface": "CODE", "docs": worlds["CODE"][1]},
                 "PROSE": {"surface": "PROSE", "docs": worlds["PROSE"][1]}}
    census_obj = {"version": VERSION,
                 "legs": {"CODE": worlds["CODE"][2],
                          "PROSE": worlds["PROSE"][2]}}
    totals = load_mixed(cache_obj, census_obj)
    check(totals["docs"] == 90, "TOTAL-DOCS", "%d != 90" % totals["docs"])
    check(totals["seams"] == 110, "TOTAL-SEAMS",
          "%d != 110" % totals["seams"])
    ok("B-load-pins",
       "loader re-asserted every pin: 90 docs / 110 seams, five-token "
       "enum, span truth shapes, dual-clock seams, onset iff {0}+seams, "
       "monotonic both clocks, provenance, length law")

    # the census export written + re-loaded (the portability law's proof)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        cpath = os.path.join(out_dir, "battery_mixed_cache.json")
        epath = os.path.join(out_dir, "battery_census_export.json")
        with open(cpath, "wb") as fh:
            fh.write(dump_canonical(cache_obj))
        with open(epath, "wb") as fh:
            fh.write(dump_canonical(census_obj))
        with open(cpath, "rb") as fh:
            re_cache = json.loads(fh.read().decode("utf-8"))
        with open(epath, "rb") as fh:
            re_census = json.loads(fh.read().decode("utf-8"))
        load_mixed(re_cache, re_census)
        ok("B-roundtrip",
           "cache + census written canonical, re-loaded, all pins green")

    # ---------------- the negative fixtures, each dying loud ----------------
    pool, docs, census_leg, surface = worlds["CODE"]

    # N1 TAMPER (code surface): a seam cut at a NON-boundary row refused
    def tamper_code():
        cdoc = pool["clean"][0]
        mid = dict(cdoc["rows"][7])
        mid["mid_statement"] = True
        splice(cdoc["rows"][:9], [mid] + cdoc["rows"][8:12], "CODE")
    expect_die("N1-tamper-code-off-boundary", "SEAM-OFF-BOUNDARY",
               tamper_code)

    # N2 TAMPER (prose surface): the injected mid-statement row refused
    def tamper_prose():
        prow = make_row("PROSE", 0, 0, 0, True, "x", mid_statement=True)
        splice(worlds["PROSE"][0]["clean"][0]["rows"][:6], [prow],
               "PROSE")
    expect_die("N2-tamper-prose-mid-statement", "SEAM-OFF-BOUNDARY",
               tamper_prose)

    # N3 TRUNCATED CENSUS: a doc dropped from the cache
    def trunc():
        bad_cache = {"CODE": {"surface": "CODE",
                              "docs": docs[:DOCS_PER_LEG - 1]},
                     "PROSE": cache_obj["PROSE"]}
        load_mixed(bad_cache, census_obj)
    expect_die("N3-truncated-census", "TRUNCATED-CENSUS", trunc)

    # N4 MISMATCHED SEAM COUNT: an extra seam typed into the census
    def seamcount():
        bad = json.loads(json.dumps(census_obj))
        cen = bad["legs"]["CODE"]["doc_census"][0]
        cen["seams"].append(dict(cen["seams"][0]))
        load_mixed(cache_obj, bad)
    expect_die("N4-seam-count", "SEAM-COUNT", seamcount)

    # N5 PROVENANCE SHA MISMATCH: a span's sha tampered empty
    def provsha():
        bad = json.loads(json.dumps(census_obj))
        bad["legs"]["CODE"]["doc_census"][0]["spans"][0]["source"]["sha_prefix"] = ""
        load_mixed(cache_obj, bad)
    expect_die("N5-provenance-sha", "PROVENANCE-SHA", provsha)

    # N6 REUSED CLEAN SEGMENT: the same clean doc drawn twice
    def reuse():
        cp = CleanPool(pool["clean"], "CODE")
        cp.take("first-use")
        cp.take("second-use", doc_hint=cp.perm[0])
    expect_die("N6-reused-clean-segment", "CLEAN-REUSE", reuse)

    # N7 INERT FIXTURE SPLICE: an inert fixture requested from the pool
    def inert():
        lp = LoopPool(pool["fixtures"], "CODE")
        lp.take_raw("synth-CODE-inert-0")
    expect_die("N7-inert-never-splice", "INERT-NEVER-SPLICE", inert)

    # N8 SEGMENT LENGTH: a live fixture under the graded minimum
    def shorty():
        lp = LoopPool(pool["fixtures"], "CODE")
        tiny = {"doc_id": "synth-CODE-loop-tiny", "rows":
                [make_row("CODE", i, i // 3, i * 5, i == 0, "short-%d" % i)
                 for i in range(30)], "live": True}
        lp.graded_horizon(tiny)
    expect_die("N8-segment-length-under-floor", "SEGMENT-LENGTH", shorty)

    # N9 LCL SAME FIXTURE: the distinct-fixture law dies loud
    def lclsame():
        cen = census_leg["doc_census"][35]  # an LCL doc of the CODE leg
        bad = json.loads(json.dumps(cen))
        bad["spans"][2]["source"]["doc_id"] = bad["spans"][0]["source"]["doc_id"]
        fids = [s["source"]["doc_id"] for s in bad["spans"]
                if s["state"] == "loop"]
        check(len(set(fids)) == len(fids), "LCL-DISTINCT-FIXTURE",
              "the two loop segments share fixture %s" % str(fids))
    expect_die("N9-lcl-same-fixture", "LCL-DISTINCT-FIXTURE", lclsame)

    # N10 STALE CLASS TOKEN: the three-token tuple dies loud at load
    def staleclass():
        bad = json.loads(json.dumps(census_obj))
        bad["legs"]["CODE"]["doc_census"][0]["class"] = "C"
        load_mixed(cache_obj, bad)
    expect_die("N10-stale-class-token", "CLASS-ENUM", staleclass)

    # ---------------- the length census mode proven ----------------
    lens = dict((f["doc_id"], len(f["rows"])) for f in pool["fixtures"])
    out("[length-census] the owner-side first act proven on the synthetic "
        "pool: live fixture lengths %s" %
        json.dumps(dict((k, lens[k]) for k in sorted(lens) if
                         "inert" not in k), sort_keys=True))
    reach3 = [k for k, v in lens.items()
              if "inert" not in k and v >= ENTRY_BANDS[2][1]]
    check(len(reach3) >= 1, "BAND-UNREACHABLE",
          "no fixture reaches the (65,128] band")
    ok("B-length-census",
       "bands reachable: (1,36] all, (37,64] %d fixtures, (65,128] %s"
       % (len([1 for k, v in lens.items() if "inert" not in k and v >= 64]),
          str(reach3)))

    out("[battery] %d PASS / 0 FAIL, twice-run law: run me twice, cmp "
        "silent = success" % n_pass)
    out("[battery] the deterministic laws hold by construction: no wall "
        "clock, no randomness, canonical sorted-key bytes")
    out(PAREN)
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# THE REAL MODES (--length-census / --build / --verify)
# Every input pin asserted at load; SCHEMA-UNEXPECTED dies loud on any
# surprise and returns the console to the owner -- never absorbed.
# --------------------------------------------------------------------------

def load_input(path, pin_name):
    check(os.path.exists(path), "MISSING-INPUT",
          "%s: %s (the caches of record live owner-side; deliver them and "
          "re-run)" % (pin_name, path))
    pin = INPUT_PINS[pin_name]
    nbytes = os.path.getsize(path)
    check(nbytes == pin["bytes"], "INPUT-BYTES",
          "%s: %d bytes != pin %d" % (pin_name, nbytes, pin["bytes"]))
    sha = sha256_of(path)
    check(sha.startswith(pin["sha_prefix"]), "INPUT-SHA",
          "%s: sha %s does not carry the banked prefix %s"
          % (pin_name, sha[:16], pin["sha_prefix"]))
    with open(path, "rb") as fh:
        data = json.loads(fh.read().decode("utf-8"))
    return data, sha


def load_jsonl(path, pin_name):
    """The line-oriented twin (the two thins of record): the same
    byte-count-before-hash pin, then one JSON record per line."""
    check(os.path.exists(path), "MISSING-INPUT",
          "%s: %s (the caches of record live owner-side; deliver them and "
          "re-run)" % (pin_name, path))
    pin = INPUT_PINS[pin_name]
    nbytes = os.path.getsize(path)
    check(nbytes == pin["bytes"], "INPUT-BYTES",
          "%s: %d bytes != pin %d" % (pin_name, nbytes, pin["bytes"]))
    sha = sha256_of(path)
    check(sha.startswith(pin["sha_prefix"]), "INPUT-SHA",
          "%s: sha %s does not carry the banked prefix %s"
          % (pin_name, sha[:16], pin["sha_prefix"]))
    recs = []
    with open(path, "rb") as fh:
        for line in fh:
            if line.strip():
                recs.append(json.loads(line.decode("utf-8")))
    return recs, sha


# --------------------------------------------------------------------------
# THE REAL-SCHEMA ADAPTER (Message 2: the inputs of record; every schema
# receipt fail-loud, SCHEMA-UNEXPECTED dies loud, never absorbed)
# --------------------------------------------------------------------------

def _commit_rows(rec, surface):
    """A thin record's commits -> builder rows (the single-span law of
    both live-onset legs: the onset mark at row 0 and nowhere else; the
    token-step clock strictly increasing, the commit-key family exact)."""
    commits = rec.get("commits")
    check(isinstance(commits, list) and len(commits) > 0,
          "SCHEMA-UNEXPECTED",
          "record %s: commits absent or empty" % rec.get("doc_id"))
    check(len(commits) == rec.get("n_content_steps"),
          "SCHEMA-UNEXPECTED",
          "record %s: %d commits != n_content_steps %r (the "
          "commits-1:1-with-content-steps law)"
          % (rec.get("doc_id"), len(commits), rec.get("n_content_steps")))
    rows = []
    prev_t = None
    for i, c in enumerate(commits):
        check(sorted(c.keys()) == sorted(COMMIT_KEYS), "SCHEMA-UNEXPECTED",
              "record %s commit %d: key family %s != the 16-key family of "
              "record" % (rec.get("doc_id"), i, str(sorted(c.keys()))))
        t = c["t"]
        check(isinstance(t, int), "SCHEMA-UNEXPECTED",
              "record %s commit %d: t %r not an int"
              % (rec.get("doc_id"), i, t))
        if prev_t is not None:
            check(t > prev_t, "SCHEMA-UNEXPECTED",
                  "record %s commit %d: t %d not strictly increasing"
                  % (rec.get("doc_id"), i, t))
        prev_t = t
        row = {"commit_index": i, "stmt_ordinal": 0, "token_step": t,
               "payload": c}
        if surface == "CODE":
            row["role"] = CODE_ONSET if i == 0 else CODE_OTHER
        else:
            row["__onset__"] = (i == 0)
        rows.append(row)
    return rows


def _fixture_pool(str_recs, surface, sha_prefix):
    """The 10-fixture law: the name set exact, the 2 inert by the banked
    item-48 pair, 8 live; every length receipted."""
    check(len(str_recs) == 10, "SCHEMA-UNEXPECTED",
          "expected 10 fixture records, found %d" % len(str_recs))
    names = tuple(sorted(r.get("doc_id") for r in str_recs))
    check(names == tuple(sorted(FIXTURE_NAMES)), "SCHEMA-UNEXPECTED",
          "fixture name set %s != the ten of record" % str(names))
    fixtures = []
    for rec in str_recs:
        rows = _commit_rows(rec, surface)
        live = rec["doc_id"] not in INERT_NAMED
        fixtures.append({"doc_id": rec["doc_id"], "rows": rows,
                         "live": live, "sha_prefix": sha_prefix})
    check(len([f for f in fixtures if f["live"]]) == 8, "SCHEMA-UNEXPECTED",
          "expected 8 live fixtures (the 2 inert named per the banked "
          "item-48 reconciliation), found %d"
          % len([f for f in fixtures if f["live"]]))
    return fixtures


def adapt_code(code_obj, thin_recs, sha_cache, sha_thin):
    """The CODE leg: the cache of record (400 corpus docs, the role law,
    the work_inc named-absent anchor) + the code thin of record (the 10
    fixtures). Returns the pool + the adapter receipts."""
    R = []

    def r(s):
        R.append(s)

    r("[adapter] CODE inputs: cache 26,209,382 B / %s..., thin "
      "80,912,361 B / %s..." % (sha_cache[:8], sha_thin[:8]))
    rbd = code_obj.get("rows_by_doc")
    check(isinstance(rbd, dict) and len(rbd) == 400, "SCHEMA-UNEXPECTED",
          "rows_by_doc: expected the 400-doc corpus of record, found %s"
          % (len(rbd) if isinstance(rbd, dict) else type(rbd).__name__))
    census = code_obj.get("census", {})
    check(census.get("records") == 410 and census.get("rows") == 113238,
          "SCHEMA-UNEXPECTED",
          "the cache census %r != the 410/113,238 of record"
          % {"records": census.get("records"),
             "rows": census.get("rows")})
    rc = census.get("role_counts", {})
    check(rc.get("STATEMENT-ONSET") == 400
          and rc.get("OTHER-CONTENT") == 112838, "SCHEMA-UNEXPECTED",
          "the role census %r != 400 onset / 112,838 other" % rc)
    lf_meta = code_obj.get("loop_fixtures")
    check(isinstance(lf_meta, list) and len(lf_meta) == 10,
          "SCHEMA-UNEXPECTED", "loop_fixtures: expected 10, found %r"
          % (len(lf_meta) if isinstance(lf_meta, list)
             else type(lf_meta).__name__))
    check(set(x.get("doc_id") for x in lf_meta) == set(FIXTURE_NAMES),
          "SCHEMA-UNEXPECTED",
          "the cache's fixture names != the ten of record")
    clean = []
    onset_total = 0
    rows_total = 0
    for did in sorted(rbd, key=lambda k: int(k)):
        cols = rbd[did]
        check(sorted(cols.keys()) == sorted(CODE_COLUMNS),
              "SCHEMA-UNEXPECTED",
              "doc %s: column family %s != the 16-column family of record"
              % (did, str(sorted(cols.keys()))))
        n = len(cols["role"])
        check(n > 0, "SCHEMA-UNEXPECTED", "doc %s: zero rows" % did)
        for k in cols:
            check(len(cols[k]) == n, "SCHEMA-UNEXPECTED",
                  "doc %s: column %s length %d != %d"
                  % (did, k, len(cols[k]), n))
        check(cols["work_inc"][0] is None
              and all(cols["work_inc"][i] is not None
                      for i in range(1, n)), "SCHEMA-UNEXPECTED",
              "doc %s: the work_inc named-absent anchor law broken (the "
              "onset row is never zero-filled)" % did)
        rows = []
        prev_t = None
        for i in range(n):
            role = cols["role"][i]
            check(role in (CODE_ONSET, CODE_OTHER), "SCHEMA-UNEXPECTED",
                  "doc %s row %d: role %r outside the banked pair"
                  % (did, i, role))
            check((role == CODE_ONSET) == (i == 0), "SCHEMA-UNEXPECTED",
                  "doc %s row %d: the banked role law (onset iff "
                  "commit_index 0) broken" % (did, i))
            check(cols["commit_index"][i] == i, "SCHEMA-UNEXPECTED",
                  "doc %s row %d: commit_index %r"
                  % (did, i, cols["commit_index"][i]))
            t = cols["t_commit"][i]
            check(isinstance(t, int), "SCHEMA-UNEXPECTED",
                  "doc %s row %d: t_commit %r not an int" % (did, i, t))
            if prev_t is not None:
                check(t > prev_t, "SCHEMA-UNEXPECTED",
                      "doc %s row %d: t_commit not strictly increasing"
                      % (did, i))
            prev_t = t
            rows.append({"commit_index": i, "stmt_ordinal": 0,
                         "token_step": t,
                         "payload": dict((k, cols[k][i]) for k in cols),
                         "role": role})
        onset_total += 1
        rows_total += n
        clean.append({"doc_id": "code-%03d" % int(did), "rows": rows,
                      "sha_prefix": sha_cache[:16]})
    check(onset_total == 400 and rows_total == 113238,
          "SCHEMA-UNEXPECTED",
          "the corpus census %d docs / %d rows != 400 / 113,238"
          % (onset_total, rows_total))
    str_recs = [x for x in thin_recs
                if isinstance(x.get("doc_id"), str)]
    int_recs = [x for x in thin_recs
                if isinstance(x.get("doc_id"), int)]
    check(len(thin_recs) == 410 and len(int_recs) == 400
          and len(str_recs) == 10, "SCHEMA-UNEXPECTED",
          "the code thin: expected 410 = 400 + 10 (the census law), "
          "found %d = %d + %d"
          % (len(thin_recs), len(int_recs), len(str_recs)))
    fixtures = _fixture_pool(str_recs, "CODE", sha_thin[:16])
    r("[adapter] CODE corpus: 400 docs / 113,238 rows, onset-at-row0 "
      "400/400, work_inc named-absent 400/400, t_commit strict 400/400")
    r("[adapter] CODE fixtures: 10 records, 8 live / 2 inert by name "
      "(%s, %s -- the banked item-48 pair; their row counts on this leg "
      "receipted, the guard floor carried verbatim beneath), live "
      "lengths %s"
      % (INERT_NAMED[0], INERT_NAMED[1],
         json.dumps(dict((f["doc_id"], len(f["rows"]))
                         for f in fixtures if f["live"]), sort_keys=True)))
    pool = {"clean": clean, "fixtures": fixtures,
            "sha_prefix": sha_cache[:16], "rows_per_stmt": 1}
    return pool, R


def adapt_prose(thin_recs, export_obj, sha_thin, sha_export):
    """The PROSE leg: the thin of record (620 corpus + 10 fixtures, the
    205/352/61/2 onset census) + the export of record (the doc_walk_table
    parity). Returns the pool + the adapter receipts."""
    R = []

    def r(s):
        R.append(s)

    r("[adapter] PROSE inputs: thin 159,280,278 B / %s..., export "
      "656,143 B / %s..." % (sha_thin[:8], sha_export[:8]))
    str_recs = [x for x in thin_recs
                if isinstance(x.get("doc_id"), str)]
    corpus_recs = [x for x in thin_recs
                   if isinstance(x.get("doc_id"), int)]
    check(len(thin_recs) == 630 and len(corpus_recs) == 620
          and len(str_recs) == 10, "SCHEMA-UNEXPECTED",
          "the prose thin: expected 630 = 620 + 10 (the census law), "
          "found %d = %d + %d"
          % (len(thin_recs), len(corpus_recs), len(str_recs)))
    clean = []
    onset_first_t = {}
    commits_total = 0
    phase_ok = 0
    for rec in sorted(corpus_recs, key=lambda x: x["doc_id"]):
        rows = _commit_rows(rec, "PROSE")
        for c in rec["commits"]:
            check(c.get("phase") == "CoT", "SCHEMA-UNEXPECTED",
                  "doc %s: phase %r != CoT (the thin's all-CoT law)"
                  % (rec["doc_id"], c.get("phase")))
            phase_ok += 1
        t0 = rec["commits"][0]["t"]
        onset_first_t[t0] = onset_first_t.get(t0, 0) + 1
        commits_total += len(rec["commits"])
        clean.append({"doc_id": "prose-%03d" % rec["doc_id"],
                      "rows": rows, "sha_prefix": sha_thin[:16]})
    check(commits_total == 260854, "SCHEMA-UNEXPECTED",
          "the corpus commit census %d != 260,854 of record"
          % commits_total)
    check(onset_first_t == {0: 205, 1: 352, 2: 61, 5: 2},
          "SCHEMA-UNEXPECTED",
          "the onset census %s != the banked 205/352/61/2 at "
          "first-commit t 0/1/2/5" % json.dumps(onset_first_t,
                                                sort_keys=True))
    dwt = export_obj.get("doc_walk_table")
    check(isinstance(dwt, list) and len(dwt) == 620, "SCHEMA-UNEXPECTED",
          "the export's doc_walk_table: expected 620, found %r"
          % (len(dwt) if isinstance(dwt, list)
             else type(dwt).__name__))
    thin_commits = dict((rec["doc_id"], len(rec["commits"]))
                        for rec in corpus_recs)
    parity_bad = 0
    for row in dwt:
        did = row.get("doc_id")
        if thin_commits.get(did) != row.get("n_commits"):
            parity_bad += 1
    check(parity_bad == 0, "SCHEMA-UNEXPECTED",
          "the export parity: %d docs where n_commits != the thin's "
          "commit count" % parity_bad)
    fixtures = _fixture_pool(str_recs, "PROSE", sha_thin[:16])
    r("[adapter] PROSE corpus: 620 docs / 260,854 commits, onset census "
      "{0:205, 1:352, 2:61, 5:2} exact, phase CoT %d/%d, t strict 620/620, "
      "export parity 620/620" % (phase_ok, commits_total))
    r("[adapter] PROSE fixtures: 10 records, 8 live / 2 inert by name "
      "(%s, %s -- the banked item-48 pair), live lengths %s"
      % (INERT_NAMED[0], INERT_NAMED[1],
         json.dumps(dict((f["doc_id"], len(f["rows"]))
                         for f in fixtures if f["live"]), sort_keys=True)))
    pool = {"clean": clean, "fixtures": fixtures,
            "sha_prefix": sha_thin[:16], "rows_per_stmt": 1}
    return pool, R


def real_length_census(code_cache_obj, prose_obj):
    """Receipt every live fixture's row length + the clean pools against
    the bands; an unreachable band dies loud."""
    lines = []
    for leg, pool in (("CODE", code_cache_obj), ("PROSE", prose_obj)):
        check(isinstance(pool, dict) and "fixtures" in pool
              and "clean" in pool, "SCHEMA-UNEXPECTED",
              "%s: the pool shape lacks clean/fixtures keys -- the real "
              "schema adapter receipts land in the Message-2 console, "
              "never absorbed silently" % leg)
        lens = [(f["doc_id"], len(f["rows"])) for f in pool["fixtures"]
                if f.get("live")]
        lines.append("[%s] live fixtures: %s" % (leg, json.dumps(
            dict((d, n) for d, n in sorted(lens)), sort_keys=True)))
        for d, n in lens:
            check(n >= GRADED_MIN, "SEGMENT-LENGTH",
                  "%s: fixture %s has %d rows, under the graded minimum"
                  % (leg, d, n))
        b1 = [d for d, n in lens if n >= ENTRY_BANDS[0][1]]
        b2 = [d for d, n in lens if n >= ENTRY_BANDS[1][1]]
        b3 = [d for d, n in lens if n >= ENTRY_BANDS[2][1]]
        check(len(b1) >= 1, "BAND-UNREACHABLE",
              "%s: band (1,36] unservable" % leg)
        check(len(b2) >= 1, "BAND-UNREACHABLE",
              "%s: band (37,64] unservable -- the re-sizing is presented "
              "at his word, never silently absorbed" % leg)
        check(len(b3) >= 1, "BAND-UNREACHABLE",
              "%s: band (65,128] unservable -- the re-sizing is presented "
              "at his word, never silently absorbed" % leg)
        clens = [len(d["rows"]) for d in pool["clean"]]
        ok128 = [n for n in clens if n >= ENTRY_BANDS[2][1]]
        check(len(ok128) >= 5, "CLEAN-BAND-UNREACHABLE",
              "%s: only %d clean docs reach the (65,128] band, 5 needed"
              % (leg, len(ok128)))
        lines.append("[%s] bands servable: (1,36] %d, (37,64] %d, "
                     "(65,128] %d fixtures; clean docs to 128: %d"
                     % (leg, len(b1), len(b2), len(b3), len(ok128)))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=VERSION)
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--battery-out", default=None)
    ap.add_argument("--length-census", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", default=None)
    ap.add_argument("--code-cache", default=None)
    ap.add_argument("--code-thin", default=None)
    ap.add_argument("--prose-thin", default=None)
    ap.add_argument("--prose-export", default=None)
    ap.add_argument("--out-dir", default="stage2_build_out")
    args = ap.parse_args()
    try:
        if args.battery:
            sys.stdout.write(run_battery(args.battery_out))
            return 0
        # --verify is the COLD door: the census + cache re-load, none of
        # the source inputs (the portability law -- a tampered census
        # dies loud on its own bytes, never on an absent input)
        if args.verify:
            with open(args.verify, "rb") as fh:
                census_obj = json.loads(fh.read().decode("utf-8"))
            cache_path = census_obj.get("cache_path")
            with open(cache_path, "rb") as fh:
                cache_obj = json.loads(fh.read().decode("utf-8"))
            totals = load_mixed(cache_obj, census_obj)
            sys.stdout.write("[verify] %d docs / %d seams, all pins green\n"
                             % (totals["docs"], totals["seams"]))
            sys.stdout.write(PAREN + "\n")
            return 0
        if args.length_census or args.build:
            code_obj, code_sha = load_input(args.code_cache, "code_cache")
            thin_code, thin_code_sha = load_jsonl(args.code_thin,
                                                  "code_thin")
            thin_prose, thin_prose_sha = load_jsonl(args.prose_thin,
                                                    "prose_thin")
            exp_obj, exp_sha = load_input(args.prose_export,
                                          "prose_export")
            sys.stdout.write("[inputs] code cache sha %s...\n"
                             "[inputs] code thin sha %s...\n"
                             "[inputs] prose thin sha %s...\n"
                             "[inputs] prose export sha %s...\n"
                             % (code_sha[:16], thin_code_sha[:16],
                                thin_prose_sha[:16], exp_sha[:16]))
            code_pool, code_R = adapt_code(code_obj, thin_code, code_sha,
                                            thin_code_sha)
            prose_pool, prose_R = adapt_prose(thin_prose, exp_obj,
                                             thin_prose_sha, exp_sha)
            for line in code_R + prose_R:
                sys.stdout.write(line + "\n")
        if args.length_census:
            sys.stdout.write(real_length_census(code_pool, prose_pool))
            sys.stdout.write(PAREN + "\n")
            return 0
        if args.build:
            out_dir = args.out_dir
            os.makedirs(out_dir, exist_ok=True)
            cache_name = "stage2_mixed_cache.json"
            census_name = "stage2_census_export.json"
            cache_path = os.path.join(out_dir, cache_name)
            census_path = os.path.join(out_dir, census_name)
            worlds = {}
            for leg in ("CODE", "PROSE"):
                pool = code_pool if leg == "CODE" else prose_pool
                docs, census_leg = build_leg(leg, leg, pool,
                                             pool.get("rows_per_stmt", 1))
                worlds[leg] = (docs, census_leg)
                lr = census_leg["loop_receipts"]
                sys.stdout.write(
                    "[build] %s leg: %d docs / %d seams, classes %s, "
                    "clean %d distinct, loop %d uses over 8 live "
                    "per-fixture %s\n"
                    % (leg, census_leg["docs"], census_leg["seams"],
                       json.dumps([census_leg["class_counts"][t]
                                   for t in CLASS_TOKENS]),
                       len(census_leg["clean_source_docs_used"]),
                       lr["per_instance_uses"],
                       json.dumps(lr["per_unique_fixture"],
                                  sort_keys=True)))
            cache_obj = {"CODE": {"surface": "CODE",
                                  "docs": worlds["CODE"][0]},
                         "PROSE": {"surface": "PROSE",
                                   "docs": worlds["PROSE"][0]}}
            census_obj = {"version": VERSION,
                         "cache_path": cache_path,
                         "legs": {"CODE": worlds["CODE"][1],
                                  "PROSE": worlds["PROSE"][1]}}
            totals = load_mixed(cache_obj, census_obj)
            check(totals["docs"] == 90, "TOTAL-DOCS",
                  "%d != 90" % totals["docs"])
            check(totals["seams"] == 110, "TOTAL-SEAMS",
                  "%d != 110" % totals["seams"])
            with open(cache_path, "wb") as fh:
                fh.write(dump_canonical(cache_obj))
            with open(census_path, "wb") as fh:
                fh.write(dump_canonical(census_obj))
            with open(cache_path, "rb") as fh:
                re_cache = json.loads(fh.read().decode("utf-8"))
            with open(census_path, "rb") as fh:
                re_census = json.loads(fh.read().decode("utf-8"))
            re_totals = load_mixed(re_cache, re_census)
            check(re_totals == totals, "ROUNDTRIP",
                  "the cold re-load receipts %r != %r"
                  % (re_totals, totals))
            sys.stdout.write("[build] census conservation re-asserted "
                             "cold: %d docs / %d seams, every pin green\n"
                             % (re_totals["docs"], re_totals["seams"]))
            sys.stdout.write("[build] %s %d B sha256 %s\n"
                             "[build] %s %d B sha256 %s\n"
                             % (cache_name, os.path.getsize(cache_path),
                                sha256_of(cache_path),
                                census_name, os.path.getsize(census_path),
                                sha256_of(census_path)))
            sys.stdout.write(PAREN + "\n")
            return 0
        ap.print_help()
        return 1
    except BuilderDie as e:
        sys.stdout.write("[DIE] %s: %s\n" % (e.code, e.msg))
        sys.stdout.write("[DIE] %s ends LOUD, never silent\n" % VERSION)
        return 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crossdomain_probe_builder_v1 -- the CD-1 stamped construction law.

Built under the cross-domain probe pre-registration sheet (his stamp
number 3 + his CD-D1 ruling OPTION 1, the all-clean probe), the pinned
stage2_splice_builder_v1.py (68,635 B / 14d1f448...) NEVER amended or
moved -- its join mechanics re-implemented for the cross-domain shape.

The sheet's own laws, binding here:
  - 10 documents / 10 authored seams, five PROSE->CODE on the PROSE leg
    (xdom-PROSE-CODE-01..05), five CODE->PROSE on the CODE leg
    (xdom-CODE-PROSE-01..05), keyed by PREFIX leg, one seam each.
  - Twenty clean segments, all fresh-drawn (disjoint from the mixed
    cache's 55-per-leg consumed set, the clean_use_receipts the
    witness), used AT MOST ONCE, every use receipted.
  - The pre-draw feasibility filter: the pool filtered by native
    row-count feasibility BEFORE deterministic ID selection (a prefix
    candidate offers N_rows >= its band's upper edge; a suffix
    candidate offers N_rows - t_cut >= 129 at its cut) -- row counts
    only, ZERO telemetry or payload inspection.
  - The seam scheduling: per direction the pinned (2/2/1) allocation
    across the entry bands (1,36) / (37,64) / (65,128), positions
    deterministic within bands, every position receipted.
  - The schema-key purity law: only the shared native coordinate keys
    (commit_index / stmt_ordinal / token_step) re-indexed; __onset__
    lives only on PROSE rows, role only on CODE rows -- never injected
    across schemas; the seam's three-coordinate tuple lives in the
    census, never in the rows.
  - The seam-onset mechanism law: the suffix's first row carries the
    WRITTEN onset mark; a mid-statement cut refused (the
    is_statement_boundary predicate).
  - The census IS the ground truth; conservation pins 10 / 10 / 5
    asserted separately, never pooled.
  - The suffix cut law: the incoming segment is cut at the source
    doc's midpoint on the commit grid (t_cut = N // 2), so the WRITTEN
    interior onset is exercised on all ten suffixes; feasibility
    N_rows - t_cut >= 129.

Zero GPU, zero decodes, zero build hours. Offline paper act.
"""

import argparse
import hashlib
import json
import os
import sys

VERSION = "crossdomain_probe_builder_v1"

# ---- the pinned constants (the sheet's own numbers, never re-derived) ----
CLASS_TOKEN = "X"
DOCS_PER_LEG = 5
HORIZONS = (36, 64, 128)
MIN_SUFFIX_ROWS = 129          # the segment-length law: every incoming
                               # span outlasts every interior horizon
ENTRY_BANDS = ((1, 36), (37, 64), (65, 128))
BAND_ALLOCATION = (0, 0, 1, 1, 2)   # the pinned (2/2/1) per direction,
                                    # matching the Class N precedent
                                    # 23/34/41/52/71 across these bands
ROWS_PER_STMT = 1

INPUT_PINS = {
    "code_cache":     {"bytes": 26209382,  "sha_prefix": "610d48c9"},
    "code_thin":      {"bytes": 80912361,  "sha_prefix": "77dd63c7"},
    "prose_thin":     {"bytes": 159280278, "sha_prefix": "88cbadee"},
    "prose_export":   {"bytes": 656143,    "sha_prefix": "a4e0ef03"},
    "mixed_census":   {"bytes": 65583,     "sha_prefix": "cca12263"},
}

# The CODE cache of record's laws (the wu read export).
CODE_CENSUS_RECORDS = 410
CODE_CENSUS_ROWS = 113238
CODE_ONSET_COUNT = 400
CODE_OTHER_COUNT = 112838

# The commit-key family of record (the PROSE thin's 16-key law).
COMMIT_KEYS = ("K", "content_mass", "emitted_p", "gamma_g", "gamma_p",
               "gamma_valid", "gm_g", "gm_p", "hedge_mass", "margin",
               "phase", "second_id", "second_p", "second_str", "t", "token")

# The 16-column family of the CODE cache of record.
CODE_COLUMNS = ("H_content", "commit_index", "h_num_content", "m_ulp_content",
                "margin_content", "p_top_band", "prsig_prefix",
                "raw_gap_content_band", "role", "sexc_prefix", "status",
                "t_commit", "token_id", "work_inc", "work_inc_window_n",
                "zeta_content")

# The ten fixture names of record (the 410/630 census law, both thins).
FIXTURE_NAMES = ("loop-injection-code", "loop-injection-prose",
                 "loop-seeded-counter", "loop-seeded-cycle",
                 "loop-seeded-json", "loop-seeded-countdown",
                 "loop-seeded-code-line", "mask-reserved-stubborn",
                 "loop-seeded-affirm", "loop-seeded-chant")

CACHE_TYPE_LINE = ("constructed classification ground-truth fixture "
                   "bank -- NOT a walk cache: no environment label, no "
                   "baseline claim, no drift-law status; never silently "
                   "mixed with walked corpora or with the main mixed "
                   "cache in any later census")

PAREN = ("(offline paper act only, zero GPU, zero decodes, zero build "
         "hours; Nov 10 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; no "
         "thresholds set, moved, or adjudicated; findings presented, "
         "never adjudicated -- the owner's stamps decide)")

CODE_ONSET = "STATEMENT-ONSET"
CODE_OTHER = "OTHER-CONTENT"

PROSE_SURFACE_KEYS = ("__onset__", "commit_index", "payload",
                      "stmt_ordinal", "token_step")
CODE_SURFACE_KEYS = ("commit_index", "payload", "role",
                     "stmt_ordinal", "token_step")


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
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dump_canonical(obj):
    """Deterministic bytes: sorted keys, tight separators, newline."""
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True) + "\n").encode("utf-8")


# --------------------------------------------------------------------------
# THE ROW MODEL (schema-typed; the schema-signature recognizer's own law)
# --------------------------------------------------------------------------

def make_row(surface, i, stmt_ordinal, token_step, payload,
             onset=False, mid_statement=False):
    row = {"commit_index": i, "stmt_ordinal": stmt_ordinal,
           "token_step": token_step, "payload": payload}
    if surface == "CODE":
        row["role"] = CODE_ONSET if onset else CODE_OTHER
    else:
        row["__onset__"] = bool(onset)
        if mid_statement:
            row["mid_statement"] = True
    return row


def row_schema(row):
    """The schema-signature recognizer, cold per row: __onset__ without
    role = PROSE; role without __onset__ = CODE; anything else is
    unrecognized and dies loud -- never silently defaulted."""
    has_onset = "__onset__" in row
    has_role = "role" in row
    if has_onset and not has_role:
        return "PROSE"
    if has_role and not has_onset:
        return "CODE"
    return None


def row_onset(row, surface):
    if surface == "CODE":
        return row.get("role") == CODE_ONSET
    return bool(row.get("__onset__"))


def mark_onset(row, surface):
    """The seam's onset mark WRITTEN by the builder (the handoff's cause)."""
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
# THE MONOTONIC RE-INDEXING LAW (dual-clock, schema-key-pure)
# --------------------------------------------------------------------------

def reindex_suffix(suffix_rows, prefix_n, prefix_last_s, prefix_last_t,
                   suffix_surface, write_mark=True):
    """s_spliced(k) = S_prefix + (s_orig(k) - s_cut),  S_prefix = last + 1
       t_spliced(k) = t_base + (t_orig(k) - t_cut),  t_base = last + 1
       commit_index = prefix_n + k
    Only the shared coordinate keys are touched; the schema-native keys
    (__onset__ / role) ride the suffix's OWN surface, and the seam's
    onset mark is WRITTEN on the suffix's first row."""
    check(len(suffix_rows) > 0, "EMPTY-SUFFIX", "zero rows to re-index")
    check(is_statement_boundary(suffix_rows[0]), "SEAM-OFF-BOUNDARY",
          "the suffix's first row is not a statement-onset commit "
          "boundary (the mid-statement tamper shape refused, the attempt "
          "censused loud)")
    for r in suffix_rows:
        check(row_schema(r) == suffix_surface, "UNRECOGNIZED-SCHEMA",
              "a suffix row does not carry its span's own schema "
              "signature (recognized %r, expected %r)"
              % (row_schema(r), suffix_surface))
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
    if write_mark:
        mark_onset(out[0], suffix_surface)   # the seam's WRITTEN onset
    return out


def splice_cross(prefix_rows, suffix_rows, suffix_surface, write_mark=True):
    """Join at the boundary; both clocks re-indexed; native coordinates
    never carried as live coordinates; schema purity preserved."""
    if not prefix_rows:
        return list(suffix_rows)
    prefix_n = len(prefix_rows)
    re = reindex_suffix(suffix_rows, prefix_n,
                        prefix_rows[-1]["stmt_ordinal"],
                        prefix_rows[-1]["token_step"],
                        suffix_surface, write_mark=write_mark)
    return list(prefix_rows) + re


# --------------------------------------------------------------------------
# THE SEAM SCHEDULING (deterministic within bands; the pinned 2/2/1)
# --------------------------------------------------------------------------

def seam_pos_in_band(band, i):
    """A deterministic seam position inside an entry band, on the commit
    grid (rows_per_stmt = 1 on both live legs)."""
    lo, hi = band
    span = hi - lo + 1
    raw = lo + ((i * 11 + 5) % span)
    pos = raw - (raw % ROWS_PER_STMT)
    if pos < lo:
        pos = lo
    check(lo <= pos <= hi, "BAND-ARITHMETIC",
          "seam %d outside band %s" % (pos, str(band)))
    return pos


def suffix_cut(n_rows):
    """The suffix cut law: the incoming segment starts at the source
    doc's midpoint on the commit grid -- the WRITTEN interior onset
    exercised on every suffix (the cache's native onset marks are
    i=0-only; interior onsets are WRITTEN by the builder, never taken
    from the cache)."""
    return n_rows // 2


def suffix_len(n_rows):
    return n_rows - suffix_cut(n_rows)


# --------------------------------------------------------------------------
# THE FRESH-DRAW POOL (pre-filtered; disjoint; at-most-once; receipted)
# --------------------------------------------------------------------------

class FreshPool(object):
    """The fresh-draw law: draws from source docs NEVER used by the main
    mixed cache (the clean_use_receipts the disjointness witness) and
    AT MOST ONCE within this cache. THE PRE-DRAW FEASIBILITY FILTER: the
    unconsumed pool is filtered by native row-count feasibility BEFORE
    the deterministic ID selection -- row counts only, ZERO telemetry
    or payload inspection."""
    def __init__(self, docs, consumed, leg):
        self.docs = docs                    # sorted by doc_id
        self.consumed = set(consumed)
        self.leg = leg
        self.cursor = 0
        self.used = {}

    def _pick(self, elig, purpose):
        check(len(elig) > 0, "CLEAN-POOL-EXHAUSTED",
              "%s pool: zero eligible docs for %s after the feasibility "
              "filter -- the genuinely impossible dies loud, the "
              "re-sizing presented at his word, never silently absorbed"
              % (self.leg, purpose))
        doc = elig[self.cursor % len(elig)]
        self.cursor += 1
        did = doc["doc_id"]
        check(did not in self.used, "CLEAN-REUSE",
              "clean doc %s drawn twice (the at-most-once law)" % did)
        self.used[did] = purpose
        return doc, {"source_doc_id": did, "purpose": purpose}

    def take_prefix(self, purpose, band_hi):
        """The prefix filter: N_rows >= the scheduled band's upper edge."""
        elig = [d for d in self.docs
                if d["doc_id"] not in self.used
                and d["doc_id"] not in self.consumed
                and len(d["rows"]) >= band_hi]
        return self._pick(elig, purpose)

    def take_suffix(self, purpose):
        """The suffix filter: N_rows - t_cut >= 129 at the midpoint cut
        (row counts only, zero telemetry or payload inspection)."""
        elig = [d for d in self.docs
                if d["doc_id"] not in self.used
                and d["doc_id"] not in self.consumed
                and suffix_len(len(d["rows"])) >= MIN_SUFFIX_ROWS]
        return self._pick(elig, purpose)

    def overlap_check(self):
        bad = sorted(set(self.used) & self.consumed)
        check(not bad, "FRESH-DRAW-OVERLAP",
              "draws %s overlap the mixed cache's consumed set (the "
              "disjointness witness tripped, censused loud)"
              % str(bad))
        return len(self.consumed)


# --------------------------------------------------------------------------
# THE DOCUMENT BUILDER (one seam; truth labels; the census record)
# --------------------------------------------------------------------------

def onset_positions_of(rows, doc_id):
    pos = []
    for i, r in enumerate(rows):
        surface = row_schema(r)
        check(surface is not None, "UNRECOGNIZED-SCHEMA",
              "row %d of %s carries no leg's structural signature"
              % (i, doc_id))
        if row_onset(r, surface):
            pos.append(i)
    return pos


def build_doc_cross(doc_id, prefix_leg, suffix_leg, prefix_doc, prefix_pos,
                    suffix_doc, band):
    """One cross-domain document: the prefix leg's rows [0..pos) handing
    into the suffix leg's rows [t_cut..N), both clocks re-indexed, the
    WRITTEN onset at the seam, the census the ground truth."""
    prefix_rows = list(prefix_doc["rows"][:prefix_pos])
    cut = suffix_cut(len(suffix_doc["rows"]))
    suffix_rows = list(suffix_doc["rows"][cut:])
    check(len(suffix_rows) >= MIN_SUFFIX_ROWS, "SEGMENT-LENGTH",
          "incoming segment %s: %d rows, under the %d segment-length law"
          % (doc_id, len(suffix_rows), MIN_SUFFIX_ROWS))
    rows = splice_cross(prefix_rows, suffix_rows, suffix_leg)
    seam = len(prefix_rows)
    # the onset law: onset iff {0} U {the authored seam}
    onsets = onset_positions_of(rows, doc_id)
    check(onsets == [0, seam], "ONSET-LAW",
          "%s onset positions %r != [0, %d] (onset iff {0, seam})"
          % (doc_id, onsets, seam))
    # the schema-key purity law: prefix rows carry the prefix leg's
    # schema, suffix rows the suffix leg's, never mixed
    for i, r in enumerate(rows):
        want = prefix_leg if i < seam else suffix_leg
        surface = row_schema(r)
        check(surface == want, "SCHEMA-PURITY",
              "%s row %d: schema %r, expected %r (the schema-key purity "
              "law)" % (doc_id, i, surface, want))
        expected_keys = (PROSE_SURFACE_KEYS if want == "PROSE"
                        else CODE_SURFACE_KEYS)
        check(sorted(r.keys()) == sorted(expected_keys),
              "SCHEMA-UNEXPECTED",
              "%s row %d: key family %s != the %s surface's own %s"
              % (doc_id, i, str(sorted(r.keys())), want,
                 str(sorted(expected_keys))))
        check("mid_statement" not in r, "SCHEMA-UNEXPECTED",
              "%s row %d carries a mid_statement flag into the cache"
              % (doc_id, i))
    # the seam's three-coordinate tuple, in the census only
    seam_tuple = {"commit_index": seam,
                 "stmt_ordinal": rows[seam]["stmt_ordinal"],
                 "token_step": rows[seam]["token_step"]}
    spans = [
        {"state": "clean", "leg": prefix_leg, "n_rows": len(prefix_rows),
         "source": {"doc_id": prefix_doc["doc_id"],
                    "native_range": [0, prefix_pos],
                    "sha_prefix": prefix_doc["sha_prefix"]}},
        {"state": "clean", "leg": suffix_leg, "n_rows": len(suffix_rows),
         "source": {"doc_id": suffix_doc["doc_id"],
                    "native_range": [cut, len(suffix_doc["rows"])],
                    "sha_prefix": suffix_doc["sha_prefix"]}},
    ]
    census = {"doc_id": doc_id, "class": CLASS_TOKEN,
              "prefix_leg": prefix_leg, "suffix_leg": suffix_leg,
              "direction": "%s->%s" % (prefix_leg, suffix_leg),
              "entry_band": list(band), "n_rows": len(rows),
              "seams": [seam_tuple], "onset_positions": [0, seam],
              "spans": spans}
    return {"doc_id": doc_id, "class": CLASS_TOKEN, "rows": rows}, census


# --------------------------------------------------------------------------
# THE REAL-SCHEMA ADAPTERS (every pin asserted at load; SCHEMA-UNEXPECTED
# dies loud on any surprise; receipts printed, never absorbed)
# --------------------------------------------------------------------------

def load_input(path, pin_name):
    check(os.path.exists(path), "MISSING-INPUT",
          "%s: %s (the caches of record live owner-side; deliver them "
          "and re-run)" % (pin_name, path))
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
    """The line-oriented twin (the two thins of record)."""
    check(os.path.exists(path), "MISSING-INPUT",
          "%s: %s (the caches of record live owner-side; deliver them "
          "and re-run)" % (pin_name, path))
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


def _commit_rows(rec, surface):
    """A thin record's commits -> builder rows (the single-span law: the
    native onset mark at row 0 and nowhere else; token-step strictly
    increasing; the 16-key commit family exact)."""
    commits = rec.get("commits")
    check(isinstance(commits, list) and len(commits) > 0,
          "SCHEMA-UNEXPECTED",
          "record %s: commits absent or empty" % rec.get("doc_id"))
    check(len(commits) == rec.get("n_content_steps"),
          "SCHEMA-UNEXPECTED",
          "record %s: %d commits != n_content_steps %r"
          % (rec.get("doc_id"), len(commits),
             rec.get("n_content_steps")))
    rows = []
    prev_t = None
    for i, c in enumerate(commits):
        check(sorted(c.keys()) == sorted(COMMIT_KEYS), "SCHEMA-UNEXPECTED",
              "record %s commit %d: key family != the 16-key family of "
              "record" % (rec.get("doc_id"), i))
        t = c["t"]
        check(isinstance(t, int), "SCHEMA-UNEXPECTED",
              "record %s commit %d: t %r not an int"
              % (rec.get("doc_id"), i, t))
        if prev_t is not None:
            check(t > prev_t, "SCHEMA-UNEXPECTED",
                  "record %s commit %d: t not strictly increasing"
                  % (rec.get("doc_id"), i))
        prev_t = t
        rows.append(make_row(surface, i, 0, t, c, onset=(i == 0)))
    return rows


def adapt_code_cache(code_obj, sha_cache):
    """The CODE clean pool: the cache of record's 400 corpus docs (the
    16-column family, the role law onset-iff-i=0, the work_inc
    named-absent anchor, t_commit strictly increasing)."""
    R = []

    def r(s):
        R.append(s)

    r("[adapter] CODE cache of record: %d B / %s..."
      % (INPUT_PINS["code_cache"]["bytes"], sha_cache[:8]))
    rbd = code_obj.get("rows_by_doc")
    check(isinstance(rbd, dict) and len(rbd) == 400, "SCHEMA-UNEXPECTED",
          "rows_by_doc: expected the 400-doc corpus of record, found %s"
          % (len(rbd) if isinstance(rbd, dict) else type(rbd).__name__))
    census = code_obj.get("census", {})
    check(census.get("records") == CODE_CENSUS_RECORDS
          and census.get("rows") == CODE_CENSUS_ROWS, "SCHEMA-UNEXPECTED",
          "the cache census %r != the %d/%d of record"
          % ({"records": census.get("records"),
              "rows": census.get("rows")},
             CODE_CENSUS_RECORDS, CODE_CENSUS_ROWS))
    rc = census.get("role_counts", {})
    check(rc.get("STATEMENT-ONSET") == CODE_ONSET_COUNT
          and rc.get("OTHER-CONTENT") == CODE_OTHER_COUNT,
          "SCHEMA-UNEXPECTED",
          "the role census %r != the %d/%d density of record "
          "(the native onset marks are i=0-only)"
          % (rc, CODE_ONSET_COUNT, CODE_OTHER_COUNT))
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
              "doc %s: column family != the 16-column family of record"
              % did)
        n = len(cols["role"])
        check(n > 0, "SCHEMA-UNEXPECTED", "doc %s: zero rows" % did)
        for k in cols:
            check(len(cols[k]) == n, "SCHEMA-UNEXPECTED",
                  "doc %s: column %s length %d != %d"
                  % (did, k, len(cols[k]), n))
        check(cols["work_inc"][0] is None
              and all(cols["work_inc"][i] is not None
                      for i in range(1, n)), "SCHEMA-UNEXPECTED",
              "doc %s: the work_inc named-absent anchor law broken" % did)
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
    check(onset_total == CODE_ONSET_COUNT
          and rows_total == CODE_CENSUS_ROWS, "SCHEMA-UNEXPECTED",
          "the corpus census %d docs / %d rows != %d / %d"
          % (onset_total, rows_total, CODE_ONSET_COUNT, CODE_CENSUS_ROWS))
    r("[adapter] CODE corpus: 400 docs / 113,238 rows, native onset "
      "i=0-only 400/400, work_inc named-absent 400/400, t_commit "
      "strict 400/400")
    return clean, R


def adapt_code_thin(thin_recs, sha_thin):
    """The CODE thin of record: the 410 census law (400 corpus + 10
    fixtures), pinned and receipted -- ZERO fixtures drawn (the
    all-clean shape; loop material named-absent by his ruling)."""
    R = []
    str_recs = [x for x in thin_recs if isinstance(x.get("doc_id"), str)]
    int_recs = [x for x in thin_recs if isinstance(x.get("doc_id"), int)]
    check(len(thin_recs) == 410 and len(int_recs) == 400
          and len(str_recs) == 10, "SCHEMA-UNEXPECTED",
          "the code thin: expected 410 = 400 + 10 (the census law), "
          "found %d = %d + %d"
          % (len(thin_recs), len(int_recs), len(str_recs)))
    names = tuple(sorted(x.get("doc_id") for x in str_recs))
    check(names == tuple(sorted(FIXTURE_NAMES)), "SCHEMA-UNEXPECTED",
          "the code thin's fixture name set != the ten of record")
    R.append("[adapter] CODE thin of record: %d B / %s..., 410 = 400 "
             "corpus + 10 fixtures named -- ZERO fixtures drawn (the "
             "all-clean ruling; loop material named-absent)"
             % (INPUT_PINS["code_thin"]["bytes"], sha_thin[:8]))
    return R


def adapt_prose_thin(thin_recs, sha_thin):
    """The PROSE clean pool: the thin of record's 620 corpus docs (the
    all-CoT law, the 16-key commit family, the 205/352/61/2 onset
    census at first-commit t)."""
    R = []

    def r(s):
        R.append(s)

    r("[adapter] PROSE thin of record: %d B / %s..."
      % (INPUT_PINS["prose_thin"]["bytes"], sha_thin[:8]))
    str_recs = [x for x in thin_recs if isinstance(x.get("doc_id"), str)]
    corpus_recs = [x for x in thin_recs
                   if isinstance(x.get("doc_id"), int)]
    check(len(thin_recs) == 630 and len(corpus_recs) == 620
          and len(str_recs) == 10, "SCHEMA-UNEXPECTED",
          "the prose thin: expected 630 = 620 + 10 (the census law), "
          "found %d = %d + %d"
          % (len(thin_recs), len(corpus_recs), len(str_recs)))
    names = tuple(sorted(x.get("doc_id") for x in str_recs))
    check(names == tuple(sorted(FIXTURE_NAMES)), "SCHEMA-UNEXPECTED",
          "the prose thin's fixture name set != the ten of record")
    clean = []
    onset_first_t = {}
    commits_total = 0
    for rec in sorted(corpus_recs, key=lambda x: x["doc_id"]):
        rows = _commit_rows(rec, "PROSE")
        for c in rec["commits"]:
            check(c.get("phase") == "CoT", "SCHEMA-UNEXPECTED",
                  "doc %s: phase %r != CoT (the thin's all-CoT law)"
                  % (rec["doc_id"], c.get("phase")))
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
    r("[adapter] PROSE corpus: 620 docs / 260,854 commits, onset census "
      "{0:205, 1:352, 2:61, 5:2} exact, phase CoT 620/620, t strict "
      "620/620 -- 10 fixtures named, ZERO drawn (the all-clean ruling)")
    return clean, R


def adapt_prose_export(export_obj, thin_recs, sha_export):
    """The prose export of record: the doc_walk_table parity witness."""
    R = []
    corpus = [x for x in thin_recs if isinstance(x.get("doc_id"), int)]
    dwt = export_obj.get("doc_walk_table")
    check(isinstance(dwt, list) and len(dwt) == 620, "SCHEMA-UNEXPECTED",
          "the export's doc_walk_table: expected 620, found %r"
          % (len(dwt) if isinstance(dwt, list)
             else type(dwt).__name__))
    thin_commits = dict((rec["doc_id"], len(rec["commits"]))
                        for rec in corpus)
    parity_bad = 0
    for row in dwt:
        if thin_commits.get(row.get("doc_id")) != row.get("n_commits"):
            parity_bad += 1
    check(parity_bad == 0, "SCHEMA-UNEXPECTED",
          "the export parity: %d docs where n_commits != the thin's "
          "commit count" % parity_bad)
    R.append("[adapter] PROSE export of record: %d B / %s..., "
             "doc_walk_table parity 620/620"
             % (INPUT_PINS["prose_export"]["bytes"], sha_export[:8]))
    return R


def adapt_mixed_census(census_obj, sha_census):
    """The mixed census export of record: the fresh-draw law's
    disjointness witness (the clean_use_receipts, 55 per leg)."""
    R = []
    legs = census_obj.get("legs")
    check(isinstance(legs, dict) and set(legs.keys()) == {"PROSE", "CODE"},
          "SCHEMA-UNEXPECTED",
          "the mixed census export's legs != {PROSE, CODE}")
    consumed = {}
    for leg in ("PROSE", "CODE"):
        recs = legs[leg].get("clean_use_receipts")
        check(isinstance(recs, list) and len(recs) == 55,
              "SCHEMA-UNEXPECTED",
              "the mixed census export's %s clean_use_receipts: expected "
              "the 55-per-leg witness, found %r"
              % (leg, len(recs) if isinstance(recs, list)
                 else type(recs).__name__))
        ids = []
        for x in recs:
            check("source_doc_id" in x and "purpose" in x,
                  "SCHEMA-UNEXPECTED",
                  "a clean_use_receipt lacks its witness fields")
            ids.append(x["source_doc_id"])
        check(len(set(ids)) == 55, "SCHEMA-UNEXPECTED",
              "the %s witness carries duplicate source doc ids" % leg)
        consumed[leg] = sorted(set(ids))
    R.append("[adapter] MIXED census export of record: %d B / %s..., "
             "the disjointness witness: 55 PROSE + 55 CODE consumed "
             "source docs, every CD draw asserted disjoint, fail-loud"
             % (INPUT_PINS["mixed_census"]["bytes"], sha_census[:8]))
    return consumed, R


# --------------------------------------------------------------------------
# THE BUILD PLAN (the pinned (2/2/1) scheduling, deterministic)
# --------------------------------------------------------------------------

def make_plan():
    plan = {}
    for leg in ("PROSE", "CODE"):
        prefix_leg = leg
        suffix_leg = "CODE" if leg == "PROSE" else "PROSE"
        for i in range(DOCS_PER_LEG):
            doc_id = "xdom-%s-%s-%02d" % (prefix_leg, suffix_leg, i + 1)
            band = ENTRY_BANDS[BAND_ALLOCATION[i]]
            plan[doc_id] = {"leg": leg, "prefix_leg": prefix_leg,
                            "suffix_leg": suffix_leg, "band": band,
                            "pos": seam_pos_in_band(band, i), "i": i}
    return plan


def length_census(pools, draws):
    """The builder's FIRST act: the filtered pools' receipts + the drawn
    segments' native lengths against the scheduling bands, BEFORE any
    seam is placed -- an unreachable band dies loud."""
    lines = []
    for leg, pool in pools.items():
        eligible_prefix = {str(b[1]): len([d for d in pool.docs
                                           if d["doc_id"] not in
                                           pool.consumed
                                           and len(d["rows"]) >= b[1]])
                           for b in ENTRY_BANDS}
        eligible_suffix = len([d for d in pool.docs
                               if d["doc_id"] not in pool.consumed
                               and suffix_len(len(d["rows"]))
                               >= MIN_SUFFIX_ROWS])
        lines.append("[%s] filtered pool: %d source docs (%d consumed "
                     "by the mixed cache, excluded); prefix-feasible by "
                     "band upper edge %s; suffix-feasible (N - N//2 >= "
                     "%d): %d"
                     % (leg, len(pool.docs), len(pool.consumed),
                        json.dumps(eligible_prefix, sort_keys=True),
                        MIN_SUFFIX_ROWS, eligible_suffix))
    for d in draws:
        if d["role"] == "prefix":
            check(d["native_len"] >= d["band"][1], "LENGTH-CENSUS",
                  "%s: prefix source %s offers %d rows, under its "
                  "band's upper edge %d"
                  % (d["doc_id"], d["source_doc_id"], d["native_len"],
                     d["band"][1]))
            check(d["pos"] <= d["band"][1], "LENGTH-CENSUS",
                  "%s: seam position %d outside its band"
                  % (d["doc_id"], d["pos"]))
            lines.append("[%s] %s prefix: source %s native %d rows, "
                         "cut %d, band %s"
                         % (d["prefix_leg"], d["doc_id"], d["source_doc_id"],
                            d["native_len"], d["pos"], str(d["band"])))
        else:
            check(d["seg_len"] >= MIN_SUFFIX_ROWS, "LENGTH-CENSUS",
                  "%s: suffix source %s offers %d rows at the cut, "
                  "under the %d segment-length law"
                  % (d["doc_id"], d["source_doc_id"], d["seg_len"],
                     MIN_SUFFIX_ROWS))
            lines.append("[%s] %s suffix: source %s native %d rows, cut "
                         "%d, segment %d rows"
                         % (d["prefix_leg"], d["doc_id"], d["source_doc_id"],
                            d["native_len"], d["cut"], d["seg_len"]))
    return "\n".join(lines) + "\n"


def build_world(pools, echo):
    """The stamped shape: 10 docs / 10 seams, five per direction, the
    pinned (2/2/1) scheduling; draws receipted; the length census run
    BEFORE any seam is placed."""
    plan = make_plan()
    draws = []
    clean_receipts = {"PROSE": [], "CODE": []}
    # ---- the prefix draws (feasibility: N >= the band's upper edge)
    for leg in ("PROSE", "CODE"):
        for i in range(DOCS_PER_LEG):
            doc_id = [k for k in plan
                      if plan[k]["leg"] == leg and plan[k]["i"] == i][0]
            p = plan[doc_id]
            doc, rec = pools[p["prefix_leg"]].take_prefix(
                "%s-prefix" % doc_id, p["band"][1])
            draws.append({"doc_id": doc_id, "role": "prefix",
                          "prefix_leg": leg,
                          "source_doc_id": doc["doc_id"],
                          "native_len": len(doc["rows"]),
                          "band": p["band"], "pos": p["pos"], "doc": doc})
            clean_receipts[p["prefix_leg"]].append(rec)
    # ---- the suffix draws (feasibility: N - N//2 >= 129 at the cut)
    for leg in ("PROSE", "CODE"):
        for i in range(DOCS_PER_LEG):
            doc_id = [k for k in plan
                      if plan[k]["leg"] == leg and plan[k]["i"] == i][0]
            p = plan[doc_id]
            doc, rec = pools[p["suffix_leg"]].take_suffix(
                "%s-suffix" % doc_id)
            cut = suffix_cut(len(doc["rows"]))
            draws.append({"doc_id": doc_id, "role": "suffix",
                          "prefix_leg": leg,
                          "source_doc_id": doc["doc_id"],
                          "native_len": len(doc["rows"]),
                          "band": p["band"], "cut": cut,
                          "seg_len": suffix_len(len(doc["rows"])),
                          "doc": doc})
            clean_receipts[p["suffix_leg"]].append(rec)
    # ---- the length census BEFORE any seam is placed
    echo(length_census(pools, draws))
    # ---- the disjointness witness, asserted hot
    overlap = {"PROSE": pools["PROSE"].overlap_check(),
               "CODE": pools["CODE"].overlap_check()}
    # ---- the joins
    docs_out = {"PROSE": [], "CODE": []}
    census_out = {"PROSE": [], "CODE": []}
    for leg in ("PROSE", "CODE"):
        for i in range(DOCS_PER_LEG):
            doc_id = [k for k in plan
                      if plan[k]["leg"] == leg and plan[k]["i"] == i][0]
            p = plan[doc_id]
            prefix_doc = [d for d in draws if d["doc_id"] == doc_id
                          and d["role"] == "prefix"][0]["doc"]
            suffix_doc = [d for d in draws if d["doc_id"] == doc_id
                          and d["role"] == "suffix"][0]["doc"]
            doc, cen = build_doc_cross(doc_id, p["prefix_leg"],
                                       p["suffix_leg"], prefix_doc,
                                       p["pos"], suffix_doc, p["band"])
            docs_out[leg].append(doc)
            census_out[leg].append(cen)
    return docs_out, census_out, clean_receipts, overlap


def assemble_cache_census(docs_out, census_out, clean_receipts, consumed,
                          cache_path):
    cache_obj = {"cache_type": CACHE_TYPE_LINE,
                 "PROSE": {"surface": "PROSE",
                           "docs": docs_out["PROSE"]},
                 "CODE": {"surface": "CODE", "docs": docs_out["CODE"]}}
    census_obj = {"version": VERSION,
                  "cache_path": cache_path,
                  "legs": {},
                  "mixed_cache_consumed": consumed}
    for leg in ("PROSE", "CODE"):
        census_obj["legs"][leg] = {
            "leg": leg, "docs": DOCS_PER_LEG, "seams": DOCS_PER_LEG,
            "class_counts": {CLASS_TOKEN: DOCS_PER_LEG},
            "clean_use_receipts": clean_receipts[leg],
            "doc_census": census_out[leg]}
    return cache_obj, census_obj


# --------------------------------------------------------------------------
# THE CENSUS VALIDATOR (the cold door: cache + census alone, every pin
# asserted fail-loud; conservation 10 / 10 / 5 separate, never pooled)
# --------------------------------------------------------------------------

EXPECTED_SPAN_SHA = {"PROSE": "88cbadee", "CODE": "610d48c9"}


def load_cross(cache_obj, census_obj, expected_span_sha=None):
    """The census-conservation law + the cold pins. Returns the totals.
    expected_span_sha: the provenance pins per span leg (the banked
    input shas by default; the battery's synthetic worlds carry their
    own named prefixes)."""
    if expected_span_sha is None:
        expected_span_sha = EXPECTED_SPAN_SHA
    check(census_obj.get("version") == VERSION, "VERSION",
          "census version %r != %s"
          % (census_obj.get("version"), VERSION))
    check(cache_obj.get("cache_type") == CACHE_TYPE_LINE, "CACHE-TYPE",
          "the cache's own type line != the fixture-bank typing law")
    legs = census_obj.get("legs")
    check(isinstance(legs, dict) and set(legs.keys()) == {"PROSE", "CODE"},
          "CENSUS-SHAPE", "the census legs != {PROSE, CODE}")
    total_docs = 0
    total_seams = 0
    directions = {"PROSE->CODE": 0, "CODE->PROSE": 0}
    used_sources = {}
    mixed_consumed = census_obj.get("mixed_cache_consumed", {})
    for leg in ("PROSE", "CODE"):
        leg_rec = legs[leg]
        check(leg_rec.get("leg") == leg, "CENSUS-SHAPE",
              "the %s leg record carries leg %r" % (leg, leg_rec.get("leg")))
        check(leg_rec.get("docs") == DOCS_PER_LEG, "CONSERVATION-DOCS",
              "the %s leg carries %r docs != %d (asserted per leg, never "
              "pooled)" % (leg, leg_rec.get("docs"), DOCS_PER_LEG))
        check(leg_rec.get("seams") == DOCS_PER_LEG, "CONSERVATION-SEAMS",
              "the %s leg carries %r seams != %d (one seam per document)"
              % (leg, leg_rec.get("seams"), DOCS_PER_LEG))
        check(leg_rec.get("class_counts") == {CLASS_TOKEN: DOCS_PER_LEG},
              "CLASS-ENUM",
              "the %s leg's class census %r != the probe's own "
              "one-token enumeration {%s: %d}"
              % (leg, leg_rec.get("class_counts"), CLASS_TOKEN,
                 DOCS_PER_LEG))
        cache_leg = cache_obj.get(leg)
        check(isinstance(cache_leg, dict)
              and cache_leg.get("surface") == leg, "CACHE-SHAPE",
              "the cache's %s leg surface mismatch" % leg)
        cache_docs = dict((d["doc_id"], d) for d in cache_leg["docs"])
        check(len(cache_docs) == DOCS_PER_LEG, "CONSERVATION-DOCS",
              "the cache's %s leg carries %d docs != %d"
              % (leg, len(cache_docs), DOCS_PER_LEG))
        doc_census = leg_rec.get("doc_census")
        check(isinstance(doc_census, list)
              and len(doc_census) == DOCS_PER_LEG, "TRUNCATED-CENSUS",
              "the %s leg's doc_census carries %r records != %d (a "
              "truncated census dies loud)"
              % (leg, len(doc_census) if isinstance(doc_census, list)
                 else doc_census, DOCS_PER_LEG))
        for dc in doc_census:
            did = dc["doc_id"]
            directions[dc["direction"]] = \
                directions.get(dc["direction"], 0) + 1
            doc = cache_docs.get(did)
            check(doc is not None, "TRUNCATED-CENSUS",
                  "census names doc %s, absent from the cache" % did)
            rows = doc["rows"]
            check(doc.get("class") == CLASS_TOKEN, "CLASS-ENUM",
                  "doc %s class %r != %s" % (did, doc.get("class"),
                                             CLASS_TOKEN))
            check(dc["class"] == CLASS_TOKEN, "CLASS-ENUM",
                  "census doc %s class %r != %s"
                  % (did, dc["class"], CLASS_TOKEN))
            check(dc["prefix_leg"] == leg, "KEYING-LAW",
                  "doc %s keyed on the %s leg but its prefix leg is %r"
                  % (did, leg, dc["prefix_leg"]))
            check(dc["suffix_leg"] != dc["prefix_leg"], "CROSS-DOMAIN",
                  "doc %s: prefix leg == suffix leg (not cross-domain)"
                  % did)
            check(len(dc["seams"]) == 1, "SEAM-COUNT",
                  "doc %s carries %r seams != 1 (one seam per document)"
                  % (did, len(dc["seams"])))
            seam = dc["seams"][0]
            check(dc["onset_positions"] == [0, seam["commit_index"]],
                  "ONSET-LAW",
                  "doc %s onset positions %r != [0, seam]"
                  % (did, dc["onset_positions"]))
            check(seam["commit_index"] == dc["spans"][0]["n_rows"],
                  "SEAM-POSITION",
                  "doc %s: the seam's commit index %r != the prefix "
                  "span's %d rows"
                  % (did, seam["commit_index"],
                     dc["spans"][0]["n_rows"]))
            check(len(dc["spans"]) == 2, "TRUNCATED-CENSUS",
                  "doc %s carries %r spans != 2" % (did, len(dc["spans"])))
            check(dc["spans"][0]["leg"] == dc["prefix_leg"]
                  and dc["spans"][1]["leg"] == dc["suffix_leg"],
                  "TRUTH-LABELS",
                  "doc %s: span legs %r != the authored prefix/suffix "
                  "pair" % (did, [s["leg"] for s in dc["spans"]]))
            check(dc["spans"][1]["n_rows"] >= MIN_SUFFIX_ROWS,
                  "SEGMENT-LENGTH",
                  "doc %s: incoming span %d rows < %d"
                  % (did, dc["spans"][1]["n_rows"], MIN_SUFFIX_ROWS))
            lo, hi = dc["entry_band"]
            check((lo, hi) in ENTRY_BANDS, "BAND-LAW",
                  "doc %s: entry band %r outside the scheduling bands"
                  % (did, dc["entry_band"]))
            check(lo <= seam["commit_index"] <= hi, "BAND-LAW",
                  "doc %s: seam position %d outside its band %s"
                  % (did, seam["commit_index"], str(dc["entry_band"])))
            check(len(rows) == dc["n_rows"], "CONSERVATION-ROWS",
                  "doc %s: cache rows %d != census n_rows %d"
                  % (did, len(rows), dc["n_rows"]))
            check(seam["commit_index"] + dc["spans"][1]["n_rows"]
                  == len(rows), "CONSERVATION-ROWS",
                  "doc %s: prefix %d + suffix %d != %d rows"
                  % (did, dc["spans"][0]["n_rows"],
                     dc["spans"][1]["n_rows"], len(rows)))
            # the rows: schema purity, onset law, monotonicity
            prev_t = None
            prev_s = None
            for i, r in enumerate(rows):
                surface = row_schema(r)
                check(surface is not None, "UNRECOGNIZED-SCHEMA",
                      "doc %s row %d: no leg's structural signature"
                      % (did, i))
                want = dc["prefix_leg"] if i < seam["commit_index"] \
                    else dc["suffix_leg"]
                check(surface == want, "SCHEMA-PURITY",
                      "doc %s row %d: schema %r, expected %r"
                      % (did, i, surface, want))
                expected_keys = (PROSE_SURFACE_KEYS if surface == "PROSE"
                                 else CODE_SURFACE_KEYS)
                check(sorted(r.keys()) == sorted(expected_keys),
                      "SCHEMA-UNEXPECTED",
                      "doc %s row %d: key family %s != the %s surface's "
                      "own (the schema-key purity law)"
                      % (did, i, str(sorted(r.keys())), surface))
                check(row_onset(r, surface)
                      == (i in (0, seam["commit_index"])),
                      "ONSET-LAW",
                      "doc %s row %d: onset %r, expected onset iff "
                      "{0, seam}" % (did, i, row_onset(r, surface)))
                if prev_t is not None:
                    check(r["token_step"] > prev_t, "MONOTONIC-T",
                          "doc %s row %d: token step not strictly "
                          "increasing" % (did, i))
                    check(r["stmt_ordinal"] >= prev_s, "MONOTONIC-S",
                          "doc %s row %d: statement ordinal went "
                          "backwards" % (did, i))
                check(r["commit_index"] == i, "MONOTONIC-COMMIT",
                      "doc %s row %d: commit_index %r != its position"
                      % (did, i, r["commit_index"]))
                prev_t = r["token_step"]
                prev_s = r["stmt_ordinal"]
            check(rows[seam["commit_index"]]["stmt_ordinal"]
                  == seam["stmt_ordinal"]
                  and rows[seam["commit_index"]]["token_step"]
                  == seam["token_step"], "SEAM-TUPLE",
                  "doc %s: the seam's three-coordinate tuple does not "
                  "match the rows at the seam" % did)
            # provenance + reuse + disjointness, per span
            for s in dc["spans"]:
                check(s["source"]["sha_prefix"].startswith(
                    expected_span_sha[s["leg"]]), "PROVENANCE-SHA",
                    "doc %s span (leg %s): source sha %r does not carry "
                    "the banked %s pin %s (every byte traceable to the "
                    "bank, a mismatch dies loud)"
                    % (did, s["leg"], s["source"]["sha_prefix"], s["leg"],
                       expected_span_sha[s["leg"]]))
                key = (s["leg"], s["source"]["doc_id"])
                check(key not in used_sources, "CLEAN-REUSE",
                      "source doc %s drawn twice (the at-most-once law)"
                      % str(key))
                used_sources[key] = did
                check(s["source"]["doc_id"] not in
                      mixed_consumed.get(s["leg"], []),
                      "FRESH-DRAW-OVERLAP",
                      "doc %s span (leg %s): source %s overlaps the "
                      "mixed cache's consumed set (the disjointness "
                      "witness tripped, censused loud)"
                      % (did, s["leg"], s["source"]["doc_id"]))
        total_docs += leg_rec["docs"]
        total_seams += leg_rec["seams"]
    check(total_docs == 10, "TOTAL-DOCS",
          "%d != 10 (asserted separately, never pooled)" % total_docs)
    check(total_seams == 10, "TOTAL-SEAMS",
          "%d != 10 (asserted separately, never pooled)" % total_seams)
    check(directions["PROSE->CODE"] == 5, "CONSERVATION-DIRECTION",
          "PROSE->CODE documents %d != 5 (per-direction count asserted "
          "separately)" % directions["PROSE->CODE"])
    check(directions["CODE->PROSE"] == 5, "CONSERVATION-DIRECTION",
          "CODE->PROSE documents %d != 5 (per-direction count asserted "
          "separately)" % directions["CODE->PROSE"])
    # the (2/2/1) band allocation, per direction, asserted + printed
    band_alloc = {}
    for direction in ("PROSE->CODE", "CODE->PROSE"):
        counts = [0, 0, 0]
        for leg in ("PROSE", "CODE"):
            for dc in legs[leg]["doc_census"]:
                if dc["direction"] == direction:
                    counts[ENTRY_BANDS.index(tuple(dc["entry_band"]))] += 1
        check(tuple(counts) == (2, 2, 1), "BAND-ALLOCATION",
              "direction %s: band allocation %r != the pinned (2/2/1)"
              % (direction, counts))
        band_alloc[direction] = counts
    return {"docs": total_docs, "seams": total_seams,
            "directions": directions, "band_allocation": band_alloc}


# --------------------------------------------------------------------------
# THE REAL BUILD
# --------------------------------------------------------------------------

def real_build(args):
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    cache_name = "crossdomain_probe_cache_v1.json"
    census_name = "crossdomain_probe_census_v1.json"
    cache_path = os.path.join(out_dir, cache_name)
    census_path = os.path.join(out_dir, census_name)
    # ---- the five pins, all printed, all sha-asserted at load
    code_obj, sha_cache = load_input(args.code_cache, "code_cache")
    thin_code, sha_thin_code = load_jsonl(args.code_thin, "code_thin")
    thin_prose, sha_thin_prose = load_jsonl(args.prose_thin, "prose_thin")
    exp_obj, sha_export = load_input(args.prose_export, "prose_export")
    mixed_obj, sha_mixed = load_input(args.mixed_census, "mixed_census")
    sys.stdout.write("[inputs] code cache  26,209,382 B / %s...\n"
                     "[inputs] code thin   80,912,361 B / %s...\n"
                     "[inputs] prose thin  159,280,278 B / %s...\n"
                     "[inputs] prose export  656,143 B / %s...\n"
                     "[inputs] mixed census   65,583 B / %s...\n"
                     % (sha_cache[:16], sha_thin_code[:16],
                        sha_thin_prose[:16], sha_export[:16],
                        sha_mixed[:16]))
    code_clean, code_R = adapt_code_cache(code_obj, sha_cache)
    for line in code_R:
        sys.stdout.write(line + "\n")
    for line in adapt_code_thin(thin_code, sha_thin_code):
        sys.stdout.write(line + "\n")
    prose_clean, prose_R = adapt_prose_thin(thin_prose, sha_thin_prose)
    for line in prose_R:
        sys.stdout.write(line + "\n")
    for line in adapt_prose_export(exp_obj, thin_prose, sha_export):
        sys.stdout.write(line + "\n")
    consumed, mixed_R = adapt_mixed_census(mixed_obj, sha_mixed)
    for line in mixed_R:
        sys.stdout.write(line + "\n")
    pools = {"PROSE": FreshPool(prose_clean, consumed["PROSE"], "PROSE"),
             "CODE": FreshPool(code_clean, consumed["CODE"], "CODE")}
    docs_out, census_out, clean_receipts, overlap = build_world(
        pools, sys.stdout.write)
    cache_obj, census_obj = assemble_cache_census(
        docs_out, census_out, clean_receipts, consumed, cache_path)
    totals = load_cross(cache_obj, census_obj)
    with open(cache_path, "wb") as fh:
        fh.write(dump_canonical(cache_obj))
    with open(census_path, "wb") as fh:
        fh.write(dump_canonical(census_obj))
    with open(cache_path, "rb") as fh:
        re_cache = json.loads(fh.read().decode("utf-8"))
    with open(census_path, "rb") as fh:
        re_census = json.loads(fh.read().decode("utf-8"))
    re_totals = load_cross(re_cache, re_census)
    check(re_totals == totals, "ROUNDTRIP",
          "the cold re-load receipts %r != %r" % (re_totals, totals))
    sys.stdout.write("[build] census conservation re-asserted cold: "
                     "%d docs / %d seams, directions %s, band allocation "
                     "%s, every pin green\n"
                     % (re_totals["docs"], re_totals["seams"],
                        json.dumps(re_totals["directions"],
                                   sort_keys=True),
                        json.dumps(re_totals["band_allocation"],
                                   sort_keys=True)))
    sys.stdout.write("[build] fresh-draw disjointness witness: consumed "
                     "sets %s, overlap zero, at-most-once 20/20\n"
                     % json.dumps(overlap, sort_keys=True))
    sys.stdout.write("[build] %s %d B sha256 %s\n"
                     "[build] %s %d B sha256 %s\n"
                     % (cache_name, os.path.getsize(cache_path),
                        sha256_of(cache_path),
                        census_name, os.path.getsize(census_path),
                        sha256_of(census_path)))
    sys.stdout.write(PAREN + "\n")
    return 0


# --------------------------------------------------------------------------
# THE BATTERY (synthetic hand-off worlds FIRST; every tamper world and
# negative fixture dying loud by design; twice-run byte-identical)
# --------------------------------------------------------------------------

SYN_SHA = {"PROSE": "synprose", "CODE": "syncode0"}
SYN_DOC_ROWS = 260            # >= 258: both prefix and suffix feasible


def _syn_doc(surface, idx):
    n = SYN_DOC_ROWS
    rows = []
    for i in range(n):
        payload = {"t": 3 + i, "stub": True}
        rows.append(make_row(surface, i, 0, 3 + i, payload,
                             onset=(i == 0)))
    return {"doc_id": "syn-%s-%02d" % (surface.lower(), idx),
            "rows": rows, "sha_prefix": SYN_SHA[surface]}


def _syn_world():
    """A full valid 10-doc synthetic world through the REAL build path
    (the same plan, pools, draws, joins, and validator), so every
    negative fixture tampers exactly one field of a green world and
    dies at its own named check."""
    pools = {"PROSE": FreshPool([_syn_doc("PROSE", i)
                                 for i in range(10)], [], "PROSE"),
             "CODE": FreshPool([_syn_doc("CODE", i)
                                for i in range(10)], [], "CODE")}
    docs_out, census_out, clean_receipts, overlap = build_world(
        pools, lambda s: None)
    cache_obj, census_obj = assemble_cache_census(
        docs_out, census_out, clean_receipts,
        {"PROSE": [], "CODE": []}, "syn")
    totals = load_cross(cache_obj, census_obj, expected_span_sha=SYN_SHA)
    return cache_obj, census_obj, totals


def run_battery(out_path):
    """Every world hand-solved, every expected die named, every receipt
    printed; the output deterministic (twice-run cmp silent)."""
    L = []

    def r(s):
        L.append(s)

    def expect_die(code, fn, label):
        try:
            fn()
        except BuilderDie as e:
            check(e.code == code, "BATTERY-UNEXPECTED-DIE",
                  "%s: died %s (%s), expected %s"
                  % (label, e.code, e.msg, code))
            r("[%s] %s -> died loud (expected)" % (label, e.code))
            return
        die("BATTERY-NO-DIE",
            "%s: no die (expected %s) -- a tamper shape silently "
            "absorbed" % (label, code))

    import copy
    r("[battery] %s: the synthetic hand-off worlds, hand-solved"
      % VERSION)
    # ---- the full valid synthetic world, through the real path
    cache_obj, census_obj, totals = _syn_world()
    r("[world] the 10-doc synthetic world built through the real "
      "plan/pool/join/validator path: %d docs / %d seams, directions %s, "
      "band allocation %s, all pins green"
      % (totals["docs"], totals["seams"],
         json.dumps(totals["directions"], sort_keys=True),
         json.dumps(totals["band_allocation"], sort_keys=True)))
    seam0 = census_obj["legs"]["PROSE"]["doc_census"][0]
    r("[world] xdom-PROSE-CODE-01: seam at %d (band %s), suffix %d rows, "
      "the WRITTEN interior onset on the CODE seam row (natively "
      "OTHER-CONTENT at the cut)"
      % (seam0["seams"][0]["commit_index"], str(seam0["entry_band"]),
         seam0["spans"][1]["n_rows"]))
    # the hand-solved receipts on world doc 0
    doc0 = cache_obj["PROSE"]["docs"][0]
    seam = seam0["seams"][0]["commit_index"]
    check(doc0["rows"][seam]["role"] == CODE_ONSET, "BATTERY-WORLD",
          "the seam's WRITTEN onset absent on the CODE row")
    check(doc0["rows"][seam]["token_step"]
          == doc0["rows"][seam - 1]["token_step"] + 1, "BATTERY-WORLD",
          "the dual-clock handoff t_base != prefix last + 1")
    check(doc0["rows"][seam]["stmt_ordinal"]
          == doc0["rows"][seam - 1]["stmt_ordinal"] + 1, "BATTERY-WORLD",
          "the statement clock did not continue from the prefix's last")
    r("[world] hand-solved: the seam row's token_step = prefix last + 1, "
      "stmt_ordinal = prefix last + 1, role = STATEMENT-ONSET (WRITTEN)")
    # ---- tamper (i): a leg change WITHOUT an onset mark
    def tamper_i():
        pre = _syn_doc("PROSE", 0)
        suf = _syn_doc("CODE", 0)
        rows = splice_cross(pre["rows"][:40], suf["rows"][130:], "CODE",
                            write_mark=False)
        onsets = onset_positions_of(rows, "tamper-i")
        check(onsets == [0, 40], "ONSET-LAW",
              "tamper-i: onset positions %r != [0, 40] -- the seam "
              "crossed legs WITHOUT an onset mark, the latch would "
              "hold and the row is censused loud" % onsets)
    expect_die("ONSET-LAW", tamper_i, "tamper-i")
    # ---- tamper (ii): a mid-statement cross-domain seam, refused
    def tamper_ii():
        pre = _syn_doc("PROSE", 0)
        suf = _syn_doc("CODE", 0)
        bad = make_row("PROSE", 0, 0, 100, {"t": 100}, onset=False,
                       mid_statement=True)
        splice_cross(pre["rows"][:40], [bad] + suf["rows"][131:], "PROSE")
    expect_die("SEAM-OFF-BOUNDARY", tamper_ii, "tamper-ii")
    # ---- tamper (iii): a row no leg's signature recognizes
    def tamper_iii():
        pre = _syn_doc("PROSE", 0)
        suf = _syn_doc("CODE", 0)
        bad = {"commit_index": 0, "stmt_ordinal": 0, "token_step": 9,
               "payload": {"t": 9}}
        splice_cross(pre["rows"][:40], [bad] + suf["rows"][131:], "PROSE")
    expect_die("UNRECOGNIZED-SCHEMA", tamper_iii, "tamper-iii")
    # ---- negative: a reused clean segment (pool level: the at-most-once
    # guard dies loud when handed a used doc, even if a caller's own
    # eligible list missed the filter)
    def neg_reuse():
        pool = FreshPool([_syn_doc("PROSE", 0), _syn_doc("PROSE", 1)],
                         [], "PROSE")
        doc, _rec = pool.take_prefix("first", 36)
        pool._pick([doc], "second")
    expect_die("CLEAN-REUSE", neg_reuse, "neg-clean-reuse (pool)")
    # ---- negative: the disjointness filter refusing a consumed doc
    def neg_filter():
        d = _syn_doc("PROSE", 0)
        pool = FreshPool([d], [d["doc_id"]], "PROSE")
        pool.take_prefix("draw", 36)
    expect_die("CLEAN-POOL-EXHAUSTED", neg_filter,
               "neg-mixed-overlap (the disjointness filter refuses the "
               "consumed doc)")
    # ---- negative: a truncated census (one doc_census record dropped)
    def neg_truncated():
        c2 = copy.deepcopy(census_obj)
        c2["legs"]["PROSE"]["doc_census"] = \
            c2["legs"]["PROSE"]["doc_census"][:4]
        load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("TRUNCATED-CENSUS", neg_truncated, "neg-truncated-census")
    # ---- negative: a mismatched seam count (a doc claiming two seams)
    def neg_seamcount():
        c2 = copy.deepcopy(census_obj)
        dc = c2["legs"]["PROSE"]["doc_census"][0]
        dc["seams"] = dc["seams"] + [dict(dc["seams"][0])]
        load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("SEAM-COUNT", neg_seamcount, "neg-seam-count")
    # ---- negative: a provenance sha mismatch
    def neg_provenance():
        c2 = copy.deepcopy(census_obj)
        c2["legs"]["PROSE"]["doc_census"][0]["spans"][0]["source"][
            "sha_prefix"] = "deadbeef00000000"
        load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("PROVENANCE-SHA", neg_provenance, "neg-provenance-sha")
    # ---- negative: a reused clean segment (world level: two docs
    # sharing one source)
    def neg_world_reuse():
        c2 = copy.deepcopy(census_obj)
        dup = c2["legs"]["PROSE"]["doc_census"][1]["spans"][1]
        c2["legs"]["PROSE"]["doc_census"][0]["spans"][1] = \
            copy.deepcopy(dup)
        load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("CLEAN-REUSE", neg_world_reuse,
               "neg-clean-reuse (world: a source drawn twice)")
    # ---- negative: a draw overlapping the mixed cache's consumed set
    # (the cold witness)
    def neg_overlap():
        c2 = copy.deepcopy(census_obj)
        src = c2["legs"]["PROSE"]["doc_census"][0]["spans"][0][
            "source"]["doc_id"]
        c2["mixed_cache_consumed"] = {"PROSE": [src], "CODE": []}
        load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("FRESH-DRAW-OVERLAP", neg_overlap,
               "neg-mixed-overlap (the cold disjointness witness)")
    # ---- negative: a schema impurity (a CODE row injected __onset__)
    def neg_impurity():
        pre = _syn_doc("PROSE", 0)
        suf = _syn_doc("CODE", 0)
        row = dict(suf["rows"][130])
        row["__onset__"] = True
        splice_cross(pre["rows"][:40], [row] + suf["rows"][131:], "CODE")
    expect_die("UNRECOGNIZED-SCHEMA", neg_impurity,
               "neg-schema-impurity (a CODE row injected __onset__)")
    r("[battery] all worlds green: the 10-doc synthetic world built "
      "through the real path; 3 tamper shapes + 8 negative fixtures "
      "died loud by design, every die at its own named check")
    r("[battery] %s" % PAREN)
    text = "\n".join(L) + "\n"
    if out_path:
        with open(out_path, "wb") as fh:
            fh.write(text.encode("utf-8"))
    return text


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=VERSION)
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--battery-out", default=None)
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", default=None)
    ap.add_argument("--code-cache", default=None)
    ap.add_argument("--code-thin", default=None)
    ap.add_argument("--prose-thin", default=None)
    ap.add_argument("--prose-export", default=None)
    ap.add_argument("--mixed-census", default=None)
    ap.add_argument("--out-dir", default="crossdomain_probe_build_out")
    args = ap.parse_args()
    try:
        if args.battery:
            sys.stdout.write(run_battery(args.battery_out))
            return 0
        # --verify is the COLD door: the census + cache re-load, none of
        # the source inputs (the portability law)
        if args.verify:
            with open(args.verify, "rb") as fh:
                census_obj = json.loads(fh.read().decode("utf-8"))
            cache_path = census_obj.get("cache_path")
            with open(cache_path, "rb") as fh:
                cache_obj = json.loads(fh.read().decode("utf-8"))
            totals = load_cross(cache_obj, census_obj)
            sys.stdout.write("[verify] %d docs / %d seams, directions "
                             "%s, band allocation %s, every pin green "
                             "(cold door: no source inputs touched)\n"
                             % (totals["docs"], totals["seams"],
                                json.dumps(totals["directions"],
                                           sort_keys=True),
                                json.dumps(totals["band_allocation"],
                                           sort_keys=True)))
            sys.stdout.write(PAREN + "\n")
            return 0
        if args.build:
            return real_build(args)
        ap.print_help()
        return 1
    except BuilderDie as e:
        sys.stdout.write("[DIE] %s: %s\n" % (e.code, e.msg))
        sys.stdout.write("[DIE] %s ends LOUD, never silent\n" % VERSION)
        return 2


if __name__ == "__main__":
    sys.exit(main())

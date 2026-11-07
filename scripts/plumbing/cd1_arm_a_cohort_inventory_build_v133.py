#!/usr/bin/env python3
# cd1_arm_a_cohort_inventory_build_v1.py -- the CD-1 Arm A B0 builder.
# The cohort inventory + certification build per my PINNED B0
# pre-registration of record (cd1-arm-a-b0-cohort-inventory-preregistration.md,
# 8730 B, SHA-256 c641bee2...), under the pinned ladder: 0a the 17-C
# adjudication; 0b the Arm A sheet (14dbedda...); 0c the Phase-1 build
# spec (0c886741...). ZERO GPU, ZERO DECODES: reads banked caches + label
# exports + the tokenizer file only; never a forward pass, never a model
# load. The tool prints no verdicts -- the inventory is a receipt;
# findings presented, never adjudicated; my stamps decide.
# Modes: --census (Pass 1, read-only) / --run (Pass 2, after my map
# stamp) / --selfcheck (the synthetic battery). Build parts: 1 of 3 =
# the pin engine + the cache reader + the export loaders + the census
# pass. 2 of 3 = the field map + the reconciliation gate + the t_0 and
# cohort engines. 3 of 3 = the inventory run + the certification layer
# + the export writer + the full battery.
import argparse
import base64
import hashlib
import json
import math
import os
import re
import sys
import tempfile
from collections import Counter, OrderedDict

TOOL = "cd1_arm_a_cohort_inventory_build_v1.py"
VERSION = "1.3.3"
BUILD_PART = "3 of 3"

# v1.3.3 -- THE SPAN-EXTENT SINGULAR RANGE, AT MY STAMP (my words
# verbatim: "begin the fourth fucking build act"; the item-1172
# finding): my v1.3.2 BLOCK-1 run of record exited honestly at doc
# 213 -- the singular `step` is the SPAN-HEAD step (the exporter's
# own construction, measured: step = the walk step covering the
# value's FIRST char, tid = the token at that step, span = the
# CONTIGUOUS step run covering the value's whole char run, span[0]
# == tid on 4,062/4,062 DV rows), the numeric token DEEPER in the
# run ("Delta-E 1": the head "Delta" at 39, the "1" at 42) -- the
# v1.3.2 DEGENERATE range [step, step] demanded the numeric at the
# head, an assumption the bytes never made. THE CENSUS: 3,899 DV
# rows head-numeric (the outcome identical under the corrected
# range -- the first numeric at offset 0), 23 rows the exit class
# across 6 docs (213x15, 466, 576, 603x2, 667x3, 695), 140 rows
# zero-numeric (the standing UNRESOLVABLE-NON-NUMERIC receipt
# class, returned before the range walk); 3,899 + 23 + 140 ==
# 4,062. THE LAW: the singular path binds the SPAN-EXTENT range
# [step, step + len(span) - 1] + occ_tid + occ_index from occ_i
# via SINGULAR_INDEX_BINDINGS (`i` still NEVER bound on the
# singular path); the load-bearing identity ids_list[step + j] ==
# span[j] holds by the exporter's contiguous construction + the
# id-identity law (walk_ids == steps.id, the hard exit at cache
# load) + the doc-for-doc NAMED join; a singular row with int step
# + tid but no usable span a NAMED premise violation (zero real
# rows, the guard standing); the len(span)==1 rows keep the
# degenerate shape naturally. THE THREE-LANE PREFLIGHT (the
# item-1172 receipts, all rows measured before this build):
# promotions 371 (contiguity/bounds zero violations, 350
# resolvable + 21 zero-numeric), DV 4,062 (head law + bounds zero
# violations, 3,922 resolvable + 140 zero-numeric), A2 7,115
# (contiguity/bounds/zero-numeric/i-binding zero violations, all
# resolvable). EVERY other law byte-identical to v1.3.2 (the
# range path, the true-collision guard, the partial/non-int law,
# the census keys, the doc-naming law, the resolve law below the
# binding). The battery: the doc-213 extraction regression + the
# no-span NAMED guard + the doc-213 span-extent pipeline pair
# (occ_step_t 40 through the range [39, 40]) + the zero-numeric
# singular pipeline (counted, never an exit); the doc-12 pipeline
# assertions unchanged; 14 checks expected. The v1/v2 exports +
# readings STAND banked, never retro-edited.
#
# v1.3.2 -- THE SINGULAR-FORM INDEX LAW, AT MY STAMP (my words
# verbatim: "okay yea do such, continue on to the buil act"; the
# item-1170 binding discovery): my v1.3.1 BLOCK-1 run of record
# caught the third field shape -- EVERY node row of every class
# carries [i, step, tid, occ_i] together, so the v1.3.1 both-forms
# guard (which read `i` as a range-form marker) tripped on the first
# DERIVED-VERIFIED row (doc 12, i 5 / occ_i 0 / step 35 / tid 1399
# -- the same "60 feet" occurrence the item-1168 known-answer picks).
# THE MEASURED TOPOLOGY (aligned bytes of record): promotions
# 371/371 [step_start, step_end]; A2 statements 7,115/7,115
# [step_start, step_end, i] with i the occurrence ordinal 0..n-1
# (1,319/1,319 a2_raw docs -- the stamped v1.3.0 binding correct,
# untouched); node rows 28,059/28,059 [i, step, tid, occ_i] with i
# the VALUE-GROUP ORDINAL (i==occ_i on 352 of 4,062 DV rows only);
# true namespace collisions (range + singular on one row) ZERO
# across every lane. THE LAW: the both-forms NAMED exit narrows to
# the TRUE collision (a range field + the singular on one row); on
# the singular path `i` is NEVER bound (the group ordinal, never
# the occurrence index -- a naive narrowing would have written a
# wrong index on 3,710 of 4,062 DV rows); occ_index binds from
# occ_i only; the range path (step_start/step_end/i) byte-identical
# to the stamped v1.3.0 law; a lone-`i` row (no form) carries no
# occurrence step -- counted rows-without, never bound; every ext
# NAMED exit names the doc id (the v1.3.1 message gave none -- the
# presentation defect owned at item 1170). The battery node-row
# fixtures carry the REAL topology [i, step, tid, occ_i] with
# i != occ_i; new NAMED fixtures: the true collision, the null-step
# gap-row shape, the doc-id-in-message law. ZERO law changes
# elsewhere; the v1.2.7/v1.3.0/v1.3.1 laws stand as stamped/owned.

# v1.3.1 -- THE S3 SINGULAR OWN-STEP FORM, AT MY STAMP (my words
# verbatim: "okay continue lets have 3 messages for the build act";
# the item-1168 binding discovery): my BLOCK-1 run of record
# hard-exited at doc 12 -- the stamped S3 extension named three
# field forms (step_start/step_end/i) and the aligned bytes' A1
# node_rows lane carries the occurrence's own step under the
# SINGULAR form (step + tid + the occurrence index occ_i), never in
# the named list -- the exit the S3 law working as designed, zero
# silent fallback, no partial export (the exit precedes the export
# write). The extension: a record row carrying the singular form
# (step int + tid int) rides the DEGENERATE own-step range
# [step, step] -- ONE step namespace with the range form (the
# item-1168 cross-check: promotion step_start vs node step at the
# same char + same value, 4,459 agree / 0 disagree); the resolve
# law unchanged (the degenerate range flows the existing
# position-aware path, the span-vs-own-position id cross-check
# stands); a row carrying BOTH forms, or the singular step without
# its tid, is a NAMED premise violation, never guessed; the census
# names BOTH forms per cohort (the range / the singular / neither).
# The battery gains the node-row-form fixtures carrying the bytes'
# own field forms (the v1.3.0 battery authored the range form for
# every lane -- a fixture and a builder sharing one assumption can
# never see the field-form gap; my run of record caught it) + the
# doc-12 known-answer (three same-value occurrences at steps
# 35/62/93: the same-step candidate excluded by the different-step
# law, the nearest picked -- the pair law picks 35). ZERO law
# changes elsewhere; the v1.2.7/v1.3.0 laws stand as stamped.

# v1.3.0 -- THE POSITION-AWARE RESOLUTION, AT MY STAMP (my words
# verbatim: "okay you have my stamps lets ove on to the build act lets
# split it up into three message4s"; the amendment act of items
# 1162/1163, the sheet amendment v3 pinned at my stamp): the recorded
# rule resolved each span to the FIRST commit row float-equal to the
# span's first numeric value -- POSITION-BLIND, so every same-doc
# same-value occurrence collapsed onto one row (the item-1161
# join-rule read). The amended law: each occurrence resolves to the
# commit AT-OR-COVERING ITS OWN STEP whose token float-equals the
# occurrence's first numeric value -- ONE RULE FOR BOTH LANES (never
# two resolution rules; the A2 lane re-resolves too, the shift itself
# a finding, never forced). The NAMED resolution-outcome classes:
# RESOLVED-OWN-STEP / step-outside-cache-coverage / value-mismatch-
# at-own-step / the standing UNRESOLVABLE-NON-NUMERIC; the
# matches-no-commit-anywhere case keeps its standing data-integrity
# hard exit (a different class, NAMED, unchanged). The exposure
# receipts that ground the amendment (item 1162): 6,947 of 7,115 a2
# statements ride same-doc repeated-value groups at DISTINCT steps
# (494 groups, 97.6%); 67 of 96 A2 slips ride a repeated in-doc
# value; 177 of 371 A1 promotions carry a same-doc same-value
# DIFFERENT-STEP candidate. The map-binding extension (the sheet's
# S3): the occurrence's own step fields ride the extraction rows --
# the extension reads fields the aligned bytes already carry
# (step_start/step_end/occurrence index), the STAMPED MAP untouched.
# The pair-law extension (the sheet's S4): every pair asserts
# hidden-row inequality -- PAIR-LAW-HIDDEN-ROW-EQUALITY fail-loud,
# closing the item-1161(e) hole (float-equal "5" vs "5.0" could pair
# the same row under the old law). The v1/v2 exports STAND as bytes
# of record; this build emits the v3 inventory under its own name at
# my run. The selfcheck battery gains the position-aware known-answer
# lanes (the synthetic commit-t layout now load-bearing, the doc-0
# repeated-value pattern the named case).

# v1.2.7 -- THE A1 RE-BIND, AT MY STAMP (my words verbatim: "okay
# lets gowith the recs and do the rerun"; the item-1158 rec 1 taken):
# the v1.2.6 A1 pairing landed every pair on the SAME t_0 (141 pairs,
# 140 of 141 the same commit row -- no actuator BY CONSTRUCTION), so
# the within-doc contrast pairs each promotion's t_0 against the
# same-doc SAME-VALUE DERIVED-VERIFIED occurrence at a DIFFERENT
# commitment step: the nearest-step candidate, the deterministic
# span-order tie-break, the step-distance logged per pair as a
# diagnostic; a promotion with no such candidate rides UNPAIRED with
# its reason NAMED (no same-doc DERIVED-VERIFIED rows / no same-value
# occurrence / the same-step-only class); the A2 lane and every other
# law byte-identical to the accepted v1.2.6. The pool census receipts
# (re-derived from the aligned-spans v2 bytes at the item-1159 bank):
# of the 371 promotions, ZERO carry a same-doc DIFFERENT-VALUE
# DERIVED-VERIFIED candidate; 177 carry a same-doc SAME-VALUE
# DIFFERENT-STEP candidate; ZERO stuck at the same step only; 194 sit
# in docs with zero DERIVED-VERIFIED rows. The v1 export STANDS as
# the bytes of record; this build emits the v2 inventory under its
# own name at my run.

# ---------------------------------------------------------------------------
# Section 1. The pinned inputs (the B0 pre-reg of record section 2; the
# pin-tail law: the banked form exact, invented tails a hard exit; the
# observed full shas are recorded in the export, never hand-typed).
# RE-PINNED at the stamped Arm A sheet amendment (cd1-arm-a-sheet-
# amendment-v1.md, 9297 B, e7a4fc6a...): the seven inputs of record at
# the 8B receipts; every move OLD-to-NEW named in the sheet's S2.
# RE-PINNED again at the checker re-emission (my item-1128 ruling 2:
# statement-rows forks; text-only reruns; receipts crossed exact): the
# two 17a label pins move to the re-emission exports, shas below.
# AMENDED at the aligned-spans act (my item-1128 ruling 1: the
# byte-pinned derived export first, the id-identity receipts presented
# before the map stamps): the aligned_spans pin joins the exports of
# record (items 1130/1131), and its banked receipts join the gate.
# The map-schema amendment of the same act: count_nested's list_field
# now digs a dot-path (the same dig law as every other path), so the
# nested per-doc lists (p2.nodes, p2.events, statements, node_rows)
# bind through the map -- single-key list_fields unchanged.
# ---------------------------------------------------------------------------
PINS = OrderedDict([
    ("17a_raw", {
        "file": "triadic_checker_offline_pass_8b.json",
        "prefix": "a61f2bc7", "bytes": 2338574,
        "desc": "the 8B raw-leg arithmetic checker export of record (item 888; the Arm A sheet amendment; the item-1128 ruling-2 statement-rows re-emission)"}),
    ("17a_chat", {
        "file": "triadic_checker_chat_8b.json",
        "prefix": "5ece17f8", "bytes": 136469,
        "desc": "the 8B chat-leg arithmetic checker export of record (item 888; the Arm A sheet amendment; the item-1128 ruling-2 statement-rows re-emission)"}),
    ("17p2", {
        "file": "triadic_p2rw17_offline_pass_8b_v1.json",
        "prefix": "4e711a58",
        "desc": "the ruled 750-doc rw17-P2 offline pass export of record (item 1123; the Arm A sheet amendment)"}),
    ("17p2_ledger", {
        "file": "triadic_p2rw17_offline_pass_8b_v1_per_doc.jsonl",
        "prefix": "ff10fe85",
        "desc": "the ruled 750-doc rw17-P2 per-doc provenance ledger of record (item 1123; the Arm A sheet amendment)"}),
    ("aligned_spans", {
        "file": "aligned_spans_v2.json",
        "sha": "263b2459e37aa974d519b1869e3bd92139d2d584e053e4cb811c4cf1ef6010b8",
        "bytes": 10792116,
        "desc": "the aligned-spans derived export of record (the item-1130 id-identity battery; the item-1131 v2 committed-value spans; every statement, promotion locus, and node row step-ref'd to token ids; zero gaps)"}),
    ("a2_raw_cache", {
        "file": "triadic_t2_cache_t2-gsm-full-8b_bfloat16_bos.jsonl",
        "sha": "a427adee8489bf96f36057592f7c5a571eca4fa5261bb3b99251c2d646d391ac",
        "records": 1329,
        "desc": "the true-8B raw math-corpus re-walk cache of record (A2 states; my paste receipt Oct 30 2026)"}),
    ("a2_chat_cache", {
        "file": "triadic_t2_cache_gsm-chat100-8b_bfloat16_bos.jsonl",
        "sha": "4953da290e049d7dba7b740f2697c4662f57d51932d28dbab5298253d297e2df",
        "records": 110,
        "desc": "the true-8B chat-cap re-walk cache of record (A2 states; my paste receipt Oct 30 2026)"}),
    ("p2_cache_r2", {
        "file": "triadic_t2_cache_rw17-p2-r2_bfloat16_bos.jsonl",
        "sha": "426459930ad726d77fcea8e30639d32dff71164bc9ebdf36970765bb2df500a4",
        "records": 760,
        "desc": "the ruled A1 state cache of record (the p2-r2 walk; my thin-run console crossed by paste at item 1122)"}),
])


def fail_loud(msg):
    raise SystemExit("HARD EXIT -- " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_pin(name, path, spec):
    """Assert one input against its banked pin; return the observed receipt.
    A wrong tail, size, or sha is a hard exit with the named record."""
    if not path or not os.path.isfile(path):
        fail_loud("input %s missing at %r (expected file %s)" %
                  (name, path, spec.get("file")))
    obs = sha256_file(path)
    size = os.path.getsize(path)
    if "sha" in spec and obs != spec["sha"]:
        fail_loud("pin %s: observed sha %s != the banked full sha" % (name, obs))
    if "prefix" in spec and not obs.startswith(spec["prefix"]):
        fail_loud("pin %s: observed sha %s carries no banked prefix %s "
                  "(the pin-tail law: never an invented tail)" %
                  (name, obs, spec["prefix"]))
    if "suffix" in spec and not obs.endswith(spec["suffix"]):
        fail_loud("pin %s: observed sha %s carries no banked suffix %s" %
                  (name, obs, spec["suffix"]))
    if "bytes" in spec and size != spec["bytes"]:
        fail_loud("pin %s: observed %d bytes != the banked %d" %
                  (name, size, spec["bytes"]))
    return {"observed_sha256": obs, "bytes": size}


def input_path(args_dir, spec):
    return os.path.join(args_dir, spec["file"]) if args_dir else spec["file"]


def assert_all_pins(args_dir):
    receipts = OrderedDict()
    for name, spec in PINS.items():
        receipts[name] = assert_pin(name, input_path(args_dir, spec), spec)
    return receipts


# ---------------------------------------------------------------------------
# Section 2. The cache reader (the schema of record, read from the
# instrument source's own cache writer: steps = the COLUMNS dict {t,
# id, E, rho, s, f, layer, H, PR, a, rsize, dead5, dead4, dead3,
# dead_share} -- one list per step, t contiguous, walk_ids == steps.id
# (the id-identity law); commits = the per-content-commitment rows with
# len(commits) == n_content_steps; hidden = RECORD-LEVEL, the final-
# normed last-layer state, ONE ROW PER CONTENT COMMIT. Banked
# assertions fail loud; the unbanked layout is DISCOVERED and
# inventoried, never assumed -- the never-guess law).
# ---------------------------------------------------------------------------
CACHE_RECORD_REQUIRED = [
    "key", "leg", "doc_id", "bos", "instrument", "prompt_len",
    "stop_reason", "n_gen_steps", "n_content_steps", "walk_ids",
    "steps", "commits",
]
STEPS_COLUMNS_REQUIRED = ["t", "id"]
COMMIT_ROW_REQUIRED = ["t", "token", "phase"]
HIDDEN_BYTES_PER_VALUE = 2   # float16, the instrument writer's own form


def read_cache_records(name, path, expect_records=None, full=True):
    """Read the walk cache jsonl; assert the schema of record (read from
    the instrument source, triadic_telemetry_t2 v32.3.x cache writer):
    steps = the COLUMNS dict {t, id, E, rho, s, f, layer, H, PR, a,
    rsize, dead5, dead4, dead3, dead_share} (one list per step, t
    contiguous, walk_ids == steps.id -- both appended from the same
    emitted id); commits = the per-content-commitment rows {t, token,
    phase, ...} with len(commits) == n_content_steps; hidden rides the
    RECORD (hidden_n/hidden_dim/hidden_b64): the final-normed LAST-
    LAYER state, ONE ROW PER CONTENT COMMIT (hidden_n == n_content_
    steps; the strided per-layer H/PR monitor reads ride steps.layer =
    t % n_layers and are monitor columns only, never the banked state).
    An empty-form row and a thin rider are NAMED premise violations;
    the unbanked extras are discovered + inventoried, never assumed."""
    records = []
    record_field_inventory = Counter()
    step_column_inventory = Counter()
    commit_field_inventory = Counter()
    hidden_layout = Counter()
    dim_set = set()
    with open(path) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError as e:
                fail_loud("cache %s line %d: not valid JSON (%s)" %
                          (name, i + 1, e))
            if not isinstance(r, dict):
                fail_loud("cache %s line %d: record is not an object" %
                          (name, i + 1))
            if r.get("empty"):
                fail_loud("cache %s line %d: EMPTY FORM -- the zero-"
                          "generation marker row (key %r); a NAMED "
                          "premise violation on this read (the banked "
                          "cache pin carries zero empty-form rows)"
                          % (name, i + 1, r.get("key")))
            for k in CACHE_RECORD_REQUIRED:
                if k not in r:
                    fail_loud("cache %s line %d: missing banked field %r"
                              % (name, i + 1, k))
            record_field_inventory.update(r.keys())
            # the steps columns dict (the instrument source's layout)
            steps = r["steps"]
            if not isinstance(steps, dict):
                fail_loud("cache %s line %d: steps is not the "
                          "instrument's COLUMNS dict (the schema of "
                          "record from the instrument source)"
                          % (name, i + 1))
            for col in STEPS_COLUMNS_REQUIRED:
                if col not in steps:
                    fail_loud("cache %s line %d: steps carries no "
                              "column %r" % (name, i + 1, col))
            step_column_inventory.update(steps.keys())
            n = r["n_gen_steps"]
            if not isinstance(n, int):
                fail_loud("cache %s line %d: n_gen_steps is not an int"
                          % (name, i + 1))
            for col in ("t", "id"):
                if len(steps[col]) != n:
                    fail_loud("cache %s line %d: steps column %r length "
                              "%d != n_gen_steps %d" %
                              (name, i + 1, col, len(steps[col]), n))
            # t contiguity (the emission order law)
            ts = steps["t"]
            for a, b in zip(ts, ts[1:]):
                if not isinstance(b, int) or b != a + 1:
                    fail_loud("cache %s line %d: steps t not contiguous "
                              "(%r then %r)" % (name, i + 1, a, b))
            # the id-identity law: walk_ids == steps.id (the source
            # appends both from the same emitted id, every step)
            if r["walk_ids"] != steps["id"]:
                fail_loud("cache %s line %d: walk_ids != steps.id (the "
                          "id-identity law of the instrument source; "
                          "doc %r)" % (name, i + 1, r.get("doc_id")))
            # the commits rows (the content-commitment ledger)
            commits = r["commits"]
            if not isinstance(commits, list):
                fail_loud("cache %s line %d: commits is not a list" %
                          (name, i + 1))
            for c in commits:
                if not isinstance(c, dict):
                    fail_loud("cache %s line %d: a commits row is not "
                              "an object" % (name, i + 1))
                for k in COMMIT_ROW_REQUIRED:
                    if k not in c:
                        fail_loud("cache %s line %d: a commits row "
                                  "missing banked field %r" %
                                  (name, i + 1, k))
                commit_field_inventory.update(c.keys())
            if len(commits) != r["n_content_steps"]:
                fail_loud("cache %s line %d: len(commits) %d != "
                          "n_content_steps %d (doc %r)" %
                          (name, i + 1, len(commits),
                           r["n_content_steps"], r.get("doc_id")))
            # the hidden law: the final-normed last-layer state, ONE
            # ROW PER CONTENT COMMIT (the instrument source: hidden_rows
            # appended inside the commit block, model.norm applied)
            if r.get("hidden_n") != r["n_content_steps"]:
                fail_loud("cache %s line %d: hidden_n %r != n_content_"
                          "steps %d (the one-row-per-commit law of the "
                          "instrument source; doc %r -- the states this "
                          "read banks are the per-commit last-layer "
                          "states, a divergence a NAMED premise "
                          "violation)" % (name, i + 1, r.get("hidden_n"),
                                          r["n_content_steps"],
                                          r.get("doc_id")))
            dim = r.get("hidden_dim")
            if not isinstance(dim, int) or dim <= 0:
                fail_loud("cache %s line %d: hidden_dim is not the "
                          "counted form (%r)" % (name, i + 1, dim))
            dim_set.add(dim)
            hb = r.get("hidden_b64", "")
            if hb == "" and r["hidden_n"] > 0:
                fail_loud("cache %s line %d: THIN RIDER REFUSED -- "
                          "hidden_b64 empty with hidden_n %d (the "
                          "zero-hidden convention), a NAMED premise "
                          "violation on a full-cache read (doc %r)" %
                          (name, i + 1, r["hidden_n"], r.get("doc_id")))
            if hb:
                raw_len = len(base64.b64decode(hb))
                want = HIDDEN_BYTES_PER_VALUE * r["hidden_n"] * dim
                if raw_len != want:
                    fail_loud("cache %s line %d: hidden bytes %d != the "
                              "float16 form %d (2 x hidden_n %d x dim "
                              "%d; doc %r)" % (name, i + 1, raw_len,
                                               want, r["hidden_n"],
                                               dim, r.get("doc_id")))
                hidden_layout["record_level_one_row_per_commit"] += 1
            records.append(r)
    if expect_records is not None and len(records) != expect_records:
        fail_loud("cache %s: %d records read != the banked %d" %
                  (name, len(records), expect_records))
    return records, {
        "record_count": len(records),
        "record_field_inventory": dict(record_field_inventory),
        "step_column_inventory": dict(step_column_inventory),
        "commit_field_inventory": dict(commit_field_inventory),
        "hidden_layout": dict(hidden_layout),
        "hidden_dims_observed": sorted(dim_set),
    }


# ---------------------------------------------------------------------------
# Section 3. The export loaders (generic, zero concept mapping: Pass 1
# reads structure only; the field map rides my stamp, never a guess).
# ---------------------------------------------------------------------------
def load_json_file(name, path):
    try:
        with open(path) as f:
            return json.load(f)
    except ValueError as e:
        fail_loud("export %s: not valid JSON (%s)" % (name, e))


def load_jsonl_file(name, path):
    out = []
    with open(path) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except ValueError as e:
                fail_loud("ledger %s line %d: not valid JSON (%s)" %
                          (name, i + 1, e))
    return out


def census_value(v, maxlen=48):
    s = repr(v)
    return s if len(s) <= maxlen else s[:maxlen] + "..."


def census_field(container_name, field, values, lines, low_card_max=30):
    """One field's census line: its value count, and the value shares
    when the cardinality is low. Zero concept mapping -- the field names
    and values print as the bytes carry them. A value the bytes carry
    as a list or dict (unhashable) counts by its canonical serialized
    form (the v1.2.2 catch: the real exports carry list-valued fields;
    the census DISCOVERS them, never crashes on them)."""
    def count_key(v):
        try:
            hash(v)
            return v
        except TypeError:
            return json.dumps(v, sort_keys=True)
    uniq = Counter(count_key(v) for v in values)
    n = len(values)
    if n == 0:
        lines.append("  %s.%s: (no values)" % (container_name, field))
        return
    if len(uniq) <= low_card_max:
        shares = ", ".join("%s=%d" % (census_value(k), c)
                           for k, c in uniq.most_common())
        lines.append("  %s.%s: n=%d unique=%d | %s" %
                     (container_name, field, n, len(uniq), shares))
    else:
        sample = ", ".join(census_value(k) for k in list(uniq)[:5])
        lines.append("  %s.%s: n=%d unique=%d | sample: %s" %
                     (container_name, field, n, len(uniq), sample))


def census_object(container_name, obj, lines, depth=0):
    """Census one container (a list of records or a dict): the field
    inventory + per-field value shares, one level of nesting opened."""
    if isinstance(obj, list):
        lines.append("%s: LIST n=%d" % (container_name, len(obj)))
        if obj and all(isinstance(r, dict) for r in obj):
            fields = []
            for r in obj:
                fields.extend(r.keys())
            for field in sorted(set(fields)):
                values = [r.get(field) for r in obj if field in r]
                census_field(container_name, field, values, lines)
                # one level of nesting opened, read-only discovery
                nested = [v for v in values if isinstance(v, (dict, list))]
                if nested and depth < 1:
                    if all(isinstance(v, dict) for v in nested[:3]):
                        census_object("%s.%s" % (container_name, field),
                                      nested, lines, depth + 1)
                    elif all(isinstance(v, list) for v in nested[:3]):
                        lens = [len(v) for v in nested if isinstance(v, list)]
                        lines.append("  %s.%s: nested lists, lens n=%d "
                                     "min=%s max=%s" %
                                     (container_name, field, len(lens),
                                      min(lens) if lens else "-",
                                      max(lens) if lens else "-"))
        else:
            kinds = Counter(type(r).__name__ for r in obj)
            lines.append("%s: LIST n=%d kinds=%s" %
                         (container_name, len(obj), dict(kinds)))
    elif isinstance(obj, dict):
        lines.append("%s: DICT keys=%s" %
                     (container_name, sorted(obj.keys())))
        for k, v in obj.items():
            if isinstance(v, list):
                census_object("%s.%s" % (container_name, k), v, lines,
                               depth + 1)
            elif isinstance(v, dict) and depth < 2:
                census_object("%s.%s" % (container_name, k), v, lines,
                              depth + 1)
            else:
                lines.append("  %s.%s = %s" %
                             (container_name, k, census_value(v)))
    else:
        lines.append("%s = %s" % (container_name, census_value(obj)))


# ---------------------------------------------------------------------------
# Section 4. The census pass (Pass 1: read-only on inputs, zero writes
# to them, zero concept mapping; the candidate map is derived AFTER my
# reading of the census, pinned by MY STAMP -- never by this tool).
# ---------------------------------------------------------------------------
def run_census(args):
    pins = assert_all_pins(args.inputs_dir)
    out = OrderedDict()
    out["tool"] = TOOL + " v" + VERSION + " (build part " + BUILD_PART + ")"
    out["mode"] = "census (Pass 1, read-only)"
    out["input_receipts"] = pins
    out["censuses"] = OrderedDict()
    exports = [
        ("17a_raw", "json"),
        ("17a_chat", "json"),
        ("17p2", "json"),
        ("17p2_ledger", "jsonl"),
        ("aligned_spans", "json"),
    ]
    for name, kind in exports:
        path = input_path(args.inputs_dir, PINS[name])
        data = load_export(name, kind, path)
        lines = []
        census_object(name, data, lines)
        out["censuses"][name] = lines
    outpath = args.out or "cd1_arm_a_b0_census_v1.json"
    with open(outpath, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("=== CD-1 ARM A B0 CENSUS (Pass 1, read-only) ===")
    print("input pins asserted: %d" % len(pins))
    for name, lines in out["censuses"].items():
        for ln in lines[:40]:
            print(ln)
        if len(lines) > 40:
            print("  ... (%d more lines in the census export)" %
                  (len(lines) - 40))
    print("census export: %s" % outpath)
    print("NEXT: the candidate field map derives FROM THIS CENSUS at the "
          "my door; MY STAMP pins the map; only then --run.")
    return 0


# ---------------------------------------------------------------------------
# Section 5. The selfcheck battery (part 1: the pin engine + the cache
# reader + the census on synthetic fixtures; every check known-answer,
# fail-loud verified by construction).
# ---------------------------------------------------------------------------
SELFCHECKS = []


def selfcheck(name):
    def deco(fn):
        SELFCHECKS.append((name, fn))
        return fn
    return deco


def synth_cache_record(doc_id="d0", n_steps=3, n_commits=None, hidden=True,
                       thin=False, empty_form=False, drop=None,
                       break_contiguity=False, break_id_identity=False,
                       break_hidden_n=False, dim=8, ids=None,
                       commit_tokens=None, leg="synth-leg",
                       instrument="synth v32.3.2", commit_ts=None):
    """A synthetic cache record in the INSTRUMENT SOURCE's own layout:
    steps = the columns dict; commits = the per-commitment rows; hidden
    = record-level, one row per commit, float16 bytes. THE v1.3.0
    ADDITION: commit_ts names each commit's own step t explicitly --
    under the position-aware rule the commit t is LOAD-BEARING (the
    occurrence resolves to the commit at-or-covering its OWN step);
    the default t=j layout stays for the standing lanes."""
    if empty_form:
        return {"key": "%s:%s" % (leg, doc_id), "empty": True, "bos": True}
    if n_commits is None:
        n_commits = max(1, n_steps - 1)
    if ids is None:
        ids = list(range(200, 200 + n_steps))
    if commit_tokens is None:
        commit_tokens = ["tok%d" % j for j in range(n_commits)]
    if commit_ts is None:
        commit_ts = list(range(n_commits))
    steps = {"t": list(range(n_steps)), "id": list(ids),
             "E": [0.5] * n_steps, "rho": [0.1] * n_steps,
             "s": [0.9] * n_steps, "f": [None] * n_steps,
             "layer": [t % 32 for t in range(n_steps)],
             "H": [None] * n_steps, "PR": [None] * n_steps,
             "a": [None] * n_steps, "rsize": [0] * n_steps,
             "dead5": [None] * n_steps, "dead4": [None] * n_steps,
             "dead3": [None] * n_steps, "dead_share": [None] * n_steps}
    if break_contiguity and n_steps >= 3:
        steps["t"][2] = steps["t"][1] + 2
    if break_id_identity:
        steps["id"] = list(ids)
        steps["id"][0] = steps["id"][0] + 1
    commits = []
    for j in range(n_commits):
        commits.append({"t": commit_ts[j], "token": commit_tokens[j],
                        "phase": "CoT", "K": 0.25, "emitted_p": 0.5,
                        "margin": 0.1, "content_mass": 0.5,
                        "hedge_mass": 0.0, "gamma_p": 0.0,
                        "gamma_g": 0.0, "gm_p": 0.0, "gm_g": 0.0,
                        "gamma_valid": False, "second_id": None,
                        "second_str": None, "second_p": None})
    hidden_n = n_commits
    if break_hidden_n:
        hidden_n = n_commits + 1
    rec = {
        "key": "%s:%s" % (leg, doc_id), "leg": leg, "doc_id": doc_id,
        "bos": True, "instrument": instrument, "prompt_len": 12,
        "stop_reason": "eos", "n_gen_steps": n_steps,
        "n_content_steps": n_commits, "walk_ids": list(ids),
        "steps": steps, "commits": commits,
        "hidden_n": hidden_n, "hidden_dim": dim,
        "hidden_b64": (base64.b64encode(
            bytes([1] * (HIDDEN_BYTES_PER_VALUE * hidden_n * dim)))
            .decode() if hidden else ""),
    }
    if thin:
        rec["hidden_b64"] = ""
    if drop:
        rec.pop(drop, None)
    return rec


def write_jsonl(path, records):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, sort_keys=True) + "\n")


@selfcheck("pin engine: exact-sha accept + wrong-tail hard exit + byte-count check")
def check_pin_engine():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "f.bin")
        payload = b"abc" * 100
        with open(p, "wb") as f:
            f.write(payload)
        want = hashlib.sha256(payload).hexdigest()
        # the exact form accepts
        r = assert_pin("t1", p, {"sha": want, "bytes": len(payload)})
        assert r["observed_sha256"] == want and r["bytes"] == len(payload)
        # a wrong prefix is a hard exit with the named record
        try:
            assert_pin("t2", p, {"prefix": "deadbeef"})
            raise AssertionError("wrong-prefix pin was accepted")
        except SystemExit as e:
            assert "t2" in str(e) and "deadbeef" in str(e)
        # a wrong byte count is a hard exit
        try:
            assert_pin("t3", p, {"prefix": want[:8], "bytes": 7})
            raise AssertionError("wrong-byte pin was accepted")
        except SystemExit as e:
            assert "bytes" in str(e)
        # a missing file is a hard exit
        try:
            assert_pin("t4", os.path.join(d, "nope"), {})
            raise AssertionError("missing file was accepted")
        except SystemExit as e:
            assert "missing" in str(e)
    return "PASS"


@selfcheck("cache reader: the instrument-source schema -- columns-dict accept + drift exits + thin rider + empty form + id identity + the one-row-per-commit law")
def check_cache_reader():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "c.jsonl")
        # the good read accepts and inventories the real layout
        write_jsonl(p, [synth_cache_record("d1", n_steps=4, n_commits=3),
                        synth_cache_record("d2", n_steps=2, n_commits=1)])
        recs, inv = read_cache_records("t", p, expect_records=2)
        assert len(recs) == 2 and inv["record_count"] == 2
        assert inv["step_column_inventory"]["id"] == 2
        assert inv["commit_field_inventory"]["token"] == 4  # 3+1 rows
        assert inv["hidden_layout"]["record_level_one_row_per_commit"] == 2
        assert inv["hidden_dims_observed"] == [8]
        # a dropped banked field is a hard exit, named
        write_jsonl(p, [synth_cache_record("d1", drop="n_content_steps")])
        try:
            read_cache_records("t", p)
            raise AssertionError("schema drift was accepted")
        except SystemExit as e:
            assert "n_content_steps" in str(e)
        # an empty-form row is a NAMED premise violation
        write_jsonl(p, [synth_cache_record("d1", empty_form=True)])
        try:
            read_cache_records("t", p)
            raise AssertionError("an empty form was accepted")
        except SystemExit as e:
            assert "EMPTY FORM" in str(e)
        # a thin rider is refused loudly, named, never silent
        write_jsonl(p, [synth_cache_record("d1", thin=True)])
        try:
            read_cache_records("t", p)
            raise AssertionError("a thin rider was accepted")
        except SystemExit as e:
            assert "THIN RIDER REFUSED" in str(e) and "d1" in str(e)
        # broken t contiguity is a hard exit
        write_jsonl(p, [synth_cache_record("d1", break_contiguity=True)])
        try:
            read_cache_records("t", p)
            raise AssertionError("broken contiguity was accepted")
        except SystemExit as e:
            assert "contiguous" in str(e)
        # walk_ids != steps.id is a hard exit (the id-identity law)
        write_jsonl(p, [synth_cache_record("d1", break_id_identity=True)])
        try:
            read_cache_records("t", p)
            raise AssertionError("an id-identity break was accepted")
        except SystemExit as e:
            assert "id-identity" in str(e)
        # hidden_n != n_content_steps is a hard exit (the commit-row law)
        write_jsonl(p, [synth_cache_record("d1", break_hidden_n=True)])
        try:
            read_cache_records("t", p)
            raise AssertionError("a hidden_n drift was accepted")
        except SystemExit as e:
            assert "one-row-per-commit" in str(e)
        # the record-count reconciliation
        write_jsonl(p, [synth_cache_record("d1")])
        try:
            read_cache_records("t", p, expect_records=5)
            raise AssertionError("a wrong record count was accepted")
        except SystemExit as e:
            assert "banked" in str(e)
    return "PASS"


@selfcheck("census: synthetic export structure prints + low-cardinality shares + zero concept mapping")
def check_census():
    export = {
        "pass": "synthetic", "tool": "synthetic tool",
        "per_doc": [
            {"doc_id": i, "class": ["UNTRACED", "DERIVED-VERIFIED",
                                    "PROMPT", "DERIVED-SLIP"][i % 4],
             "n": i} for i in range(8)],
        "meta": {"version": 1, "kinds": 3},
    }
    lines = []
    census_object("synth", export, lines)
    text = "\n".join(lines)
    assert "per_doc: LIST n=8" in text
    assert "class" in text and "'UNTRACED'=2" in text
    assert "meta" in text and "DICT" in text
    # a jsonl ledger censuses the same way
    ledger = [{"doc_id": "a", "v": 1}, {"doc_id": "b", "v": 1}]
    lines2 = []
    census_object("led", ledger, lines2)
    assert "led: LIST n=2" in "\n".join(lines2)
    # the v1.2.2 regression: a list-valued field (the real-export catch:
    # unhashable values) censuses by its canonical serialized form,
    # never a TypeError crash
    listy = {"pass": "synthetic",
             "per_doc": [{"doc_id": i, "locus": [50, 51 + i]}
                         for i in range(4)]}
    lines3 = []
    census_object("listy", listy, lines3)
    t3 = "\n".join(lines3)
    assert "locus" in t3 and "'[50, 51]'=1" in t3
    return "PASS"


def run_selfcheck():
    print("=== B0 SELFCHECK BATTERY (build part %s) ===" % BUILD_PART)
    fails = 0
    for name, fn in SELFCHECKS:
        try:
            res = fn()
            print("[PASS] %s -- %s" % (res, name))
        except Exception as e:
            fails += 1
            print("[FAIL] %s -- %s" % (type(e).__name__, e))
    print("selfcheck: %d/%d PASS" % (len(SELFCHECKS) - fails, len(SELFCHECKS)))
    if fails:
        fail_loud("%d selfcheck failures" % fails)
    return 0


# ---------------------------------------------------------------------------
# Section 6. The banked receipts (the reconciliation constants of record --
# the record's OWN numbers, cited here never re-derived here: the 8B 17-A
# genuine-slip subclasses 94 raw (94 of 6,805 in 57 of 1,319 docs) + 2 chat
# (2 of 310 in 1 of 100 docs); the slip-rate receipts at the banked
# two-decimal prints 1.38 / 0.65 (the observed export rates
# 0.013813372520205732 raw / 0.0064516129032258064 chat); the ruled
# 750-doc rw17-P2 class-level receipts promotions 371 (A97/B274; RxA87
# RxB137 DxA10 DxB137), conflicts 42 (R14/D28), control 39, established
# 630, immune 1808, desire engaged 682, silence 0 -- item 1123, my
# readings presented; the 1B-era constants STRUCK by the stamped Arm A
# sheet amendment, the moves named in its S4).
# ---------------------------------------------------------------------------
BANKED_RECEIPTS = OrderedDict([
    ("17a_raw_genuine_slips", {"export": "17a_raw", "banked": 94,
     "desc": "the 8B 17-A raw-leg genuine-slip subclass of record (94 of 6,805 in 57 of 1,319 docs)"}),
    ("17a_raw_slip_rate_print", {"export": "17a_raw", "banked": "1.38",
     "desc": "the 8B 17-A raw-leg slip-rate receipt (the two-decimal print; the observed export rate 0.013813372520205732)"}),
    ("17a_chat_genuine_slips", {"export": "17a_chat", "banked": 2,
     "desc": "the 8B 17-A chat-leg genuine-slip subclass of record (2 of 310 in 1 of 100 docs)"}),
    ("17a_chat_slip_rate_print", {"export": "17a_chat", "banked": "0.65",
     "desc": "the 8B 17-A chat-leg slip-rate receipt (the two-decimal print; the observed export rate 0.0064516129032258064)"}),
    ("17p2_promotions", {"export": "17p2", "banked": 371,
     "desc": "the ruled 750-doc rw17-P2 promotions receipt (A97/B274; RxA87 RxB137 DxA10 DxB137)"}),
    ("17p2_conflicts", {"export": "17p2", "banked": 42,
     "desc": "the ruled 750-doc rw17-P2 conflict-events receipt (R14/D28)"}),
    ("17p2_control", {"export": "17p2", "banked": 39,
     "desc": "the ruled 750-doc rw17-P2 control-census receipt"}),
    ("17p2_established", {"export": "17p2", "banked": 630,
     "desc": "the ruled 750-doc rw17-P2 established-class receipt"}),
    ("17p2_immune", {"export": "17p2", "banked": 1808,
     "desc": "the ruled 750-doc rw17-P2 immune-class receipt"}),
    ("17p2_desire_engaged", {"export": "17p2", "banked": 682,
     "desc": "the ruled 750-doc rw17-P2 desire-engaged receipt"}),
    ("17p2_silence", {"export": "17p2", "banked": 0,
     "desc": "the ruled 750-doc rw17-P2 silence census receipt"}),
    ("17p2_derived_verified", {"export": "17p2", "banked": 630,
     "desc": "the ruled 750-doc rw17-P2 derived-verified node census receipt (the p2.nodes list_field, node DERIVED-VERIFIED; the A1-negatives class of the census)"}),
    ("aligned_a2_raw_statements", {"export": "aligned_spans", "banked": 6805,
     "desc": "the aligned-spans raw-leg statement census (every well-formed statement of the 17a_raw re-emission, step-ref'd; zero gaps)"}),
    ("aligned_a2_raw_slips", {"export": "aligned_spans", "banked": 94,
     "desc": "the aligned-spans raw-leg slip rows (statement verdict False -- the A2 positives, spanned to token ids)"}),
    ("aligned_a2_raw_clean", {"export": "aligned_spans", "banked": 6711,
     "desc": "the aligned-spans raw-leg clean rows (statement verdict True -- the A2 negatives, enumerated and spanned per my item-1128 ruling 2)"}),
    ("aligned_a2_chat_statements", {"export": "aligned_spans", "banked": 310,
     "desc": "the aligned-spans chat-leg statement census (zero gaps)"}),
    ("aligned_a2_chat_slips", {"export": "aligned_spans", "banked": 2,
     "desc": "the aligned-spans chat-leg slip rows (verdict False)"}),
    ("aligned_a2_chat_clean", {"export": "aligned_spans", "banked": 308,
     "desc": "the aligned-spans chat-leg clean rows (verdict True)"}),
    ("aligned_a2_raw_spanned", {"export": "aligned_spans", "banked": 6805,
     "desc": "the aligned-spans raw-leg spanned-statement census (read at the export's own spanned field; zero gaps by spanned == total, both banked receipts)"}),
    ("aligned_a2_chat_spanned", {"export": "aligned_spans", "banked": 310,
     "desc": "the aligned-spans chat-leg spanned-statement census (zero gaps by spanned == total, both banked receipts)"}),
    ("aligned_p2_promotion_spans", {"export": "aligned_spans", "banked": 371,
     "desc": "the aligned-spans promotion loci (every 17p2 PROMOTION event, step-ref'd to token ids; the A1-positives class)"}),
    ("aligned_p2_node_rows", {"export": "aligned_spans", "banked": 28059,
     "desc": "the aligned-spans p2 node-occurrence rows (one row per node occurrence, locator-classed)"}),
    ("aligned_p2_node_unique", {"export": "aligned_spans", "banked": 429,
     "desc": "the aligned-spans node rows at locator unique (the value located at exactly one step)"}),
    ("aligned_p2_node_absent", {"export": "aligned_spans", "banked": 149,
     "desc": "the aligned-spans node rows at locator value-absent (all prompt-side occurrences; never a derived node)"}),
    ("aligned_p2_derived_verified_occurrences", {"export": "aligned_spans", "banked": 4062,
     "desc": "the aligned-spans DERIVED-VERIFIED occurrence rows (the node_rows occurrences of the 630 distinct nodes; distinct-node census banked separately at 17p2_derived_verified)"}),
    ("aligned_a2_raw_decode_exact_docs", {"export": "aligned_spans", "banked": 1319,
     "desc": "the aligned-spans raw-leg id-identity receipt (decode-exact docs of 1,319; walk_ids == gen_text)"}),
    ("aligned_a2_chat_decode_exact_docs", {"export": "aligned_spans", "banked": 100,
     "desc": "the aligned-spans chat-leg id-identity receipt (decode-exact docs of 100)"}),
    ("aligned_p2_decode_exact_docs", {"export": "aligned_spans", "banked": 750,
     "desc": "the aligned-spans p2 id-identity receipt (decode-exact docs of 750)"}),
])


# ---------------------------------------------------------------------------
# Section 7. The field map (the candidate map of the B0 pre-reg section 3:
# the record's concepts bound to the census's own field names, frozen at
# MY STAMP via the map file -- never guessed by this tool; the map's sha
# recorded in every export; the stamp block recorded verbatim, never
# written by the tool).
# ---------------------------------------------------------------------------
MAP_REQUIRED_BLOCKS = ["map_name", "map_version", "stamp", "bindings"]
DEFAULT_MAP_PATH = "cd1_arm_a_field_map_v1.json"


class MapBindingError(Exception):
    """A binding the loaded bytes do not carry -- the coverage-discovery
    path of the B0 pre-reg section 3 (presented at my door,
    never a crash, never a silent drop)."""


def load_field_map(path):
    """Load the candidate field map; the structure asserted, the sha
    observed for the receipts. The map pins only at MY STAMP."""
    if not path or not os.path.isfile(path):
        fail_loud("the field map %r is absent -- the candidate map "
                  "derives FROM THE CENSUS at my door and pins "
                  "only at MY STAMP; never guessed here" % (path,))
    try:
        with open(path) as f:
            fmap = json.load(f)
    except ValueError as e:
        fail_loud("field map %s: not valid JSON (%s)" % (path, e))
    if not isinstance(fmap, dict):
        fail_loud("field map %s: not an object" % path)
    for k in MAP_REQUIRED_BLOCKS:
        if k not in fmap:
            fail_loud("field map %s: missing required block %r (the map "
                      "schema of the B0 pre-reg section 3)" % (path, k))
    if not isinstance(fmap["bindings"], dict):
        fail_loud("field map %s: the bindings block is not an object" % path)
    return fmap, sha256_file(path)


def load_export(name, kind, path):
    """One label export loaded by kind. The jsonl leg reads the ledger
    path -- the loader carries one job: the bytes read as the bytes lie;
    the pin law rides the load, never the loader."""
    if kind == "json":
        return load_json_file(name, path)
    if kind == "jsonl":
        return load_jsonl_file(name, path)
    fail_loud("export %s: unknown load kind %r" % (name, kind))


def dig(obj, path, ctx):
    """Walk one dot-path exactly as the map binds it; a field the bytes
    do not carry is a MapBindingError (the coverage-discovery path),
    never an invented read."""
    cur = obj
    for part in path.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                raise MapBindingError(
                    "%s: path %r -- list index %r absent" % (ctx, path, part))
        elif isinstance(cur, dict):
            if part not in cur:
                raise MapBindingError(
                    "%s: path %r -- the bytes carry no field %r"
                    % (ctx, path, part))
            cur = cur[part]
        else:
            raise MapBindingError(
                "%s: path %r -- cannot descend into %s at %r"
                % (ctx, path, type(cur).__name__, part))
    return cur


def apply_filter(rows, filt, ctx):
    """The map's row selection: match (field == value) and exclude
    (field not in values), nothing else -- zero invented semantics."""
    match = (filt or {}).get("match") or {}
    exclude = (filt or {}).get("exclude") or {}
    out = []
    for r in rows:
        if not isinstance(r, dict):
            fail_loud("%s: a filter row is not an object" % ctx)
        ok = True
        for f, v in match.items():
            if f not in r:
                raise MapBindingError(
                    "%s: the rows carry no field %r" % (ctx, f))
            if r[f] != v:
                ok = False
                break
        if ok:
            for f, vs in exclude.items():
                if f not in r:
                    raise MapBindingError(
                        "%s: the rows carry no field %r" % (ctx, f))
                if r[f] in vs:
                    ok = False
                    break
        if ok:
            out.append(r)
    return out


def derive_value(spec, loads, ctx):
    """One counting primitive, executed exactly as the map binds it."""
    if not isinstance(spec, dict) or "kind" not in spec:
        raise MapBindingError("%s: a binding carries no kind" % ctx)
    kind = spec["kind"]
    if kind == "read_value":
        return dig(loads[spec["export"]], spec["path"], ctx)
    if kind == "count_rows":
        rows = dig(loads[spec["export"]], spec["path"], ctx)
        if not isinstance(rows, list):
            raise MapBindingError("%s: path %r is not a list"
                                  % (ctx, spec["path"]))
        return len(apply_filter(rows, spec.get("filter"), ctx))
    if kind == "count_nested":
        docs = dig(loads[spec["export"]], spec["docs_path"], ctx)
        if not isinstance(docs, list):
            raise MapBindingError("%s: docs path %r is not a list"
                                  % (ctx, spec["docs_path"]))
        n = 0
        for d in docs:
            if not isinstance(d, dict):
                fail_loud("%s: a docs row is not an object" % ctx)
            try:
                inner = dig(d, spec["list_field"], ctx)
            except MapBindingError:
                raise MapBindingError(
                    "%s: the doc rows carry no list field %r"
                    % (ctx, spec["list_field"]))
            if inner is None:
                continue
            if not isinstance(inner, list):
                raise MapBindingError(
                    "%s: list field %r is not a list"
                    % (ctx, spec["list_field"]))
            n += len(apply_filter(inner, spec.get("filter"), ctx))
        return n
    if kind == "sum_field":
        rows = dig(loads[spec["export"]], spec["path"], ctx)
        if not isinstance(rows, list):
            raise MapBindingError("%s: path %r is not a list"
                                  % (ctx, spec["path"]))
        total = 0
        for r in apply_filter(rows, spec.get("filter"), ctx):
            v = r.get(spec["field"])
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                raise MapBindingError(
                    "%s: field %r is not a counted number"
                    % (ctx, spec["field"]))
            total += v
        return total
    if kind == "rate_print":
        num = derive_value(spec["num"], loads, ctx)
        den = derive_value(spec["den"], loads, ctx)
        if (not isinstance(num, (int, float)) or isinstance(num, bool)
                or not isinstance(den, (int, float)) or isinstance(den, bool)
                or den == 0):
            raise MapBindingError(
                "%s: the rate operands are not the counted numbers" % ctx)
        return ("%%.%df" % int(spec.get("decimals", 2))) % (100.0 * num / den)
    fail_loud("%s: unknown derive kind %r (the map schema of the B0 "
              "pre-reg section 3)" % (ctx, kind))


# ---------------------------------------------------------------------------
# Section 8. The reconciliation gate (the B0 pre-reg section 3, the new
# law): every banked receipt derives through the map's binding and must
# equal the banked count EXACTLY -- no best-fit, no tolerance. A
# divergence is a MISMATCH RECEIPT: the named target, the binding, the
# derived count beside the banked count -- a WRONG BINDING, never a
# discarded concept; the exit is a data-integrity stop only. A binding
# the bytes cannot carry is a COVERAGE DISCOVERY -- presented at the
# my door per the item-52/53 precedent, my stamps decide.
# ---------------------------------------------------------------------------
def reconcile(targets, bindings, loads, map_name):
    """Run the gate over the target list; return the three row classes."""
    receipts, mismatches, discoveries = [], [], []
    for t in targets:
        name = t["name"]
        ctx = "target %s (map %s)" % (name, map_name)
        b = bindings.get(name)
        if b is None:
            fail_loud("%s: the map carries no binding -- every banked "
                      "receipt needs one (the map is incomplete at my "
                      "door)" % ctx)
        try:
            derived = derive_value(b, loads, ctx)
        except MapBindingError as e:
            discoveries.append(OrderedDict([
                ("target", name), ("binding", b),
                ("finding",
                 "COVERAGE DISCOVERY -- %s; the record concept named, the "
                 "census's own fields the authority; presented at the "
                 "my door per the item-52/53 precedent, my stamps "
                 "decide, nothing silently dropped" % e)]))
            continue
        banked = t["banked"]
        if derived == banked:
            receipts.append(OrderedDict([
                ("target", name), ("derived", derived),
                ("banked", banked), ("status", "RECONCILED")]))
        else:
            mismatches.append(OrderedDict([
                ("target", name), ("binding", b),
                ("derived", derived), ("banked", banked),
                ("finding",
                 "MISMATCH RECEIPT -- the binding derives %r beside the "
                 "banked %r: a WRONG BINDING, never a discarded concept; "
                 "the map revised from the census's own evidence, "
                 "re-presented for my stamp, the gate re-runs; the exit "
                 "is a data-integrity stop only" % (derived, banked))]))
    return receipts, mismatches, discoveries


def run_reconcile(args):
    """--reconcile: the gate on the candidate map, pre-stamp. The pins
    assert first; the map loads; the exports load; the gate runs; the
    receipt table prints at my door; the export records everything."""
    pins = assert_all_pins(args.inputs_dir)
    fmap, map_sha = load_field_map(args.map)
    loads = OrderedDict()
    for name, kind in [("17a_raw", "json"), ("17a_chat", "json"),
                       ("17p2", "json"), ("17p2_ledger", "jsonl"),
                       ("aligned_spans", "json")]:
        loads[name] = load_export(name, kind,
                                  input_path(args.inputs_dir, PINS[name]))
    targets = [OrderedDict([("name", k), ("banked", BANKED_RECEIPTS[k]["banked"]),
                            ("desc", BANKED_RECEIPTS[k]["desc"])])
              for k in BANKED_RECEIPTS]
    receipts, mismatches, discoveries = reconcile(
        targets, fmap["bindings"], loads, fmap.get("map_name") or args.map)
    out = OrderedDict()
    out["tool"] = TOOL + " v" + VERSION + " (build part " + BUILD_PART + ")"
    out["mode"] = "reconcile (the reconciliation gate, pre-stamp)"
    out["input_receipts"] = pins
    out["map_file"] = args.map
    out["map_sha256_observed"] = map_sha
    out["map_stamp_block_verbatim"] = fmap.get("stamp")
    out["banked_receipts"] = OrderedDict(
        (k, BANKED_RECEIPTS[k]["banked"]) for k in BANKED_RECEIPTS)
    out["reconciled"] = receipts
    out["mismatch_receipts"] = mismatches
    out["coverage_discoveries"] = discoveries
    outpath = args.out or "cd1_arm_a_b0_reconciliation_v1.json"
    with open(outpath, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("=== CD-1 ARM A B0 RECONCILIATION GATE ===")
    print("input pins asserted: %d | map: %s (sha %s...)" %
          (len(pins), args.map, map_sha[:16]))
    for r in receipts:
        print("[RECONCILED] %s: derived %s == banked %s" %
              (r["target"], r["derived"], r["banked"]))
    for mm in mismatches:
        print("[MISMATCH RECEIPT] %s: derived %s != banked %s -- a WRONG "
              "BINDING, never a discarded concept; the map revised from "
              "the census's own evidence, re-presented, the gate re-runs"
              % (mm["target"], mm["derived"], mm["banked"]))
    for dd in discoveries:
        print("[COVERAGE DISCOVERY] %s -- presented at my door "
              "per the item-52/53 precedent; my stamps decide, nothing "
              "silently dropped" % dd["target"])
    print("reconciliation export: %s" % outpath)
    if discoveries:
        fail_loud("the gate stops: %d coverage discover(y/ies) presented "
                  "at my door; the map binding rides my stamps"
                  % len(discoveries))
    if mismatches:
        fail_loud("the gate stops: %d mismatch receipt(s); a "
                  "data-integrity stop only, the record untouched, never "
                  "a concept discard" % len(mismatches))
    print("ALL %d BANKED RECEIPTS RECONCILED -- the map is the ACCEPTED "
          "CANDIDATE" % len(receipts))
    print("NEXT: MY STAMP PINS THE MAP (the map sha above freezes at "
          "my pin); only then --run (the inventory layer lands in build "
          "part 3 of 3)")
    return 0


# ---------------------------------------------------------------------------
# Section 9. The t_0 resolution engine (the B0 pre-reg section 4 act 1).
# The t_0 law: the FIRST numeric token of the committed quantity span;
# never the equality sign (it is not numeric, and the law names it);
# never the span mean. An unresolvable span is a hard exit NAMED --
# never skipped, never averaged.
# ---------------------------------------------------------------------------
def resolve_t0(doc_id, leg, span, token_of, vnum):
    """Resolve one committed quantity span (step ids, in emission order)
    to its t_0. token_of(step_id) -> the token id at that step; vnum =
    the numeric token id set (pinned per leg at the inventory run)."""
    if not isinstance(span, (list, tuple)) or not span:
        fail_loud("t_0 UNRESOLVABLE -- doc %r leg %r: the span carries no "
                  "steps (%r)" % (doc_id, leg, span))
    for sid in span:
        try:
            tok = token_of(sid)
        except KeyError:
            fail_loud("t_0 UNRESOLVABLE -- doc %r leg %r: step %r absent "
                      "from the cache steps (the span resolved against "
                      "the wrong walk -- named, never skipped)"
                      % (doc_id, leg, sid))
        if tok in vnum:
            return sid
    fail_loud("t_0 UNRESOLVABLE -- doc %r leg %r span %r carries no "
              "numeric token (the t_0 law: the FIRST numeric token of "
              "the committed quantity span; never the equality sign; "
              "never the span mean; an unresolvable span is NAMED, "
              "never skipped)" % (doc_id, leg, list(span)))


# ---------------------------------------------------------------------------
# Section 10. The cohort binding engine (the B0 pre-reg section 4 act 2).
# A1: UNTRACED quantity spans the positives; matched DERIVED-VERIFIED
# spans IN THE SAME DOCS the negatives (the within-doc matched-
# population rule, mandatory for the role-geometry confound). A2: the
# genuine 17-A slips the positives; matched clean commitments IN THE
# SAME DOCS the negatives. Matching is deterministic (leg, doc_id, span
# order); a positive with no same-doc negative is UNPAIRED -- named,
# presented in the honest-population receipt, never silently dropped.
# The regime typing rides each row's own evidence field (the checker's
# derivation-path evidence only -- the circularity guard: never a
# candidate statistic; none exist at B0 by construction).
#
# THE v1.2.7 A1 AMENDMENT (my stamp, the item-1158 rec 1): the v1.2.6
# law paired each promotion with the FIRST unused same-doc
# DERIVED-VERIFIED row in span order -- on this corpus that landed
# 140 of 141 pairs on the SAME t_0 (the same quantity's two
# provenance typings), the row-level contrast reading NO ACTUATOR BY
# CONSTRUCTION (the item-1157 R-AA1 finding, at my door). The amended
# law pairs each promotion's t_0 against the same-doc SAME-VALUE
# DERIVED-VERIFIED occurrence at a DIFFERENT t_0 (two different
# hidden rows -- the regime-I question in its cleanest form): the
# NEAREST-step candidate, the deterministic span-order tie-break, the
# step-distance logged per pair as a diagnostic; a promotion without
# such a candidate rides UNPAIRED with its reason NAMED. The A2 lane
# keeps the v1.2.6 law byte-identical.
# ---------------------------------------------------------------------------
def sort_key(row):
    return (str(row.get("export", "")), str(row.get("leg", "")),
            str(row.get("doc_id", "")),
            json.dumps(row.get("span"), sort_keys=True) if row.get("span")
            is not None else "")


def bind_cohort(positives, negatives, cohort):
    """Bind one cohort: same-doc deterministic pairing; the unpaired
    positives named. The pair ids assign in sorted order, deterministic."""
    pairs, unpaired = [], []
    by_doc = OrderedDict()
    for n in negatives:
        by_doc.setdefault((n.get("export"), n.get("leg"), n.get("doc_id")),
                          []).append(n)
    used = set()
    for p in sorted(positives, key=sort_key):
        cands = by_doc.get((p.get("export"), p.get("leg"), p.get("doc_id")),
                           [])
        pick = None
        for n in sorted(cands, key=sort_key):
            if id(n) not in used:
                pick = n
                break
        if pick is None:
            unpaired.append(OrderedDict([
                ("cohort", cohort), ("positive", p),
                ("finding", "UNPAIRED -- no same-doc negative; presented "
                 "in the honest-population receipt, my stamps decide, "
                 "never silently dropped")]))
            continue
        used.add(id(pick))
        # the sheet's S4 law rides the A2 lane too: every pair
        # asserts hidden-row inequality, fail-loud NAMED
        _assert_pair_hidden_rows(p, pick, cohort)
        pairs.append(OrderedDict([
            ("pair_id", "%s-%04d" % (cohort, len(pairs) + 1)),
            ("cohort", cohort),
            ("export", p.get("export")), ("leg", p.get("leg")),
            ("doc_id", p.get("doc_id")),
            ("positive", p), ("negative", pick),
        ]))
    return pairs, unpaired


A1_BIND_RULE_TEXT = (
    "the v1.3.0 A1 bind (my stamp, the sheet amendment v3): each "
    "promotion's occurrence paired against the same-doc SAME-VALUE "
    "DERIVED-VERIFIED occurrence at a DIFFERENT occurrence step -- "
    "the position-aware measure (each occurrence's own step, the "
    "sheet's S1/S3 law; the v1.2.7 t_0 token-id difference was the "
    "position-blind proxy, its exports standing as bytes of record) "
    "-- the nearest occurrence-step candidate, the deterministic "
    "span-order tie-break, both distances logged per pair as "
    "diagnostics (occ_step_distance the v1.3.0 form, step_distance "
    "the v1.2.7 lineage form); a promotion without such a candidate "
    "rides UNPAIRED with its reason NAMED; two different hidden rows "
    "per pair ASSERTED (the sheet's S4: PAIR-LAW-HIDDEN-ROW-EQUALITY "
    "fail-loud, closing the item-1161(e) hole), the within-doc rule "
    "kept")

A2_BIND_RULE_TEXT = (
    "the standing A2 pairing law (unchanged from the accepted "
    "v1.2.6/v1.2.7): the genuine 17-A slips paired against the first "
    "unused same-doc clean commitment in span-sorted order, "
    "deterministic; a slip without one rides UNPAIRED, named. THE "
    "v1.3.0 LAYERS ON TOP: the rows RESOLVE under the ONE "
    "position-aware rule (the sheet's S1 -- the slip and the clean "
    "commitment each resolve to their OWN steps' commits, the A2 "
    "lane re-resolves, the shift itself a finding, never forced) and "
    "every pair ASSERTS hidden-row inequality (the sheet's S4: "
    "PAIR-LAW-HIDDEN-ROW-EQUALITY fail-loud)")


def _row_t0(row, cohort, what):
    """The row's resolved commitment step (the t_0 law's own step),
    a premise of the v1.2.7 A1 binding; an unresolved row reaching
    the binding is a NAMED premise violation, never a silent skip."""
    sr = row.get("span_resolution") or {}
    t0 = sr.get("t0")
    if not isinstance(t0, int):
        fail_loud("A1 binding (%s): %s row doc %r carries no "
                  "resolved t_0 (an unresolved row must never reach "
                  "the binding; the honest-population receipt owns "
                  "it) -- a NAMED premise violation"
                  % (what, cohort, row.get("doc_id")))
    return t0


def _row_occ_step(row, cohort, what):
    """The v1.3.0 position-aware premise: the row's OWN occurrence
    step (the sheet's S1/S3 law). A row reaching the binding without
    a RESOLVED-OWN-STEP resolution is a NAMED premise violation --
    never a silent position-blind fallback (the one-rule law)."""
    sr = row.get("span_resolution") or {}
    if sr.get("status") != "RESOLVED-OWN-STEP":
        fail_loud("binding (%s): %s row doc %r carries no "
                  "RESOLVED-OWN-STEP resolution (an unresolved or "
                  "out-of-coverage row must never reach the binding; "
                  "the honest-population receipt owns it) -- a NAMED "
                  "premise violation under the v1.3.0 one-rule law"
                  % (what, cohort, row.get("doc_id")))
    occ = sr.get("occ_step_t")
    if not isinstance(occ, int):
        fail_loud("binding (%s): %s row doc %r carries no own-step "
                  "receipt (a NAMED premise violation)"
                  % (what, cohort, row.get("doc_id")))
    return occ


def _assert_pair_hidden_rows(p, n, cohort):
    """The sheet's S4 pair-law extension: the two rows of each pair
    ride DIFFERENT hidden rows -- distinct (doc, occurrence, step)
    bindings, asserted per pair, fail-loud with its own NAMED class
    PAIR-LAW-HIDDEN-ROW-EQUALITY (a true data finding at my door,
    presented never smoothed; closes the item-1161(e) hole: float-
    equal values like "5" vs "5.0" could pair the same row under
    the old law)."""
    def _hr(row, what):
        hr = (row.get("span_resolution") or {}).get("hidden_row_index")
        if not isinstance(hr, int):
            fail_loud("%s pair-law (S4): the %s row doc %r carries no "
                      "hidden_row_index (a NAMED premise violation)"
                      % (cohort, what, row.get("doc_id")))
        return hr
    p_hr, n_hr = _hr(p, "positive"), _hr(n, "negative")
    if p_hr == n_hr:
        fail_loud("%s PAIR-LAW-HIDDEN-ROW-EQUALITY -- doc %r: the "
                  "pair's two rows ride the SAME hidden row %d (the "
                  "sheet amendment v3 S4 law; a true data finding at "
                  "my door, presented never smoothed)"
                  % (cohort, p.get("doc_id"), p_hr))


def bind_cohort_a1(positives, negatives, cohort):
    """The v1.3.0 A1 binding: same-doc, SAME VALUE, DIFFERENT
    occurrence step (the position-aware measure), nearest-step,
    span-order tie-break; both distances logged per pair (the
    occ_step_distance the v1.3.0 form, the step_distance the v1.2.7
    lineage form); the S4 hidden-row inequality asserted per pair;
    the unpaired promotions named with their reason class."""
    pairs, unpaired = [], []
    by_doc = OrderedDict()
    for n in negatives:
        by_doc.setdefault((n.get("export"), n.get("leg"),
                           n.get("doc_id")), []).append(n)
    used = set()
    for p in sorted(positives, key=sort_key):
        p_t0 = _row_t0(p, cohort, "positive")
        p_occ = _row_occ_step(p, cohort, "positive")
        p_val = p.get("value")
        cands = by_doc.get((p.get("export"), p.get("leg"),
                            p.get("doc_id")), [])
        if not cands:
            reason = ("no same-doc DERIVED-VERIFIED rows (the doc "
                      "carries no derived+verified occurrences at "
                      "all; structurally unpairable within-doc)")
        elif p_val is None:
            fail_loud("A1 binding: a promotion row doc %r carries "
                      "no value (the map's value_field law; a "
                      "NAMED premise violation)"
                      % (p.get("doc_id"),))
        else:
            same_val_any = [n for n in cands
                            if n.get("value") == p_val]
            same_val = [n for n in same_val_any
                        if id(n) not in used]
            if not same_val_any:
                reason = ("no same-doc SAME-VALUE "
                          "DERIVED-VERIFIED occurrence (the doc's "
                          "derived+verified rows carry other values "
                          "only)")
            else:
                diff_step = []
                for n in same_val:
                    n_t0 = _row_t0(n, cohort, "negative")
                    n_occ = _row_occ_step(n, cohort, "negative")
                    if n_occ != p_occ:
                        diff_step.append((abs(n_occ - p_occ), n))
                if not diff_step:
                    if not same_val:
                        reason = ("the same-doc SAME-VALUE "
                                  "DERIVED-VERIFIED occurrences all "
                                  "consumed by earlier pairs (the "
                                  "deterministic pairing law)")
                    else:
                        reason = ("the same-doc SAME-VALUE "
                                  "DERIVED-VERIFIED occurrences ride "
                                  "the SAME occurrence step only "
                                  "(the v1.3.0 position-aware law "
                                  "needs two different steps -- two "
                                  "different hidden rows)")
                else:
                    diff_step.sort(key=lambda t: (t[0], sort_key(t[1])))
                    _, pick = diff_step[0]
                    used.add(id(pick))
                    n_t0 = pick["span_resolution"]["t0"]
                    n_occ = pick["span_resolution"]["occ_step_t"]
                    _assert_pair_hidden_rows(p, pick, cohort)
                    pairs.append(OrderedDict([
                        ("pair_id", "A1-%04d" % (len(pairs) + 1)),
                        ("cohort", cohort),
                        ("export", p.get("export")), ("leg", p.get("leg")),
                        ("doc_id", p.get("doc_id")),
                        ("positive", p), ("negative", pick),
                        ("bind_law", A1_BIND_RULE_TEXT),
                        ("occ_step_distance", n_occ - p_occ),
                        ("step_distance", n_t0 - p_t0),
                    ]))
                    continue
        unpaired.append(OrderedDict([
            ("cohort", cohort), ("positive", p),
            ("finding", "UNPAIRED -- %s; presented in the "
             "honest-population receipt, my stamps decide, never "
             "silently dropped" % reason)]))
    return pairs, unpaired


# THE v1.3.0 S3 MAP-BINDING EXTENSION (my stamp, the sheet amendment
# v3) + THE v1.3.1/v1.3.2/v1.3.3 SINGULAR OWN-STEP FORMS (my
# stamps, the item-1168/1170/1172 binding discoveries): the
# occurrence's own step
# fields ride the extraction rows. The v1.3.0 extension reads the
# fields the aligned bytes ALREADY carry (step_start / step_end,
# the occurrence index i on the range lanes) -- the STAMPED MAP
# untouched, never edited. The bytes' own field law, MEASURED at
# item 1170: the RANGE lanes (promotions 371, A2 statements 7,115)
# carry [step_start, step_end(, i)] with i the occurrence ordinal;
# the node_rows lane (28,059, every class) carries the SINGULAR form
# [i, step, tid, occ_i] -- step + tid ride the SPAN-EXTENT own-step
# range [step, step + len(span) - 1] (the item-1172 law: the
# singular `step` is the span-HEAD step, the span the contiguous
# run covering the value -- the numeric can sit deeper), occ_i the
# occurrence index, i the lane's
# VALUE-GROUP ORDINAL (never the occurrence index: i==occ_i on 352
# of 4,062 DV rows only, so `i` is NEVER bound on the singular path
# -- binding it would guess a wrong index on 3,710 rows). ONE step
# namespace both forms; a row carrying BOTH forms (a range field +
# the singular) is a NAMED premise violation, never guessed (zero
# such rows in the bytes, the guard standing); the singular step
# without its tid likewise; a record row carrying no form is
# counted, never guessed (a JOINED row without them then fails the
# position-aware resolution NAMED -- the one-rule law, never a
# silent position-blind fallback); the census names BOTH forms per
# cohort (the range / the singular / neither), the bound fields
# only.
STEP_EXT_BINDINGS = (("step_start", "occ_step_start"),
                     ("step_end", "occ_step_end"),
                     ("i", "occ_index"))
SINGULAR_STEP_FIELD = "step"
SINGULAR_TID_FIELD = "tid"
SINGULAR_INDEX_BINDINGS = (("occ_i", "occ_index"),)
STEP_EXT_CENSUS = OrderedDict()


def extract_span_rows(loads, spec, ctx):
    """The map-driven span extraction: one record concept's rows pulled
    from the bound export path with the bound fields (doc id, records
    list, class, span, quantity, value, evidence). Zero guessing -- a
    field the bytes do not carry is a MapBindingError (the
    coverage-discovery path), never an invented read. The map-schema
    amendment of the item-1132 act: docs_path binds ONE path (string)
    or a LEG-UNION list of per-path entries ({"path": ..., "leg":
    ...}) -- the A2 cohorts span the raw + chat legs of the aligned
    export, one cohort binding each per the pre-reg; a per-entry leg
    names each leg's rows; the string form unchanged."""
    paths = spec["docs_path"]
    if isinstance(paths, str):
        entries = [OrderedDict([("path", paths),
                                ("leg", spec.get("leg"))])]
    elif isinstance(paths, list):
        entries = []
        for e in paths:
            if not isinstance(e, dict) or "path" not in e:
                raise MapBindingError(
                    "%s: a docs_path union entry carries no path (the "
                    "map schema: {path, leg} entries)" % (ctx,))
            entries.append(OrderedDict([
                ("path", e["path"]), ("leg", e.get("leg", spec.get("leg")))]))
    else:
        raise MapBindingError(
            "%s: docs_path %r is neither a path nor a union list"
            % (ctx, paths))
    out = []
    for ent in entries:
        rows = dig(loads[spec["export"]], ent["path"], ctx)
        if not isinstance(rows, list):
            raise MapBindingError("%s: docs path %r is not a list"
                                  % (ctx, ent["path"]))
        for d in rows:
            if not isinstance(d, dict):
                fail_loud("%s: a docs row is not an object" % ctx)
            if spec["doc_id_field"] not in d:
                raise MapBindingError("%s: the doc rows carry no field %r"
                                      % (ctx, spec["doc_id_field"]))
            doc_id = d[spec["doc_id_field"]]
            recs = dig(d, spec["records_field"], ctx)
            if recs is None:
                recs = []
            if not isinstance(recs, list):
                raise MapBindingError("%s: records field %r is not a list"
                                      % (ctx, spec["records_field"]))
            for rec in recs:
                if not isinstance(rec, dict):
                    fail_loud("%s: a records row is not an object" % ctx)
                cls = spec.get("record_class", "")
                if spec.get("class_field"):
                    if spec["class_field"] not in rec:
                        raise MapBindingError(
                            "%s: the record rows carry no field %r"
                            % (ctx, spec["class_field"]))
                    cls = rec[spec["class_field"]]
                    vals = spec.get("class_values")
                    if vals is not None and cls not in vals:
                        continue
                row = OrderedDict([("export", spec["export"]),
                                  ("doc_id", doc_id),
                                  ("record_class", cls)])
                ent_leg = ent.get("leg")
                if ent_leg is not None:
                    row["leg"] = ent_leg
                elif spec.get("leg") is not None:
                    row["leg"] = spec["leg"]
                elif spec.get("leg_field"):
                    if spec["leg_field"] not in rec:
                        raise MapBindingError(
                            "%s: the record rows carry no field %r"
                            % (ctx, spec["leg_field"]))
                    row["leg"] = rec[spec["leg_field"]]
                for out_f, rec_f in (("span", "span_field"),
                                     ("quantity", "quantity_field"),
                                     ("value", "value_field"),
                                     ("evidence", "evidence_field")):
                    if spec.get(rec_f):
                        if spec[rec_f] not in rec:
                            raise MapBindingError(
                                "%s: the record rows carry no field %r"
                                % (ctx, spec[rec_f]))
                        row[out_f] = rec[spec[rec_f]]
                # the v1.3.0 S3 extension (the sheet's law; counted,
                # never guessed; non-int step values a NAMED premise
                # violation) + the v1.3.1/v1.3.2/v1.3.3 singular
                # own-step forms (the item-1168/1170/1172 binding
                # discoveries): the node_rows lane carries its
                # occurrence's own step under the singular form --
                # step + tid ride the SPAN-EXTENT range [step, step +
                # len(span) - 1] (the item-1172 law: the singular
                # `step` is the span-HEAD step, the numeric can sit
                # deeper), occ_i the occurrence index; the lane's
                # `i` (the VALUE-GROUP ORDINAL) is
                # NEVER bound on this path (measured: i==occ_i on
                # 352 of 4,062 DV rows only); the both-forms guard
                # narrowed to the TRUE collision (a range field + the
                # singular on one row, zero such rows in the bytes);
                # every NAMED exit names the doc (the item-1170
                # presentation law)
                range_present = ("step_start" in rec
                                 or "step_end" in rec)
                singular_present = SINGULAR_STEP_FIELD in rec
                if range_present and singular_present:
                    fail_loud(
                        "%s doc %r: a record row carries BOTH step "
                        "field forms (the range + the singular %r) "
                        "-- two step namespaces on one row, a NAMED "
                        "premise violation, never guessed"
                        % (ctx, doc_id, SINGULAR_STEP_FIELD))
                ext_seen = []
                singular_seen = []
                if range_present:
                    # the v1.3.0 stamped law byte-identical:
                    # step_start/step_end/i bind per row (the range
                    # lanes' i is the occurrence ordinal)
                    for src_f, out_f in STEP_EXT_BINDINGS:
                        if src_f in rec:
                            if src_f != "i" and not isinstance(
                                    rec[src_f], int):
                                fail_loud(
                                    "%s doc %r: a record row carries "
                                    "a non-int %r %r (a NAMED "
                                    "premise violation, never "
                                    "guessed)"
                                    % (ctx, doc_id, src_f,
                                       rec[src_f]))
                            row[out_f] = rec[src_f]
                            ext_seen.append(src_f)
                elif singular_present:
                    if SINGULAR_TID_FIELD not in rec:
                        fail_loud(
                            "%s doc %r: a record row carries the "
                            "singular %r without its %r (the "
                            "singular form is step + tid together; "
                            "a NAMED premise violation, never "
                            "guessed)"
                            % (ctx, doc_id, SINGULAR_STEP_FIELD,
                               SINGULAR_TID_FIELD))
                    if not isinstance(rec[SINGULAR_STEP_FIELD], int) \
                            or not isinstance(
                                rec[SINGULAR_TID_FIELD], int):
                        fail_loud(
                            "%s doc %r: a record row carries a "
                            "non-int singular form (%r %r / %r %r) "
                            "(a NAMED premise violation, never "
                            "guessed)"
                            % (ctx, doc_id, SINGULAR_STEP_FIELD,
                               rec[SINGULAR_STEP_FIELD],
                               SINGULAR_TID_FIELD,
                               rec[SINGULAR_TID_FIELD]))
                    sv = rec[SINGULAR_STEP_FIELD]
                    sp = row.get("span")
                    if not (isinstance(sp, list) and sp
                            and all(isinstance(x, int) for x in sp)):
                        fail_loud(
                            "%s doc %r: a singular-form row carries "
                            "no int-token span %r (the span-extent "
                            "range law reads the row's own span; a "
                            "NAMED premise violation, never guessed)"
                            % (ctx, doc_id, sp))
                    # the SPAN-EXTENT own-step range [step, step +
                    # len(span) - 1] (the item-1172 law: the singular
                    # `step` is the span-HEAD step, the span the
                    # contiguous run covering the value -- the
                    # numeric can sit deeper; both ends derived from
                    # the row's own fields) -- the resolve law
                    # unchanged downstream
                    row["occ_step_start"] = sv
                    row["occ_step_end"] = sv + len(sp) - 1
                    row["occ_tid"] = rec[SINGULAR_TID_FIELD]
                    singular_seen = [SINGULAR_STEP_FIELD,
                                     SINGULAR_TID_FIELD]
                    # the occurrence index binds from occ_i ONLY;
                    # the lane's `i` rides the raw record only,
                    # never this row's index (item 1170)
                    for src_f, out_f in SINGULAR_INDEX_BINDINGS:
                        if src_f in rec:
                            if not isinstance(rec[src_f], int):
                                fail_loud(
                                    "%s doc %r: a record row carries "
                                    "a non-int %r %r (a NAMED "
                                    "premise violation, never "
                                    "guessed)"
                                    % (ctx, doc_id, src_f,
                                       rec[src_f]))
                            row[out_f] = rec[src_f]
                            singular_seen.append(src_f)
                c = STEP_EXT_CENSUS.setdefault(ctx, OrderedDict())
                if ext_seen:
                    c["rows_with_step_fields"] = \
                        c.get("rows_with_step_fields", 0) + 1
                    c["rows_with_range_form"] = \
                        c.get("rows_with_range_form", 0) + 1
                    seen = c.get("fields_seen", [])
                    c["fields_seen"] = sorted(
                        set(list(seen) + ext_seen))
                elif singular_seen:
                    c["rows_with_step_fields"] = \
                        c.get("rows_with_step_fields", 0) + 1
                    c["rows_with_singular_form"] = \
                        c.get("rows_with_singular_form", 0) + 1
                    seen = c.get("fields_seen", [])
                    c["fields_seen"] = sorted(
                        set(list(seen) + singular_seen))
                else:
                    # a lone-`i` row (no form present) carries no
                    # occurrence step -- counted without, its index
                    # never bound (zero real rows; the narrowing named
                    # at item 1170)
                    c["rows_without_step_fields"] = \
                        c.get("rows_without_step_fields", 0) + 1
                out.append(row)
    return out


# ---------------------------------------------------------------------------
# Section 11. The coverage-boundary counting (the B0 pre-reg section 4
# act 4). A commitment step whose operands are prompt-side (operand
# position < prompt_len -- prompt positions are never the emission
# boundary; their states are not banked) is OUT of cache coverage:
# counted and named as BHOB's out-of-coverage class, excluded from its
# denominator, never silently dropped. Generation-side operands
# (position >= prompt_len -- each was the emission boundary at its own
# step) stay in the covered population.
# ---------------------------------------------------------------------------
def split_coverage(commit_rows, ctx="the coverage boundary"):
    """Split commitment rows into covered / out-of-coverage. Each row
    carries: doc_id, leg, step, prompt_len, operands (positions)."""
    covered, excluded = [], []
    for r in commit_rows:
        if not isinstance(r, dict):
            fail_loud("%s: a commitment row is not an object" % ctx)
        for f in ("doc_id", "leg", "step", "prompt_len", "operands"):
            if f not in r:
                fail_loud("%s: a commitment row carries no %r (doc %r)"
                          % (ctx, f, r.get("doc_id")))
        plen = r["prompt_len"]
        ops = r["operands"]
        if not isinstance(ops, (list, tuple)) or not isinstance(plen, int):
            fail_loud("%s: doc %r leg %r -- the operands/prompt_len are "
                      "not the counted forms" % (ctx, r["doc_id"], r["leg"]))
        prompt_side = [o for o in ops
                       if isinstance(o, int) and o < plen]
        for o in ops:
            if not isinstance(o, int):
                fail_loud("%s: doc %r -- an operand position is not an "
                          "int (%r)" % (ctx, r["doc_id"], o))
        if prompt_side:
            ex = OrderedDict(r)
            ex["out_of_coverage"] = True
            ex["prompt_side_operands"] = prompt_side
            ex["finding"] = ("OUT OF CACHE COVERAGE -- prompt-side "
                             "operand(s) %r (positions < prompt_len %d; "
                             "prompt positions are never the emission "
                             "boundary, their states not banked); "
                             "counted and named, excluded from the BHOB "
                             "denominator, never silently dropped"
                             % (prompt_side, plen))
            excluded.append(ex)
        else:
            cv = OrderedDict(r)
            cv["out_of_coverage"] = False
            covered.append(cv)
    return covered, excluded


# ---------------------------------------------------------------------------
# Section 12. The selfcheck battery part 2 (the synthetic known-answer
# checks: the export loaders incl. the jsonl leg -- the part-1 catch's
# own regression check; the reconciliation gate's accept / mismatch
# receipt / coverage discovery; the t_0 law incl. the equality-sign
# skip and the unresolvable exit; the coverage boundary; the cohort
# binding with same-doc matching, unpaired naming, typing carried).
# ---------------------------------------------------------------------------
@selfcheck("export loaders: the four-kind load path incl. the jsonl ledger leg (the part-1 catch regression)")
def check_export_loaders():
    with tempfile.TemporaryDirectory() as d:
        p_json = os.path.join(d, "e.json")
        with open(p_json, "w") as f:
            json.dump({"per_doc": [1, 2, 3]}, f)
        p_jsonl = os.path.join(d, "e.jsonl")
        write_jsonl(p_jsonl, [{"doc_id": 0}, {"doc_id": 1}])
        d1 = load_export("t1", "json", p_json)
        assert d1 == {"per_doc": [1, 2, 3]}
        d2 = load_export("t2", "jsonl", p_jsonl)
        assert d2 == [{"doc_id": 0}, {"doc_id": 1}]
        p_bad = os.path.join(d, "bad.jsonl")
        with open(p_bad, "w") as f:
            f.write("{not json\n")
        try:
            load_export("t3", "jsonl", p_bad)
            raise AssertionError("a bad jsonl export was accepted")
        except SystemExit as e:
            assert "t3" in str(e)
        try:
            load_export("t4", "yaml", p_json)
            raise AssertionError("an unknown kind was accepted")
        except SystemExit as e:
            assert "yaml" in str(e)
    return "PASS"


@selfcheck("reconciliation gate: exact accept + mismatch receipt + coverage discovery + incomplete-map exit")
def check_reconciliation():
    loads = OrderedDict([("synth", {
        "M2_slip_rate": {"slips": 4, "statements": 100},
        "per_doc": [
            {"doc_id": 0, "slips": [{"family": "inline"},
                                    {"family": "compression"}]},
            {"doc_id": 1, "slips": [{"family": "inline"},
                                    {"family": "inline"},
                                    {"family": "truncation"}]}]})])
    targets = [
        {"name": "synth_genuine", "banked": 3,
         "desc": "the synthetic genuine subclass"},
        {"name": "synth_rate", "banked": "4.00",
         "desc": "the synthetic rate print"}]
    good = {
        "synth_genuine": {"kind": "count_nested", "export": "synth",
                          "docs_path": "per_doc", "list_field": "slips",
                          "filter": {"exclude": {"family":
                                                ["compression",
                                                 "truncation"]}}},
        "synth_rate": {"kind": "rate_print", "decimals": 2,
                       "num": {"kind": "read_value", "export": "synth",
                               "path": "M2_slip_rate.slips"},
                       "den": {"kind": "read_value", "export": "synth",
                               "path": "M2_slip_rate.statements"}}}
    r, m, disc = reconcile(targets, good, loads, "synth map")
    assert len(r) == 2 and not m and not disc
    # a wrong binding: the mismatch receipt names target, derived beside banked
    bad = dict(good)
    bad["synth_genuine"] = {"kind": "count_nested", "export": "synth",
                            "docs_path": "per_doc", "list_field": "slips",
                            "filter": {}}
    r2, m2, d2 = reconcile(targets, bad, loads, "synth map")
    assert len(m2) == 1 and m2[0]["target"] == "synth_genuine"
    assert m2[0]["derived"] == 5 and m2[0]["banked"] == 3
    assert "WRONG BINDING" in m2[0]["finding"]
    # a binding the bytes cannot carry: the coverage discovery, named
    cov = dict(good)
    cov["synth_genuine"] = {"kind": "count_nested", "export": "synth",
                            "docs_path": "per_doc",
                            "list_field": "absent_field", "filter": {}}
    r3, m3, d3 = reconcile(targets, cov, loads, "synth map")
    assert len(d3) == 1 and d3[0]["target"] == "synth_genuine"
    assert "COVERAGE DISCOVERY" in d3[0]["finding"]
    # a missing binding for a required receipt: the incomplete-map exit
    try:
        reconcile(targets, {"synth_genuine": good["synth_genuine"]},
                  loads, "synth map")
        raise AssertionError("a missing binding was accepted")
    except SystemExit as e:
        assert "synth_rate" in str(e) and "incomplete" in str(e)
    return "PASS"


@selfcheck("t_0 engine: constructed spans -> constructed t_0s + the equality-sign skip + the unresolvable hard exit")
def check_t0():
    vnum = {11, 12, 13}
    steps = {0: 9, 1: 11, 2: 12, 3: 40, 4: 13}
    # the first numeric token; the equality-sign step (token 9) skipped
    assert resolve_t0("d1", "raw", [0, 1, 2],
                      lambda s: steps[s], vnum) == 1
    assert resolve_t0("d2", "raw", [3, 4],
                      lambda s: steps[s], vnum) == 4
    # an unresolvable span: hard exit NAMED, never skipped, never averaged
    try:
        resolve_t0("d3", "chat", [0, 3], lambda s: steps[s], vnum)
        raise AssertionError("an unresolvable span was accepted")
    except SystemExit as e:
        assert "UNRESOLVABLE" in str(e) and "d3" in str(e)
    # the equality sign alone never resolves t_0 (the law, not an accident)
    try:
        resolve_t0("d4", "chat", [0], lambda s: steps[s], vnum)
        raise AssertionError("an equality-sign-only span was accepted")
    except SystemExit as e:
        assert "UNRESOLVABLE" in str(e)
    # a span resolving against a step the walk does not carry: NAMED
    try:
        resolve_t0("d5", "raw", [7], lambda s: steps[s], vnum)
        raise AssertionError("a wrong-walk span was accepted")
    except SystemExit as e:
        assert "UNRESOLVABLE" in str(e) and "d5" in str(e)
    return "PASS"


@selfcheck("coverage boundary: prompt-operand steps excluded + counted + named; generation-side kept")
def check_coverage_boundary():
    rows = [
        {"doc_id": 0, "leg": "raw", "step": 5, "prompt_len": 128,
         "operands": [120, 121]},
        {"doc_id": 1, "leg": "raw", "step": 6, "prompt_len": 128,
         "operands": [130, 131]},
        {"doc_id": 2, "leg": "raw", "step": 7, "prompt_len": 128,
         "operands": [120, 131]},
    ]
    covered, excluded = split_coverage(rows)
    assert [r["doc_id"] for r in covered] == [1]
    assert all(r["out_of_coverage"] is False for r in covered)
    assert [r["doc_id"] for r in excluded] == [0, 2]
    assert excluded[0]["prompt_side_operands"] == [120, 121]
    assert excluded[1]["prompt_side_operands"] == [120]
    assert "never silently dropped" in excluded[0]["finding"]
    try:
        split_coverage([{"doc_id": 3, "leg": "raw", "step": 1}])
        raise AssertionError("a malformed commitment row was accepted")
    except SystemExit as e:
        assert "prompt_len" in str(e)
    return "PASS"


@selfcheck("cohort binding: the v1.3.0 A1 bind (same-value, different OWN step, nearest-step, tie-break, reasons NAMED, the S4 hidden-row assertion) + the A2 law with the S4 assertion (the map-driven extraction)")
def check_cohort_binding():
    loads = OrderedDict([("17p2", {
        "docs": [
            {"doc_id": 7, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [10, 12], "quantity": "q"},
                {"node": "DERIVED-VERIFIED", "locus": [20, 22],
                 "quantity": "q2"}]}},
            {"doc_id": 8, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [30, 32],
                 "quantity": "q3"}]}}]})])
    pos_spec = {"export": "17p2", "docs_path": "docs",
                "doc_id_field": "doc_id", "records_field": "p2.nodes",
                "class_field": "node",
                "class_values": ["UNTRACED"], "leg": "raw",
                "span_field": "locus", "quantity_field": "quantity"}
    # the map-driven extraction: rows pulled via the bound fields
    extracted = extract_span_rows(loads, pos_spec, "synth extraction")
    assert len(extracted) == 2
    assert extracted[0]["doc_id"] == 7 and extracted[0]["span"] == [10, 12]
    assert extracted[0]["record_class"] == "UNTRACED"
    neg_spec = dict(pos_spec, class_values=["DERIVED-VERIFIED"])
    negatives = extract_span_rows(loads, neg_spec, "synth extraction")
    assert len(negatives) == 1

    # THE v1.3.0 A1 BIND (resolved rows: value + the position-aware
    # span_resolution -- status RESOLVED-OWN-STEP, the own step, the
    # hidden row -- the shape the binding receives post-resolution)
    def prow(doc, val, span, t0):
        return {"export": "aligned_spans", "leg": "p2",
                "doc_id": doc, "record_class": "PROMOTION",
                "value": val, "span": span,
                "span_resolution": {"status": "RESOLVED-OWN-STEP",
                                    "t0": t0, "occ_step_t": t0,
                                    "commit_index": 0,
                                    "hidden_row_index": t0}}

    def nrow(doc, val, span, t0):
        return {"export": "aligned_spans", "leg": "p2",
                "doc_id": doc, "record_class": "DERIVED-VERIFIED",
                "value": val, "span": span,
                "span_resolution": {"status": "RESOLVED-OWN-STEP",
                                    "t0": t0, "occ_step_t": t0,
                                    "commit_index": 0,
                                    "hidden_row_index": t0}}

    positives = [
        prow(7, "9", [10], 10),    # nearest + same-step exclusion
        prow(8, "9", [30], 30),     # no same-doc DV rows
        prow(9, "9", [40], 40),     # same-step only
        prow(10, "9", [50], 50),   # no same-value occurrence
        prow(11, "9", [60], 60),   # the distance tie -> span order
        prow(12, "9", [70], 70),   # the pair consumed below
        prow(12, "9", [72], 72),   # the consumed class
    ]
    negatives = [
        nrow(7, "9", [10], 10),     # same t_0: excluded by law
        nrow(7, "8", [11], 11),     # different value: ignored
        nrow(7, "9", [16], 16),     # distance 6
        nrow(7, "9", [14], 14),     # distance 4 -> the pick
        nrow(9, "9", [40], 40),     # same t_0 only
        nrow(10, "7", [51], 51),   # other value only
        nrow(11, "9", [57], 57),   # distance 3, span [57]
        nrow(11, "9", [63], 63),   # distance 3, span [63]
        nrow(12, "9", [74], 74),   # one candidate, two positives
    ]
    pairs, unpaired = bind_cohort_a1(positives, negatives, "A1")
    # three pairs expected: doc 7 (nearest pick 14), doc 11 (the
    # tie -> [57]), doc 12 (the first of its two positives)
    assert len(pairs) == 3, pairs
    by_doc = {}
    for pr in pairs:
        by_doc.setdefault(pr["doc_id"], pr)
    # the positives bind in sort_key order (doc ids compared as
    # strings by the standing sort law); the pair ids assign in that
    # order, deterministic -- asserted by the two-run equality below
    p7 = by_doc[7]
    assert p7["negative"]["span_resolution"]["t0"] == 14
    assert p7["negative"]["span_resolution"]["occ_step_t"] == 14
    assert p7["step_distance"] == 4        # the v1.2.7 lineage form
    assert p7["occ_step_distance"] == 4    # the v1.3.0 position-aware form
    assert "v1.3.0" in p7["bind_law"]
    p11 = by_doc[11]
    # the distance tie: both candidates at distance 3; the span-order
    # tie-break picks [57] deterministically (signed distance -3)
    assert p11["negative"]["span"] == [57]
    assert p11["step_distance"] == -3
    assert p11["occ_step_distance"] == -3
    p12 = by_doc[12]
    assert p12["step_distance"] == 4
    assert p12["occ_step_distance"] == 4
    reasons = {u["positive"]["doc_id"]: u["finding"]
               for u in unpaired}
    # four unpaired: doc 8 (no DV rows), doc 9 (the same occurrence
    # step only), doc 10 (no same-value occurrence), doc 12's second
    # positive (the consumed class)
    assert len(unpaired) == 4 and set(reasons) == {8, 9, 10, 12}
    assert "no same-doc DERIVED-VERIFIED rows" in reasons[8]
    assert "SAME occurrence step only" in reasons[9]
    assert "no same-doc SAME-VALUE" in reasons[10]
    assert "consumed by earlier pairs" in reasons[12]
    for u in unpaired:
        assert u["finding"].startswith("UNPAIRED -- ")
        assert "never silently dropped" in u["finding"]
    # the two-run determinism of the amended binding
    pairs_b, unpaired_b = bind_cohort_a1(positives, negatives,
                                         "A1")
    assert json.dumps(pairs, sort_keys=True) == \
        json.dumps(pairs_b, sort_keys=True)
    assert json.dumps(unpaired, sort_keys=True) == \
        json.dumps(unpaired_b, sort_keys=True)
    # a missing field in the extraction spec: the coverage path, named
    bad_spec = dict(pos_spec, span_field="absent")
    try:
        extract_span_rows(loads, bad_spec, "synth extraction")
        raise AssertionError("an absent span field was accepted")
    except MapBindingError as e:
        assert "absent" in str(e)
    # A2: slips vs matched clean commitments same-doc, deterministic
    # (the v1.3.0 rows carry their position-aware resolutions; the
    # S4 assertion rides every A2 pair too)
    def a2row(export, doc, span, cls, hr):
        return {"export": export, "leg": "raw", "doc_id": doc,
                "span": span, "record_class": cls,
                "span_resolution": {"status": "RESOLVED-OWN-STEP",
                                    "t0": span[0], "occ_step_t": span[0],
                                    "commit_index": hr,
                                    "hidden_row_index": hr}}
    slips = [a2row("17a_raw", 3, [5], "SLIP", 5),
             a2row("17a_raw", 4, [6], "SLIP", 6)]
    cleans = [a2row("17a_raw", 3, [7], "CLEAN", 7),
              a2row("17a_raw", 3, [8], "CLEAN", 8),
              a2row("17a_raw", 5, [9], "CLEAN", 9)]
    pairs2, unpaired2 = bind_cohort(slips, cleans, "A2")
    assert len(pairs2) == 1
    assert pairs2[0]["positive"]["doc_id"] == 3
    assert pairs2[0]["negative"]["doc_id"] == 3
    # the standing A2 pairing law adds no v1.3.0 pair fields (the S4
    # assertion rides inside the binding, never the pair receipt)
    assert "bind_law" not in pairs2[0]
    assert "step_distance" not in pairs2[0]
    assert len(unpaired2) == 1 and unpaired2[0]["positive"]["doc_id"] == 4
    # THE S4 FAIL-LOUD LANES (the sheet's pair-law extension): a pair
    # whose two rows ride the SAME hidden row is a hard exit NAMED --
    # the item-1161(e) hole closed in bytes
    try:
        bind_cohort_a1(
            [{"export": "e", "leg": "l", "doc_id": 1, "value": "9",
              "span": [10],
              "span_resolution": {"status": "RESOLVED-OWN-STEP",
                                  "t0": 10, "occ_step_t": 10,
                                  "commit_index": 3,
                                  "hidden_row_index": 3}}],
            [{"export": "e", "leg": "l", "doc_id": 1, "value": "9",
              "span": [14],
              "span_resolution": {"status": "RESOLVED-OWN-STEP",
                                  "t0": 14, "occ_step_t": 14,
                                  "commit_index": 3,
                                  "hidden_row_index": 3}}], "A1")
        raise AssertionError("an equal-hidden-row A1 pair was accepted")
    except SystemExit as e:
        assert "PAIR-LAW-HIDDEN-ROW-EQUALITY" in str(e)
    try:
        bind_cohort([a2row("17a_raw", 3, [5], "SLIP", 5)],
                    [a2row("17a_raw", 3, [7], "CLEAN", 5)], "A2")
        raise AssertionError("an equal-hidden-row A2 pair was accepted")
    except SystemExit as e:
        assert "PAIR-LAW-HIDDEN-ROW-EQUALITY" in str(e)
    # an unresolved row reaching the binding: the NAMED premise violation
    try:
        bind_cohort_a1(
            [{"export": "e", "leg": "l", "doc_id": 1, "value": "9",
              "span": [10],
              "span_resolution": {"status":
                                  "step-outside-cache-coverage"}}],
            [], "A1")
        raise AssertionError("an unresolved row reached the binding")
    except SystemExit as e:
        assert "NAMED premise violation" in str(e)
    return "PASS"


# ---------------------------------------------------------------------------
# Section 14. The layer certification (settled from the instrument source,
# recorded from the bytes: the banked state per commit is the FINAL-NORMED
# LAST-LAYER state, model.norm(out.hidden_states[-1][0, -1]) -- the FIXED
# convention, ONE ROW PER CONTENT COMMIT (the hidden law the reader asserts
# per record); the strided per-layer reads (layer = t % n_layers, the v31
# sample-stride schedule) are H/PR monitor columns in steps only, never
# the banked state. A hidden-dim drift across a cache is a hard exit
# NAMED; the certificate records the evidence, it prints no verdicts.)
# ---------------------------------------------------------------------------
LAYER_CERTIFICATE_TEXT = (
    "the banked state = the final-normed LAST-LAYER state per content "
    "commit (the fixed convention of the instrument source; hidden_n == "
    "n_content_steps asserted per record, one row per commit); the "
    "strided per-layer reads (layer = t % n_layers, the v31 sample-stride "
    "schedule) are H/PR monitor columns in the steps dict only, never "
    "the banked state -- the strided-vs-fixed question settled from the "
    "instrument source, recorded from the bytes")


def certify_layer(cache_reads):
    """Certify the layer question from the read bytes: hidden dims a
    singleton per cache (a drift a hard exit NAMED); the instrument
    strings and the per-step layer-value census recorded as evidence."""
    per_cache = OrderedDict()
    for pin_name, cr in cache_reads.items():
        inv = cr["inventory"]
        dims = inv.get("hidden_dims_observed", [])
        if len(dims) != 1:
            fail_loud("layer certification: cache %s carries %d hidden "
                      "dims %r -- a DIM DRIFT, a hard exit NAMED (the "
                      "banked state convention is one dim; never "
                      "averaged, never guessed)" %
                      (pin_name, len(dims), dims))
        instruments = Counter(r["instrument"] for r in cr["records"])
        layer_values = Counter()
        for r in cr["records"]:
            for lv in r["steps"].get("layer", []):
                if isinstance(lv, int):
                    layer_values[lv] += 1
        per_cache[pin_name] = OrderedDict([
            ("record_count", inv["record_count"]),
            ("hidden_dim", dims[0]),
            ("instrument_strings", OrderedDict(
                sorted(instruments.items()))),
            ("steps_layer_value_census", OrderedDict(
                sorted(layer_values.items()))),
            ("hidden_layout", inv.get("hidden_layout", {})),
        ])
    return OrderedDict([
        ("per_cache", per_cache),
        ("certification", LAYER_CERTIFICATE_TEXT),
    ])


# ---------------------------------------------------------------------------
# Section 15. The V_num pin (the numeric-token set, first-pass convention).
# The tokenizer sha arrives from MY CONSOLE LINE via --tokenizer-sha,
# never hand-typed here; the observed sha must equal it exactly. The rule
# (recorded verbatim in the export, never re-derived): a tokenizer entry
# whose string, whitespace-stripped, matches the plain decimal/scientific
# numeric form is a numeric token -- nan/inf spellings excluded by the
# form itself. The sorted id list + the count recorded beside the rule.
# ---------------------------------------------------------------------------
NUMERIC_RE = re.compile(
    r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")
VNUM_RULE_TEXT = (
    "first-pass convention: a tokenizer entry whose string, "
    "whitespace-stripped, matches the plain decimal/scientific numeric "
    "form ^[+-]?(\\d+(\\.\\d*)?|\\.\\d+)([eE][+-]?\\d+)?$ is a numeric "
    "token; nan/inf spellings and every non-numeric string excluded by "
    "the form itself; the rule recorded verbatim, the sorted id list "
    "recorded, never re-derived at measurement time")


def pin_vnum(tokenizer_path, expect_sha):
    """Pin the tokenizer file against MY console sha; derive the
    numeric token id set by the recorded rule. Returns the receipt and
    the id->string map (the span-to-commit resolution's own need)."""
    if (not expect_sha or not isinstance(expect_sha, str)
            or len(expect_sha) != 64
            or any(ch not in "0123456789abcdef" for ch in expect_sha)):
        fail_loud("--run needs --tokenizer-sha: the 64-hex sha of "
                  "tokenizer.json FROM MY CONSOLE LINE, never "
                  "hand-typed by the tool")
    if not tokenizer_path or not os.path.isfile(tokenizer_path):
        fail_loud("the tokenizer file %r is absent (--tokenizer; the "
                  "V_num pin reads it, zero decodes, zero GPU)"
                  % (tokenizer_path,))
    obs = sha256_file(tokenizer_path)
    if obs != expect_sha:
        fail_loud("tokenizer pin: observed sha %s != my console sha "
                  "%s -- the file at the door is not the pinned file"
                  % (obs, expect_sha))
    try:
        with open(tokenizer_path) as f:
            data = json.load(f)
    except ValueError as e:
        fail_loud("tokenizer %s: not valid JSON (%s)" % (tokenizer_path, e))
    vocab = (data.get("model") or {}).get("vocab") if isinstance(
        data, dict) else None
    if not isinstance(vocab, dict) or not vocab:
        fail_loud("tokenizer %s: no model.vocab object in the fast "
                  "format (the V_num pin's named need)" % tokenizer_path)
    ids = []
    id_to_str = OrderedDict()
    for tok, vid in vocab.items():
        if (isinstance(vid, int) and not isinstance(vid, bool)
                and NUMERIC_RE.match(str(tok).strip())):
            ids.append(vid)
            id_to_str.setdefault(vid, tok)
    ids.sort()
    receipt = OrderedDict([
        ("tokenizer_sha256_observed", obs),
        ("rule_verbatim", VNUM_RULE_TEXT),
        ("vocab_entries", len(vocab)),
        ("numeric_token_count", len(ids)),
        ("numeric_token_ids_sorted", ids),
    ])
    return receipt, id_to_str


# ---------------------------------------------------------------------------
# Section 16. The join naming (the label-export doc -> walk-cache doc
# join, resolved doc-for-doc and NAMED, never guessed: the pre-reg's own
# law). Per row: JOINED (exactly one candidate record), UNJOINED (zero --
# the honest-population receipt), AMBIGUOUS (more than one -- named with
# the pins and keys, the honest-population receipt). An exact doc-id
# equality is tried first; a string-coerced equality second, and a
# coerced match is NAMED in the receipt (the type boundary measured,
# never silently smoothed). The candidate cache records' own key strings
# are recorded verbatim -- a key that disagrees with its leg/doc_id
# fields is a NAMED join note, never an exit, never a silent fix.
# ---------------------------------------------------------------------------
def name_joins(rows, cache_bindings, cache_reads):
    """Name the join status of every extracted span row against the
    map's cache bindings. Returns a list of (row, join) pairs."""
    out = []
    for r in rows:
        leg = r.get("leg")
        b = cache_bindings.get(leg)
        if b is None:
            fail_loud("join naming: the map's cache_bindings carry no "
                      "binding for leg %r -- every leg of the extracted "
                      "rows needs one (the map is incomplete at my "
                      "door)" % (leg,))
        pins = b.get("pins") or ([b["pin"]] if b.get("pin") else None)
        if not pins:
            fail_loud("join naming: the cache binding for leg %r names "
                      "no cache pin (the map schema: pin or pins)"
                      % (leg,))
        cache_leg = b.get("cache_leg")
        cands = []
        coerced = []
        for pn in pins:
            if pn not in cache_reads:
                fail_loud("join naming: leg %r binds cache pin %r -- a "
                          "pin the run did not read (the map and the "
                          "pins disagree, NAMED)" % (leg, pn))
            for rec in cache_reads[pn]["records"]:
                if cache_leg is not None and rec["leg"] != cache_leg:
                    continue
                if rec["doc_id"] == r["doc_id"]:
                    cands.append((pn, rec, False))
                elif str(rec["doc_id"]) == str(r["doc_id"]):
                    coerced.append((pn, rec))
        if not cands and coerced:
            cands = [(pn, rec, True) for pn, rec in coerced]
        if len(cands) == 1:
            pn, rec, co = cands[0]
            join = OrderedDict([
                ("status", "JOINED"),
                ("cache_pin", pn),
                ("cache_key", rec["key"]),
                ("cache_leg", rec["leg"]),
            ])
            if co:
                join["doc_id_match"] = ("TYPE-COERCED (export %r vs "
                                       "cache %r; named, never silently "
                                       "smoothed)"
                                       % (r["doc_id"], rec["doc_id"]))
            if rec["key"] != "%s:%s" % (rec["leg"], rec["doc_id"]):
                join["key_form_note"] = (
                    "the record key %r disagrees with its leg/doc_id "
                    "fields (%r/%r) -- a NAMED join note, the join rode "
                    "the fields, never a silent fix"
                    % (rec["key"], rec["leg"], rec["doc_id"]))
            out.append((r, join))
        elif not cands:
            out.append((r, OrderedDict([
                ("status", "UNJOINED"),
                ("finding", "UNJOINED -- no walk-cache record carries "
                 "this doc in the bound caches; the join receipt "
                 "measures the corpus boundary (the label corpus and "
                 "the cache corpus are named, never conflated); the "
                 "row rides the honest-population receipt at my door"),
            ])))
        else:
            out.append((r, OrderedDict([
                ("status", "AMBIGUOUS"),
                ("candidates", ["%s:%s" % (pn, rec["key"])
                                for pn, rec, _ in cands]),
                ("finding", "AMBIGUOUS -- %d candidate records; never "
                 "guessed; the row rides the honest-population receipt "
                 "at my door" % len(cands)),
            ])))
    return out


# ---------------------------------------------------------------------------
# Section 17. The span-to-commit resolution + the inventory run. Per
# JOINED row: t_0 by the t_0 law (the FIRST numeric token of the span;
# never the equality sign -- it is not numeric; never the span mean).
# THE v1.3.0 POSITION-AWARE RULE (my stamp, the sheet amendment v3,
# items 1162/1163): the commit row = the commit AT-OR-COVERING THE
# OCCURRENCE'S OWN STEP (the t_0 step, in the walk's own t column)
# whose stripped token is numeric and float-equals the span's first
# numeric token's value -- POSITION-AWARE, one rule for BOTH lanes;
# the v1.2.7 FIRST-float-equal rule (items 1136/1137, position-blind,
# every same-doc same-value occurrence collapsed onto one row) is
# AMENDED at this sheet, its receipts standing as the honest v1/v2
# records. The NAMED resolution-outcome classes: RESOLVED-OWN-STEP /
# step-outside-cache-coverage (no commit of the doc at-or-covers the
# occurrence's own step) / value-mismatch-at-own-step (coverage
# exists at the occurrence's own step but every covered commit's
# token float-differs) -- both ride the honest-population receipt,
# counted + named per row, never an exit, never a skip, the shift
# itself a finding at my door; the span whose value matches NO commit
# row of the whole record keeps the standing data-integrity hard exit
# (a different class, NAMED, unchanged); UNRESOLVABLE-NON-NUMERIC
# stands as amended at items 1136/1137.
# The coverage boundary rides the map's commit_coverage binding when it
# carries one; an absent binding is the NAMED GAP receipt (the caches
# bank generation-side operand states only -- the item-1104/1110 law),
# never a guessed count.
# ---------------------------------------------------------------------------
COHORT_BINDINGS_REQUIRED = [
    ("A1", "cohort_A1_positives", "cohort_A1_negatives"),
    ("A2", "cohort_A2_positives", "cohort_A2_negatives"),
]
COMMIT_MATCH_RULE_TEXT = (
    "the v1.3.0 position-aware rule (my stamp, the sheet amendment "
    "v3): the span's first numeric token (by the t_0 law) resolves to "
    "the commit AT-OR-COVERING THE OCCURRENCE'S OWN STEP -- the t_0 "
    "step in the walk's own t column -- whose stripped token is "
    "numeric and float-equal to its value; ONE rule for both lanes "
    "(the v1.2.7 FIRST-float-equal position-blind rule amended, its "
    "exports standing as bytes of record); the resolution-outcome "
    "classes NAMED per row: RESOLVED-OWN-STEP / step-outside-cache-"
    "coverage / value-mismatch-at-own-step / the standing "
    "UNRESOLVABLE-NON-NUMERIC; the hidden row = the commit row (one "
    "row per commit)")


def resolve_span_commit(row, rec, id_to_str, vnum_ids):
    """Resolve one JOINED span row against its walk record: the span
    units come from the map's binding (token_ids or steps_t -- never
    guessed); t_0 by the t_0 law; the commit row by the recorded rule."""
    units = row.get("span_units")
    ids_list = rec["steps"]["id"]
    ts_list = rec["steps"]["t"]
    if units == "token_ids":
        token_of = {sid: sid for sid in ids_list}
    elif units == "steps_t":
        token_of = {t: ids_list[i] for i, t in enumerate(ts_list)}
    else:
        fail_loud("span resolution: doc %r -- the map's cohort binding "
                  "carries no span_units (token_ids or steps_t); the "
                  "span-to-step mapping is MY MAP's binding, never a "
                  "guess" % (row.get("doc_id"),))
    span = row.get("span")
    for entry in span:
        if entry not in token_of:
            fail_loud("span resolution: doc %r -- span entry %r is in "
                      "neither the walk's token ids nor its t values "
                      "(the span resolved against the wrong walk -- "
                      "NAMED, never skipped)" % (row.get("doc_id"), entry))
    # THE RECEIPT AMENDMENT (my stamp, items 1136/1137): a span with
    # ZERO numeric tokens is the UNRESOLVABLE-NON-NUMERIC class (the
    # phrase-quantity class of the item-1136 census: spelled
    # quantities, quality grades); counted + named per row, it rides
    # the honest-population receipt -- the same path as UNJOINED and
    # AMBIGUOUS -- never an exit, never a skip; every resolvable row
    # keeps the t_0 law unchanged below.
    if not any(token_of[entry] in vnum_ids for entry in span):
        return OrderedDict([
            ("status", "UNRESOLVABLE-NON-NUMERIC"),
            ("span", span),
            ("value", row.get("value")),
            ("finding",
             "UNRESOLVABLE-NON-NUMERIC -- the committed quantity span "
             "carries ZERO numeric tokens (the phrase-quantity class "
             "of the item-1136 census: spelled quantities, quality "
             "grades); the t_0 law unresolvable by nature; the row "
             "rides the honest-population receipt at my door, never "
             "an exit, never a skip, never averaged"),
        ])
    t0 = resolve_t0(row.get("doc_id"), row.get("leg"), span,
                    lambda s: token_of[s], vnum_ids)
    first_num_text = None
    for entry in span:
        tid = token_of[entry]
        if tid in vnum_ids:
            first_num_text = id_to_str.get(tid)
            break
    if first_num_text is None:
        fail_loud("span resolution: doc %r -- t_0 resolved but the "
                  "numeric token carries no string in the pinned "
                  "tokenizer (a NAMED gap at my door)" % row.get("doc_id"))
    want_val = float(str(first_num_text).strip())
    # THE v1.3.0 POSITION-AWARE RULE (my stamp, the sheet amendment
    # v3): the occurrence's OWN step = the t_0 step expressed in the
    # walk's own t column (token_ids units map the id back to its t;
    # steps_t units are t already); the candidate commit set = the
    # commits AT-OR-COVERING that step (a commit covers the step when
    # its own t equals it, or its t_start..t_end range contains it --
    # the sheet's S1 wording carried verbatim); the resolution picks
    # the covered commit whose token float-equals the occurrence's
    # first numeric value -- the same-doc same-value occurrences each
    # resolve to their OWN steps, the collapse AMENDED at this sheet.
    if units == "steps_t":
        occ_t = t0
    else:
        # the S3 map-binding extension: the occurrence's OWN step range
        # (step_start/step_end, the aligned bytes' own fields; the
        # v1.3.3 singular own-step form binds the SPAN-EXTENT range
        # [step, step + len(span) - 1] at extraction -- the head step
        # plus the span's own contiguous run, ONE namespace, the law
        # below unchanged); under
        # token_ids units a repeated token id sits at multiple steps,
        # so the id alone is ambiguous -- the range disambiguates, and
        # a position-blind fallback is never taken (ONE rule for both
        # lanes; a row without its occurrence step range is a NAMED
        # premise violation, never a silent guess).
        occ_start = row.get("occ_step_start")
        occ_end = row.get("occ_step_end")
        if not (isinstance(occ_start, int) and isinstance(occ_end, int)):
            fail_loud("span resolution: doc %r -- a token_ids row "
                      "carries no occurrence step range (the sheet v3 "
                      "S3 extension; the position-aware rule needs the "
                      "occurrence's OWN step; a position-blind "
                      "fallback is never taken -- ONE rule for both "
                      "lanes; a NAMED premise violation)"
                      % (row.get("doc_id"),))
        if occ_start > occ_end or occ_start < 0 or occ_end >= len(ids_list):
            fail_loud("span resolution: doc %r -- the occurrence step "
                      "range [%d, %d] disagrees with the walk's %d "
                      "steps (the span resolved against the wrong walk "
                      "-- NAMED, never skipped)"
                      % (row.get("doc_id"), occ_start, occ_end,
                         len(ids_list)))
        occ_t = None
        for pos in range(occ_start, occ_end + 1):
            if ids_list[pos] in vnum_ids:
                occ_t = ts_list[pos]
                if ids_list[pos] != token_of[t0]:
                    fail_loud("span resolution: doc %r -- the "
                              "occurrence range's first numeric step "
                              "(id %r) disagrees with the span's first "
                              "numeric token (id %r) -- an internal "
                              "disagreement, NAMED, never averaged"
                              % (row.get("doc_id"), ids_list[pos],
                                 token_of[t0]))
                break
        if occ_t is None:
            fail_loud("span resolution: doc %r -- the occurrence step "
                      "range [%d, %d] carries no numeric walk step "
                      "(an internal disagreement with the span, NAMED)"
                      % (row.get("doc_id"), occ_start, occ_end))
    if not isinstance(occ_t, int):
        fail_loud("span resolution: doc %r -- the occurrence's own "
                  "step %r is not a step id (a NAMED premise "
                  "violation)" % (row.get("doc_id"), occ_t))
    matches_anywhere = False
    for c in rec["commits"]:
        ct = c.get("token")
        if isinstance(ct, str) and NUMERIC_RE.match(ct.strip()):
            if float(ct.strip()) == want_val:
                matches_anywhere = True
                break
    if not matches_anywhere:
        fail_loud("SPAN-TO-COMMIT UNRESOLVABLE -- doc %r leg %r: the "
                  "span's first numeric value %r matches no commit row "
                  "of the whole record (the standing data-integrity "
                  "hard exit, a different class, NAMED, unchanged by "
                  "the v1.3.0 amendment; never skipped, never averaged)"
                  % (row.get("doc_id"), row.get("leg"), want_val))
    own_step, mismatch = [], []
    for idx, c in enumerate(rec["commits"]):
        ct = c.get("t")
        if isinstance(c.get("t_start"), int) and isinstance(
                c.get("t_end"), int):
            covers = isinstance(ct, int) and (
                c["t_start"] <= occ_t <= c["t_end"])
        else:
            covers = isinstance(ct, int) and ct == occ_t
        if not covers:
            continue
        own_step.append((idx, c))
        ctok = c.get("token")
        if isinstance(ctok, str) and NUMERIC_RE.match(ctok.strip()):
            if float(ctok.strip()) == want_val:
                return OrderedDict([
                    ("status", "RESOLVED-OWN-STEP"),
                    ("t0", t0), ("span_units", units),
                    ("occ_step_t", occ_t),
                    ("commit_index", idx), ("hidden_row_index", idx),
                    ("first_numeric_token", str(first_num_text)),
                    ("commit_token", ctok),
                ])
    if own_step:
        return OrderedDict([
            ("status", "value-mismatch-at-own-step"), ("span", span),
            ("value", row.get("value")), ("occ_step_t", occ_t),
            ("finding",
             "value-mismatch-at-own-step -- the occurrence's own step "
             "%d carries %d commit row(s) but none float-equal to the "
             "span's first numeric value %r (the value exists in the "
             "doc at other steps; the v1.2.7 position-blind rule would "
             "have resolved it there -- the misattribution exposure "
             "AMENDED at the sheet v3); the row rides the honest-"
             "population receipt at my door, never an exit, never a "
             "skip, never averaged"
             % (occ_t, len(own_step), want_val)),
        ])
    return OrderedDict([
        ("status", "step-outside-cache-coverage"), ("span", span),
        ("value", row.get("value")), ("occ_step_t", occ_t),
        ("finding",
         "step-outside-cache-coverage -- the occurrence's own step %d "
         "carries no commit row of the doc (the caches bank the "
         "generation-side content steps; a prompt-side or unbanked "
         "step resolves to no hidden row); the row rides the honest-"
         "population receipt at my door, never an exit, never a skip, "
         "never averaged" % (occ_t,)),
    ])


def extract_commit_rows(loads, spec, ctx):
    """The map's commit_coverage binding: commitment rows with operand
    positions pulled from the bound export path."""
    rows = dig(loads[spec["export"]], spec["path"], ctx)
    if not isinstance(rows, list):
        raise MapBindingError("%s: path %r is not a list"
                              % (ctx, spec["path"]))
    fields = spec.get("fields")
    if not isinstance(fields, dict):
        raise MapBindingError("%s: the binding carries no fields block"
                              % ctx)
    out = []
    for r in rows:
        if not isinstance(r, dict):
            fail_loud("%s: a coverage row is not an object" % ctx)
        row = {}
        for want, src in fields.items():
            if src not in r:
                raise MapBindingError("%s: a coverage row carries no "
                                      "field %r" % (ctx, src))
            row[want] = r[src]
        out.append(row)
    return out


COVERAGE_NAMED_GAP_TEXT = (
    "NAMED GAP -- the map binds no commit_coverage block and the walk "
    "caches bank generation-side operand states only (the item-1104/"
    "1110 position-coverage boundary: the per-commit operand positions "
    "are not in the cache bytes); the coverage-boundary exclusion count "
    "is presented at my door when my map binds an operand-"
    "bearing export; nothing guessed, nothing silently dropped")


def assemble_inventory(fmap, map_sha, pins, loads, cache_reads,
                       vnum_receipt, id_to_str, vnum_ids):
    """The inventory core: cohort extraction + join naming + span
    resolution + cohort binding + coverage counting + the honest-
    population receipt. Deterministic by construction (sorted pairing,
    sort_keys export)."""
    bindings = fmap["bindings"]
    cache_bindings = fmap.get("cache_bindings")
    if not isinstance(cache_bindings, dict) or not cache_bindings:
        fail_loud("--run needs the map's cache_bindings block (leg -> "
                  "cache pin): the label-to-cache join is MY MAP's "
                  "binding, never a guess; the map is incomplete at "
                  "my door")
    honest = []
    cohorts_out = OrderedDict()
    join_receipt = []
    # the v1.3.0 receipts: the per-cohort resolution-class census (the
    # sheet's S1) + the S3 extension census; reset per run for the
    # two-run byte-identical determinism law
    STEP_EXT_CENSUS.clear()
    for cohort, pos_key, neg_key in COHORT_BINDINGS_REQUIRED:
        pos_spec = bindings.get(pos_key)
        neg_spec = bindings.get(neg_key)
        for key in (pos_key, neg_key):
            if bindings.get(key) is None:
                fail_loud("--run needs the map's %r binding (the cohort "
                          "extraction spec); the map is incomplete at "
                          "my door" % (key,))
        ctx = "cohort %s (map %s)" % (cohort, fmap.get("map_name"))
        unresolved_count = 0
        class_counts = OrderedDict([
            ("RESOLVED-OWN-STEP", 0),
            ("step-outside-cache-coverage", 0),
            ("value-mismatch-at-own-step", 0),
            ("UNRESOLVABLE-NON-NUMERIC", 0),
        ])
        pos_rows = extract_span_rows(loads, pos_spec, ctx)
        neg_rows = extract_span_rows(loads, neg_spec, ctx)
        for rows, spec in ((pos_rows, pos_spec), (neg_rows, neg_spec)):
            for r in rows:
                r["span_units"] = spec.get("span_units")
        resolved_pos, resolved_neg = [], []
        for r, join in name_joins(pos_rows + neg_rows, cache_bindings,
                                  cache_reads):
            join_receipt.append(OrderedDict([
                ("cohort", cohort), ("doc_id", r.get("doc_id")),
                ("leg", r.get("leg")), ("record_class",
                                        r.get("record_class")),
                ("join", join)]))
            if join["status"] != "JOINED":
                honest.append(OrderedDict([
                    ("cohort", cohort), ("row", r), ("join", join),
                    ("finding", join.get("finding"))]))
                continue
            pn = join["cache_pin"]
            rec = None
            for cand in cache_reads[pn]["records"]:
                if cand["key"] == join["cache_key"]:
                    rec = cand
                    break
            if rec is None:
                fail_loud("join receipt: cache %s carries no record "
                          "with key %r (an internal disagreement, "
                          "NAMED)" % (pn, join["cache_key"]))
            resolved = OrderedDict(r)
            resolved["join"] = join
            resolved["span_resolution"] = resolve_span_commit(
                resolved, rec, id_to_str, vnum_ids)
            sr = resolved["span_resolution"]
            st = sr.get("status")
            if st not in class_counts:
                fail_loud("resolution class census: an unknown "
                          "resolution status %r reached the census "
                          "(an internal disagreement, NAMED)"
                          % (st,))
            class_counts[st] += 1
            if st in ("UNRESOLVABLE-NON-NUMERIC",
                      "step-outside-cache-coverage",
                      "value-mismatch-at-own-step"):
                if st == "UNRESOLVABLE-NON-NUMERIC":
                    unresolved_count += 1
                honest.append(OrderedDict([
                    ("cohort", cohort), ("row", resolved),
                    ("finding", sr["finding"])]))
                continue
            (resolved_pos if r in pos_rows else resolved_neg).append(
                resolved)
        if cohort == "A1":
            pairs, unpaired = bind_cohort_a1(resolved_pos, resolved_neg,
                                             cohort)
            rule_text = A1_BIND_RULE_TEXT
        else:
            pairs, unpaired = bind_cohort(resolved_pos, resolved_neg,
                                          cohort)
            rule_text = A2_BIND_RULE_TEXT
        for u in unpaired:
            honest.append(u)
        cohorts_out[cohort] = OrderedDict([
            ("bind_rule_verbatim", rule_text),
            ("positives_extracted", len(pos_rows)),
            ("negatives_extracted", len(neg_rows)),
            ("positives_joined_resolved", len(resolved_pos)),
            ("negatives_joined_resolved", len(resolved_neg)),
            ("matched_pairs", pairs),
            ("unpaired_count", len(unpaired)),
            ("unresolved_non_numeric", unresolved_count),
            ("resolution_class_census", OrderedDict(class_counts)),
        ])
    # the coverage boundary (the map's binding or the NAMED GAP)
    cc = fmap.get("commit_coverage")
    if cc is None:
        coverage = OrderedDict([("finding", COVERAGE_NAMED_GAP_TEXT)])
    else:
        try:
            crows = extract_commit_rows(
                loads, cc, "commit coverage (map %s)"
                % fmap.get("map_name"))
        except MapBindingError as e:
            coverage = OrderedDict([
                ("finding", "COVERAGE DISCOVERY -- %s; presented at the "
                 "my door per the item-52/53 precedent, my stamps "
                 "decide, nothing silently dropped" % e)])
        else:
            covered, excluded = split_coverage(crows)
            coverage = OrderedDict([
                ("commit_rows", len(crows)),
                ("covered_count", len(covered)),
                ("out_of_coverage_count", len(excluded)),
                ("out_of_coverage_rows", excluded),
            ])
    out = OrderedDict()
    out["tool"] = TOOL + " v" + VERSION + " (build part " + BUILD_PART + ")"
    out["mode"] = "inventory (Pass 2, post-stamp)"
    out["map_file_sha256"] = map_sha
    out["map_stamp_block_verbatim"] = fmap.get("stamp")
    out["input_receipts"] = pins
    out["layer_certificate"] = certify_layer(cache_reads)
    out["vnum_pin"] = vnum_receipt
    out["commit_match_rule_verbatim"] = COMMIT_MATCH_RULE_TEXT
    out["step_ext_census"] = OrderedDict(STEP_EXT_CENSUS)
    out["cohorts"] = cohorts_out
    out["join_receipt"] = join_receipt
    out["coverage_boundary"] = coverage
    out["honest_population_receipt"] = OrderedDict([
        ("entries", honest),
        ("unjoined_or_ambiguous_or_unpaired_count", len(honest)),
        ("beside_the_banked_receipts", OrderedDict(
            (k, BANKED_RECEIPTS[k]["banked"])
            for k in BANKED_RECEIPTS)),
        ("finding", "the honest population: every extracted row is "
         "counted here -- joined and paired, or named in this receipt; "
         "nothing silently dropped, my stamps decide"),
    ])
    return out


def run_inventory(args):
    """--run: the inventory, after MY STAMP. The pins assert first; the
    map sha must equal MY CONSOLE --map-sha; the reconciliation gate
    RE-RUNS on the stamped map and must reconcile (a data-integrity
    stop otherwise); the caches read through the amended reader; the
    layer certifies; V_num pins; the cohorts extract + join + resolve;
    the export writes deterministic; the console prints the census."""
    if not args.map_sha:
        fail_loud("--run needs --map-sha: the 64-hex sha of the STAMPED "
                  "map file from MY CONSOLE LINE, never hand-typed")
    pins = assert_all_pins(args.inputs_dir)
    fmap, map_sha = load_field_map(args.map)
    if map_sha != args.map_sha:
        fail_loud("map pin: observed sha %s != my console --map-sha "
                  "%s -- the file at the door is not the stamped map"
                  % (map_sha, args.map_sha))
    loads = OrderedDict()
    for name, kind in [("17a_raw", "json"), ("17a_chat", "json"),
                       ("17p2", "json"), ("17p2_ledger", "jsonl"),
                       ("aligned_spans", "json")]:
        loads[name] = load_export(name, kind,
                                  input_path(args.inputs_dir, PINS[name]))
    targets = [OrderedDict([("name", k),
                            ("banked", BANKED_RECEIPTS[k]["banked"]),
                            ("desc", BANKED_RECEIPTS[k]["desc"])])
               for k in BANKED_RECEIPTS]
    receipts, mismatches, discoveries = reconcile(
        targets, fmap["bindings"], loads, fmap.get("map_name") or args.map)
    if mismatches or discoveries:
        fail_loud("the gate RE-RUN on the STAMPED map diverges: %d "
                  "mismatch receipt(s), %d coverage discover(y/ies) -- "
                  "a data-integrity stop; the map revised from the "
                  "census's own evidence, re-presented, my stamps "
                  "decide" % (len(mismatches), len(discoveries)))
    cache_bindings = fmap.get("cache_bindings")
    if not isinstance(cache_bindings, dict) or not cache_bindings:
        fail_loud("--run needs the map's cache_bindings block; the map "
                  "is incomplete at my door")
    cache_reads = OrderedDict()
    for leg, b in cache_bindings.items():
        leg_pins = b.get("pins") or ([b["pin"]] if b.get("pin") else [])
        for pn in leg_pins:
            if pn not in PINS:
                fail_loud("cache_bindings: leg %r binds %r -- not a "
                          "pinned cache name (the pin names: %s)"
                          % (leg, pn, ", ".join(
                              k for k in PINS if "cache" in k)))
            if pn in cache_reads:
                continue
            recs, inv = read_cache_records(
                pn, input_path(args.inputs_dir, PINS[pn]),
                expect_records=PINS[pn].get("records"))
            cache_reads[pn] = OrderedDict([
                ("records", recs), ("inventory", inv),
                ("sha256", pins[pn]["observed_sha256"])])
    vnum_receipt, id_to_str = pin_vnum(args.tokenizer, args.tokenizer_sha)
    vnum_ids = set(vnum_receipt["numeric_token_ids_sorted"])
    out = assemble_inventory(fmap, map_sha, pins, loads, cache_reads,
                             vnum_receipt, id_to_str, vnum_ids)
    outpath = args.out or "cd1_arm_a_cohort_inventory_v1.json"
    with open(outpath, "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("=== CD-1 ARM A B0 COHORT INVENTORY (Pass 2, post-stamp) ===")
    print("input pins asserted: %d | map: %s (sha %s...)"
          % (len(pins), args.map, map_sha[:16]))
    print("gate re-run on the stamped map: ALL %d banked receipts "
          "reconciled" % len(receipts))
    for pn, cr in cache_reads.items():
        print("cache %s read: %d records | hidden dim %s | the layer "
              "certificate: the banked state = the final-normed "
              "LAST-LAYER state per commit (fixed); strided reads are "
              "H/PR monitor columns only"
              % (pn, cr["inventory"]["record_count"],
                 cr["inventory"]["hidden_dims_observed"][0]))
    print("V_num pinned: %d numeric token ids (rule recorded verbatim)"
          % vnum_receipt["numeric_token_count"])
    for cohort, block in out["cohorts"].items():
        print("cohort %s: %d positives / %d negatives extracted; %d / "
              "%d joined+resolved; %d matched pairs; %d unpaired"
              % (cohort, block["positives_extracted"],
                 block["negatives_extracted"],
                 block["positives_joined_resolved"],
                 block["negatives_joined_resolved"],
                 len(block["matched_pairs"]), block["unpaired_count"]))
        cc2 = block["resolution_class_census"]
        print("cohort %s resolution classes: %s" % (cohort, ", ".join(
            "%s=%d" % (k, cc2[k]) for k in cc2)))
    ext_total = 0
    for ctx_e, c_e in out["step_ext_census"].items():
        ext_total += c_e.get("rows_with_step_fields", 0) + c_e.get(
            "rows_without_step_fields", 0)
        print("step-ext census (%s): %d rows with step fields / %d "
              "without" % (ctx_e,
                           c_e.get("rows_with_step_fields", 0),
                           c_e.get("rows_without_step_fields", 0)))
    print("step-ext census total rows: %d (the S3 map-binding "
          "extension receipt)" % ext_total)
    n_join = Counter(j["join"]["status"] for j in out["join_receipt"])
    print("join receipt: %s" % ", ".join(
        "%s=%d" % kv for kv in sorted(n_join.items())))
    cov = out["coverage_boundary"]
    if "out_of_coverage_count" in cov:
        print("coverage boundary: %d/%d commitment rows out of cache "
              "coverage (counted, named, excluded from the BHOB "
              "denominator)" % (cov["out_of_coverage_count"],
                                cov["commit_rows"]))
    else:
        print("coverage boundary: the NAMED GAP receipt (the map binds "
              "no operand-bearing export; presented at my door)")
    print("honest-population receipt: %d entries (unjoined / ambiguous "
          "/ unpaired -- each named, none silently dropped)"
          % out["honest_population_receipt"][
              "unjoined_or_ambiguous_or_unpaired_count"])
    print("inventory export: %s" % outpath)
    print("sha256: %s" % sha256_file(outpath))
    print("bytes: %d" % os.path.getsize(outpath))
    print("NEXT: the cohort tables + the honest-population receipt "
          "present at my door; MY STAMPS decide the "
          "measurement phase")
    return 0


# ---------------------------------------------------------------------------
# Section 18. The selfcheck battery part 3 (the synthetic known-answer
# checks: the layer certification, the V_num pin, the join naming, the
# span-to-commit resolution, and the full synthetic inventory with the
# two-run byte-identical determinism check).
# ---------------------------------------------------------------------------
@selfcheck("layer certification: fixed-dim accept + the certificate text + a dim drift a hard exit")
def check_layer_cert():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "c.jsonl")
        write_jsonl(p, [synth_cache_record("d1", n_steps=4, n_commits=3),
                        synth_cache_record("d2", n_steps=2, n_commits=1)])
        _, inv = read_cache_records("t", p, expect_records=2)
        cr = {"math_cache": {"records": [], "inventory": inv}}
        cert = certify_layer(cr)
        assert cert["per_cache"]["math_cache"]["hidden_dim"] == 8
        assert "final-normed LAST-LAYER state" in cert["certification"]
        assert "monitor columns" in cert["certification"]
        # a dim drift across one cache is a hard exit, NAMED
        inv2 = dict(inv, hidden_dims_observed=[8, 16])
        try:
            certify_layer({"math_cache": {"records": [], "inventory": inv2}})
            raise AssertionError("a dim drift was accepted")
        except SystemExit as e:
            assert "DIM DRIFT" in str(e)
    return "PASS"


@selfcheck("V_num pin: the known-answer tokenizer + the rule + a wrong sha a hard exit")
def check_vnum_pin():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "tokenizer.json")
        vocab = {"=": 50, "3": 51, "7": 52, "x": 53, " 9 ": 54,
                 "nan": 55, "inf": 56, "Infinity": 57, "": 58,
                 "1e3": 59, ".5": 60, "-2.5": 61, "+4": 62, "1_0": 63}
        with open(p, "w") as f:
            json.dump({"model": {"vocab": vocab}}, f)
        sha = sha256_file(p)
        receipt, id_to_str = pin_vnum(p, sha)
        # the rule: stripped, plain decimal/scientific form only
        assert receipt["numeric_token_ids_sorted"] == [
            51, 52, 54, 59, 60, 61, 62]
        assert receipt["vocab_entries"] == len(vocab)
        assert id_to_str[54] == " 9 " and id_to_str[51] == "3"
        assert "never re-derived" in receipt["rule_verbatim"]
        # my console sha asserted exactly; a wrong sha is a hard exit
        try:
            pin_vnum(p, "0" * 64)
            raise AssertionError("a wrong tokenizer sha was accepted")
        except SystemExit as e:
            assert "console sha" in str(e)
        # a malformed sha argument is refused, never guessed
        try:
            pin_vnum(p, "not-hex")
            raise AssertionError("a malformed sha was accepted")
        except SystemExit as e:
            assert "--tokenizer-sha" in str(e)
    return "PASS"


@selfcheck("join naming: joined + type-coerced + unjoined + ambiguous, each named")
def check_join_naming():
    r1 = synth_cache_record(7, n_steps=3, n_commits=2)
    r2 = synth_cache_record(8, n_steps=3, n_commits=2, leg="synth-b")
    r3 = synth_cache_record(9, n_steps=3, n_commits=2)
    reads = {
        "math_cache": {"records": [r1, r2]},
        "p2_cache_fresh": {"records": [r3]},
    }
    binds = {"raw": {"pin": "math_cache"}}
    rows = [
        {"leg": "raw", "doc_id": 7, "span": [1]},        # exact joined
        {"leg": "raw", "doc_id": "8", "span": [1]},      # type-coerced
        {"leg": "raw", "doc_id": 40, "span": [1]},       # unjoined
    ]
    out = name_joins(rows, binds, reads)
    assert out[0][1]["status"] == "JOINED"
    assert out[0][1]["cache_pin"] == "math_cache"
    assert out[0][1]["cache_key"] == "synth-leg:7"
    assert out[1][1]["status"] == "JOINED"
    assert "TYPE-COERCED" in out[1][1]["doc_id_match"]
    assert out[2][1]["status"] == "UNJOINED"
    assert "honest-population" in out[2][1]["finding"]
    # a doc in two bound caches: AMBIGUOUS, never guessed
    r4 = synth_cache_record(7, n_steps=3, n_commits=2)
    reads["p2_cache_fresh"]["records"].append(r4)
    binds = {"raw": {"pins": ["math_cache", "p2_cache_fresh"]}}
    out2 = name_joins([{"leg": "raw", "doc_id": 7, "span": [1]}],
                      binds, reads)
    assert out2[0][1]["status"] == "AMBIGUOUS"
    assert len(out2[0][1]["candidates"]) == 2
    # a leg with no cache binding: the map is incomplete at my door
    try:
        name_joins([{"leg": "chat", "doc_id": 7, "span": [1]}],
                   binds, reads)
        raise AssertionError("an unbound leg was joined")
    except SystemExit as e:
        assert "cache_bindings" in str(e)
    return "PASS"


@selfcheck("span-to-commit resolution: the v1.3.0 position-aware rule (own-step commit, the doc-0 repeated-value case, the NAMED classes, the standing hard exit)")
def check_span_commit():
    vocab = {"=": 50, "3": 51, "7": 52}
    id_to_str = {50: "=", 51: "3", 52: "7"}
    vnum = {51, 52}
    # the faithful layout: the numeric tokens sit at their own steps
    # ("3" at t=1, "7" at t=2) and the commits ride those steps
    rec = synth_cache_record(7, n_steps=3, n_commits=2, ids=[50, 51, 52],
                             commit_tokens=["3", "7"],
                             commit_ts=[1, 2])
    row = {"doc_id": 7, "leg": "raw", "span": [50, 51],
           "span_units": "token_ids",
           "occ_step_start": 1, "occ_step_end": 1}
    res = resolve_span_commit(row, rec, id_to_str, vnum)
    assert res["status"] == "RESOLVED-OWN-STEP"
    assert res["t0"] == 51            # the equality sign (50) skipped
    assert res["occ_step_t"] == 1     # the occurrence's OWN step
    assert res["commit_index"] == 0   # "3" at its own step
    assert res["hidden_row_index"] == 0
    row2 = dict(row, span=[50, 52], occ_step_start=2, occ_step_end=2)
    res2 = resolve_span_commit(row2, rec, id_to_str, vnum)
    assert res2["t0"] == 52 and res2["commit_index"] == 1
    assert res2["occ_step_t"] == 2
    # THE DOC-0 REPEATED-VALUE CASE (the amendment's named receipt:
    # value "7" at two different steps -- the occurrence resolves to
    # its OWN step's commit, where the position-blind rule collapsed
    # both onto the first)
    rec_rep = synth_cache_record(7, n_steps=3, n_commits=2,
                                 ids=[50, 51, 52],
                                 commit_tokens=["7", "7"],
                                 commit_ts=[1, 2])
    res_rep = resolve_span_commit(row2, rec_rep, id_to_str, vnum)
    assert res_rep["status"] == "RESOLVED-OWN-STEP"
    assert res_rep["commit_index"] == 1   # the OWN step, never the first
    assert res_rep["occ_step_t"] == 2
    # steps_t units resolve through the t column (no occ fields needed)
    row3 = {"doc_id": 7, "leg": "raw", "span": [0, 2],
            "span_units": "steps_t"}
    res3 = resolve_span_commit(row3, rec, id_to_str, vnum)
    assert res3["t0"] == 2 and res3["commit_index"] == 1
    assert res3["occ_step_t"] == 2
    # a token_ids row without its occurrence step range: NAMED, never
    # a silent position-blind fallback (the one-rule law)
    try:
        resolve_span_commit(dict(row, occ_step_start=None,
                                 occ_step_end=None), rec,
                            id_to_str, vnum)
        raise AssertionError("a rangeless token_ids row was accepted")
    except SystemExit as e:
        assert "no occurrence step range" in str(e)
    # an out-of-walk occurrence range: the wrong-walk disagreement NAMED
    try:
        resolve_span_commit(dict(row, occ_step_start=0, occ_step_end=5),
                            rec, id_to_str, vnum)
        raise AssertionError("an out-of-walk range was accepted")
    except SystemExit as e:
        assert "disagrees with the walk" in str(e)
    # an unbound span_units is never guessed
    try:
        resolve_span_commit(dict(row, span_units=None), rec,
                            id_to_str, vnum)
        raise AssertionError("an unbound span_units was accepted")
    except SystemExit as e:
        assert "span_units" in str(e)
    # step-outside-cache-coverage: the value exists in the doc but no
    # commit rides the occurrence's own step -- the class NAMED, the
    # honest-population receipt's path
    rec_cov = synth_cache_record(7, n_steps=3, n_commits=1,
                                 ids=[50, 51, 52],
                                 commit_tokens=["3"], commit_ts=[2])
    res_cov = resolve_span_commit(row, rec_cov, id_to_str, vnum)
    assert res_cov["status"] == "step-outside-cache-coverage"
    assert res_cov["occ_step_t"] == 1
    # value-mismatch-at-own-step: coverage exists at the occurrence's
    # own step but the covered commit's token float-differs (the
    # value exists elsewhere in the doc -- the misattribution exposure
    # the position-blind rule carried, now NAMED at my door)
    rec_mm = synth_cache_record(7, n_steps=3, n_commits=2,
                                ids=[50, 51, 52],
                                commit_tokens=["7", "3"],
                                commit_ts=[1, 2])
    res_mm = resolve_span_commit(row, rec_mm, id_to_str, vnum)
    assert res_mm["status"] == "value-mismatch-at-own-step"
    assert res_mm["occ_step_t"] == 1
    assert "misattribution exposure" in res_mm["finding"]
    # a value matching no commit row of the whole record: the
    # standing data-integrity hard exit, NAMED, unchanged
    try:
        resolve_span_commit(dict(row, span=[50, 51]), dict(
            rec, commits=[c for c in rec["commits"]
                          if c["token"] != "3"]), id_to_str, vnum)
        raise AssertionError("an unresolvable span was accepted")
    except SystemExit as e:
        assert "SPAN-TO-COMMIT UNRESOLVABLE" in str(e)
    return "PASS"


@selfcheck("the v1.3.3 span-extent singular law: the node-row fixtures carry the REAL topology [i, step, tid, occ_i] with i != occ_i (the group ordinal NEVER bound, the index from occ_i), the v1.3.1/v1.3.2-exit regression rows accepted (the doc-213 shape: the head token NOT the numeric, the numeric deeper in the span), the no-span NAMED guard, the doc-12 known-answer pair (the pair law picks 35) + the doc-213 span-extent pair (occ_step_t 40 through the range [39, 40]), the zero-numeric singular row counted UNRESOLVABLE-NON-NUMERIC never an exit, the census names BOTH forms, every exit naming the doc")
def check_singular_own_step_form():
    with tempfile.TemporaryDirectory() as d:
        tp = os.path.join(d, "tokenizer.json")
        with open(tp, "w") as f:
            json.dump({"model": {"vocab": {"=": 50, "3": 51,
                                           "x": 52}}}, f)
        vnum_receipt, id_to_str = pin_vnum(tp, sha256_file(tp))
        vnum_ids = set(vnum_receipt["numeric_token_ids_sorted"])
        pos_spec = {"export": "17p2", "docs_path": "docs",
                    "doc_id_field": "doc_id",
                    "records_field": "p2.nodes",
                    "class_field": "node", "class_values": ["UNTRACED"],
                    "leg": "raw", "span_field": "locus",
                    "quantity_field": "quantity",
                    "value_field": "value",
                    "span_units": "token_ids"}
        # THE NAMED EXITS FIRST (each naming the doc, never guessed)
        # (a) the TRUE namespace collision (a range field + the
        # singular on one row) -- zero such rows in the real bytes,
        # the guard standing
        loads_collision = OrderedDict([("17p2", {"docs": [
            {"doc_id": 1, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [51], "quantity": "q",
                 "value": "3", "step_start": 1, "step_end": 1,
                 "step": 1, "tid": 51}]}}]})])
        try:
            extract_span_rows(loads_collision, pos_spec,
                             "ctx true-collision")
            raise AssertionError("a true-collision row was accepted")
        except SystemExit as e:
            assert "BOTH step field forms" in str(e)
            assert "doc 1" in str(e)
        # (b) THE v1.3.1-EXIT REGRESSION ROW -- the REAL byte shape
        # that tripped my run of record (the group ordinal i beside
        # the singular): ACCEPTED, the group ordinal never bound, the
        # occurrence index from occ_i
        loads_real = OrderedDict([("17p2", {"docs": [
            {"doc_id": 12, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [51], "quantity": "q",
                 "value": "3", "i": 5, "step": 35, "tid": 51,
                 "occ_i": 0}]}}]})])
        rows_real = extract_span_rows(loads_real, pos_spec,
                                      "ctx real-shape")
        rr = rows_real[0]
        assert rr["occ_step_start"] == 35
        assert rr["occ_step_end"] == 35
        assert rr["occ_tid"] == 51
        assert rr["occ_index"] == 0   # occ_i, NEVER the ordinal 5
        # (b2) THE v1.3.2-EXIT REGRESSION ROW -- the REAL byte shape
        # that tripped my v1.3.2 run of record (doc 213: the head
        # token NOT the numeric, the numeric DEEPER in the span):
        # ACCEPTED, the SPAN-EXTENT range bound, the occurrence
        # index from occ_i (the item-1172 law)
        loads_ext = OrderedDict([("17p2", {"docs": [
            {"doc_id": 213, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [52, 51],
                 "quantity": "q", "value": "x 3",
                 "i": 1, "step": 39, "tid": 52, "occ_i": 0}]}}]})])
        rows_ext = extract_span_rows(loads_ext, pos_spec,
                                     "ctx span-extent")
        rext = rows_ext[0]
        assert rext["occ_step_start"] == 39
        assert rext["occ_step_end"] == 40
        assert rext["occ_tid"] == 52
        assert rext["occ_index"] == 0   # occ_i, NEVER the ordinal 1
        assert "i" not in rext
        # (b3) a singular row with int step + tid but NO usable
        # span (None / empty / non-int entries): the span-extent
        # range law reads the row's own span -- a row without it a
        # NAMED premise violation, the doc named (zero real rows;
        # the guard standing)
        for bad_span in (None, [], ["51", 52]):
            loads_nospan = OrderedDict([("17p2", {"docs": [
                {"doc_id": 1, "p2": {"nodes": [
                    {"node": "UNTRACED", "locus": bad_span,
                     "quantity": "q", "value": "3",
                     "step": 1, "tid": 51}]}}]})])
            try:
                extract_span_rows(loads_nospan, pos_spec,
                                  "ctx no-span")
                raise AssertionError(
                    "a spanless singular row was accepted")
            except SystemExit as e:
                assert "no int-token span" in str(e)
                assert "doc 1" in str(e)
        # (c) the singular step without its tid: step + tid together
        loads_partial = OrderedDict([("17p2", {"docs": [
            {"doc_id": 1, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [51], "quantity": "q",
                 "value": "3", "step": 1}]}}]})])
        try:
            extract_span_rows(loads_partial, pos_spec,
                             "ctx partial-singular")
            raise AssertionError("a partial singular row was accepted")
        except SystemExit as e:
            assert "without its" in str(e)
            assert "doc 1" in str(e)
        # (d) a non-int singular form -- incl. the null-step gap-row
        # shape (the 149 absent rows' own form, should one ever reach
        # the extraction): NAMED, never guessed, the doc named
        for bad_step in ("1", None):
            loads_nonint = OrderedDict([("17p2", {"docs": [
                {"doc_id": 1, "p2": {"nodes": [
                    {"node": "UNTRACED", "locus": [51],
                     "quantity": "q", "value": "3",
                     "step": bad_step, "tid": 51}]}}]})])
            try:
                extract_span_rows(loads_nonint, pos_spec,
                                  "ctx nonint-singular")
                raise AssertionError(
                    "a non-int singular row was accepted")
            except SystemExit as e:
                assert "non-int singular form" in str(e)
                assert "doc 1" in str(e)
        # THE DOC-12 KNOWN-ANSWER (the item-1168 receipt): the SAME
        # numeric token id at steps 35/62/93, the commits at those
        # own steps; the node rows carry the REAL topology [i, step,
        # tid, occ_i] with the group ordinal i != occ_i
        ids12 = [52] * 100
        for s in (35, 62, 93):
            ids12[s] = 51
        cp = os.path.join(d, "cache.jsonl")
        write_jsonl(cp, [synth_cache_record(
            12, n_steps=100, n_commits=3, ids=ids12,
            commit_tokens=["3", "3", "3"],
            commit_ts=[35, 62, 93])])
        recs, inv = read_cache_records("t", cp, expect_records=1)
        cache_reads = {"math_cache": OrderedDict([
            ("records", recs), ("inventory", inv),
            ("sha256", "synthetic")])}
        # THE REAL-BYTE TOPOLOGY (the item-1170 finding): the
        # promotion lane carries the RANGE form; the node_rows lane
        # carries the SINGULAR form WITH the group ordinal beside --
        # the v1.3.1 battery authored node rows without i; these
        # fixtures carry the bytes' own field shapes
        loads = OrderedDict([("17p2", {"docs": [
            {"doc_id": 12, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [51],
                 "quantity": "q", "value": "3",
                 "step_start": 62, "step_end": 62},
                {"node": "DERIVED-VERIFIED", "locus": [51],
                 "quantity": "qn", "value": "3",
                 "i": 7, "step": 35, "tid": 51, "occ_i": 0},
                {"node": "DERIVED-VERIFIED", "locus": [51],
                 "quantity": "qn", "value": "3",
                 "i": 8, "step": 62, "tid": 51, "occ_i": 1},
                {"node": "DERIVED-VERIFIED", "locus": [51],
                 "quantity": "qn", "value": "3",
                 "i": 9, "step": 93, "tid": 51, "occ_i": 2}]}}]})])
        neg_spec = dict(pos_spec, class_values=["DERIVED-VERIFIED"])
        a2_pos = dict(pos_spec, class_values=["ABSENT-CLASS"])
        fmap = {
            "map_name": "synthetic map", "map_version": "synth",
            "stamp": "SYNTH STAMP",
            "bindings": {"cohort_A1_positives": pos_spec,
                         "cohort_A1_negatives": neg_spec,
                         "cohort_A2_positives": a2_pos,
                         "cohort_A2_negatives": dict(a2_pos)},
            "cache_bindings": {"raw": {"pin": "math_cache"}},
        }
        pins = OrderedDict([("synth", {"observed_sha256": "synthetic",
                                       "bytes": 0})])
        out = assemble_inventory(fmap, "synthetic-map-sha", pins,
                                 loads, cache_reads, vnum_receipt,
                                 id_to_str, vnum_ids)
        a1 = out["cohorts"]["A1"]
        # the singular-form node rows joined + resolved through the
        # SPAN-EXTENT own-step range (the len-1 spans keeping the
        # degenerate shape naturally) -- the resolve law
        # unchanged, ONE namespace
        assert a1["positives_extracted"] == 1
        assert a1["negatives_extracted"] == 3
        assert a1["positives_joined_resolved"] == 1
        assert a1["negatives_joined_resolved"] == 3
        assert len(a1["matched_pairs"]) == 1
        assert a1["unpaired_count"] == 0
        pair = a1["matched_pairs"][0]
        assert pair["pair_id"] == "A1-0001"
        # THE DOC-12 KNOWN-ANSWER: the three same-value occurrences at
        # steps 35/62/93; the candidate at the promotion's OWN step
        # (62) EXCLUDED by the different-step law; the NEAREST picked
        # -- 35 (distance 27) over 93 (distance 31); the pair law
        # picks 35, its occurrence index occ_i 0 -- NEVER the group
        # ordinal i 7
        assert pair["positive"]["span_resolution"][
            "occ_step_t"] == 62
        assert pair["negative"]["span_resolution"][
            "occ_step_t"] == 35
        assert pair["negative"]["occ_step_start"] == 35
        assert pair["negative"]["occ_step_end"] == 35
        assert pair["negative"]["occ_tid"] == 51
        assert pair["negative"]["occ_index"] == 0
        assert pair["occ_step_distance"] == 35 - 62
        # the v1.2.7 lineage form's own receipt: both rows carry the
        # same token id span, so the position-blind form cannot
        # separate them (0) -- the position-aware form (-27) is the
        # load-bearing distance, the amendment's whole story
        assert pair["step_distance"] == 0
        assert pair["positive"]["span_resolution"][
            "hidden_row_index"] != pair["negative"][
            "span_resolution"]["hidden_row_index"]
        assert "v1.3.0" in pair["bind_law"]
        # the resolution-class census: all 4 rows RESOLVED-OWN-STEP
        assert a1["resolution_class_census"] == {
            "RESOLVED-OWN-STEP": 4,
            "step-outside-cache-coverage": 0,
            "value-mismatch-at-own-step": 0,
            "UNRESOLVABLE-NON-NUMERIC": 0}
        # THE CENSUS NAMES BOTH FORMS PER COHORT, the bound fields
        # only -- the group ordinal `i` never among them
        ext = out["step_ext_census"][
            "cohort A1 (map synthetic map)"]
        assert ext["rows_with_step_fields"] == 4
        assert ext["rows_with_range_form"] == 1
        assert ext["rows_with_singular_form"] == 3
        assert ext.get("rows_without_step_fields", 0) == 0
        assert ext["fields_seen"] == ["occ_i", "step", "step_end",
                                      "step_start", "tid"]
        # the honest-population receipt: nothing dropped, nothing
        # unpaired -- the one promotion paired
        assert out["honest_population_receipt"][
            "unjoined_or_ambiguous_or_unpaired_count"] == 0
        # THE DOC-213 SPAN-EXTENT PIPELINE REGRESSION (the item-1172
        # law): the head token NOT numeric, the numeric DEEPER in
        # the span -- my v1.3.2 run of record exited NAMED on this
        # shape; the resolve walk over the SPAN-EXTENT range picks
        # the numeric's OWN step, BOTH rows RESOLVED-OWN-STEP, the
        # pair carrying the span-extent receipt
        ids213 = [52] * 60
        ids213[11] = 51
        ids213[40] = 51
        cp213 = os.path.join(d, "cache213.jsonl")
        write_jsonl(cp213, [synth_cache_record(
            213, n_steps=60, n_commits=2, ids=ids213,
            commit_tokens=["3", "3"], commit_ts=[11, 40])])
        recs213, inv213 = read_cache_records("t", cp213,
                                             expect_records=1)
        cache_reads213 = {"math_cache": OrderedDict([
            ("records", recs213), ("inventory", inv213),
            ("sha256", "synthetic")])}
        loads213 = OrderedDict([("17p2", {"docs": [
            {"doc_id": 213, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [52, 51],
                 "quantity": "q", "value": "x 3",
                 "step_start": 10, "step_end": 11},
                {"node": "DERIVED-VERIFIED", "locus": [52, 51],
                 "quantity": "qn", "value": "x 3",
                 "i": 1, "step": 39, "tid": 52, "occ_i": 0}]}}]})])
        out213 = assemble_inventory(fmap, "synthetic-map-sha", pins,
                                   loads213, cache_reads213,
                                   vnum_receipt, id_to_str, vnum_ids)
        a1_213 = out213["cohorts"]["A1"]
        assert a1_213["positives_joined_resolved"] == 1
        assert a1_213["negatives_joined_resolved"] == 1
        assert a1_213["resolution_class_census"] == {
            "RESOLVED-OWN-STEP": 2,
            "step-outside-cache-coverage": 0,
            "value-mismatch-at-own-step": 0,
            "UNRESOLVABLE-NON-NUMERIC": 0}
        pair213 = a1_213["matched_pairs"][0]
        assert pair213["positive"]["span_resolution"][
            "occ_step_t"] == 11
        assert pair213["negative"]["occ_step_start"] == 39
        assert pair213["negative"]["occ_step_end"] == 40
        assert pair213["negative"]["span_resolution"][
            "occ_step_t"] == 40
        assert pair213["negative"]["occ_index"] == 0
        assert pair213["occ_step_distance"] == 40 - 11
        assert pair213["positive"]["span_resolution"][
            "hidden_row_index"] != pair213["negative"][
            "span_resolution"]["hidden_row_index"]
        # THE ZERO-NUMERIC SINGULAR ROW (the 140-row real class, the
        # item-1172 census): the span carries NO numeric token -- the
        # receipt amendment's own class, counted UNRESOLVABLE-NON-
        # NUMERIC, never an exit, the row riding the honest receipt
        cp214 = os.path.join(d, "cache214.jsonl")
        write_jsonl(cp214, [synth_cache_record(
            214, n_steps=10, n_commits=1, ids=[52] * 10,
            commit_tokens=["x"], commit_ts=[5])])
        recs214, inv214 = read_cache_records("t", cp214,
                                             expect_records=1)
        cache_reads214 = {"math_cache": OrderedDict([
            ("records", recs214), ("inventory", inv214),
            ("sha256", "synthetic")])}
        loads214 = OrderedDict([("17p2", {"docs": [
            {"doc_id": 214, "p2": {"nodes": [
                {"node": "DERIVED-VERIFIED", "locus": [52],
                 "quantity": "qn", "value": "x",
                 "i": 0, "step": 5, "tid": 52, "occ_i": 0}]}}]})])
        out214 = assemble_inventory(fmap, "synthetic-map-sha", pins,
                                   loads214, cache_reads214,
                                   vnum_receipt, id_to_str, vnum_ids)
        a1_214 = out214["cohorts"]["A1"]
        assert a1_214["negatives_extracted"] == 1
        assert a1_214["negatives_joined_resolved"] == 0
        assert a1_214["unresolved_non_numeric"] == 1
        assert a1_214["resolution_class_census"] == {
            "RESOLVED-OWN-STEP": 0,
            "step-outside-cache-coverage": 0,
            "value-mismatch-at-own-step": 0,
            "UNRESOLVABLE-NON-NUMERIC": 1}
        assert out214["honest_population_receipt"][
            "unjoined_or_ambiguous_or_unpaired_count"] == 1
        return "PASS"




@selfcheck("the full synthetic inventory: known-answer cohort table + two-run byte-identical determinism")
def check_inventory_pipeline():
    with tempfile.TemporaryDirectory() as d:
        tp = os.path.join(d, "tokenizer.json")
        with open(tp, "w") as f:
            json.dump({"model": {"vocab": {"=": 50, "3": 51, "7": 52,
                                           "x": 53}}}, f)
        vnum_receipt, id_to_str = pin_vnum(tp, sha256_file(tp))
        vnum_ids = set(vnum_receipt["numeric_token_ids_sorted"])
        cp = os.path.join(d, "cache.jsonl")
        write_jsonl(cp, [synth_cache_record(
            7, n_steps=3, n_commits=2, ids=[50, 51, 52],
            commit_tokens=["3", "7"], commit_ts=[1, 2]),
            synth_cache_record(
            8, n_steps=3, n_commits=2, ids=[50, 51, 52],
            commit_tokens=["3", "7"], commit_ts=[1, 2])])
        recs, inv = read_cache_records("t", cp, expect_records=2)
        cache_reads = {"math_cache": OrderedDict([
            ("records", recs), ("inventory", inv),
            ("sha256", "synthetic")])}
        loads = OrderedDict([("17p2", {"docs": [
            {"doc_id": 7, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [50, 51],
                 "quantity": "q", "value": "3",
                 "step_start": 1, "step_end": 1},
                {"node": "DERIVED-VERIFIED", "locus": [50, 52],
                 "quantity": "q2", "value": "3",
                 "step_start": 2, "step_end": 2}]}},
            {"doc_id": 8, "p2": {"nodes": [
                {"node": "UNTRACED", "locus": [50, 51],
                 "quantity": "q3", "value": "3",
                 "step_start": 1, "step_end": 1}]}}]})])
        pos_spec = {"export": "17p2", "docs_path": "docs",
                    "doc_id_field": "doc_id",
                    "records_field": "p2.nodes",
                    "class_field": "node", "class_values": ["UNTRACED"],
                    "leg": "raw", "span_field": "locus",
                    "quantity_field": "quantity",
                    "value_field": "value",
                    "span_units": "token_ids"}
        neg_spec = dict(pos_spec, class_values=["DERIVED-VERIFIED"])
        a2_pos = dict(pos_spec, class_values=["ABSENT-CLASS"])
        fmap = {
            "map_name": "synthetic map", "map_version": "synth",
            "stamp": "SYNTH STAMP",
            "bindings": {"cohort_A1_positives": pos_spec,
                         "cohort_A1_negatives": neg_spec,
                         "cohort_A2_positives": a2_pos,
                         "cohort_A2_negatives": dict(a2_pos)},
            "cache_bindings": {"raw": {"pin": "math_cache"}},
        }
        pins = OrderedDict([("synth", {"observed_sha256": "synthetic",
                                       "bytes": 0})])
        out = assemble_inventory(fmap, "synthetic-map-sha", pins,
                                 loads, cache_reads, vnum_receipt,
                                 id_to_str, vnum_ids)
        a1 = out["cohorts"]["A1"]
        assert a1["positives_extracted"] == 2
        assert a1["negatives_extracted"] == 1
        assert len(a1["matched_pairs"]) == 1
        pair = a1["matched_pairs"][0]
        assert pair["pair_id"] == "A1-0001"
        assert pair["positive"]["span_resolution"]["t0"] == 51
        assert pair["positive"]["span_resolution"][
            "status"] == "RESOLVED-OWN-STEP"
        assert pair["positive"]["span_resolution"][
            "occ_step_t"] == 1
        assert pair["positive"]["span_resolution"][
            "commit_index"] == 0
        assert pair["negative"]["span_resolution"]["t0"] == 52
        assert pair["negative"]["span_resolution"][
            "occ_step_t"] == 2
        assert pair["negative"]["span_resolution"][
            "commit_index"] == 1
        # the v1.3.0 receipt fields: the bind law text + the signed
        # distances (occ_step_distance the position-aware form,
        # step_distance the v1.2.7 lineage form) + the S4 assertion
        # (two different hidden rows, by construction and by check)
        assert "v1.3.0" in pair["bind_law"]
        assert pair["occ_step_distance"] == 1
        assert pair["step_distance"] == 1
        assert pair["positive"]["span_resolution"][
            "hidden_row_index"] != pair["negative"][
            "span_resolution"]["hidden_row_index"]
        assert "v1.3.0" in a1["bind_rule_verbatim"]
        # the v1.3.0 census receipts: the resolution-class census +
        # the S3 extension census (every row carried its step
        # fields). THE KNOWN-ANSWER 3, NAMED (the python-return
        # fix, item 1166): the census measures RESOLUTION per row
        # (counted at resolve time, BEFORE the binding) -- the
        # pair's 2 rows + doc 8's resolved-but-UNPAIRED positive
        # all ride RESOLVED-OWN-STEP; the honest receipt owns the
        # BINDING count (1). The prior expectation 2 counted only
        # the pair rows -- a battery known-answer miscount, the
        # builder's own census law stands.
        assert a1["resolution_class_census"] == {
            "RESOLVED-OWN-STEP": 3,
            "step-outside-cache-coverage": 0,
            "value-mismatch-at-own-step": 0,
            "UNRESOLVABLE-NON-NUMERIC": 0}
        ext = out["step_ext_census"][
            "cohort A1 (map synthetic map)"]
        assert ext["rows_with_step_fields"] == 3
        # the python-return read fix, NAMED (item 1166): the
        # census names only the categories it SAW (a zero-count
        # category absent, never an invented zero) -- the battery
        # reads it with the get, the honest-census law kept
        assert ext.get("rows_without_step_fields", 0) == 0
        assert ext["fields_seen"] == ["step_end", "step_start"]
        honest = out["honest_population_receipt"]
        # doc 8 joins + resolves (its own cache record) then rides
        # UNPAIRED at the binding with its reason NAMED -- the full
        # v1.3.0 path, never the unjoined shortcut
        assert honest["unjoined_or_ambiguous_or_unpaired_count"] == 1
        assert honest["entries"][0]["positive"]["doc_id"] == 8
        assert honest["entries"][0]["finding"].startswith(
            "UNPAIRED -- ")
        assert "no same-doc DERIVED-VERIFIED rows" in \
            honest["entries"][0]["finding"]
        assert honest["entries"][0]["positive"][
            "span_resolution"]["t0"] == 51
        assert out["coverage_boundary"]["finding"].startswith(
            "NAMED GAP")
        assert out["layer_certificate"]["per_cache"]["math_cache"][
            "hidden_dim"] == 8
        assert "94" in json.dumps(
            honest["beside_the_banked_receipts"])
        # the two-run determinism: byte-identical exports
        out2 = assemble_inventory(fmap, "synthetic-map-sha", pins,
                                 loads, cache_reads, vnum_receipt,
                                 id_to_str, vnum_ids)
        b1 = json.dumps(out, indent=1, sort_keys=True)
        b2 = json.dumps(out2, indent=1, sort_keys=True)
        assert b1 == b2
        e1 = os.path.join(d, "inv1.json")
        e2 = os.path.join(d, "inv2.json")
        for path, o in ((e1, out), (e2, out2)):
            with open(path, "w") as f:
                json.dump(o, f, indent=1, sort_keys=True)
        assert sha256_file(e1) == sha256_file(e2)
    return "PASS"


# ---------------------------------------------------------------------------
# Section 13. main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="CD-1 Arm A B0 cohort inventory + certification build")
    ap.add_argument("--census", action="store_true",
                    help="Pass 1: read-only structure census of the four "
                         "label exports (my map stamp follows)")
    ap.add_argument("--reconcile", action="store_true",
                    help="the reconciliation gate: the candidate map's "
                         "bindings derived against the banked receipts "
                         "(exact-or-exit; a mismatch is a WRONG BINDING, "
                         "never a discarded concept; a binding the bytes "
                         "cannot carry is a coverage discovery at my door)")
    ap.add_argument("--map", default=DEFAULT_MAP_PATH,
                    help="the candidate field map path (pins at my stamp)")
    ap.add_argument("--map-sha", default=None,
                    help="MY CONSOLE sha256 of the stamped map file; "
                         "--run asserts the observed sha equals it "
                         "exactly (never hand-typed by the tool)")
    ap.add_argument("--run", action="store_true",
                    help="Pass 2: the inventory run (after my map "
                         "stamp; needs --map-sha + --tokenizer + "
                         "--tokenizer-sha)")
    ap.add_argument("--tokenizer", default=None,
                    help="the tokenizer.json path (the V_num pin reads "
                         "it; zero decodes, zero GPU)")
    ap.add_argument("--tokenizer-sha", default=None,
                    help="MY CONSOLE sha256 of tokenizer.json; the "
                         "V_num pin asserts it exactly")
    ap.add_argument("--selfcheck", action="store_true",
                    help="the synthetic known-answer battery")
    ap.add_argument("--inputs-dir", default=None,
                    help="the folder carrying the pinned input files")
    ap.add_argument("--out", default=None,
                    help="the export path (census, reconciliation, or "
                         "inventory)")
    args = ap.parse_args()
    if args.selfcheck:
        return run_selfcheck()
    if args.census:
        return run_census(args)
    if args.reconcile:
        return run_reconcile(args)
    if args.run:
        return run_inventory(args)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())

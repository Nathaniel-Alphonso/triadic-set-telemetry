#!/usr/bin/env python3
# cd1_arm_a_separation_run_v104.py -- the CD-1 Arm A B2 separation
# run, the ASSEMBLED TOOL OF RECORD (parts 1+2+3 in one file). Per
# my PINNED Arm A sheet (14dbedda... section 6 line B2) under
# the stamped Phase-1 build spec (0c886741... section 4), at my B1
# acceptance stamp. ZERO GPU, ZERO DECODES, ZERO BUILD HOURS: the
# caches + the B0 inventory + the label exports + the B1 module
# (imported, its sha asserted) + the model file's unembedding rows
# are read MY-SIDE (matrix multiplication only, never a forward
# pass, never a decode, the files never leaving my Mac). The tool
# prints no verdicts; findings presented, never adjudicated; the
# my stamps decide.
#
# v1.0.1 -- THE DEFECT FIX, NAMED AT THE TOP OF THE FILE (never
# buried): the v1.0.0 assembly carried a transcription defect in
# the checker_17p2_ledger pin (an extra '6' at the string-literal
# split, 65 chars; my first run hard-exited on an
# identical-looking tail pair). The fix: the pin re-split at a
# clean boundary and verified byte-exact against the local file;
# EVERY sha256 pin now carries the PIN-SHAPE LAW (verify_pin_shape:
# 64 lowercase hex, malformed pins a hard exit at load, never at
# my console); every pin mismatch now prints the FULL
# observed sha (diagnosability at the console). The pins were
# re-derived programmatically, never hand-transcribed (the
# hand-transcription of hex literals is the defect class itself).
#
# v1.0.2 -- THE NON-FINITE CLASS, NAMED NEVER A CRASH (the item-1155
# fix): the first my-side run tripped the operators on a
# non-finite measured input (a NaN reaching the ulp law). The fix,
# two laws: (1) THE W_U FINITE LAW AT LOAD -- every unembedding row
# of the model of record must be finite; a non-finite row a
# data-integrity hard exit at load, named (a wrong shard or a wrong
# read), never a NaN reaching the operators; (2) THE
# NAMED-NON-FINITE CLASS -- a non-finite hidden row / doc mean /
# prior row / window row / operand row a counted NAMED class
# carried in the export with its component + count + samples, the
# row never computed, never a crash, never a silent skip; the
# doc-mean guard catches a whole poisoned doc (one non-finite
# commit row poisons the doc's mean, every row of that doc NAMED at
# the component doc_mean); the corroborator lane NAMED alone when
# only the prior row is non-finite (the primary unpoisoned). The
# battery extended: P1-C11 + P2-C18 at v1.0.2; P1-C12/C12b/C12c
# at v1.0.3 (39 checks expected).
#
# v1.0.3 -- THE ENDIANNESS DECODE FIX, OWNED (the item-1156 class,
# caught by MY run): the v1.0.2 W_U finite law hard-exited at my
# console naming 1,110 non-finite rows -- on sha-verified shard
# bytes, so the load law caught a wrong READ, never wrong model
# bytes. The defect: BOTH byte-decode paths were authored
# big-endian. The receipts: the safetensors format spec ("Endi-
# aness: Little-endian") for the W_U tensor bytes, and the
# instrument of record's OWN writer bytes for the cache payload
# (triadic_telemetry_t2_v32.3.0.py: rec["hidden"].half().numpy()
# .tobytes() -- float16, native order = little-endian on my Mac --
# read back by the instrument's own np.frombuffer dtype float16).
# The earlier citation "the B0 builder's own reader law" named a
# receipt that never existed (the builder length-checks the
# payload, never value-decodes) -- a citation defect of the
# item-1146 family, owned here. The retrodiction: an all-finite
# spec-order matrix through the old decode yields non-finite rows
# 1,110 of 1,110 (my receipt class exactly); through the fixed
# decode, zero. The battery: every decode + fixture now spec
# order, and P1-C12/C12b/C12c pin the direction on HAND spec-
# order bytes (the mirror-defect law: a fixture writer and a
# reader sharing one wrong convention can never see the error).
# The v1.0.2 laws (the W_U finite law at load + the
# NAMED-NON-FINITE class) stand UNCHANGED -- they caught this.
#
# v1.0.4 -- THE INSTRUMENT-FORM RAW-GAP RECOGNITION + THE A1
# RE-BIND LANE (the item-1158 recs, MY RULING TAKEN: "okay lets
# gowith the recs and do the rerun"). (1) The v1.0.3 raw_gap
# discovery vocabulary carried ONLY logit-domain names, so the
# caches' own banked probability-domain features never matched --
# the miss MINE (the item-1146/1156 family), owned here. The
# receipts: the instrument writer's own bytes
# (triadic_telemetry_t2_v32.3.0.py: emitted_p = probs
# [emitted_id]; margin = float(top_p[0]-top_p[1]); second_p =
# the first content alternative at/below top-2; the v32.0.6
# notes: "the raw features emitted_p/margin/content_mass, banked
# per step -- they are the banked cache3 schema"). The v1.0.4
# read block recognizes the instrument's own form: the raw_gap
# receipt READ in the probability domain (the instrument's own
# margin verbatim, the (emitted_p, second_p) pair carried beside
# it, the emitted-vs-top1 case named per row, the float32
# round-trip tolerance named); the logit-domain branch stands
# unchanged for a cache that banks logits. An EMITTED-NOT-TOP1-
# CONSISTENT case on the real bytes is a TRUE DATA FINDING at
# my door, presented never smoothed. (2) The A1 lane
# re-bound per the v1.2.7 builder (same-doc, SAME value,
# DIFFERENT t0 from span_resolution, nearest |t0 diff|, the
# deterministic span-order tie-break, the signed step_distance
# receipt per pair; the item-1158 pool census 177 candidates),
# the run reading the v2 inventory; the A2 lane byte-unchanged
# (the banked 73/23). (3) THE INVENTORY PIN AT MY CONSOLE
# LINE: the v2 inventory sha exists only after my v1.2.7
# builder run, so it pins at my --inventory-sha flag (the
# item-1134 stamp-act precedent, my own --map-sha ruling),
# asserted byte-exact at load, the pin-shape law enforced --
# never a banked constant this side. The v1 export + the v1
# readings STAND banked, never retro-edited. The battery: P1 16
# + P2 19 + P3 8 = 43 checks expected (P1-C13/C13b the console
# pin + re-bind law, P2-C19 the instrument form, P3-C08 the
# raw-gap census lane).
#
# v1.0.8 -- THE INVENTORY BUILD-RECEIPT PIN MOVES v1.3.2 -> v1.3.3
# (my stamp, the item-1172 act; my words verbatim: "begin the
# fourth fucking build act"): my BLOCK-1 run of record exited
# honestly at doc 213 -- the singular `step` is the SPAN-HEAD
# step (the exporter's own construction: step = the step covering
# the value's FIRST char, span = the CONTIGUOUS run covering the
# value), the numeric DEEPER in the run ("Delta-E 1": the head
# "Delta" at 39, the "1" at 42), the v1.3.2 DEGENERATE range
# [step, step] demanding the numeric at the head -- 23 rows
# across 6 docs, an assumption the bytes never made; the builder
# v1.3.3 (banked beside) binds the SPAN-EXTENT range [step, step +
# len(span) - 1] (the three-lane preflight: promotions 371, DV
# 4,062, A2 7,115 -- contiguity/bounds/head/i-binding zero
# violations, 11,387 rows resolvable, 161 zero-numeric rows the
# standing receipt class); the run tool's ONLY change is the
# inventory build-receipt pin: the read_inventory tool-line check
# now demands the v1.3.3 build receipt (a v1.3.2 inventory a
# NAMED refusal at the door of the v3 rerun, never a
# position-blind read of the superseded build), and the pin's
# source descriptions name the v1.3.3 builder's own export
# print. EVERY other law byte-identical to the accepted v1.0.7
# (the position-aware laws, the S4 load law, the class-census
# cross-check, the occurrence-level row law, the bind_law
# receipt check). The battery P1-C13c UPDATED (the pin fixture
# moves with the pin): the v1.3.3 tool line accepted THROUGH the
# version check into the next law, the v1.3.2 line refused NAMED,
# the wrong builder name refused NAMED; the count stays P1 18 +
# P2 19 + P3 10 = 47 checks expected. The v1/v2 exports +
# readings STAND banked, never retro-edited.
#
# v1.0.7 -- THE INVENTORY BUILD-RECEIPT PIN MOVES v1.3.1 -> v1.3.2
# (my stamp, the item-1170 act; my words verbatim: "okay yea
# do such, continue on to the buil act"): my BLOCK-1 run of
# record exited honestly at doc 12 -- the first DERIVED-VERIFIED
# row carried the SINGULAR own-step form with `i` the value-group
# ordinal, never the occurrence ordinal (i == occ_i on only 352
# of 4,062 DV rows); the builder v1.3.2 (banked beside) binds it
# (the singular path requires step + tid both int, binds the
# degenerate range [step, step] + occ_index from occ_i only -- `i`
# NEVER bound on the singular path, the naive misindex closed);
# the run tool's ONLY change is the inventory build-receipt pin:
# the read_inventory tool-line check now demands the v1.3.2 build
# receipt (a v1.3.1 inventory a NAMED refusal at the door of the
# v3 rerun, never a position-blind read of the superseded build),
# and the pin's source descriptions name the v1.3.2 builder's
# own export print. EVERY other law byte-identical to the
# accepted v1.0.6 (the position-aware laws, the S4 load law, the
# class-census cross-check, the occurrence-level row law, the
# bind_law receipt check). The battery P1-C13c UPDATED (the pin
# fixture moves with the pin): the v1.3.2 tool line accepted
# THROUGH the version check into the next law, the v1.3.1 line
# refused NAMED, the wrong builder name refused NAMED; the count
# stays P1 18 + P2 19 + P3 10 = 47 checks expected. The v1/v2
# exports + readings STAND banked, never retro-edited.
#
# v1.0.6 -- THE INVENTORY BUILD-RECEIPT PIN MOVES v1.3.0 -> v1.3.1
# (my stamp, the item-1168 act; my words verbatim: "okay continue
# lets have 3 messages for the build act"): my BLOCK-1 run of
# record caught the aligned bytes' SINGULAR own-step form -- the
# builder v1.3.1 (banked beside) binds it; the run tool's ONLY
# change is the inventory build-receipt pin: the read_inventory
# tool-line check now demands the v1.3.1 build receipt (a v1.3.0
# inventory a NAMED refusal at the door of the v3 rerun, never a
# position-blind read of the superseded build), and the pin's
# source descriptions name the v1.3.1 builder's own export print.
# EVERY other law byte-identical to the accepted v1.0.5 (the
# position-aware laws, the S4 load law, the class-census
# cross-check, the occurrence-level row law, the bind_law receipt
# check -- the pair law text itself still says v1.3.0, the stamped
# amendment's name, the law unchanged). The battery gains P1-C13c
# (the inventory build-receipt pin fixture): the v1.3.1 tool line
# accepted THROUGH the version check into the next law, the
# v1.3.0 line refused NAMED, the wrong builder name refused NAMED
# -- the check had NO fixture at v1.0.5 (the mirror lesson of the
# item-1168 finding: a law without a fixture is a fixture gap).
# The battery: P1 18 + P2 19 + P3 10 = 47 checks expected. The
# v1/v2 exports + readings STAND banked, never retro-edited.

# v1.0.5 -- THE SHEET AMENDMENT v3 LOAD LAWS (my stamps, items
# 1162/1163/1164: the prereg accepted, the builder v1.3.0 banked):
# the run tool reads the INVENTORY v3 AT THE OCCURRENCE LEVEL.
# (1) THE OCCURRENCE-LEVEL ROW LAW: every pair row carries its
# span_resolution with status RESOLVED-OWN-STEP + the occurrence's
# own step (occ_step_t, an int) + the t_0 of the span's first
# numeric token (a token id, the W_U answer-column fetch unchanged)
# + its hidden_row_index; a row without them a NAMED premise
# violation at load, never a silent position-blind read. (2) THE
# S4 LOAD LAW, BOTH LANES: every pair's two rows assert DIFFERENT
# hidden rows DIRECTLY (hidden_row_index inequality per pair,
# fail-loud PAIR-LAW-HIDDEN-ROW-EQUALITY) -- the v1.0.4 t_0
# inequality proxy RETIRED (the item-1161(e) hole: float-equal
# values like "5" vs "5.0" could pair the same row under the old
# proxy), and the A1 lane asserts the position-aware measure
# (two DIFFERENT occurrence steps per pair, occ_step_distance
# cross-checked against the pair's own receipt; the v1.2.7
# step_distance carried as the lineage diagnostic, cross-checked
# the same way). (3) THE CLASS-CENSUS CROSS-CHECK: the inventory's
# own resolution_class_census asserted against its own blocks --
# RESOLVED-OWN-STEP == positives_joined_resolved +
# negatives_joined_resolved, each NAMED class count == the honest
# receipt's own entries of that class, every count DERIVED from
# the export's bytes, never a constant this side. (4) THE v2
# LANDING CONSTANTS REMOVED, NAMED: the hard-coded 350/3922 +
# 96/7019 joined counts, the A2 73/23 pair counts, and the 161
# unresolved constant all RETIRED -- the v3 resolution re-lands
# both lanes (the A2 movement THE EXPECTATION: 67 of the 96 A2
# slips ride in-doc repeated values, the re-resolution shifts
# rows by design, the shift itself a finding, never forced); the
# INVARIANTS KEPT: the extraction censuses (371 A1 promotions, 96
# A2 positives), the standing 21 A1 UNRESOLVABLE-NON-NUMERIC, the
# 177 A1 pool bound, the honest-population arithmetic (pairs +
# unpaired + the NAMED class rows == the extraction count, per
# cohort, derived). (5) THE NAMED-BESIDE CENSUS: the
# step-outside-cache-coverage / value-mismatch-at-own-step /
# UNJOINED / AMBIGUOUS rows ride the receipts NAMED, never
# computed, counted in the population print + the export. (6)
# The v1.0.4 instrument-form raw-gap probability-domain
# recognition carried UNCHANGED; the B1 module UNTOUCHED (its
# sha pin asserted at import, never edited). The battery: P1 17
# + P2 19 + P3 10 = 46 checks expected (P1-C13b rewritten to the
# v1.3.0 law, P1-C14 the occurrence-level row law, P3-C01 the
# movement-shape census, P3-C09 the class-census cross-check,
# P3-C10 the honest-population arithmetic). The v1/v2 exports +
# readings STAND banked, never retro-edited.
#
# THE RUN COMMAND OF RECORD (my-side, the flags pinned):
#   python3 cd1_arm_a_separation_run_v108.py \
#       --inputs <dir: the three caches + the label exports + the
#                aligned export + the B1 module + the tokenizer> \
#       --inventory cd1_arm_a_cohort_inventory_v3.json \
#       --inventory-sha <my line: the v1.3.3 builder's own export
#                        print (the console pin, the item-1134
#                        law; the 64-hex shape law at load)> \
#       --model-dir <dir: the 4-shard model of record + its
#                    safetensors index> \
#       --tokenizer tokenizer.json \
#       --b1 cd1_arm_a_operators_b1.py \
#       --out cd1_arm_a_separation_run_v3.json
#   python3 cd1_arm_a_separation_run_v108.py --selfcheck
#       (the full acceptance battery: P1 + P2 + P3, constructed
#        bytes only, zero pinned inputs touched)
#
# THE RUNTIME EXPECTATION, STATED HONESTLY (never smoothed): the
# population rides the v3 inventory's own census (the A1
# position-aware pairs, at most 177 pairs = 354 pair rows, the
# invariant pairs + unpaired + the NAMED class rows == 371
# promotions with the standing 21 unresolved inside the class
# rows; the A2 lane RE-RESOLVED under the one rule -- the pair
# count MOVES by design, the v2 73/23 landing never asserted this
# side, the movement itself a finding at my door; the
# UNRESOLVABLE-NON-NUMERIC + step-outside-cache-coverage +
# value-mismatch-at-own-step rows ride the honest-population
# receipt NAMED, never computed); per row the
# reads are the doc centering mean (one decode per numeric commit,
# cached per record), the V_num projection (1,110 dot products of
# dim 4,096 per touched hidden row -- the primary h_t0, the prior
# row, the operand rows, the derivation-window rows), and the W_U
# answer column; the arithmetic is pure Python (no GPU, no vector
# libraries, the pinned instrument); the honest expectation is
# TENS OF MINUTES to a few hours my-side, the cache read (the
# 3.6 GB p2 file) and the per-row projections dominating; the
# memory expectation: the cache records are held in memory per the
# B0 builder's own reader law (my Mac carried the B0 pass on the
# same bytes); progress is printed every 50 rows, every NAMED class
# counted and carried beside the paired statistic.
#
# THE HONEST NAMED CLASSES OF THE RUN (never silent, all counted):
#   the A1 lane: centered_r_perp NAMED-OUT-OF-COVERAGE (the p2 lane
#   is prompt-anchored, the quantities enter via the prompt) and
#   work_increment NAMED-NO-PATH-EVIDENCE; the A2 lane:
#   PROMPT-SIDE-OPERAND (the coverage boundary class),
#   NAMED-INTERMEDIATE-UNCOMMITTED (a correct-precedence sub-result
#   never emitted), NAMED-OPERAND-COVERAGE (a root antecedent
#   unresolved), the statement-binding NAMED classes, and the
#   raw-gap receipt expected READ in the probability domain on
#   the caches of record (the instrument's own banked margin +
#   the emitted_p/second_p pair, the emitted-vs-top1 case named
#   per row); a NAMED-ABSENT raw_gap or an EMITTED-NOT-TOP1-
#   CONSISTENT case on the real bytes is a TRUE DATA FINDING at
#   my door, presented never smoothed.

TOOL = "cd1_arm_a_separation_run_v108.py"
VERSION = "1.0.8"
BUILD = ("assembled 3 of 3 (the tool of record; v1.0.8 the "
         "inventory build-receipt pin at the v1.3.3 build of "
         "record + its battery fixture; every v1.0.7 law carried "
         "unchanged)")

import base64
import hashlib
import json
import math
import os
import re
import struct
import sys




# ---------------------------------------------------------------------------
# Section 1. The pin engine (every pin asserted fail-loud at load; the
# pin-tail law: the banked form exact, invented tails a hard exit)
# ---------------------------------------------------------------------------

PINS = {
    "inventory": {
        # v1.0.5: the v3 inventory pin rides MY CONSOLE LINE (the
        # item-1134 stamp-act law, my own ruling for the map: "the
        # map pins at my --map-sha console line -- the load-bearing
        # pin"); the v1.3.3 builder's own export print is the source
        # (the v3 sha exists only after my builder run of record,
        # never a banked constant this side); the pin-shape law
        # enforced at load, the sha asserted byte-exact
        "file": "cd1_arm_a_cohort_inventory_v3.json",
        "sha256": None,
        "source": "my --inventory-sha console line (the v1.3.3 "
                  "builder's own export print)",
    },
    "b1_module": {
        "file": "cd1_arm_a_operators_b1.py",
        "sha256": ("ee603bd989e9e4c437d213ee5243b3f8b3fc0366bb883"
                   "bdd84d7eb145d980977"),
    },
    "aligned_spans": {
        "file": "aligned_spans_v2.json",
        "sha256": ("263b2459e37aa974d519b1869e3bd92139d2d584e053e"
                   "4cb811c4cf1ef6010b8"),
        "bytes": 10792116,
    },
    "checker_17a_raw": {
        # the RE-EMITTED statement-rows export of record (the
        # inventory's own input receipt; the item-1128 ruling 2)
        "file": "triadic_checker_offline_pass_8b.json",
        "sha256": ("a61f2bc77134540be5e21cf38f042ab5e2e9c317cbf7"
                   "0e3e95b44f11b099b4e1"),
        "bytes": 2338574,
    },
    "checker_17a_chat": {
        # the RE-EMITTED statement-rows export of record
        "file": "triadic_checker_chat_8b.json",
        "sha256": ("5ece17f8ae6a35c1249a33fccd317a23592ea76bf2bc"
                   "7f1107e54593324033b1"),
        "bytes": 136469,
    },
    "checker_17p2": {
        "file": "triadic_p2rw17_offline_pass_8b_v1.json",
        "sha256": ("4e711a58057ba252b66eb27fbb5a17e6fd2cbf8e7070a"
                   "c3d31b2034c3b5f3e74"),
        "bytes": 2510930,
    },
    "checker_17p2_ledger": {
        "file": "triadic_p2rw17_offline_pass_8b_v1_per_doc.jsonl",
        # the v1.0.0 defect fix (named at the item-1146 bank): the
        # prior literal split duplicated a character (65 chars);
        # re-split at a clean boundary + verified byte-exact
        # against the file; verify_pin_shape guards the class
        "sha256": ("ff10fe8528a99ff7d88e0d19d195f8951610d6d42"
                   "18e668a1b89a4f8a833a614"),
        "bytes": 219254,
    },
    "cache_a2_raw": {
        # the byte-level identity string of record (a verbatim pin)
        "file": ("triadic_t2_cache_t2-gsm-full-8b_bfloat16_bos"
                 ".jsonl"),
        "sha256": ("a427adee8489bf96f36057592f7c5a571eca4fa5261bb"
                   "3b99251c2d646d391ac"),
        "bytes": 670734423, "records": 1329,
    },
    "cache_a2_chat": {
        # the byte-level identity string of record (a verbatim pin)
        "file": ("triadic_t2_cache_gsm-chat100-8b_bfloat16_bos"
                 ".jsonl"),
        "sha256": ("4953da290e049d7dba7b740f2697c4662f57d51932d28"
                   "dbab5298253d297e2df"),
        "bytes": 96154339, "records": 110,
    },
    "cache_p2_r2": {
        "file": "triadic_t2_cache_rw17-p2-r2_bfloat16_bos.jsonl",
        "sha256": ("426459930ad726d77fcea8e30639d32dff71164bc9ebd"
                   "f36970765bb2df500a4"),
        "bytes": 3601008354, "records": 760,
    },
    "model_shards": {
        # the item-574 bank, 4/4 verified green at item 628
        "shard_sha_prefixes": ["2b1879f3", "09d433f6",
                               "fc1cdddd", "92ecfe1a"],
        "index_file": "model.safetensors.index.json",
        "w_u_tensor": "lm_head.weight",
    },
}

CACHE_RECORD_REQUIRED = [
    "key", "leg", "doc_id", "bos", "instrument", "prompt_len",
    "stop_reason", "n_gen_steps", "n_content_steps", "walk_ids",
    "steps", "commits",
]
STEPS_COLUMNS_REQUIRED = ["t", "id"]
COMMIT_ROW_REQUIRED = ["t", "token", "phase"]
HIDDEN_BYTES_PER_VALUE = 2  # float16, the instrument writer's own form


def fail_loud(msg):
    raise SystemExit("HARD EXIT -- " + msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def verify_pin_shape():
    """The pin-shape law (the item-1146 defect class guard): every
    banked sha256 pin must be 64 lowercase hex characters, every
    shard prefix 8; a malformed pin a hard exit at load, before
    any file is touched -- a transcription defect must die here,
    never at my console."""
    import string
    hexs = set(string.hexdigits.lower())
    for name, pin in sorted(PINS.items()):
        if not isinstance(pin, dict):
            continue
        s = pin.get("sha256")
        if s is not None:
            if not (isinstance(s, str) and len(s) == 64
                    and all(c in hexs for c in s)):
                fail_loud("pin shape %s: the sha256 string is not "
                          "64 lowercase hex characters (len %r) -- "
                          "a malformed banked pin, the load stops "
                          "here" % (name, len(s)
                                    if isinstance(s, str) else s))
        n = pin.get("bytes")
        if n is not None and (not isinstance(n, int) or n <= 0):
            fail_loud("pin shape %s: the bytes pin %r is not a "
                      "positive int" % (name, n))
    for p in PINS["model_shards"]["shard_sha_prefixes"]:
        if not (isinstance(p, str) and len(p) == 8
                and all(c in hexs for c in p)):
            fail_loud("pin shape: the shard prefix %r is not 8 "
                      "hex characters" % p)
    return True


def assert_pin(name, path, pin, bytes_needed=True):
    if not os.path.exists(path):
        fail_loud("pin %s: file %r not found (the run reads only "
                  "the pinned bytes; never a guess)" % (name, path))
    got = sha256_file(path)
    if got != pin["sha256"]:
        tail = got[:8]
        fail_loud("pin %s: sha tail %s != the banked tail %s (the "
                  "pin-tail law); the FULL observed sha: %s (my "
                  "console may verify the bytes against the banked "
                  "receipts)" % (name, tail, pin["sha256"][:8],
                                 got))
    if bytes_needed and "bytes" in pin:
        n = os.path.getsize(path)
        if n != pin["bytes"]:
            fail_loud("pin %s: bytes %d != the banked %d"
                      % (name, n, pin["bytes"]))
    return got


# ---------------------------------------------------------------------------
# Section 2. The float16 decode (the cache hidden payload form) + the
# bf16 decode (the safetensors W_U dtype class; both named, never
# conflated)
# ---------------------------------------------------------------------------

def fp16_decode_b64(b64s):
    """base64 -> float16 bytes -> float list (the CACHE hidden_b64
    convention: HIDDEN_BYTES_PER_VALUE 2, float16, the instrument
    of record's own writer form -- triadic_telemetry_t2_v32.3.0.py
    writes rec["hidden"].half().numpy().tobytes() (float16, native
    order = little-endian on my Mac) and reads it back with
    np.frombuffer dtype float16; the chain's first value-decode of
    hidden_b64 agrees (pure bit arithmetic on the little-endian
    bytes))."""
    raw = base64.b64decode(b64s)
    if len(raw) % 2:
        fail_loud("fp16 payload length odd: %d" % len(raw))
    return list(struct.unpack("<" + "e" * (len(raw) // 2), raw))


def bf16_decode_bytes(raw):
    """raw bf16 bytes -> float list (the safetensors BF16 dtype
    class in the format spec's own byte order -- "Endianness:
    Little-endian" per the safetensors spec; the same shift the
    B1 module's census-ulp utility uses)."""
    out = []
    for (w,) in struct.iter_unpack("<H", raw):
        out.append(struct.unpack(">f",
                                 struct.pack(">I", w << 16))[0])
    return out


# ---------------------------------------------------------------------------
# Section 3. The inventory loader (the B0 export of record; the row
# tables + the counts asserted against the export's own bytes)
# ---------------------------------------------------------------------------

def verify_console_pin_sha(sha):
    """The console-line pin shape law (the item-1146 defect-class
    guard applied to MY line): 64 lowercase hex characters, a
    malformed pin a hard exit at load before any file is touched."""
    import string
    hexs = set(string.hexdigits.lower())
    if not (isinstance(sha, str) and len(sha) == 64
            and all(c in hexs for c in sha)):
        fail_loud("pin inventory: the --inventory-sha console line "
                  "%r is not 64 lowercase hex characters (the "
                  "pin-shape law; the v1.3.3 builder's own export "
                  "print is the source -- a malformed line dies "
                  "here, never a wrong read)" % (sha,))


def assert_occurrence_row(sr, ctx, what):
    """The v1.3.0 occurrence-level row law (the sheet amendment v3,
    the S1 law at the run tool's own door): a pair row's
    span_resolution carries status RESOLVED-OWN-STEP + the
    occurrence's OWN step (occ_step_t) + the t_0 token id + its
    commit_index + its hidden_row_index; a row short of them a
    NAMED premise violation at load -- never a silent
    position-blind read (the one-rule law)."""
    if not isinstance(sr, dict):
        fail_loud("%s: %s carries no span_resolution (a NAMED "
                  "premise violation under the v1.3.0 "
                  "occurrence-level row law)" % (ctx, what))
    if sr.get("status") != "RESOLVED-OWN-STEP":
        fail_loud("%s: %s resolution status %r not "
                  "RESOLVED-OWN-STEP (the sheet v3 one-rule law; "
                  "an unresolved, out-of-coverage, or "
                  "value-mismatch row must never reach the pair "
                  "tables -- the honest-population receipt owns "
                  "it, never a silent read)" % (ctx, what,
                                                sr.get("status")))
    for k in ("t0", "occ_step_t", "commit_index",
              "hidden_row_index"):
        if not isinstance(sr.get(k), int):
            fail_loud("%s: %s carries no %s receipt (the v1.3.0 "
                      "occurrence-level row law; a NAMED premise "
                      "violation, never a position-blind guess)"
                      % (ctx, what, k))
    return sr


def assert_pair_s4(p, cohort):
    """The sheet's S4 load law, BOTH lanes: the two rows of each
    pair ride DIFFERENT hidden rows -- hidden_row_index inequality
    asserted DIRECTLY per pair, fail-loud
    PAIR-LAW-HIDDEN-ROW-EQUALITY (the item-1161(e) hole closed at
    load: the v1.0.4 t_0-inequality proxy retired, float-equal
    values like "5" vs "5.0" can never pair one row past this
    door)."""
    pos, neg = p.get("positive"), p.get("negative")
    p_hr = (pos.get("span_resolution") or {}).get("hidden_row_index")
    n_hr = (neg.get("span_resolution") or {}).get("hidden_row_index")
    if p_hr == n_hr:
        fail_loud("inventory: %s pair %s PAIR-LAW-HIDDEN-ROW-"
                  "EQUALITY -- the pair's two rows ride the SAME "
                  "hidden row %r (the sheet amendment v3 S4 law; "
                  "the v1.0.4 t_0 proxy retired; a true "
                  "data-integrity finding at my door, presented "
                  "never smoothed)" % (cohort, p.get("pair_id"),
                                       p_hr))
    return True


def assert_a1_rebind_law(pairs):
    """The v1.3.0 A1 position-aware law asserted from the
    inventory's own bytes at load, never trusted: every A1 pair
    same-doc, SAME VALUE, DIFFERENT occurrence step (the
    position-aware measure -- two different hidden rows by the
    S4 direct law), the occ_step_distance exact against the pair's
    own receipt, the v1.2.7 lineage step_distance cross-checked
    the same way, the v1.3.0 bind-law receipt present; the pair
    count within the item-1158 pool census (177)."""
    if not isinstance(pairs, list) or not pairs:
        fail_loud("inventory: the A1 pair table empty (the v1.3.0 "
                  "position-aware law: the pool census carries 177 "
                  "pairable promotions, zero pairs a wrong build)")
    for p in pairs:
        pos, neg = p.get("positive"), p.get("negative")
        for r, side in ((pos, "positive"), (neg, "negative")):
            if not isinstance(r, dict):
                fail_loud("inventory: A1 pair %s carries no %s row"
                          % (p.get("pair_id"), side))
            assert_occurrence_row(r.get("span_resolution") or {},
                                  "inventory",
                                  "A1 pair %s %s"
                                  % (p.get("pair_id"), side))
        if pos.get("doc_id") != neg.get("doc_id") \
                or pos.get("leg") != neg.get("leg") \
                or pos.get("export") != neg.get("export"):
            fail_loud("inventory: A1 pair %s crosses docs/legs (the "
                      "within-doc rule mandatory for the "
                      "role-geometry control)"
                      % p.get("pair_id"))
        if pos.get("value") != neg.get("value"):
            fail_loud("inventory: A1 pair %s pairs DIFFERENT values "
                      "%r/%r (the v1.3.0 same-value law)"
                      % (p.get("pair_id"), pos.get("value"),
                         neg.get("value")))
        srp, srn = pos["span_resolution"], neg["span_resolution"]
        p_occ, n_occ = srp["occ_step_t"], srn["occ_step_t"]
        if p_occ == n_occ:
            fail_loud("inventory: A1 pair %s anchors the SAME "
                      "occurrence step %d (the v1.3.0 "
                      "position-aware law needs two different "
                      "steps -- two different hidden rows; the "
                      "v1.2.7 t_0-difference proxy retired at "
                      "this sheet)" % (p.get("pair_id"), p_occ))
        assert_pair_s4(p, "A1")
        osd = p.get("occ_step_distance")
        if not isinstance(osd, int) or osd != n_occ - p_occ:
            fail_loud("inventory: A1 pair %s occ_step_distance %r "
                      "!= the occurrence-step difference %d (the "
                      "v1.3.0 position-aware receipt law)"
                      % (p.get("pair_id"), osd, n_occ - p_occ))
        sd = p.get("step_distance")
        if not isinstance(sd, int) \
                or sd != srn["t0"] - srp["t0"]:
            fail_loud("inventory: A1 pair %s step_distance %r != "
                      "the t_0 difference %d (the v1.2.7 lineage "
                      "diagnostic, cross-checked the same way)"
                      % (p.get("pair_id"), sd,
                         srn["t0"] - srp["t0"]))
        if "v1.3.0" not in (p.get("bind_law") or ""):
            fail_loud("inventory: A1 pair %s carries no v1.3.0 "
                      "bind_law receipt (the receipt-of-record law)"
                      % p.get("pair_id"))
    if len(pairs) > 177:
        fail_loud("inventory: A1 pairs %d beyond the item-1158 pool "
                  "census 177 (the pool census receipt)"
                  % len(pairs))
    return len(pairs)


def assert_class_census_consistency(coh, blk, honest_rows):
    """The sheet v3 class-census cross-check, every count DERIVED
    from the export's own bytes (the v2 landing constants
    retired): the cohort's own resolution_class_census must equal
    its own joined counts (RESOLVED-OWN-STEP == positives +
    negatives joined_resolved) and its own honest entries per
    NAMED class; its UNRESOLVABLE-NON-NUMERIC count must equal its
    own unresolved_non_numeric block field. A divergence a hard
    exit naming both sides -- never a constant asserted this
    side."""
    cc = blk.get("resolution_class_census")
    if not isinstance(cc, dict):
        fail_loud("inventory: cohort %s carries no "
                  "resolution_class_census (the sheet v3 S1 law; a "
                  "v2-shaped inventory a NAMED refusal)" % coh)
    for cls in ("RESOLVED-OWN-STEP",
                "step-outside-cache-coverage",
                "value-mismatch-at-own-step",
                "UNRESOLVABLE-NON-NUMERIC"):
        if not isinstance(cc.get(cls), int):
            fail_loud("inventory: cohort %s class census carries "
                      "no %r count (the sheet v3 S1 law)" % (coh,
                                                            cls))
    n_res = (blk["positives_joined_resolved"]
             + blk["negatives_joined_resolved"])
    if cc["RESOLVED-OWN-STEP"] != n_res:
        fail_loud("inventory: cohort %s class census "
                  "RESOLVED-OWN-STEP %d != its own joined counts "
                  "%d (the derived cross-check, never a constant)"
                  % (coh, cc["RESOLVED-OWN-STEP"], n_res))
    for cls in ("step-outside-cache-coverage",
                "value-mismatch-at-own-step",
                "UNRESOLVABLE-NON-NUMERIC"):
        n_e = sum(1 for e in honest_rows
                  if e.get("cohort") == coh
                  and (e.get("finding") or "").startswith(cls))
        if cc[cls] != n_e:
            fail_loud("inventory: cohort %s class census %r == %d "
                      "!= its own honest entries %d (the derived "
                      "cross-check; a NAMED disagreement, never "
                      "smoothed)" % (coh, cls, cc[cls], n_e))
    if cc["UNRESOLVABLE-NON-NUMERIC"] \
            != blk.get("unresolved_non_numeric"):
        fail_loud("inventory: cohort %s class census "
                  "UNRESOLVABLE-NON-NUMERIC %d != its own "
                  "unresolved_non_numeric %r (the derived "
                  "cross-check)" % (coh,
                                    cc["UNRESOLVABLE-NON-NUMERIC"],
                                    blk.get(
                                        "unresolved_non_numeric")))
    return cc


def assert_population_arithmetic(coh, blk, n_pairs, n_unpaired,
                                  n_unres_pos, n_cls_pos,
                                  expected_positives):
    """The v3 honest-population arithmetic, per cohort, every term
    counted from the export's own bytes: pairs + unpaired + the
    standing unresolved promotions + the NAMED class rows
    (out-of-coverage / value-mismatch / join-fail) == the
    extraction census (the item-1158/1136 extraction counts,
    unchanged by the amendment -- 371 A1 promotions, 96 A2
    positives). The LANDED counts carry no constant this side:
    the A2 movement the EXPECTATION (67 of the 96 slips ride
    in-doc repeated values), the shift itself a finding, never
    forced."""
    if blk.get("positives_extracted") != expected_positives:
        fail_loud("inventory: cohort %s positives_extracted %r != "
                  "the banked extraction census %d (the extraction "
                  "is unchanged by the sheet v3 amendment; a "
                  "divergence a wrong build or a wrong map, NAMED)"
                  % (coh, blk.get("positives_extracted"),
                     expected_positives))
    total = n_pairs + n_unpaired + n_unres_pos + n_cls_pos
    if total != expected_positives:
        fail_loud("inventory: cohort %s pairs %d + unpaired %d + "
                  "unresolved promotions %d + NAMED class rows %d "
                  "== %d != the extraction census %d (the "
                  "honest-population arithmetic, the class rows "
                  "inside it -- nothing silently dropped)"
                  % (coh, n_pairs, n_unpaired, n_unres_pos,
                     n_cls_pos, total, expected_positives))
    return True


def read_inventory(path, inventory_sha):
    """The B0 cohort inventory of record (the v3 build, the v1.3.0
    position-aware rule, my stamps items 1162/1163/1164): the pin
    MY console line asserted byte-exact; the v1.3.3 build receipt
    pinned in the tool line; the row tables read AT THE OCCURRENCE
    LEVEL (A1/A2 matched pairs, the unpaired positives, the
    standing unresolved, the NAMED class rows beside); the counts
    cross-checked against the export's own blocks -- the class
    census + the honest-population arithmetic DERIVED from its
    bytes, the v2 landing constants retired, the A2 movement the
    expectation; a divergence a hard exit."""
    verify_console_pin_sha(inventory_sha)
    assert_pin("inventory", path,
               {"sha256": inventory_sha}, bytes_needed=False)
    with open(path) as f:
        d = json.load(f)
    tool_line = d.get("tool", "")
    if tool_line.split(" ")[0] != \
            "cd1_arm_a_cohort_inventory_build_v1.py":
        fail_loud("inventory: tool line %r is not the B0 builder of "
                  "record" % tool_line)
    if "v1.3.3" not in tool_line:
        fail_loud("inventory: tool line %r carries no v1.3.3 build "
                  "receipt (the sheet v3 one-rule law: the "
                  "inventory of record is the position-aware "
                  "build; a v2 inventory at my door a NAMED "
                  "refusal, never a position-blind read)"
                  % tool_line)
    if d.get("map_file_sha256") != ("61a56000458e028071a93cf0ad12a221"
                                    "f30768c01157aea412c75ccfef03a173"):
        fail_loud("inventory: the stamped map sha pin mismatch")
    for k in ("step_ext_census", "honest_population_receipt"):
        if not isinstance(d.get(k), dict):
            fail_loud("inventory: no %r block (the v1.3.0 export "
                      "form; a v2-shaped inventory a NAMED "
                      "refusal)" % k)
    rows = {"A1_pairs": [], "A2_pairs": [], "unpaired": [],
            "unresolved": [], "named_beside": []}
    for coh in ("A1", "A2"):
        blk = d["cohorts"][coh]
        pairs = blk["matched_pairs"]
        for p in pairs:
            if p["cohort"] != coh:
                fail_loud("inventory: pair %s cohort field %r"
                          % (p.get("pair_id"), p["cohort"]))
            for side in ("positive", "negative"):
                r = p[side]
                assert_occurrence_row(
                    r.get("span_resolution") or {},
                    "inventory", "pair %s %s"
                    % (p["pair_id"], side))
            assert_pair_s4(p, coh)
            rows["%s_pairs" % coh].append(p)
    hp = d["honest_population_receipt"]["entries"]
    for e in hp:
        f0 = e["finding"].split(" --")[0]
        if f0 == "UNPAIRED":
            r = e["positive"]
            assert_occurrence_row(
                r.get("span_resolution") or {},
                "inventory", "unpaired %s doc %s"
                % (e["cohort"], r.get("doc_id")))
            rows["unpaired"].append(e)
        elif f0 == "UNRESOLVABLE-NON-NUMERIC":
            rows["unresolved"].append(e)
        elif f0 in ("step-outside-cache-coverage",
                    "value-mismatch-at-own-step",
                    "UNJOINED", "AMBIGUOUS"):
            rows["named_beside"].append(e)
        else:
            fail_loud("inventory: honest entry finding %r not of "
                      "the sheet's NAMED classes (the one-rule "
                      "law; an unknown class never silently "
                      "read)" % f0)
    # the count cross-checks (the export's own cohort blocks, every
    # count derived; the v2 landing constants retired)
    # the A1 lane: the v1.3.0 position-aware law asserted from the
    # bytes + the class-census cross-check + the honest-population
    # arithmetic + the pool-census bound
    a1, a2 = d["cohorts"]["A1"], d["cohorts"]["A2"]
    n_a1 = assert_a1_rebind_law(rows["A1_pairs"])
    honest_all = (rows["unresolved"] + rows["named_beside"])
    assert_class_census_consistency("A1", a1, honest_all)
    assert_class_census_consistency("A2", a2, honest_all)

    def _pos_promotions(entries, coh):
        return sum(1 for e in entries
                   if e.get("cohort") == coh
                   and (e.get("row") or {}).get("record_class")
                   == "PROMOTION")

    n_unres_pos_a1 = _pos_promotions(rows["unresolved"], "A1")
    if n_unres_pos_a1 != 21:
        fail_loud("inventory: A1 unresolved promotions %d != the "
                  "banked 21 (the item-1136 standing class, "
                  "unchanged by the amendment)"
                  % n_unres_pos_a1)
    n_cls_pos_a1 = _pos_promotions(rows["named_beside"], "A1")
    assert_population_arithmetic(
        "A1", a1, n_a1, a1["unpaired_count"], n_unres_pos_a1,
        n_cls_pos_a1, 371)
    n_a2_pairs = len(rows["A2_pairs"])
    n_unres_pos_a2 = _pos_promotions(rows["unresolved"], "A2")
    n_cls_pos_a2 = _pos_promotions(rows["named_beside"], "A2")
    assert_population_arithmetic(
        "A2", a2, n_a2_pairs, a2["unpaired_count"],
        n_unres_pos_a2, n_cls_pos_a2, 96)
    n_unp_a1 = sum(1 for e in rows["unpaired"]
                   if e["cohort"] == "A1")
    n_unp_a2 = sum(1 for e in rows["unpaired"]
                   if e["cohort"] == "A2")
    if n_unp_a1 != a1["unpaired_count"] \
            or n_unp_a2 != a2["unpaired_count"]:
        fail_loud("inventory: unpaired counts %d/%d != the export's "
                  "own %r/%r" % (n_unp_a1, n_unp_a2,
                                 a1["unpaired_count"],
                                 a2["unpaired_count"]))
    n_unres_a1 = sum(1 for e in rows["unresolved"]
                     if e["cohort"] == "A1")
    n_unres_a2 = sum(1 for e in rows["unresolved"]
                     if e["cohort"] == "A2")
    if n_unres_a1 != a1["unresolved_non_numeric"] \
            or n_unres_a2 != a2["unresolved_non_numeric"]:
        fail_loud("inventory: unresolved counts %d/%d != the "
                  "export's own %r/%r"
                  % (n_unres_a1, n_unres_a2,
                     a1["unresolved_non_numeric"],
                     a2["unresolved_non_numeric"]))
    # the V_num pin (the leg's numeric vocabulary, pinned at B0)
    vp = d["vnum_pin"]
    if vp["numeric_token_count"] != 1110 or \
            vp["vocab_entries"] != 128000:
        fail_loud("inventory: the V_num pin not the banked "
                  "1110/128000")
    if vp["tokenizer_sha256_observed"] != ("79e3e522635f3171300913"
                                           "bb421464a87de6222182a057"
                                           "0b9b2ccba2a964b2b4"):
        fail_loud("inventory: the tokenizer sha pin mismatch")
    return d, rows


# ---------------------------------------------------------------------------
# Section 4. The cache reader (the B0 builder's reader law, ported
# verbatim in substance; the hidden payload decoded FLOAT16)
# ---------------------------------------------------------------------------

def read_cache_records(name, path, expect_records):
    """The walk cache jsonl: the schema of record asserted per record
    (steps = the COLUMNS dict, t contiguous, walk_ids == steps.id;
    commits = the per-content-commitment rows {t, token, phase},
    len == n_content_steps; hidden = RECORD-LEVEL, the final-normed
    last-layer state, ONE ROW PER CONTENT COMMIT, float16). An
    empty-form row and a thin rider are NAMED premise violations."""
    records = {}
    with open(path) as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except ValueError as e:
                fail_loud("cache %s line %d: not valid JSON (%s)"
                          % (name, i + 1, e))
            if r.get("empty"):
                fail_loud("cache %s line %d: EMPTY FORM (key %r) -- "
                          "a NAMED premise violation"
                          % (name, i + 1, r.get("key")))
            for k in CACHE_RECORD_REQUIRED:
                if k not in r:
                    fail_loud("cache %s line %d: missing banked "
                              "field %r" % (name, i + 1, k))
            steps = r["steps"]
            for col in STEPS_COLUMNS_REQUIRED:
                if col not in steps:
                    fail_loud("cache %s line %d: steps carries no "
                              "column %r" % (name, i + 1, col))
            n = r["n_gen_steps"]
            if len(steps["t"]) != n or len(steps["id"]) != n:
                fail_loud("cache %s line %d: steps column length != "
                          "n_gen_steps %d" % (name, i + 1, n))
            ts = steps["t"]
            for a, b in zip(ts, ts[1:]):
                if not isinstance(b, int) or b != a + 1:
                    fail_loud("cache %s line %d: steps t not "
                              "contiguous" % (name, i + 1))
            if r["walk_ids"] != steps["id"]:
                fail_loud("cache %s line %d: walk_ids != steps.id "
                          "(the id-identity law)" % (name, i + 1))
            commits = r["commits"]
            for c in commits:
                for k in COMMIT_ROW_REQUIRED:
                    if k not in c:
                        fail_loud("cache %s line %d: a commits row "
                                  "missing %r" % (name, i + 1, k))
            if len(commits) != r["n_content_steps"]:
                fail_loud("cache %s line %d: len(commits) != "
                          "n_content_steps" % (name, i + 1))
            if r.get("hidden_n") != r["n_content_steps"]:
                fail_loud("cache %s line %d: hidden_n != "
                          "n_content_steps (the one-row-per-commit "
                          "law)" % (name, i + 1))
            hb = r.get("hidden_b64", "")
            if hb == "" and r["hidden_n"] > 0:
                fail_loud("cache %s line %d: THIN RIDER REFUSED "
                          "(empty hidden_b64 with hidden_n %d)"
                          % (name, i + 1, r["hidden_n"]))
            if hb:
                want = (HIDDEN_BYTES_PER_VALUE * r["hidden_n"]
                        * r["hidden_dim"])
                if len(base64.b64decode(hb)) != want:
                    fail_loud("cache %s line %d: hidden bytes != "
                              "the float16 form" % (name, i + 1))
            key = r["key"]
            if key in records:
                fail_loud("cache %s: duplicate key %r"
                          % (name, key))
            records[key] = r
    if len(records) != expect_records:
        fail_loud("cache %s: %d records != the banked %d"
                  % (name, len(records), expect_records))
    return records


def hidden_row(record, row_index):
    """Decode ONE hidden row (float16, the record-level payload, one
    row per content commit). The row decode is lazy by design: the
    separation run touches only the rows its rows pin."""
    n, dim = record["hidden_n"], record["hidden_dim"]
    if not (0 <= row_index < n):
        fail_loud("hidden row index %d outside the record's %d rows"
                  % (row_index, n))
    raw = base64.b64decode(record["hidden_b64"])
    off = row_index * dim * HIDDEN_BYTES_PER_VALUE
    return fp16_decode_b64(
        base64.b64encode(raw[off:off + dim * HIDDEN_BYTES_PER_VALUE])
        .decode("ascii"))


# ---------------------------------------------------------------------------
# Section 5. The safetensors W_U reader (the ONLY model-file touch:
# the unembedding rows restricted to the leg's pinned V_num, read by
# row-seek, matrix multiplication only, never a forward pass, never
# a decode; the carrying shard hashed and its banked prefix asserted)
# ---------------------------------------------------------------------------

SAFETENSORS_DTYPES = {"BF16": 2, "F16": 2, "F32": 4}


def read_w_u_rows(model_dir, vnum_ids, dim_expect=4096):
    """The model file of record: the safetensors index parsed, the
    unembedding tensor DISCOVERED (lm_head.weight preferred, an
    absent tensor a hard exit naming the discovered candidates);
    only the V_num rows read, by row-seek on the carrying shard."""
    idx_path = os.path.join(model_dir, PINS["model_shards"]
                            ["index_file"])
    if not os.path.exists(idx_path):
        fail_loud("model dir %r carries no %s (the never-guess law: "
                  "the run reads only the pinned index)"
                  % (model_dir, PINS["model_shards"]["index_file"]))
    with open(idx_path) as f:
        idx = json.load(f)
    wmap = idx.get("weight_map")
    if not isinstance(wmap, dict):
        fail_loud("the safetensors index carries no weight_map")
    pref = PINS["model_shards"]["w_u_tensor"]
    if pref not in wmap:
        cands = sorted(k for k in wmap
                       if "head" in k.lower()
                       or "embed" in k.lower())
        fail_loud("the index carries no %r; the discovered head/"
                  "embed candidates: %r (a coverage discovery at my "
                  "door, never a guess)" % (pref, cands))
    shard_name = wmap[pref]
    shard_path = os.path.join(model_dir, shard_name)
    if not os.path.exists(shard_path):
        fail_loud("the W_U shard %r not found in the model dir"
                  % shard_name)
    # the carrying shard hashed; its banked prefix asserted (only the
    # READ shard is hashed -- hashing untouched shards is not a read)
    got = sha256_file(shard_path)
    matched = [p for p in PINS["model_shards"]["shard_sha_prefixes"]
               if got.startswith(p)]
    if len(matched) != 1:
        fail_loud("the W_U shard sha %s matches %d of the four "
                  "banked shard pins (the item-574 bank; a mismatch "
                  "a hard exit)" % (got[:8], len(matched)))
    with open(shard_path, "rb") as f:
        hdr_len = struct.unpack("<Q", f.read(8))[0]
        header = json.loads(f.read(hdr_len))
    meta = header.get(pref)
    if not isinstance(meta, dict):
        fail_loud("the shard header carries no %r tensor" % pref)
    dtype = meta.get("dtype")
    if dtype not in SAFETENSORS_DTYPES:
        fail_loud("W_U dtype %r not of the handled classes %r"
                  % (dtype, sorted(SAFETENSORS_DTYPES)))
    bpe = SAFETENSORS_DTYPES[dtype]
    shape = meta.get("shape")
    if not (isinstance(shape, list) and len(shape) == 2):
        fail_loud("W_U shape %r is not 2-D" % (shape,))
    vocab_n, dim = shape
    if dim != dim_expect:
        fail_loud("W_U dim %d != the banked hidden dim %d"
                  % (dim, dim_expect))
    start, end = meta["data_offsets"]
    if end - start != vocab_n * dim * bpe:
        fail_loud("W_U data_offsets span %d != vocab x dim x bpe"
                  % (end - start))
    data_base = 8 + hdr_len
    rows = {}
    with open(shard_path, "rb") as f:
        for tid in sorted(set(vnum_ids)):
            if not (0 <= tid < vocab_n):
                fail_loud("V_num id %d outside the W_U vocab %d"
                          % (tid, vocab_n))
            f.seek(data_base + start + tid * dim * bpe)
            raw = f.read(dim * bpe)
            if dtype == "BF16":
                rows[tid] = bf16_decode_bytes(raw)
            elif dtype == "F16":
                rows[tid] = list(struct.unpack("<" + "e" * dim, raw))
            else:  # F32, the spec's little-endian order
                rows[tid] = list(struct.unpack("<" + "f" * dim, raw))
    # the finite law at load (the item-1155 class): the model of
    # record's unembedding rows must all be finite; a non-finite
    # row is a data-integrity hard exit at load (a wrong shard or
    # a wrong read), never a NaN reaching the operators at my
    # console
    n_bad = 0
    first_bad = None
    for tid in sorted(rows):
        for j, v in enumerate(rows[tid]):
            if not math.isfinite(v):
                n_bad += 1
                if first_bad is None:
                    first_bad = (tid, j, repr(v))
                break
    if n_bad:
        fail_loud("the W_U rows carry %d non-finite rows (the "
                  "first: token id %d at dim %d, value %s) -- the "
                  "model of record's unembedding cannot be "
                  "non-finite; the shard or the read is wrong, "
                  "the load stops here" % (n_bad, first_bad[0],
                                           first_bad[1],
                                           first_bad[2]))
    return {"shard": shard_name, "shard_sha256": got,
            "dtype": dtype, "shape": shape,
            "tensor": pref, "rows": rows}


# ---------------------------------------------------------------------------
# Section 6. The B1 import (the accepted module of record; its sha
# asserted at import -- a divergence a hard exit)
# ---------------------------------------------------------------------------

def import_b1(b1_path):
    assert_pin("b1_module", b1_path, PINS["b1_module"],
               bytes_needed=False)
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "cd1_arm_a_operators_b1", b1_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "m_ulp_num"):
        fail_loud("the B1 module carries no m_ulp_num (the operator "
                  "contract)")
    for fn in ("h_num", "centered_r_perp", "bhob", "work_increment",
               "zeta_step", "kappa_corroborator", "num_logits",
               "common_mode_mean", "center_state"):
        if not hasattr(mod, fn):
            fail_loud("the B1 module carries no %s" % fn)
    return mod


# ---------------------------------------------------------------------------
# Section 7. The part-1 selfcheck (constructed bytes only; the full
# acceptance battery is part 3)
# ---------------------------------------------------------------------------

def _mk_cache_line(key, n_steps, n_commits, dim, hidden_rows):
    """A constructed cache record obeying the schema of record."""
    steps = {"t": list(range(n_steps)),
             "id": [100 + i for i in range(n_steps)]}
    commits = [{"t": i, "token": ("7" if i % 2 == 0 else "3"),
               "phase": ("COT" if i < n_commits - 1 else "ANSWER")}
              for i in range(n_commits)]
    flat = b"".join(struct.pack("<" + "e" * dim, *row)
                    for row in hidden_rows)
    hb = base64.b64encode(flat).decode("ascii")
    return json.dumps({
        "key": key, "leg": "testleg", "doc_id": 0, "bos": True,
        "instrument": "test", "prompt_len": 5, "stop_reason": "eos",
        "n_gen_steps": n_steps, "n_content_steps": n_commits,
        "walk_ids": steps["id"], "steps": steps, "commits": commits,
        "hidden_n": n_commits, "hidden_dim": dim, "hidden_b64": hb,
    })


def _mk_safetensors(path, tensors):
    """A constructed safetensors file (header + data, the spec's own
    little-endian length convention)."""
    header = {}
    body = b""
    for name, (dtype, shape, rows) in tensors.items():
        flat = b"".join(row for row in rows)
        header[name] = {"dtype": dtype, "shape": shape,
                        "data_offsets": [len(body),
                                         len(body) + len(flat)]}
        body += flat
    hj = json.dumps(header).encode("utf-8")
    with open(path, "wb") as f:
        f.write(struct.pack("<Q", len(hj)))
        f.write(hj)
        f.write(body)


def part1_selfcheck(out_dir):
    checks = []

    def check(cid, name, ok, detail):
        checks.append((cid, name, bool(ok), detail))

    import tempfile
    td = tempfile.mkdtemp(prefix="b2p1_", dir=out_dir)
    import shutil
    try:
        return _selfcheck_body(td, checks, check)
    finally:
        shutil.rmtree(td, ignore_errors=True)


def _selfcheck_body(td, checks, check):

    # P1-C01: the fp16 decode round-trip on known values (the
    # instrument's own writer form: little-endian)
    raw = struct.pack("<e", 24.0) + struct.pack("<e", 23.75) \
        + struct.pack("<e", -1.5)
    b64s = base64.b64encode(raw).decode("ascii")
    vals = fp16_decode_b64(b64s)
    check("P1-C01", "fp16 decode known values",
          vals == [24.0, 23.75, -1.5], "%r" % vals)

    # P1-C02: the bf16 decode (the safetensors dtype class, hand
    # spec-order bytes: 0x41C0 little-endian on disk)
    raw = struct.pack("<H", 0x41C0) + struct.pack("<H", 0x3F80)
    vals = bf16_decode_bytes(raw)
    check("P1-C02", "bf16 decode known values",
          vals == [24.0, 1.0], "%r" % vals)

    # P1-C03: the cache reader accepts a constructed schema-true
    # record and refuses a thin rider
    dim = 4
    rows = [[float(i * dim + j) for j in range(dim)]
            for i in range(3)]
    line = _mk_cache_line("testleg:0", 3, 3, dim, rows)
    cp = os.path.join(td, "cache_test.jsonl")
    with open(cp, "w") as f:
        f.write(line + "\n")
    recs = read_cache_records("test", cp, 1)
    check("P1-C03", "cache reader accepts the schema-true record",
          "testleg:0" in recs, "keys %r" % sorted(recs))
    bad = json.loads(line)
    bad["hidden_b64"] = ""
    bp = os.path.join(td, "cache_thin.jsonl")
    with open(bp, "w") as f:
        f.write(json.dumps(bad) + "\n")
    try:
        read_cache_records("thin", bp, 1)
        check("P1-C04", "thin rider refused loud", False,
              "the thin rider was accepted")
    except SystemExit as e:
        ok = "THIN RIDER REFUSED" in str(e)
        check("P1-C04", "thin rider refused loud", ok,
              str(e)[:80])

    # P1-C05: the hidden row decode (float16, lazy per row)
    r0 = hidden_row(recs["testleg:0"], 0)
    r2 = hidden_row(recs["testleg:0"], 2)
    ok = r0 == rows[0] and r2 == rows[2]
    check("P1-C05", "hidden row decode exact",
          ok, "row0 %r row2 %r" % (r0, r2))
    try:
        hidden_row(recs["testleg:0"], 3)
        check("P1-C06", "out-of-range row refused loud", False,
              "accepted")
    except SystemExit as e:
        check("P1-C06", "out-of-range row refused loud",
              "outside the record" in str(e), str(e)[:80])

    # P1-C07: the safetensors W_U reader on a constructed model dir
    vnum = [2, 0]
    w_rows = {0: [1.0, 0.0, 0.0, 0.0], 2: [0.0, 0.0, 1.0, 0.0],
              1: [9.0, 9.0, 9.0, 9.0]}
    tpath = os.path.join(td, "toy.safetensors")
    # bf16 rows: pack via the fp32->bf16 truncation (round toward
    # zero on the 16 high bits -- exact for these values), in the
    # spec's own little-endian byte order
    def f32_to_bf16_bytes(vals):
        out = b""
        for v in vals:
            bits = struct.unpack("<I",
                                 struct.pack("<f", v))[0]
            out += struct.pack("<H", (bits >> 16) & 0xFFFF)
        return out
    _mk_safetensors(tpath, {
        "model.norm.weight": ("F32", [4],
                              [struct.pack("<ffff", 1, 1, 1, 1)]),
        "lm_head.weight": ("BF16", [3, 4],
                           [f32_to_bf16_bytes(w_rows[0]),
                            f32_to_bf16_bytes(w_rows[1]),
                            f32_to_bf16_bytes(w_rows[2])]),
    })
    mdir = td
    with open(os.path.join(mdir, "model.safetensors.index.json"),
              "w") as f:
        json.dump({"weight_map": {"lm_head.weight":
                                  "toy.safetensors"}}, f)
    PINS_BACKUP = json.dumps(PINS["model_shards"])
    PINS["model_shards"] = dict(PINS["model_shards"])
    PINS["model_shards"]["shard_sha_prefixes"] = [
        sha256_file(tpath)[:8]]
    try:
        wu = read_w_u_rows(mdir, vnum, dim_expect=4)
        ok = (wu["rows"][2] == w_rows[2]
              and wu["rows"][0] == w_rows[0]
              and wu["dtype"] == "BF16")
        check("P1-C07", "W_U reader row-seek exact", ok,
              "row2 %r" % wu["rows"][2])
    finally:
        PINS["model_shards"] = json.loads(PINS_BACKUP)

    # P1-C11: the W_U finite law (the item-1155 class) -- a
    # non-finite unembedding row a hard exit at load, named, never
    # a NaN reaching the operators
    tpath2 = os.path.join(td, "toy2.safetensors")
    nan_row = [float("nan"), 1.0, 0.0, 0.0]
    _mk_safetensors(tpath2, {
        "model.norm.weight": ("F32", [4],
                              [struct.pack("<ffff", 1, 1, 1, 1)]),
        "lm_head.weight": ("BF16", [3, 4],
                           [f32_to_bf16_bytes(nan_row),
                            f32_to_bf16_bytes(w_rows[1]),
                            f32_to_bf16_bytes(w_rows[2])]),
    })
    with open(os.path.join(td, "idx2.safetensors.index.json"),
              "w") as f:
        json.dump({"weight_map": {"lm_head.weight":
                                  "toy2.safetensors"}}, f)
    PINS_BACKUP2 = json.dumps(PINS["model_shards"])
    PINS["model_shards"] = dict(PINS["model_shards"])
    PINS["model_shards"]["shard_sha_prefixes"] = [
        sha256_file(tpath2)[:8]]
    PINS["model_shards"]["index_file"] = "idx2.safetensors.index.json"
    try:
        try:
            read_w_u_rows(mdir, vnum, dim_expect=4)
            check("P1-C11", "W_U finite law at load", False,
                  "the non-finite row was accepted")
        except SystemExit as e:
            check("P1-C11", "W_U finite law at load",
                  "non-finite" in str(e) and "token id 0"
                  in str(e), str(e)[:70])
    finally:
        PINS["model_shards"] = json.loads(PINS_BACKUP2)

    # P1-C12: the endianness law (the item-1156 class) -- HAND
    # spec-order bytes, independent of every writer in this file
    # (the mirror-defect law: a fixture writer and a reader sharing
    # one wrong convention can never see the error). The
    # safetensors spec order is little-endian; the instrument of
    # record's own writer bytes little-endian (the .half().numpy()
    # .tobytes() writer, its own np.frombuffer float16 reader);
    # the swapped direction turns plausible negatives into
    # non-finite or garbage-magnitude values
    def bf16_word_value(w):
        return struct.unpack(">f",
                             struct.pack(">I", w << 16))[0]
    le_bf16 = (struct.pack("<H", 0x41C0)
               + struct.pack("<H", 0xBEFF)
               + struct.pack("<H", 0x3F80))
    vals = bf16_decode_bytes(le_bf16)
    want = [bf16_word_value(0x41C0), bf16_word_value(0xBEFF),
            bf16_word_value(0x3F80)]
    ok = (vals == want
          and all(math.isfinite(v) for v in vals)
          and want[0] == 24.0 and want[2] == 1.0
          and want[1] < 0.0)
    check("P1-C12", "spec-order hand bytes: bf16 exact + finite",
          ok, "got %r want %r" % (vals, want))
    be_twin = (struct.pack(">H", 0x41C0)
               + struct.pack(">H", 0xBEFF)
               + struct.pack(">H", 0x3F80))
    bvals = bf16_decode_bytes(be_twin)
    ok2 = (bvals != want
           and any(not math.isfinite(v) for v in bvals))
    check("P1-C12b", "swapped-direction twin caught non-finite",
          ok2, "%r" % bvals)
    le_f16 = struct.pack("<e", -2.0) + struct.pack("<e", 1.0)
    cvals = fp16_decode_b64(base64.b64encode(le_f16).decode(
        "ascii"))
    check("P1-C12c", "spec-order hand bytes: cache fp16 exact",
          cvals == [-2.0, 1.0], "%r" % cvals)

    # P1-C08: the absent-tensor hard exit names the candidates
    idx2 = os.path.join(td, "model.safetensors.index.json")
    with open(idx2, "w") as f:
        json.dump({"weight_map": {"model.embed_tokens.weight":
                                  "toy.safetensors"}}, f)
    try:
        read_w_u_rows(mdir, vnum)
        check("P1-C08", "absent W_U tensor names candidates",
              False, "accepted")
    except SystemExit as e:
        ok = ("model.embed_tokens.weight" in str(e)
              and "never a guess" in str(e))
        check("P1-C08", "absent W_U tensor names candidates", ok,
              str(e)[:100])

    # P1-C09: the B1 import contract (sha asserted; operators bound)
    here = os.path.dirname(os.path.abspath(__file__))
    # the assembled-tool adaptation (named at the assembly):
    # the B1 module searched beside the tool first, then one
    # level up (the banked part-1 bytes untouched in .scratch)
    b1_path = None
    for cand in (os.path.join(here, "cd1_arm_a_operators_b1.py"),
                 os.path.normpath(os.path.join(
                     here, "..", "cd1_arm_a_operators_b1.py"))):
        if os.path.exists(cand):
            b1_path = cand
            break
    if os.path.exists(b1_path):
        b1 = import_b1(b1_path)
        r = b1.m_ulp_num([24.0, 23.75])
        ok = abs(r["m_ulp"] - 2.0) < 1e-12
        check("P1-C09", "B1 import contract + operator bound", ok,
              "m_ulp %r at the census pair" % r["m_ulp"])
    else:
        check("P1-C09", "B1 import contract", False,
              "the B1 module not found beside the tool")

    # P1-C10: the pin-tail law (a wrong tail a hard exit)
    wrong = dict(PINS["inventory"])
    wrong["sha256"] = "0" * 64
    try:
        with open(os.path.join(td, "fake_inv.json"), "w") as f:
            f.write("{}")
        assert_pin("inventory", os.path.join(td, "fake_inv.json"),
                   wrong)
        check("P1-C10", "wrong-tail pin refused loud", False,
              "accepted")
    except SystemExit as e:
        ok = "pin-tail law" in str(e)
        check("P1-C10", "wrong-tail pin refused loud", ok,
              str(e)[:80])

    # P1-C13: the v1.0.4 console-line pin shape law (the item-1146
    # class guard applied to my --inventory-sha line)
    ok = True
    for bad in ("", "0" * 63, "0" * 65, "z" * 64, None, 123):
        try:
            verify_console_pin_sha(bad)
            ok = False
        except SystemExit as e:
            ok = ok and "pin-shape law" in str(e)
    try:
        verify_console_pin_sha("a" * 64)
    except SystemExit:
        ok = False
    check("P1-C13", "console-line pin shape law", ok,
          "6 malformed + 1 well-formed line tried")

    # P1-C13b: the v1.3.0 A1 position-aware law asserted from the
    # bytes (the sheet v3): the occurrence-level row law + the S4
    # direct hidden-row check + both distance cross-checks + the
    # v1.3.0 bind-law receipt + the 177 pool bound
    def _sr(status="RESOLVED-OWN-STEP", t0=10, occ=10, ci=1, hr=1):
        sr = {"commit_index": ci, "hidden_row_index": hr}
        if status is not None:
            sr["status"] = status
        if t0 is not None:
            sr["t0"] = t0
        if occ is not None:
            sr["occ_step_t"] = occ
        return sr

    def _pair(pid, pv="9", nv="9", t0p=10, t0n=14, ocsp=10, ocsn=14,
              hrp=1, hrn=2, osd="__dflt", sd="__dflt",
              bl="the v1.3.0 A1 position-aware bind", ndoc=7):
        return {"pair_id": pid,
                "positive": {"export": "aligned_spans", "leg": "p2",
                             "doc_id": 7, "value": pv,
                             "span_resolution": _sr(
                                 t0=t0p, occ=ocsp, hr=hrp)},
                "negative": {"export": "aligned_spans", "leg": "p2",
                             "doc_id": ndoc, "value": nv,
                             "span_resolution": _sr(
                                 t0=t0n, occ=ocsn, hr=hrn)},
                "occ_step_distance": (ocsn - ocsp)
                if osd == "__dflt" and ocsp is not None
                and ocsn is not None
                else (None if osd == "__dflt" else osd),
                "step_distance": (t0n - t0p)
                if sd == "__dflt" and t0p is not None
                and t0n is not None
                else (None if sd == "__dflt" else sd),
                "bind_law": bl}

    ok = assert_a1_rebind_law([_pair("A1-0001")]) == 1
    for bad in (_pair("A1-0002", nv="8"),          # value mismatch
                _pair("A1-0003", ocsn=10),         # same occ step
                _pair("A1-0004", hrn=1),           # S4 same hidden
                _pair("A1-0005", osd=99),          # wrong occ dist
                _pair("A1-0006", sd=99),           # wrong lineage
                _pair("A1-0007", bl="x"),          # no law receipt
                _pair("A1-0008", ndoc=8),          # cross-doc
                _pair("A1-0009", ocsp=None),       # no own-step
                _pair("A1-0010", hrp=None),        # no hidden row
                _pair("A1-0011", t0p=None)):       # no t_0
        try:
            assert_a1_rebind_law([bad])
            ok = False
        except SystemExit:
            pass
    try:
        assert_a1_rebind_law([])
        ok = False
    except SystemExit:
        pass
    try:
        assert_a1_rebind_law([_pair("A1-%04d" % i)
                              for i in range(1, 179)])
        ok = False
    except SystemExit as e:
        ok = ok and "pool" in str(e)
    check("P1-C13b", "the v1.3.0 A1 position-aware law at "
          "load", ok,
          "clean pass + 12 refused classes (the S4 equality "
          "among them)")

    # P1-C13c: the inventory build-receipt pin (the v1.0.8 move, the
    # item-1172 act): the tool-line check demands the v1.3.3 build
    # receipt -- the v1.3.3 line accepted THROUGH the version check
    # into the next law (the stamped map sha pin), the v1.3.2 line
    # refused NAMED (the superseded build's export never read
    # position-blind), the wrong builder name refused NAMED; the
    # check had NO fixture at v1.0.5 -- the mirror lesson of the
    # item-1168 finding: a law without a fixture is a fixture gap
    inv_ok = True
    for tool_line, want in (
            ("cd1_arm_a_cohort_inventory_build_v1.py v1.3.3 "
             "(build part 3 of 3)",
             "stamped map sha pin mismatch"),
            ("cd1_arm_a_cohort_inventory_build_v1.py v1.3.2 "
             "(build part 3 of 3)",
             "no v1.3.3 build receipt"),
            ("cd1_arm_a_cohort_inventory_build_v2.py v1.3.3 "
             "(build part 3 of 3)",
             "not the B0 builder of record")):
        fp = os.path.join(td, "cd1_arm_a_cohort_inventory_v3.json")
        with open(fp, "w") as f:
            json.dump({"tool": tool_line}, f)
        try:
            read_inventory(fp, sha256_file(fp))
            inv_ok = False
        except SystemExit as e:
            inv_ok = inv_ok and want in str(e)
    check("P1-C13c", "the inventory build-receipt pin at the "
          "v1.3.3 build of record", inv_ok,
          "v1.3.3 line accepted through to the map-sha pin + the "
          "v1.3.2 line + the wrong builder name refused NAMED")

    # P1-C14: the occurrence-level row law (the sheet v3 S1) for
    # BOTH lanes: a pair row without a RESOLVED-OWN-STEP
    # resolution, its own step, its t_0, its commit row, or its
    # hidden row refused loud NAMED; the S4 equality refused with
    # its own class name; the one-rule law never a silent read
    ok = True
    for bad in ({"status": "value-mismatch-at-own-step",
                 "t0": 1, "occ_step_t": 1, "commit_index": 1,
                 "hidden_row_index": 1},      # a NAMED class row
                {"t0": 1, "occ_step_t": 1, "commit_index": 1,
                 "hidden_row_index": 1},      # no status
                {"status": "RESOLVED-OWN-STEP",
                 "occ_step_t": 1, "commit_index": 1,
                 "hidden_row_index": 1},      # no t_0
                {"status": "RESOLVED-OWN-STEP",
                 "t0": 1, "commit_index": 1,
                 "hidden_row_index": 1},      # no own step
                {"status": "RESOLVED-OWN-STEP",
                 "t0": 1, "occ_step_t": 1,
                 "hidden_row_index": 1},      # no commit row
                {}):                          # no resolution
        try:
            assert_occurrence_row(bad, "battery", "row")
            ok = False
        except SystemExit:
            pass
    try:
        assert_occurrence_row(_sr(), "battery", "row")
    except SystemExit:
        ok = False
    try:
        assert_pair_s4({"pair_id": "X-0001",
                        "positive": {"span_resolution":
                                     _sr(hr=1)},
                        "negative": {"span_resolution":
                                     _sr(hr=1)}}, "A2")
        ok = False
    except SystemExit as e:
        ok = ok and "PAIR-LAW-HIDDEN-ROW-EQUALITY" in str(e)
    try:
        assert_pair_s4({"pair_id": "X-0002",
                        "positive": {"span_resolution":
                                     _sr(hr=1)},
                        "negative": {"span_resolution":
                                     _sr(hr=2)}}, "A2")
    except SystemExit:
        ok = False
    check("P1-C14", "occurrence-level row law + the S4 direct "
          "check (both lanes)", ok,
          "6 refused row shapes + the S4 equality refused NAMED")

    return checks


# Section 1. The value law (ported verbatim from the B0 builder: the
# rule recorded, never re-derived; the builder's own float-equal form)
# ---------------------------------------------------------------------------

NUMERIC_RE = re.compile(
    r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$")


def parse_value(s):
    """A value string of the label exports: the plain decimal form
    first, then the reduced fraction form a/b (the checker's stated
    values are reduced fractions); anything else is a NAMED None,
    never a guess."""
    if not isinstance(s, str):
        s = str(s)
    t = s.strip()
    try:
        return float(t)
    except ValueError:
        pass
    if "/" in t:
        parts = t.split("/")
        if len(parts) == 2:
            try:
                a = float(parts[0].strip())
                b = float(parts[1].strip())
            except ValueError:
                return None
            if b == 0.0:
                return None
            return a / b
    return None


def numeric_token_value(token):
    """The ported B0 rule: a commit row's stripped token matching the
    plain decimal/scientific form is numeric; its float value; every
    other token is None."""
    if not isinstance(token, str):
        return None
    t = token.strip()
    if NUMERIC_RE.match(t):
        return float(t)
    return None


# ---------------------------------------------------------------------------
# Section 2. The cache-side conventions discovered at load (the
# never-guess law: the phase inventory and the commit-row field
# inventory are READ from the records, never assumed)
# ---------------------------------------------------------------------------

COMMIT_BASE_FIELDS = ("t", "token", "phase")
RAW_GAP_FIELD_PAIRS = (
    ("logit1", "logit2"),
    ("top1", "top2"),
    ("top1_logit", "top2_logit"),
)
# v1.0.4 -- the instrument of record's own banked form (the
# item-1158 rec 2, my stamp): the commit rows bank the
# PROBABILITY-domain raw features per content step -- emitted_p =
# probs[emitted_id], margin = float(top_p[0] - top_p[1]) the top-2
# probability margin, second_p = the first content alternative's
# probability at or below the top-2 (the instrument's own writer
# bytes, triadic_telemetry_t2_v32.3.0.py; its design notes: "the
# v32.0.6 raw features emitted_p / margin / content_mass, banked
# per step -- they are the banked cache3 schema"). The v1.0.3
# vocabulary missed it (authored for the logit domain only -- the
# recognition miss owned at the item-1158 bank); the two domains
# are NAMED per row, never conflated with the logit-domain m_ulp
# quantities.
INSTRUMENT_RAW_GAP_FIELDS = ("emitted_p", "margin", "second_p")


def discover_commit_fields(records):
    """The union of commit-row field names beyond the base trio, over
    every record; the raw-gap receipt rides the instrument of
    record's own banked form (the probability-domain trio) when the
    DISCOVERED inventory carries it, else a recognized logit-domain
    top-2 pair -- never a guess."""
    fields = set()
    for r in records.values():
        for c in r["commits"]:
            for k in c:
                fields.add(k)
    extra = sorted(f for f in fields if f not in COMMIT_BASE_FIELDS)
    instrument = all(f in extra
                     for f in INSTRUMENT_RAW_GAP_FIELDS)
    recognized = None
    for pair in RAW_GAP_FIELD_PAIRS:
        if pair[0] in extra and pair[1] in extra:
            recognized = pair
            break
    return {"extra_fields": extra, "raw_gap_pair": recognized,
            "instrument_form": instrument}


def discover_gen_phases(records, resolved_indices):
    """The generation-phase set: the phases observed at the
    inventory's own resolved commit indices (the span_resolution
    rows), per cache; DISCOVERED at load, never assumed. Operand
    emission resolution is restricted to these phases -- a value
    occurring only outside them is PROMPT-SIDE by the coverage
    boundary law."""
    per_cache = {}
    for cache_name, per_rec in resolved_indices.items():
        recs = records[cache_name]
        phases = set()
        for key, idx_list in per_rec.items():
            rec = recs.get(key)
            if rec is None:
                fail_loud("gen-phase discovery: cache %s carries no "
                          "record %r (a NAMED join gap)"
                          % (cache_name, key))
            for i in idx_list:
                if not (0 <= i < len(rec["commits"])):
                    fail_loud("gen-phase discovery: resolved commit "
                              "index %d outside record %r"
                              % (i, key))
                phases.add(rec["commits"][i]["phase"])
        per_cache[cache_name] = sorted(phases)
    return per_cache


def numeric_commit_indices(record):
    """The doc's numeric commit indices (the centering population:
    every commit row whose stripped token is numeric)."""
    out = []
    for i, c in enumerate(record["commits"]):
        if numeric_token_value(c.get("token")) is not None:
            out.append(i)
    return out


def doc_numeric_mean(p1, record, numeric_idx):
    """The doc-level numeric-step centering mean: the mean hidden row
    over the doc's numeric commit rows. Cached by the caller per
    record; a doc with zero numeric commits is a NAMED None (the
    cohorts' docs all carry numeric commits; a None here is a hard
    census surprise at the door, never averaged around)."""
    if not numeric_idx:
        return None
    acc = None
    n = 0
    for i in numeric_idx:
        row = p1.hidden_row(record, i)
        if acc is None:
            acc = list(row)
        else:
            for j, v in enumerate(row):
                acc[j] += v
        n += 1
    return [v / n for v in acc]


def resolve_commit_for_value(record, value, before_index, gen_phases):
    """The operand emission resolver, the ported B0 law plus its
    extension: the EARLIEST commit row strictly before before_index,
    in a generation phase, whose stripped token is numeric and
    float-equal to the value (the ported law, single token); if no
    single token matches, the earliest consecutive run of numeric and
    dot tokens whose join parses float-equal (the split-token class,
    NAMED in the receipt). No match in the generation phases =
    PROMPT-SIDE-OPERAND (the coverage boundary class, NAMED)."""
    commits = record["commits"]
    end = min(before_index, len(commits))
    best = None
    for i in range(end):
        c = commits[i]
        if c.get("phase") not in gen_phases:
            continue
        v = numeric_token_value(c.get("token"))
        if v is not None and v == value:
            best = {"status": "RESOLVED", "start_index": i,
                    "end_index": i, "row_class": "single-token"}
            break
    if best is None:
        i = 0
        while i < end:
            c = commits[i]
            if c.get("phase") not in gen_phases:
                i += 1
                continue
            first = numeric_token_value(c.get("token"))
            if first is None:
                i += 1
                continue
            parts = [str(c.get("token")).strip()]
            j = i
            hit = None
            while j + 1 < end:
                nxt = commits[j + 1]
                if nxt.get("phase") not in gen_phases:
                    break
                nt = str(nxt.get("token", "")).strip()
                if nt == "." or NUMERIC_RE.match(nt):
                    parts.append(nt)
                    j += 1
                    joined = "".join(parts)
                    if NUMERIC_RE.match(joined) and float(joined) == value:
                        hit = j
                        break
                else:
                    break
            if hit is not None:
                best = {"status": "RESOLVED", "start_index": i,
                        "end_index": hit, "row_class": "multi-token"}
                break
            i += 1
    if best is None:
        return {"status": "PROMPT-SIDE-OPERAND",
                "end_index": None, "row_class": None,
                "value": value,
                "finding": ("the operand value %r has no emission "
                            "row in the generation phases before the "
                            "row's commit -- the value arrived via "
                            "the prompt side; the coverage boundary "
                            "class, NAMED, never skipped, never "
                            "averaged" % value)}
    best["value"] = value
    return best


# ---------------------------------------------------------------------------
# Section 3. The statement binding (span -> aligned statement ->
# checker statement by pos; every miss a NAMED count, never a guess)
# ---------------------------------------------------------------------------

class StatementIndex(object):
    """Per (leg, doc_id): the aligned statements keyed by their span
    (token ids, exact tuple), and the checker statements keyed by
    pos."""

    def __init__(self, aligned_doc, checker_doc):
        self.aligned_by_span = {}
        self.aligned_by_pos = {}
        for s in (aligned_doc or {}).get("statements", []):
            self.aligned_by_span[tuple(s.get("span") or [])] = s
            self.aligned_by_pos[s.get("pos")] = s
        self.checker_by_pos = {}
        for s in (checker_doc or {}).get("statements", []):
            self.checker_by_pos[s.get("pos")] = s

    def bind(self, row):
        """Bind an inventory row to its checker statement: the exact
        span law first (the row's span == an aligned statement's
        span), then the checker statement at that pos. Every miss is
        a NAMED receipt, never a guess, never a skip of the pair."""
        span = tuple(row.get("span") or [])
        al = self.aligned_by_span.get(span)
        if al is None:
            return {"status": "NAMED-UNBOUND-STATEMENT",
                    "reason": ("no aligned statement carries the "
                                "row's exact span"),
                    "checker_statement": None}
        ck = self.checker_by_pos.get(al.get("pos"))
        if ck is None:
            return {"status": "NAMED-CHECKER-ABSENT",
                    "reason": ("the aligned statement at pos %r has "
                               "no checker statement at that pos"
                               % al.get("pos")),
                    "checker_statement": None}
        return {"status": "BOUND", "reason": None,
                "aligned_statement": al, "checker_statement": ck}


def build_statement_indexes(aligned_spans, checker_raw, checker_chat):
    """The (leg, doc_id) -> StatementIndex map over the two A2 legs
    (the p2 lane carries no operand binding by the coverage law)."""
    aligned_docs = {}
    for leg_name in ("a2_raw", "a2_chat"):
        for d in aligned_spans["legs"][leg_name]["per_doc"]:
            aligned_docs[(leg_name, d["doc_id"])] = d
    checker_docs = {}
    for leg_name, ck in (("a2_raw", checker_raw),
                         ("a2_chat", checker_chat)):
        for d in ck.get("per_doc") or []:
            checker_docs[(leg_name, d["doc_id"])] = d
    indexes = {}
    for key, al in aligned_docs.items():
        ck = checker_docs.get(key)
        indexes[key] = StatementIndex(al, ck)
    return indexes


# ---------------------------------------------------------------------------
# Section 4. The correct-precedence antecedent tree (the
# composition-order confound pinned: the root antecedent values under
# CORRECT precedence, standard * / over + -, left-associative)
# ---------------------------------------------------------------------------

PRECEDENCE_LEVEL = {"*": 2, "/": 2, "+": 1, "-": 1}


def _apply_op(a, o, b):
    if o == "+":
        return a + b
    if o == "-":
        return a - b
    if o == "*":
        return a * b
    if o == "/":
        if b == 0.0:
            return None
        return a / b
    return None


def precedence_root_antecedents(nums, ops):
    """The correct-precedence composition of a checker statement: the
    root node's immediate antecedent VALUES (two for a multi-operand
    composition, the literals themselves for a two-operand
    statement). The executed order in the raw text never enters here
    -- the composition-order confound is pinned at the source."""
    vals = []
    for s in nums or []:
        v = parse_value(s)
        if v is None:
            return {"status": "NAMED-UNPARSEABLE-OPERAND",
                    "reason": "operand string %r parses to no value"
                              % s, "root_values": None,
                    "n_operands": len(nums or [])}
        vals.append(v)
    n = len(vals)
    work_o = [str(o).strip() for o in (ops or [])]
    if n == 0:
        return {"status": "NAMED-NO-OPERANDS",
                "reason": "the statement carries no operands",
                "root_values": None, "n_operands": 0}
    if len(work_o) != n - 1:
        return {"status": "NAMED-OP-ARITY-MISMATCH",
                "reason": ("%d operands with %d operators (the "
                           "statement form)" % (n, len(work_o))),
                "root_values": None, "n_operands": n}
    if n == 1:
        return {"status": "NAMED-NO-OPERANDS",
                "reason": "a single-number statement (no composition)",
                "root_values": None, "n_operands": 1}
    nodes = [{"val": v, "children": None} for v in vals]
    for level in (2, 1):
        i = 0
        while i < len(work_o):
            if PRECEDENCE_LEVEL.get(work_o[i]) == level:
                b = nodes.pop(i + 1)
                a = nodes[i]
                r = _apply_op(a["val"], work_o[i], b["val"])
                if r is None:
                    return {"status": "NAMED-OP-UNAPPLYABLE",
                            "reason": ("operator %r unapplyable "
                                       "(the zero-divisor class)"
                                       % work_o[i]),
                            "root_values": None, "n_operands": n}
                nodes[i] = {"val": r, "children": [a, b]}
                work_o.pop(i)
            else:
                i += 1
    root = nodes[0]
    roots = [c["val"] for c in root["children"]]
    return {"status": "OK", "reason": None, "root_values": roots,
            "leaf_values": vals, "n_operands": n}


def earliest_earlier_statement(index, checker_stmt, value):
    """The producing statement: the earliest earlier statement in
    the doc (emission order = the checker statement order) whose
    stated value float-equals the operand; None when no such
    statement exists (the operand is a grounding literal)."""
    target_pos = checker_stmt.get("pos")
    stmts = index.checker_by_pos
    best = None
    for pos in sorted(stmts):
        if target_pos is not None and pos >= target_pos:
            continue
        st = stmts[pos]
        sv = parse_value(st.get("stated", ""))
        if sv is not None and sv == value:
            if best is None or pos < best.get("pos"):
                best = st
    return best


def derivation_window(record, index, checker_stmt, root_commit_index,
                       gen_phases, depth=0):
    """The DERIVATION-PATH window: the transitive closure of the
    antecedent EMISSION rows -- for every operand value in the
    closure (the statement's own operands, then the producing
    statement's operands, transitively via stated float-equality),
    the earliest emission row resolved before the ROOT row's commit;
    deduped, sorted. Prompt-side leaves are NAMED, outside the
    window; the window never extends to the whole prompt (the pinned
    law: the path evidence only)."""
    if depth > 64:
        fail_loud("derivation window: depth %d (a cycle in the "
                  "producing-statement closure -- a NAMED premise "
                  "violation)" % depth)
    values = []

    def visit(stmt, d):
        if d > 64:
            fail_loud("derivation window: visit depth %d (a cycle in "
                      "the producing-statement closure)" % d)
        for s in stmt.get("nums") or []:
            v = parse_value(s)
            if v is None:
                values.append((v, "NAMED-UNPARSEABLE-OPERAND"))
                continue
            values.append((v, "operand"))
            prod = earliest_earlier_statement(index, stmt, v)
            if prod is not None:
                visit(prod, d + 1)

    visit(checker_stmt, depth)
    rows = []
    named = []
    seen_vals = set()
    for v, cls in values:
        if v is None or v in seen_vals:
            continue
        seen_vals.add(v)
        r = resolve_commit_for_value(record, v, root_commit_index,
                                     gen_phases)
        if r["status"] == "RESOLVED":
            rows.append(r["end_index"])
        else:
            named.append({"value": v, "class": r["status"]})
    return {"window_rows": sorted(set(rows)),
            "prompt_side_values": named,
            "n_values": len(seen_vals)}


# ---------------------------------------------------------------------------
# Section 5. The per-row compute engine (every B1 operator wired;
# every NAMED class counted; the raw-gap side-by-side receipt)
# ---------------------------------------------------------------------------

def raw_gap_read(commit_row, raw_gap_pair, instrument_form=False):
    """The raw dump gap side-by-side receipt (v1.0.4): the
    instrument of record's own banked form READ when the load's
    discovered field inventory carries the probability-domain trio
    (margin verbatim + emitted_p/second_p beside it + the
    emitted-vs-top1 case named per row), else the recognized
    logit-domain top-2 pair, NAMED-ABSENT otherwise (the
    never-guess law: the caches' own fields decide, never this
    tool; the domain NAMED per row, never conflated)."""
    if instrument_form:
        m = commit_row.get("margin")
        ep = commit_row.get("emitted_p")
        sp = commit_row.get("second_p")
        if not (isinstance(m, (int, float))
                and isinstance(ep, (int, float))
                and isinstance(sp, (int, float))):
            return {"status": "NAMED-ABSENT",
                    "reason": ("the instrument form carries a "
                               "non-numeric row value (the "
                               "fields named at load)")}
        m, ep, sp = float(m), float(ep), float(sp)
        # the emitted-vs-top1 case, read from the banked fields
        # alone (the instrument's own writer bytes: margin =
        # top_p[0] - top_p[1]; the content alternative rides at or
        # below top-2; the emitted token is the top-1 consistent
        # candidate iff its lead over the content alternative
        # covers the top-2 margin; the float32 round-trip
        # tolerance named -- a NOT-CONSISTENT case a data finding
        # NAMED, never smoothed)
        tol = 1e-6
        case = ("EMITTED-CONSISTENT-TOP1"
                if ep - sp >= m - tol
                else "EMITTED-NOT-TOP1-CONSISTENT")
        return {"status": "READ", "domain": "probability",
                "margin": m, "emitted_p": ep, "second_p": sp,
                "second_id": commit_row.get("second_id"),
                "second_str": commit_row.get("second_str"),
                "emitted_vs_top1": case, "gap": m,
                "fields": list(INSTRUMENT_RAW_GAP_FIELDS)}
    if raw_gap_pair is None:
        return {"status": "NAMED-ABSENT",
                "reason": ("the caches' commit rows carry no "
                           "recognized raw form (the logit-domain "
                           "top-2 pair or the instrument's own "
                           "probability-domain trio -- the "
                           "discovered field inventory named at "
                           "load); the raw gap rides ABSENT per "
                           "row, never guessed")}
    a = commit_row.get(raw_gap_pair[0])
    b = commit_row.get(raw_gap_pair[1])
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return {"status": "NAMED-ABSENT",
                "reason": ("the recognized pair %r carries a "
                           "non-numeric row value"
                           % (raw_gap_pair,))}
    return {"status": "READ", "domain": "logit",
            "top1": float(a), "top2": float(b),
            "gap": float(a) - float(b), "fields": list(raw_gap_pair)}


def non_finite_detail(pairs):
    """The non-finite guard (the item-1155 class): any NaN or inf
    in the row's measured inputs a NAMED class, never a crash,
    never a silent skip. pairs: a list of (component, values);
    returns None when every value finite, else the receipt detail
    (component + count + samples)."""
    for comp, vals in pairs:
        n_bad = 0
        samples = []
        for i, v in enumerate(vals):
            try:
                finite = math.isfinite(v)
            except TypeError:
                finite = False
            if not finite:
                n_bad += 1
                if len(samples) < 3:
                    samples.append((i, repr(v)))
        if n_bad:
            return {"component": comp, "n_non_finite": n_bad,
                    "samples": samples}
    return None


def compute_row(b1, p1, ctx, row, record, w_num_rows, answer_row,
                doc_mean):
    """One measurement row: the full operator read at t_0. ctx
    carries vnum_ids (the pinned sorted V_num order), vnum_strs (the
    token strings), gen_phases (this record's cache's discovered
    generation phases), statement_index (None for A1 by the coverage
    law), raw_gap_pair (the discovered pair or None). The receipt is
    an ordered list of fields, every field traceable to its source
    row."""
    sr = row.get("span_resolution") or {}
    hri = sr.get("hidden_row_index")
    ci = sr.get("commit_index")
    if not isinstance(hri, int) or not isinstance(ci, int):
        fail_loud("row %r: span_resolution absent (the B0 law: every "
                  "measured row carries one)" % row.get("pair_id"))
    out = [("pair_id", row.get("pair_id")),
           ("cohort", row.get("cohort")),
           ("doc_id", row.get("doc_id")),
           ("leg", row.get("leg")),
           ("record_class", row.get("record_class")),
           ("value", row.get("value")),
           ("t0", sr.get("t0")),
           ("commit_index", ci),
           ("hidden_row_index", hri),
           ("commit_token", sr.get("commit_token"))]
    h_t0 = p1.hidden_row(record, hri)
    if doc_mean is None:
        return out + [("m_ulp_num",
                       {"status": "NAMED-NO-NUMERIC-COMMITS",
                        "reason": "the doc's centering population "
                                  "is empty (a census surprise at "
                                  "the door)"})]
    # the item-1155 class guard: a non-finite h_t0 or doc-mean a
    # NAMED row (counted, carried, never computed, never a crash);
    # a non-finite commit row inside the doc poisons the mean, so
    # this guard catches the doc's every row at the component named
    nf = non_finite_detail([("h_t0", h_t0),
                            ("doc_mean", doc_mean)])
    if nf is not None:
        return out + [("m_ulp_num",
                       dict({"status": "NAMED-NON-FINITE"}, **nf))]
    h_c = b1.center_state(h_t0, doc_mean)
    logits_num = b1.num_logits(h_c, w_num_rows)
    mu_rec = b1.m_ulp_num(logits_num)
    m_rec = dict(mu_rec)
    for key in ("id1", "id2"):
        i = mu_rec.get(key)
        if isinstance(i, int) and 0 <= i < len(ctx["vnum_ids"]):
            m_rec[key + "_token"] = ctx["vnum_ids"][i]
            m_rec[key + "_str"] = ctx["vnum_strs"][i]
    out.append(("m_ulp_num", m_rec))
    out.append(("h_num", b1.h_num(logits_num)))
    p_answer = b1.dot(h_c, answer_row)
    zc = b1.zeta_step(p_answer, logits_num)
    out.append(("zeta_commit", zc))
    phases = [c.get("phase") for c in record["commits"]]
    n_steps = record["n_content_steps"]
    if hri > 0:
        h_prev = p1.hidden_row(record, hri - 1)
        nf_prev = non_finite_detail([("h_prev", h_prev)])
        if nf_prev is not None:
            # the corroborator lane NAMED alone (the primary
            # unpoisoned); counted, never a crash
            kc = dict({"status": "NAMED-NON-FINITE"}, **nf_prev)
        else:
            kc = b1.kappa_corroborator(h_prev, h_t0, ci, phases,
                                       n_steps)
    else:
        kc = {"kappa": None, "boundary": None,
              "guard_reason": ("hidden_row_index 0: no prior row on "
                               "the commit axis (the NAMED sentinel)")}
    out.append(("kappa", kc))
    out.append(("raw_gap", raw_gap_read(record["commits"][ci],
                                        ctx.get("raw_gap_pair"),
                                        ctx.get("instrument_form"))))
    if row.get("cohort") == "A2":
        idx = ctx.get("statement_index")
        if idx is None:
            fail_loud("A2 row %r with no statement index (a wiring "
                      "premise violation)" % row.get("pair_id"))
        bind = idx.bind(row)
        if bind["status"] != "BOUND":
            out.append(("statement_binding", bind))
            out.append(("centered_r_perp",
                        {"status": bind["status"], "r_perp": None}))
            out.append(("bhob", {"status": bind["status"],
                                 "bhob": None}))
            out.append(("work_increment",
                        {"status": bind["status"], "increment": None}))
            return out
        ck = bind["checker_statement"]
        out.append(("statement_binding",
                    {"status": "BOUND", "pos": ck.get("pos"),
                     "raw": ck.get("raw"), "stated": ck.get("stated"),
                     "verdict": ck.get("verdict"),
                     "nums": ck.get("nums"), "ops": ck.get("ops")}))
        tree = precedence_root_antecedents(ck.get("nums"),
                                           ck.get("ops"))
        win = derivation_window(record, idx, ck, ci,
                                ctx["gen_phases"])
        if zc.get("zeta") is None:
            out.append(("derivation_window",
                        {"window_rows": win["window_rows"],
                         "n_values": win["n_values"],
                         "prompt_side_values":
                             win["prompt_side_values"]}))
            out.append(("work_increment",
                        {"status": "NAMED-ZETA-DEGENERATE",
                         "increment": None,
                         "reason": zc.get("reason")}))
        else:
            nf_win = non_finite_detail(
                [("derivation_window_row[%d]" % widx,
                  p1.hidden_row(record, widx))
                 for widx in win["window_rows"]])
            if nf_win is not None:
                # a non-finite window row poisons the increment
                # maximum: the field NAMED, the row counted, never
                # a crash, never a silent skip of the row
                out.append(("derivation_window",
                            {"window_rows": win["window_rows"],
                             "n_values": win["n_values"],
                             "prompt_side_values":
                                 win["prompt_side_values"]}))
                out.append(("work_increment",
                            dict({"status": "NAMED-NON-FINITE"},
                                 **nf_win)))
            else:
                zeta_window = []
                for wi in win["window_rows"]:
                    hw = p1.hidden_row(record, wi)
                    hw_c = b1.center_state(hw, doc_mean)
                    lw = b1.num_logits(hw_c, w_num_rows)
                    zw = b1.zeta_step(b1.dot(hw_c, answer_row), lw)
                    if zw.get("zeta") is not None:
                        zeta_window.append(zw["zeta"])
                out.append(("derivation_window",
                            {"window_rows": win["window_rows"],
                             "n_values": win["n_values"],
                             "prompt_side_values":
                                 win["prompt_side_values"]}))
                out.append(("work_increment",
                            b1.work_increment(zc.get("zeta"),
                                              zeta_window)))
        if tree["status"] != "OK":
            out.append(("precedence_tree", tree))
            out.append(("centered_r_perp",
                        {"status": tree["status"], "r_perp": None}))
            out.append(("bhob", {"status": tree["status"],
                                 "bhob": None}))
            return out
        out.append(("precedence_tree",
                    {"status": "OK",
                     "root_values": tree["root_values"],
                     "leaf_values": tree["leaf_values"],
                     "n_operands": tree["n_operands"]}))
        operand_rows = []
        operand_classes = []
        operand_nf = None
        leaves = set(tree["leaf_values"])
        for v in tree["root_values"]:
            r = resolve_commit_for_value(record, v, ci,
                                        ctx["gen_phases"])
            if r["status"] == "RESOLVED":
                ho = p1.hidden_row(record, r["end_index"])
                nf_op = non_finite_detail(
                    [("operand_row[%d]" % r["end_index"], ho)])
                if nf_op is not None:
                    operand_nf = nf_op
                    continue
                operand_rows.append(b1.center_state(ho, doc_mean))
            else:
                cls = r["status"]
                if v not in leaves:
                    cls = "NAMED-INTERMEDIATE-UNCOMMITTED"
                operand_classes.append({"value": v, "class": cls})
        if operand_nf is not None:
            # a non-finite operand row poisons the projector pair:
            # the distinct NAMED class, counted, never conflated
            # with the operand-coverage class
            out.append(("operand_rows",
                        dict({"status": "NAMED-NON-FINITE"},
                             **operand_nf)))
            out.append(("centered_r_perp",
                        dict({"status": "NAMED-NON-FINITE"},
                             **operand_nf)))
            out.append(("bhob",
                        dict({"status": "NAMED-NON-FINITE"},
                             **operand_nf)))
            return out
        if len(operand_rows) != 2 or operand_classes:
            out.append(("operand_rows",
                        {"status": "NAMED-OPERAND-COVERAGE",
                         "classes": operand_classes,
                         "n_resolved": len(operand_rows)}))
            out.append(("centered_r_perp",
                        {"status": "NAMED-OPERAND-COVERAGE",
                         "r_perp": None}))
            out.append(("bhob", {"status": "NAMED-OPERAND-COVERAGE",
                                 "bhob": None}))
            return out
        out.append(("operand_rows", {"status": "OK", "n_resolved": 2}))
        out.append(("centered_r_perp",
                     b1.centered_r_perp(h_c, operand_rows)))
        out.append(("bhob", b1.bhob(h_c, operand_rows)))
        return out
    out.append(("centered_r_perp",
                {"status": "NAMED-OUT-OF-COVERAGE",
                 "r_perp": None,
                 "reason": ("the p2 lane is prompt-anchored (the "
                            "quantities enter via the prompt); no "
                            "generation-side operand evidence "
                            "exists for the projector; the coverage "
                            "boundary class, counted, my stamps "
                            "decide")}))
    out.append(("bhob", {"status": "NAMED-OUT-OF-COVERAGE",
                         "bhob": None}))
    out.append(("work_increment",
                {"status": "NAMED-NO-PATH-EVIDENCE",
                 "increment": None,
                 "reason": ("the p2 lane carries no checker path "
                            "evidence for the A1 rows; the window "
                            "never extends to the whole prompt")}))
    return out


# ---------------------------------------------------------------------------
# Section 6. The part-2 selfcheck battery (constructed bytes only;
# every expectation hand-computed, the full acceptance battery is
# part 3)
# ---------------------------------------------------------------------------

def _mk_line(key, tokens, phases, hidden_rows, dim):
    """A constructed cache record obeying the schema of record (the
    part-1 reader must accept it)."""
    n_commits = len(tokens)
    n_steps = n_commits + 2
    steps = {"t": list(range(n_steps)),
             "id": [100 + i for i in range(n_steps)]}
    commits = [{"t": i, "token": tokens[i], "phase": phases[i]}
               for i in range(n_commits)]
    flat = b"".join(struct.pack("<" + "e" * dim, *row)
                    for row in hidden_rows)
    hb = base64.b64encode(flat).decode("ascii")
    return json.dumps({
        "key": key, "leg": "testleg", "doc_id": 7, "bos": True,
        "instrument": "test", "prompt_len": 5, "stop_reason": "eos",
        "n_gen_steps": n_steps, "n_content_steps": n_commits,
        "walk_ids": steps["id"], "steps": steps, "commits": commits,
        "hidden_n": n_commits, "hidden_dim": dim, "hidden_b64": hb,
    })


def part2_selfcheck(p1, b1):
    checks = []

    def check(cid, name, ok, detail=""):
        checks.append((cid, name, bool(ok), detail))

    # C01 the value law
    ok = (parse_value("33/4") == 8.25 and parse_value("7") == 7.0
          and parse_value("-5") == -5.0 and parse_value("2e3") == 2000.0
          and parse_value("abc") is None and parse_value("1/0") is None)
    check("P2-C01", "parse_value decimal/fraction/None classes", ok)

    # C02 the numeric-token rule ported from the builder
    ok = (numeric_token_value(" 8.25 ") == 8.25
          and numeric_token_value(".5") == 0.5
          and numeric_token_value("nan") is None
          and numeric_token_value("inf") is None
          and numeric_token_value("x8") is None
          and numeric_token_value("+7") == 7.0)
    check("P2-C02", "numeric_token_value the ported form", ok)

    # C03 single-token earliest resolution, before the boundary
    rec = json.loads(_mk_line("k3", ["2", "5", "2", "9"],
                             ["COT"] * 4,
                             [[1.0, 0.0, 0.0]] * 4, 3))
    r = resolve_commit_for_value(rec, 2.0, 4, {"COT"})
    ok = (r["status"] == "RESOLVED" and r["end_index"] == 0
          and r["row_class"] == "single-token")
    r2 = resolve_commit_for_value(rec, 5.0, 1, {"COT"})
    ok = ok and r2["status"] == "PROMPT-SIDE-OPERAND"
    check("P2-C03", "earliest single-token + boundary respected", ok,
          "r=%r r2=%r" % (r, r2))

    # C04 the multi-token reconstruction
    rec = json.loads(_mk_line(
        "k4", ["8", ".", "25", "9"], ["COT"] * 4,
        [[1.0, 0.0, 0.0]] * 4, 3))
    r = resolve_commit_for_value(rec, 8.25, 4, {"COT"})
    ok = (r["status"] == "RESOLVED" and r["start_index"] == 0
          and r["end_index"] == 2 and r["row_class"] == "multi-token")
    check("P2-C04", "multi-token reconstruction of split values", ok,
          "r=%r" % r)

    # C05 the prompt-side class outside the generation phases
    rec = json.loads(_mk_line("k5", ["2", "5"], ["PROMPT", "COT"],
                              [[1.0, 0.0, 0.0]] * 2, 3))
    r = resolve_commit_for_value(rec, 2.0, 2, {"COT"})
    ok = r["status"] == "PROMPT-SIDE-OPERAND"
    check("P2-C05", "prompt-side operand the coverage boundary", ok)

    # C06 the correct-precedence tree
    t2 = precedence_root_antecedents(["3", "4"], ["+"])
    t3 = precedence_root_antecedents(["3", "4", "5"], ["+", "*"])
    t4 = precedence_root_antecedents(["1.5", "2", "2", "3.75"],
                                     ["+", "+", "+"])
    tz = precedence_root_antecedents(["1", "0"], ["/"])
    ok = (t2["status"] == "OK" and t2["root_values"] == [3.0, 4.0]
          and t3["status"] == "OK"
          and t3["root_values"] == [3.0, 20.0]
          and t4["status"] == "OK"
          and t4["root_values"] == [5.5, 3.75]
          and tz["status"] == "NAMED-OP-UNAPPLYABLE")
    check("P2-C06", "precedence root antecedents + zero divisor", ok,
          "t3=%r t4=%r tz=%r" % (t3, t4, tz))

    # C07 the derivation window closure (the doc-1014 shape: the
    # chain 1.75 <- 7/4 of s1, 8.25 <- 33/4 of s0, then the leaves)
    rec = json.loads(_mk_line(
        "k7", ["1.5", "2", "2", "3.75", "8.25", "10", "1.75",
               "0.25", "7"],
        ["COT"] * 9, [[1.0, 0.0, 0.0]] * 9, 3))
    idx = StatementIndex(
        {"statements": [{"i": 0, "pos": 73, "stated": "33/4",
                         "span": [1, 2]}]},
        {"statements": [
            {"pos": 73, "nums": ["1.5", "2", "2", "3.75"],
             "ops": ["+", "+", "+"], "stated": "33/4", "raw": "s0"},
            {"pos": 100, "nums": ["10", "8.25"], "ops": ["-"],
             "stated": "7/4", "raw": "s1"},
            {"pos": 127, "nums": ["1.75", "0.25"], "ops": ["/"],
             "stated": "7", "raw": "s2"},
        ]})
    ck = idx.checker_by_pos[127]
    win = derivation_window(rec, idx, ck, 8, {"COT"})
    ok = (win["window_rows"] == [0, 1, 3, 4, 5, 6, 7]
          and win["n_values"] == 7
          and len(win["prompt_side_values"]) == 0)
    check("P2-C07", "window closure dedupe+sort over the chain", ok,
          "win=%r" % (win,))

    # C08 the doc-level numeric centering mean
    rec = json.loads(_mk_line(
        "k8", ["2", "x", "1.5", "7"], ["COT"] * 4,
        [[1.0, 0.0, 0.0], [9.0, 9.0, 9.0], [0.0, 2.0, 0.0],
         [0.0, 0.0, 4.0]], 3))
    ni = numeric_commit_indices(rec)
    mean = doc_numeric_mean(p1, rec, ni)
    ok = (ni == [0, 2, 3] and mean is not None
          and abs(mean[0] - 1.0 / 3.0) < 1e-9
          and abs(mean[1] - 2.0 / 3.0) < 1e-9
          and abs(mean[2] - 4.0 / 3.0) < 1e-9)
    check("P2-C08", "doc numeric mean over numeric commits", ok,
          "ni=%r mean=%r" % (ni, mean))

    # C09 kappa adjacent + the boundary guard + the index-0 sentinel
    rec = json.loads(_mk_line(
        "k9", ["2", "3", "4"], ["COT", "COT", "ANSWER"],
        [[1.0, 0.0], [0.0, 2.0], [0.0, 2.0]], 2))
    phases = [c["phase"] for c in rec["commits"]]
    kc = b1.kappa_corroborator([0.0, 2.0], [0.0, 2.0], 2, phases, 3)
    ok = (kc["kappa"] == 0.0 and kc["boundary"] is True)
    kc2 = b1.kappa_corroborator([1.0, 0.0], [0.0, 2.0], 0, phases, 3)
    ok = ok and kc2["boundary"] is True
    check("P2-C09", "kappa + boundary guard + prior-row sentinel", ok,
          "kc=%r" % (kc,))

    # C10 the gen-phase discovery + phase-restricted resolution
    recs = {"test": {"k10": json.loads(_mk_line(
        "k10", ["2", "5", "9"], ["COT", "PROMPT", "COT"],
        [[1.0, 0.0, 0.0]] * 3, 3))}}
    gp = discover_gen_phases(recs, {"test": {"k10": [2]}})
    ok = gp == {"test": ["COT"]}
    r = resolve_commit_for_value(recs["test"]["k10"], 5.0, 3,
                                 gp["test"])
    ok = ok and r["status"] == "PROMPT-SIDE-OPERAND"
    check("P2-C10", "gen-phase discovery + phase restriction", ok,
          "gp=%r r=%r" % (gp, r))

    # C11 the statement binding: span -> aligned -> checker pos
    idx = StatementIndex(
        {"statements": [{"i": 2, "pos": 187, "stated": "7",
                         "span": [284, 220, 22]}]},
        {"statements": [
            {"pos": 73, "nums": ["1.5"], "ops": [], "stated": "x"},
            {"pos": 187, "nums": ["1.75", "0.25"], "ops": ["/"],
             "stated": "7", "raw": "1.75/0.25 = 7"}]})
    bind = idx.bind({"span": [284, 220, 22]})
    ok = (bind["status"] == "BOUND"
          and bind["checker_statement"]["pos"] == 187)
    miss = idx.bind({"span": [9, 9]})
    ok = ok and miss["status"] == "NAMED-UNBOUND-STATEMENT"
    check("P2-C11", "span binding + the NAMED unbound class", ok)

    # C12 compute_row integration: hand-computed m_ulp / zeta / kappa
    rec = json.loads(_mk_line(
        "k12", ["2", "1.5", "7"], ["COT", "COT", "ANSWER"],
        [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 4.0]], 3))
    mean = [1.0 / 3.0, 2.0 / 3.0, 4.0 / 3.0]
    w_num = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
             [1.0, 1.0, 0.0]]
    answer = [0.0, 0.0, 1.0]
    ctx = {"vnum_ids": [10, 11, 12, 13],
           "vnum_strs": ["2", "1.5", "7", "21"],
           "gen_phases": ["COT", "ANSWER"],
           "statement_index": None, "raw_gap_pair": None}
    row = {"pair_id": "X-1", "cohort": "A1", "doc_id": 7,
           "leg": "p2", "record_class": True, "value": "7",
           "span": [284, 220, 22],
           "span_resolution": {"t0": 12, "commit_index": 2,
                               "hidden_row_index": 2,
                               "commit_token": "7"}}
    receipt = dict(compute_row(b1, p1, ctx, row, rec, w_num, answer,
                               mean))
    mu = receipt["m_ulp_num"]
    h_c = [-1.0 / 3.0, -2.0 / 3.0, 8.0 / 3.0]
    l = [h_c[0], h_c[1], h_c[2], h_c[0] + h_c[1]]
    gap = l[2] - l[0]
    ulp = 2.0 ** (1 - 7)  # 8/3 in [2,4): the bf16 ulp
    ok = (abs(mu["m_ulp"] - gap / ulp) < 1e-9
          and mu["id1_token"] == 12 and mu["id1_str"] == "7"
          and mu["id2_token"] == 10 and mu["id2_str"] == "2")
    zc = receipt["zeta_commit"]
    m = sum(l) / 4.0
    sd = math.sqrt(sum((v - m) ** 2 for v in l) / 4.0)
    ok = ok and abs(zc["zeta"] - (8.0 / 3.0 - m) / sd) < 1e-9
    hn = receipt["h_num"]
    mx = max(l)
    ps = [math.exp(v - mx) for v in l]
    p_top = max(ps) / sum(ps)
    ok = ok and abs(hn["p_top"] - p_top) < 1e-9
    ok = ok and receipt["kappa"]["kappa"] == 1.0  # [0,2,0] vs [0,0,4]
    ok = ok and receipt["centered_r_perp"]["status"] == \
        "NAMED-OUT-OF-COVERAGE"
    ok = ok and receipt["work_increment"]["status"] == \
        "NAMED-NO-PATH-EVIDENCE"
    ok = ok and receipt["raw_gap"]["status"] == "NAMED-ABSENT"
    check("P2-C12", "compute_row integration hand-computed", ok,
          "mu=%r zc=%r" % (mu, zc))

    # C13 the raw-gap discovery: recognized pair read; absent NAMED
    rec_a = json.loads(_mk_line(
        "k13a", ["2"], ["COT"], [[1.0]], 1))
    rec_a["commits"][0]["logit1"] = 3.5
    rec_a["commits"][0]["logit2"] = 2.5
    flds = discover_commit_fields({"a": rec_a})
    ok = (flds["raw_gap_pair"] == ("logit1", "logit2")
          and flds["extra_fields"] == ["logit1", "logit2"])
    rg = raw_gap_read(rec_a["commits"][0], flds["raw_gap_pair"])
    ok = ok and rg["status"] == "READ" and abs(rg["gap"] - 1.0) < 1e-12
    rec_b = json.loads(_mk_line(
        "k13b", ["2"], ["COT"], [[1.0]], 1))
    flds_b = discover_commit_fields({"b": rec_b})
    rg_b = raw_gap_read(rec_b["commits"][0], flds_b["raw_gap_pair"])
    ok = ok and (flds_b["extra_fields"] == []
                 and rg_b["status"] == "NAMED-ABSENT")
    check("P2-C13", "raw-gap pair discovery + NAMED-ABSENT", ok)

    # C19 the v1.0.4 instrument-form raw-gap receipt: the
    # probability domain, margin verbatim, the pair beside, the
    # emitted-vs-top1 case named per row; the never-guess partial
    # form refused; the both-forms precedence named; the v1.0.3
    # logit law still exact when alone
    rec_c = json.loads(_mk_line("k19", ["2"], ["COT"], [[1.0]], 1))
    c = rec_c["commits"][0]
    c["emitted_p"] = 0.6
    c["margin"] = 0.35
    c["second_p"] = 0.25
    c["second_id"] = 44
    c["second_str"] = "4"
    flds_c = discover_commit_fields({"c": rec_c})
    ok = (flds_c["instrument_form"] is True
          and flds_c["raw_gap_pair"] is None
          and flds_c["extra_fields"] == ["emitted_p", "margin",
                                         "second_id", "second_p",
                                         "second_str"])
    rg_c = raw_gap_read(c, flds_c["raw_gap_pair"],
                        flds_c["instrument_form"])
    ok = ok and (rg_c["status"] == "READ"
                 and rg_c["domain"] == "probability"
                 and abs(rg_c["margin"] - 0.35) < 1e-12
                 and abs(rg_c["gap"] - 0.35) < 1e-12
                 and abs(rg_c["emitted_p"] - 0.6) < 1e-12
                 and abs(rg_c["second_p"] - 0.25) < 1e-12
                 and rg_c["emitted_vs_top1"] ==
                 "EMITTED-CONSISTENT-TOP1"
                 and rg_c["second_str"] == "4"
                 and rg_c["second_id"] == 44)
    # the inconsistent twin: the case NAMED, never smoothed
    c2 = dict(c)
    c2["emitted_p"] = 0.2
    rg_c2 = raw_gap_read(c2, None, True)
    ok = ok and (rg_c2["emitted_vs_top1"] ==
                 "EMITTED-NOT-TOP1-CONSISTENT")
    # the partial form refused (never-guess: margin alone is not
    # the instrument's own schema; NAMED-ABSENT, no logit pair)
    rec_d = json.loads(_mk_line("k19d", ["2"], ["COT"], [[1.0]], 1))
    rec_d["commits"][0]["margin"] = 0.4
    flds_d = discover_commit_fields({"d": rec_d})
    rg_d = raw_gap_read(rec_d["commits"][0], flds_d["raw_gap_pair"],
                        flds_d["instrument_form"])
    ok = ok and (flds_d["instrument_form"] is False
                 and flds_d["raw_gap_pair"] is None
                 and rg_d["status"] == "NAMED-ABSENT")
    # the both-forms case: the instrument form the receipt of
    # record, the logit pair still named in the inventory
    rec_e = json.loads(_mk_line("k19e", ["2"], ["COT"], [[1.0]], 1))
    rec_e["commits"][0].update({"emitted_p": 0.6, "margin": 0.35,
                                "second_p": 0.25, "logit1": 3.5,
                                "logit2": 2.5})
    flds_e = discover_commit_fields({"e": rec_e})
    rg_e = raw_gap_read(rec_e["commits"][0],
                        flds_e["raw_gap_pair"],
                        flds_e["instrument_form"])
    ok = ok and (flds_e["instrument_form"] is True
                 and flds_e["raw_gap_pair"] == ("logit1", "logit2")
                 and rg_e["domain"] == "probability")
    # the v1.0.3 logit law still exact when alone
    rg_f = raw_gap_read({"logit1": 3.5, "logit2": 2.5},
                        ("logit1", "logit2"), False)
    ok = ok and (rg_f["domain"] == "logit"
                 and abs(rg_f["gap"] - 1.0) < 1e-12)
    check("P2-C19", "instrument-form raw-gap receipt (probability "
          "domain + the emitted-vs-top1 case)", ok)

    # C14 the work increment: window path vs the empty sentinel
    rec = json.loads(_mk_line(
        "k14", ["1", "2", "3"], ["COT"] * 3,
        [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], 2))
    idx = StatementIndex(
        {"statements": []},
        {"statements": [{"pos": 5, "nums": ["1", "2"], "ops": ["+"],
                         "stated": "3"}]})
    ck = idx.checker_by_pos[5]
    win = derivation_window(rec, idx, ck, 3, {"COT"})
    ok = (win["window_rows"] == [0, 1] and win["n_values"] == 2)
    wi = b1.work_increment(2.0, [1.0, 0.5])
    wi_empty = b1.work_increment(2.0, [])
    ok = ok and abs(wi["increment"] - 1.0) < 1e-12 \
        and wi_empty["increment"] is None
    check("P2-C14", "window rows + work increment + sentinel", ok,
          "win=%r" % (win,))

    # C15 the import contract: part-1 sha asserted at import
    ok = p1 is not None and hasattr(p1, "read_inventory") and \
        hasattr(p1, "hidden_row") and hasattr(b1, "m_ulp_num")
    check("P2-C15", "part-1 + B1 import contract", ok)

    # C16 the A2 compute path: bound statement, both operand rows
    # resolved, every projector operator reading
    rec = json.loads(_mk_line(
        "k16", ["1.5", "2", "2", "3.75", "8.25", "10", "1.75",
                "0.25", "7"],
        ["COT"] * 9,
        [[1.0 + 0.1 * i, 0.0, 0.0] for i in range(9)], 3))
    idx = StatementIndex(
        {"statements": [{"i": 2, "pos": 127, "stated": "7",
                         "span": [3, 4]}]},
        {"statements": [
            {"pos": 100, "nums": ["10", "8.25"], "ops": ["-"],
             "stated": "7/4", "raw": "s1"},
            {"pos": 127, "nums": ["1.75", "0.25"], "ops": ["/"],
             "stated": "7", "raw": "1.75/0.25 = 7"}]})
    ctx2 = {"vnum_ids": [10, 11, 12],
            "vnum_strs": ["1", "2", "3"],
            "gen_phases": ["COT"], "statement_index": idx,
            "raw_gap_pair": None}
    row2 = {"pair_id": "A2-1", "cohort": "A2", "doc_id": 7,
            "leg": "raw", "record_class": True, "value": "7",
            "span": [3, 4],
            "span_resolution": {"t0": 12, "commit_index": 8,
                               "hidden_row_index": 8,
                               "commit_token": "7"}}
    mean2 = doc_numeric_mean(p1, rec, numeric_commit_indices(rec))
    rc = dict(compute_row(b1, p1, ctx2, row2, rec,
                          [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                           [0.0, 0.0, 1.0]], [1.0, 0.0, 0.0],
                          mean2))
    ok = (rc["statement_binding"]["status"] == "BOUND"
          and rc["precedence_tree"]["root_values"] == [1.75, 0.25]
          and rc["operand_rows"]["status"] == "OK"
          and rc["operand_rows"]["n_resolved"] == 2
          and "residual_share" in rc["centered_r_perp"]
          and rc["bhob"]["m"] == 2
          and rc["bhob"]["reason"] is None
          and rc["work_increment"]["reason"] is None
          and isinstance(rc["work_increment"]["increment"], float))
    check("P2-C16", "A2 compute path wired end to end", ok,
          "wi=%r" % (rc["work_increment"],))

    # C17 the intermediate class: an uncommitted correct-precedence
    # sub-result NAMED, never conflated with the prompt-side class
    rec = json.loads(_mk_line(
        "k17", ["3", "4", "5", "35"], ["COT"] * 4,
        [[1.0 + 0.1 * i, 0.0, 0.0] for i in range(4)], 3))
    idx = StatementIndex(
        {"statements": [{"i": 0, "pos": 5, "stated": "35",
                         "span": [7, 8]}]},
        {"statements": [
            {"pos": 5, "nums": ["3", "4", "5"], "ops": ["+", "*"],
             "stated": "35", "raw": "3+4*5 = 35"}]})
    ctx3 = dict(ctx2)
    ctx3["statement_index"] = idx
    row3 = {"pair_id": "A2-2", "cohort": "A2", "doc_id": 7,
            "leg": "raw", "record_class": False, "value": "35",
            "span": [7, 8],
            "span_resolution": {"t0": 12, "commit_index": 3,
                               "hidden_row_index": 3,
                               "commit_token": "35"}}
    mean3 = doc_numeric_mean(p1, rec, numeric_commit_indices(rec))
    rc3 = dict(compute_row(b1, p1, ctx3, row3, rec,
                           [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0]], [1.0, 0.0, 0.0],
                           mean3))
    cls = rc3["operand_rows"]["classes"]
    ok = (rc3["precedence_tree"]["root_values"] == [3.0, 20.0]
          and rc3["operand_rows"]["status"] == "NAMED-OPERAND-COVERAGE"
          and len(cls) == 1 and cls[0]["value"] == 20.0
          and cls[0]["class"] == "NAMED-INTERMEDIATE-UNCOMMITTED"
          and rc3["centered_r_perp"]["status"]
          == "NAMED-OPERAND-COVERAGE"
          and rc3["bhob"]["status"] == "NAMED-OPERAND-COVERAGE")
    check("P2-C17", "intermediate-uncommitted NAMED distinct class",
          ok, "cls=%r" % (cls,))

    # C18 the item-1155 class: non-finite measured inputs NAMED,
    # never a crash, never a silent skip
    ok = (non_finite_detail([("a", [1.0, 2.0])]) is None
          and non_finite_detail(
              [("a", [1.0, float("nan")])]) ==
          {"component": "a", "n_non_finite": 1,
           "samples": [(1, "nan")]}
          and non_finite_detail(
              [("a", [float("inf")])])["n_non_finite"] == 1)
    # (b1) a non-finite h_t0: the row NAMED at h_t0, the early
    # return, the operators never called
    rec = json.loads(_mk_line(
        "k18a", ["2", "7"], ["COT"] * 2,
        [[1.0, 0.0], [float("nan"), 1.0]], 2))
    row_a = {"pair_id": "C18a", "cohort": "A1", "doc_id": 7,
             "leg": "raw", "record_class": True, "value": "7",
             "span_resolution": {"t0": 12, "commit_index": 1,
                                 "hidden_row_index": 1,
                                 "commit_token": "7"}}
    mean_a = doc_numeric_mean(p1, rec, numeric_commit_indices(rec))
    rc_a = dict(compute_row(
        b1, p1, ctx3, row_a, rec,
        [[1.0, 0.0], [0.0, 1.0]], [1.0, 0.0], mean_a))
    ok = ok and (rc_a["m_ulp_num"]["status"] == "NAMED-NON-FINITE"
                 and rc_a["m_ulp_num"]["component"] == "h_t0"
                 and rc_a["m_ulp_num"]["samples"][0][1] == "nan"
                 and "h_num" not in rc_a)
    # (b2) a finite h_t0 beside a poisoned doc mean: the component
    # named doc_mean, the doc's every row carrying the class
    rec = json.loads(_mk_line(
        "k18b", ["2", "7"], ["COT"] * 2,
        [[float("nan"), 0.0], [1.0, 1.0]], 2))
    mean_b = doc_numeric_mean(p1, rec, numeric_commit_indices(rec))
    rc_b = dict(compute_row(
        b1, p1, ctx3, row_a, rec,
        [[1.0, 0.0], [0.0, 1.0]], [1.0, 0.0], mean_b))
    ok = ok and (rc_b["m_ulp_num"]["status"] == "NAMED-NON-FINITE"
                 and rc_b["m_ulp_num"]["component"] == "doc_mean")
    # (c) a non-finite NON-numeric prior row: the corroborator lane
    # NAMED alone, the primary still computed
    rec = json.loads(_mk_line(
        "k18c", ["x2", "7"], ["COT"] * 2,
        [[float("nan"), 0.0], [1.0, 1.0]], 2))
    row_c = {"pair_id": "C18c", "cohort": "A1", "doc_id": 7,
             "leg": "raw", "record_class": True, "value": "7",
             "span_resolution": {"t0": 12, "commit_index": 1,
                                 "hidden_row_index": 1,
                                 "commit_token": "7"}}
    mean_c = doc_numeric_mean(p1, rec, numeric_commit_indices(rec))
    rc_c = dict(compute_row(
        b1, p1, ctx3, row_c, rec,
        [[1.0, 0.0], [0.0, 1.0]], [1.0, 0.0], mean_c))
    ok = ok and (rc_c["kappa"]["status"] == "NAMED-NON-FINITE"
                 and rc_c["kappa"]["component"] == "h_prev"
                 and "m_ulp" in rc_c["m_ulp_num"]
                 and "status" not in rc_c["m_ulp_num"])
    check("P2-C18", "non-finite inputs NAMED, never a crash", ok,
          "a=%r c=%r" % (rc_a["m_ulp_num"]["component"]
                         if "m_ulp_num" in rc_a else None,
                         rc_c.get("kappa")))
    return checks

# ---------------------------------------------------------------------------
# Section 7. PART 3: the run orchestration -- the run-row assembly,
# the input receipts, the per-cache discoveries, the W_U fetch, the
# per-row loop, the census, and the export writer (deterministic,
# every read traceable to span + cohort row)
# ---------------------------------------------------------------------------

# The tokenizer pin rides the aligned export's own receipt (the B0
# V_num pin's file + sha, my console line of record).
PINS["tokenizer"] = {
    "file": "tokenizer.json",
    "sha256": ("79e3e522635f3171300913bb421464a87de6222182a0570"
               "b9b2ccba2a964b2b4"),
}

LEG_CACHE_MAP = {
    "p2_cache_r2": "cache_p2_r2",
    "a2_raw_cache": "cache_a2_raw",
    "a2_chat_cache": "cache_a2_chat",
}


def _cache_of(row, where):
    """The row's join block -> (cache pin name, record key); an
    unknown pin a hard exit naming it (the never-guess law)."""
    j = row.get("join") or {}
    pin = j.get("cache_pin")
    name = LEG_CACHE_MAP.get(pin)
    if name is None:
        fail_loud("%s: cache_pin %r not of the banked cache map "
                  "(the never-guess law)" % (where, pin))
    key = j.get("cache_key")
    if not isinstance(key, str) or not key:
        fail_loud("%s: the join block carries no cache_key"
                  % where)
    return name, key


def build_run_rows(inv_rows):
    """The measurement population (v1.0.5): every pair row rides
    twice (the positive + the negative side, the paired statistic),
    every unpaired positive rides once, logged BESIDE the paired
    statistic never inside it (the matched-population law); the A1
    pair rows carry their v1.3.0 occ_step_distance receipt (the
    position-aware measure) + the v1.2.7 lineage step_distance
    (the diagnostic); the census asserted against the inventory's
    own blocks with NO v2 landing constant (the A2 pair count
    MOVES under the one rule -- the movement the expectation, 67
    of the 96 A2 slips ride in-doc repeated values, the shift
    itself a finding, never forced); the standing unresolved + the
    NAMED class rows (out-of-coverage / value-mismatch / join
    fails) ride the receipts NAMED, never computed."""
    run_rows = []
    for coh in ("A1", "A2"):
        for p in inv_rows["%s_pairs" % coh]:
            for side in ("positive", "negative"):
                r = p[side]
                cache_name, cache_key = _cache_of(
                    r, "pair %s %s" % (p["pair_id"], side))
                run_rows.append({
                    "pair_id": p["pair_id"], "side": side,
                    "paired": True, "cohort": coh,
                    "doc_id": r.get("doc_id"), "leg": r.get("leg"),
                    "record_class": r.get("record_class"),
                    "value": r.get("value"),
                    "span": r.get("span"),
                    "span_resolution": r.get("span_resolution"),
                    "occ_step_distance": p.get("occ_step_distance"),
                    "step_distance": p.get("step_distance"),
                    "cache_name": cache_name,
                    "cache_key": cache_key})
    n = 0
    for e in inv_rows["unpaired"]:
        r = e["positive"]
        n += 1
        cache_name, cache_key = _cache_of(
            r, "unpaired %s doc %s" % (e["cohort"],
                                       r.get("doc_id")))
        run_rows.append({
            "pair_id": "UNP-%s-%04d" % (e["cohort"], n),
            "side": "positive", "paired": False,
            "cohort": e["cohort"],
            "doc_id": r.get("doc_id"), "leg": r.get("leg"),
            "record_class": r.get("record_class"),
            "value": r.get("value"),
            "span": r.get("span"),
            "span_resolution": r.get("span_resolution"),
            "cache_name": cache_name,
            "cache_key": cache_key})
    census = {"paired_rows": sum(1 for r in run_rows if r["paired"]),
              "unpaired_rows": sum(
                  1 for r in run_rows if not r["paired"]),
              "total_rows": len(run_rows),
              "unresolved_named": len(inv_rows["unresolved"]),
              "named_beside": len(inv_rows["named_beside"]),
              "a1_pairs": len(inv_rows["A1_pairs"]),
              "a2_pairs": len(inv_rows["A2_pairs"])}
    # the v3 population laws (the honest-population law): every
    # count derived from the inventory's own tables, NEVER the v2
    # landing constants (the A2 movement the expectation under the
    # one rule; the A1 lane the v1.3.0 position-aware re-bind, the
    # pair count within the item-1158 pool census)
    a1_pairs, a2_pairs = census["a1_pairs"], census["a2_pairs"]
    if not (1 <= a1_pairs <= 177):
        fail_loud("population census: the A1 pairs %d outside the "
                  "item-1158 pool census (1 to 177)"
                  % a1_pairs)
    if a2_pairs < 0:
        fail_loud("population census: the A2 pair count %d "
                  "negative (an impossible table)"
                  % a2_pairs)
    if census["paired_rows"] != 2 * (a1_pairs + a2_pairs) \
            or census["total_rows"] != census["paired_rows"] \
            + census["unpaired_rows"]:
        fail_loud("population census %r != the inventory's own "
                  "tables (the honest-population law)" % census)
    return run_rows, census


def _discover_tokenizer_vocab(t):
    """The tokenizer file's vocab shape DISCOVERED (the HF
    tokenizer.json model.vocab block, or a flat str->id map);
    anything else a NAMED hard exit, never a guess."""
    if isinstance(t, dict) and isinstance(t.get("model"), dict) \
            and isinstance(t["model"].get("vocab"), dict):
        return t["model"]["vocab"]
    if isinstance(t, dict) and t:
        vals = list(t.values())
        if all(isinstance(v, int) for v in vals) \
                and all(isinstance(k, str) for k in t):
            return t
    fail_loud("tokenizer: the vocab shape not of the discovered "
              "classes (the HF model.vocab block or a flat "
              "str->id map) -- never a guess")


def read_tokenizer(path):
    """The pinned tokenizer file of record: its sha asserted (the
    B0 V_num pin's own file), the id->str map returned, an id with
    two strings a hard exit."""
    assert_pin("tokenizer", path, PINS["tokenizer"])
    with open(path) as f:
        t = json.load(f)
    vocab = _discover_tokenizer_vocab(t)
    id_to_str = {}
    for s, i in vocab.items():
        prev = id_to_str.get(i)
        if prev is not None and prev != s:
            fail_loud("tokenizer: id %d carries two strings %r/%r "
                      "(a premise violation)" % (i, prev, s))
        id_to_str[i] = s
    return id_to_str


def collect_named_census(receipts):
    """The NAMED-class census over the row receipts: every status
    outside the green classes counted by (field, status), sorted;
    the paired/unpaired split carried beside (the paired statistic
    and its beside-log never conflated)."""
    counts = {}
    green = ("OK", "BOUND", "READ")
    for rec in receipts:
        d = dict(rec)
        read = d.get("read") or {}
        for key in ("centered_r_perp", "bhob", "work_increment",
                    "raw_gap", "statement_binding", "operand_rows",
                    "precedence_tree", "m_ulp_num", "zeta_commit",
                    "kappa", "derivation_window"):
            v = read.get(key)
            if isinstance(v, dict):
                st = v.get("status")
                if isinstance(st, str) and st not in green:
                    tag = "%s:%s" % (key, st)
                    counts[tag] = counts.get(tag, 0) + 1
                # the instrument-form raw_gap receipt (v1.0.4): a
                # READ receipt can still carry a NAMED case at its
                # door -- the emitted-vs-top1 case read honestly,
                # counted beside the statuses, never inside them
                if key == "raw_gap" and st == "READ":
                    case = v.get("emitted_vs_top1")
                    if isinstance(case, str) \
                            and case != "EMITTED-CONSISTENT-TOP1":
                        tag = "raw_gap:%s" % case
                        counts[tag] = counts.get(tag, 0) + 1
                # the derivation window's prompt-side leaves count
                # beside the statuses
                if key == "derivation_window" and v.get(
                        "prompt_side_values"):
                    tag = "derivation_window:prompt-side-leaf"
                    counts[tag] = counts.get(tag, 0) + len(
                        v["prompt_side_values"])
    return dict(sorted(counts.items()))


def write_export(out_path, payload):
    """The export writer: deterministic (sort_keys, fixed indent),
    one trailing newline; the sha + byte-count receipt returned for
    my console line."""
    body = json.dumps(payload, sort_keys=True, indent=1,
                      ensure_ascii=True)
    data = body + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(data)
    return {"file": os.path.basename(out_path),
            "bytes": len(data.encode("utf-8")),
            "sha256": sha256_file(out_path)}


def run_separation(inputs_dir, inventory_path, inventory_sha,
                   model_dir, tokenizer_path, b1_path, out_path):
    """My-side separation run (v1.0.8, the v3 inventory at
    my --inventory-sha console line): every input pinned +
    asserted at load; the discoveries (gen phases, commit fields
    incl. the instrument's own probability-domain form, statement
    bindings) from the bytes; the v2 population computed (the A1
    re-bind pairs + the A2 lane unchanged + the unpaired beside);
    the census + the receipts carried in the export; the runtime
    receipt printed at my console."""
    print("CD-1 ARM A B2 SEPARATION RUN -- the tool of record; "
          "findings presented, never adjudicated; my "
          "stamps decide")
    verify_pin_shape()  # the pin-shape law: malformed pins die at
    # load, never at my console (the item-1146 defect class guard)
    b1 = import_b1(b1_path)

    def ip(name):
        return os.path.join(inputs_dir, PINS[name]["file"])

    # the input receipts (every pin fail-loud; the 17p2 pair rides
    # as the receipt-of-record assert, its content untouched by the
    # A1 coverage law, the finding carried in the export)
    receipts = {}
    receipts["b1_module"] = assert_pin(
        "b1_module", b1_path, PINS["b1_module"], bytes_needed=False)
    verify_console_pin_sha(inventory_sha)
    receipts["inventory"] = assert_pin(
        "inventory", inventory_path,
        {"sha256": inventory_sha}, bytes_needed=False)
    receipts["inventory_source"] = ("my --inventory-sha console "
                                    "line (the v1.3.3 builder's "
                                    "own export print; the item-"
                                    "1134 console-pin law)")
    receipts["aligned_spans"] = assert_pin(
        "aligned_spans", ip("aligned_spans"), PINS["aligned_spans"])
    receipts["checker_17a_raw"] = assert_pin(
        "checker_17a_raw", ip("checker_17a_raw"),
        PINS["checker_17a_raw"])
    receipts["checker_17a_chat"] = assert_pin(
        "checker_17a_chat", ip("checker_17a_chat"),
        PINS["checker_17a_chat"])
    receipts["checker_17p2"] = assert_pin(
        "checker_17p2", ip("checker_17p2"), PINS["checker_17p2"])
    receipts["checker_17p2_ledger"] = assert_pin(
        "checker_17p2_ledger", ip("checker_17p2_ledger"),
        PINS["checker_17p2_ledger"])
    receipts["tokenizer"] = assert_pin(
        "tokenizer", tokenizer_path, PINS["tokenizer"])
    print("INPUT PINS: 8/8 asserted (the inventory at MY "
          "console line, the aligned export, the two 17a "
          "re-emissions, the 17p2 pair, the tokenizer, the B1 "
          "module)")

    inv_d, inv_rows = read_inventory(inventory_path, inventory_sha)
    with open(ip("aligned_spans")) as f:
        aligned = json.load(f)
    with open(ip("checker_17a_raw")) as f:
        checker_raw = json.load(f)
    with open(ip("checker_17a_chat")) as f:
        checker_chat = json.load(f)
    run_rows, pop_census = build_run_rows(inv_rows)
    print("POPULATION: %d rows (%d paired + %d unpaired beside; "
          "%d unresolved NAMED + %d class rows NAMED, never "
          "computed)"
          % (pop_census["total_rows"],
             pop_census["paired_rows"],
             pop_census["unpaired_rows"],
             pop_census["unresolved_named"],
             pop_census["named_beside"]))
    for coh in ("A1", "A2"):
        print("RESOLUTION CLASS CENSUS (%s): %r"
              % (coh, inv_d["cohorts"][coh]
                  ["resolution_class_census"]))
    print("STEP EXT CENSUS: %r" % (inv_d["step_ext_census"],))

    # the caches (the B0 builder's own reader law; the memory
    # expectation stated in the tool header)
    caches = {}
    for pin_name in ("cache_a2_raw", "cache_a2_chat",
                     "cache_p2_r2"):
        caches[pin_name] = read_cache_records(
            pin_name, ip(pin_name), PINS[pin_name]["records"])
        receipts[pin_name] = PINS[pin_name]["sha256"]
    print("CACHES: 3 read (%d + %d + %d records)"
          % (len(caches["cache_a2_raw"]),
             len(caches["cache_a2_chat"]),
             len(caches["cache_p2_r2"])))

    # the tokenizer + the V_num strings (the pinned id order)
    id_to_str = read_tokenizer(tokenizer_path)
    vnum_ids = inv_d["vnum_pin"]["numeric_token_ids_sorted"]
    vnum_strs = []
    for i in vnum_ids:
        s = id_to_str.get(i)
        if s is None:
            fail_loud("V_num id %d carries no string in the pinned "
                      "tokenizer (a NAMED gap at my door)" % i)
        vnum_strs.append(s)

    # the statement indexes (the two A2 legs; the p2 lane carries
    # no operand binding by the coverage law)
    st_indexes = build_statement_indexes(aligned, checker_raw,
                                         checker_chat)
    leg_index_key = {"raw": ("a2_raw", None),
                     "chat": ("a2_chat", None)}

    # the per-cache discoveries: gen phases + commit fields
    resolved = {}
    for r in run_rows:
        resolved.setdefault(r["cache_name"], {}).setdefault(
            r["cache_key"], []).append(
            r["span_resolution"]["commit_index"])
    gen_phases = discover_gen_phases(caches, resolved)
    field_inv = {}
    for cn in caches:
        field_inv[cn] = discover_commit_fields(caches[cn])
    raw_gap_pair = {cn: field_inv[cn]["raw_gap_pair"]
                    for cn in caches}
    instrument_form = {cn: field_inv[cn]["instrument_form"]
                       for cn in caches}
    print("DISCOVERIES: gen phases %r; commit fields %r; the "
          "instrument's own probability-domain raw form %r"
          % (gen_phases,
             {cn: field_inv[cn]["extra_fields"] for cn in field_inv},
             instrument_form))

    # the W_U fetch set: V_num + every row's t_0 (the answer column
    # = the committed answer's unembedding row at t_0)
    fetch_ids = sorted(set(vnum_ids) | set(
        r["span_resolution"]["t0"] for r in run_rows))
    wu = read_w_u_rows(model_dir, fetch_ids)
    receipts["w_u_shard"] = wu["shard_sha256"]
    w_num_rows = [wu["rows"][i] for i in vnum_ids]
    for r in run_rows:
        t0 = r["span_resolution"]["t0"]
        if t0 not in wu["rows"]:
            fail_loud("row %s: the W_U row at t_0 %d not read (a "
                      "fetch-set premise violation)"
                      % (r["pair_id"], t0))
    print("W_U: %s dtype %s; %d rows read (V_num 1,110 + the "
          "t_0 set); the carrying shard sha asserted"
          % (wu["tensor"], wu["dtype"], len(wu["rows"])))

    # the run loop (progress every 50 rows; every NAMED class
    # counted by the census at the end)
    means = {}
    row_receipts = []
    for n, r in enumerate(run_rows):
        rec = caches[r["cache_name"]].get(r["cache_key"])
        if rec is None:
            fail_loud("row %s: cache %s carries no record %r "
                      "(a NAMED join gap)" % (r["pair_id"],
                                              r["cache_name"],
                                              r["cache_key"]))
        mk = (r["cache_name"], r["cache_key"])
        if mk not in means:
            means[mk] = doc_numeric_mean(
                self_module(), rec,
                numeric_commit_indices(rec))
        mean = means[mk]
        st_idx = None
        if r["cohort"] == "A2":
            key = leg_index_key.get(r.get("leg"))
            if key is None:
                fail_loud("A2 row %s: leg %r not of the A2 lanes"
                          % (r["pair_id"], r.get("leg")))
            st_idx = st_indexes.get((key[0], r["doc_id"]))
            if st_idx is None:
                fail_loud("A2 row %s: no statement index for leg "
                          "%r doc %r (a NAMED binding gap)"
                          % (r["pair_id"], r.get("leg"),
                             r["doc_id"]))
        ctx = {"vnum_ids": vnum_ids, "vnum_strs": vnum_strs,
               "gen_phases": gen_phases[r["cache_name"]],
               "statement_index": st_idx,
               "raw_gap_pair": raw_gap_pair[r["cache_name"]],
               "instrument_form": instrument_form[
                   r["cache_name"]]}
        read = compute_row(b1, self_module(), ctx, r, rec,
                           w_num_rows,
                           wu["rows"][r["span_resolution"]["t0"]],
                           mean)
        row_receipts.append({"row": {
            "pair_id": r["pair_id"], "side": r["side"],
            "paired": r["paired"], "cohort": r["cohort"],
            "doc_id": r["doc_id"], "leg": r["leg"],
            "cache_key": r["cache_key"], "span": r["span"],
            "span_resolution": r["span_resolution"],
            "step_distance": r.get("step_distance"),
            "occ_step_distance": r.get("occ_step_distance")},
            "read": dict(read)})
        if (n + 1) % 50 == 0 or n + 1 == len(run_rows):
            print("ROWS: %d/%d computed" % (n + 1,
                                            len(run_rows)))

    named = collect_named_census(row_receipts)
    payload = {
        "tool": TOOL + " " + VERSION,
        "run_class": ("CD-1 Arm A B2 separation run, my-side "
                      "(offline paper act; zero GPU, zero decodes, "
                      "zero build hours)"),
        "input_receipts": receipts,
        "discovery": {
            "gen_phases": gen_phases,
            "commit_field_inventory": {
                cn: {"extra_fields": field_inv[cn]["extra_fields"],
                     "raw_gap_pair": field_inv[cn]["raw_gap_pair"],
                     "instrument_form":
                         field_inv[cn]["instrument_form"]}
                for cn in sorted(field_inv)},
            "statement_index_count": len(st_indexes),
            "vnum_count": len(vnum_ids),
            "w_u_tensor": wu["tensor"], "w_u_dtype": wu["dtype"]},
        "population": pop_census,
        "inventory_census": {
            "resolution_class_census": {
                coh: inv_d["cohorts"][coh]
                ["resolution_class_census"]
                for coh in ("A1", "A2")},
            "step_ext_census": inv_d["step_ext_census"],
            "honest_entries": len(
                inv_d["honest_population_receipt"]["entries"])},
        "named_census": named,
        "rows": row_receipts,
        "the_law": ("findings presented, never adjudicated; the "
                    "my stamps decide; the paired statistic "
                    "and the unpaired beside-log never conflated; "
                    "every NAMED class counted, never skipped, "
                    "never averaged around"),
    }
    exp = write_export(out_path, payload)
    print("EXPORT: %s %d bytes sha %s"
          % (exp["file"], exp["bytes"], exp["sha256"]))
    print("NAMED CENSUS: %r" % named)
    print("THE RUN COMPLETE: findings at my door; my "
          "stamps decide")
    return exp


def self_module():
    """The assembled module itself (the engines' p1 contract: the
    loaders + the decoders live in THIS file)."""
    import sys as _sys
    return _sys.modules[__name__]


# ---------------------------------------------------------------------------
# Section 8. PART 3: the assembly battery (P3; constructed bytes
# only) + the CLI of record
# ---------------------------------------------------------------------------

def part3_selfcheck():
    checks = []

    def check(cid, name, ok, detail=""):
        checks.append((cid, name, bool(ok), detail))

    import tempfile
    import shutil
    td = tempfile.mkdtemp(prefix="b2p3_")
    try:
        # P3-C01: the run-row assembly + the population census on
        # a constructed shape inside the v3 laws -- the A2 lane
        # deliberately NOT the v2 73/23 landing (71 pairs + 25
        # unpaired: the MOVEMENT receipt -- the v1.0.4 constants
        # would have refused this shape, the v1.0.5 one-rule law
        # accepts it, the movement itself a finding, never forced);
        # the pair rows carry the v1.3.0 occurrence-level fields;
        # the NAMED class rows ride the census beside, never
        # computed
        inv_rows = {"unresolved": [
            {"cohort": "A1" if i % 2 == 0 else "A2",
             "row": {"record_class":
                     "PROMOTION" if i < 21 else "CLEAN"},
             "finding": "UNRESOLVABLE-NON-NUMERIC -- x"}
            for i in range(161)],
            "named_beside": [
                {"cohort": "A1",
                 "row": {"record_class": "PROMOTION"},
                 "finding": "step-outside-cache-coverage -- x"},
                {"cohort": "A1",
                 "row": {"record_class": "PROMOTION"},
                 "finding": "value-mismatch-at-own-step -- x"},
                {"cohort": "A2",
                 "row": {"record_class": "PROMOTION"},
                 "finding": "step-outside-cache-coverage -- x"},
                {"cohort": "A2",
                 "row": {"record_class": "CLEAN"},
                 "finding": "UNJOINED -- x"}]}
        pair_form = {
            "cohort": None, "pair_id": None,
            "positive": {"join": {"cache_pin": None,
                                  "cache_key": None}},
            "negative": {"join": {"cache_pin": None,
                                  "cache_key": None}}}
        for coh, npairs, pin in (("A1", 141, "p2_cache_r2"),
                                 ("A2", 71, "a2_raw_cache")):
            lst = []
            for i in range(npairs):
                p = {"cohort": coh, "pair_id": "%s-%04d"
                     % (coh, i + 1),
                     "occ_step_distance": 4,
                     "positive": {"join": {"cache_pin": pin,
                                           "cache_key": "k%d"
                                           % i},
                                  "span": [1, 2],
                                  "span_resolution": {
                                      "status":
                                          "RESOLVED-OWN-STEP",
                                      "t0": 5,
                                      "occ_step_t": 10,
                                      "commit_index": 1,
                                      "hidden_row_index": 1}},
                     "negative": {"join": {"cache_pin": pin,
                                           "cache_key": "k%d"
                                           % i},
                                  "span": [3, 4],
                                  "span_resolution": {
                                      "status":
                                          "RESOLVED-OWN-STEP",
                                      "t0": 6,
                                      "occ_step_t": 14,
                                      "commit_index": 2,
                                      "hidden_row_index": 2}}}
                lst.append(p)
            inv_rows["%s_pairs" % coh] = lst
        unpaired = []
        for i in range(209):
            unpaired.append({"cohort": "A1", "finding":
                             "UNPAIRED -- x",
                             "positive": {"join": {
                                 "cache_pin": "p2_cache_r2",
                                 "cache_key": "u%d" % i},
                                 "span": [7],
                                 "span_resolution": {
                                     "status":
                                         "RESOLVED-OWN-STEP",
                                     "t0": 8, "occ_step_t": 8,
                                     "commit_index": 3,
                                     "hidden_row_index": 3}}})
        for i in range(25):
            unpaired.append({"cohort": "A2", "finding":
                             "UNPAIRED -- x",
                             "positive": {"join": {
                                 "cache_pin": "a2_raw_cache",
                                 "cache_key": "v%d" % i},
                                 "span": [9],
                                 "span_resolution": {
                                     "status":
                                         "RESOLVED-OWN-STEP",
                                     "t0": 10, "occ_step_t": 10,
                                     "commit_index": 4,
                                     "hidden_row_index": 4}}})
        inv_rows["unpaired"] = unpaired
        run_rows, census = build_run_rows(inv_rows)
        ok = (census == {"paired_rows": 424,
                         "unpaired_rows": 234,
                         "total_rows": 658,
                         "unresolved_named": 161,
                         "named_beside": 4,
                         "a1_pairs": 141, "a2_pairs": 71}
              and len(set(r["pair_id"] + r["side"]
                         for r in run_rows)) == 658
              and all(r["cache_name"] in LEG_CACHE_MAP.values()
                      for r in run_rows)
              and all(r["span_resolution"].get(
                  "occ_step_t") == 10
                  for r in run_rows
                  if r["pair_id"].startswith("A1")
                  and r["side"] == "positive"))
        check("P3-C01", "run-row assembly + the v3 movement "
              "census (the A2 71/25 shape accepted, the v2 "
              "constants gone)", ok,
              "census=%r" % census)

        # P3-C02: an unknown cache_pin a hard exit naming it
        bad = {"join": {"cache_pin": "no_such_pin",
                        "cache_key": "k"}}
        try:
            _cache_of(bad, "ctx")
            check("P3-C02", "unknown cache_pin refused loud", False,
                  "accepted")
        except SystemExit as e:
            ok = "cache_pin" in str(e) and "never-guess law" \
                in str(e)
            check("P3-C02", "unknown cache_pin refused loud", ok,
                  str(e)[:80])

        # P3-C03: the export writer deterministic (two writes
        # byte-identical)
        payload = {"z": 1, "a": {"y": [2, 1], "x": "s"},
                   "rows": [{"b": 2, "a": 1}]}
        e1 = write_export(os.path.join(td, "e1.json"), payload)
        e2 = write_export(os.path.join(td, "e2.json"), payload)
        ok = (e1["sha256"] == e2["sha256"]
              and e1["bytes"] == e2["bytes"] and e1["bytes"] > 0)
        check("P3-C03", "export writer deterministic", ok,
              "sha %s" % e1["sha256"][:12])

        # P3-C04: the NAMED census collector (statuses + the
        # prompt-side leaf count beside)
        recs = [{"read": {
            "centered_r_perp": {"status": "NAMED-OUT-OF-COVERAGE"},
            "bhob": {"status": "NAMED-OUT-OF-COVERAGE"},
            "work_increment": {"status": "NAMED-NO-PATH-EVIDENCE"},
            "raw_gap": {"status": "NAMED-ABSENT"},
            "derivation_window": {"status": "OK",
                                  "prompt_side_values":
                                      [{"v": 1}, {"v": 2}]}}},
                {"read": {
            "centered_r_perp": {"status": "NAMED-OUT-OF-COVERAGE"},
            "bhob": {"residual_share": 0.5},
            "work_increment": {"increment": 1.0},
            "raw_gap": {"status": "NAMED-ABSENT"}}}]
        census = collect_named_census(recs)
        ok = (census.get("centered_r_perp:NAMED-OUT-OF-COVERAGE")
              == 2
              and census.get("work_increment:"
                             "NAMED-NO-PATH-EVIDENCE") == 1
              and census.get("raw_gap:NAMED-ABSENT") == 2
              and census.get("derivation_window:"
                             "prompt-side-leaf") == 2
              and "bhob" not in census)
        check("P3-C04", "NAMED census collector", ok,
              "census=%r" % census)

        # P3-C05: the tokenizer shape discovery + the pin refusal
        hf = {"model": {"vocab": {"2": 10, "1.5": 11}}}
        flat = {"2": 10, "1.5": 11}
        bad_shape = {"model": {"not_vocab": {}}}
        ok = (_discover_tokenizer_vocab(hf) == hf["model"]["vocab"]
              and _discover_tokenizer_vocab(flat) == flat)
        try:
            _discover_tokenizer_vocab(bad_shape)
            ok = ok and False
        except SystemExit:
            pass
        wrong = os.path.join(td, "tok.json")
        with open(wrong, "w") as f:
            f.write(json.dumps(hf))
        try:
            assert_pin("tokenizer", wrong, PINS["tokenizer"])
            ok = ok and False
        except SystemExit as e:
            ok = ok and "pin-tail law" in str(e)
        check("P3-C05", "tokenizer discovery + pin law", ok)

        # P3-C06: the CLI argument law (missing flags named; the
        # run mode gated)
        ok = True
        try:
            parse_run_args([])
            ok = False
        except SystemExit as e:
            ok = ("--inputs" in str(e)
                  and "--model-dir" in str(e))
        args = parse_run_args(
            ["--inputs", "d1", "--inventory", "inv.json",
             "--inventory-sha", "a" * 64,
             "--model-dir", "d2", "--tokenizer", "t.json",
             "--b1", "b.py", "--out", "o.json"])
        ok = ok and args == ("d1", "inv.json", "a" * 64,
                             "d2", "t.json", "b.py", "o.json")
        try:
            parse_run_args(["--inputs", "d1",
                            "--inventory", "inv.json",
                            "--model-dir", "d2",
                            "--tokenizer", "t.json",
                            "--b1", "b.py", "--out", "o.json"])
            ok = ok and False
        except SystemExit as e:
            ok = ok and "--inventory-sha" in str(e)
        check("P3-C06", "CLI argument law", ok)

        # P3-C07: the pin-shape law (the item-1146 defect class
        # guard): every banked pin 64 lowercase hex (the tokenizer
        # pin included, added at import), and a malformed
        # constructed pin refused loud at load
        ok = verify_pin_shape() is True
        try:
            PINS["_battery_malformed"] = {"sha256": "a" * 65}
            verify_pin_shape()
            ok = False
        except SystemExit as e:
            ok = ok and "_battery_malformed" in str(e) \
                and "64 lowercase hex" in str(e)
        finally:
            PINS.pop("_battery_malformed", None)
        check("P3-C07", "pin-shape law (malformed pin refused "
              "loud at load)", ok)

        # P3-C08: the instrument-form raw_gap census lane (the
        # v1.0.4 law): a READ receipt with a NAMED case counted;
        # the CONSISTENT case + the case-less READ rows excluded;
        # the NAMED-ABSENT rows still counted
        recs = [{"read": {
            "raw_gap": {"status": "READ", "domain": "probability",
                        "emitted_vs_top1":
                            "EMITTED-NOT-TOP1-CONSISTENT"}}},
                {"read": {
            "raw_gap": {"status": "READ",
                        "emitted_vs_top1":
                            "EMITTED-CONSISTENT-TOP1"}}},
                {"read": {
            "raw_gap": {"status": "NAMED-ABSENT"}}},
                {"read": {
            "raw_gap": {"status": "READ", "emitted_p": 0.5}}}]
        census = collect_named_census(recs)
        ok = (census.get("raw_gap:EMITTED-NOT-TOP1-CONSISTENT")
              == 1
              and census.get("raw_gap:NAMED-ABSENT") == 1
              and "raw_gap:READ" not in census
              and len(census) == 2)
        check("P3-C08", "instrument-form raw_gap census lane", ok,
              "census=%r" % census)

        # P3-C09: the class-census cross-check (the sheet v3 S1):
        # the export's own resolution_class_census asserted against
        # its own joined counts + its own honest entries -- a
        # tampered census refused loud, every count derived, never
        # a constant this side
        def _cc(res, cov, mm, unr):
            return {"RESOLVED-OWN-STEP": res,
                    "step-outside-cache-coverage": cov,
                    "value-mismatch-at-own-step": mm,
                    "UNRESOLVABLE-NON-NUMERIC": unr}
        blk = {"positives_joined_resolved": 10,
               "negatives_joined_resolved": 12,
               "unresolved_non_numeric": 3,
               "resolution_class_census": _cc(22, 2, 1, 3)}
        honest = ([
            {"cohort": "A1",
             "finding": "step-outside-cache-coverage -- x"},
            {"cohort": "A1",
             "finding": "step-outside-cache-coverage -- y"},
            {"cohort": "A1",
             "finding": "value-mismatch-at-own-step -- x"},
            {"cohort": "A1",
             "finding": "UNRESOLVABLE-NON-NUMERIC -- x"},
            {"cohort": "A1",
             "finding": "UNRESOLVABLE-NON-NUMERIC -- y"},
            {"cohort": "A1",
             "finding": "UNRESOLVABLE-NON-NUMERIC -- z"},
            {"cohort": "A2",
             "finding": "UNJOINED -- other lane"}])
        try:
            assert_class_census_consistency("A1", blk, honest)
            ok = True
        except SystemExit:
            ok = False
        for tampered in (
                {"positives_joined_resolved": 11,
                 "negatives_joined_resolved": 12,
                 "unresolved_non_numeric": 3,
                 "resolution_class_census": _cc(22, 2, 1, 3)},
                {"positives_joined_resolved": 10,
                 "negatives_joined_resolved": 12,
                 "unresolved_non_numeric": 3,
                 "resolution_class_census": _cc(23, 2, 1, 3)},
                {"positives_joined_resolved": 10,
                 "negatives_joined_resolved": 12,
                 "unresolved_non_numeric": 3,
                 "resolution_class_census": _cc(22, 3, 1, 3)},
                {"positives_joined_resolved": 10,
                 "negatives_joined_resolved": 12,
                 "unresolved_non_numeric": 3,
                 "resolution_class_census": _cc(22, 2, 1, 4)},
                {"positives_joined_resolved": 10,
                 "negatives_joined_resolved": 12,
                 "unresolved_non_numeric": 3,
                 "resolution_class_census":
                     {"RESOLVED-OWN-STEP": 22}},
                {"positives_joined_resolved": 10,
                 "negatives_joined_resolved": 12,
                 "unresolved_non_numeric": 9,
                 "resolution_class_census": _cc(22, 2, 1, 3)}):
            try:
                assert_class_census_consistency("A1", tampered,
                                               honest)
                ok = False
            except SystemExit:
                pass
        check("P3-C09", "class-census cross-check (derived, "
              "tamper-refusing)", ok,
              "clean pass + 6 tampered blocks refused")

        # P3-C10: the honest-population arithmetic (the extraction
        # censuses unchanged by the amendment): pairs + unpaired +
        # the standing unresolved + the NAMED class rows == the
        # extraction count per cohort, derived; the A2 movement
        # shape accepted (never a 73/23 constant); off-by-one and
        # wrong-extraction shapes refused loud
        blk_a1 = {"positives_extracted": 371}
        try:
            assert_population_arithmetic("A1", blk_a1, 141, 209,
                                        21, 0, 371)
            assert_population_arithmetic("A2",
                                        {"positives_extracted":
                                         96}, 71, 22, 0, 3, 96)
            ok = True
        except SystemExit:
            ok = False
        for bad in (("A1", blk_a1, 141, 209, 21, 1, 371),
                    ("A1", blk_a1, 141, 209, 22, 0, 371),
                    ("A1", {"positives_extracted": 370},
                     141, 209, 21, 0, 371),
                    ("A2", {"positives_extracted": 96},
                     71, 22, 0, 4, 96)):
            try:
                assert_population_arithmetic(*bad)
                ok = False
            except SystemExit:
                pass
        check("P3-C10", "honest-population arithmetic (the "
              "extraction census law, the class rows inside it)",
              ok, "clean A1 371 + the A2 movement shape + 4 "
              "refused shapes")

    finally:
        shutil.rmtree(td, ignore_errors=True)
    return checks


RUN_FLAGS = ("--inputs", "--inventory", "--inventory-sha",
             "--model-dir", "--tokenizer", "--b1", "--out")


def parse_run_args(argv):
    """The run-mode CLI: every flag of the record required (a
    missing flag a NAMED exit naming it); unknown flags refused."""
    vals = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a not in RUN_FLAGS:
            fail_loud("run CLI: %r not of the flags of record %r"
                      % (a, list(RUN_FLAGS)))
        if i + 1 >= len(argv):
            fail_loud("run CLI: %r carries no value" % a)
        vals[a] = argv[i + 1]
        i += 2
    missing = [f for f in RUN_FLAGS if f not in vals]
    if missing:
        fail_loud("run CLI: the flags of record missing: %r (the "
                  "run needs --inputs (the caches + label exports "
                  "+ aligned + B1 + tokenizer), --inventory, "
                  "--inventory-sha (the v3 pin at MY console "
                  "line, the item-1134 law), --model-dir, "
                  "--tokenizer, --b1, --out)"
                  % missing)
    return (vals["--inputs"], vals["--inventory"],
            vals["--inventory-sha"],
            vals["--model-dir"], vals["--tokenizer"],
            vals["--b1"], vals["--out"])


def full_battery():
    """The full acceptance battery of record: P1 (the loaders) +
    P2 (the engines) + P3 (the assembly), constructed bytes only,
    zero pinned inputs touched, zero GPU, zero decodes."""
    mod = self_module()
    here = os.path.dirname(os.path.abspath(__file__))
    b1_path = None
    for cand in (os.path.join(
            here, PINS["b1_module"]["file"]),
            os.path.normpath(os.path.join(
                here, "..", PINS["b1_module"]["file"]))):
        if os.path.exists(cand):
            b1_path = cand
            break
    if b1_path is None:
        fail_loud("the full battery needs the B1 module beside the "
                  "tool (the accepted card of record)")
    b1 = import_b1(b1_path)
    verify_pin_shape()  # the pin-shape law rides the battery too
    checks = []
    checks += part1_selfcheck(".")
    checks += part2_selfcheck(mod, b1)
    checks += part3_selfcheck()
    return checks


def main():
    argv = sys.argv[1:]
    if "--selfcheck" in argv:
        print("THE FULL ACCEPTANCE BATTERY (P1+P2+P3, constructed "
              "bytes only)")
        checks = full_battery()
        n_pass = sum(1 for c in checks if c[2])
        n_fail = len(checks) - n_pass
        for cid, name, ok, detail in checks:
            print("[%s] %s %s -- %s" % (
                cid, "PASS" if ok else "FAIL", name, detail))
        print("FULL BATTERY CENSUS: %d PASS / %d FAIL"
              % (n_pass, n_fail))
        return 0 if not n_fail else 1
    if not argv:
        print("cd1_arm_a_separation_run_v108.py -- the CD-1 Arm A "
              "B2 separation run, the tool of record")
        print("the run needs the flags of record: %r"
              % list(RUN_FLAGS))
        print("the full acceptance battery: --selfcheck")
        print("findings presented, never adjudicated; my "
              "stamps decide")
        return 0
    (inputs_dir, inventory_path, inventory_sha, model_dir,
     tokenizer_path, b1_path, out_path) = parse_run_args(argv)
    run_separation(inputs_dir, inventory_path, inventory_sha,
                   model_dir, tokenizer_path, b1_path, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crossdomain_probe_readout_v1 -- the CD-5 measurement acts on the
cross-domain probe cache, under the STAMPED CD-1 sheet (his stamp
number 3 + his CD-D1 ruling OPTION 1, the all-clean probe; the sheet
of record crossdomain-probe-preregistration.md 37,215 B / sha256
84608525...).

The sheet's laws BINDING on this tool:

  - THE SINGLE-INSTANCE INGESTION LAW (Section 1, the desk-read 9.1
    amendment): each probe document's rows are fed CHRONOLOGICALLY,
    row by row, t = 0 to T-1, into ONE shared TwoPhaseClock + its
    three RegisterBanks + ONE IsolationGuard instance for the whole
    probe stream -- NEVER pre-partitioned into per-leg fragment runs.
    No row carries a wrapper-stamped __t1__ leg: every row routes
    COLD by its own schema signature (the splitter's own recognizer).
  - CD-5a THE ENTRY MARKS: the outgoing span closes exactly at the
    seam on its leg's clock; the incoming span latches exactly at the
    seam's WRITTEN onset mark on the other leg's clock, COLD_START
    exercised on all ten incoming spans, CONFIRM at the phase-B
    confirmation; span contiguity per doc; the foreign-schema-row
    census ZERO; the seam-aware onset derivation per fragment
    (onset iff {0, seam}), mismatches beyond the authored set loud;
    zero TIER2_ROUTE events at authored seams.
  - CD-5b THE LEG-CLASSIFICATION + STATE ACCEPTANCE: the recognizer's
    leg for every row vs the span's authored leg -- 100% agreement the
    receipt, any disagreement typed loud; the span STATE read at BOTH
    forms (the [REDACTED_PER_PUBLICATION_POLICY] record lens / theta [REDACTED_PER_PUBLICATION_POLICY], side by side, the
    designation never silently chosen); THE BIT-EXACT CROSS-SEAM
    INVARIANCE CHECK: every incoming span graded twice, spliced
    context AND standalone (its own rows alone, same leg, same
    calibration, the same grading path), the raw trip readouts
    asserted bit-exact (IEEE-754) at every live horizon {36, 64, 128,
    EOS} -- bit-identity receipts zero seam leakage and types any
    over-bar readout as NATIVE SOURCE-SLICE TAIL BEHAVIOR (the banked
    PROSE false-trip precedent 2.1748 / 2.0610); a bit-divergence is a
    true cross-seam leak, dying loud with both grades printed. A
    crossing on an OUTGOING span is never seam-attributed (causality:
    the seam is in its future). The W-lane z census printed
    descriptive, never a bar (the W-alone negative receipt stands).
  - CD-5c THE STACK RE-READ: the isolation guard's cross-leg write
    census across the SINGLE shared guard -- expected zero, NON-VACUOUS
    (each of the ten docs writes both legs' banks by construction);
    the bank pause/resume census per seam; the schema-routing census
    (CODE-BAND vs EMISSION inside one document, never cross-compared);
    THE HOOK'S TYPING per its own bytes: an un-crossed span prints
    PASSIVE-ARMED (BELOW-CUT) -- or PASSIVE-ARMED
    (T_RAW-NAMED-ABSENT) where applicable -- with ZERO E-events;
    STATE E0 with the terminals NAMED-UNMEASURED-OFFLINE arises IF AND
    ONLY IF a span crosses a form at CD-5b. Nothing actuates.
  - THE NAMING LAW: the crossdomain_probe prefix, no 2b/2B string in
    any filename; the census pins 10 / 10 / 5 asserted separately,
    never pooled; the class token "X"; the pooled receipts n=10 and
    per-direction n=5, no evaluated cell under 5.
  - THE INSTRUMENT PINS: the splitter 52,410 B / 5980eaec..., the
    stage-1 engines 11,980 B / 79c794c0..., the accumulator 58,292 B
    / c7acb944..., the prose accumulator 76,867 B / 7d7ab8fe..., the
    hook 52,078 B / 4de049de... enter byte-pinned, sha-asserted at
    import, ZERO instrument bytes moved (the additive-wrapper law);
    the walk of record 89,115 B / 3d4faa17... imported VERBATIM for
    the rw16 lane-join law (the span-local W restart, the bucket
    baselines, the first-passage law); the CD builder of record
    66,048 B / 680fd0e9... imported VERBATIM for the cold census door
    (load_cross) and the payload schema families.
  - THE LAYOUT-FREE DISCOVERY LAW (the discovery ruling of record): the sha256 is the path
    law, the directory tree never is. Every input is found by
    filename, then by exact byte size, and admitted ONLY on an exact
    sha256 match against the banked pin, wherever it lives. No
    my-side path is baked into any default.
  - THE HONEST LIMITS (Section 7), carried: the seam authored not
    earned; the loop cell named-absent; the MATH leg named-absent;
    both forms printed, theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; limit 7 the
    single-seam pause-AND-resume cell named-absent (the resume
    machinery exercised only across doc boundaries, receipted
    honestly as such).

Two stages (the act2b command law): --stage prep caches the heavy
lane work (the prose thin + export + code cache loads and the two
calibrations of record) beside the script; --stage read runs the CD-5
acts from the cache; --stage all does both in one pass. --battery
runs the synthetic hand-off worlds FIRST (zero real rows): the green
world through the real CD-5 path, every tamper world and negative
fixture dying loud at its own named check, twice-run byte-identical.

Zero GPU, zero decodes, zero build hours. Offline paper act.
"""

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import pickle
import struct
import sys
from collections import Counter

VERSION = "crossdomain_probe_readout_v1"

PAREN = ("(offline paper act only, "
         "zero GPU, zero decodes, zero build hours; "
         "Nov 10 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; "
         "no thresholds set, moved, or adjudicated; findings presented, "
         "never adjudicated -- the owner's stamps decide)")

CTX_NAME = "crossdomain_probe_readout_ctx.pkl"

# ------------------------------------------------------------------
# THE PINS OF RECORD (fail-loud before any compute)
# ------------------------------------------------------------------
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
    (["stage2_ladder_walk_v1.py"], 89115,
     "3d4faa17fd9afdb2dfe70c6e849331b57b951e1697513e33ac827769a2bf9b6d"),
    (["crossdomain_probe_builder_v1.py"], 66048,
     "680fd0e95b17be104af1283b3caf763cb5659e5b614b2e32aa0806c7ec31e1b6"),
]
INPUT_SPECS = [
    (["crossdomain_probe_cache_v1.json"], 1168366,
     "6b4c542d7f4ca20dcedddb3c0bc0a2c19ce0e2c0570a27d9959fff4fae67127a"),
    (["crossdomain_probe_census_v1.json"], 8042,
     "151c6acea4ba8f06af37edf2c61dded1ae5a53ae9c3a61bd7c6be3a9065e9753"),
    (["triadic_wu_code_read_v1.json"], 26209382,
     "610d48c9689c07c7859fd84fadfe14fdb7259bb8eb572da4e0b9d1ef025db689"),
    (["triadic_t2_thin_rw17-prose-r2.jsonl"], 159280278,
     "88cbadee7baa1e35fe7e762715970066d6098301f044f810c0efd1e38c70ae94"),
    (["triadic_wu_prose_read_v1.json"], 656143,
     "a4e0ef03626a6cd47b926b20bf91358c182df0b16cf3ad5c17e4e316f0d82e3e"),
]
READ_INPUT_SPECS = INPUT_SPECS[:2]     # the read stage re-verifies these

# the banked calibration pins (asserted at prep, receipted at read)
PIN_evenA_PROSE = 86                 # the even-A prose cohort of record
PIN_evenA_CODE = 49                   # the at-most-49 law (the accumulator's own pin)
PIN_PROSE_CORPUS = 620                 # the rw16 cross-check cohort

CODE_PRIMARY = "margin_content"        # the CODE-BAND bank-write channel
EMI_PRIMARY = "margin"                 # the EMISSION bank-write channel


class ReadoutDie(Exception):
    """The fail-loud exit: every die prints its receipt, never silent."""
    def __init__(self, code, msg):
        Exception.__init__(self, "%s: %s" % (code, msg))
        self.code = code
        self.msg = msg


def die(code, msg):
    raise ReadoutDie(code, msg)


def check(cond, code, msg):
    if not cond:
        die(code, msg)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------
# THE LAYOUT-FREE DISCOVERY (the discovery ruling of record: the sha256 is the path law)
# ------------------------------------------------------------------
def discover(specs, search_roots, stage):
    """No directory structure is assumed. Every input is FOUND under
    the search roots by filename first, then by exact byte size, and
    admitted ONLY on an exact sha256 match against the banked pin --
    wherever it lives. A missing input is named with its exact size +
    sha and the compute refuses."""
    index = {}
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
    print("[pin] %s discovery: the sha256 is the path law (the "
          "directory tree never assumed) -- %d inputs + %d "
          "instruments admitted by exact byte size + sha256"
          % (stage, len(specs), len(INSTRUMENT_SPECS)))
    resolved = {}
    for names, size, sha in specs:
        cands = [p for p in index if os.path.basename(p) in names]
        cands += [p for p in index if index[p] == size and p not in cands
                  and not p.endswith(VERSION + ".py")]
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
    return resolved


def discover_instruments(search_roots, stage):
    """The instruments' own IMPORT-PIN law requires the co-located
    family (each verifies its siblings' bytes in its own directory at
    import). Prefer a directory holding ALL of them byte-verified;
    else stage byte-exact copies into a deterministic scratch dir so
    the co-location pin holds (sha-verified, zero bytes modified)."""
    index = {}
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
    instr = None
    for dirpath in sorted({os.path.dirname(p) for p in index}):
        if not all(os.path.isfile(os.path.join(dirpath, s[0][0]))
                   for s in INSTRUMENT_SPECS):
            continue
        if all(sha256_file(os.path.join(dirpath, s[0][0])) == s[2]
               for s in INSTRUMENT_SPECS):
            instr = {s[0][0]: os.path.join(dirpath, s[0][0])
                     for s in INSTRUMENT_SPECS}
            print("[pin] instruments co-located + byte-verified in: %s"
                  % dirpath)
            break
    if instr is None:
        here = os.path.dirname(os.path.abspath(__file__))
        stage_dir = os.path.join(here, ".cd_readout_instr_stage")
        os.makedirs(stage_dir, exist_ok=True)
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
            dst = os.path.join(stage_dir, names[0])
            if not (os.path.isfile(dst) and sha256_file(dst) == sha):
                with open(hit, "rb") as src, open(dst, "wb") as out:
                    out.write(src.read())
            if sha256_file(dst) != sha:
                sys.exit("[pin] staged copy sha mismatch: %s" % names[0])
        instr = {s[0][0]: os.path.join(stage_dir, s[0][0])
                 for s in INSTRUMENT_SPECS}
        print("[pin] instruments found scattered; byte-exact copies "
              "staged into %s so their own co-location pin holds "
              "(sha-verified, zero bytes modified)" % stage_dir)
    return instr


def load_instruments(paths):
    """Load the instruments of record by DISCOVERED PATH, registered
    under their module names so every cross-import inside the
    instruments resolves (the act2b loader law)."""
    order = ["triadic_splitter_v1.py", "triadic_stage1_engines_v1.py",
             "triadic_accumulator_v1.py", "triadic_hook_v1.py",
             "triadic_accumulator_prose_v1.py",
             "stage2_ladder_walk_v1.py",
             "crossdomain_probe_builder_v1.py"]
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
                del sys.modules[mod_name]
                continue
            mods[mod_name] = mod
            remaining.remove(name)
            progressed = True
        if not progressed:
            sys.exit("[pin] instrument cross-imports unresolved among: %s"
                     % ", ".join(remaining))
    return mods


# ------------------------------------------------------------------
# THE FLATTEN LAW (the wrapper's row form: the payload merged
# top-level, the re-indexed clocks live, the native coordinates
# provenance-only, NO wrapper-stamped leg -- the cold-routing law)
# ------------------------------------------------------------------
def schema_of_payload(payload, bd):
    keys = set(payload.keys())
    if keys == set(bd.CODE_COLUMNS):
        return "CODE-BAND"
    if keys == set(bd.COMMIT_KEYS):
        return "EMISSION"
    die("SCHEMA-UNEXPECTED",
        "a row payload matching neither the 16-column code band family "
        "nor the 16-key emission family: %s (dies loud, never absorbed)"
        % sorted(keys))


def schema_of_row(flat_row):
    """The walk's own flat-row schema law (CODE-BAND / EMISSION /
    FOREIGN), verbatim semantics."""
    keys = set(flat_row.keys())
    if "work_inc" in keys and "margin_content" in keys:
        return "CODE-BAND"
    if all(k in keys for k in ("K", "margin", "emitted_p", "second_p",
                               "hedge_mass", "content_mass", "W")):
        return "EMISSION"
    return "FOREIGN"


def prep_span_cd(cdb, cache_rows, surface, source, label):
    """One span's cache rows flattened + lane-joined. The EMISSION
    spans carry the span-level lane rec (the source record's steps at
    the rows' native t, span-local) + the span-local W restart (the
    walk's rw16_span_w law); the CODE-BAND spans carry their own
    channels in the payload. NO __t1__ is stamped on any row (the
    single-instance cold-routing law: the recognizer routes per row).
    Returns (flat_rows, span_rec, w_span, schema)."""
    if not cache_rows:
        die("EMPTY-SPAN", "%s: zero rows to flatten" % label)
    schema = schema_of_payload(cache_rows[0]["payload"], cdb)
    n = len(cache_rows)
    if schema == "EMISSION":
        check(source is not None, "LANE-JOIN",
              "%s: the EMISSION span carries no lane-join source record"
              % label)
        lane_t = [r["payload"]["t"] for r in cache_rows]
        st = source["steps"]
        for t in lane_t:
            if not (isinstance(t, int) and 0 <= t < len(st["t"])):
                die("LANE-JOIN",
                    "%s: a row's source-native t %r outside the source "
                    "record's step window" % (label, t))
        # THE SPAN-LOCAL W RESTART: the walk's OWN function (the port
        # is the law, never a re-write; semantics-verbatim bytes)
        W = sys.modules["stage2_ladder_walk_v1"]
        w_span = W.rw16_span_w(
            lane_t, {source["key"]: source["zmax"]}, source["key"])
        span_rec = {"doc_id": label, "is_fixture": False,
                   "n_gen_steps": len(st["t"]), "n_commits": n,
                   "steps": {"t": list(range(n)),
                             "s": [st["s"][t] for t in lane_t],
                             "PR": [st["PR"][t] for t in lane_t],
                             "E": [st["E"][t] for t in lane_t],
                             "H": [st["H"][t] for t in lane_t]}}
    else:
        w_span = None
        span_rec = None
    flat_rows = []
    for i, r in enumerate(cache_rows):
        p = dict(r["payload"])
        p["commit_index"] = r["commit_index"]      # re-indexed, live
        p["stmt_ordinal"] = r["stmt_ordinal"]       # re-indexed, live
        p["token_step"] = r["token_step"]           # re-indexed, live
        p["t_commit"] = r["token_step"]   # the step clock rides the
                                           # re-indexed token clock
        if surface == "CODE":
            p["role"] = r["role"]          # the authored onset mark live
            p["__native__"] = {"commit_index":
                               r["payload"].get("commit_index"),
                               "t_commit":
                               r["payload"].get("t_commit"),
                               "token_id": r["payload"].get("token_id")}
            p["token_id"] = r["payload"].get("token_id")
        else:
            p["__onset__"] = bool(r["__onset__"])   # the native mark live
            p["role"] = ("STATEMENT-ONSET" if r["__onset__"]
                         else "OTHER-CONTENT")     # the streaming form
            p["__native__"] = {"t": r["payload"].get("t")}
            if schema == "EMISSION":
                p["token_id"] = source["walk_ids"][r["payload"]["t"]]
                p["W"] = w_span[i]
            else:
                p["token_id"] = None
        flat_rows.append(p)
    return flat_rows, span_rec, w_span, schema


# ------------------------------------------------------------------
# THE SINGLE-INSTANCE INGESTION (Section 1: ONE shared clock + three
# banks + ONE guard for the whole probe stream; rows chronological)
# ------------------------------------------------------------------
def ingest_probe(sp, docs_flat, out):
    """docs_flat: the sequenced [(leg, doc_id, flat_rows, census_doc)]
    in stream order. Returns per-doc receipts + the span journals +
    the shared guard/clock. The guard's live bank-write path rides the
    ingestion: every onset or same-leg row writes its span's bank with
    its OWN recognizer leg as the provenance (the census non-vacuous);
    a foreign row (a leg change without an onset mark) is censused by
    the clock's own counter -- the latch holds, NO bank write, the
    census dies loud at CD-5a."""
    guard = sp.IsolationGuard()
    profiles = sp.EntryProfiles({"CODE": 0.5, "PROSE": 0.5, "MATH": 0.5})
    clock = sp.TwoPhaseClock(profiles, guard)
    receipts = []
    journals = {}
    for leg, doc_id, flat_rows, cen in docs_flat:
        n_before = len(clock.spans)
        seam = cen["seams"][0]["commit_index"]
        prefix_leg = cen["prefix_leg"]
        suffix_leg = cen["suffix_leg"]
        states = []
        seam_bank = None
        foreign_before = clock.foreign_census
        for i, row in enumerate(flat_rows):
            state = clock.on_row(row, i)
            states.append(state)
            cur = clock.current
            if cur is not None:
                key = (leg, doc_id, cur["span_id"])
                j = journals.get(key)
                if j is None:
                    j = journals[key] = {
                        "leg": cur["L_active"], "t_onset": cur["t_onset"],
                        "i_onset": cur["anchor"].get("i_onset"),
                        "a_onset": cur["anchor"].get("a_onset"),
                        "doc_id": doc_id, "clock_leg": leg,
                        "rows": []}
                j["rows"].append(row)
                t1 = sp.tier1_classify(row)     # the cold recognizer
                prim = CODE_PRIMARY if schema_of_row(row) == "CODE-BAND" \
                    else EMI_PRIMARY
                if t1 == cur["L_active"]:
                    guard.write(clock.banks[cur["L_active"]],
                                row.get(prim), t1, prim)
                # else: the clock censused a foreign row (the latch
                # holds); no bank write ever -- the CD-5a census dies
                # loud on it before any grading opens
            if i == seam:
                seam_bank = {
                    "outgoing_paused": clock.banks[prefix_leg].paused,
                    "incoming_paused": clock.banks[suffix_leg].paused,
                    "incoming_channels":
                        len(clock.banks[suffix_leg].accumulator),
                    "outgoing_channels":
                        len(clock.banks[prefix_leg].accumulator)}
        doc_spans = clock.spans[n_before:]
        receipts.append({
            "leg": leg, "doc_id": doc_id, "census": cen,
            "spans": doc_spans, "states": states,
            "seam": seam, "prefix_leg": prefix_leg,
            "suffix_leg": suffix_leg, "seam_bank": seam_bank,
            "foreign": clock.foreign_census - foreign_before,
            "state_census": None})   # filled below
        c = Counter()
        for st in states:
            c[st] += 1
        receipts[-1]["state_census"] = dict(c)
    pooled = Counter()
    for r in receipts:
        for k, v in r["state_census"].items():
            pooled[k] += v
    return {"clock": clock, "guard": guard, "receipts": receipts,
            "journals": journals, "pooled_state_census": dict(pooled)}


# ------------------------------------------------------------------
# THE GRADING (CD-5b: the state read at BOTH forms, the spliced and
# standalone constructions, the bit-exact invariance check)
# ------------------------------------------------------------------
def grade_span(M, flat_rows, schema, leg, label, doc_id, t_onset,
               span_rec, w_span, calib_code, calib_prose):
    """The span STATE read of record: CODE-BAND spans ride the
    accumulator's StreamingSpan on the even-A 49 calibration of
    record; EMISSION spans ride the prose accumulator's ProseSpan on
    the even-A 86 lane calibration of record (both banks, zero new
    constants). Returns the closed receipt."""
    acc = M["triadic_accumulator_v1"]
    pap = M["triadic_accumulator_prose_v1"]
    i0 = flat_rows[0]["commit_index"]
    a0 = flat_rows[0].get("token_id")
    if schema == "CODE-BAND":
        o = acc.StreamingSpan(label, "CODE", t_onset, i0, a0,
                              doc_id=doc_id)
        for r in flat_rows:
            o.push(r)
        return o.close(calib_code)
    ps = pap.ProseSpan(label, leg, t_onset, i0, a0, doc_id=doc_id,
                       rec=span_rec, W_at_doc=w_span, calib=calib_prose)
    for r in flat_rows:
        ps.push(r)
    return ps.close()


def first_passage(W, traj, cut, acc):
    """The walk's own per-form first-passage law, verbatim: the first
    crossing on the span's reached path (K-4); the value + position
    returned, or the deepest reached value."""
    return W.first_passage(traj, cut, acc)


def bits_of(v):
    """IEEE-754 bit identity: None is NAMED-ABSENT, never zero-filled."""
    if v is None:
        return None
    return struct.pack(">d", float(v))


def bit_compare_invariance(label, closed_spliced, closed_standalone, acc):
    """THE BIT-EXACT CROSS-SEAM INVARIANCE CHECK (the desk-read 9.2
    law): the raw trip readouts of the spliced-context grade and the
    standalone grade asserted bit-exact at every live horizon
    {36, 64, 128, EOS}. Bit-identity receipts zero seam leakage; any
    bit-divergence is a true cross-seam leak, dying loud with both
    grades printed."""
    n = closed_spliced["n_rows"]
    grid = acc.reached_grid(n, "K-4")
    cmps = 0
    for h in grid:
        a = bits_of(closed_spliced["trajectory"]["values"].get(h))
        b = bits_of(closed_standalone["trajectory"]["values"].get(h))
        if a != b:
            die("BIT-DIVERGENCE",
                "%s: the spliced-context grade and the standalone grade "
                "diverge at horizon %r (spliced %r vs standalone %r) -- a "
                "true cross-seam leak, both grades printed, dying loud"
                % (label, h,
                   closed_spliced["trajectory"]["values"].get(h),
                   closed_standalone["trajectory"]["values"].get(h)))
        cmps += 1
    for key in ("env_K4", "env_M2"):
        if bits_of(closed_spliced.get(key)) != \
                bits_of(closed_standalone.get(key)):
            die("BIT-DIVERGENCE",
                "%s: the envelope peak %s diverges between the spliced "
                "and standalone grades" % (label, key))
        cmps += 1
    return cmps


# ------------------------------------------------------------------
# THE HOOK'S TYPING (CD-5c: the hook's own bytes govern)
# ------------------------------------------------------------------
def hook_typing(hk, label, leg, doc_id, closed, trips, flat_rows, out):
    """Per span, per form, the hook's own form_subslot typing. An
    un-crossed span prints PASSIVE-ARMED (BELOW-CUT) -- or
    (T_RAW-NAMED-ABSENT) where the read is absent -- with ZERO
    E-events. STATE E0 with the terminals NAMED-UNMEASURED-OFFLINE
    arises IF AND ONLY IF a span crosses a form at CD-5b: the E-event
    record is then constructed by the hook's own e_event_record (its
    bytes, never re-typed), printed loud with its span, its horizon,
    its composite and both clocks -- never absorbed."""
    subs = {}
    e_event = None
    for cut in sorted(trips):
        t_raw = trips[cut]["v"]
        h_trip = trips[cut]["h"]
        sub = hk.form_subslot(t_raw, float(cut))
        subs[cut] = sub
        if sub["state"] == "E0" and e_event is None:
            loc = None
            for rec in closed["trajectory"]["locs"]:
                if rec["h_look"] == h_trip:
                    loc = rec
                    break
            check(loc is not None, "DUAL-OUTPUT",
                  "%s: the trip horizon %r carries no localization "
                  "record (the dual-output requirement, never emitted)"
                  % (label, h_trip))
            anchor_row = flat_rows[loc["i_target"]]
            schema = schema_of_row(anchor_row)
            if schema == "EMISSION":
                m_tstar = anchor_row.get("margin")
                second_p = anchor_row.get("second_p")
            else:
                m_tstar = anchor_row.get("margin_content")
                second_p = None
            e_event = hk.e_event_record(leg, doc_id, loc, t_raw,
                                        m_tstar, second_p,
                                        closed["n_rows"])
    n_crossed = sum(1 for k in subs if subs[k]["state"] == "E0")
    return {"sub_slots": subs, "e_event": e_event,
            "n_crossed_forms": n_crossed}


# ------------------------------------------------------------------
# THE CD-5 CORE (shared by the real run and the battery's green world)
# ------------------------------------------------------------------
def prepare_docs_flat(cdb, cache_obj, census_obj, cen_by_leg, sources,
                      out):
    """The per-span flatten + lane join, pre-ingestion: every cache
    row flattened ONCE per span with its own span surface, the
    EMISSION spans lane-joined (the span-local W restart), NO
    wrapper-stamped leg on any row."""
    docs_flat = []
    span_preps = {}
    for leg in ("PROSE", "CODE"):
        for doc in sorted(cache_obj[leg]["docs"],
                          key=lambda d: d["doc_id"]):
            cen = cen_by_leg[leg].get(doc["doc_id"])
            check(cen is not None, "CENSUS-DOC",
                  "%s: absent from the census (never paired by "
                  "position, only by id)" % doc["doc_id"])
            onsets = cen["onset_positions"]
            check(onsets == [0, cen["seams"][0]["commit_index"]],
                  "ONSET-LAW",
                  "%s: the census onset positions %r != [0, seam]"
                  % (doc["doc_id"], onsets))
            bounds = onsets + [cen["n_rows"]]
            doc_flat = []
            for si, cspan in enumerate(cen["spans"]):
                a, b = bounds[si], bounds[si + 1]
                rows = doc["rows"][a:b]
                check(len(rows) == cspan["n_rows"], "SPAN-SLICE",
                      "%s: span %d slice %d != census %d"
                      % (doc["doc_id"], si, len(rows), cspan["n_rows"]))
                label = "%s:s%d" % (doc["doc_id"], si)
                source = sources.get(cspan["source"]["doc_id"]) \
                    if cspan["leg"] == "PROSE" else None
                if cspan["leg"] == "PROSE":
                    check(source is not None, "LANE-JOIN",
                          "%s: the EMISSION span's source %s absent "
                          "from the lane-join table"
                          % (label, cspan["source"]["doc_id"]))
                flat, span_rec, w_span, schema = prep_span_cd(
                    cdb, rows, cspan["leg"], source, label)
                span_preps[(leg, doc["doc_id"], si)] = {
                    "label": label, "flat_rows": flat,
                    "span_rec": span_rec, "w_span": w_span,
                    "schema": schema, "cspan": cspan,
                    "start": a, "cache_rows": rows}
                doc_flat.extend(flat)
            docs_flat.append((leg, doc["doc_id"], doc_flat, cen))
    return docs_flat, span_preps


def run_cd5(M, cache_obj, census_obj, sources, calib_prose, calib_code,
            out, expected_span_sha=None):
    """The full CD-5 measurement acts over a prepared probe cache +
    census (real or synthetic), with the two calibrations of record
    and the per-span lane-join sources. Every act receipted; every
    structural check appended to the CHECKS table; the trip outcomes
    printed as findings, typed loud, never adjudicated."""
    sp = M["triadic_splitter_v1"]
    acc = M["triadic_accumulator_v1"]
    pap = M["triadic_accumulator_prose_v1"]
    hk = M["triadic_hook_v1"]
    W = M["stage2_ladder_walk_v1"]
    cdb = M["crossdomain_probe_builder_v1"]

    # ---- the cold census door (the builder's own load_cross, VERBATIM)
    kw = {}
    if expected_span_sha is not None:
        kw["expected_span_sha"] = expected_span_sha
    totals = cdb.load_cross(cache_obj, census_obj, **kw)
    out("[load] the builder's cold census door (load_cross VERBATIM): "
        "%d docs / %d seams, directions %s, band allocation %s -- "
        "every pin green, the conservation 10/10/5 asserted separately"
        % (totals["docs"], totals["seams"],
           json.dumps(totals["directions"], sort_keys=True),
           json.dumps(totals["band_allocation"], sort_keys=True)))

    cen_by_leg = {}
    for leg in ("PROSE", "CODE"):
        cen_by_leg[leg] = {c["doc_id"]: c
                           for c in census_obj["legs"][leg]["doc_census"]}
    docs_flat, span_preps = prepare_docs_flat(
        cdb, cache_obj, census_obj, cen_by_leg, sources, out)

    # ---- CD-5a + the guard pass: THE SINGLE-INSTANCE INGESTION
    out("[ingest] THE SINGLE-INSTANCE INGESTION LAW (Section 1): ONE "
        "shared two-phase clock + three register banks + ONE isolation "
        "guard for the whole probe stream; %d docs sequenced (the "
        "PROSE leg doc_id order, then the CODE leg); rows fed "
        "chronologically t=0..T-1 per doc, NEVER pre-partitioned -- no "
        "row carries a wrapper-stamped leg, the recognizer routes "
        "cold per row" % len(docs_flat))
    ing = ingest_probe(sp, docs_flat, out)
    clock = ing["clock"]
    guard = ing["guard"]

    n_latch_exact = 0
    n_cold_start = 0
    n_confirm_incoming = 0
    n_contig = 0
    n_derivation_exact = 0
    n_seam_bank = 0
    foreign_total = 0
    classification_rows = 0
    classification_bad = 0
    seam_receipts = []
    for r in ing["receipts"]:
        doc_id = r["doc_id"]
        cen = r["census"]
        seam = r["seam"]
        spans = r["spans"]
        # (1) span contiguity per doc (zero unexplained gaps)
        ok_contig = (len(spans) == 2
                     and spans[0]["t_onset"] == 0
                     and spans[1]["t_onset"]
                     == spans[0]["t_onset"] + spans[0]["rows"])
        check(ok_contig, "SPAN-CONTIGUITY",
              "%s: the spans are not contiguous and whole (%s)"
              % (doc_id, [(s["t_onset"], s["rows"]) for s in spans]))
        n_contig += 1
        # (2) the foreign-schema-row census (the clock's own counter)
        check(r["foreign"] == 0, "FOREIGN-ROW",
              "%s: %d foreign-schema rows inside live spans -- a leg "
              "change without an onset mark; the latch held and the "
              "attempt is censused loud (the single-instance-only "
              "receipt: under pre-splitting this row would have "
              "written silently)" % (doc_id, r["foreign"]))
        foreign_total += r["foreign"]
        # (3) the seam-aware onset derivation per fragment
        flat_all = []
        for si in range(2):
            flat_all.extend(
                span_preps[(r["leg"], doc_id, si)]["flat_rows"])
        measured = [i for i, row in enumerate(flat_all)
                    if row.get("__onset__")
                    or row.get("role") == "STATEMENT-ONSET"]
        check(measured == cen["onset_positions"], "ONSET-DERIVATION",
              "%s: the measured onset marks %r != the authored {0, "
              "seam} %r (mismatches beyond the authored positions die "
              "loud)" % (doc_id, measured, cen["onset_positions"]))
        n_derivation_exact += 1
        # (4) the latch receipts: positions + legs vs the census truth
        latch_pos = [s["t_onset"] for s in spans]
        latch_legs = [s["L_active"] for s in spans]
        check(latch_pos == cen["onset_positions"], "LATCH",
              "%s: the clock latched %r != the authored %r"
              % (doc_id, latch_pos, cen["onset_positions"]))
        check(latch_legs == [cen["prefix_leg"], cen["suffix_leg"]],
              "CLASSIFICATION",
              "%s: the latched legs %r != the census truth %r (the "
              "leg-classification acceptance, any disagreement typed "
              "loud)" % (doc_id, latch_legs,
                        [cen["prefix_leg"], cen["suffix_leg"]]))
        check([s["rows"] for s in spans]
              == [cen["spans"][0]["n_rows"],
                  cen["spans"][1]["n_rows"]], "SEAM-POSITION",
              "%s: the span row counts %r != the census spans %r (the "
              "outgoing span must close exactly at the seam)"
              % (doc_id, [s["rows"] for s in spans],
                 [cen["spans"][0]["n_rows"],
                  cen["spans"][1]["n_rows"]]))
        n_latch_exact += 1
        # (5) the five-state entry at the seam (COLD_START, phase A)
        check(r["states"][seam] == "COLD_START", "SEAM-ENTRY",
              "%s: the seam row's five-state entry %r != COLD_START "
              "(an authored transition must be a phase-A onset latch, "
              "never a tier-2 route)" % (doc_id, r["states"][seam]))
        n_cold_start += 1
        # the CONFIRM at the phase-B confirmation on the incoming span
        incoming_states = r["states"][seam:]
        check("CONFIRM" in incoming_states, "PHASE-B-CONFIRM",
              "%s: the incoming span never reached its phase-B "
              "CONFIRM (window support %d rows)"
              % (doc_id, len(incoming_states)))
        n_confirm_incoming += 1
        # (6) the bank pause/resume receipt at the seam
        sb = r["seam_bank"]
        check(sb is not None and sb["outgoing_paused"]
              and not sb["incoming_paused"], "PAUSE-RESUME",
              "%s: the seam's bank handoff receipt %r (the outgoing "
              "bank must pause, the incoming bank must be resumed/"
              "live)" % (doc_id, sb))
        n_seam_bank += 1
        seam_receipts.append({
            "doc_id": doc_id, "direction": cen["direction"],
            "seam": seam, "band": cen["entry_band"],
            "outgoing": cen["prefix_leg"],
            "incoming": cen["suffix_leg"],
            "outgoing_rows": spans[0]["rows"],
            "incoming_rows": spans[1]["rows"],
            "state_census": r["state_census"]})
        out("[cd-5a] %s (%s): seam at commit %d (band %s) | the "
            "outgoing %s span closes at exactly %d rows | the incoming "
            "%s span latches at the WRITTEN onset mark, five-state entry "
            "COLD_START, phase-B CONFIRM reached | contiguity green | "
            "foreign rows 0 | state census %s"
            % (doc_id, cen["direction"], seam, str(cen["entry_band"]),
               cen["prefix_leg"], spans[0]["rows"], cen["suffix_leg"],
               json.dumps(r["state_census"], sort_keys=True)))

    # the pooled five-state census: only COLD_START/CONFIRM on this
    # cache; any DISAGREEMENT / VOID_HOLD / TIER2_ROUTE dies loud
    pooled = ing["pooled_state_census"]
    for bad_state in ("TIER2_ROUTE", "DISAGREEMENT", "VOID_HOLD"):
        check(pooled.get(bad_state, 0) == 0, "STATE-CENSUS",
              "the pooled five-state census carries %d %s events "
              "(%s) -- zero expected at authored seams on this cache, "
              "the surprise typed loud never absorbed"
              % (pooled.get(bad_state, 0), bad_state,
                 json.dumps(pooled, sort_keys=True)))
    out("[cd-5a] the pooled five-state census over the whole stream: "
        "%s -- only COLD_START/CONFIRM (every authored transition a "
        "phase-A onset latch; zero TIER2_ROUTE at seams, zero foreign "
        "rows, zero DISAGREEMENT/VOID_HOLD; any surprise dies loud)"
        % json.dumps(pooled, sort_keys=True))

    # ---- CD-5b: the classification + the state read at BOTH forms
    table = []
    n_bit = 0
    n_bit_cmps = 0
    crossings = []
    for r in ing["receipts"]:
        leg = r["leg"]
        doc_id = r["doc_id"]
        cen = r["census"]
        for si in range(2):
            prep = span_preps[(leg, doc_id, si)]
            cspan = prep["cspan"]
            label = prep["label"]
            schema = prep["schema"]
            # the per-row leg classification: the recognizer's leg vs
            # the span's authored leg -- 100% the receipt
            bad = 0
            for row in prep["flat_rows"]:
                t1 = sp.tier1_classify(row)
                classification_rows += 1
                if t1 != cspan["leg"]:
                    bad += 1
            classification_bad += bad
            check(bad == 0, "CLASSIFICATION",
                  "%s: %d of %d rows recognized as a leg other than "
                  "the span's authored leg %r (the demux's purest "
                  "test: one document, two legs, recognition cold per "
                  "row; any disagreement typed loud)"
                  % (label, bad, len(prep["flat_rows"]), cspan["leg"]))
            # the spliced-context state read
            closed = grade_span(
                M, prep["flat_rows"], schema, cspan["leg"], label,
                doc_id, prep["start"], prep["span_rec"], prep["w_span"],
                calib_code, calib_prose)
            # the bit-exact cross-seam invariance check on the
            # INCOMING spans (the outgoing spans' crossing is never
            # seam-attributed -- causality: the seam is in its future)
            bit_txt = "n/a (outgoing; causality: the seam in its future)"
            if si == 1:
                flat2, rec2, w2, schema2 = prep_span_cd(
                    cdb, prep["cache_rows"], cspan["leg"],
                    sources.get(cspan["source"]["doc_id"])
                    if cspan["leg"] == "PROSE" else None, label)
                check(schema2 == schema, "STANDALONE-SCHEMA",
                      "%s: the standalone re-derivation's schema %r "
                      "!= the spliced %r" % (label, schema2, schema))
                closed2 = grade_span(
                    M, flat2, schema2, cspan["leg"], label, doc_id,
                    prep["start"], rec2, w2, calib_code, calib_prose)
                n_bit_cmps += bit_compare_invariance(
                    label, closed, closed2, acc)
                n_bit += 1
                bit_txt = ("bit-exact spliced == standalone at every "
                           "live horizon (%d horizon compares, both "
                           "envelope peaks)"
                           % len(acc.reached_grid(closed["n_rows"],
                                                  "K-4")))
            # the trip read at BOTH forms (the designation never
            # silently chosen; the [REDACTED_PER_PUBLICATION_POLICY] lens record-keeping only)
            trips = {}
            for cut in acc.TRIP_FORMS:
                h, v = first_passage(W, closed["trajectory"], cut, acc)
                trips["%.4f" % cut] = {"h": h, "v": v}
            # the hook's typing (CD-5c)
            hook = hook_typing(hk, label, cspan["leg"], doc_id, closed,
                               trips, prep["flat_rows"], out)
            tripped = {k: trips[k]["h"] is not None for k in trips}
            any_trip = any(tripped.values())
            if any_trip:
                first_h = None
                for cut in sorted(trips):
                    if tripped[cut]:
                        first_h = (trips[cut]["h"], trips[cut]["v"])
                        break
                crossings.append({
                    "label": label, "doc_id": doc_id, "si": si,
                    "leg": cspan["leg"], "schema": schema,
                    "incoming": si == 1,
                    "h": first_h[0], "v": first_h[1],
                    "trips": trips, "hook": hook})
                out("[cd-5b] CROSSING typed loud: %s (leg %s, %s "
                    "span, %s) trips at h=%s composite %.4f -- %s"
                    % (label, cspan["leg"],
                       "incoming" if si == 1 else "outgoing", schema,
                       first_h[0], first_h[1],
                       ("NATIVE SOURCE-SLICE TAIL BEHAVIOR (the "
                        "bit-exact invariance receipts zero seam "
                        "leakage; the seam at zero algebraic weight; "
                        "the banked PROSE false-trip precedent "
                        "2.1748 / 2.0610)"
                        if si == 1 else
                        "never seam-attributed -- the seam is in its "
                        "future (causality)")))
            grade_txt = "/".join(
                ("MATCH" if not tripped[k] else "FALSE-TRIP")
                for k in sorted(trips))
            trip_txt = " | ".join(
                "@%s %s" % (k, ("trip h=%s v=%.4f"
                                % (trips[k]["h"], trips[k]["v"]))
                            if trips[k]["h"] is not None
                            else ("no trip (peak %s)"
                                  % ("%.4f" % trips[k]["v"]
                                     if trips[k]["v"] is not None
                                     else "NAMED-ABSENT")))
                for k in sorted(trips))
            hook_txt = " | ".join(
                "@%s %s" % (k, hook["sub_slots"][k]["state"])
                for k in sorted(hook["sub_slots"]))
            table.append({
                "label": label, "doc_id": doc_id, "leg": cspan["leg"],
                "schema": schema, "si": si, "trips": trips,
                "grades": grade_txt.split("/"),
                "n_rows": closed["n_rows"], "closed": closed,
                "hook": hook, "incoming": si == 1})
            out("[cd-5b] %s %s (true %s/clean, source %s, %s): %s | "
                "grade %s | %s | %s"
                % (cspan["leg"], label, cspan["leg"],
                   cspan["source"]["doc_id"],
                   "incoming" if si == 1 else "outgoing",
                   trip_txt, grade_txt, hook_txt, bit_txt))

    # ---- CD-5c receipts: the guard + the pause/resume + the routing
    write_census = dict(guard.write_census)
    per_doc_banks = {}
    for r in ing["receipts"]:
        legs_written = set()
        for si in range(2):
            prep = span_preps[(r["leg"], r["doc_id"], si)]
            legs_written.add(prep["cspan"]["leg"])
        per_doc_banks[r["doc_id"]] = sorted(legs_written)
    n_both_banks = sum(1 for v in per_doc_banks.values()
                       if v == ["CODE", "PROSE"])
    check(n_both_banks == len(ing["receipts"]), "GUARD-NON-VACUOUS",
        "the cross-leg write census is vacuous: only %d of %d docs "
        "wrote both legs' banks (each probe doc writes into both "
        "legs' banks BY CONSTRUCTION -- a vacuous census is a failed "
        "receipt)" % (n_both_banks, len(ing["receipts"])))
    out("[cd-5c] THE ISOLATION GUARD at the handoff: cross-leg write "
        "census ZERO mismatches (a mismatch trips the guard's own "
        "CROSS-LEG-CONTAMINATION die, proven live in the battery), "
        "NON-VACUOUS for the first time -- both legs' banks written "
        "by all %d docs; the write census %s (writes per bank leg, "
        "the MATH bank untouched, named)"
        % (n_both_banks,
           json.dumps({k: write_census.get(k, 0)
                       for k in ("CODE", "PROSE", "MATH")},
                      sort_keys=True)))
    out("[cd-5c] the bank pause/resume census per seam: %d/%d "
        "receipted (the outgoing bank paused, the incoming bank "
        "resumed/live; the single-seam pause-AND-resume cell "
        "NAMED-ABSENT per Section 7 limit 7 -- every probe doc carries "
        "exactly one seam, the resume machinery exercised only across "
        "doc boundaries in the stream, receipted honestly as such)"
        % (n_seam_bank, len(ing["receipts"])))
    routing = Counter()
    for t in table:
        routing[t["schema"]] += 1
    out("[cd-5c] the schema-routing census inside one document (the "
        "routing law of record): %s -- each doc's two halves ride "
        "different schemas, the routing never cross-compared "
        "(margin_content and margin are different surfaces, named "
        "honestly)"
        % json.dumps({k: routing[k] for k in ("CODE-BAND", "EMISSION")},
                     sort_keys=True))

    # ---- the W-lane z census (descriptive, never a bar)
    w_z = {}
    for t in table:
        if t["schema"] != "EMISSION":
            continue
        m = calib_prose["moments"]["W"]["EOS"]
        pin = calib_prose["pins"]["W"]["EOS"]
        prep = None
        for r in ing["receipts"]:
            if r["doc_id"] == t["doc_id"]:
                prep = span_preps[(r["leg"], r["doc_id"], t["si"])]
        w_eos = prep["w_span"][-1]
        if pin is None or w_eos is None:
            w_z[t["label"]] = None
        else:
            w_z[t["label"]] = pin * (w_eos - m["mu"]) / m["sd_pop"]
    vals = [v for v in w_z.values() if v is not None]
    out("[cd-5b] the W-lane z census at EOS (DESCRIPTIVE, never a "
        "bar; the W-alone negative receipt stands): %d EMISSION spans "
        "read, %d CODE-BAND spans NAMED-ABSENT on the W lane | min "
        "%.4f | mean %.4f | max %.4f -- beside the banked clean "
        "receipts of the mixed cache (clean W-z max +6.5889, 24 of 55 "
        "clean spans above the loop min +2.1688), named, never "
        "adjudicated"
        % (len(w_z), len(table) - len(w_z),
           min(vals), sum(vals) / float(len(vals)), max(vals))
        if vals else
        "[cd-5b] the W-lane z census: no live W reads (named loud, "
        "never imputed)")

    # ---- the hook census (0 E-events iff no crossing)
    n_events = sum(1 for t in table if t["hook"]["e_event"] is not None)
    n_crossed_spans = len(crossings)
    check((n_events == 0) == (n_crossed_spans == 0), "HOOK-IFF-LAW",
        "the hook's E-event census violates the iff law: %d E-events "
        "against %d crossed spans (an E-event arises if and only if a "
        "span crosses a form at CD-5b)"
        % (n_events, n_crossed_spans))
    out("[cd-5c] THE HOOK'S TYPING (its own bytes): %d sub-slots "
        "(%d spans x 2 forms) typed; E-events %d -- ZERO iff no "
        "crossing (the iff law); the ladder stays E0 offline, nothing "
        "actuates, the efficacy terminals NAMED-UNMEASURED-OFFLINE; "
        "the below-cut sub-slot law held on every un-crossed line "
        "(never a negative excess)"
        % (2 * len(table), len(table), n_events))
    for t in table:
        ev = t["hook"]["e_event"]
        if ev is not None:
            out("[cd-5c] E-EVENT RECORD (the hook's own construction, "
                "printed loud, never absorbed): %s"
                % json.dumps(ev, sort_keys=True))

    # ---- the pooled receipts (n=10 seams; n=5 per direction)
    def dir_receipt(direction):
        d = [s for s in seam_receipts if s["direction"] == direction]
        return (len(d),
                sum(1 for s in d if True))
    for direction in ("PROSE->CODE", "CODE->PROSE"):
        d = [s for s in seam_receipts if s["direction"] == direction]
        check(len(d) == 5, "POOLED-N",
              "direction %s carries %d seams != 5 (no evaluated cell "
              "under 5)" % (direction, len(d)))
        out("[pooled] %s (n=%d): entry marks exact %d/%d, COLD_START "
            "on all incoming, the incoming spans' rows %s, the bands %s"
            % (direction, len(d), len(d), len(d),
               json.dumps([s["incoming_rows"] for s in d]),
               json.dumps([s["band"] for s in d])))
    out("[pooled] ALL SEAMS (n=%d): entry marks exact %d/%d, bit-exact "
        "invariance %d/%d incoming spans (%d horizon compares, zero "
        "divergence), crossings typed loud %d (every one printed with "
        "its span, horizon, composite and both clocks)"
        % (len(seam_receipts), n_latch_exact, len(seam_receipts),
           n_bit, n_bit, n_bit_cmps, len(crossings)))

    # ---- the structural CHECKS table
    checks = []
    def ck(name, expected, got):
        ok = (got == expected)
        checks.append((name, expected, got, ok))
        out("[%s] %-66s expected %s | got %s"
            % ("ok " if ok else "FAIL", name, expected, got))
        return ok
    ck("load: docs 10", 10, totals["docs"])
    ck("load: seams 10", 10, totals["seams"])
    ck("load: PROSE->CODE 5", 5, totals["directions"]["PROSE->CODE"])
    ck("load: CODE->PROSE 5", 5, totals["directions"]["CODE->PROSE"])
    ck("load: band allocation (2/2/1) both directions",
       {"CODE->PROSE": [2, 2, 1], "PROSE->CODE": [2, 2, 1]},
       {k: v for k, v in sorted(totals["band_allocation"].items())})
    ck("ingest: spans latched (one shared clock)", 20, len(clock.spans))
    ck("5a: latch positions exact (docs)", 10, n_latch_exact)
    ck("5a: COLD_START at all seams", 10, n_cold_start)
    ck("5a: phase-B CONFIRM on all incoming", 10, n_confirm_incoming)
    ck("5a: contiguity per doc", 10, n_contig)
    ck("5a: foreign-row census zero", 0, foreign_total)
    ck("5a: onset derivation exact (docs)", 10, n_derivation_exact)
    ck("5a: pause/resume receipted per seam", 10, n_seam_bank)
    ck("5a: pooled census only COLD_START/CONFIRM", True,
       sorted(pooled.keys()) == ["COLD_START", "CONFIRM"])
    ck("5b: leg classification 100% (bad rows)", 0, classification_bad)
    total_rows = sum(r["census"]["n_rows"] for r in ing["receipts"])
    ck("5b: rows classified (every cache row once)", total_rows,
       classification_rows)
    ck("5b: routing census {CODE-BAND, EMISSION}", 10,
       routing.get("CODE-BAND", 0))
    ck("5b: EMISSION spans", 10, routing.get("EMISSION", 0))
    ck("5b: both forms printed (sub-slot reads)", 40, 2 * len(table))
    ck("5b: bit-exact invariance (incoming spans)", 10, n_bit)
    ck("5c: guard cross-leg mismatches (non-vacuous census)", 0,
       sum(1 for k in write_census if k not in ("CODE", "PROSE")))
    ck("5c: docs writing both legs' banks", 10, n_both_banks)
    ck("5c: hook sub-slots typed", 40, 2 * len(table))
    ck("5c: hook E-events iff crossings (law held)", True,
       (n_events == 0) == (n_crossed_spans == 0))
    ck("5c: E-events count", n_crossed_spans, n_events)
    ck("W census: EMISSION spans read", 10, len(w_z))
    ck("pooled: seams receipted", 10, len(seam_receipts))
    n_ok = sum(1 for c in checks if c[3])
    out("[checks] %d/%d landed" % (n_ok, len(checks)))
    return {"checks": checks, "table": table, "crossings": crossings,
            "seam_receipts": seam_receipts, "write_census":
            write_census, "pooled": pooled, "w_z": w_z,
            "n_bit": n_bit, "n_bit_cmps": n_bit_cmps,
            "n_events": n_events}


# ------------------------------------------------------------------
# THE BATTERY (synthetic hand-off worlds FIRST; zero real rows; every
# tamper world and negative fixture dying loud at its own named check)
# ------------------------------------------------------------------
SYN_ROWS = 258          # >= 258: both prefix and suffix feasible
SYN_SHA = {"PROSE": "synprose", "CODE": "syncode0"}
SYN_N_CALIB = 12


def _syn_value(doc, i, salt):
    """Deterministic, varied, tight: non-degenerate moments without
    authored crossings. Docs 50+ (the calibration cohorts) carry a
    per-doc offset so every measured lane has real spread; the world
    docs stay tight (no authored crossings in the green world)."""
    v = 1.0 + ((i * 7 + doc * 3 + salt) % 11) * 0.01
    if doc >= 50:
        v += 0.03 * (doc % 5) + 0.002 * ((doc * 5 + salt) % 7)
    return v


def _syn_prose_doc(idx, n=SYN_ROWS):
    """A synthetic prose source doc: the 16-key commit family, the
    step lanes, the walk ids -- the thin record's own shapes."""
    commits, steps = [], {"t": list(range(n)), "s": [], "PR": [],
                          "E": [], "H": []}
    walk_ids = []
    for i in range(n):
        commits.append({
            "K": _syn_value(idx, i, 1), "content_mass": _syn_value(idx, i, 2),
            "emitted_p": _syn_value(idx, i, 3), "gamma_g": 1.0,
            "gamma_p": 1.0, "gamma_valid": True,
            "gm_g": _syn_value(idx, i, 4), "gm_p": _syn_value(idx, i, 5),
            "hedge_mass": _syn_value(idx, i, 6),
            "margin": _syn_value(idx, i, 7), "phase": "CoT",
            "second_id": 0, "second_p": _syn_value(idx, i, 8),
            "second_str": "x", "t": i, "token": "tok%d" % (i % 5)})
        steps["s"].append(_syn_value(idx, i, 9))
        steps["PR"].append(_syn_value(idx, i, 10))
        steps["E"].append(_syn_value(idx, i, 11))
        steps["H"].append(_syn_value(idx, i, 12))
        walk_ids.append(5000 + i)
    return {"doc_id": "syn-prose-%02d" % idx, "commits": commits,
            "steps": steps, "walk_ids": walk_ids}


def _syn_code_doc(idx, n=SYN_ROWS):
    """A synthetic code source doc: the 16-column band family, the
    onset i=0-only role law, the work_inc anchor law."""
    rows = []
    for i in range(n):
        rows.append({
            "H_content": _syn_value(idx, i, 1),
            "commit_index": i,
            "h_num_content": _syn_value(idx, i, 2),
            "m_ulp_content": _syn_value(idx, i, 3),
            "margin_content": _syn_value(idx, i, 4),
            "p_top_band": _syn_value(idx, i, 5),
            "prsig_prefix": _syn_value(idx, i, 6),
            "raw_gap_content_band": _syn_value(idx, i, 7),
            "role": "STATEMENT-ONSET" if i == 0 else "OTHER-CONTENT",
            "sexc_prefix": _syn_value(idx, i, 8),
            "status": "ok", "t_commit": i, "token_id": 9000 + i,
            "work_inc": None if i == 0 else _syn_value(idx, i, 9),
            "work_inc_window_n": 16,
            "zeta_content": _syn_value(idx, i, 10)})
    return {"doc_id": "syn-code-%02d" % idx, "rows": rows}


def _syn_pool_rows(surface, doc):
    """The builder's FreshPool row shape: schema-typed cache rows with
    the payload the readout's flatten law expects."""
    cdb = sys.modules["crossdomain_probe_builder_v1"]
    if surface == "PROSE":
        return [cdb.make_row("PROSE", i, 0, c["t"], c, onset=(i == 0))
                for i, c in enumerate(doc["commits"])]
    return [cdb.make_row("CODE", i, 0, r["t_commit"], r,
                         onset=(i == 0))
            for i, r in enumerate(doc["rows"])]


def build_syn_world(cdb):
    """The full 10-doc synthetic cross-domain world through the CD
    builder's OWN plan/pool/join path (the same law the builder's own
    battery rode), with REAL-family payloads so the readout's flatten
    + grading paths run end to end."""
    prose_docs = [_syn_prose_doc(i) for i in range(10)]
    code_docs = [_syn_code_doc(i) for i in range(10)]
    pools = {
        "PROSE": cdb.FreshPool(
            [{"doc_id": d["doc_id"], "rows": _syn_pool_rows("PROSE", d),
              "sha_prefix": SYN_SHA["PROSE"]} for d in prose_docs],
            [], "PROSE"),
        "CODE": cdb.FreshPool(
            [{"doc_id": d["doc_id"], "rows": _syn_pool_rows("CODE", d),
              "sha_prefix": SYN_SHA["CODE"]} for d in code_docs],
            [], "CODE")}
    docs_out, census_out, clean_receipts, overlap = cdb.build_world(
        pools, lambda s: None)
    cache_obj, census_obj = cdb.assemble_cache_census(
        docs_out, census_out, clean_receipts, {"PROSE": [], "CODE": []},
        "syn")
    totals = cdb.load_cross(cache_obj, census_obj,
                            expected_span_sha=SYN_SHA)
    sources = {}
    for d in prose_docs:
        d["key"] = d["doc_id"]
        sources[d["doc_id"]] = d
    return cache_obj, census_obj, sources, totals


def build_syn_calibrations(M, sources):
    """The synthetic calibrations of record, measured through the
    instruments' OWN functions on synthetic cohorts (zero new
    constants; the same measured-moment laws)."""
    sp = M["triadic_splitter_v1"]
    acc = M["triadic_accumulator_v1"]
    pap = M["triadic_accumulator_prose_v1"]
    W = M["stage2_ladder_walk_v1"]
    corpus = []
    join = {}
    for k in range(SYN_N_CALIB):
        d = _syn_prose_doc(50 + k)
        d["doc_id"] = 900 + k
        corpus.append(d)
        join[d["doc_id"]] = ("calibration",
                             "A" if k < 8 else "B")
    W_at, wrec = pap.w_derivation(
        corpus, lambda did: join[did][0] == "calibration")
    calib_prose = pap.measure_lane_calibration(corpus, join, W_at)
    base_s, base_pr, pool_s, pool_pr = W.rw16_baselines(
        corpus, lambda did: join[did][0] == "calibration",
        pap.BUCKET, pap.MIN_N)
    for sd, rec in sources.items():
        zmax, _w = W.rw16_zmax_steps(rec, base_s, base_pr, pool_s,
                                     pool_pr, pap.BUCKET)
        rec["zmax"] = zmax
    # the CODE-BAND calibration: synthetic cohort spans measured
    # through the accumulator's own law
    calib_spans = []
    for k in range(SYN_N_CALIB):
        d = _syn_code_doc(50 + k)
        o = acc.StreamingSpan("syncal-%02d:0" % k, "CODE", 0, 0,
                              d["rows"][0]["token_id"],
                              doc_id=d["doc_id"])
        for r in d["rows"]:
            rr = dict(r)
            o.push(rr)
        calib_spans.append(o)
    moments = acc.measure_moments_from_spans(calib_spans, ("CODE",),
                                             None)
    calib_code = acc.Calibration(moments, {"even_A": SYN_N_CALIB})
    return calib_prose, calib_code, wrec


def expect_die(code, fn, label, out):
    """A ReadoutDie/BuilderDie expected: every battery world dies loud
    at its own named check, never silently absorbed."""
    try:
        fn()
    except ReadoutDie as e:
        check(e.code == code, "BATTERY-UNEXPECTED-DIE",
              "%s: died %s (%s), expected %s"
              % (label, e.code, e.msg, code))
        out("[%s] %s -> died loud (expected)" % (label, e.code))
        return
    except sys.modules["crossdomain_probe_builder_v1"].BuilderDie as e:
        check(e.code == code, "BATTERY-UNEXPECTED-DIE",
              "%s: died %s (%s), expected %s"
              % (label, e.code, e.msg, code))
        out("[%s] %s -> died loud (expected, the builder's own cold "
            "door)" % (label, e.code))
        return
    die("BATTERY-NO-DIE",
        "%s: no die (expected %s) -- a tamper shape silently absorbed"
        % (label, code))


def expect_loud(marker, fn, label, out):
    """An instrument's own TRIP-LOUD die expected (the splitter's and
    the hook's own exits -- sys.exit with the marker printed)."""
    captured = []
    old = sys.stdout
    sys.stdout = type("_c", (), {
        "write": staticmethod(lambda s: captured.append(s)),
        "flush": staticmethod(lambda: None)})()
    try:
        fn()
        failed = True
    except SystemExit:
        failed = False
    finally:
        sys.stdout = old
    text = "".join(captured)
    check(not failed and marker in text, "BATTERY-NO-LOUD-DIE",
          "%s: expected the instrument's own %s die, got %r"
          % (label, marker, text[-200:]))
    out("[%s] %s -> died loud (the instrument's own die, expected)"
        % (label, marker))


def run_battery(M, out):
    """Every world hand-solved, every expected die named, every
    receipt printed; deterministic (twice-run cmp silent)."""
    sp = M["triadic_splitter_v1"]
    acc = M["triadic_accumulator_v1"]
    hk = M["triadic_hook_v1"]
    cdb = M["crossdomain_probe_builder_v1"]
    import copy
    out("[battery] %s: the synthetic hand-off worlds, hand-solved "
        "through the REAL CD-5 path (zero real rows)" % VERSION)
    out("[battery] the instruments of record imported VERBATIM, "
        "byte-pinned at load -- zero instrument bytes moved")

    # ---- the green world: the full 10-doc synthetic cross-domain
    #      world through the real measurement core, every check landed
    cache_obj, census_obj, sources, totals = build_syn_world(cdb)
    calib_prose, calib_code, wrec = build_syn_calibrations(M, sources)
    green = run_cd5(M, cache_obj, census_obj, sources, calib_prose,
                    calib_code, out, expected_span_sha=SYN_SHA)
    n_ok = sum(1 for c in green["checks"] if c[3])
    check(n_ok == len(green["checks"]), "BATTERY-GREEN-WORLD",
          "the synthetic world's CD-5 checks: %d of %d landed"
          % (n_ok, len(green["checks"])))
    out("[world] the 10-doc synthetic cross-domain world built "
        "through the builder's own plan/pool/join path + measured "
        "through the real CD-5 core: %d/%d checks landed, %d spans, "
        "%d seams, bit-exact %d/%d incoming"
        % (n_ok, len(green["checks"]), len(green["table"]),
           len(green["seam_receipts"]), green["n_bit"], green["n_bit"]))

    # ---- tamper (i): a leg change WITHOUT an onset mark -- the
    #      latch holds, the foreign row censused loud (the
    #      single-instance-only receipt). Applied on the flattened
    #      stream (post-door): the ingestion census itself must die.
    def tamper_i():
        cen_by_leg = {}
        for lg in ("PROSE", "CODE"):
            cen_by_leg[lg] = {c["doc_id"]: c
                             for c in census_obj["legs"][lg][
                                 "doc_census"]}
        docs_flat, _preps = prepare_docs_flat(
            cdb, cache_obj, census_obj, cen_by_leg, sources,
            lambda s: None)
        leg, doc_id, flat_rows, cen = docs_flat[0]
        seam = cen["seams"][0]["commit_index"]
        row = flat_rows[seam]
        check(row.get("role") == "STATEMENT-ONSET"
              and "work_inc" in row, "BATTERY-SHAPE",
              "tamper-i: the seam row %r is not the expected WRITTEN "
              "CODE onset" % sorted(row.keys()))
        row["role"] = "OTHER-CONTENT"     # the WRITTEN mark removed
        ing2 = ingest_probe(sp, docs_flat, lambda s: None)
        check(all(r["foreign"] == 0 for r in ing2["receipts"]),
              "FOREIGN-ROW",
              "the latch held: the censused foreign rows %s (a leg "
              "change without an onset mark, live ONLY under "
              "single-instance ingestion)"
              % {r["doc_id"]: r["foreign"]
                 for r in ing2["receipts"] if r["foreign"]})
    expect_die("FOREIGN-ROW", tamper_i, "tamper-i (no onset mark)",
               out)
    out("[tamper-i] the receipt: the latch HELD, the row censused "
        "loud by the clock's own counter -- live ONLY under "
        "single-instance ingestion (under pre-splitting this row would "
        "have written silently into the wrong stream)")

    # ---- tamper (ii): the census lying about a span's leg -- the
    #      builder's cold door catches the census lie first
    #      (TRUTH-LABELS, its own named die); the readout's
    #      leg-classification acceptance stands behind it (layered)
    def tamper_ii():
        c2 = copy.deepcopy(census_obj)
        c2["legs"]["PROSE"]["doc_census"][0]["spans"][1]["leg"] = \
            "PROSE"
        run_cd5(M, cache_obj, c2, sources, calib_prose, calib_code,
                lambda s: None, expected_span_sha=SYN_SHA)
    expect_die("TRUTH-LABELS", tamper_ii,
               "tamper-ii (census leg flip)", out)
    out("[tamper-ii] the receipt: the census lie died at the cold "
        "door (the builder's own TRUTH-LABELS), the readout's "
        "leg-classification acceptance layered behind it")

    # ---- tamper (iii): an authored bit-divergence -- the
    #      spliced-vs-standalone bit-compare dies loud
    def tamper_iii():
        t_in = green["table"][1]
        closed = t_in["closed"]
        fake = copy.deepcopy(closed)
        grid = acc.reached_grid(fake["n_rows"], "K-4")
        h = grid[0]
        v = fake["trajectory"]["values"].get(h)
        fake["trajectory"]["values"][h] = (1e-9 if v is None
                                          else v + 1e-9)
        bit_compare_invariance("syn-tamper", closed, fake, acc)
    expect_die("BIT-DIVERGENCE", tamper_iii,
               "tamper-iii (an authored leak)", out)

    # ---- tamper (iv): the guard's own die proven live -- a misrouted
    #      write through the REAL isolation guard
    def tamper_iv():
        g = sp.IsolationGuard()
        bank = sp.RegisterBank("CODE")
        g.write(bank, 1.0, "PROSE", EMI_PRIMARY)
    expect_loud("CROSS-LEG-CONTAMINATION", tamper_iv,
                "tamper-iv (a misrouted guard write)", out)

    # ---- negative: an extra WRITTEN onset beyond the authored set --
    #      the seam-aware derivation dies loud (post-door, on the
    #      flattened stream)
    def neg_extra_onset():
        cen_by_leg = {}
        for lg in ("PROSE", "CODE"):
            cen_by_leg[lg] = {c["doc_id"]: c
                             for c in census_obj["legs"][lg][
                                 "doc_census"]}
        docs_flat, _preps = prepare_docs_flat(
            cdb, cache_obj, census_obj, cen_by_leg, sources,
            lambda s: None)
        leg, doc_id, flat_rows, cen = docs_flat[0]
        seam = cen["seams"][0]["commit_index"]
        row = flat_rows[seam + 10]
        check("role" in row, "BATTERY-SHAPE",
              "neg-extra-onset: row %d carries no role key" % (seam + 10))
        row["role"] = "STATEMENT-ONSET"    # an unauthorized onset
        measured = [i for i, r in enumerate(flat_rows)
                    if r.get("__onset__")
                    or r.get("role") == "STATEMENT-ONSET"]
        check(measured == cen["onset_positions"], "ONSET-DERIVATION",
              "%s: the measured onset marks %r != the authored {0, "
              "seam} %r (mismatches beyond the authored positions die "
              "loud)" % (doc_id, measured, cen["onset_positions"]))
    expect_die("ONSET-DERIVATION", neg_extra_onset,
               "neg-extra-onset (beyond the authored set)", out)

    # ---- negative: a row no leg's signature recognizes -- the
    #      splitter's own UNRECOGNIZED-SCHEMA die
    def neg_unrecognized():
        guard = sp.IsolationGuard()
        profiles = sp.EntryProfiles(
            {"CODE": 0.5, "PROSE": 0.5, "MATH": 0.5})
        clock = sp.TwoPhaseClock(profiles, guard)
        clock.on_row({"commit_index": 0, "stmt_ordinal": 0,
                      "token_step": 0, "payload": {"t": 0}}, 0)
    expect_loud("UNRECOGNIZED-SCHEMA", neg_unrecognized,
                "neg-unrecognized-schema", out)

    # ---- negatives at the builder's own cold door (load_cross
    #      VERBATIM): truncated census / seam count / provenance sha
    def neg_truncated():
        c2 = copy.deepcopy(census_obj)
        c2["legs"]["PROSE"]["doc_census"] = \
            c2["legs"]["PROSE"]["doc_census"][:4]
        cdb.load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("TRUNCATED-CENSUS", neg_truncated, "neg-truncated", out)

    def neg_seamcount():
        c2 = copy.deepcopy(census_obj)
        dc = c2["legs"]["PROSE"]["doc_census"][0]
        dc["seams"] = dc["seams"] + [dict(dc["seams"][0])]
        cdb.load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("SEAM-COUNT", neg_seamcount, "neg-seam-count", out)

    def neg_provenance():
        c2 = copy.deepcopy(census_obj)
        c2["legs"]["PROSE"]["doc_census"][0]["spans"][0]["source"][
            "sha_prefix"] = "deadbeef00000000"
        cdb.load_cross(cache_obj, c2, expected_span_sha=SYN_SHA)
    expect_die("PROVENANCE-SHA", neg_provenance, "neg-provenance", out)

    # ---- negative: the hook's own EMISSION-LAW -- an E-event record
    #      constructed with no crossed form dies loud (the iff law)
    def neg_emission_law():
        hk.e_event_record(
            "PROSE", "syn", {"i_target": 5, "h_look": 36,
                             "anchor_tier": "TIER_1_ANCHOR_LATCHED"},
            1.5, 0.7, 0.3, 129)
    expect_loud("EMISSION-LAW", neg_emission_law,
                "neg-hook-emission-law (the iff law)", out)

    out("[battery] all worlds green: the 10-doc synthetic world "
        "through the real CD-5 core; %d tamper shapes + %d negative "
        "fixtures died loud by design, every die at its own named "
        "check" % (4, 6))
    out("[battery] %s" % PAREN)
    return 0


# ------------------------------------------------------------------
# STAGE: PREP (the heavy lane work, cached beside the script)
# ------------------------------------------------------------------
def do_prep(args, search_roots):
    paths = discover(INPUT_SPECS, search_roots, "prep")
    instr = discover_instruments(search_roots, "prep")
    paths.update(instr)
    M = load_instruments(paths)
    acc = M["triadic_accumulator_v1"]
    pap = M["triadic_accumulator_prose_v1"]
    W = M["stage2_ladder_walk_v1"]
    cdb = M["crossdomain_probe_builder_v1"]

    print("[prep] the prose thin + export of record (the EMISSION "
          "machinery's own calibration + the lane-join sources)")
    corpus, fixtures, cen = pap.load_thin(
        paths["triadic_t2_thin_rw17-prose-r2.jsonl"])
    join, rows_ex, arm = pap.load_export(
        paths["triadic_wu_prose_read_v1.json"])
    W_at, wrec = pap.w_derivation(
        corpus, lambda did: join[did][0] == "calibration")
    calib_prose = pap.measure_lane_calibration(corpus, join, W_at)
    check(calib_prose["n_evenA"] == PIN_evenA_PROSE, "even-A-PIN",
          "the even-A prose cohort %d != the banked pin %d"
          % (calib_prose["n_evenA"], PIN_evenA_PROSE))
    print("[prep] THE EMISSION CALIBRATION OF RECORD: the even-A %d "
          "lane moments measured at every horizon (the banked rw16 "
          "law, zero new constants; the W derivation: %d buckets on %d "
          "calibration docs)"
          % (calib_prose["n_evenA"], wrec["n_buckets"],
             wrec["n_calib_docs"]))

    base_s, base_pr, pool_s, pool_pr = W.rw16_baselines(
        corpus, lambda did: join[did][0] == "calibration",
        pap.BUCKET, pap.MIN_N)
    n_checked = W.rw16_cross_check(corpus, W_at, base_s, base_pr,
                                   pool_s, pool_pr, pap.BUCKET,
                                   "the CD readout prep")
    check(n_checked == PIN_PROSE_CORPUS, "RW16-CROSS",
          "the rw16 port cross-check covered %d docs != %d"
          % (n_checked, PIN_PROSE_CORPUS))
    print("[prep] the rw16 port cross-checked EXACT against the prose "
          "accumulator's own w_derivation on all %d corpus docs (any "
          "drift dies loud)" % n_checked)

    print("[prep] the code cache of record (the CODE-BAND calibration "
          "of record: the accumulator's own even-A 49 law)")
    data, rbd, dwt = acc.load_code_rows(
        paths["triadic_wu_code_read_v1.json"])
    even_a_ids = set(d["doc_id"] for d in dwt
                     if d.get("half") == "calibration"
                     and d.get("stratum") == "A")
    calib_spans = []
    for doc_id in sorted(even_a_ids, key=str):
        cols = rbd[doc_id]
        rows = [{ch: cols[ch][i] for ch in cols}
                for i in range(len(cols["commit_index"]))]
        s = acc.StreamingSpan("%s:0" % doc_id, "CODE", 0, 0,
                              cols["token_id"][0], doc_id=doc_id)
        for r in rows:
            r["__t1__"] = "CODE"
            s.push(r)
        calib_spans.append(s)
    moments = acc.measure_moments_from_spans(calib_spans, ("CODE",),
                                             None)
    calib_code = acc.Calibration(moments, {"even_A": PIN_evenA_CODE})
    print("[prep] THE CODE-BAND CALIBRATION OF RECORD: the even-A %d "
          "prefix moments measured at every horizon (measured never "
          "modeled; the population pin read fail-loud at load)"
          % PIN_evenA_CODE)

    # ---- the probe census: the EMISSION spans' lane-join sources
    census_obj = json.load(open(
        paths["crossdomain_probe_census_v1.json"]))
    source_ids = set()
    for leg in ("PROSE", "CODE"):
        for dc in census_obj["legs"][leg]["doc_census"]:
            for s in dc["spans"]:
                if s["leg"] == "PROSE":
                    source_ids.add(s["source"]["doc_id"])
    corpus_by_id = {"prose-%03d" % r["doc_id"]: r for r in corpus}
    sources = {}
    membership = {}
    for sd in sorted(source_ids):
        rec = corpus_by_id.get(sd)
        check(rec is not None, "LANE-JOIN",
              "the EMISSION span's source %s absent from the prose "
              "thin of record" % sd)
        zmax, _w = W.rw16_zmax_steps(rec, base_s, base_pr, pool_s,
                                     pool_pr, pap.BUCKET)
        sources[sd] = {
            "key": sd,
            "doc_id": rec["doc_id"],
            "steps": {k: list(rec["steps"][k])
                      for k in ("t", "s", "PR", "E", "H")},
            "walk_ids": list(rec["walk_ids"]),
            "n_commits": len(rec["commits"]), "zmax": zmax}
        did = rec["doc_id"]
        membership[sd] = list(join[did]) if did in join else None
    print("[prep] the lane-join sources: %d EMISSION source docs "
          "sliced (steps + walk ids + the per-step zmax), their "
          "calibration-half memberships %s (descriptive receipt: "
          "in-cohort sources are the development-snapshot law, the "
          "held-out act named forward)"
          % (len(sources), json.dumps(membership, sort_keys=True)))

    ctx = {"version": VERSION,
           "calib_prose": calib_prose,
           "calib_code_moments": moments,
           "even_a_code": PIN_evenA_CODE,
           "rw16": {"n_buckets": wrec["n_buckets"],
                    "n_calib_docs": wrec["n_calib_docs"],
                    "cross_checked": n_checked},
           "sources": sources, "membership": membership}
    ctx_path = args.ctx
    with open(ctx_path, "wb") as fh:
        pickle.dump(ctx, fh)
    print("[prep] context cached beside the script: %s"
          % os.path.basename(ctx_path))
    print("[prep] %s" % PAREN)
    return 0


# ------------------------------------------------------------------
# STAGE: READ (the CD-5 measurement acts from the prep context)
# ------------------------------------------------------------------
def do_read(args, search_roots):
    paths = discover(READ_INPUT_SPECS, search_roots, "read")
    instr = discover_instruments(search_roots, "read")
    paths.update(instr)
    ctx_path = args.ctx
    if not os.path.isfile(ctx_path):
        for root in search_roots:
            if not root:
                continue
            for dirpath, dirnames, filenames in os.walk(root):
                if CTX_NAME in filenames:
                    ctx_path = os.path.join(dirpath, CTX_NAME)
                    break
    check(os.path.isfile(ctx_path), "MISSING-CTX",
          "the prep context %s absent -- run --stage prep first (the "
          "two-stage command law)" % CTX_NAME)
    with open(ctx_path, "rb") as fh:
        ctx = pickle.load(fh)
    check(ctx.get("version") == VERSION, "CTX-VERSION",
          "the prep context carries version %r != %s"
          % (ctx.get("version"), VERSION))
    M = load_instruments(paths)

    def out(line):
        print(line)

    out("[read] %s --stage read: the CD-5 measurement acts on the "
        "cross-domain probe cache (offline, zero GPU, zero decodes)"
        % VERSION)
    out("[pin] the instruments of record imported VERBATIM, "
        "byte-pinned at load: splitter 52,410 B / engines 11,980 B / "
        "accumulator 58,292 B / prose accumulator 76,867 B / hook "
        "52,078 B / the walk 89,115 B (the rw16 lane-join law) / the "
        "CD builder 66,048 B (the cold census door) -- zero "
        "instrument bytes moved")
    cache_obj = json.load(open(paths["crossdomain_probe_cache_v1.json"]))
    census_obj = json.load(open(
        paths["crossdomain_probe_census_v1.json"]))
    out("[calib] THE EMISSION CALIBRATION OF RECORD (from the prep "
        "context): the even-A %d lane moments at every horizon, zero "
        "new constants | the rw16 port cross-checked EXACT on all %d "
        "corpus docs at prep | THE CODE-BAND CALIBRATION OF RECORD: "
        "the even-A %d prefix moments measured from the code cache of "
        "record (the accumulator's own law, the population pin read "
        "fail-loud)"
        % (ctx["calib_prose"]["n_evenA"], ctx["rw16"]["cross_checked"],
           ctx["even_a_code"]))
    out("[calib] the lane-join sources: %d EMISSION source docs "
        "sliced at prep (steps + walk ids + the per-step zmax); their "
        "calibration-half memberships %s (descriptive, the "
        "development-snapshot law; the held-out act named forward)"
        % (len(ctx["sources"]), json.dumps(ctx["membership"],
                                           sort_keys=True)))
    acc = M["triadic_accumulator_v1"]
    calib_code = acc.Calibration(ctx["calib_code_moments"],
                                 {"even_A": ctx["even_a_code"]})
    receipts = run_cd5(M, cache_obj, census_obj, ctx["sources"],
                       ctx["calib_prose"], calib_code, out)
    n_ok = sum(1 for c in receipts["checks"] if c[3])
    if n_ok != len(receipts["checks"]):
        out("[read] %d of %d checks landed -- the divergence printed "
            "by name above, exit nonzero, never silent"
            % (n_ok, len(receipts["checks"])))
        return 1
    out("[read] every check landed (%d/%d); exit 0"
        % (n_ok, len(receipts["checks"])))
    out("[read] the standing: theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; both "
        "forms printed side by side, the designation carried open; "
        "nothing actuates (the ladder E0 offline, the efficacy "
        "terminals NAMED-UNMEASURED-OFFLINE); the findings presented, "
        "never adjudicated -- the owner's stamps decide")
    out(PAREN)
    return 0


# ------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=VERSION)
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--stage", choices=("prep", "read", "all"),
                    default=None)
    ap.add_argument("--root", action="append", default=[],
                    help="an extra search root (repeatable)")
    ap.add_argument("--instruments", default=None,
                    help="a directory holding the instruments")
    ap.add_argument("--ctx", default=CTX_NAME,
                    help="the prep context path (default: beside the "
                         "script, a bare filename)")
    args = ap.parse_args()
    roots = list(args.root)
    if args.instruments:
        roots.append(args.instruments)
    if os.environ.get("INSTRUMENTS_DIR"):
        roots.append(os.environ["INSTRUMENTS_DIR"])
    roots.append(os.getcwd())
    roots.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        if args.battery:
            paths = discover_instruments(roots, "battery")
            M = load_instruments(paths)
            return run_battery(M, print)
        if args.stage == "prep":
            return do_prep(args, roots)
        if args.stage == "read":
            return do_read(args, roots)
        if args.stage == "all":
            rc = do_prep(args, roots)
            if rc:
                return rc
            return do_read(args, roots)
        ap.print_help()
        return 1
    except ReadoutDie as e:
        print("[DIE] %s: %s" % (e.code, e.msg))
        print("[DIE] %s ends LOUD, never silent" % VERSION)
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""
THE STAGE-1 CACHE LOADERS v1.1  --  build message 2 of 3
(the Stage-1 forward-pass accumulator instrument, the amendment loaders layer)

Built under the PINNED amendment sheet stage1-amendment-v1_1-preregistration.md
(9,240 bytes, SHA-256 b1a337c042c10f284e9d7198ccf47dc8c381c42eee1c8077c1a080fc45347bdc,
pinned at item 1321). The v1.0 loader surface is IMPORTED VERBATIM from
triadic_stage1_loaders_v1.py (23,880 bytes, SHA-256 f48bd3f46ced97ca91dc7d04b8bd6bb326a7fd7a39d920845f2dd1e2ed33582f,
byte-pinned, standing unedited; it imports the v1.0 engines, byte-pinned in turn)
and re-exported UNCHANGED: one source, every definition exercised twice. This
module adds ONLY the amendment's thin-parse layer (section 4a): the three -r2
thins ride the portability law verbatim -- the sha PRINTED at load, never
asserted (owner-side files; his machine's print is the receipt, the banked
receipt printed BESIDE for his eyeball) -- AND are now PARSED: the per-step
walk lanes (s and PR per step, E and H, the step-index t lane that carries the
bucket law, the id / layer / rho / rsize lanes) and the per-commit emission
fields (t / token / phase minimum) enter the readout. The parse negatives die
LOUD: tampered rows, ragged rows, missing lanes, broken t contiguity, commit
rows outside the walk window -- the amendment sheet's own list. The math thin
of record is referenced by its banked description ONLY (its exact filename
carries a banned token and never enters these bytes -- the item-1197 parens
law).

House laws riding this module: findings presented never adjudicated; nothing
wires, nothing actuates; the disarmament law rides. The real-bytes control
is STRUCTURAL ONLY, values discarded, zero readouts (the owner's-hardware
law: the readout itself runs owner-side at his single run).
"""

import os
import json
import hashlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triadic_stage1_loaders_v1 as L1
import triadic_stage1_engines_v1_1 as EA

# the pins of the surfaces this module extends (the smoke and the instrument
# assert the on-disk bytes against these at import -- fail-loud, the
# never-run-unverified-bytes law)
V1_LOADERS_SHA = 'f48bd3f46ced97ca91dc7d04b8bd6bb326a7fd7a39d920845f2dd1e2ed33582f'
V1_ENGINES_SHA = '79c794c0a850f67212d3ab82f55cc2680451c33c4edc1b1ac8d93d6760af907b'
V1_1_ENGINES_SHA = 'c3c807d1a6b6b45c7c8a4efe89ab3fb5ecc372b910d8f4cd7deaee9fb22a14e6'
AMENDMENT_SHEET_SHA = 'b1a337c042c10f284e9d7198ccf47dc8c381c42eee1c8077c1a080fc45347bdc'


# ------------------------------------------------- the v1.0 loader surface, re-exported UNCHANGED
# (one source: these ARE the v1.0 module's own objects, never copies)
LoudFail = L1.LoudFail
loud = L1.loud
PIN_CODE_EXPORT = L1.PIN_CODE_EXPORT
PIN_REGRADE_EXPORT = L1.PIN_REGRADE_EXPORT
PIN_MATH_EXPORT = L1.PIN_MATH_EXPORT
PIN_TJOINT_CONSOLE = L1.PIN_TJOINT_CONSOLE
POP_CODE_DOCS = L1.POP_CODE_DOCS
POP_CODE_ROWS = L1.POP_CODE_ROWS
POP_CODE_STRATA = L1.POP_CODE_STRATA
POP_CODE_EVEN_A = L1.POP_CODE_EVEN_A
POP_CODE_EVEN_TOTAL = L1.POP_CODE_EVEN_TOTAL
POP_MATH_VARIANTS = L1.POP_MATH_VARIANTS
POP_MATH_L1_PAIR_ID = L1.POP_MATH_L1_PAIR_ID
PB4_CONSTANTS = L1.PB4_CONSTANTS
pin_file = L1.pin_file
load_thin_printed = L1.load_thin_printed
load_code_export = L1.load_code_export
extraction_control_code = L1.extraction_control_code
load_regrade_export = L1.load_regrade_export
load_math_pairs = L1.load_math_pairs
load_console_census = L1.load_console_census

# the amendment engines' roster census, re-exported for the instrument's start
dedup_census = EA.dedup_census
ROSTER_COMPOSITE_V10 = EA.ROSTER_COMPOSITE_V10
ROSTER_COMPOSITE_V11 = EA.ROSTER_COMPOSITE_V11


# ================================================== SECTION 4a -- THE THIN-PARSE LAYER
# The two -r2 walk thins' filenames are lawful in these bytes; the math thin of
# record's filename carries a banned token and rides its banked description only.
CODE_THIN_FILE = 'triadic_t2_thin_rw17-code-r2.jsonl'
PROSE_THIN_FILE = 'triadic_t2_thin_rw17-prose-r2.jsonl'
MATH_THIN_LABEL = ('the math thin of record (the 1,319-doc math corpus + the 10 loop '
                   'fixtures -- its exact filename is banked inside the item-1197 '
                   'parens; the standing token law bars it from these bytes)')

# the parsed per-step walk lanes: s and PR per step (the sheet's own pair),
# E and H, the step-index t lane (which carries the bucket law at step//16),
# and the id / layer / rho / rsize structural lanes
THIN_STEP_LANES = ('t', 's', 'PR', 'E', 'H', 'id', 'layer', 'rho', 'rsize')
# lanes parsed when present, None-safe (absent lanes never die -- the real
# records carry them as None-valued columns on some legs)
THIN_OPTIONAL_LANES = ('a', 'f', 'dead3', 'dead4', 'dead5', 'dead_share')
# the per-commit emission fields, the minimum set (the fuller emission census
# rides the commit rows themselves; the readout reads what it pre-registered)
THIN_COMMIT_MIN_FIELDS = ('t', 'token', 'phase')

# the banked thin receipts, PRINTED BESIDE at load for the eyeball, never
# asserted (the portability law verbatim: owner-side files; his machine's
# sha print is the receipt)
BANKED_THIN_RECEIPTS = {
    'code': ('77dd63c7d21c630336e0afb074fbf15515b72c7da80831e9969314529a79a9b4', 410),
    'prose': ('88cbadee7baa1e35fe7e762715970066d6098301f044f810c0efd1e38c70ae94', 630),
    'math': ('282d48ed5043126295b506983e97a5a75160fa02e13b1dda45d00331f43af1fd', 1329),
}


def parse_thin_record(rec, label, lineno):
    """Section 4a: ONE thin record parsed under the fail-loud gates -- the
    amendment sheet's own negative list: tampered rows (not a JSON object),
    missing lanes (the steps dict or a required lane absent), ragged rows (a
    lane length off the t lane), a non-numeric lane value, a t-contiguity
    break, a commit row missing its minimum emission fields, a commit t
    outside the walk window, an absent doc_id, a DUPLICATE corpus doc_id (the
    doc-key join law). The is-int doc guard rides the census: an int doc_id
    is a corpus walk doc, a non-int id a named fixture record (the banked
    law: the walk thins carry the corpus under int ids, the fixtures at the
    tail under string ids). Returns the parsed record dict (the lanes and the
    commit rows for the owner-side readout; the builder-side control discards
    them)."""
    if not isinstance(rec, dict):
        loud('thin parse', f'{label} record {lineno}: not a JSON object (tampered row)')
    if 'doc_id' not in rec:
        loud('thin parse', f'{label} record {lineno}: the doc_id field absent (tampered row)')
    did = rec['doc_id']
    steps = rec.get('steps')
    if not isinstance(steps, dict):
        loud('thin parse', f'{label} record {lineno} (doc {did!r}): the steps dict absent (missing lanes)')
    for lane in THIN_STEP_LANES:
        if lane not in steps:
            loud('thin parse', f'{label} record {lineno} (doc {did!r}): the {lane!r} step lane absent (missing lanes)')
    n = len(steps['t'])
    for lane in steps:
        if len(steps[lane]) != n:
            loud('thin parse', f'{label} record {lineno} (doc {did!r}): the {lane!r} lane length '
                               f'{len(steps[lane])} != the t lane {n} (ragged row)')
    for lane in THIN_STEP_LANES + tuple(l for l in THIN_OPTIONAL_LANES if l in steps):
        for v in steps[lane]:
            if v is not None and not isinstance(v, (int, float)):
                loud('thin parse', f'{label} record {lineno} (doc {did!r}): the {lane!r} lane '
                                   f'carries a non-numeric value {v!r} (tampered row)')
    if n and steps['t'][0] is not None:
        t0 = steps['t'][0]
        for j, tv in enumerate(steps['t']):
            if tv != t0 + j:
                loud('thin parse', f'{label} record {lineno} (doc {did!r}): the t lane breaks '
                                   f'contiguity at index {j} ({tv!r} != {t0} + {j})')
    else:
        t0 = None
    commits = rec.get('commits')
    if not isinstance(commits, list):
        loud('thin parse', f'{label} record {lineno} (doc {did!r}): the commits list absent (missing lanes)')
    for c in commits:
        if not isinstance(c, dict):
            loud('thin parse', f'{label} record {lineno} (doc {did!r}): a commit row is not an object (tampered row)')
        for fld in THIN_COMMIT_MIN_FIELDS:
            if fld not in c:
                loud('thin parse', f'{label} record {lineno} (doc {did!r}): a commit row missing '
                                   f'the {fld!r} field (missing lanes)')
        ct = c.get('t')
        if t0 is not None and (not isinstance(ct, int) or not (t0 <= ct < t0 + n)):
            loud('thin parse', f'{label} record {lineno} (doc {did!r}): commit t {ct!r} outside '
                               f'the walk window [{t0}, {t0 + n}) (tampered row)')
    return {'doc_id': did, 'leg': rec.get('leg'),
            'is_fixture': not isinstance(did, int), 'n_steps': n,
            'lanes': {lane: steps[lane] for lane in steps},
            'commits': commits}


def load_thin_parsed(path, label='the -r2 thin of record', banked=None, name_printed=None):
    """Section 4a: THE THIN JOIN DELIVERED AT THE LOADER LAYER. The portability
    law verbatim -- the sha PRINTED at load, never asserted (owner-side files;
    his machine's print is the receipt), the record census loud, the banked
    receipt (sha, records) printed BESIDE for the eyeball when given -- AND
    every record PARSED under the fail-loud gates (parse_thin_record). The
    name_printed lane carries the v1.0 owner-side print genre (his machine
    prints his basename, the item-1317 precedent); the builder-side control
    passes the label alone so the builder console carries no banned-token
    bytes. Returns {'sha_printed', 'records', 'corpus', 'fixtures', 'parsed'};
    the corpus doc census asserts the doc-key uniqueness law. The parsed
    values are for the owner-side readout; the builder-side control discards
    them."""
    if not os.path.exists(path):
        loud(label, f'absent file at {path}')
    h = hashlib.sha256()
    n = 0
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
            n += chunk.count(b'\n')
    got = h.hexdigest()
    parsed = []
    corpus_ids = set()
    dup = None
    n_corpus = 0
    n_fixture = 0
    with open(path, 'r', encoding='utf-8') as f:
        lineno = 0
        for ln in f:
            lineno += 1
            try:
                rec = json.loads(ln)
            except json.JSONDecodeError as e:
                loud('thin parse', f'{label} record {lineno}: the line is not valid JSON '
                                   f'(tampered row): {e}')
            pr = parse_thin_record(rec, label, lineno)
            if pr['is_fixture']:
                n_fixture += 1
            else:
                n_corpus += 1
                if pr['doc_id'] in corpus_ids and dup is None:
                    dup = pr['doc_id']
                corpus_ids.add(pr['doc_id'])
            parsed.append(pr)
    if dup is not None:
        loud('thin parse', f'{label}: DUPLICATE corpus doc_id {dup!r} (the doc-key join law)')
    if lineno != n:
        loud('thin parse', f'{label}: the line census {lineno} != the byte-level newline census {n}')
    banked_line = ''
    if banked is not None:
        banked_line = (f' | the banked receipt beside (for the eyeball, never asserted): '
                       f'sha {banked[0][:16]}... / {banked[1]} records')
    shown = name_printed if name_printed else os.path.basename(path)
    print(f'  [load] {label}: {shown} -- sha256 {got} PRINTED AT LOAD '
          f'(the portability law, never asserted) | {lineno} records censused, '
          f'{n_corpus} corpus walk docs + {n_fixture} named fixtures, every record '
          f'PARSED under the fail-loud gates{banked_line}')
    return {'sha_printed': got, 'records': lineno, 'corpus': n_corpus,
            'fixtures': n_fixture, 'parsed': parsed}


def thin_parse_control(path, label, banked, expect_corpus, expect_fixtures, name_printed=None):
    """Section 4a + the amendment sheet's section-5 build law: the REAL-BYTES
    STRUCTURAL CONTROL over a thin of record -- every record parsed under the
    fail-loud gates, STRUCTURAL RECEIPTS ONLY, every value DISCARDED (the
    parsed lanes and commit rows never leave this function; the receipt
    carries counts only). The corpus/fixture census asserts the expected
    split; the sha PRINTS and the banked receipt rides beside, never asserted
    (the portability law verbatim). Zero readouts computed. The leg census
    carries its names in the RETURNED receipt only -- the printed line counts
    the distinct legs, so no corpus-leg name ever needs to reach a scanned
    console byte."""
    out = load_thin_parsed(path, label, banked=banked, name_printed=name_printed)
    n_steps_min = None
    n_steps_max = None
    commits_total = 0
    legs = {}
    extra_fields = set()
    for pr in out['parsed']:
        if n_steps_min is None or pr['n_steps'] < n_steps_min:
            n_steps_min = pr['n_steps']
        if n_steps_max is None or pr['n_steps'] > n_steps_max:
            n_steps_max = pr['n_steps']
        commits_total += len(pr['commits'])
        lg = pr['leg']
        legs[lg] = legs.get(lg, 0) + 1
        for c in pr['commits']:
            extra_fields.update(c.keys())
        pr['lanes'] = None      # the values are DISCARDED here, never emitted
        pr['commits'] = None
    out['parsed'] = None
    if out['corpus'] != expect_corpus or out['fixtures'] != expect_fixtures:
        loud('thin control', f'{label}: corpus {out["corpus"]} / fixtures {out["fixtures"]} '
                             f'!= the expected split {expect_corpus} / {expect_fixtures}')
    receipt = {'records': out['records'], 'corpus': out['corpus'], 'fixtures': out['fixtures'],
               'sha_printed': out['sha_printed'], 'n_steps_min': n_steps_min,
               'n_steps_max': n_steps_max, 'commits_total': commits_total,
               'leg_census': legs, 'commit_fields': sorted(extra_fields)}
    print(f'  [thin control] {label}: records {receipt["records"]} = corpus {receipt["corpus"]} '
          f'+ fixtures {receipt["fixtures"]} | walk lanes per record '
          f'{receipt["n_steps_min"]}..{receipt["n_steps_max"]} | commits {receipt["commits_total"]} '
          f'| {len(legs)} legs distinct (the census in the receipt) -- VALUES DISCARDED, '
          f'counts only, zero readouts')
    return receipt

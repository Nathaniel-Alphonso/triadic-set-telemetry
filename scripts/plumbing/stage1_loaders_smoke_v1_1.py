"""
THE STAGE-1 LOADERS KNOWN-ANSWER SMOKE v1.1  --  build message 2 of 3

PART A: synthetic fixture worlds, ZERO real rows (my-hardware law):
the pin machinery probed by tampering, the thin-parse laws exercised on
hand-authored records with every negative dying its named loud line (the
amendment sheet's own list: tampered rows, ragged rows, missing lanes, the
t-contiguity break, commit rows outside the walk window), the portability
law proven (the sha PRINTED at load, never asserted; the banked receipt
printed beside for the eyeball), the determinism battery run twice
byte-identical. PART B: THE REAL-BYTES CONTROL (the amendment sheet's
section-5 build law) -- the four local files of record loaded through the
re-exported v1.0 loaders with every pin exact, and THE THREE REAL THINS
PARSED under the fail-loud gates for STRUCTURAL RECEIPTS ONLY, every value
DISCARDED, zero readouts computed (the readout itself runs on my side at
my single run).
"""

import os
import sys
import json
import math
import hashlib
import shutil
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import triadic_stage1_loaders_v1 as L1
import triadic_stage1_engines_v1_1 as EA
import triadic_stage1_loaders_v1_1 as A

PASS = 0
FAIL = 0


def ok(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f'PASS {name} {detail}')
    else:
        FAIL += 1
        print(f'FAIL {name} {detail}')


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol


def expect_loud(name, marker, fn):
    try:
        fn()
        ok(name, False, f'no loud fail -- expected the {marker!r} line')
    except (A.LoudFail, RuntimeError) as e:
        ok(name, marker in str(e), str(e)[:100])


def sha_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


WORLD = os.path.join(BASE, '.scratch', 'stage1_loader_v11_smoke_world')
shutil.rmtree(WORLD, ignore_errors=True)
os.makedirs(WORLD)


# ============================================== S0 the one-source world
print()
print('== S0 THE ONE-SOURCE WORLD (the v1.0 loader surface re-exported UNCHANGED, sha-guarded) ==')
ok('S0a the v1.0 loaders sha exact', sha_of(os.path.join(BASE, 'triadic_stage1_loaders_v1.py')) == A.V1_LOADERS_SHA)
ok('S0b the v1.0 engines sha carried', sha_of(os.path.join(BASE, 'triadic_stage1_engines_v1.py')) == A.V1_ENGINES_SHA)
ok('S0c the v1.1 engines sha exact', sha_of(os.path.join(BASE, 'triadic_stage1_engines_v1_1.py')) == A.V1_1_ENGINES_SHA)
ok('S0d the pinned amendment sheet sha exact',
   sha_of(os.path.join(BASE, 'stage1-amendment-v1_1-preregistration.md')) == A.AMENDMENT_SHEET_SHA)
ok('S0e pin_file is the v1.0 object (one source, no copy)', A.pin_file is L1.pin_file)
ok('S0f load_code_export is the v1.0 object', A.load_code_export is L1.load_code_export)
ok('S0g load_console_census is the v1.0 object', A.load_console_census is L1.load_console_census)
ok('S0h LoudFail is the v1.0 object', A.LoudFail is L1.LoudFail)
ok('S0i dedup_census is the v1.1 engines\' object', A.dedup_census is EA.dedup_census)
ok('S0j the v1.0 population pins carried', A.POP_CODE_DOCS == 400
   and A.POP_MATH_VARIANTS == (48, 47, 46, 43) and A.PB4_CONSTANTS['tail'] == [19, 36])
ok('S0k the deduplicated roster carried', len(A.ROSTER_COMPOSITE_V11) == 9
   and 'h_num_content' not in A.ROSTER_COMPOSITE_V11)


# ============================================== P-A the pin machinery world
print()
print('== P-A THE PIN MACHINERY WORLD (byte-count-before-hash, fail-loud, tampered probes) ==')
p_ok = os.path.join(WORLD, 'pin_ok.bin')
with open(p_ok, 'wb') as f:
    f.write(b'hello world')
good_sha = hashlib.sha256(b'hello world').hexdigest()
try:
    got = A.pin_file(p_ok, 11, good_sha, 'the probe file')
    ok('Pa1 a correct pin passes and returns the bytes', got == b'hello world')
except A.LoudFail as e:
    ok('Pa1 a correct pin passes and returns the bytes', False, str(e)[:100])
expect_loud('Pa2 a wrong sha dies with the named line', 'sha',
            lambda: A.pin_file(p_ok, 11, '0' * 64, 'the probe file'))
expect_loud('Pa3 a wrong byte count dies BEFORE any hash (the house law)', 'byte count',
            lambda: A.pin_file(p_ok, 12, good_sha, 'the probe file'))
expect_loud('Pa4 the absent file dies loud', 'absent file',
            lambda: A.pin_file(os.path.join(WORLD, 'absent.bin'), 11, good_sha, 'the probe file'))


# ============================================== P-B the thin-parse world
print()
print('== P-B THE THIN-PARSE WORLD (section 4a: the portability law verbatim + the parse negatives) ==')


def rec_corpus(did, ns, commits):
    t = list(range(ns))
    return {'doc_id': did, 'leg': 'toyleg',
            'steps': {'t': t, 's': [1.0 + i for i in t], 'PR': [0.5 * i for i in t],
                      'E': [0.1] * ns, 'H': [2.0] * ns, 'id': [7 * (i + 1) for i in t],
                      'layer': [1] * ns, 'rho': [0.5] * ns, 'rsize': [4] * ns},
            'commits': [{'t': ct, 'token': f'tok{j}', 'phase': ph}
                        for j, (ct, ph) in enumerate(commits)]}


def rec_fixture(did, ns):
    return rec_corpus(did, ns, [(ns - 1, 'return')])


def write_thin(path, records, trailing_newline=True):
    with open(path, 'w', encoding='utf-8') as f:
        for i, r in enumerate(records):
            f.write(json.dumps(r))
            if trailing_newline or i < len(records) - 1:
                f.write('\n')


good = os.path.join(WORLD, 'good_thin.jsonl')
records_good = [
    rec_corpus(0, 4, [(1, 'def'), (3, 'return')]),
    rec_corpus(1, 3, [(2, 'def')]),
    dict(rec_fixture('loop-seeded-code-line', 2), leg='loop'),
]
write_thin(good, records_good)
out = A.load_thin_parsed(good, 'the synthetic thin')
ok('Pb1 the record census exact (3 records, 2 corpus + 1 fixture)',
   out['records'] == 3 and out['corpus'] == 2 and out['fixtures'] == 1)
ok('Pb2 the sha PRINTED at load matches the file (the portability receipt)',
   out['sha_printed'] == sha_of(good))
ok('Pb3 the lanes parsed exact', out['parsed'][0]['lanes']['s'] == [1.0, 2.0, 3.0, 4.0]
   and out['parsed'][0]['n_steps'] == 4)
ok('Pb4 the is-int doc guard rides the census (corpus int / fixture string)',
   out['parsed'][0]['is_fixture'] is False and out['parsed'][2]['is_fixture'] is True)
ok('Pb5 the commit rows parsed', len(out['parsed'][0]['commits']) == 2
   and out['parsed'][0]['commits'][0]['phase'] == 'def')
try:
    out2 = A.load_thin_parsed(good, 'the synthetic thin', banked=('f' * 64, 999))
    ok('Pb6 the portability law held: a WRONG banked receipt NEVER asserts (eyeball law)',
       out2['records'] == 3)
except A.LoudFail as e:
    ok('Pb6 the portability law held: a WRONG banked receipt NEVER asserts (eyeball law)',
       False, str(e)[:100])
try:
    out3 = A.load_thin_parsed(good, 'the synthetic thin', name_printed='the named lane')
    ok('Pb7 the name_printed lane carries (my-side print genre, the builder bytes clean)',
       out3['records'] == 3)
except A.LoudFail as e:
    ok('Pb7 the name_printed lane carries (my-side print genre, the builder bytes clean)',
       False, str(e)[:100])

# the parse negatives, each dying its named loud line
tampered = os.path.join(WORLD, 'tampered.jsonl')
write_thin(tampered, records_good)
with open(tampered, 'a', encoding='utf-8') as f:
    f.write('this line is not json\n')
expect_loud('Pb8 a tampered row (invalid JSON) dies loud', 'tampered row',
            lambda: A.load_thin_parsed(tampered, 'the synthetic thin'))

ragged = os.path.join(WORLD, 'ragged.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
r['steps']['s'] = r['steps']['s'][:3]          # the s lane off the t lane
write_thin(ragged, [r])
expect_loud('Pb9 a ragged row (lane length off the t lane) dies loud', 'ragged row',
            lambda: A.load_thin_parsed(ragged, 'the synthetic thin'))

missing_lane = os.path.join(WORLD, 'missing_lane.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
del r['steps']['s']
write_thin(missing_lane, [r])
expect_loud('Pb10 a missing lane (the s lane absent) dies loud', 'missing lanes',
            lambda: A.load_thin_parsed(missing_lane, 'the synthetic thin'))

missing_steps = os.path.join(WORLD, 'missing_steps.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
del r['steps']
write_thin(missing_steps, [r])
expect_loud('Pb11 the steps dict absent dies loud', 'missing lanes',
            lambda: A.load_thin_parsed(missing_steps, 'the synthetic thin'))

nonnum = os.path.join(WORLD, 'nonnum.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
r['steps']['E'] = [0.1, 'x', 0.1, 0.1]
write_thin(nonnum, [r])
expect_loud('Pb12 a non-numeric lane value dies loud', 'tampered row',
            lambda: A.load_thin_parsed(nonnum, 'the synthetic thin'))

contig = os.path.join(WORLD, 'contig.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
r['steps']['t'] = [0, 1, 3, 3]
write_thin(contig, [r])
expect_loud('Pb13 a t-contiguity break dies loud', 'contiguity',
            lambda: A.load_thin_parsed(contig, 'the synthetic thin'))

commit_field = os.path.join(WORLD, 'commit_field.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
del r['commits'][0]['phase']
write_thin(commit_field, [r])
expect_loud('Pb14 a commit row missing a field dies loud', 'missing lanes',
            lambda: A.load_thin_parsed(commit_field, 'the synthetic thin'))

commit_range = os.path.join(WORLD, 'commit_range.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
r['commits'][0]['t'] = 9
write_thin(commit_range, [r])
expect_loud('Pb15 a commit t outside the walk window dies loud', 'outside the walk window',
            lambda: A.load_thin_parsed(commit_range, 'the synthetic thin'))

no_docid = os.path.join(WORLD, 'no_docid.jsonl')
r = rec_corpus(0, 4, [(1, 'def')])
del r['doc_id']
write_thin(no_docid, [r])
expect_loud('Pb16 an absent doc_id dies loud', 'doc_id field absent',
            lambda: A.load_thin_parsed(no_docid, 'the synthetic thin'))

dup = os.path.join(WORLD, 'dup.jsonl')
write_thin(dup, [rec_corpus(0, 4, [(1, 'def')]), rec_corpus(0, 3, [(1, 'def')])])
expect_loud('Pb17 a DUPLICATE corpus doc_id dies loud (the doc-key join law)', 'DUPLICATE corpus doc_id',
            lambda: A.load_thin_parsed(dup, 'the synthetic thin'))

no_trail = os.path.join(WORLD, 'no_trail.jsonl')
write_thin(no_trail, records_good, trailing_newline=False)
expect_loud('Pb18 a line/newline census mismatch dies loud', 'line census',
            lambda: A.load_thin_parsed(no_trail, 'the synthetic thin'))

# the structural control: counts only, values discarded
ctrl = A.thin_parse_control(good, 'the synthetic thin', ('f' * 64, 3), 2, 1)
ok('Pb19 the control receipt exact (counts only)',
   ctrl['records'] == 3 and ctrl['corpus'] == 2 and ctrl['fixtures'] == 1
   and ctrl['commits_total'] == 4 and ctrl['n_steps_min'] == 2 and ctrl['n_steps_max'] == 4)
ok('Pb20 the leg census carried in the receipt (names never printed)',
   ctrl['leg_census'] == {'toyleg': 2, 'loop': 1})
ok('Pb21 the control carries NO parsed values (discarded by construction)',
   'parsed' not in ctrl and 'lanes' not in ctrl)
expect_loud('Pb22 a control census mismatch dies loud', 'thin control',
            lambda: A.thin_parse_control(good, 'the synthetic thin', ('f' * 64, 3), 3, 1))

# the v1.0 portability loader still standing beside (one source, exercised)
old = L1.load_thin_printed(good, 'the synthetic thin')
ok('Pb23 the v1.0 load_thin_printed re-exported and standing (the census genre)',
   old['records'] == 3 and old['sha_printed'] == sha_of(good))


# ============================================== P-C the determinism world
print()
print('== P-C THE DETERMINISM WORLD (the parse battery run twice, byte-identical) ==')
def canonical_bytes():
    o = A.load_thin_parsed(good, 'the synthetic thin')
    parts = [repr((o['records'], o['corpus'], o['fixtures'], o['sha_printed']))]
    for pr in o['parsed']:
        parts.append(repr((pr['doc_id'], pr['is_fixture'], pr['n_steps'], pr['leg'],
                           pr['lanes']['s'], pr['lanes']['t'],
                           [(c['t'], c['phase']) for c in pr['commits']])))
    return '\n'.join(parts).encode('utf-8')


c1 = canonical_bytes()
c2 = canonical_bytes()
ok('Pc1 the parse battery run twice byte-identical', c1 == c2,
   f'sha {hashlib.sha256(c1).hexdigest()[:16]}... twice')


# ============================================== PART B: the real-bytes control
print()
print('== PART B: THE REAL-BYTES CONTROL (the four files of record + the three real thins,')
print('   every record parsed, counts only, VALUES DISCARDED, zero readouts) ==')
code_path = os.path.join(BASE, 'wu-read-receipts', 'triadic_wu_code_read_v1.json')
regrade_path = os.path.join(BASE, '.scratch', 'port_eq', 'regrade-v2_export.json')
math_path = os.path.join(BASE, '.scratch', 'owner_see_everything_v1.json')
console_path = os.path.join(BASE, '.scratch', 'tjoint_read_v2_console.txt')
THINS = os.path.join(BASE, '.scratch', 'thins')

d, rec = A.load_code_export(code_path)
ok('B1 the code export pins exact (docs / rows / onset / empty windows)',
   rec['docs'] == 400 and rec['rows'] == 113238 and rec['onset'] == 400
   and rec['work_empty'] == 400)
ok('B2 even-A 49 COUNTED from the halves (never derived)', rec['even_a'] == 49)
ok('B3 the strata cells exact', rec['strata'] == {'A': 102, 'B': 237, 'C': 61, 'D': 0})
ok('B4 the survival cohorts 49 / 49 / 49 with zero censoring',
   rec['cohorts'] == {36: (49, 0), 64: (49, 0), 128: (49, 0)})
ec = A.extraction_control_code(d, pins_rows=113238)
ok('B5 the extraction control swept every doc and row',
   ec['docs'] == 400 and ec['rows_total'] == 113238 and ec['len_min'] == 166
   and ec['len_max'] == 502 and all(v == 400 for v in ec['reach'].values()))

rg, rgrec = A.load_regrade_export(regrade_path)
ok('B6 the regrade cells + the P-B4 constants exact',
   rgrec['prose_cells'] == {'A': 210, 'B': 363, 'C': 43, 'D': 4}
   and rgrec['code_cells'] == {'A': 102, 'B': 237, 'C': 61, 'D': 0}
   and rgrec['pb4']['tail'] == [19, 36])

mp = A.load_math_pairs(math_path)
ok('B7 the math pair census + the L1 law counted',
   mp['complete'] == 68 and mp['incomplete'] == 5 and mp['l1_ids'] == ['A2-0033'])

cc = A.load_console_census(console_path)
ok('B8 the 616 census line read exact',
   cc['docs'] == 620 and cc['commits'] == 260854 and cc['odd'] == (186, 124)
   and cc['even'] == (220, 86) and cc['strata'] == {'A': 210, 'B': 363, 'C': 43, 'D': 4})
ok('B9 the pooled-arm selection receipt exact', cc['arm'] == (65, 23))

# ---- the three real thins, PARSED (the thin join at the loader layer, structural only)
ctc = A.thin_parse_control(os.path.join(THINS, 'triadic_t2_thin_rw17-code-r2.jsonl'),
                           'the code thin of record', A.BANKED_THIN_RECEIPTS['code'], 400, 10)
ok('B10 the code thin parsed: 410 records = 400 corpus + 10 fixtures',
   ctc['records'] == 410 and ctc['corpus'] == 400 and ctc['fixtures'] == 10)
ok('B11 the code thin sha print == the banked receipt (the local copy is the banked bytes)',
   ctc['sha_printed'] == A.BANKED_THIN_RECEIPTS['code'][0])
ok('B12 the code thin leg census exact (in the receipt, never printed)',
   ctc['leg_census'].get('mbpprw17') == 400 and ctc['leg_census'].get('loop') == 10
   and len(ctc['leg_census']) == 2)
ok('B13 the code thin commit fields carry the emission set',
   set(A.THIN_COMMIT_MIN_FIELDS).issubset(set(ctc['commit_fields'])))

ptc = A.thin_parse_control(os.path.join(THINS, 'triadic_t2_thin_rw17-prose-r2.jsonl'),
                           'the prose thin of record', A.BANKED_THIN_RECEIPTS['prose'], 620, 10)
ok('B14 the prose thin parsed: 630 records = 620 corpus + 10 fixtures',
   ptc['records'] == 630 and ptc['corpus'] == 620 and ptc['fixtures'] == 10)
ok('B15 the prose thin sha print == the banked receipt',
   ptc['sha_printed'] == A.BANKED_THIN_RECEIPTS['prose'][0])
ok('B16 the prose thin leg census exact (in the receipt, never printed)',
   ptc['leg_census'].get('prose17p-rw17') == 620 and ptc['leg_census'].get('loop') == 10
   and len(ptc['leg_census']) == 2)

matches = sorted(glob.glob(os.path.join(THINS, 'triadic_t2_thin_t2-*.jsonl')))
ok('B17 the math thin of record located by its lawful pattern (exactly one match)',
   len(matches) == 1)
if matches:
    mtc = A.thin_parse_control(matches[0], 'the math thin of record',
                               A.BANKED_THIN_RECEIPTS['math'], 1319, 10,
                               name_printed='the math thin of record (its name in the item-1197 parens)')
    ok('B18 the math thin parsed: 1,329 records = 1,319 corpus + 10 fixtures',
       mtc['records'] == 1329 and mtc['corpus'] == 1319 and mtc['fixtures'] == 10)
    ok('B19 the math thin sha print == the banked receipt',
       mtc['sha_printed'] == A.BANKED_THIN_RECEIPTS['math'][0])
    ok('B20 the math thin leg census structural (the corpus leg + the loop leg, names in the receipt)',
       len(mtc['leg_census']) == 2 and max(mtc['leg_census'].values()) == 1319
       and mtc['leg_census'].get('loop') == 10)
else:
    ok('B17 the math thin of record located by its lawful pattern (exactly one match)', False)
    ok('B18 the math thin parsed: 1,329 records = 1,319 corpus + 10 fixtures', False)
    ok('B19 the math thin sha print == the banked receipt', False)
    ok('B20 the math thin leg census structural (the corpus leg + the loop leg, names in the receipt)', False)

print('  [real control] ZERO READOUTS COMPUTED -- every parsed value discarded, '
      'receipts carry counts only; the readout itself runs on my side at my single run')


# ============================================== the totals
print()
print(f'THE SMOKE TOTALS: PASS {PASS} | FAIL {FAIL}')
if FAIL:
    print('THE SMOKE FAILED LOUD -- the loaders or a fixture must be fixed before any bank')
    sys.exit(1)
print('THE SMOKE ALL GREEN -- the amendment loaders layer stands for build message 3 of 3 '
      '(the assembled instrument + the EXTENDED battery + the run book v5 + the publication)')
sys.exit(0)

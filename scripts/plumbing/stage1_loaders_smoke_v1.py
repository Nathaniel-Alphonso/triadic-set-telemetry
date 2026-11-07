"""
THE STAGE-1 LOADERS KNOWN-ANSWER SMOKE v1.0  --  build message 2 of 3

Two parts. PART A: synthetic fixture worlds (zero real rows), every expected
value recomputed in this file's own arithmetic, the fail-loud gates probed by
deliberate tampering (a tampered cache must die with the named line, never
pass). PART B: THE REAL-BYTES CONTROL (the build law: the readout tool's own
acceptance and a real-bytes control before his single run) -- the four local
pinned files of record loaded through the loaders with the REAL pins, every
population pin COUNTED from the bytes, STRUCTURAL RECEIPTS ONLY, every value
discarded, zero readouts computed (the owner's-hardware law: the readout
itself runs owner-side at his single run).
"""

import json
import os
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triadic_stage1_loaders_v1 as L
import triadic_stage1_engines_v1 as E

BASE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(BASE, '.scratch', 'stage1_loader_smoke_world')
os.makedirs(WORLD, exist_ok=True)

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


def loud_probe(name, fn, needle):
    """The tamper probe: the call must die with the named loud line, never pass."""
    try:
        fn()
    except L.LoudFail as e:
        ok(name, needle in str(e), f'caught: {str(e)[:100]}')
        return
    except Exception as e:  # noqa: BLE001
        ok(name, False, f'wrong exception class: {type(e).__name__}: {e}')
        return
    ok(name, False, 'NO LOUD FAIL -- the tampered cache passed silently, a gate defect')


def write_json(name, obj):
    p = os.path.join(WORLD, name)
    with open(p, 'w') as f:
        json.dump(obj, f)
    return p


def file_pin(path):
    n = os.path.getsize(path)
    h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    return {'file': ('x', n, h)}


print()
print('== PART A: THE SYNTHETIC FIXTURE WORLDS (zero real rows) ==')

# ---------------------------------------------------------------- A1 the pin machinery
print()
print('== A1 THE PIN MACHINERY (byte-count-before-hash, the sha assert, both fail-loud) ==')
p1 = write_json('a1_fixture.json', {'k': 1})
raw = L.pin_file(p1, os.path.getsize(p1), hashlib.sha256(open(p1, 'rb').read()).hexdigest(), 'A1')
ok('A1a pin pass returns the bytes', raw == open(p1, 'rb').read())
loud_probe('A1b wrong sha dies loud', lambda: L.pin_file(p1, os.path.getsize(p1), '0' * 64, 'A1'), 'sha')
loud_probe('A1c wrong byte count dies BEFORE the hash',
           lambda: L.pin_file(p1, os.path.getsize(p1) + 5, hashlib.sha256(open(p1, 'rb').read()).hexdigest(), 'A1'),
           'byte count')
loud_probe('A1d absent file dies loud', lambda: L.pin_file(os.path.join(WORLD, 'nope.json'), 10, '0' * 64, 'A1'),
           'absent')

# ---------------------------------------------------------------- A2 the synthetic code export
print()
print('== A2 THE SYNTHETIC CODE-EXPORT WORLD (every census gate counted from the bytes) ==')
LENS = [8, 12, 40, 70, 130, 200]
HALVES = ['calibration', 'calibration', 'calibration', 'held-out', 'held-out', 'held-out']
STRATA = ['A', 'B', 'A', 'C', 'B', 'A']


def build_code_export(lens=LENS, strata=STRATA):
    rd = {}
    for i, n in enumerate(lens):
        rd[str(i)] = {
            'commit_index': list(range(n)),
            'role': ['STATEMENT-ONSET'] + ['OTHER-CONTENT'] * (n - 1),
            'work_inc': [None] + [1.0] * (n - 1),
            'm_ulp_content': [1.0] * n,
            'status': ['OK'] * n,
        }
    wt = [{'doc_id': str(i), 'half': HALVES[i], 'stratum': strata[i], 'n_commits': lens[i]}
          for i in range(len(lens))]
    return {'rows_by_doc': rd, 'doc_walk_table': wt,
            'census': {'emission': {'def_by_stratum': {'A': 8, 'B': 9, 'C': 1, 'D': 0},
                                    'return_docs': 49}}}


fx = build_code_export()
fxp = write_json('a2_code_export.json', fx)
fx_pins = dict(file=file_pin(fxp)['file'], docs=6, rows=sum(LENS),
               strata={'A': 3, 'B': 2, 'C': 1, 'D': 0}, even_a=2, even_total=3,
               onset=6, other=sum(LENS) - 6, work_empty=6, mulp_sentinels=0,
               emission_def={'A': 8, 'B': 9, 'C': 1, 'D': 0}, emission_return=49)
d_out, rec = L.load_code_export(fxp, pins=dict(fx_pins))
ok('A2a load pass, receipts exact', rec['docs'] == 6 and rec['rows'] == sum(LENS)
   and rec['even_a'] == 2 and rec['strata'] == {'A': 3, 'B': 2, 'C': 1, 'D': 0})
# the even-A survival cohorts on the fixture (docs 0 and 2; lens 8 and 40)
coh = rec['cohorts']
ok('A2b horizon 36 cohort (1 live / 1 censored)', coh[36] == (1, 1))
ok('A2c horizon 64 cohort (0 live, the guard state)', coh[64] == (0, 2))
ok('A2d horizon 128 cohort (0 live)', coh[128] == (0, 2))
# the tamper probes, each a named census gate
bad = build_code_export(strata=['B', 'B', 'A', 'C', 'B', 'A'])  # stratum A->B flips two cells
badp = write_json('a2_bad_strata.json', bad)
loud_probe('A2e tampered strata dies loud',
           lambda: L.load_code_export(badp, pins=dict(fx_pins, file=file_pin(badp)['file'])),
           'strata cells')
wrong_ea = write_json('a2_code_export.json', fx)  # same bytes, but the even-A pin lied
loud_probe('A2f the halving lie dies loud (even-A pin 3 vs counted 2)',
           lambda: L.load_code_export(wrong_ea, pins=dict(fx_pins, even_a=3)),
           'never derived by halving')
bad2 = build_code_export(lens=[8, 12, 40, 70, 130, 200])
bad2['census']['emission']['return_docs'] = 48
bad2p = write_json('a2_bad_emission.json', bad2)
loud_probe('A2g tampered emission census dies loud',
           lambda: L.load_code_export(bad2p, pins=dict(fx_pins, file=file_pin(bad2p)['file'])),
           'emission census')
bad3 = build_code_export()
bad3['rows_by_doc']['0']['role'] = ['OTHER-CONTENT'] * 8
bad3p = write_json('a2_bad_roles.json', bad3)
loud_probe('A2h tampered role census dies loud',
           lambda: L.load_code_export(bad3p, pins=dict(fx_pins, file=file_pin(bad3p)['file'])),
           'role census')

# ---------------------------------------------------------------- A3 the extraction control
print()
print('== A3 THE EXTRACTION CONTROL (values discarded, counts only) ==')
ctl = L.extraction_control_code(fx, pins_rows=sum(LENS))
ok('A3a the sweep receipts counts only', ctl['docs'] == 6 and ctl['rows_total'] == sum(LENS)
   and ctl['reach'] == {36: 4, 64: 3, 128: 2} and ctl['len_min'] == 8 and ctl['len_max'] == 200)
ok('A3b the receipt carries no value-bearing field',
   all(isinstance(v, int) for v in ctl['reach'].values())
   and set(ctl.keys()) == {'docs', 'rows_total', 'reach', 'len_min', 'len_max'})
loud_probe('A3c a row-total mismatch dies loud',
           lambda: L.extraction_control_code(fx, pins_rows=sum(LENS) + 1), 'row total')

# ---------------------------------------------------------------- A4 the console census world
print()
print('== A4 THE CONSOLE-CENSUS WORLD (the population pins READ from the console of record) ==')
CONS = ('== 1. THE PROSE LEG REBUILT ==\n'
        '  GATE census: 12 docs / 500 commits | B 6/C 1/A 4/D 1 (held out [1, 2, 3, 4]) '
        '| 10 ODD 6 vs 4, EVEN 6 vs 2\n'
        '  prose doc selection receipt (EVEN row-docs 5 vs 2, raw): E_d -0.3807\n')
conp = os.path.join(WORLD, 'a4_console.txt')
open(conp, 'w').write(CONS)
con_pins = dict(file=file_pin(conp)['file'], docs=12, commits=500,
                strata={'A': 4, 'B': 6, 'C': 1, 'D': 1}, held_out=[1, 2, 3, 4],
                odd=(6, 4), even=(6, 2), arm_raw=(5, 2), arm_pooled=7, arm_neg=2)
cc = L.load_console_census(conp, pins=dict(con_pins))
ok('A4a the census line parsed + asserted', cc['docs'] == 12 and cc['odd'] == (6, 4)
   and cc['even'] == (6, 2) and cc['arm'] == (5, 2))
CONS_BAD = CONS.replace('ODD 6 vs 4', 'ODD 7 vs 4')
badp = os.path.join(WORLD, 'a4_console_bad.txt')
open(badp, 'w').write(CONS_BAD)
loud_probe('A4b the tampered ODD pairing dies loud',
           lambda: L.load_console_census(badp, pins=dict(con_pins, file=file_pin(badp)['file'])),
           'ODD pairing')
CONS_BAD2 = CONS.replace('EVEN 6 vs 2', 'EVEN 5 vs 3')
badp2 = os.path.join(WORLD, 'a4_console_bad2.txt')
open(badp2, 'w').write(CONS_BAD2)
loud_probe('A4c the halving lie on the console dies loud (EVEN pin vs the line)',
           lambda: L.load_console_census(badp2, pins=dict(con_pins, file=file_pin(badp2)['file'])),
           'never derived by halving')

# ---------------------------------------------------------------- A5 the regrade census world
print()
print('== A5 THE REGRADE-CENSUS WORLD (the legs cells + the P-B4 constants) ==')
REG = {'legs': {'prose17p-rw17':
                     {'strata': {'cells': {'A': 210, 'B': 363, 'C': 43, 'D': 4}},
                      'parity': {'n_cal': 310, 'n_held': 310, 'n_live': 10, 'n_inert': 0}},
                 'mbpprw17':
                     {'strata': {'cells': {'A': 102, 'B': 237, 'C': 61, 'D': 0}},
                      'parity': {'n_cal': 200, 'n_held': 200, 'n_live': 10, 'n_inert': 0},
                      'pb4_pa1': {'constants': {'tail': [19, 36], 'late': [28, 36],
                                                'support_pairs': 8, 'mask_q_primary': 0.5}}}}}
regp = write_json('a5_regrade.json', REG)
_, rrec = L.load_regrade_export(regp, pins=dict(file=file_pin(regp)['file']))
ok('A5a the legs cells asserted + the pb4 block verified',
   rrec['prose_cells'] == {'A': 210, 'B': 363, 'C': 43, 'D': 4}
   and rrec['code_cells'] == {'A': 102, 'B': 237, 'C': 61, 'D': 0}
   and rrec['pb4'] is not None)
REG_BAD = json.loads(json.dumps(REG))
REG_BAD['legs']['mbpprw17']['pb4_pa1']['constants']['support_pairs'] = 12
badp = write_json('a5_regrade_bad.json', REG_BAD)
loud_probe('A5b the tampered P-B4 constant dies loud',
           lambda: L.load_regrade_export(badp, pins=dict(file=file_pin(badp)['file'])),
           'pb4 constant')
REG_BAD2 = json.loads(json.dumps(REG))
REG_BAD2['legs']['prose17p-rw17']['strata']['cells']['A'] = 211
badp2 = write_json('a5_regrade_bad2.json', REG_BAD2)
loud_probe('A5c the tampered prose cells die loud',
           lambda: L.load_regrade_export(badp2, pins=dict(file=file_pin(badp2)['file'])),
           'prose strata cells')

# ---------------------------------------------------------------- A6 the math pairs world
print()
print('== A6 THE MATH-PAIRS WORLD (the L1 self-pair law counted, never hardcoded) ==')
def build_math(n_pairs=8, self_pair_at=3, dup_self=False, break_half=None):
    pairs = []
    for i in range(1, n_pairs + 1):
        did = str(100 + i)
        val = '7' if i == self_pair_at else str(i)
        nval = '7' if i == self_pair_at else str(100 + i)
        pairs.append({'pair_id': f'FIX-{i:04d}', 'doc_id': did,
                      'positive': {'value': val}, 'negative': {'value': nval}})
    if dup_self:
        pairs[5]['negative']['value'] = pairs[5]['positive']['value']
    walks = {'raw_math_walk': {'docs': []}}
    doc_rows = walks['raw_math_walk']['docs']
    for pr in pairs:
        doc_rows.append({'doc_id': pr['doc_id'],
                         'half': 'calibration' if int(pr['doc_id']) % 2 == 0 else 'held-out'})
    if break_half is not None:
        target = pairs[break_half]['doc_id']
        doc_rows[:] = [r for r in doc_rows if r['doc_id'] != target]
    return {'a2_pairs_complete': pairs, 'a2_pairs_named_incomplete':
            [{'pair_id': 'FIX-9001', 'doc_id': '999', 'status': 'NAMED'}], 'walks': walks}

mx = build_math()
mxp = write_json('a6_math.json', mx)
mrec = L.load_math_pairs(mxp, pins=dict(file=file_pin(mxp)['file'], complete=8, incomplete=1,
                                        l1=1, l1_id='FIX-0003'))
ok('A6a the pair census + the L1 law counted', mrec['complete'] == 8 and mrec['incomplete'] == 1
   and mrec['l1_ids'] == ['FIX-0003'])
mx2 = build_math(dup_self=True)
mx2p = write_json('a6_math_dup.json', mx2)
loud_probe('A6b a second self-pair dies loud (the count is the law)',
           lambda: L.load_math_pairs(mx2p, pins=dict(file=file_pin(mx2p)['file'], complete=8,
                                                    incomplete=1, l1=1, l1_id='FIX-0003')),
           'COUNTED')
mx3 = build_math(break_half=2)
mx3p = write_json('a6_math_nohalf.json', mx3)
loud_probe('A6c an unresolved doc half dies loud (the join integrity gate)',
           lambda: L.load_math_pairs(mx3p, pins=dict(file=file_pin(mx3p)['file'], complete=8,
                                                     incomplete=1, l1=1, l1_id='FIX-0003')),
           'unresolved doc halves')

# ---------------------------------------------------------------- A7 the module pin constants
print()
print('== A7 THE MODULE PIN CONSTANTS (the banked receipts, carried exact) ==')
ok('A7a the code pins', L.POP_CODE_DOCS == 400 and L.POP_CODE_ROWS == 113238
   and L.POP_CODE_EVEN_A == 49 and L.POP_CODE_STRATA == {'A': 102, 'B': 237, 'C': 61, 'D': 0}
   and L.POP_CODE_ONSET == 400 and L.POP_CODE_OTHER == 112838
   and L.POP_CODE_WORK_EMPTY == 400 and L.POP_CODE_MULP_SENTINELS == 0
   and L.POP_CODE_EMISSION_DEF == {'A': 8, 'B': 9, 'C': 1, 'D': 0}
   and L.POP_CODE_EMISSION_RETURN == 49)
ok('A7b the prose pins', L.POP_PROSE_DOCS == 620 and L.POP_PROSE_COMMITS == 260854
   and L.POP_PROSE_STRATA == {'A': 210, 'B': 363, 'C': 43, 'D': 4}
   and L.POP_PROSE_HELD_OUT == [98, 258, 288, 298] and L.POP_PROSE_ODD == (186, 124)
   and L.POP_PROSE_EVEN == (220, 86) and L.POP_PROSE_EMPTY_ODD == [103, 113])
ok('A7c the pooled-arm pins', L.POP_ARM_EVEN_RAW == (65, 23) and L.POP_ARM_POOLED == 88
   and L.POP_ARM_NEG == 23)
ok('A7d the math pins', L.POP_MATH_COMPLETE == 68 and L.POP_MATH_INCOMPLETE == 5
   and L.POP_MATH_L1_SELF_PAIRS == 1 and L.POP_MATH_L1_PAIR_ID == 'A2-0033'
   and L.POP_MATH_VARIANTS == (48, 47, 46, 43) and L.POP_MATH_EVEN_CLEAN == 19
   and L.POP_MATH_ODD_CLEAN == 24)
ok('A7e the P-B4 constants', L.PB4_CONSTANTS == {'tail': [19, 36], 'late': [28, 36],
                                                 'lag': [2, 36], 'support_pairs': 8,
                                                 'mask_q_primary': 0.5})
ok('A7f the file pins of record', L.PIN_CODE_EXPORT[1] == 26209382 and L.PIN_REGRADE_EXPORT[1] == 1375510
   and L.PIN_MATH_EXPORT[1] == 629648 and L.PIN_TJOINT_CONSOLE[1] == 256500)

# ---------------------------------------------------------------- A8 determinism
print()
print('== A8 THE DETERMINISM WORLD (the fixture battery twice, byte-identical) ==')
def battery():
    parts = []
    _, r1 = L.load_code_export(fxp, pins=dict(fx_pins))
    parts.append(repr(sorted(r1.items(), key=lambda kv: str(kv[0]))))
    parts.append(repr(L.extraction_control_code(fx, pins_rows=sum(LENS))))
    parts.append(repr(sorted(L.load_console_census(conp, pins=dict(con_pins)).items(), key=lambda kv: str(kv[0]))))
    parts.append(repr(L.load_math_pairs(mxp, pins=dict(file=file_pin(mxp)['file'], complete=8,
                                                       incomplete=1, l1=1, l1_id='FIX-0003'))))
    return '\n'.join(parts).encode('utf-8')


b1 = battery()
b2 = battery()
ok('A8a the battery run twice byte-identical', b1 == b2,
   f'sha {hashlib.sha256(b1).hexdigest()[:16]}... twice')

print()
print('== PART B: THE REAL-BYTES CONTROL (the four local files of record, counts only, zero readouts) ==')
code_path = os.path.join(BASE, 'wu-read-receipts', 'triadic_wu_code_read_v1.json')
regrade_path = os.path.join(BASE, '.scratch', 'port_eq', 'regrade-v2_export.json')
math_path = os.path.join(BASE, '.scratch', 'owner_see_everything_v1.json')
console_path = os.path.join(BASE, '.scratch', 'tjoint_read_v2_console.txt')
missing = [p for p in (code_path, regrade_path, math_path, console_path) if not os.path.exists(p)]
if missing:
    print(f'  [real-bytes control] SKIPPED, named honestly: absent files {missing}')
    FAIL += 1
else:
    print('  [real-bytes control] B1 the code export of record:')
    d_real, rec_real = L.load_code_export(code_path)
    ok('B1a every code pin exact (counted from the bytes)',
       rec_real['docs'] == 400 and rec_real['rows'] == 113238 and rec_real['even_a'] == 49
       and rec_real['onset'] == 400 and rec_real['other'] == 112838
       and rec_real['work_empty'] == 400
       and rec_real['strata'] == {'A': 102, 'B': 237, 'C': 61, 'D': 0})
    ok('B1b the survival cohorts 49 / 49 / 49 (zero censoring at the interior horizons, '
       'every even-A doc reaches 128)',
       rec_real['cohorts'] == {36: (49, 0), 64: (49, 0), 128: (49, 0)})
    print('  [real-bytes control] B2 the extraction sweep over the real export:')
    ctl_real = L.extraction_control_code(d_real, pins_rows=113238)
    ok('B2a the real sweep counts exact, values discarded',
       ctl_real['docs'] == 400 and ctl_real['rows_total'] == 113238
       and ctl_real['reach'] == {36: 400, 64: 400, 128: 400}
       and ctl_real['len_min'] == 166 and ctl_real['len_max'] == 502)
    print('  [real-bytes control] B3 the regrade export of record:')
    _, rrec_real = L.load_regrade_export(regrade_path)
    ok('B3a the regrade cells + parity + pb4 constants exact',
       rrec_real['prose_cells'] == {'A': 210, 'B': 363, 'C': 43, 'D': 4}
       and rrec_real['code_cells'] == {'A': 102, 'B': 237, 'C': 61, 'D': 0}
       and rrec_real['pb4'] is not None)
    print('  [real-bytes control] B4 the math pair export of record:')
    mrec_real = L.load_math_pairs(math_path)
    ok('B4a the math pair census exact (68 / 5 / the L1 law counted 1 = A2-0033)',
       mrec_real['complete'] == 68 and mrec_real['incomplete'] == 5
       and mrec_real['l1_ids'] == ['A2-0033'])
    print('  [real-bytes control] B5 the console of record:')
    cc_real = L.load_console_census(console_path)
    ok('B5a the 616 census line + the pooled-arm line read exact',
       cc_real['docs'] == 620 and cc_real['commits'] == 260854
       and cc_real['odd'] == (186, 124) and cc_real['even'] == (220, 86)
       and cc_real['arm'] == (65, 23))
    print('  [real-bytes control] every pin exact, every count from the bytes, '
          'ZERO READOUTS COMPUTED, every value discarded -- the owner\'s run proves the same '
          'gates on his machine')

# ---------------------------------------------------------------- the totals
print()
print(f'THE SMOKE TOTALS: PASS {PASS} | FAIL {FAIL}')
if FAIL:
    print('THE SMOKE FAILED LOUD -- the loaders or a fixture must be fixed before any bank')
    sys.exit(1)
print('THE SMOKE ALL GREEN -- the loaders layer stands for build message 3 of 3 '
      '(the assembled instrument + the full acceptance + the published bundle)')
sys.exit(0)

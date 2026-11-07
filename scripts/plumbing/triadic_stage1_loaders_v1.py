"""
THE STAGE-1 CACHE LOADERS v1.0  --  build message 2 of 3
(the Stage-1 forward-pass accumulator instrument, the loaders layer)

Built under the pinned sheet stage1-accumulator-preregistration.md
(SHA-256 e9472bb32ad6405b10c7e752453301bec3b523668488fda249cc2209edb1b8ec,
pinned at item 1309). Every cache pin asserted at load, fail-loud, with
BYTE-COUNT-BEFORE-HASH on every pinned file (the house law). Every
population pin COUNTED from the loaded bytes -- never derived by
halving (the item-1306 correction, the law of the sheet). The census
guards print the survival cohorts at every grid horizon with the
at-most-49 law asserted. The extraction control touches real bytes for
STRUCTURAL RECEIPTS ONLY: counts and lengths, every value DISCARDED,
never printed, never read out (my-hardware law; the readout
itself runs on my side at my single run).

The -r2 thins ride the portability law verbatim (the Track C form):
their sha PRINTED at load, riding beside the asserted pins -- they are
my-side files; the instrument prints what it loads on my machine.

House laws riding this module: findings presented never adjudicated;
nothing wires, nothing actuates; the disarmament law rides.
"""

import os
import json
import hashlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triadic_stage1_engines_v1 as E


class LoudFail(Exception):
    """The fail-loud gate: any pin or census mismatch stops the load with a named line."""
    pass


def loud(label, detail):
    raise LoudFail(f'LOADER GATE FAILED -- {label}: {detail}')


# ---------------------------------------------------------------- the pinned files of record
# label: (filename, expected bytes, expected sha-256)
PIN_CODE_EXPORT = ('triadic_wu_code_read_v1.json',
                   26209382,
                   '610d48c9689c07c7859fd84fadfe14fdb7259bb8eb572da4e0b9d1ef025db689')
PIN_REGRADE_EXPORT = ('regrade-v2_export.json',
                      1375510,
                      '5cc229c827468740ede543242742416043cf67bdf6e1dd596d5983eba4261018')
PIN_MATH_EXPORT = ('owner_see_everything_v1.json',
                   629648,
                   '1d2d5f5f25e30e0d8b35cb1232c9038527476a8f046d34f5292877faa72e8252')
PIN_TJOINT_CONSOLE = ('tjoint_read_v2_console.txt',
                      256500,
                      'fd8842e4c38e9c01570acd8527907dc9ec488564261738f11de0511b3286d2f2')

# ---------------------------------------------------------------- the population pins (COUNTED, never derived)
POP_CODE_DOCS = 400
POP_CODE_ROWS = 113238
POP_CODE_STRATA = {'A': 102, 'B': 237, 'C': 61, 'D': 0}
POP_CODE_EVEN_A = 49                 # the prefix standardization population at the full doc
POP_CODE_EVEN_TOTAL = 200            # calibration == EVEN (the export's own half law, item 1262)
POP_CODE_ONSET = 400
POP_CODE_OTHER = 112838
POP_CODE_WORK_EMPTY = 400            # the ONSET anchor rows, named-absent never zero-filled
POP_CODE_MULP_SENTINELS = 0
POP_CODE_EMISSION_DEF = {'A': 8, 'B': 9, 'C': 1, 'D': 0}
POP_CODE_EMISSION_RETURN = 49
POP_PROSE_DOCS = 620
POP_PROSE_COMMITS = 260854
POP_PROSE_STRATA = {'A': 210, 'B': 363, 'C': 43, 'D': 4}
POP_PROSE_HELD_OUT = [98, 258, 288, 298]
POP_PROSE_ODD = (186, 124)           # the strictly-odd pairing population
POP_PROSE_EVEN = (220, 86)           # the even standardization populations (pooled B+C vs A)
POP_PROSE_EMPTY_ODD = [103, 113]     # the 2 odd-side empty rows, drop-with-receipt
POP_ARM_EVEN_RAW = (65, 23)          # the console's own selection receipt line
POP_ARM_POOLED = 88                  # the pooled even form (65 + 23, the pooled-census law)
POP_ARM_NEG = 23                     # the NEG form, the thin baseline named
POP_MATH_COMPLETE = 68
POP_MATH_INCOMPLETE = 5
POP_MATH_L1_SELF_PAIRS = 1           # counted by the L1 law (same value string or decimal-equal)
POP_MATH_L1_PAIR_ID = 'A2-0033'      # the banked receipt of the counted law
POP_MATH_VARIANTS = (48, 47, 46, 43)  # the banked item-1197 variant receipts, printed at load
POP_MATH_EVEN_CLEAN = 19             # the even-doc clean witnesses (the 43-pair full law)
POP_MATH_ODD_CLEAN = 24              # the odd-doc clean witnesses
PB4_CONSTANTS = {'tail': [19, 36], 'late': [28, 36], 'lag': [2, 36],
                 'support_pairs': 8, 'mask_q_primary': 0.5}

# ---------------------------------------------------------------- the pin machinery
def pin_file(path, expect_bytes, expect_sha, label):
    """BYTE-COUNT-BEFORE-HASH, then the sha assert, both fail-loud. Returns the raw bytes."""
    if not os.path.exists(path):
        loud(label, f'absent file at {path}')
    n = os.path.getsize(path)
    if n != expect_bytes:
        loud(label, f'byte count {n} != pinned {expect_bytes} (byte-count-before-hash, the load stops before any hash)')
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    got = h.hexdigest()
    if got != expect_sha:
        loud(label, f'sha {got} != pinned {expect_sha}')
    with open(path, 'rb') as f:
        return f.read()


def load_thin_printed(path, label='the -r2 thin of record'):
    """The portability law verbatim (the Track C form): the thin's sha PRINTED at load,
    riding beside the asserted pins; the record count censused loud. Returns the count."""
    if not os.path.exists(path):
        loud(label, f'absent file at {path}')
    h = hashlib.sha256()
    n = 0
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
            n += chunk.count(b'\n')
    got = h.hexdigest()
    print(f'  [load] {label}: {os.path.basename(path)} -- sha256 {got} PRINTED AT LOAD '
          f'(the portability law, riding beside the asserted pins) | {n} records censused')
    return {'sha_printed': got, 'records': n}


# ---------------------------------------------------------------- the code export loader
def load_code_export(path, pins=None):
    """The code-leg export of record: pin asserted, then every census gate COUNTED from the
    parsed bytes and asserted against the population pins. Returns the parsed export plus
    the receipts dict. The survival cohorts print at every grid horizon with the at-most-49
    law asserted. NO VALUES EMITTED: the receipts carry counts only."""
    p = dict(docs=POP_CODE_DOCS, rows=POP_CODE_ROWS, strata=POP_CODE_STRATA,
             even_a=POP_CODE_EVEN_A, even_total=POP_CODE_EVEN_TOTAL,
             onset=POP_CODE_ONSET, other=POP_CODE_OTHER,
             work_empty=POP_CODE_WORK_EMPTY, mulp_sentinels=POP_CODE_MULP_SENTINELS,
             emission_def=POP_CODE_EMISSION_DEF, emission_return=POP_CODE_EMISSION_RETURN)
    p.update(pins or {})
    fp = p.pop('file', PIN_CODE_EXPORT)
    raw = pin_file(path, fp[1], fp[2], 'the code export of record')
    d = json.loads(raw)
    rd = d.get('rows_by_doc')
    if not isinstance(rd, dict) or len(rd) != p['docs']:
        loud('code census', f'docs {len(rd) if isinstance(rd, dict) else type(rd)} != pinned {p["docs"]}')
    # the row census counted from the bytes themselves, never trusted from the header
    n_rows = 0
    onset = 0
    other = 0
    work_empty = 0
    mulp_live = 0
    lens = {}
    for doc_id, cols in rd.items():
        ci = cols.get('commit_index')
        if not isinstance(ci, list) or not ci:
            loud('code census', f'doc {doc_id} carries no commit_index lane')
        n_rows += len(ci)
        lens[doc_id] = len(ci)
        roles = cols.get('role')
        if not isinstance(roles, list) or len(roles) != len(ci):
            loud('code census', f'doc {doc_id} role lane length mismatch')
        for r in roles:
            if r == 'STATEMENT-ONSET':
                onset += 1
            else:
                other += 1
        wi = cols.get('work_inc')
        if not isinstance(wi, list) or len(wi) != len(ci):
            loud('code census', f'doc {doc_id} work_inc lane length mismatch')
        for v in wi:
            if v is None:
                work_empty += 1
        mu = cols.get('m_ulp_content')
        if not isinstance(mu, list) or len(mu) != len(ci):
            loud('code census', f'doc {doc_id} m_ulp lane length mismatch')
        for v in mu:
            if v is not None:
                mulp_live += 1
    if n_rows != p['rows']:
        loud('code census', f'rows {n_rows} != pinned {p["rows"]}')
    if onset != p['onset'] or other != p['other']:
        loud('code census', f'role census onset {onset}/other {other} != pinned {p["onset"]}/{p["other"]}')
    if work_empty != p['work_empty']:
        loud('code census', f'work_inc empty windows {work_empty} != pinned {p["work_empty"]}')
    if mulp_live != p['rows'] - p['mulp_sentinels']:
        loud('code census', f'm_ulp live rows {mulp_live} != pinned {p["rows"] - p["mulp_sentinels"]}')
    # the strata cells counted from the walk table (the join's own strata source)
    wt = d.get('doc_walk_table')
    if not isinstance(wt, list):
        loud('code census', 'doc_walk_table absent')
    counted = {}
    even_total = 0
    even_a_ids = set()
    for r in wt:
        st = r.get('stratum')
        counted[st] = counted.get(st, 0) + 1
        if r.get('half') == 'calibration':       # calibration == EVEN, the export's own half law
            even_total += 1
            if st == 'A':
                even_a_ids.add(str(r.get('doc_id')))
    strata = {st: counted.get(st, 0) for st in ('A', 'B', 'C', 'D')}  # absent cells normalize to zero
    if strata != p['strata']:
        loud('code census', f'strata cells {strata} != pinned {p["strata"]}')
    if even_total != p['even_total']:
        loud('code census', f'even (calibration) total {even_total} != pinned {p["even_total"]}')
    if len(even_a_ids) != p['even_a']:
        loud('code census', f'even-A COUNTED {len(even_a_ids)} != pinned {p["even_a"]} '
                            f'(counted from the halves, never derived by halving)')
    # the emission census
    cen = d.get('census', {}).get('emission', {})
    if cen.get('def_by_stratum') != p['emission_def'] or cen.get('return_docs') != p['emission_return']:
        loud('code census', f'emission census {cen} != the pinned def/return receipts')
    # the survival cohorts at every grid horizon, the census guards loud
    ea_lengths = {i: lens[i] for i in even_a_ids if i in lens}
    if len(ea_lengths) != len(even_a_ids):
        loud('code census', 'an even-A doc absent from rows_by_doc (the join broke)')
    cohorts = {}
    for h in E.GRID:
        sc = E.survival_cohort(ea_lengths, h)
        if sc['n_live'] > p['even_a']:
            loud('code census', f'survival cohort at {h}: {sc["n_live"]} live exceeds the population {p["even_a"]}')
        cohorts[h] = sc
        print(f'  [census guard] horizon {h}: live {sc["n_live"]} / censored {sc["n_censored"]} '
              f'| guard {sc["guard"]} | thin {sc["thin"]} (the at-most-{p["even_a"]} law held)')
    receipts = {'docs': len(rd), 'rows': n_rows, 'onset': onset, 'other': other,
                'work_empty': work_empty, 'even_a': len(even_a_ids),
                'strata': strata, 'cohorts': {h: (c['n_live'], c['n_censored'])
                                              for h, c in cohorts.items()}}
    print(f'  [load] the code export of record: every pin exact -- docs {len(rd)} / rows {n_rows} / '
          f'even-A {len(even_a_ids)} counted / strata {strata}')
    return d, receipts


def extraction_control_code(export, pins_rows=None):
    """THE REAL-BYTES EXTRACTION CONTROL (my-hardware law): iterates every doc and
    row for STRUCTURAL RECEIPTS ONLY -- per-doc commit counts, length-vs-walk-table checks,
    the horizon reach census -- then DISCARDS every value. Nothing value-bearing is returned
    or printed: the returned receipt carries ints and counts only, and the row references
    are dropped on return (the values never leave this function)."""
    rd = export['rows_by_doc']
    wt = {str(r.get('doc_id')): r for r in export.get('doc_walk_table', [])}
    expect_rows = pins_rows
    per_doc = {}
    reach = {h: 0 for h in E.GRID}
    total = 0
    for doc_id, cols in rd.items():
        n = len(cols.get('commit_index', []))
        per_doc[doc_id] = n
        total += n
        walk_row = wt.get(str(doc_id))
        if walk_row is not None:
            nc = walk_row.get('n_commits')
            if str(nc) != str(n):
                loud('extraction control', f'doc {doc_id}: rows {n} vs walk-table n_commits {nc}')
        for h in E.GRID:
            if n >= h:
                reach[h] += 1
    if expect_rows is not None and total != expect_rows:
        loud('extraction control', f'row total {total} != pinned {expect_rows}')
    # the values are never emitted: the caller receives counts only, and cols/rd go out of scope here
    receipt = {'docs': len(per_doc), 'rows_total': total,
               'reach': dict(reach),
               'len_min': min(per_doc.values()), 'len_max': max(per_doc.values())}
    print(f'  [extraction control] {receipt["docs"]} docs swept / {receipt["rows_total"]} rows counted / '
          f'reach at the horizons {dict(reach)} -- VALUES DISCARDED, counts only, zero readouts')
    return receipt


# ---------------------------------------------------------------- the regrade export loader
def load_regrade_export(path, pins=None):
    """The P-B4 walk-revisit export of record: pin asserted; the legs' strata cells counted
    and asserted (the prose cells carrying the 2 empty odd-side rows, docs 103 / 113, the
    drop-with-receipt law riding as the pinned receipt); the parity blocks asserted; the
    P-B4 constants block verified against the banked constants."""
    p = dict(prose_strata=POP_PROSE_STRATA, prose_parity={'n_cal': 310, 'n_held': 310, 'n_live': 10, 'n_inert': 0},
             code_strata=POP_CODE_STRATA, code_parity={'n_cal': 200, 'n_held': 200, 'n_live': 10, 'n_inert': 0})
    p.update(pins or {})
    fp = p.pop('file', PIN_REGRADE_EXPORT)
    raw = pin_file(path, fp[1], fp[2], 'the regrade export of record')
    d = json.loads(raw)
    legs = d.get('legs')
    if not isinstance(legs, dict):
        loud('regrade census', 'the legs block absent')
    if 'prose17p-rw17' not in legs or 'mbpprw17' not in legs:
        loud('regrade census', f'the two census legs absent: {list(legs)}')
    prose_cells = legs['prose17p-rw17'].get('strata', {}).get('cells')
    code_cells = legs['mbpprw17'].get('strata', {}).get('cells')
    if prose_cells != p['prose_strata']:
        loud('regrade census', f'prose strata cells {prose_cells} != pinned {p["prose_strata"]}')
    if code_cells != p['code_strata']:
        loud('regrade census', f'code strata cells {code_cells} != pinned {p["code_strata"]}')
    prose_parity = legs['prose17p-rw17'].get('parity')
    code_parity = legs['mbpprw17'].get('parity')
    if prose_parity != p['prose_parity']:
        loud('regrade census', f'prose parity {prose_parity} != pinned {p["prose_parity"]}')
    if code_parity != p['code_parity']:
        loud('regrade census', f'code parity {code_parity} != pinned {p["code_parity"]}')
    print(f'  [load] the regrade export of record: pin exact | prose cells {prose_cells} '
          f'(the A side 208 OK + 2 EMPTY odd-side, docs {POP_PROSE_EMPTY_ODD}, drop-with-receipt) '
          f'| code cells {code_cells} (zero EMPTY)')
    # the P-B4 constants block: the export carries tail / late / support_pairs /
    # mask_q_primary at legs.<leg>.pb4_pa1.constants; the lag window rides the banked
    # console line, printed beside (never re-derived from the export)
    pb4 = None
    for leg in d.get('legs', {}).values():
        if isinstance(leg, dict) and isinstance(leg.get('pb4_pa1'), dict):
            c = leg['pb4_pa1'].get('constants')
            if isinstance(c, dict):
                pb4 = c
                break
    if pb4 is None:
        loud('regrade census', 'the pb4 constants block absent')
    for k2 in ('tail', 'late', 'support_pairs', 'mask_q_primary'):
        if pb4.get(k2) != PB4_CONSTANTS[k2]:
            loud('regrade census', f'pb4 constant {k2}: {pb4.get(k2)} != banked {PB4_CONSTANTS[k2]}')
    print(f'  [load] the P-B4 constants block verified against the banked constants '
          f'{{tail {pb4["tail"]}, late {pb4["late"]}, support_pairs {pb4["support_pairs"]}, '
          f'mask_q_primary {pb4["mask_q_primary"]}}} | the lag window {PB4_CONSTANTS["lag"]} '
          f'rides the banked console line, printed beside')
    return d, {'prose_cells': prose_cells, 'code_cells': code_cells, 'pb4': pb4}


# ---------------------------------------------------------------- the math pairs loader
def load_math_pairs(path, pins=None):
    """The math-leg pair source of record (the see-everything export): pin asserted; the
    complete/incomplete pair census counted; every complete pair's doc half resolved in the
    walk tables (the join integrity gate); the L1 self-pair law COUNTED (a pair whose
    positive and negative bind the same clean value -- identical value string, or
    decimal-equal -- the item-1196 law, never hardcoded); the banked variant receipts
    (48 / 47 / 46 / 43, even clean 19 / odd 24) PRINTED at load as the item-1197 receipts.
    The variant-frame construction itself rides message 3's extraction (the L2 rendering
    law). NO pair values emitted: the receipt carries counts and pair ids only."""
    p = dict(complete=POP_MATH_COMPLETE, incomplete=POP_MATH_INCOMPLETE,
             l1=POP_MATH_L1_SELF_PAIRS, l1_id=POP_MATH_L1_PAIR_ID)
    p.update(pins or {})
    fp = p.pop('file', PIN_MATH_EXPORT)
    raw = pin_file(path, fp[1], fp[2], 'the math pair export of record')
    d = json.loads(raw)
    complete = d.get('a2_pairs_complete')
    incomplete = d.get('a2_pairs_named_incomplete')
    if not isinstance(complete, list) or len(complete) != p['complete']:
        loud('math census', f'complete pairs {len(complete) if isinstance(complete, list) else "?"} != pinned {p["complete"]}')
    if not isinstance(incomplete, list) or len(incomplete) != p['incomplete']:
        loud('math census', f'incomplete pairs {len(incomplete) if isinstance(incomplete, list) else "?"} != pinned {p["incomplete"]}')
    # the join integrity gate: every complete pair's doc half resolvable in the walk tables
    walks = d.get('walks', {})
    half_by_doc = {}
    for wk, wv in walks.items():
        rows = None
        if isinstance(wv, dict):
            rows = wv.get('docs')
        elif isinstance(wv, list):
            rows = wv
        if isinstance(rows, list):
            for r in rows:
                if isinstance(r, dict) and 'half' in r:
                    half_by_doc[str(r.get('doc_id'))] = r['half']
    unresolved = []
    l1_ids = []
    for pr in complete:
        did = str(pr.get('doc_id'))
        if did not in half_by_doc:
            unresolved.append(pr.get('pair_id'))
        pos, neg = pr.get('positive'), pr.get('negative')
        a, b = str(pos.get('value')), str(neg.get('value'))
        same = (a == b)
        if not same:
            try:
                same = (float(a) == float(b))
            except (ValueError, TypeError):
                same = False
        if same:
            l1_ids.append(pr.get('pair_id'))
    if unresolved:
        loud('math census', f'pairs with unresolved doc halves: {unresolved}')
    if len(l1_ids) != p['l1'] or (p['l1_id'] not in l1_ids):
        loud('math census', f'L1 self-pairs COUNTED {l1_ids} != the pinned receipt '
                            f'[{p["l1_id"]}] (counted by the law, never hardcoded)')
    print(f'  [load] the math pair export of record: pin exact | complete {len(complete)} / '
          f'incomplete {len(incomplete)} / L1 self-pairs counted {len(l1_ids)} = {l1_ids}')
    print(f'  [load] the banked item-1197 variant receipts printed at load: '
          f'variants {POP_MATH_VARIANTS} (48 the banked frame; 47 L1; 46 the audit selective '
          f'variant, flagged; 43 the L1+L2 full law) | even clean {POP_MATH_EVEN_CLEAN} / '
          f'odd clean {POP_MATH_ODD_CLEAN} -- the variant-frame construction rides message 3')
    return {'complete': len(complete), 'incomplete': len(incomplete),
            'l1_ids': l1_ids, 'variant_receipts': POP_MATH_VARIANTS,
            'even_clean': POP_MATH_EVEN_CLEAN, 'odd_clean': POP_MATH_ODD_CLEAN}


# ---------------------------------------------------------------- the console census loader
def load_console_census(path, pins=None):
    """The population pins READ from the console of record (the sheet's law: read from the
    consoles and exports, never derived by halving): the 616 census line and the pooled-arm
    selection receipt line, parsed and asserted against the pinned receipts."""
    p = dict(docs=POP_PROSE_DOCS, commits=POP_PROSE_COMMITS, strata=POP_PROSE_STRATA,
             held_out=POP_PROSE_HELD_OUT, odd=POP_PROSE_ODD, even=POP_PROSE_EVEN,
             arm_raw=POP_ARM_EVEN_RAW, arm_pooled=POP_ARM_POOLED, arm_neg=POP_ARM_NEG)
    p.update(pins or {})
    fp = p.pop('file', PIN_TJOINT_CONSOLE)
    raw = pin_file(path, fp[1], fp[2],
                   'the console of record (the census line source)')
    text = raw.decode('utf-8')
    line = None
    arm_line = None
    import re
    pat = re.compile(r'GATE census:\s*([\d,]+) docs / ([\d,]+) commits \| B (\d+)/C (\d+)/A (\d+)/D (\d+) '
                     r'\(held out \[(\d+), (\d+), (\d+), (\d+)\]\) \| (\d+) ODD (\d+) vs (\d+), '
                     r'EVEN (\d+) vs (\d+)')
    for ln in text.splitlines():
        if line is None and 'ODD' in ln and pat.search(ln):
            line = ln
        if 'prose doc selection receipt' in ln:
            arm_line = ln
    if line is None:
        loud('console census', 'the 616 census line not found (or does not parse) in the console of record')
    if arm_line is None:
        loud('console census', 'the pooled-arm selection receipt line not found')
    m = pat.search(line)
    if not m:
        loud('console census', f'the census line does not parse: {line!r}')
    g = [int(x.replace(',', '')) for x in m.groups()]
    if g[0] != p['docs'] or g[1] != p['commits']:
        loud('console census', f'docs/commits {g[0]}/{g[1]} != pinned {p["docs"]}/{p["commits"]}')
    strata = {'A': g[4], 'B': g[2], 'C': g[3], 'D': g[5]}
    if strata != p['strata']:
        loud('console census', f'strata {strata} != pinned {p["strata"]}')
    if g[6:10] != p['held_out']:
        loud('console census', f'held-out {g[6:10]} != pinned {p["held_out"]}')
    odd = (g[11], g[12])
    even = (g[13], g[14])
    if odd != p['odd']:
        loud('console census', f'ODD pairing {odd} != pinned {p["odd"]}')
    if even != p['even']:
        loud('console census', f'EVEN populations {even} != pinned {p["even"]} '
                               f'(the even NEG 86 the standardization pin, never derived by halving)')
    m2 = re.search(r'EVEN row-docs (\d+) vs (\d+), raw', arm_line)
    if not m2:
        loud('console census', f'the arm selection line does not parse: {arm_line!r}')
    arm = (int(m2.group(1)), int(m2.group(2)))
    if arm != p['arm_raw']:
        loud('console census', f'arm selection {arm} != pinned {p["arm_raw"]}')
    if arm[0] + arm[1] != p['arm_pooled'] or arm[1] != p['arm_neg']:
        loud('console census', f'arm pooled {arm[0] + arm[1]} / NEG {arm[1]} != '
                               f'pinned {p["arm_pooled"]}/{p["arm_neg"]}')
    print(f'  [load] the console of record: pin exact -- the 616 census line READ and asserted '
          f'(docs {g[0]} / commits {g[1]} | ODD {odd} | EVEN {even}) | the pooled-arm selection '
          f'{arm} -> pooled {p["arm_pooled"]} / NEG {p["arm_neg"]} (the thin baseline named)')
    return {'docs': g[0], 'commits': g[1], 'strata': strata, 'odd': odd, 'even': even, 'arm': arm}

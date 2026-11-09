"""
THE STAGE-1 READOUT ENGINES v1.0  --  build message 1 of 3
(the Stage-1 forward-pass accumulator instrument, the engines layer)

Built under the pinned sheet stage1-accumulator-preregistration.md
(SHA-256 e9472bb32ad6405b10c7e752453301bec3b523668488fda249cc2209edb1b8ec,
pinned at the banked sheet). This module is PURE: zero real rows touched, zero
file I/O, zero leg-specific extraction (that is build message 2 of 3).
The banked conventions of the tool of record (trackc_read_v122.py) are
ported CHARACTER-FOR-CHARACTER: the pooled SMD both forms, the midrank
AUC, the record-lane cut (NEG mean + 2 sd), the negative-side glass
scale with its 5e-4 identity gate, and the under-5 population guard.

House laws riding this module:
- Both trip bars PRINTED side-by-side everywhere, never adjudicated
  in-tool; the operating trip-line sub-slot stays the owner's open
  ruling (the pinned sheet, section 1).
- Zero constants tuned: the grid, the thin-baseline line, the
  population guard, and the maturity rosters are the banked laws of
  the sheet and the tool of record, nothing new.
- Findings presented, never adjudicated; the disarmament law rides
  (nothing here wires or actuates anything).

Leg names in plain English (the house rule): the math leg, the prose
leg, the code leg. Coordinate names are the banked short names of the
eight-coordinate code-leg form (spelled out owner-facing in the ledger).
"""

import math

# ---------------------------------------------------------------- the pinned constants
TRIP_BAR_RECORD = [REDACTED_PER_PUBLICATION_POLICY]     # the record-lane cut: NEG mean + [REDACTED_PER_PUBLICATION_POLICY] * NEG pop sd (the tool of record's own cut)
TRIP_BAR_TIERC = [REDACTED_PER_PUBLICATION_POLICY]   # the Tier C exit datum -- carried unmoved, printed beside
TRIP_BARS = (TRIP_BAR_RECORD, TRIP_BAR_TIERC)  # both, side-by-side, every table (his Call-1 stamp)
GRID = (36, 64, 128)      # the interior checkpoint horizons (36 = the probe-B4 lock; 64 / 128 = the banked window cells)
MIN_N = 30                # the thin-baseline flag line (the bucket-fallback kin)
POP_GUARD_N = 5           # the population guard: below this a read is INCONCLUSIVE
IDENT_TOL = 5e-4          # the glass identity tolerance, the tool of record's own


def identity_trip(label, glass, ident):
    """The loud fail of the glass identity gate (never a silent zero)."""
    raise RuntimeError(
        f'ENGINE IDENTITY GATE FAILED on {label}: glass {glass:.6f} vs identity {ident:.6f}')


# ------------------------------------------------- the banked conventions, ported verbatim
def mean_sd_n1(v):
    m = sum(v) / len(v)
    return m, math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def mean_sd_0(v):
    m = sum(v) / len(v)
    return m, math.sqrt(sum((x - m) ** 2 for x in v) / len(v))


def smd_pop(xs, ys):
    mx, sx = mean_sd_0(xs)
    my, sy = mean_sd_0(ys)
    pool = math.sqrt((sx * sx + sy * sy) / 2)
    return (mx - my) / pool if pool else 0.0


def smd_n1(xs, ys):
    mx, sx = mean_sd_n1(xs)
    my, sy = mean_sd_n1(ys)
    pool = math.sqrt((sx * sx + sy * sy) / 2)
    return (mx - my) / pool if pool else 0.0


def midrank_auc(xs, ys):
    nx, ny = len(xs), len(ys)
    allv = sorted([(x, 1) for x in xs] + [(y, 0) for y in ys], key=lambda z: z[0])
    ranks = [0.0] * len(allv)
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
            j += 1
        rr = (i + j) / 2 + 1
        for k2 in range(i, j + 1):
            ranks[k2] = rr
        i = j + 1
    sp = sum(ranks[k2] for k2, (v, lab) in enumerate(allv) if lab == 1)
    return (sp - nx * (nx + 1) / 2) / (nx * ny)


def tail_share(xs, cut):
    """The share of a side's values strictly above the cut (the tool's own tail convention)."""
    return sum(1 for x in xs if x > cut) / len(xs)


# ------------------------------------------------- the readout line (both bars, printed never adjudicated)
def readout_line(label, xs, ys):
    """The banked readout body, extended per the pinned sheet: the tails computed and
    printed at BOTH trip bars side-by-side. Returns the full dict, or None under the
    population guard (the guard line printed, reported)."""
    if len(xs) < POP_GUARD_N or len(ys) < POP_GUARD_N:
        print(f'  {label}: INCONCLUSIVE-POPULATION-GUARD (n {len(xs)} vs {len(ys)}), reported')
        return None
    d0 = smd_pop(xs, ys)
    d1 = smd_n1(xs, ys)
    auc = midrank_auc(xs, ys)
    mx, sx = mean_sd_0(xs)
    my, sy = mean_sd_0(ys)
    glass = (mx - my) / sy if sy else float('nan')
    sr = sx / sy if sy else float('nan')
    ident = d0 * math.sqrt((sr * sr + 1) / 2)
    if abs(glass - ident) > IDENT_TOL:
        identity_trip(label, glass, ident)
    bar_rows = []
    for b in TRIP_BARS:
        cut = my + b * sy
        bar_rows.append({
            'bar': b, 'cut': cut,
            'pos_tail': tail_share(xs, cut), 'neg_tail': tail_share(ys, cut),
            'smd_pop_minus_bar': d0 - b})
    out = {'label': label, 'n_pos': len(xs), 'n_neg': len(ys),
           'smd_pop': d0, 'smd_n1': d1, 'auc': auc, 'glass_neg': glass,
           'identity': ident, 'mx': mx, 'sx': sx, 'my': my, 'sy': sy,
           'bars': bar_rows}
    print(f'  {label}: POS n {len(xs)} | NEG n {len(ys)} | SMD pop {d0:+.4f} n-1 {d1:+.4f} | '
          f'AUC {auc:.4f} | Glass delta_NEG {glass:+.4f} (identity {ident:+.4f} held at 5e-4)')
    for r in bar_rows:
        print(f'    bar {r["bar"]:.4f}: cut {r["cut"]:+.4f} | POS tail {r["pos_tail"]:.4f} | '
              f'NEG tail {r["neg_tail"]:.4f} | SMD pop minus bar {r["smd_pop_minus_bar"]:+.4f} '
              f'-- printed, never adjudicated in-tool')
    return out


# ------------------------------------------------- the checkpoint-grid laws (the pinned sheet, section 2)
def survival_cohort(lengths, n):
    """The uncensored cohort at horizon n: the docs whose commit count reaches n.
    The census prints loud: the live count, the censored count, the guard, the thin flag."""
    live = {d: N for d, N in lengths.items() if N >= n}
    n_live = len(live)
    return {'live': live, 'n_live': n_live, 'n_censored': len(lengths) - n_live,
            'guard': n_live < POP_GUARD_N, 'thin': 0 < n_live < MIN_N}


def grid_reached(N):
    """The interior grid looks a doc of N commits takes: the horizons STRICTLY below N
    (a doc closing exactly at a horizon takes that horizon as its single close look,
    never as two looks -- the K-law of the pinned sheet, section 4)."""
    return tuple(h for h in GRID if h < N)


def k_look_count(N):
    """The total look count at the doc close: the interior looks + the single close look."""
    return 1 + len(grid_reached(N))


# ------------------------------------------------- the empirical prefix standardization (section 3)
def standardize_population(values):
    """The empirical prefix moments of one coordinate at one horizon: MEASURED on the
    given per-doc values (the survival cohort's values at the cut, truncated and
    censused by the caller), never modeled, zero parametric forms. Pop sd is the
    primary scale (the readout's own glass convention); the n-1 form carried beside."""
    n = len(values)
    mu, sd_pop = mean_sd_0(values)
    _, sd_n1 = mean_sd_n1(values)
    return {'n': n, 'mu': mu, 'sd_pop': sd_pop, 'sd_n1': sd_n1,
            'guard': n < POP_GUARD_N, 'thin': n < MIN_N}


def z_pop(x, moments):
    """The prefix-standardized value on the pop scale; None loud if the sd degenerates."""
    if not moments['sd_pop']:
        return None
    return (x - moments['mu']) / moments['sd_pop']


# ------------------------------------------------- the censoring-conditioned envelope (section 4)
def trajectory_peaks(traj):
    """The running cumulative peak path of a trajectory (the per-stage maxima, in order)."""
    peaks = []
    best = None
    for t in traj:
        best = t if best is None or t > best else best
        peaks.append(best)
    return peaks


def final_peak(traj):
    """The trajectory's cumulative peak over all reached looks."""
    return max(traj) if traj else None


def envelope_standardize(peak, mu_sup, sd_sup):
    """The envelope standardization of a cumulative peak against the survival-cohort
    even baseline at the stage; None loud if the baseline sd degenerates (the caller
    prints the inconclusive line, never a silent zero)."""
    if not sd_sup:
        return None
    return (peak - mu_sup) / sd_sup


# ------------------------------------------------- the two deltas (printed separately, every table)
def pop_drift_delta(neg_tail_odd_single, neg_tail_even_single):
    """The even-to-odd single-horizon population drift at a fixed horizon (never the
    multiplicity delta -- the two mechanisms never conflated, the pinned sheet section 4)."""
    return neg_tail_odd_single - neg_tail_even_single


def seq_mult_delta(neg_tail_odd_running_max, neg_tail_odd_close):
    """The within-doc sequential-looks multiplicity on the odd half: the running-max
    NEG tail minus the single close-read NEG tail, before and after the envelope."""
    return neg_tail_odd_running_max - neg_tail_odd_close


# ------------------------------------------------- the math unpaired point fold (section 5)
def math_fold_moments(witness_rows, signs):
    """The six-operator fold's negative moments locked on the even-numbered clean witnesses only.
    Per-operator pop moments + the equal-weight signed composite's pop moments (the
    glass scale of the readout convention). Directions pinned a priori by the caller
    (the banked machinery directions owner-side), zero direction shopping here.
    Returns None loud on any degenerate column or degenerate composite."""
    k = len(signs)
    if not witness_rows or any(len(r) != k for r in witness_rows):
        return None
    mus, sds = [], []
    for j in range(k):
        col = [r[j] for r in witness_rows]
        m, s = mean_sd_0(col)
        if s == 0.0:
            return None  # a degenerate operator column: no fold, the caller prints loud
        mus.append(m)
        sds.append(s)
    f_raws = []
    for r in witness_rows:
        f_raws.append(sum(sgn * (x - m) / s for sgn, x, m, s in zip(signs, r, mus, sds)))
    mu_f, sd_f = mean_sd_0(f_raws)
    if sd_f == 0.0:
        return None  # a degenerate composite: no point score, the caller prints loud
    return {'mus': mus, 'sds': sds, 'signs': list(signs), 'f_raws': f_raws,
            'mu_f': mu_f, 'sd_f': sd_f, 'n_witness': len(witness_rows)}


def math_point_score(op_row, fold):
    """The unpaired in-band point score: the signed equal-weight operator sum on the
    clean-witness scale, then the composite standardization. One look at the terminal
    answer commit (the M-Terminal variant), or the running peak under the envelope
    (the M-Envelope variant, section 5) -- the variant discipline is the caller's."""
    if fold is None:
        return None
    f_raw = sum(sgn * (x - m) / s for sgn, x, m, s in zip(fold['signs'], op_row, fold['mus'], fold['sds']))
    return (f_raw - fold['mu_f']) / fold['sd_f']


# ------------------------------------------------- the maturity rosters (section 3, the rung ladder)
ROSTER_ONSET = ('onset_guard',)
ROSTER_EARLY = ('z_mu', 'z_walk', 'z_sigma', 'z_wu_ext', 'z_temporal')
ROSTER_MID = ROSTER_EARLY + ('z_fork', 'z_couple')
ROSTER_L64 = ROSTER_MID + ('z_win_l64',)
ROSTER_L128 = ROSTER_MID + ('z_win_l128',)


def rung_roster(n):
    """The maturity rung at commit count n: the point-anchor guard below 5; the 5-name
    early span to 35; the 7-name mid span once the probe-B4 locks at 36; the full
    8-name L=64 cell from 64; the 8-name L=128 form of record from 128 and beyond.
    Rosters by NAME -- the pinned bases and weights are the calibration's, loaded by
    the instrument (build message 3), never invented here."""
    if n < 5:
        return ROSTER_ONSET
    if n < 36:
        return ROSTER_EARLY
    if n < 64:
        return ROSTER_MID
    if n < 128:
        return ROSTER_L64
    return ROSTER_L128

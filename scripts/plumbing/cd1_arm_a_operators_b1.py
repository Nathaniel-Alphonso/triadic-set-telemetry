#!/usr/bin/env python3
# cd1_arm_a_operators_b1.py -- the CD-1 Arm A B1 operator module of record.
# Per the OWNER-PINNED Arm A sheet of record
# (cd1-arm-a-fabrication-separation-preregistration.md, 14022 B, 14dbedda...)
# section 6 line B1, under the stamped Phase-1 build spec
# (cd1-arm-a-phase1-build-spec.md, 8241 B, 0c886741...) section 3, at
# the B0 acceptance (his stamp opening the measurement phase; B0 closed
# at the item-1139 readout). ZERO GPU, ZERO DECODES: this module
# computes on constructed and passed-in arrays only; the model-file
# touch class (the W_U numeric-subspace rows) arrives as ARGUMENTS at
# B2, owner-side, matrix multiplication only, never a forward pass,
# never a decode, never a model load here. The module prints no
# verdicts; findings presented, never adjudicated; the owner's stamps
# decide.
#
# Modes: import (B2 imports the pure functions) / --battery (the
# fail-loud known-answer battery of record, constructed bytes only).
#
# THE PINNED CONVENTIONS, each with its record source (this block is
# the module's own pin; the battery reproduces every one):
#   (1) THE t_0 LAW (the sheet section 3): the FIRST numeric token of
#       the committed quantity span; never the equality sign; never
#       the span mean. B1 COMPUTES AT a given t_0; the t_0s themselves
#       ride the B0 inventory, never re-derived here.
#   (2) V_num (the sheet section 2 + the item-1103 correction 1): the
#       numeric vocabulary pinned per leg at B0 (1,110 ids at the
#       pinned tokenizer); B1 receives the numeric logits or the W_U
#       rows restricted to V_num as arguments; the softmax and the
#       top-2 are RENORMALIZED INSIDE V_num, never the full vocab.
#   (3) THE bf16-ulp NORMALIZATION (the near-tie census convention of
#       record: 6/41 reads within 2 bf16 ulps, two exact ties; the
#       item-1103 correction 3): m_ulp = gap / ulp_bf16(logit1), with
#       ulp_bf16(x) = 2^(floor(log2|x|) - 7) at normal magnitudes and
#       2^-133 at subnormal magnitudes; a zero top-1 is a NAMED
#       sentinel (reason string), never a silent skip.
#   (4) THE COMMON-MODE CENTERING (the item-1104 defect-1 ruling):
#       centered against the doc-level numeric-step mean -- the mean
#       of the doc's own numeric-step states; MANDATORY precondition
#       for centered R_perp and BHOB (the anisotropic cone).
#   (5) THE RIDGE PROJECTOR: P = A^T (A A^T + lam I)^-1 A onto the
#       centered operand rows; lam = LAM_REL * mean(row squared
#       norms), LAM_REL = 1e-8 pinned here (scale-relative; the
#       battery reproduces the convention).
#   (6) centered R_perp (the item-1104 defect-1 ruling): the residual
#       ENERGY SHARE of the centered state outside the projector;
#       FIXED m=2; the d/(d-m) standardization carried as the
#       multi-operand fallback (the standardize flag).
#   (7) BHOB (the item-1104 defect-2 ruling): min over the two
#       operands of the leave-one-operand-out residual drop, on
#       centered states; LOW = operand-blind = the myopic signature;
#       the operand rows pinned to the CORRECT-precedence
#       composition's antecedent positions at B2 from the checker's
#       path evidence; m must equal 2, else a NAMED sentinel.
#   (8) zeta (the item-1104 defect-4 ruling): the sigma_num-
#       standardized projection of h_t onto the committed answer's
#       unembedding column: zeta = (h.u_a - mu_num) / sigma_num, with
#       mu_num and sigma_num the mean and the POPULATION standard
#       deviation (ddof=0) of the leg's V_num logits at that step; a
#       zero sigma_num is a NAMED sentinel.
#   (9) THE LINEAR WORK INCREMENT (the item-1104 defect-4 ruling):
#       zeta at the commit step minus the early-window MAX of zeta
#       over the DERIVATION-PATH steps (the checker's path evidence;
#       never the whole prompt); an EMPTY window is a NAMED sentinel;
#       at or below zero = the answer active early = the item-74c
#       answer-first-backfill signature; high positive = the answer
#       arriving with the final integration.
#  (10) kappa (the item-1103(e) demotion ruling): the step angular
#       shear, 1 - cosine of adjacent hidden states; CORROBORATOR
#       ONLY, boundary-guarded per the item-257 machinery
#       (BOUNDARY_STEPS 3 / TAIL_FRAC 0.15): a t_0 within 3 steps of
#       a phase transition, or in the last 15% of the run, types the
#       read BOUNDARY (flagged, logged, never a clean corroborator
#       read); never primary, never alone (the F4 precedent).
#  (11) THE RAW DUMP GAPS ride B2 side-by-side as logged receipts
#       (the item-1104 defect-3 status change); B1 carries no raw-gap
#       function by design.
import argparse
import base64
import hashlib
import json
import math
import os
import struct
import sys

TOOL = "cd1_arm_a_operators_b1.py"
VERSION = "1.0.0"
LAM_REL = 1e-8
BOUNDARY_STEPS = 3
TAIL_FRAC = 0.15
SENTINEL = "SENTINEL"


# ---------------------------------------------------------------------------
# Section 1. The bf16 utilities (the cache hidden-state decode + the ulp law)
# ---------------------------------------------------------------------------

def bf16_decode_b64(b64s):
    """base64 -> bf16 bytes -> float list (the cache hidden_b64 convention)."""
    raw = base64.b64decode(b64s)
    if len(raw) % 2:
        raise ValueError("bf16 payload length odd: %d" % len(raw))
    n = len(raw) // 2
    words = struct.unpack(">" + "H" * n, raw)
    out = []
    for w in words:
        bits = w << 16
        out.append(struct.unpack(">f", struct.pack(">I", bits))[0])
    return out


def bf16_ulp(x):
    """The bf16 ulp at magnitude |x| (normals 2^(e-7); subnormals 2^-133)."""
    ax = abs(float(x))
    if ax == 0.0:
        return 2.0 ** -133
    e = math.floor(math.log2(ax))
    if e < -126:
        return 2.0 ** -133
    return 2.0 ** (e - 7)


# ---------------------------------------------------------------------------
# Section 2. The shared measurement utilities (pure; constructed or
# passed-in arrays only)
# ---------------------------------------------------------------------------

def dot(a, b):
    s = 0.0
    for x, y in zip(a, b):
        s += x * y
    return s


def cosine(a, b):
    d = dot(a, b)
    na = math.sqrt(dot(a, a))
    nb = math.sqrt(dot(b, b))
    if na == 0.0 or nb == 0.0:
        return None
    return d / (na * nb)


def num_logits(h, w_num):
    """h (d,) x W_U[V_num] rows (n_num, d) -> the numeric logits (n_num,).

    The ONLY model-file-touch class of function in the module: B2 feeds
    the W_U rows restricted to the leg's pinned V_num, owner-side;
    matrix multiplication only, never a forward pass, never a decode.
    """
    return [dot(h, w) for w in w_num]


def _mu_sigma(values):
    mu = sum(values) / len(values)
    var = 0.0
    for v in values:
        var += (v - mu) * (v - mu)
    return mu, math.sqrt(var / len(values))


def common_mode_mean(states):
    """The doc-level numeric-step mean (the item-1104 centering law)."""
    n = len(states)
    d = len(states[0])
    acc = [0.0] * d
    for s in states:
        for i, x in enumerate(s):
            acc[i] += x
    return [x / n for x in acc]


def center_state(h, mean):
    return [x - m for x, m in zip(h, mean)]


def ridge_residual_share(h_c, operand_rows, standardize=False):
    """Residual energy share of centered h_c outside the ridge projector
    onto the centered operand rows (m rows, d dims).

    P = A^T (A A^T + lam I)^-1 A ; residual = (I - P) h_c.
    Returns the residual energy share (and the in-span share beside it;
    the two sum to 1 by construction). The d/(d-m) standardization is
    the multi-operand fallback (standardize=True), carried per the
    item-1104 ruling, off at the fixed m=2 default.
    """
    m = len(operand_rows)
    d = len(h_c)
    if m == 0:
        raise ValueError("empty operand set")
    if any(len(r) != d for r in operand_rows):
        raise ValueError("operand row dim mismatch")
    sq = 0.0
    for r in operand_rows:
        sq += dot(r, r)
    lam = LAM_REL * (sq / m)
    # gram = A A^T + lam I  (m x m, small m)
    gram = [[dot(operand_rows[i], operand_rows[j]) for j in range(m)]
            for i in range(m)]
    for i in range(m):
        gram[i][i] += lam
    # solve gram^-1 via Gaussian elimination with partial pivoting
    rhs = [dot(operand_rows[i], h_c) for i in range(m)]
    alpha = _solve_linear(gram, rhs)
    # in-span component: sum_i alpha_i * A_i
    in_span = [0.0] * d
    for i in range(m):
        ai = alpha[i]
        row = operand_rows[i]
        for j in range(d):
            in_span[j] += ai * row[j]
    resid = [h_c[j] - in_span[j] for j in range(d)]
    e_res = dot(resid, resid)
    e_tot = dot(h_c, h_c)
    if e_tot <= 0.0:
        return {"residual_share": None, "in_span_share": None,
                "lam_eff": lam, "m": m, "d": d,
                "reason": "zero centered state energy"}
    share = e_res / e_tot
    out = {"residual_share": share,
           "in_span_share": 1.0 - share,
           "lam_eff": lam, "m": m, "d": d}
    if standardize:
        out["residual_share_std"] = share * (d / (d - m)) if d > m else None
    return out


def _solve_linear(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) == 0.0:
            raise ValueError("singular projector gram (lam degenerate)")
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col] / pv
            if f == 0.0:
                continue
            for c in range(col, n + 1):
                M[r][c] -= f * M[col][c]
    return [M[i][n] / M[i][i] for i in range(n)]


# ---------------------------------------------------------------------------
# Section 3. The operators (one pure function per operator; the sheet
# section 4 roster, Phase-1 members + the corroborator)
# ---------------------------------------------------------------------------

def m_ulp_num(logits_num):
    """OPERATOR 1, the A1 PRIMARY: the numeric top-2 margin at t_0 in
    bf16 ulps (the item-1104 defect-3 refinement: inside V_num, the
    raw dump gap rides B2 as the side-by-side receipt)."""
    if not logits_num:
        raise ValueError("empty V_num logits")
    order = sorted(range(len(logits_num)),
                   key=lambda i: (-logits_num[i], i))
    i1, i2 = order[0], order[1]
    l1 = logits_num[i1]
    l2 = logits_num[i2]
    gap = l1 - l2
    if l1 == 0.0:
        return {"m_ulp": None, "logit1": l1, "logit2": l2, "gap": gap,
                "ulp": None, "id1": i1, "id2": i2,
                "reason": "zero top-1 numeric logit: the ulp undefined"}
    ulp = bf16_ulp(l1)
    return {"m_ulp": gap / ulp, "logit1": l1, "logit2": l2, "gap": gap,
            "ulp": ulp, "id1": i1, "id2": i2, "reason": None}


def h_num(logits_num):
    """OPERATOR 2, A1 diagnostic: the entropy (bits) of the softmax
    renormalized over V_num at t_0 (the item-1103 correction 1)."""
    if not logits_num:
        raise ValueError("empty V_num logits")
    mx = max(logits_num)
    exps = [math.exp(v - mx) for v in logits_num]
    tot = sum(exps)
    ps = [e / tot for e in exps]
    H = 0.0
    for p in ps:
        if p > 0.0:
            H -= p * math.log2(p)
    return {"h_num": H, "p_top": max(ps)}


def centered_r_perp(h_c, operand_rows, standardize=False):
    """OPERATOR 3, A1 + A2 diagnostic: the residual energy share of the
    common-mode-centered state outside the ridge projector onto the two
    immediate grounded operands' centered states (fixed m=2; the
    d/(d-m) standardization the multi-operand fallback). HIGH residual
    = the state outside the grounded operand span = untraced pull; the
    role-geometry confound carried at the read, never here."""
    return ridge_residual_share(h_c, operand_rows,
                                standardize=standardize)


def bhob(h_c, operand_rows):
    """OPERATOR 4, A2 diagnostic: min over the two operands of the
    leave-one-operand-out residual drop, on centered states. LOW = the
    least-used operand contributes nothing = operand-blind = the myopic
    signature. m must equal 2 (the pinned fixed form), else a NAMED
    sentinel."""
    m = len(operand_rows)
    if m != 2:
        return {"bhob": None, "drops": None, "m": m,
                "reason": "BHOB requires exactly 2 operands (fixed m=2)"}
    full = ridge_residual_share(h_c, operand_rows)
    drops = []
    for i in range(2):
        loo_rows = [operand_rows[j] for j in range(2) if j != i]
        loo = ridge_residual_share(h_c, loo_rows)
        drops.append(loo["residual_share"] - full["residual_share"])
    return {"bhob": min(drops), "drops": drops,
            "residual_full": full["residual_share"], "m": m,
            "reason": None}


def zeta_step(p_answer, logits_num):
    """OPERATOR 5 support: the sigma_num-standardized projection of h_t
    onto the committed answer's unembedding column (p_answer = h.u_a,
    precomputed; standardized over the leg's V_num logits at the step;
    population std ddof=0)."""
    if not logits_num:
        raise ValueError("empty V_num logits")
    mu, sigma = _mu_sigma(logits_num)
    if sigma == 0.0:
        return {"zeta": None, "mu_num": mu, "sigma_num": sigma,
                "reason": "zero sigma_num: the V_num logits degenerate"}
    return {"zeta": (p_answer - mu) / sigma, "mu_num": mu,
            "sigma_num": sigma, "reason": None}


def work_increment(zeta_commit, zeta_window):
    """OPERATOR 5, the A2 PRIMARY: the linear work increment (the
    item-1104 defect-4 re-form): zeta at the commit step minus the
    early-window max of zeta over the DERIVATION-PATH steps. At or
    below zero = the answer active early = the item-74c answer-first-
    backfill signature; high positive = the answer arriving with the
    final integration. The window rides the checker's path evidence at
    B2, never the whole prompt; an EMPTY window is a NAMED sentinel."""
    if not zeta_window:
        return {"increment": None, "window_max": None, "window_n": 0,
                "reason": "empty derivation-path window: the path "
                          "evidence absent, never the whole prompt"}
    wmax = max(zeta_window)
    return {"increment": zeta_commit - wmax, "window_max": wmax,
            "window_n": len(zeta_window), "reason": None}


def kappa_step(h_prev, h_t):
    """CORROBORATOR (never primary, never alone; the F4 precedent): the
    step angular shear, 1 - cosine of adjacent hidden states."""
    c = cosine(h_prev, h_t)
    if c is None:
        return None
    return 1.0 - c


def kappa_boundary(t, phases, n_steps,
                   boundary_steps=BOUNDARY_STEPS, tail_frac=TAIL_FRAC):
    """The item-257 boundary guard: a step within BOUNDARY_STEPS of a
    phase transition (inclusive), or in the last TAIL_FRAC of the run,
    types BOUNDARY. The guard rides every kappa read."""
    for i in range(1, len(phases)):
        if phases[i] != phases[i - 1]:
            if abs(t - i) <= boundary_steps:
                return {"boundary": True,
                        "reason": "within %d steps of a phase transition "
                                   "(transition at step %d)"
                                   % (boundary_steps, i)}
    tail_start = math.ceil((1.0 - tail_frac) * n_steps)
    if t >= tail_start:
        return {"boundary": True,
                "reason": "in the last %d%% of the run (tail start %d)"
                          % (int(tail_frac * 100), tail_start)}
    return {"boundary": False, "reason": None}


def kappa_corroborator(h_prev, h_t, t, phases, n_steps):
    """kappa + the boundary guard, one read: the boundary flag rides,
    the read logged, never primary, never alone."""
    k = kappa_step(h_prev, h_t)
    guard = kappa_boundary(t, phases, n_steps)
    return {"kappa": k, "boundary": guard["boundary"],
            "guard_reason": guard["reason"]}


# ---------------------------------------------------------------------------
# Section 4. The known-answer battery (fail-loud, constructed bytes
# only, every exit named; the Phase-1 spec section 3 + the item-1109(d)
# battery law)
# ---------------------------------------------------------------------------

def _b64_of(words):
    return base64.b64encode(struct.pack(">" + "H" * len(words),
                                        *words)).decode("ascii")


def run_battery(out_dir):
    lines = []
    checks = []

    def check(cid, name, ok, detail):
        checks.append({"id": cid, "name": name, "pass": bool(ok),
                        "detail": detail})
        lines.append("[%s] %s %s -- %s" % (cid, "PASS" if ok else "FAIL",
                                           name, detail))

    # py_compile of the module itself, asserted first
    import py_compile
    try:
        py_compile.compile(os.path.abspath(__file__), doraise=True)
        check("B1-C00", "py_compile clean", True, "module compiles")
    except py_compile.PyCompileError as e:
        check("B1-C00", "py_compile clean", False, str(e))

    # C01: bf16 decode, known bit patterns exact
    b64s = _b64_of([0x41C0, 0x41BE, 0x3F80])
    vals = bf16_decode_b64(b64s)
    ok = vals == [24.0, 23.75, 1.0]
    check("B1-C01", "bf16 decode known patterns",
          ok, "0x41C0/0x41BE/0x3F80 -> %r" % (vals,))

    # C02: the bf16 ulp law at known magnitudes
    ok = (bf16_ulp(24.0) == 0.125 and bf16_ulp(1.0) == 2.0 ** -7
          and bf16_ulp(0.5) == 2.0 ** -8 and bf16_ulp(4.0) == 0.03125)
    check("B1-C02", "bf16 ulp law", ok,
          "ulp(24.0)=0.125, ulp(1.0)=2^-7, ulp(0.5)=2^-8, ulp(4.0)=2^-5")

    # C03: the near-tie census convention reproduced on constructed
    # values (the convention, never the data): the six census-shaped
    # rows at magnitude 24 -> ulps [2,2,1,0,0,1], 6 within 2 ulps,
    # two exact ties
    gaps = [0.25, 0.25, 0.125, 0.0, 0.0, 0.125]
    ulps = [m_ulp_num([24.0, 24.0 - g])["m_ulp"] for g in gaps]
    expect = [2.0, 2.0, 1.0, 0.0, 0.0, 1.0]
    within2 = sum(1 for u in ulps if u <= 2.0)
    ties = sum(1 for u in ulps if u == 0.0)
    ok = ulps == expect and within2 == 6 and ties == 2
    check("B1-C03", "near-tie census convention on constructed values",
          ok, "ulps %r -> within-2 count %d, exact ties %d"
              % (ulps, within2, ties))

    # C04: the W_U numeric-subspace projection, hand-computed
    h = [1.0, 2.0, 3.0]
    w_num = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0]]
    lg = num_logits(h, w_num)
    ok = lg == [1.0, 2.0, 3.0]
    check("B1-C04", "numeric-subspace projection hand answer",
          ok, "h x W_num rows -> %r" % (lg,))

    # C05: the numeric top-2 law (order, gap, ulp) with a
    # formatting-token stand-in OUTSIDE the numeric logits
    r = m_ulp_num([5.0, 24.0, 23.75, 7.0])
    ok = (r["id1"] == 1 and r["id2"] == 2 and r["gap"] == 0.25
          and r["m_ulp"] == 2.0)
    check("B1-C05", "numeric top-2 margin", ok,
          "top-2 inside V_num: gap %r, m_ulp %r" % (r["gap"], r["m_ulp"]))

    # C06: the zero-top-1 sentinel trips loud
    r = m_ulp_num([0.0, -1.0])
    ok = r["m_ulp"] is None and r["reason"]
    check("B1-C06", "zero top-1 sentinel named", ok, r["reason"])

    # C07: H_num closed form -- the uniform distribution
    r = h_num([1.0] * 8)
    ok = abs(r["h_num"] - 3.0) < 1e-12 and abs(r["p_top"] - 0.125) < 1e-12
    check("B1-C07", "H_num uniform closed form", ok,
          "8 equal logits -> %r bits, p_top %r"
              % (r["h_num"], r["p_top"]))

    # C08: H_num closed form -- the four-point one-hot-biased mix
    lg = [math.log(3.0), 0.0, 0.0, 0.0]
    r = h_num(lg)
    expect_H = -(0.5 * math.log2(0.5)
                 - 3 * (1.0 / 6.0) * math.log2(1.0 / 6.0)) * -1.0
    expect_H = -(0.5 * math.log2(0.5)) - 3 * ((1.0 / 6.0)
                                              * math.log2(1.0 / 6.0))
    ok = abs(r["h_num"] - expect_H) < 1e-12
    check("B1-C08", "H_num mixed closed form", ok,
          "p=[1/2,1/6,1/6,1/6] -> %r vs %r" % (r["h_num"], expect_H))

    # C09: the common-mode centering kills the constructed common mode
    common = [1.5, -0.7, 0.25, 3.0]
    e = [[0.2, 0.1, -0.3, 0.0], [-0.1, -0.2, 0.3, 0.0],
         [-0.05, 0.05, 0.0, 0.0], [-0.05, 0.05, 0.0, 0.0],
         [0.0, 0.0, 0.0, 0.0]]
    ref = [[common[i] + e[k][i] for i in range(4)] for k in range(5)]
    mean = common_mode_mean(ref)
    sig = [0.3, -0.2, 0.1, 0.0]
    operand = [common[i] + sig[i] for i in range(4)]
    cent = center_state(operand, mean)
    dev = max(abs(c - s) for c, s in zip(cent, sig))
    ref_cent = [center_state(r, mean) for r in ref]
    ref_mean_cent = common_mode_mean(ref_cent)
    ref_res = max(abs(x) for x in ref_mean_cent)
    ok = dev < 1e-12 and ref_res < 1e-12
    check("B1-C09", "centering kills the common mode exactly", ok,
          "centered operand == signal (max dev %r); the centered ref "
          "population's own mean zero (max res %r)"
              % (dev, ref_res))

    # C10: the ridge projector -- the in-span state
    A = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]
    h_in = [3.0, -4.0, 0.0, 0.0]
    r = ridge_residual_share(h_in, A)
    ok = r["residual_share"] < 1e-6 and r["in_span_share"] > 1 - 1e-6
    check("B1-C10", "ridge projector in-span residual", ok,
          "residual share %r, in-span %r"
              % (r["residual_share"], r["in_span_share"]))

    # C11: the ridge projector -- the orthogonal state
    h_out = [0.0, 0.0, 5.0, 2.0]
    r = ridge_residual_share(h_out, A)
    ok = abs(r["residual_share"] - 1.0) < 1e-9
    check("B1-C11", "ridge projector orthogonal residual", ok,
          "residual share %r" % r["residual_share"])

    # C12: the energy conservation law
    r = ridge_residual_share([1.0, 2.0, 1.5, -0.5], A)
    ok = abs(r["residual_share"] + r["in_span_share"] - 1.0) < 1e-9
    check("B1-C12", "projector energy conservation", ok,
          "residual %r + in-span %r == 1"
              % (r["residual_share"], r["in_span_share"]))

    # C13: the d/(d-m) standardization fallback
    r = ridge_residual_share([1.0, 2.0, 1.5, -0.5], A, standardize=True)
    ok = abs(r["residual_share_std"]
             - r["residual_share"] * (4.0 / 2.0)) < 1e-12
    check("B1-C13", "d/(d-m) standardization fallback", ok,
          "share %r -> standardized %r (d 4, m 2)"
              % (r["residual_share"], r["residual_share_std"]))

    # C14: centered R_perp, the fixed m=2 wrapper reads the projector
    r = centered_r_perp(h_out, A)
    ok = abs(r["residual_share"] - 1.0) < 1e-9 and r["m"] == 2
    check("B1-C14", "centered R_perp fixed m=2", ok,
          "m %d, residual share %r" % (r["m"], r["residual_share"]))

    # C15: BHOB on the bilobed state (both operands used)
    h_bi = [math.sqrt(0.5), math.sqrt(0.5), 0.0, 0.0]
    r = bhob(h_bi, A)
    ok = (r["bhob"] is not None and r["bhob"] > 0.4
          and abs(min(r["drops"]) - r["bhob"]) < 1e-12)
    check("B1-C15", "BHOB bilobed direction", ok,
          "drops %r, bhob %r (min law held)"
              % (r["drops"], r["bhob"]))

    # C16: BHOB on the single-operand collapse (the myopic signature:
    # the unused operand's drop ~ 0, the min ~ 0)
    h_mono = [1.0, 0.0, 0.0, 0.0]
    r = bhob(h_mono, A)
    ok = (r["bhob"] is not None and r["bhob"] < 1e-6)
    check("B1-C16", "BHOB myopic direction", ok,
          "drops %r, bhob %r (LOW = operand-blind)" % (r["drops"],
                                                       r["bhob"]))

    # C17: BHOB m!=2 sentinel trips loud
    A3 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0],
          [0.0, 0.0, 1.0, 0.0]]
    r = bhob([1.0, 1.0, 1.0, 0.0], A3)
    ok = r["bhob"] is None and "2 operands" in r["reason"]
    check("B1-C17", "BHOB m!=2 sentinel named", ok, r["reason"])

    # C18: zeta at exactly +2 sigma_num
    logits = [1.0, 2.0, 3.0, 4.0, 5.0]
    mu, sigma = _mu_sigma(logits)
    p_answer = mu + 2.0 * sigma
    r = zeta_step(p_answer, logits)
    ok = abs(r["zeta"] - 2.0) < 1e-12
    check("B1-C18", "zeta standardization hand answer", ok,
          "p_answer at mu + 2 sigma -> zeta %r" % r["zeta"])

    # C19: the work increment -- the early-locked backfill direction
    r = work_increment(0.5, [2.0, 1.5, 1.8])
    ok = abs(r["increment"] - (0.5 - 2.0)) < 1e-12 and r["increment"] < 0.0
    check("B1-C19", "work increment early-locked direction", ok,
          "increment %r (at or below zero = the backfill signature)"
              % r["increment"])

    # C20: the work increment -- the late-arriving direction + the
    # window-max law
    r = work_increment(1.9, [0.1, 0.2, 0.15])
    ok = abs(r["increment"] - (1.9 - 0.2)) < 1e-12 and r["increment"] > 0.0
    check("B1-C20", "work increment late-arriving direction", ok,
          "increment %r, window_max %r"
              % (r["increment"], r["window_max"]))

    # C21: the empty-window sentinel trips loud
    r = work_increment(1.0, [])
    ok = r["increment"] is None and r["reason"]
    check("B1-C21", "empty derivation-path window sentinel named",
          ok, r["reason"])

    # C22: the zero-sigma_num sentinel trips loud
    r = zeta_step(1.0, [2.0, 2.0, 2.0])
    ok = r["zeta"] is None and r["reason"]
    check("B1-C22", "zero sigma_num sentinel named", ok, r["reason"])

    # C23: kappa closed forms (the step angular shear)
    th = math.radians(60.0)
    a = [1.0, 0.0]
    b = [math.cos(th), math.sin(th)]
    k1 = kappa_step(a, b)
    k2 = kappa_step([1.0, 0.0], [1.0, 0.0])
    k3 = kappa_step([1.0, 0.0], [0.0, 1.0])
    ok = (abs(k1 - 0.5) < 1e-12 and abs(k2) < 1e-12
          and abs(k3 - 1.0) < 1e-12)
    check("B1-C23", "kappa closed forms", ok,
          "60deg -> %r, identical -> %r, orthogonal -> %r"
              % (k1, k2, k3))

    # C24: the kappa boundary guard -- the phase-transition window
    phases = ["COT"] * 100 + ["ANSWER"] * 100
    g_clean = kappa_boundary(104, phases, 200)
    g_near = kappa_boundary(102, phases, 200)
    g_before = kappa_boundary(96, phases, 200)
    ok = (not g_clean["boundary"] and g_near["boundary"]
          and not g_before["boundary"])
    check("B1-C24", "kappa boundary guard transition window", ok,
          "t=96 clean, t=102 BOUNDARY, t=104 clean (window %d "
          "inclusive)" % BOUNDARY_STEPS)

    # C25: the kappa boundary guard -- the tail
    g_tail_in = kappa_boundary(170, phases, 200)
    g_tail_out = kappa_boundary(169, phases, 200)
    ok = g_tail_in["boundary"] and not g_tail_out["boundary"]
    check("B1-C25", "kappa boundary guard tail", ok,
          "t=169 clean, t=170 BOUNDARY (tail start 170 of 200)")

    # C26: the corroborator integration -- the guard flag rides the read
    rc = kappa_corroborator(a, b, 102, phases, 200)
    ok = rc["boundary"] and abs(rc["kappa"] - 0.5) < 1e-12
    check("B1-C26", "kappa corroborator guard integration", ok,
          "kappa %r, boundary %r (%s)"
              % (rc["kappa"], rc["boundary"], rc["guard_reason"]))

    # assemble the battery export (deterministic sort_keys; the
    # module's own sha rides the export)
    n_pass = sum(1 for c in checks if c["pass"])
    n_fail = len(checks) - n_pass
    with open(__file__, "rb") as f:
        mod_sha = hashlib.sha256(f.read()).hexdigest()
    export = {
        "tool": TOOL,
        "version": VERSION,
        "act": "B1 the operator module, the known-answer battery",
        "lineage": {
            "arm_a_sheet": "cd1-arm-a-fabrication-separation-"
                           "preregistration.md 14dbedda...",
            "phase1_build_spec": "cd1-arm-a-phase1-build-spec.md "
                                 "0c886741...",
            "battery_law": "the Phase-1 spec section 3 + item 1109(d)",
            "constructed_bytes_only": True,
        },
        "pinned_conventions": {
            "lam_rel": LAM_REL,
            "boundary_steps": BOUNDARY_STEPS,
            "tail_frac": TAIL_FRAC,
            "zeta_standardization": "population mu/sigma over the leg's "
                                    "V_num logits at the step (ddof 0)",
            "work_increment_window": "the derivation-path steps from "
                                     "the checker's path evidence",
            "m_ulp_normalization": "gap / bf16_ulp(logit1), the "
                                   "near-tie census convention "
                                   "(6/41 within 2 ulps, two exact "
                                   "ties)",
            "centering": "the doc-level numeric-step mean",
        },
        "battery": {"n_pass": n_pass, "n_fail": n_fail,
                    "checks": checks},
        "module_sha256": mod_sha,
    }
    # C27: determinism -- the assembled export rebuilt twice
    # byte-identical (the final written export below carries this row
    # and the final census)
    ok = json.dumps(export, sort_keys=True, indent=1) == \
        json.dumps(export, sort_keys=True, indent=1)
    check("B1-C27", "battery export determinism", ok,
          "the assembled export rebuilt twice byte-identical")

    n_pass = sum(1 for c in checks if c["pass"])
    n_fail = len(checks) - n_pass
    export["battery"]["n_pass"] = n_pass
    export["battery"]["n_fail"] = n_fail
    txt = json.dumps(export, sort_keys=True, indent=1)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cd1_arm_a_b1_battery_export.json")
    with open(out_path, "w") as f:
        f.write(txt + "\n")
    return lines, checks, out_path, mod_sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--battery", action="store_true",
                    help="run the known-answer battery (constructed "
                         "bytes only)")
    ap.add_argument("--out-dir", default=".",
                    help="battery output directory")
    args = ap.parse_args()
    if not args.battery:
        print("the B1 operator module of record; import from B2, or "
              "run --battery")
        return 0
    lines, checks, out_path, mod_sha = run_battery(args.out_dir)
    for ln in lines:
        print(ln)
    n_pass = sum(1 for c in checks if c["pass"])
    n_fail = len(checks) - n_pass
    print("BATTERY CENSUS: %d PASS / %d FAIL" % (n_pass, n_fail))
    print("battery export: %s" % out_path)
    print("module sha256: %s" % mod_sha)
    if n_fail:
        print("HARD EXIT -- the battery is fail-loud; a FAIL is named "
              "above, never skipped")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

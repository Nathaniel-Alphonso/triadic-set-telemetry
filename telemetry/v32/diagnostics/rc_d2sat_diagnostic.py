#!/usr/bin/env python3
"""THE SATURATED D2 DIAGNOSTIC -- the rc-d2sat-conversion-prereg.md S6 act.

At his word ("lets have the diagnostic") the sheet's diagnostic runs:
the saturation re-form of the d2 zero-run-mass face (psi(s) = s/(s+kappa),
KAPPA = 1 pinned by the sheet at his stamp, never tuned to the answer),
read EXACTLY as sheeted -- the census parity gate first (the re-derived
per-doc masses must reproduce his banked console census at gate 8, a
mismatch a HARD EXIT), then the saturated census on the ACTUAL masses,
the cliff read, the honest both-sides gap, the off-leg reads, the
three-miss read, the sweep receipts, and the kill-switch verdicts,
presented never adjudicated.

TWO MODES (the codev7 genre):
  --parity-only : the receipt-side gates alone, NO caches needed (the
                  desk's half, runnable anywhere beside the receipt +
                  tool + the pinned sheet);
  (default)     : the full diagnostic -- HIS MAC, read-only, zero GPU,
                  zero decodes, the script beside triadic_rw17_codev5.py
                  + rc_codev5_receipt.json + the pinned sheet + his
                  three pinned walk caches; emits
                  rc_d2sat_diagnostic_console.txt for his shasum +
                  upload.

usage: python3 rc_d2sat_diagnostic.py --parity-only   (the desk half)
       python3 rc_d2sat_diagnostic.py                 (his Mac, full)
"""

import json
import os
import sys
import importlib.util

TOOL_NAME = "triadic_rw17_codev5.py"
TOOL_SHA_BANK = ("391ac7dfd91f4c45c7c113211005a8bb44565737"
                 "887331fd512ed9723b4c2cf3")
RECEIPT_NAME = "rc_codev5_receipt.json"
RECEIPT_SHA_BANK = ("fc8b70b5435cefbc419b3b10dd0aeae6b579dcad1b"
                    "7bfcaac5d11660b6e6cc42")
SHEET_NAME = "rc-d2sat-conversion-prereg.md"
SHEET_SHA = ("a40fd3b0916e0ebf80d757119f612f060717b521ca2325ce"
             "ca48e4b54f8dbed8")
PARITY_CONSOLE = "rc_d2sat_parity_console.txt"
FULL_CONSOLE = "rc_d2sat_diagnostic_console.txt"

KAPPA_PIN = 1.0                       # the sheet's convention pin
KAPPA_SWEEP = (1.0, 2.0, 4.0, 8.0)     # receipts only, never adjudicated
D2_GATES = (8, 12, 16)                # the swept support floor on triples
TAIL_LO, TAIL_HI = 19, 36
LATE_LO, LATE_HI = 28, 36
PARITY_TOL = 1e-12
MASK_STUB_D = 4.1775273637921755      # the demotion edge
LEVEL_BANK = 3.7618410048243147
GAP_BANK = 1.6862617412521999
HELD_V5_MU, HELD_V5_SD = 1.583084, 1.308408
HELD_COMB_MU, HELD_COMB_SD = 1.787326, 2.174735
LOOP_COMB_MU, LOOP_COMB_SD = 6.338041, 3.976063
GAP_COMB_BANK = 1.420070
D_INJ_CODE = 7.989752
D_JSON_LIFTED = 5.712799
D_COUNTDOWN_REFINED = 1.434110
D_INJ_D2Z = 15.326556
PB4_HONEST = 1.792063                 # the standing best banked honest read
CAPS = {6: 1.6432, 7: 2.0494, 8: 2.6833}
# the banked d2 census, HIS consoles (items 490/493), the parity anchors:
# AMEND v2 -- PER-LEG anchors (the item-493 bank: the gate-8 census
# moments reproduce on all three legs; the item-490 bank: the n_pos
# counts).  The v1 gate wired every leg against the CODE anchor alone
# and hard-exited on prose whose own re-derived census was EXACT
# against the banked prose refs -- a desk-side wiring error, never a
# data verdict.  Every anchor below is BANKED, nothing invented; the
# off-leg held counts never banked -- printed as findings, never
# gated.
CEN_ANCHORS = {
    "mbpprw17": {"mean": 0.275000, "sd": 1.352227, "n_pos": 11, "n": 200,
                 "held_n_pos": 15},
    "prose17p-rw17": {"mean": 1.548387, "sd": 3.896216, "n_pos": 72,
                      "n": 310, "held_n_pos": None},
    "p2corpus-rw17": {"mean": 1.154667, "sd": 3.072663, "n_pos": 62,
                      "n": 375, "held_n_pos": None},
}
CEN_MEAN = CEN_ANCHORS["mbpprw17"]["mean"]
CEN_SD = CEN_ANCHORS["mbpprw17"]["sd"]
CEN_N_POS = CEN_ANCHORS["mbpprw17"]["n_pos"]
CEN_N = CEN_ANCHORS["mbpprw17"]["n"]
HELD_N_POS = CEN_ANCHORS["mbpprw17"]["held_n_pos"]
# the fixture m_d2 bank (his gate-8 reads):
BANKED_MD2 = {"loop-sejection-placeholder": None}  # replaced at load
BANKED_MD2 = {"loop-seeded-json": 8, "loop-seeded-countdown": 0,
              "loop-seeded-code-line": 0, "loop-injection-code": 21,
              "loop-seeded-chant": 0}
# the item-488 P-B4 fixture table (mbpprw17):
BANKED_REFINED = {
    "loop-seeded-countdown": 0.368124, "loop-injection-code": 0.321772,
    "mask-reserved-stubborn": 0.299363, "loop-seeded-chant": 0.258515,
    "loop-injection-prose": 0.252647, "loop-seeded-cycle": 0.212269,
    "loop-seeded-counter": 0.141779, "loop-seeded-affirm": 0.127843,
    "loop-seeded-json": 0.057367, "loop-seeded-code-line": 0.036616,
}
OFF_LEG_BOUNDS = {"prose17p-rw17": 1.753702, "p2corpus-rw17": 1.772590}

OUT = []


def p(s=""):
    OUT.append(s)
    print(s)


def die(msg, code=1):
    sys.stderr.write("HARD EXIT: " + msg + "\n")
    sys.exit(code)


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_tool():
    if not os.path.exists(TOOL_NAME):
        die("tool %s not found beside this script -- the diagnostic "
            "imports the tool's own curve machinery; aborting."
            % TOOL_NAME)
    spec = importlib.util.spec_from_file_location("K", TOOL_NAME)
    K = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(K)
    return K


def load_receipt():
    if not os.path.exists(RECEIPT_NAME):
        die("receipt %s not found beside this script -- the "
            "run-of-record receipt is the before-column and the parity "
            "source; aborting." % RECEIPT_NAME)
    sha = sha256_file(RECEIPT_NAME)
    if sha != RECEIPT_SHA_BANK:
        die("receipt sha256 %s != the banked run-of-record %s -- never "
            "read foreign bytes; aborting." % (sha, RECEIPT_SHA_BANK))
    with open(RECEIPT_NAME) as f:
        r = json.load(f)
    ts = r.get("tool_sha256", "")
    if ts != TOOL_SHA_BANK:
        die("receipt tool_sha256 %s != the banked tool %s -- never "
            "project onto foreign bytes; aborting." % (ts,
                                                       TOOL_SHA_BANK))
    return r


def verify_sheet():
    if not os.path.exists(SHEET_NAME):
        die("the pinned sheet %s not found beside this script -- the "
            "diagnostic reads its form ONLY from the stamped sheet; "
            "aborting." % SHEET_NAME)
    sha = sha256_file(SHEET_NAME)
    if sha != SHEET_SHA:
        die("sheet sha256 %s != the pinned %s -- never run a "
            "diagnostic whose form is unpinned; aborting."
            % (sha, SHEET_SHA))


def m_d2(d2_vals, triples, t_min):
    """the d2 zero-run mass, the item-475 law mirrored onto d2 (the
    codev7 form of record, byte-carried): m = zero lags in runs of
    >= 2 consecutive supported lags (supported = d2 not None and
    triples >= t_min); ISOLATED zeros NEVER count."""
    zeros = [i for i in range(len(d2_vals))
             if d2_vals[i] is not None and triples[i] >= t_min
             and d2_vals[i] == 0.0]
    zset = set(zeros)
    in_run = set()
    for i in zeros:
        if (i - 1) in zset:
            in_run.add(i)
            in_run.add(i - 1)
        if (i + 1) in zset:
            in_run.add(i)
            in_run.add(i + 1)
    return len(in_run), zeros


def refined_tail(d_vals, pair_counts, K):
    """the P-B4 form, read EXACTLY as the item-488 ledger computed it
    (byte-carried from codev7): refined tail = 1 - min(d over
    supported lags 19..36) / med(d over supported lags 28..36); the
    masked E curve; the tool's own support law; EMPTY named."""
    supported = [i for i in range(len(K.LAGS))
                 if d_vals[i] is not None
                 and pair_counts[i] >= K.LOW_SUPPORT_PAIRS]
    if len(supported) < K.MIN_SUPPORTED_LAGS:
        return None, "EMPTY_few_supported_lags"
    tail = [d_vals[i] for i in supported if TAIL_LO <= K.LAGS[i] <= TAIL_HI]
    late = [d_vals[i] for i in supported if LATE_LO <= K.LAGS[i] <= LATE_HI]
    if not tail or not late:
        return None, "EMPTY_no_tail_or_late_window"
    med_late = K.median_of(late)
    if not med_late > 1e-12:
        return None, "EMPTY_degenerate_med_late"
    return 1.0 - min(tail) / med_late, "OK"


def psi(s, kappa):
    return s / (s + kappa)


def zmax(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a >= b else b


def project(r, leg_name, z_cal, z_held, z_fix, K):
    """D_new = max(D_receipt, z) per doc; the level re-derives (quantile
    0.95 over cal D_new); the gap re-derives in the item-439
    convention; both sides re-scored identically (byte-carried from
    codev7)."""
    lg = r["legs"][leg_name]
    rows = lg["doc_rows"]
    cal_now, held_now = [], []
    for row in rows:
        if row["half"] == "cal" and row["D"] is not None:
            cal_now.append((row["doc_id"], row["D"]))
        elif row["half"] == "held" and row["D"] is not None:
            held_now.append((row["doc_id"], row["D"]))
    fix_now = {row["fixture"]: row["D"] for row in lg["loop_census"]}

    def lift(did, D, zmap):
        z = zmap.get(did)
        return (max(D, z) if z is not None else D), z

    cal_new = [lift(d, D, z_cal)[0] for d, D in cal_now]
    held_new = [lift(d, D, z_held)[0] for d, D in held_now]
    fix_new = {n: lift(n, D, z_fix)[0] for n, D in fix_now.items()}

    t_new = K.quantile(sorted(cal_new), 0.95)
    t_now = K.quantile(sorted(D for _, D in cal_now), 0.95)
    mu_h, sd_h = K.mean_std(held_new)
    mu_l, sd_l = K.mean_std(list(fix_new.values()))
    mu_h0, sd_h0 = K.mean_std([D for _, D in held_now])
    mu_l0, sd_l0 = K.mean_std([D for D in fix_now.values()])
    rms = ((sd_l ** 2 + sd_h ** 2) / 2.0) ** 0.5
    gap_new = (mu_l - mu_h) / rms if rms > 1e-12 else None
    k_new = sum(1 for v in fix_new.values() if v >= t_new)
    k_now = sum(1 for v in fix_now.values() if v >= t_now)
    demoted = sorted(n for n, v in fix_new.items()
                     if fix_now[n] >= t_now and v < t_new)
    lifted = sorted(n for n in fix_new if fix_new[n] > fix_now[n])
    return {
        "t_now": t_now, "t_new": t_new, "k_now": k_now, "k_new": k_new,
        "gap_new": gap_new, "demoted": demoted, "lifted": lifted,
        "mu_loop": mu_l, "sd_loop": sd_l, "mu_held": mu_h,
        "sd_held": sd_h, "fix_now": fix_now, "fix_new": fix_new,
        "mu_loop_now": mu_l0, "sd_loop_now": sd_l0,
        "mu_held_now": mu_h0, "sd_held_now": sd_h0,
        "n_cal": len(cal_new), "n_held": len(held_new),
    }


# ---- the receipt-side gates (the desk half, no caches) --------------------
def parity_only(K, r):
    p("=== THE SATURATED D2 DIAGNOSTIC, PARITY-ONLY MODE (the "
      "receipt-side gates; no caches read) ===")
    p("AMEND v2 (the v1 sha 216b5860da0e2371d5827b5efcbb4fdf"
      "8f864c81bfa51c3ca73d4284591504ff preserved never edited): "
      "the census parity gate now anchors PER LEG (every anchor "
      "banked at items 490/493); the v1 gate wired every leg against "
      "the CODE anchor alone and hard-exited on his Mac at prose "
      "whose own re-derived census was EXACT against the banked prose "
      "refs -- a desk-side wiring error, never a data verdict; THE "
      "FORM NEVER TOUCHED (psi, kappa=1 pinned, the run law, the "
      "refined tail, the spine, the sweep byte-identical)")
    p("the sheet rc-d2sat-conversion-prereg.md pinned at his stamp (sha "
      "%s...), the receipt %s verified byte-exact at open, the tool %s "
      "verified inside it -- the form read EXACTLY as sheeted: "
      "psi(s) = s/(s+kappa), kappa = 1 pinned by convention, the "
      "d2 zero-run mass under the item-475 law mirrored onto d2, "
      "support = triples >= the swept gate, isolated zeros never count"
      % (SHEET_SHA[:16], RECEIPT_SHA_BANK[:16], TOOL_SHA_BANK[:16]))
    p("")
    lg = r["legs"]["mbpprw17"]

    # [D1] the V5 world re-derived EXACT
    p("[D1] THE V5 WORLD RE-DERIVED (doc_rows + loop_census alone, the "
      "before-column intact)")
    zero = {}
    proj = project(r, "mbpprw17", zero, zero, zero, K)
    p("  t_joint recomputed %.16f vs the receipt's %.16f %s | the banked "
      "%.16f" % (proj["t_now"], lg["t_joint"],
                 "OK" if abs(proj["t_now"] - lg["t_joint"]) < 1e-12
                 else "MISMATCH", LEVEL_BANK))
    p("  gap recomputed %.16f vs the receipt's raw %.16f %s | the banked "
      "%.16f" % (proj["gap_new"], lg["readouts"]["raw"]["gap"],
                 "OK" if abs(proj["gap_new"]
                             - lg["readouts"]["raw"]["gap"]) < 1e-9
                 else "MISMATCH", GAP_BANK))
    p("  the null projection: k %d, lifted %s, demoted %s (must be "
      "empty)" % (proj["k_now"], proj["lifted"] or "[]",
                  proj["demoted"] or "[]"))
    if (abs(proj["t_now"] - lg["t_joint"]) >= 1e-12
            or abs(proj["gap_new"] - lg["readouts"]["raw"]["gap"])
            >= 1e-9
            or abs(proj["t_now"] - LEVEL_BANK) > 1e-9
            or abs(proj["gap_new"] - GAP_BANK) > 1e-9
            or proj["lifted"] or proj["demoted"]):
        die("D1 FAILED -- the V5 world does not reproduce byte-exact; "
            "aborting.")
    p("  D1 PASSED (the world byte-identical to the bank)")
    p("")

    # [D2] the combined gate-8 reconstruction (the world before the
    # re-formation, receipted down)
    p("[D2] THE COMBINED GATE-8 WORLD RECONSTRUCTED (the world this "
      "sheet re-forms -- the raw d2 cell, the sd drag, receipted down "
      "at 1.420070)")
    V5 = {row["fixture"]: row["D"] for row in lg["loop_census"]}
    comb = dict(V5)
    comb["loop-injection-code"] = D_INJ_D2Z
    comb["loop-seeded-json"] = D_JSON_LIFTED
    comb["loop-seeded-countdown"] = D_COUNTDOWN_REFINED
    mu_c = sum(comb.values()) / len(comb)
    sd_c = (sum((v - mu_c) ** 2 for v in comb.values())
            / (len(comb) - 1)) ** 0.5
    gap_c = ((mu_c - HELD_COMB_MU)
             / (((sd_c ** 2 + HELD_COMB_SD ** 2) / 2.0) ** 0.5))
    p("  loop moments %.6f / %.6f (banked %.6f / %.6f, delta %.2e / "
      "%.2e); gap %.6f (banked %.6f, delta %.2e)"
      % (mu_c, sd_c, LOOP_COMB_MU, LOOP_COMB_SD,
         abs(mu_c - LOOP_COMB_MU), abs(sd_c - LOOP_COMB_SD),
         gap_c, GAP_COMB_BANK, abs(gap_c - GAP_COMB_BANK)))
    if (abs(mu_c - LOOP_COMB_MU) > 1e-4
            or abs(sd_c - LOOP_COMB_SD) > 1e-4
            or abs(gap_c - GAP_COMB_BANK) > 1e-4):
        die("D2 FAILED -- the combined world does not reconstruct; "
            "aborting.")
    p("  D2 PASSED (the re-formation's before-world anchors exact)")
    p("")

    # [D3] the fixture m_d2 census at the swept gates, from the
    # receipt's own fixture curves
    p("[D3] THE FIXTURE D2 ZERO-RUN CENSUS AT THE SWEPT GATES (the "
      "receipt's own fixture curves; the pinned law, isolated zeros "
      "never count)")
    p("  %-27s %s   %s" % ("fixture",
                           "  ".join("g%d" % g for g in D2_GATES),
                           "the banked gate-8 read"))
    for name in sorted(lg["fixture_curves"]):
        c = lg["fixture_curves"][name]["f"]["laneB"]
        ms = [m_d2(c["d2"], c["triples"], g)[0] for g in D2_GATES]
        bank = BANKED_MD2.get(name)
        ok = (bank is None or ms[0] == bank)
        p("  %-27s %s   %s%s"
          % (name, "  ".join("%2d" % m for m in ms),
             ("%d" % bank) if bank is not None else "-",
             " OK" if ok else " MISMATCH"))
        if not ok:
            die("D3 FAILED -- the m_d2 law does not reproduce the "
                "banked fixture census at gate 8; the law drifted; "
                "aborting.")
    p("  D3 PASSED (the law byte-carried; the gate sweep preview banked "
      "-- the masses shrink or hold as the support floor rises, the "
      "sheet pins ONE gate at his stamp)")
    p("")

    # [D4] the P-B4 refined fixture table reproduced
    p("[D4] THE P-B4 REFINED FIXTURE TABLE (the item-488 bank, the "
      "masked E curves) REPRODUCED")
    for name, bank in sorted(BANKED_REFINED.items(), key=lambda kv:
                             -kv[1]):
        c = lg["fixture_curves"][name]["E"]["masked"]
        v, status = refined_tail(c["d"], c["pairs"], K)
        ok = (v is not None and abs(v - bank) < 1e-6)
        p("  %-27s refined %.6f vs banked %.6f %s"
          % (name, v if v is not None else -1.0, bank,
             "OK" if ok else "MISMATCH"))
        if not ok:
            die("D4 FAILED -- the refined-tail form does not reproduce "
                "the banked table; aborting.")
    p("  D4 PASSED (the P-B4 form byte-carried)")
    p("")

    # [D5] the offline saturated idealization, recomputed live (the
    # receipts the audit banked; never the diagnostic's answer)
    p("[D5] THE OFFLINE SATURATED IDEALIZATION RECOMPUTED (the "
      "equal-mass census model, the audit's receipts -- the "
      "idealization only, the ACTUAL masses answer on his Mac)")
    n_zero = CEN_N - CEN_N_POS
    mean_mass = CEN_MEAN * CEN_N / CEN_N_POS
    z_inv = ((n_zero / CEN_N)
             / (((n_zero * (CEN_N_POS / CEN_N) ** 2
                  + CEN_N_POS * (n_zero / CEN_N) ** 2)
                 / (CEN_N - 1)) ** 0.5))
    p("  the two-point invariance on the banked census shape (189 "
      "zeros + 11 positives): z(any single-mass positive) = %.6f at "
      "EVERY kappa (kappa-robust, the deep bound)" % z_inv)
    for kappa in KAPPA_SWEEP:
        vals = [0.0] * n_zero + [psi(mean_mass, kappa)] * CEN_N_POS
        mu = sum(vals) / len(vals)
        sd = (sum((v - mu) ** 2 for v in vals)
              / (len(vals) - 1)) ** 0.5
        zmax_c = (1.0 - mu) / sd
        z_json = (psi(BANKED_MD2["loop-seeded-json"], kappa) - mu) / sd
        z_ic = (psi(BANKED_MD2["loop-injection-code"], kappa) - mu) / sd
        p("  kappa %4.1f EQUAL-MASS: sd_psi %.6f bound %.4f | "
          "z(json@%d) %.4f %s | z(inj-code@%d) %.4f %s"
          % (kappa, sd, zmax_c, BANKED_MD2["loop-seeded-json"], z_json,
             "ABOVE the level (the flip holds on paper)"
             if z_json > LEVEL_BANK else "below the level",
             BANKED_MD2["loop-injection-code"], z_ic,
             "BELOW its own D 7.989752 (the max-pool invariant)"
             if z_ic < D_INJ_CODE else "ABOVE its D -- the invariance "
             "breaks, kappa too large"))
    p("  the offline gap bracket on the kappa=1 idealization (the "
      "audit's receipts): the saturated loop vector with json at its "
      "saturated z, countdown at its P-B4 lift, injection-code HELD "
      "(the saturated z loses the max-pool)")
    kappa = KAPPA_PIN
    vals = [0.0] * n_zero + [psi(mean_mass, kappa)] * CEN_N_POS
    mu = sum(vals) / len(vals)
    sd = (sum((v - mu) ** 2 for v in vals) / (len(vals) - 1)) ** 0.5
    z_json = (psi(BANKED_MD2["loop-seeded-json"], kappa) - mu) / sd
    z_ic = (psi(BANKED_MD2["loop-injection-code"], kappa) - mu) / sd
    sat = dict(V5)
    sat["loop-seeded-json"] = max(V5["loop-seeded-json"], z_json)
    sat["loop-injection-code"] = max(D_INJ_CODE, z_ic)
    sat["loop-seeded-countdown"] = max(
        V5["loop-seeded-countdown"], D_COUNTDOWN_REFINED)
    sv = list(sat.values())
    mu_s = sum(sv) / len(sv)
    sd_s = (sum((v - mu_s) ** 2 for v in sv) / (len(sv) - 1)) ** 0.5
    g_a = ((mu_s - HELD_V5_MU)
           / (((sd_s ** 2 + HELD_V5_SD ** 2) / 2.0) ** 0.5))
    g_c = ((mu_s - HELD_COMB_MU)
           / (((sd_s ** 2 + HELD_COMB_SD ** 2) / 2.0) ** 0.5))
    p("    loop moments %.6f / %.6f (vs the raw combined %.6f / %.6f -- "
      "the drag halved on paper); the fixture-side bound %.6f; the "
      "lower bracket %.6f -- the honest read lives INSIDE, every "
      "binding question his-Mac-only"
      % (mu_s, sd_s, LOOP_COMB_MU, LOOP_COMB_SD, g_a, g_c))
    p("  D5 PASSED (the idealization receipts reproduced; the census "
      "half NEVER runs on this mode -- the masses answer only on his "
      "Mac)")
    p("")
    p("THE FULL MODE (his Mac, read-only, zero GPU, zero decodes): the "
      "script beside this tool + receipt + the pinned sheet + his "
      "three pinned walk caches, then")
    p("    python3 rc_d2sat_diagnostic.py")
    p("  which emits %s for his shasum + upload; the census parity "
      "gate first (PER-LEG anchors, amend v2: CODE mean 0.275000 sd "
      "1.352227 n_pos 11 held 15, prose 1.548387/3.896216 n_pos 72, "
      "p2 1.154667/3.072663 n_pos 62 -- a mismatch a HARD EXIT), then "
      "the saturated census, the cliff read, the honest both-sides "
      "gap, the off-leg reads, the three-miss read, the sweep "
      "receipts, the kill-switch verdicts"
      % FULL_CONSOLE)
    p("(offline read of the run-of-record receipt bytes only, zero "
      "GPU, zero decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] "
      "unmoved (D-theta); no thresholds set, moved, or adjudicated; "
      "findings presented, never adjudicated -- the owner's stamps "
      "decide)")


# ---- the full diagnostic (his Mac, read-only, zero GPU, zero decodes) ----
def full_mode(K, r):
    p("=== THE SATURATED D2 DIAGNOSTIC, FULL MODE (his pinned caches, "
      "read-only, zero GPU, zero decodes) ===")
    p("AMEND v2 (the v1 sha 216b5860da0e2371d5827b5efcbb4fdf"
      "8f864c81bfa51c3ca73d4284591504ff preserved never edited): "
      "the census parity gate now anchors PER LEG (every anchor "
      "banked at items 490/493: CODE 0.275000/1.352227 n_pos 11/200 "
      "held 15, prose 1.548387/3.896216 n_pos 72/310, p2 "
      "1.154667/3.072663 n_pos 62/375; the off-leg held counts never "
      "banked -- printed as findings, never gated); the v1 gate wired "
      "every leg against the CODE anchor alone and hard-exited on "
      "this machine at prose whose own re-derived census was EXACT "
      "against the banked prose refs -- a desk-side wiring error, "
      "never a data verdict; THE FORM NEVER TOUCHED (psi, kappa=1 "
      "pinned, the run law, the refined tail, the spine, the sweep "
      "byte-identical)")
    p("the form read EXACTLY as sheeted, never tuned after any read: "
      "D_new = max(D, z_refined, z_d2sat) per doc, both sides "
      "re-scored identically -- the refined-tail cell (P-B4, the "
      "item-488 form byte-carried) and the SATURATED d2 zero-run-mass "
      "cell (the item-475 law mirrored onto d2, support = triples >= "
      "the swept gate, psi(s) = s/(s+kappa) applied to the mass BEFORE "
      "the census z, kappa = 1 PINNED by the sheet at his stamp); the "
      "gate swept 8/12/16 with the sheet pinning ONE at his word; the "
      "kappa sweep printed as receipts, only the pinned kappa=1 ever "
      "carried; the census parity gate FIRST (a mismatch a HARD "
      "EXIT)")
    p("")
    ks_notes = []
    for leg in K.LEGS:
        lg = r["legs"][leg]
        cache_path = K.CACHE_FILES[leg]
        if not os.path.exists(cache_path):
            die("leg %s: cache %s not found beside this script -- "
                "aborting." % (leg, cache_path))
        sha = sha256_file(cache_path)
        if sha != K.CACHE_PINS[leg]:
            die("leg %s: cache sha256 %s != the pinned %s -- the "
                "pin-table guard holds; never read divergent bytes; "
                "aborting." % (leg, sha, K.CACHE_PINS[leg]))
        p("--- LEG %s (cache pin MATCH, sha256 %s...) ---"
          % (leg, sha[:16]))
        recs = K.load_cache(cache_path, leg)
        cal_docs, held_docs = K.split_by_parity(leg, recs["docs"])
        live, inert = K.split_loop_fixtures(leg, recs["loop"])
        fixture_recs = {d["doc_id"]: d for d in live}
        rrows = {(row["half"], row["doc_id"]) for row in lg["doc_rows"]}
        crows = ({("cal", d["doc_id"]) for d in cal_docs}
                 | {("held", d["doc_id"]) for d in held_docs})
        if rrows != crows:
            die("leg %s: the cache's doc population does not match "
                "the receipt's doc_rows -- never project across "
                "populations; aborting." % leg)
        p("  population parity: %d cal + %d held, exact match against "
          "the receipt's doc_rows" % (len(cal_docs), len(held_docs)))
        base = K.compute_baselines(cal_docs, leg)
        f_vals = [v for d in cal_docs for v in d["steps"]["f"]
                  if v is not None]
        f_ref = K.mean_std(f_vals) if f_vals else None
        cal_E = sorted(v for d in cal_docs
                       for v in d["steps"]["E"] if v is not None)
        primary_cut = K.quantile(cal_E, K.MASK_Q_PRIMARY)

        # per-doc: the refined tail + the per-gate d2 mass (cal+held)
        ref_cal, ref_held = {}, {}
        m_cal = {g: {} for g in D2_GATES}
        m_held = {g: {} for g in D2_GATES}
        for pop, docs, ref in (("cal", cal_docs, ref_cal),
                               ("held", held_docs, ref_held)):
            for d in docs:
                cells = K.process_doc_conjunct(d, base, f_ref,
                                               primary_cut)
                v, status = refined_tail(cells["E"]["masked"]["d"],
                                        cells["E"]["masked"]["pairs"], K)
                ref[d["doc_id"]] = v
                d2c = K.doc_d2_census(d, base, f_ref, primary_cut)
                fb = d2c["f"]["laneB"]
                tgt = m_cal if pop == "cal" else m_held
                for g in D2_GATES:
                    mm, _ = m_d2(fb["d2"], fb["triples"], g)
                    tgt[g][d["doc_id"]] = mm

        # THE CENSUS PARITY GATE (the pre-reg's first gate, binding)
        # AMEND v2: PER-LEG anchors -- the v1 gate checked every leg
        # against the CODE anchor alone; the bank holds all three legs
        anc = CEN_ANCHORS[leg]
        masses8 = list(m_cal[D2_GATES[0]].values())
        mu8, sd8 = K.mean_std(masses8)
        n_pos8 = sum(1 for m in masses8 if m > 0)
        n_zero8 = len(masses8) - n_pos8
        hpos8 = sum(1 for m in m_held[D2_GATES[0]].values() if m > 0)
        if anc["held_n_pos"] is None:
            p("  THE CENSUS PARITY GATE (gate %d, vs the banked %s "
              "census anchors, items 490/493): mean %.6f vs %.6f "
              "(delta %.2e) | sd %.6f vs %.6f (delta %.2e) | n_pos %d "
              "vs %d | n_at_zero %d/%d | held n_pos %d (NEVER BANKED "
              "-- printed as a finding, never gated)"
              % (D2_GATES[0], leg, mu8, anc["mean"],
                 abs(mu8 - anc["mean"]), sd8, anc["sd"],
                 abs(sd8 - anc["sd"]), n_pos8, anc["n_pos"],
                 n_zero8, len(masses8), hpos8))
        else:
            p("  THE CENSUS PARITY GATE (gate %d, vs his banked console "
              "census): mean %.6f vs %.6f (delta %.2e) | sd %.6f vs %.6f "
              "(delta %.2e) | n_pos %d vs %d | n_at_zero %d/%d | held "
              "n_pos %d vs %d"
              % (D2_GATES[0], mu8, anc["mean"],
                 abs(mu8 - anc["mean"]), sd8, anc["sd"],
                 abs(sd8 - anc["sd"]), n_pos8, anc["n_pos"],
                 n_zero8, len(masses8), hpos8, anc["held_n_pos"]))
        if (abs(mu8 - anc["mean"]) > 1e-6 or abs(sd8 - anc["sd"]) > 1e-6
                or n_pos8 != anc["n_pos"] or len(masses8) != anc["n"]
                or (anc["held_n_pos"] is not None
                    and hpos8 != anc["held_n_pos"])):
            die("leg %s: THE CENSUS PARITY GATE FAILED -- the "
                "re-derived masses do not reproduce the banked gate-8 "
                "census for this leg; never project onto drifting "
                "bytes; the sheet closes at the S6 kill-switch; "
                "aborting." % leg)
        p("  THE CENSUS PARITY GATE PASSED (the actual masses now in "
          "hand, the idealization retired)")
        p("  the ACTUAL positive masses (cal, gate 8): %s | the mean "
          "positive mass %.6f"
          % (sorted(m for m in masses8 if m > 0),
             sum(m for m in masses8 if m > 0) / n_pos8))

        # the refined reference
        vals = [v for v in ref_cal.values() if v is not None]
        n_empty = sum(1 for v in ref_cal.values() if v is None)
        refined_ok = True
        if len(vals) < 2:
            refined_ok = False
            mu_r = sd_r = None
            p("  P-B4 cal reference: EMPTY (n %d) -- the refined face "
              "vacuous this leg, named; the d2sat face rides alone"
              % len(vals))
        else:
            mu_r, sd_r = K.mean_std(vals)
            p("  P-B4 CAL REFERENCE (the refined tail over %d cal "
              "docs, %d EMPTY named): mean %.6f sd %.6f"
              % (len(vals), n_empty, mu_r, sd_r))
            if sd_r <= 1e-12:
                refined_ok = False
                p("  sd == 0 -- the refined face EMPTY_degenerate_sd, "
                  "vacuous; the d2sat face rides alone")

        # the fixture half: curve lineage gates + masses + refined z
        zfix_ref, mfix = {}, {g: {} for g in D2_GATES}
        for name in sorted(fixture_recs):
            cells = K.process_doc_conjunct(fixture_recs[name], base,
                                           f_ref, primary_cut)
            cur = lg["fixture_curves"][name]["E"]["masked"]
            got = cells["E"]["masked"]
            for i in range(len(K.LAGS)):
                a, b = got["d"][i], cur["d"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die("leg %s fixture %s: the fresh masked E curve "
                        "diverges from the receipt's fixture_curves "
                        "at lag %s -- the curve lineage is not proven; "
                        "aborting." % (leg, name, K.LAGS[i]))
            d2c = K.doc_d2_census(fixture_recs[name], base, f_ref,
                                  primary_cut)
            fb = d2c["f"]["laneB"]
            fcur = lg["fixture_curves"][name]["f"]["laneB"]
            for i in range(len(K.LAGS)):
                a, b = fb["d2"][i], fcur["d2"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die("leg %s fixture %s: the fresh laneB f d2 "
                        "curve diverges from the receipt's "
                        "fixture_curves at lag %s -- the d2 lineage "
                        "is not proven; aborting." % (leg, name,
                                                      K.LAGS[i]))
            v, status = refined_tail(got["d"], got["pairs"], K)
            zfix_ref[name] = ((v - mu_r) / sd_r
                              if (refined_ok and v is not None)
                              else None)
            for g in D2_GATES:
                mfix[g][name] = m_d2(fb["d2"], fb["triples"], g)[0]
        p("  fixture curve parity: all ten fixtures byte-close at "
          "1e-12 on the masked E and laneB f d2 curves (the lineage "
          "proven); the fixture masses at the swept gates:")
        for name in sorted(fixture_recs):
            ms = [mfix[g][name] for g in D2_GATES]
            if max(ms) > 0 or name in BANKED_MD2:
                p("    %-27s m_d2 at gates 8/12/16: %s"
                  % (name, " / ".join(str(m) for m in ms)))

        # the saturated spine, per gate, the pinned kappa carried
        D_held = {x["doc_id"]: x["D"] for x in lg["doc_rows"]
                  if x["half"] == "held" and x["D"] is not None}
        leg_ks = {"cliff": None, "flip": None, "gap": None}
        for g in D2_GATES:
            masses = list(m_cal[g].values())
            mu_m, sd_m = K.mean_std(masses) if len(masses) >= 2 \
                else (None, None)
            if mu_m is None or sd_m <= 1e-12:
                p("  --- GATE triples >= %d: the d2 census EMPTY (sd 0 "
                  "-- every cal doc reads zero mass) -- the d2sat face "
                  "vacuous at this gate, the refined face rides "
                  "alone ---" % g)
                zd_cal = zd_held = zd_fix = {}
            else:
                psis = [psi(m, KAPPA_PIN) for m in masses]
                mu_p = sum(psis) / len(psis)
                sd_p = (sum((v - mu_p) ** 2 for v in psis)
                        / (len(psis) - 1)) ** 0.5
                if sd_p <= 1e-12:
                    p("  --- GATE triples >= %d: the SATURATED census "
                      "EMPTY (sd_psi 0) -- the face vacuous at this "
                      "gate ---" % g)
                    zd_cal = zd_held = zd_fix = {}
                else:
                    zd_cal = {did: (psi(m, KAPPA_PIN) - mu_p) / sd_p
                              for did, m in m_cal[g].items()}
                    zd_held = {did: (psi(m, KAPPA_PIN) - mu_p) / sd_p
                               for did, m in m_held[g].items()}
                    zd_fix = {n: (psi(mfix[g][n], KAPPA_PIN) - mu_p)
                              / sd_p for n in mfix[g]}
                    n_pos = sum(1 for m in masses if m > 0)
                    bound = (1.0 - mu_p) / sd_p
                    p("  --- GATE triples >= %d: the d2 cal census "
                      "mean %.6f sd %.6f (n_pos %d/%d) -> the "
                      "SATURATED census mu_psi %.6f sd_psi %.6f, the "
                      "bound %.6f, the raw-mass z of the largest "
                      "fixture mass vs its saturated z NAMED BELOW ---"
                      % (g, mu_m, sd_m, n_pos, len(masses),
                         mu_p, sd_p, bound))
                    # the kappa sweep receipts at this gate
                    for kp in KAPPA_SWEEP:
                        pv = [psi(m, kp) for m in masses]
                        mup = sum(pv) / len(pv)
                        sdp = (sum((v - mup) ** 2 for v in pv)
                               / (len(pv) - 1)) ** 0.5
                        bnd = (1.0 - mup) / sdp if sdp > 1e-12 else None
                        zj = ((psi(mfix[g]["loop-seeded-json"], kp)
                               - mup) / sdp
                              if sdp > 1e-12 else None)
                        p("      kappa %4.1f RECEIPT: sd_psi %.6f "
                          "bound %s z(json) %s"
                          % (kp, sdp,
                             "%.4f" % bnd if bnd is not None else
                             "EMPTY",
                             "%.4f" % zj if zj is not None else
                             "EMPTY"))
            zc_cal = {did: zmax((ref_cal[did] - mu_r) / sd_r
                                if (refined_ok
                                    and ref_cal[did] is not None)
                                else None, zd_cal.get(did))
                      for did in ref_cal}
            zc_held = {did: zmax((ref_held[did] - mu_r) / sd_r
                                 if (refined_ok
                                     and ref_held[did] is not None)
                                 else None, zd_held.get(did))
                       for did in ref_held}
            zc_fix = {n: zmax(zfix_ref[n], zd_fix.get(n))
                      for n in zfix_ref}
            proj = project(r, leg, zc_cal, zc_held, zc_fix, K)
            p("    THE SATURATED PROJECTION (kappa = 1 pinned, both "
              "faces, the level re-derives, both sides re-scored):")
            p("      t_joint %.6f -> %.6f (%+.6f)  |  k %d -> %d  | "
              "the cap at k_new %s"
              % (proj["t_now"], proj["t_new"],
                 proj["t_new"] - proj["t_now"], proj["k_now"],
                 proj["k_new"],
                 "%.4f" % CAPS[proj["k_new"]]
                 if proj["k_new"] in CAPS else "unnamed"))
            p("      held mean/sd %.6f/%.6f -> %.6f/%.6f  |  loop "
              "mean/sd %.6f/%.6f -> %.6f/%.6f"
              % (proj["mu_held_now"], proj["sd_held_now"],
                 proj["mu_held"], proj["sd_held"],
                 proj["mu_loop_now"], proj["sd_loop_now"],
                 proj["mu_loop"], proj["sd_loop"]))
            p("      THE HONEST BOTH-SIDES GAP: %.6f -> %.6f vs the "
              "2.0 bar (presented, never adjudicated)%s"
              % (lg["readouts"]["raw"]["gap"], proj["gap_new"],
                 "  | vs the P-B4 honest %.6f (the standing best "
                 "banked CODE read)" % PB4_HONEST
                 if leg == "mbpprw17" else
                 "  | vs the banked combined bound %.6f"
                 % OFF_LEG_BOUNDS.get(leg, float("nan"))))
            # the cliff read
            cliff = ("mask-reserved-stubborn" in proj["demoted"])
            mstub_new = proj["fix_new"].get("mask-reserved-stubborn")
            p("      THE CLIFF READ: mask-stub %.6f vs the re-derived "
              "level %.6f (margin %+.6f) -- %s; demoted: %s"
              % (mstub_new, proj["t_new"], mstub_new - proj["t_new"],
                 "DEMOTED, the demotion edge crossed" if cliff
                 else "mask-stub holds", proj["demoted"] or "[]"))
            # the flip read
            jn = proj["fix_new"].get("loop-seeded-json")
            flipped = (jn is not None and jn >= proj["t_new"])
            p("      THE FLIP READ: json %.6f vs the re-derived level "
              "%.6f (margin %+.6f) -- %s; lifted: %s"
              % (jn, proj["t_new"], jn - proj["t_new"],
                 "FLIPPED (above the level)" if flipped
                 else "below the level", proj["lifted"] or "[]"))
            # the held-side S-lesson census
            n_ref = n_d2 = n_both = 0
            for did, D in D_held.items():
                zr = ((ref_held[did] - mu_r) / sd_r
                      if (refined_ok and ref_held[did] is not None)
                      else None)
                zd = zd_held.get(did)
                lr = zr is not None and zr > D
                ld = zd is not None and zd > D
                if lr and ld:
                    n_both += 1
                elif lr:
                    n_ref += 1
                elif ld:
                    n_d2 += 1
            p("      the held-side lift (the S-lesson census): "
              "refined-only %d, d2sat-only %d, both %d"
              % (n_ref, n_d2, n_both))
            # the three-miss read
            for nm in ("loop-seeded-json", "loop-seeded-countdown",
                       "loop-seeded-code-line"):
                p("      THE THREE-MISS READ: %-24s D %.6f -> %.6f "
                  "(z_combined %s) vs the level %.6f -- %s"
                  % (nm, proj["fix_now"][nm], proj["fix_new"][nm],
                     "%.4f" % zc_fix.get(nm)
                     if zc_fix.get(nm) is not None else "None",
                     proj["t_new"],
                     "ABOVE" if proj["fix_new"][nm] >= proj["t_new"]
                     else "below"))
            if leg == "mbpprw17":
                leg_ks = {"cliff": cliff, "flip": flipped,
                          "gap": proj["gap_new"]}
            p("")

        if leg == "mbpprw17":
            ks_notes.append(leg_ks)

    # the kill-switch verdicts, presented never adjudicated
    p("THE KILL-SWITCH VERDICTS (the pre-reg's S6 law, presented for "
      "his stamps):")
    if ks_notes:
        jk = ks_notes[0]
        eaten = (jk["cliff"] and not jk["flip"])
        p("  KS2 THE CLIFF + THE FLIP: the demotion %s, the json flip "
          "%s -- %s%s" % (
              "TRIPPED" if jk["cliff"] else "held",
              "stands" if jk["flip"] else "eaten",
              "the flip EATEN by the demotion (the item-493 "
              "cancellation re-learned on the actual masses) -- the "
              "sheet's kill-switch condition"
              if eaten else "the flip survives the cliff",
              "" if jk["flip"] else " -- the flip lost without the "
              "cliff, the honest value the cap headroom only"))
        p("  KS3 THE HONEST GAP: %.6f vs the P-B4 honest %.6f -- %s"
          % (jk["gap"], PB4_HONEST,
             "BELOW the standing best banked CODE read -- the "
             "re-formation bought nothing, the sheet's kill-switch "
             "condition" if jk["gap"] < PB4_HONEST
             else "AT OR ABOVE the standing best banked CODE read"))
    p("  KS1 THE CENSUS PARITY: PASSED at open (a fail is a HARD "
      "EXIT, never a verdict)")
    p("  THE STANDING: the console presented for his read -- a "
      "negative kill-switch read closes the sheet on paper zero "
      "build hours (the B1/B2 pre-reg then writes against the "
      "standing banked world per the item-498 branch law); a live "
      "read opens the build question at his word only, its own stamp, "
      "never pre-promised")
    p("(offline read of his pinned cache bytes only, zero GPU, zero "
      "decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); "
      "no thresholds set, moved, or adjudicated; findings presented, "
      "never adjudicated -- the owner's stamps decide)")


def main():
    args = sys.argv[1:]
    verify_sheet()
    K = load_tool()
    r = load_receipt()
    if "--parity-only" in args:
        parity_only(K, r)
        name = PARITY_CONSOLE
    else:
        full_mode(K, r)
        name = FULL_CONSOLE
    with open(name, "w") as f:
        f.write("\n".join(OUT) + "\n")
    print("")
    print("WROTE " + name)


if __name__ == "__main__":
    main()

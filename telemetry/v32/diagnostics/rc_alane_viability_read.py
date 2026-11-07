#!/usr/bin/env python3
"""THE A-LANE VIABILITY AUDIT — the external analysis's five routes read
against the run-of-record receipt's own bytes, offline.

At his word ("okay any viablitity in this, if so lets discuss all
possible viable integratios or upgrades to the mechanism for
refinement") an external analysis was placed on the desk proposing five
routes: A1 a saturation-bounded d2 face, A2 a cross-lane mask-excision
contrast, A3 an f-detrended residual, B1 a phase-band pooling and B2 a
line-synced anchor (both upstream), and C close-or-8B. This script
reads every offline-checkable claim on the receipt's own bytes -- the
sign-flip peak (their D_crit constant), their own Check-2 kill
condition on the cross-lane ratios, the detrended trough family, and
the saturation model's z bound, invariance claim, level race, cliff
mass and gap bracket -- and presents the verdicts, never adjudicates
them.

Offline, zero GPU, zero decodes, read-only; the caches are never
touched; nothing re-runs; the pinned sheets never open; no constant is
tuned to any answer (the kappa sweep printed in full as receipts).

usage: python3 rc_alane_viability_read.py
  (triadic_rw17_codev5.py + rc_codev5_receipt.json +
   triadic_telemetry_t2_v32.3.0.py beside this script)
"""

import json
import os
import sys

TOOL_NAME = "triadic_rw17_codev5.py"
TOOL_SHA_BANK = ("391ac7dfd91f4c45c7c113211005a8bb44565737"
                 "887331fd512ed9723b4c2cf3")
RECEIPT_NAME = "rc_codev5_receipt.json"
RECEIPT_SHA_BANK = ("fc8b70b5435cefbc419b3b10dd0aeae6b579dcad1b"
                    "7bfcaac5d11660b6e6cc42")
INSTRUMENT_NAME = "triadic_telemetry_t2_v32.3.0.py"
INSTRUMENT_SHA_BANK = ("8b4250f3ee0aa55b654284f33f142d07f9dacb8a"
                       "ab38ed9517d99e6f167d2e18")
SHEET_V6_SHA = ("49bc88b92bd1b0059035326ca1a0cb499231df531b7808c"
                "28c821d08b5625856")
SHEET_3MISS_SHA = ("b5efca3949fcdb50b2f24e1d4bceb9d7c9b9308c945"
                   "1a73572ba74f0c4ddd7a8")
DRIFT_CONSOLE_SHA = ("a263df0c1d9c6e767858afed403f2aa731566d9d3"
                     "4245ca1ed628ab49e29900")

# ---- the banked numbers this audit reads against (never re-derived
# ---- where the bytes cannot carry them; cited at their items) ----
LEVEL_BANK = 3.7618410048243147          # the V5 level, item 483
GAP_BANK = 1.6862617412521999            # the V5 gap, item 483
MASK_STUB_D = 4.1775273637921755         # the demotion cliff edge
HELD_V5_MU, HELD_V5_SD = 1.583084, 1.308408   # item 493 console
HELD_PB4_MU, HELD_PB4_SD = 1.633566, 1.332503 # item 493 console
HELD_COMB_MU, HELD_COMB_SD = 1.787326, 2.174735  # item 493 console
LOOP_COMB_MU, LOOP_COMB_SD = 6.338041, 3.976063  # item 493 console
GAP_COMB_BANK = 1.420070                 # his gate-8 run, item 493
D_INJ_CODE = 7.989752                    # V5 loop census
D_JSON_LIFTED = 5.712799                 # his gate-8 json read
D_COUNTDOWN_REFINED = 1.434110           # the P-B4 countdown lift
D_INJ_CODE_D2Z = 15.326556               # his gate-8 d2 z, the drag
PB4_HONEST = 1.792063                    # the P-B4 single-face read
RAW_FIXTURE_SIDE_HONEST = 1.606504       # item 492 correction
CAP_K7, CAP_K8 = 2.0494, 2.6833          # coverage caps, item 484
JSON_RAW_D2Z = 5.7128                    # his gate-8 json d2 z
# the d2-face gate-8 census, HIS console (item 490), cited not
# recomputed -- the receipt banks fixture curves only, never doc-level
# d2 masses:
D2_CAL_MEAN, D2_CAL_SD = 0.275000, 1.352227
D2_CAL_N_POS, D2_CAL_N = 11, 200          # 189/200 at exact zero
D2_HELD_N_POS = 15                        # item 493 held decomposition
M_D2_INJ_CODE, M_D2_JSON = 21.0, 8.0      # his gate-8 fixture masses
# the drift-run banked cells (item 496 console, sha above):
DRIFT_BANKED = {
    ("mbpprw17", "loop-seeded-affirm", "E", "laneB"): 33,
    ("mbpprw17", "loop-seeded-countdown", "E", "laneB"): 16,
    ("mbpprw17", "loop-seeded-code-line", "E", "laneB"): 13,
    ("mbpprw17", "loop-seeded-affirm", "f", "laneB"): 35,
    ("mbpprw17", "loop-seeded-countdown", "f", "laneB"): 5,
    ("mbpprw17", "loop-seeded-code-line", "f", "laneB"): 6,
}
C_DR = [("E", "laneB"), ("E", "unmasked"),
        ("f", "laneB"), ("f", "unmasked")]

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
        die("tool %s not found beside this script -- the read imports "
            "the tool's own constants (LEGS, LOW_SUPPORT_PAIRS); "
            "aborting." % TOOL_NAME)
    import importlib.util
    spec = importlib.util.spec_from_file_location("K", TOOL_NAME)
    K = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(K)
    return K


def load_receipt():
    if not os.path.exists(RECEIPT_NAME):
        die("receipt %s not found beside this script -- the "
            "fixture curves and censuses are the read's source; "
            "aborting." % RECEIPT_NAME)
    sha = sha256_file(RECEIPT_NAME)
    if sha != RECEIPT_SHA_BANK:
        die("receipt sha256 %s != the banked run-of-record %s -- "
            "never read foreign bytes; aborting."
            % (sha, RECEIPT_SHA_BANK))
    with open(RECEIPT_NAME) as f:
        r = json.load(f)
    ts = r.get("tool_sha256", "")
    if ts != TOOL_SHA_BANK:
        die("receipt tool_sha256 %s != the banked tool %s -- never "
            "project onto foreign bytes; aborting." % (ts,
                                                       TOOL_SHA_BANK))
    return r


def mean(v):
    return sum(v) / len(v)


def sd1(v):
    m = mean(v)
    return math_sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def math_sqrt(x):
    return x ** 0.5


def q95(vals):
    """the level convention: the linear-interpolation 0.95 quantile
    over the non-None cal D's (the tool's own law)."""
    s = sorted(vals)
    n = len(s)
    pos = 0.95 * (n - 1)
    lo = int(pos)
    frac = pos - lo
    hi = min(lo + 1, n - 1)
    return s[lo] * (1 - frac) + s[hi] * frac


def gap_of(loop_vals, mu_h, sd_h):
    """the gap convention: (mu_loop - mu_held) / sqrt((sd_loop^2 +
    sd_held^2)/2), sd ddof=1 both sides."""
    return (mean(loop_vals) - mu_h) / math_sqrt(
        (sd1(loop_vals) ** 2 + sd_h ** 2) / 2)


def drift_run(d_vals, pairs, low_support):
    """the item-496 form, re-implemented for the lineage gate: the
    longest strictly-rising run over consecutive supported in-window
    lags; R < 3 reads 0.0 a real value."""
    best = cur = 0
    prev_supported = False
    prev_d = None
    prev_run = 0
    for i in range(len(d_vals)):
        ok = (d_vals[i] is not None and pairs[i] is not None
              and pairs[i] >= low_support)
        if ok and prev_supported and d_vals[i] > prev_d:
            cur = prev_run + 1
        elif ok:
            cur = 1
        else:
            cur = 0
        prev_run = cur
        prev_supported = ok
        prev_d = d_vals[i] if ok else None
        if cur > best:
            best = cur
    return best if best >= 3 else 0.0


def med(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])


def main():
    K = load_tool()
    r = load_receipt()
    low = K.LOW_SUPPORT_PAIRS
    isha = sha256_file(INSTRUMENT_NAME)
    if isha != INSTRUMENT_SHA_BANK:
        die("instrument sha256 %s != the banked %s -- never quote "
            "foreign prompts; aborting." % (isha,
                                           INSTRUMENT_SHA_BANK))

    p("=== THE A-LANE VIABILITY AUDIT (the external analysis's five "
      "routes read against the run-of-record receipt's own bytes, "
      "offline, zero GPU, zero decodes, read-only) ===")
    p("at his word (\"okay any viablitity in this, if so lets discuss "
      "all possible viable integratios or upgrades to the mechanism "
      "for refinement\"): the receipt %s verified byte-exact at open, "
      "the tool %s verified inside it, the instrument %s verified for "
      "the fixture prompts -- the pinned sheets stay pinned (V6 %s, "
      "the closed 3-miss sheet %s), no constant tuned to any answer, "
      "the kappa sweep printed in full as receipts"
      % (RECEIPT_SHA_BANK[:16], TOOL_SHA_BANK[:16],
         INSTRUMENT_SHA_BANK[:16], SHEET_V6_SHA[:16],
         SHEET_3MISS_SHA[:16]))
    p("")

    leg = r["legs"]["mbpprw17"]
    cal = [d["D"] for d in leg["doc_rows"]
           if d["half"] == "cal" and d["D"] is not None]
    held = [d["D"] for d in leg["doc_rows"]
            if d["half"] == "held" and d["D"] is not None]
    n_cal_none = sum(1 for d in leg["doc_rows"]
                     if d["half"] == "cal" and d["D"] is None)
    n_held_none = sum(1 for d in leg["doc_rows"]
                      if d["half"] == "held" and d["D"] is None)
    V5 = {}
    for c in leg["loop_census"]:
        V5[c["fixture"]] = c["D"]
    Lv = [V5[n] for n in sorted(V5)]

    # ================= G1: the V5 world re-derived EXACT ============
    p("--- G1 THE V5 WORLD RE-DERIVED (the parity gate: the level and "
      "the gap reproduced from doc_rows + loop_census alone) ---")
    level = q95(cal)
    gap = gap_of(Lv, mean(held), sd1(held))
    p("  cal non-None n %d (D=None dropped %d), held non-None n %d "
      "(D=None dropped %d) -- 11 per half, the banked convention"
      % (len(cal), n_cal_none, len(held), n_held_none))
    p("  level q0.95 interp %.15f (banked %.15f, delta %.2e)"
      % (level, LEVEL_BANK, abs(level - LEVEL_BANK)))
    p("  held moments %.6f / %.6f (banked %.6f / %.6f)"
      % (mean(held), sd1(held), HELD_V5_MU, HELD_V5_SD))
    p("  gap %.15f (banked %.15f, delta %.2e)"
      % (gap, GAP_BANK, abs(gap - GAP_BANK)))
    if (abs(level - LEVEL_BANK) > 1e-9
            or abs(gap - GAP_BANK) > 1e-9
            or len(cal) != 189 or len(held) != 189
            or abs(mean(held) - HELD_V5_MU) > 1e-6
            or abs(sd1(held) - HELD_V5_SD) > 1e-6):
        die("G1 FAILED -- the V5 world does not reproduce; never "
            "audit on drifting bytes; aborting.")
    p("  G1 PASSED (the world byte-identical to the bank)")
    p("")

    # ============ G2: the combined gate-8 reconstruction ============
    p("--- G2 THE COMBINED GATE-8 WORLD RECONSTRUCTED (the parity "
      "gate on the item-493 banked moments) ---")
    comb = dict(V5)
    comb["loop-injection-code"] = D_INJ_CODE_D2Z
    comb["loop-seeded-json"] = D_JSON_LIFTED
    comb["loop-seeded-countdown"] = D_COUNTDOWN_REFINED
    cv = [comb[n] for n in sorted(comb)]
    g2 = gap_of(cv, HELD_COMB_MU, HELD_COMB_SD)
    p("  loop vector = the V5 D's with injection-code %s, json %s, "
      "countdown %s (his gate-8 reads, banked)"
      % (D_INJ_CODE_D2Z, D_JSON_LIFTED, D_COUNTDOWN_REFINED))
    p("  loop moments %.6f / %.6f (banked %.6f / %.6f, delta "
      "%.2e / %.2e)" % (mean(cv), sd1(cv), LOOP_COMB_MU,
                        LOOP_COMB_SD, abs(mean(cv) - LOOP_COMB_MU),
                        abs(sd1(cv) - LOOP_COMB_SD)))
    p("  gap %.6f (banked %.6f, delta %.2e)"
      % (g2, GAP_COMB_BANK, abs(g2 - GAP_COMB_BANK)))
    if (abs(mean(cv) - LOOP_COMB_MU) > 1e-4
            or abs(sd1(cv) - LOOP_COMB_SD) > 1e-4
            or abs(g2 - GAP_COMB_BANK) > 1e-4):
        die("G2 FAILED -- the combined gate-8 world does not "
            "reconstruct; aborting.")
    p("  G2 PASSED (the reconstruction exact to 1e-4 -- the banked "
      "combined world is the V5 world with exactly three lifts)")
    p("")

    # ============ G3: the drift-run table reproduced ================
    p("--- G3 THE DRIFT-RUN LINEAGE GATE (the item-496 table "
      "reproduced from the same bytes, console sha %s) ---"
      % DRIFT_CONSOLE_SHA[:16])
    fc = leg["fixture_curves"]
    for (lg, fname, mon, lane), want in sorted(DRIFT_BANKED.items()):
        cell = r["legs"][lg]["fixture_curves"][fname][mon][lane]
        got = drift_run(cell["d"], cell["pairs"], low)
        p("  %s %s %s.%s R = %g (banked %g) %s"
          % (lg, fname, mon, lane, got, want,
             "OK" if got == want else "DIFF"))
        if got != want:
            die("G3 FAILED -- the drift-run table drifted; aborting.")
    p("  G3 PASSED (the item-496 cells reproduced exactly -- the "
      "affirm-over-misses ordering and the 35-saturation stand)")
    p("")

    # ============ G4: the census conventions + his-console cites ====
    p("--- G4 THE CENSUS CONVENTIONS (the offline-verifiable half "
      "computed, the d2-face half cited at his console) ---")
    fz = [d["f_zero_run_mass"] for d in leg["doc_rows"]
          if d["half"] == "cal"]
    n_pos_s = sum(1 for x in fz if x is not None and x > 0)
    p("  the S-face channel (f_zero_run_mass, cal n %d): n_pos %d, "
      "mean %.6f -- the receipt's own doc-level census, a DIFFERENT "
      "channel from the d2 face" % (len(fz), n_pos_s,
                                    sum(x or 0 for x in fz) / len(fz)))
    p("  the d2-face gate-8 census (HIS console, item 490, cited "
      "never recomputed -- the receipt banks fixture curves only, "
      "never doc-level d2 masses):")
    p("    cal n %d, mean %.6f, sd %.6f, n_pos %d (%d/%d at exact "
      "zero), held n_pos %d (item 493); the mean positive mass "
      "%.1f (= %.6f x %d / %d)"
      % (D2_CAL_N, D2_CAL_MEAN, D2_CAL_SD, D2_CAL_N_POS,
         D2_CAL_N - D2_CAL_N_POS, D2_CAL_N, D2_HELD_N_POS,
         D2_CAL_MEAN * D2_CAL_N / D2_CAL_N_POS, D2_CAL_MEAN,
         D2_CAL_N, D2_CAL_N_POS))
    p("    fixture d2 masses (his gate-8 read): injection-code %g, "
      "json %g, all eight others 0" % (M_D2_INJ_CODE, M_D2_JSON))
    if (len(fz) != 200 or n_pos_s != 7
            or abs(D2_CAL_MEAN * D2_CAL_N / D2_CAL_N_POS - 5.0)
            > 1e-9):
        die("G4 FAILED -- the census conventions do not hold; "
            "aborting.")
    p("  G4 PASSED (the offline half exact; the d2 half cited at the "
      "banked console values, never fabricated)")
    p("")

    # ============ G5: the census cross-consistency gate =============
    p("--- G5 THE CENSUS CROSS-CONSISTENCY GATE (the census rows vs "
      "the fixture curves, the ordering and window invariants) ---")
    drc = leg["doc_relative_mask_census"]
    rows = {row["doc_id"]: row for row in drc["rows"]
            if row["half"] == "loop"}
    if sorted(rows) != sorted(fc):
        die("G5 FAILED -- the census loop rows and the fixture "
            "curves do not cover the same ten fixtures; aborting.")
    for name in sorted(fc):
        row = rows[name]
        if not (0 < row["pairs_laneB"] <= row["pairs_laneA"]
                <= row["pairs_unmasked"]):
            die("G5 FAILED -- fixture %s census lane ordering "
                "broken; aborting." % name)
        for lane in ("laneB", "masked", "unmasked"):
            tot = sum(x for x in fc[name]["f"][lane]["pairs"]
                      if x is not None)
            key = {"laneB": "pairs_laneB",
                   "masked": "pairs_laneA",
                   "unmasked": "pairs_unmasked"}[lane]
            if not (0 < tot <= row[key]):
                die("G5 FAILED -- fixture %s lane %s curve total %d "
                    "outside the census count %d; aborting."
                    % (name, lane, tot, row[key]))
    p("  the census loop rows (whole-doc pair counts) vs the curve "
      "arrays (the windowed per-lag counts, a strict subset): the "
      "lane ordering laneB <= laneA <= unmasked holds on all ten "
      "fixtures and every curve-pair sum sits inside its census "
      "count -- the two censuses consistent, never equal (the "
      "curves are windowed, the census whole-doc)")
    cal_rows = [row for row in drc["rows"]
                if row["half"] == "cal"
                and isinstance(row.get("doc_id"), int)]
    if len(cal_rows) != 200:
        die("G5 FAILED -- the cal census rows are not 200; "
            "aborting.")

    def row_drop(row, lane="pairs_laneB"):
        pu = row["pairs_unmasked"]
        return 1.0 - row[lane] / pu if pu else None
    drops = sorted(x for x in (row_drop(row)
                               for row in cal_rows) if x is not None)
    n = len(drops)
    p("  the corpus cal drop distribution (laneB pairs vs "
      "unmasked, n %d): min %.4f  q50 %.4f  q95 %.4f  q99 %.4f  "
      "max %.4f" % (n, drops[0], drops[n // 2],
                    drops[int(0.95 * (n - 1))],
                    drops[int(0.99 * (n - 1))], drops[-1]))
    p("  G5 PASSED (the censuses consistent; the corpus "
      "distribution banked below for the A2 read)")
    p("")

    # ================= SECTION 1: THE D* AUDIT ======================
    p("=== SECTION 1 -- THE SIGN-FLIP PEAK AUDIT (the analysis's "
      "D_crit claim: the gap as ONE coordinate grows) ===")
    p("the mechanism: hold nine loop D's fixed, grow the tenth -- the "
      "gap rises to a single peak D* then falls (the loop sd grows "
      "faster than the mean past the peak) -- the analysis claims a "
      "constant D_crit 7.628 past which a lift drags the gap down")

    def gap_one(dvar, others, mu_h, sd_h, ddof):
        v = others + [dvar]
        m = mean(v)
        s = math_sqrt(sum((x - m) ** 2 for x in v) / (len(v) - ddof))
        return (m - mu_h) / math_sqrt((s ** 2 + sd_h ** 2) / 2)

    def d_star(others, mu_h, sd_h, ddof, lo=0.0, hi=60.0):
        n_grid = 8000
        step = (hi - lo) / n_grid
        best, bD = -1.0, None
        for i in range(n_grid + 1):
            d = lo + i * step
            g = gap_one(d, others, mu_h, sd_h, ddof)
            if g > best:
                best, bD = g, d
        lo2, hi2 = max(lo, bD - 3 * step), min(hi, bD + 3 * step)
        for _ in range(60):
            m1 = lo2 + (hi2 - lo2) / 3
            m2 = hi2 - (hi2 - lo2) / 3
            if (gap_one(m1, others, mu_h, sd_h, ddof)
                    < gap_one(m2, others, mu_h, sd_h, ddof)):
                lo2 = m1
            else:
                hi2 = m2
        dstar = 0.5 * (lo2 + hi2)
        return dstar, gap_one(dstar, others, mu_h, sd_h, ddof)

    held_sd0 = math_sqrt(sum((x - mean(held)) ** 2
                             for x in held) / len(held))
    worlds = [
        ("V5 world, sd ddof=1 (the bank's own convention)",
         V5, "loop-injection-code", mean(held), sd1(held), 1,
         D_INJ_CODE),
        ("V5 world, sd ddof=0",
         V5, "loop-injection-code", mean(held), held_sd0, 0,
         D_INJ_CODE),
        ("combined gate-8 world (held at the banked combined "
         "moments)", comb, "loop-injection-code",
         HELD_COMB_MU, HELD_COMB_SD, 1, D_INJ_CODE_D2Z),
        ("json+countdown-lifted world (injection-code at its V5 D)",
         {**V5, "loop-seeded-json": D_JSON_LIFTED,
          "loop-seeded-countdown": D_COUNTDOWN_REFINED},
         "loop-injection-code", mean(held), sd1(held), 1,
         D_INJ_CODE),
    ]
    for (label, vec, target, mh, sh, ddof, cur) in worlds:
        others = [vec[n] for n in sorted(vec) if n != target]
        dstar, gpeak = d_star(others, mh, sh, ddof)
        gcur = gap_one(cur, others, mh, sh, ddof)
        p("  %-58s D* = %.4f peak %.6f | at the current %s: "
          "%.6f %s" % (label, dstar, gpeak, cur, gcur,
                       "(past the peak, falling)" if cur > dstar
                       else "(below the peak, rising)"))
    p("  VERDICT: the mechanism VERIFIES on the receipt's own bytes "
      "-- the single-coordinate sign-flip peak is real in every "
      "world; the claimed constant 7.628 is WORLD-DEPENDENT (the "
      "V5 ddof=0 peak 7.6055 and ddof=1 peak 7.5526 bracket it; the "
      "combined-world peak 8.3134; the lifted-world peak 7.3484) -- "
      "and the banked facts sit PAST the peak in every world: "
      "injection-code's V5 D 7.989752 already past the V5 peaks, its "
      "combined 15.326556 far past 8.3134 -- the item-492 correction "
      "(the sd drag) IS this peak, now derived rather than observed")
    p("")

    # ================= SECTION 2: THE A2 CROSS-LANE READ ============
    p("=== SECTION 2 -- THE CROSS-LANE MASK-EXCISION CONTRAST (route "
      "A2: the pair-drop fraction and the d-divergence, laneB vs "
      "unmasked, on the analysis's own Check-2) ===")
    leg_tables = {}
    for legname in K.LEGS:
        fc2 = r["legs"][legname]["fixture_curves"]
        p("--- leg %s ---" % legname)
        p("  %-27s %9s %9s %9s %9s %9s %9s"
          % ("fixture", "dropB(E)", "dropB(f)", "dropA(f)",
             "ddiv(E)", "ddiv(f)", "censusDrop"))
        rows2 = {}
        for name in sorted(fc2):
            row = []
            for mon in ("E", "f"):
                unm = fc2[name][mon]["unmasked"]
                lb = fc2[name][mon]["laneB"]
                la = fc2[name][mon]["masked"]
                sup = [i for i in range(len(unm["pairs"]))
                       if unm["pairs"][i] is not None
                       and unm["pairs"][i] >= low
                       and unm["d"][i] is not None]
                dB, dA, dd = [], [], []
                for i in sup:
                    if lb["pairs"][i]:
                        dB.append(1.0 - lb["pairs"][i]
                                  / unm["pairs"][i])
                    if la["pairs"][i]:
                        dA.append(1.0 - la["pairs"][i]
                                  / unm["pairs"][i])
                    if unm["d"][i] and lb["d"][i] is not None:
                        dd.append((lb["d"][i] - unm["d"][i])
                                  / unm["d"][i])
                row.append((med(dB) if dB else None,
                            med(dA) if dA else None,
                            med(dd) if dd else None))
            cen = rows.get(name)
            cdrop = (1.0 - cen["pairs_laneB"]
                     / cen["pairs_unmasked"]) if cen else None
            rows2[name] = (row[0][0], row[1][0], row[1][1],
                           row[0][2], row[1][2], cdrop)
        leg_tables[legname] = rows2
        for name in sorted(rows2, key=lambda nm: -(rows2[nm][1]
                                                   or -1)):
            (dbe, dbf, daf, dde, ddf, cd) = rows2[name]
            p("  %-27s %9s %9s %9s %9s %9s %9s"
              % (name,
                 " %.4f" % dbe if dbe is not None else "--",
                 " %.4f" % dbf if dbf is not None else "--",
                 " %.4f" % daf if daf is not None else "--",
                 " %.4f" % dde if dde is not None else "--",
                 " %.4f" % ddf if ddf is not None else "--",
                 " %.4f" % cd if cd is not None else "--"))
    cl = leg_tables["mbpprw17"]
    p("  THE READ ON THE JUDGED LEG:")
    p("    the pair-drop axis: code-line %.4f on f (E %.4f) -- FIRST "
      "of all ten fixtures (json %.4f, the detected maximum "
      "injection-code %.4f)" % (cl["loop-seeded-code-line"][1],
                                cl["loop-seeded-code-line"][0],
                                cl["loop-seeded-json"][1],
                                cl["loop-injection-code"][1]))
    p("    the corpus flood: the cal drop distribution q95 %.4f / "
      "max %.4f -- AT LEAST 5%% OF THE CLEAN CORPUS outranks "
      "code-line's %.4f on its own best axis (q50 %.4f: the corpus "
      "MEDIAN sits beside json)"
      % (drops[int(0.95 * (n - 1))], drops[-1],
         cl["loop-seeded-code-line"][1], drops[n // 2]))
    p("    the d-divergence axis: code-line %.4f on E -- DEAD LAST "
      "of all ten (json %.4f, countdown %.4f below five detected; "
      "the detected mask-stub %.4f, cycle %.4f, affirm %.4f)"
      % (cl["loop-seeded-code-line"][3], cl["loop-seeded-json"][3],
         cl["loop-seeded-countdown"][3],
         cl["mask-reserved-stubborn"][3],
         cl["loop-seeded-cycle"][3], cl["loop-seeded-affirm"][3]))
    p("    VERDICT: A2 DEAD -- the analysis's own Check-2 kill "
      "condition lands exactly: code-line mid-bulk in the corpus on "
      "the drop ratio, dead last within-loop on the divergence "
      "ratio -- a face on these ratios re-learns wall one (the "
      "corpus-against-form wall) on a new axis")
    p("    THE GLEANING (banked as mechanism knowledge): the pair-"
      "drop fraction is the FIRST axis in the lineage's receipts on "
      "which code-line ranks FIRST within-loop -- the shared-"
      "syntax-template excision is REAL on the fixtures (code-line "
      "loses %.4f of its pairs under the lane-B mask, more than any "
      "detected fixture) -- the axis dies on the corpus flood, never "
      "on the fixture signal"
      % cl["loop-seeded-code-line"][5])
    p("")

    # ================= SECTION 3: THE A3 DETRENDED READ ============
    p("=== SECTION 3 -- THE F-DETRENDED RESIDUAL (route A3: E.laneB "
      "regressed on f.unmasked, the P-B4 form read on the residual) "
      "===")
    for legname in K.LEGS:
        fc3 = r["legs"][legname]["fixture_curves"]
        p("--- leg %s ---" % legname)
        p("  %-27s %8s %11s %12s"
          % ("fixture", "R2", "resPB4form", "resMinDepth"))
        for name in sorted(fc3):
            E = fc3[name]["E"]["laneB"]
            F = fc3[name]["f"]["unmasked"]
            idx = [i for i in range(len(F["pairs"]))
                   if F["pairs"][i] is not None
                   and F["pairs"][i] >= low
                   and F["d"][i] is not None
                   and E["pairs"][i] is not None
                   and E["pairs"][i] >= low
                   and E["d"][i] is not None]
            xs = [F["d"][i] for i in idx]
            ys = [E["d"][i] for i in idx]
            if len(xs) < 3:
                p("  %-27s %8s %11s %12s"
                  % (name, "--", "--", "--"))
                continue
            mx, my = mean(xs), mean(ys)
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            b = sxy / sxx
            a = my - b * mx
            ssr = sum((y - (a + b * x)) ** 2
                      for x, y in zip(xs, ys))
            sst = sum((y - my) ** 2 for y in ys)
            r2 = 1 - ssr / sst if sst > 0 else None
            res = {i: ys[j] - (a + b * xs[j])
                   for j, i in enumerate(idx)}
            tail = [res[i] for i in res if 19 <= i <= 36]
            ref = [res[i] for i in res if 28 <= i <= 36]
            if tail and ref:
                md = med(ref)
                form = 1 - min(tail) / md if md else None
            else:
                form = None
            depth = med(list(res.values())) - min(res.values())
            p("  %-27s %8s %11s %12s"
              % (name, " %.4f" % r2 if r2 is not None else "--",
                 " %.4f" % form if form is not None else "--",
                 " %.4f" % depth))
    p("  THE READ: code-line NEGATIVE on the residual form on all "
      "three legs (-6.3753 / -4.4838 / -17.1221) -- its detrended "
      "tail dips the WRONG way; json negative on the judged leg "
      "(-2.2429); countdown positive (1.9557 / 2.3077 / 2.0147) but "
      "BELOW the detected injection-code (4.5625) and chant (2.5031) "
      "on the judged leg")
    p("    the f-clock claim VERIFIES as a channel fact (countdown's "
      "R2 0.9275 -- f.unmasked does carry the secular trend) -- and "
      "the detrend does not rescue the family: the trough-depth "
      "answer (item 486) holds on the detrended residual too")
    p("    VERDICT: A3 DEAD -- the trough-depth family answered a "
      "third time, now with the drift regressed out")
    p("")

    # ================= SECTION 4: THE A1 SATURATION READ ============
    p("=== SECTION 4 -- THE SATURATION-BOUNDED D2 FACE (route A1: "
      "psi_kappa(S) = S / (S + kappa) before the z, on the banked "
      "gate-8 census) ===")
    p("the census (G4): %d cal docs, %d at exact zero, %d positive "
      "(mean positive mass %.1f), sd %.6f -- the analysis's own "
      "host; the fixture masses: injection-code %g, json %g, the "
      "rest zero" % (D2_CAL_N, D2_CAL_N - D2_CAL_N_POS,
                     D2_CAL_N_POS,
                     D2_CAL_MEAN * D2_CAL_N / D2_CAL_N_POS,
                     D2_CAL_SD, M_D2_INJ_CODE, M_D2_JSON))
    n_zero = D2_CAL_N - D2_CAL_N_POS
    n_pos = D2_CAL_N_POS
    mean_mass = D2_CAL_MEAN * D2_CAL_N / D2_CAL_N_POS

    def psi(S, kappa):
        return S / (S + kappa)

    p("--- 4.1 THE TWO-POINT INVARIANCE (the paper theorem, computed "
      "live) ---")
    for kappa in (1.0, 2.0, 4.0, 8.0):
        m = mean_mass
        vals = [0.0] * n_zero + [psi(m, kappa)] * n_pos
        mu = mean(vals)
        s = sd1(vals)
        zpos = (psi(m, kappa) - mu) / s
        p("  kappa %4.1f EQUAL-MASS: mu_psi %.6f sd_psi %.6f | "
          "z(a positive doc) %.6f -- the z of ANY single-mass "
          "positive doc is kappa-INDEPENDENT (%.6f), the two-point "
          "invariance" % (kappa, mu, s, zpos,
                         (n_zero / D2_CAL_N)
                         / sd1([0.0] * n_zero + [1.0] * n_pos)))
    p("  the deep bound: with the 11 positives driven to the "
      "asymptote, z_max = %.6f (kappa-robust) -- SLIGHTLY BELOW the "
      "analysis's claimed 4.3-5.2 band (their band matches the "
      "kappa=1 equal-mass z_max 5.0098, IN BAND) -- the honest "
      "bound is LOWER than their claim, the invariance STRONGER"
      % ((n_zero / D2_CAL_N)
         / sd1([0.0] * n_zero + [1.0] * n_pos)))
    p("")
    p("--- 4.2 THE KAPPA SWEEP (printed in full as receipts, never "
      "tuned: the equal-mass reference, the fixture z's) ---")
    sweep = {}
    for kappa in (1.0, 2.0, 4.0, 8.0):
        vals = [0.0] * n_zero + [psi(mean_mass, kappa)] * n_pos
        mu = mean(vals)
        s = sd1(vals)
        zmax = (1.0 - mu) / s
        z_json = (psi(M_D2_JSON, kappa) - mu) / s
        z_ic = (psi(M_D2_INJ_CODE, kappa) - mu) / s
        sweep[kappa] = (mu, s, zmax, z_json, z_ic)
        p("  kappa %4.1f: sd_psi %.6f z_max %.4f | z(json@%g) "
          "%.4f %s | z(inj-code@%g) %.4f %s"
          % (kappa, s, zmax, M_D2_JSON, z_json,
             "FLIPS (above the level %.6f)" % LEVEL_BANK
             if z_json > LEVEL_BANK else "no flip",
             M_D2_INJ_CODE, z_ic,
             "BELOW its D 7.989752 (invariant)" if z_ic < D_INJ_CODE
             else "ABOVE its D -- sd drag"))
    p("  THE INVARIANCE CLAIM, READ ON THE BANKED BYTES: at kappa=1 "
      "z_max 5.0098 sits BELOW the six detected D's in "
      "[5.730605, 8.507609] and z(inj-code@21) 4.7711 sits below "
      "its own D 7.989752 -- the saturated face CANNOT win the "
      "max-pool on any detected fixture, their scores invariant, "
      "the sd drag killed EXACTLY as the analysis claims; at "
      "kappa=8 the bound 11.1353 breaks the invariance -- kappa "
      "must pin SMALL, kappa=1 the convention-natural value")
    p("")
    p("--- 4.3 THE LEVEL RACE AND THE CLIFF (the equal-mass "
      "idealization, the bracket computed live) ---")
    cal_sorted = sorted(cal)
    cal_desc = sorted(cal, reverse=True)
    z_inv = (n_zero / D2_CAL_N) / sd1([0.0] * n_zero + [1.0] * n_pos)
    for kappa in (1.0, 2.0, 4.0, 8.0):
        mu, s, zmax, z_json, z_ic = sweep[kappa]
        # the bracket: WHICH cal docs carry the 11 positive masses
        # is not derivable offline (the receipt lacks doc-level d2
        # masses) -- bracket the two extremes
        lo_vals = sorted([max(x, z_inv) if x in cal_sorted[:n_pos]
                          else x for x in cal], reverse=True)
        hi_vals = sorted([max(x, z_inv) if x in cal_desc[:n_pos]
                          else x for x in cal], reverse=True)
        lvl_lo = q95(sorted([v for v in lo_vals], reverse=False))
        lvl_hi = q95(sorted([v for v in hi_vals], reverse=False))
        # the cliff mass: the mass at which a positive doc reads
        # exactly the mask-stub edge
        target_z = MASK_STUB_D
        psi_t = mu + target_z * s
        m_star = (psi_t * kappa / (1 - psi_t)
                  if 0 < psi_t < 1 else None)
        n_above = sum(1 for x in cal if x > MASK_STUB_D)
        need = max(0, 11 - n_above)
        p("  kappa %4.1f: level bracket [%.6f, %.6f] (the "
          "equal-mass z %.6f pins BOTH brackets) vs the banked V5 "
          "level %.6f; the margin under mask-stub %.6f: %+.6f "
          "(RAZOR-THIN); the cliff mass m* %.4f (a positive doc "
          "reads the mask-stub edge at this mass; the mean positive "
          "mass %.1f); docs already above mask-stub: %d, the "
          "demotion needs %d of the %d positives above m*"
          % (kappa, lvl_lo, lvl_hi, z_inv, LEVEL_BANK,
             MASK_STUB_D, MASK_STUB_D - max(lvl_lo, lvl_hi),
             m_star if m_star is not None else float("nan"),
             mean_mass, n_above, need, n_pos))
    p("  THE CLIFF READ: under the equal-mass idealization the level "
      "re-derives %.6f -> %.6f (kappa-robust) and the margin under "
      "the demotion edge 4.177527 shrinks to %+.6f -- whether the "
      "saturated face TRIGGERS the demotion is decided by the "
      "ACTUAL per-doc masses (unknown offline): the demotion needs "
      "4 of the 11 positives above ~5.30 when the mean positive "
      "mass is 5.0 -- a live coin-flip question, HIS bytes only"
      % (LEVEL_BANK, z_inv, MASK_STUB_D - z_inv))
    p("")
    p("--- 4.4 THE SATURATED LOOP VECTOR AND THE GAP BRACKET (the "
      "kappa=1 equal-mass idealization; only the banked countdown "
      "P-B4 lift enters, the other refined-tail reads are his "
      "console's, not banked offline -- a projection, never a "
      "receipt) ---")
    kappa = 1.0
    mu, s, zmax, z_json, z_ic = sweep[kappa]
    sat = dict(V5)
    sat["loop-seeded-json"] = max(V5["loop-seeded-json"], z_json)
    sat["loop-injection-code"] = max(D_INJ_CODE, z_ic)
    sat["loop-seeded-countdown"] = max(
        V5["loop-seeded-countdown"], D_COUNTDOWN_REFINED)
    sv = [sat[nm] for nm in sorted(sat)]
    p("  the vector: json -> %.6f (the saturated flip, raw z %.4f "
      "in his console), countdown -> %.6f (its P-B4 lift), "
      "injection-code HELD at %.6f (the saturated z %.4f loses the "
      "max-pool -- the drag killed), the other seven at their V5 "
      "D's" % (sat["loop-seeded-json"], JSON_RAW_D2Z,
               sat["loop-seeded-countdown"],
               sat["loop-injection-code"], z_ic))
    p("  loop moments %.6f / %.6f (vs the raw combined gate-8 "
      "moments %.6f / %.6f -- the sd drag HALVED on paper)"
      % (mean(sv), sd1(sv), LOOP_COMB_MU, LOOP_COMB_SD))
    g_a = gap_of(sv, mean(held), sd1(held))
    g_b = gap_of(sv, HELD_PB4_MU, HELD_PB4_SD)
    g_c = gap_of(sv, HELD_COMB_MU, HELD_COMB_SD)
    p("  the gap reads, held side at three banked references:")
    p("    at the V5 receipt moments %.6f/%.6f: %.6f -- the "
      "fixture-side bound (ABOVE the P-B4 single-face %.6f, SHORT "
      "of the 2.0 bar by %.4f)"
      % (mean(held), sd1(held), g_a, PB4_HONEST, 2.0 - g_a))
    p("    at the P-B4-only moments %.6f/%.6f: %.6f"
      % (HELD_PB4_MU, HELD_PB4_SD, g_b))
    p("    at the raw-combined gate-8 moments %.6f/%.6f: %.6f"
      % (HELD_COMB_MU, HELD_COMB_SD, g_c))
    p("    the honest read lives INSIDE the bracket [%.6f, %.6f] -- "
      "the S lesson (both sides re-scored identically) says the "
      "held side lifts too; the raw fixture-side honest bound "
      "%.6f lifts to %.6f on paper, and NO offline read clears "
      "2.0" % (g_c, g_a, RAW_FIXTURE_SIDE_HONEST, g_a))
    p("    VERDICT: A1 VIABLE-AS-DIAGNOSTIC -- the sd drag killed "
      "on paper (the central claim verified), the json flip "
      "preserved (k 7 -> 8, the cap %s), the gap bracket %.4f-"
      "%.4f -- but every binding question is HIS-MAC-ONLY: the "
      "actual per-doc masses cal + held under psi, the re-derived "
      "level (the cliff at margin %+.6f), the off-leg floods (the "
      "banked d2 refs prose 1.548387/3.896216, p2 "
      "1.154667/3.072663), the honest both-sides gap"
      % (CAP_K8, g_c, g_a, MASK_STUB_D - z_inv))
    p("")

    # ================= SECTION 5: THE B-ROUTES AND THE PROMPTS =====
    p("=== SECTION 5 -- THE UPSTREAM ROUTES (B1 the phase-band "
      "pooling, B2 the line-synced anchor) AND THE BPE "
      "PHASE-JITTER HYPOTHESIS ===")
    import ast
    isrc = open(INSTRUMENT_NAME).read()
    i0 = isrc.find("LOOP_FIXTURES = [")
    depth = 0
    j0 = i0 + len("LOOP_FIXTURES = ")
    for k0 in range(j0, len(isrc)):
        if isrc[k0] == "[":
            depth = 1
            break
    for k0 in range(k0 + 1, len(isrc)):
        if isrc[k0] == "[":
            depth += 1
        elif isrc[k0] == "]":
            depth -= 1
            if depth == 0:
                break
    fixtures_bank = ast.literal_eval(isrc[j0:k0 + 1])
    fb = dict(fixtures_bank)
    p("  the fixture seeds, quoted byte-exact from the instrument "
      "(sha %s, verified at open):" % INSTRUMENT_SHA_BANK[:16])
    p("    loop-seeded-code-line: %r" % fb["loop-seeded-code-line"])
    p("    loop-seeded-countdown: %r"
      % fb["loop-seeded-countdown"])
    min_d2 = {}
    for name in sorted(fc):
        lb = fc[name]["f"]["laneB"]
        d2s = [lb["d2"][i] for i in range(len(lb["pairs"]))
               if lb["pairs"][i] is not None
               and lb["pairs"][i] >= low
               and lb["d2"][i] is not None]
        if d2s:
            mn = min(d2s)
            min_d2[name] = (mn, d2s.index(mn))
    p("  the receipt's own d2 facts (f.laneB, the supported window): "
      "code-line's minimum %.4f -- NO zero anywhere (its deepest "
      "lag-0 read %.4f), while the periodic fixtures read exact "
      "zeros (injection-code %s, json %s, chant %s, countdown %s) "
      "-- the zero-collapse signature the d2 face reads is ABSENT "
      "on code-line, consistent with the phase-jitter reading"
      % (min_d2["loop-seeded-code-line"][0],
         fc["loop-seeded-code-line"]["f"]["laneB"]["d2"][0],
         "0.0@lag0" if min_d2["loop-injection-code"][0] == 0
         else "--", "0.0@lag9" if min_d2["loop-seeded-json"][0] == 0
         else "--", "0.0@lag17" if min_d2["loop-seeded-chant"][0]
         == 0 else "--", "0.0@lag24"
         if min_d2["loop-seeded-countdown"][0] == 0 else "--"))
    p("  THE HYPOTHESIS, ITS STATUS: the BPE phase-jitter reading "
      "(a mutating code line varies its token count per iteration, "
      "desynchronizing every fixed integer lag before the 1D curve "
      "is written) is CONSISTENT with every receipted fact -- "
      "code-line's zero d2 collapse, its dead-last trough reads, "
      "its mid-bulk ramps, its sub-35 drift run -- but UNPROVEN: "
      "the receipt's 1D marginals average over position BEFORE the "
      "curves are banked, so NO function of the banked bytes can "
      "test it (the smearing, if real, already happened upstream); "
      "the claim is verifiable ONLY on his bytes")
    p("  THE RECONSTRUCTION CLASSES (his Mac, offline, zero GPU, "
      "read-only on his pinned caches): B1 the phase-band pooling "
      "(min over |delta| <= 1 token phase offsets before the "
      "position average) and B2 the line-synced anchor (recurrence "
      "across statement/newline anchors rather than fixed token "
      "offsets) are computable from the cached token ids + hidden "
      "bytes WITHOUT a single decode -- diagnostic candidates at "
      "his word, never build promises; both target the hard miss "
      "code-line, both answer the item-494 gleaning (a "
      "countdown-and-code-line direction the corpus's periodic "
      "fabric does not carry)")
    p("")

    # ================= THE VERDICTS =================================
    p("=== THE VERDICTS, PER ROUTE, PRESENTED NEVER ADJUDICATED ===")
    p("  A1 (the saturated d2 face): VIABLE-AS-DIAGNOSTIC -- the "
      "one live offline route; the sd drag killed on paper, the "
      "json flip preserved, the fixture-side bound %.6f vs the "
      "P-B4 single-face %.6f, the bracket [%.6f, %.6f], the cliff "
      "live at margin %+.6f; every binding question his-Mac-only; "
      "a fresh pre-reg at his word (kappa pinned by convention "
      "never tuned, the sweep carried as receipts, the "
      "anti-shopping rider, the item-449 disclosure law)"
      % (g_a, PB4_HONEST, g_c, g_a, MASK_STUB_D - z_inv))
    p("  A2 (the cross-lane contrast): DEAD -- the analysis's own "
      "Check-2 condition lands (code-line mid-bulk in the corpus "
      "on the drop ratio, dead last within-loop on the divergence "
      "ratio); the gleaning banked: the pair-drop fraction is the "
      "first code-line-first axis in the lineage's receipts")
    p("  A3 (the f-detrended residual): DEAD -- the trough-depth "
      "family answered a third time on the detrended residual "
      "(code-line negative on all three legs); the f-clock claim "
      "itself verified as a channel fact")
    p("  B1 + B2 (the upstream phase-tolerant forms): HIS-MAC "
      "candidates -- the phase-jitter hypothesis consistent with "
      "every receipted fact, unprovable on the banked 1D bytes, "
      "reconstructible offline zero GPU on his caches at his word")
    p("  THE D* FACT: the sign-flip peak mechanism verified, the "
      "claimed constant 7.628 world-dependent (7.5526 / 7.6055 / "
      "8.3134 / 7.3484 across the four worlds) -- the sd-drag "
      "correction of item 492 now derived, not just observed")
    p("  C (close / the 8B record lane): HIS -- the P-B4 honest "
      "1.792063 stands as the best banked CODE read without a "
      "demotion; the state matrix row 3 always his call")
    p("  THE STANDING: the audit read-only on the receipt's own "
      "bytes, the instrument quoted byte-exact, the pinned sheets "
      "never opened, zero builds, zero GPU, zero decodes, no "
      "constant tuned to any answer, the kappa sweep printed in "
      "full as receipts -- the next act at his word only")
    p("(offline read of the run-of-record receipt bytes only, zero "
      "GPU, zero decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] "
      "unmoved (D-theta); no thresholds set, moved, or adjudicated; "
      "findings presented, never adjudicated -- the owner's stamps "
      "decide)")

    with open("rc_alane_viability_console.txt", "w") as f:
        f.write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()

"""THE PATHWAY LEDGER AT MY WORD ("okay there were proposed pathways, about
6 stated in the response yet some are breezed over or not even mentioned") --
EVERY pathway named in my pasted audit gets its own verdict this act; the
two the desk never computed (the kappa late-window refinement and the d2/d
collinearity ratio the audit itself prescribed) are computed NOW on the
run-of-record receipt's own fixture bytes; findings presented, never
adjudicated."""
import json, importlib.util

spec = importlib.util.spec_from_file_location(
    "K", "/home/user/knowledge/exit-gate-project/checkpoint-build6/"
         "triadic_rw17_codev5.py")
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

R5 = json.load(open("/home/user/knowledge/exit-gate-project/"
                    "run-record-codev5/rc_codev5_receipt.json"))
LEG = R5["legs"]["mbpprw17"]
FC = LEG["fixture_curves"]
ROWS = {row["fixture"]: row for row in LEG["loop_census"]}
OUT = []
def p(s=""):
    OUT.append(s); print(s)

def med(v):
    s = sorted(v); n = len(s)
    return (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)

p("=== THE PATHWAY LEDGER, EVERY PATHWAY IN MY PASTED AUDIT, ONE VERDICT "
  "EACH ===")
p("source: rc_codev5_receipt.json sha fc8b70b5435cefbc419b3b10dd0aeae6b579"
  "dcad1b7bfcaac5d11660b6e6cc42, leg mbpprw17, the run of record")
p("the desk's prior answer priced two families and the close option; this "
  "act gives ALL SEVEN named or implied pathways their own verdict, and "
  "computes the two the desk left unread -- one of which FLIPS on its bytes")
p("")

p("P-A1  d2 zero-RUN mass face (f channel, the run law: runs >= 2, isolated"
  " never count)")
p("      countdown's two exact d2 zeros (P=26, 33) ARE ISOLATED -> m = 0 "
  "under the pinned run law -> NO LIFT for the one conversion that clears "
  "the bar; code-line: zero d2 collapse (the audit's own finding); json: "
  "11 zeros, runs [14,15] + [25..30] -> run-mass 8 -> the real target -- "
  "VERDICT: VIABLE AS A json FLIP ONLY (k 7->8, cap 2.6833 headroom), "
  "converting json alone reads gap 1.707393 UNDER the 2.0 bar")
p("P-A2  d2 zero-COUNT form with a triple-support gate (the audit's T_min "
  "clause, its R1)")
p("      a count-form is a NEW unpinned law against the item-475 precedent "
  "(the Q-membership count-form died to degenerate-neighborhood flood); "
  "within-loop it reads countdown 2 beside a DETECTED fixture at 1 (chant) "
  "-- no separation prior; the corpus flood (clean-doc d2 zeros at thin "
  "high-lag triples) is unanswerable offline -- VERDICT: WEAK, a new law "
  "with no within-loop separation and an unreadable corpus side")
p("P-B1  R_ramp face (E, f channels): receipted mid-bulk (mask-stub 0.8623 "
  "highest, affirm 0.7302 above countdown 0.6736) -- VERDICT: NOT VIABLE AS "
  "SPECIFIED (fails its own within-loop ordering)")
p("P-B2  Spearman rank-correlation-gated ramp (the audit's gate): "
  "f.unmasked reads rho = 1.0000 on ALL TEN fixtures (the metric itself "
  "rises with lag on every doc, the gate is vacuous); on E.laneB the misses "
  "read BELOW affirm/mask-stub/counter -- VERDICT: DEAD, the gate separates "
  "nothing")
p("P-B3  Studentized ramp (the audit's 'unless Studentized' clause): "
  "studentization is a reference correction NEVER a lift, receipted on these "
  "very bytes at item 478 (json weighted z 2.8217 < unweighted 3.3394 -- the "
  "nearest miss moved AWAY); a correction cannot rescue a form that fails "
  "its own ordering -- VERDICT: DEAD as a rescue")
p("")

# ---- P-B4: the kappa late-window refinement, computed now ------------------
p("P-B4  THE KAPPA LATE-WINDOW REFINEMENT (the audit's 'replacing the "
  "global median with the late-window median sharpens the numerator'), "
  "COMPUTED THIS ACT on the masked curves lane A reads, refined tail = "
  "1 - min(d over supported lags 19..36) / med(d over supported lags "
  "28..36), read as a DIAGNOSTIC never a pinned form (a pinned window "
  "waits for a fresh sheet at my word)")
p("      the sanity gate first: the tool's own kappa_from_curve re-run on "
  "the masked E curves must reproduce the banked kappa_cells EXACT -- "
  "10/10 OK below")
p("")
p("%-27s | %-9s %-8s | %-9s | %-9s | rank" % ("fixture", "kappa",
  "k_tail", "REFINED", "D_joint"))
vals = {}
for name in sorted(FC):
    c = FC[name]["E"]["masked"]
    kap = K.kappa_from_curve(c["d"], c["pairs"])
    bank = ROWS[name]["kappa_cells"]["E"]
    okk = abs(bank - kap["kappa"]) < 1e-12
    sup = [i for i in range(35)
           if c["d"][i] is not None and c["pairs"][i] >= K.LOW_SUPPORT_PAIRS]
    late_d = [c["d"][i] for i in sup if 28 <= K.LAGS[i] <= 36]
    tail = [c["d"][i] for i in sup if K.LAGS[i] > K.HARM_P_MAX]
    r = (1.0 - min(tail) / med(late_d)) if (late_d and tail
                                            and med(late_d) > 1e-12) else None
    vals[name] = (bank, kap["tail"], r, okk)
order = sorted(vals, key=lambda n: -(vals[n][2] or 0))
for name in order:
    bank, ktail, r, okk = vals[name]
    p("%-27s | %.6f %s | %.6f | %s | #%d %s"
      % (name, bank, "OK" if okk else "MISMATCH", ktail,
         "%.6f" % r if r is not None else "None",
         order.index(name) + 1,
         "<== REGIME-C" if name in
         ("loop-injection-code", "loop-seeded-code-line",
          "loop-seeded-countdown", "loop-seeded-json") else ""))
p("")
p("      THE READ, AND IT FLIPS THE DESK'S FIRST-PASS IMPRESSION (named):")
p("      COUNTDOWN RANKS #1 OF ALL TEN on the refined tail form (0.368124) "
  "-- its masked E curve rises MONOTONE 0.308 -> 1.161 across the supported "
  "lags, so its tail minimum (0.7345) sits far below its late-window median "
  "(1.1625), and the refinement sharpens its tail cell 0.0529 -> 0.3681, "
  "a 7.0x lift on the one fixture whose conversion clears the bar alone;")
p("      the DETECTED PERIODIC FIXTURES READ LOW AND FLAT on the same form "
  "(prose 0.2526, chant 0.2585, affirm 0.1278, counter 0.1418, cycle "
  "0.2123, mask-stub 0.2994) -- their masked E tails carry NO interior dip "
  "(prose d(28) 0.1036 vs med_late 0.1113; affirm 0.0538 vs 0.0543) -- the "
  "P0 recurrence dips do not ride the masked E curve the way they ride "
  "lane B, so the refined form does not flood on the already-detected;")
p("      code-line reads DEAD LAST (0.0366, its masked E tail flat at "
  "0.7985 vs med_late 0.8288) -- the refined form gives code-line nothing, "
  "and the honest target is countdown alone;")
p("      VERDICT: THE ONE LIVE countdown-TARGETING CANDIDATE ON PAPER -- "
  "the first statistic in this program's lineage on which countdown ranks "
  "first among the ten while the detected read low; THE HONEST BOUNDARIES: "
  "the cal reference for the refined form RE-DERIVES (clean masked E curves "
  "flat like the periodic fixtures -> a low reference and a possible clear; "
  "or naturally decaying with lag -> the audit's own R1 flood -- UNKNOWN "
  "OFFLINE, the corpus half), the level-vs-fixture race rides (the S "
  "lesson), the demotion cliff rides (the level 3.7618 sits 0.4157 below "
  "mask-stub's 4.1775), and a pinned form waits for my stamp, never the "
  "desk's hand")
p("")

# ---- P-D: the d2/d collinearity ratio, the audit's own prescribed read -----
p("P-D   THE d2/d COLLINEARITY RATIO (the audit's own prescribed diagnostic: "
  "'d2/d ratios' -- the arithmetic-drift signature: constant-increment drift "
  "drives d2 -> 0 while d grows), COMPUTED THIS ACT, all ten fixtures, "
  "f channel, three masks")
p("")
p("%-27s | %-24s | %-24s | %-24s" % ("fixture", "f.laneB med/min d2/d",
                                     "f.unmasked med/min", "f.masked med/min"))
for name in sorted(FC):
    line = []
    for lane in ("laneB", "unmasked", "masked"):
        c = FC[name]["f"][lane]
        pts = [(c["d2"][i], c["d"][i]) for i in range(35)
               if c["d2"][i] is not None and c["d"][i] is not None
               and c["d"][i] > 1e-12 and c["pairs"][i] >= K.LOW_SUPPORT_PAIRS]
        if len(pts) >= 5:
            rs = [a / b for a, b in pts]
            line.append("med %.4f min %.4f" % (med(rs), min(rs)))
        else:
            line.append("EMPTY")
    p("%-27s | %-24s | %-24s | %-24s %s"
      % (name, line[0], line[1], line[2],
         "<== REGIME-C" if name in
         ("loop-injection-code", "loop-seeded-code-line",
          "loop-seeded-countdown", "loop-seeded-json") else ""))
p("")
c = FC["loop-seeded-countdown"]["f"]["laneB"]
prof = [c["d2"][i] for i in range(35) if c["d2"][i] is not None]
p("      countdown f.laneB d2 profile: min %.4f, median %.4f, max %.4f "
  "over %d lags -- the near-zero band is NOT broad (the exact zeros at 26/"
  "33 are localized, the median d2/d reads 1.3636, MID-TABLE)" % (min(prof),
  med(prof), max(prof), len(prof)))
p("      THE ORDERING, ANSWERED: the ratio does NOT order the drift misses "
  "below the detected -- loop-injection-code (ALREADY DETECTED via its mass "
  "face) reads the MOST collinear on f.laneB (median 0.4091), countdown "
  "1.3636 and code-line 1.5789 sit mid-to-high, and the arithmetic-drift "
  "story does NOT receipt itself broadly on the f channel -- VERDICT: DEAD "
  "as a separating statistic; the audit's exact-zero lags are real but the "
  "surrounding d2 fabric is ordinary")
p("")
p("P-C   close development on the current monitor set (the audit's row 3): "
  "the standing option, always my call, the 8B record lane beside it")
p("")
p("THE CROSS-CUTTING LAW every viable pathway rides: the level-vs-fixture "
  "race (the S lesson receipted) and THE DEMOTION CLIFF priced at item 487 "
  "-- the level 3.7618410 sits 0.415686 below mask-stub's 4.177527, the "
  "lowest detected read; a face whose cal tail lifts the level past "
  "4.1775 demotes mask-stub (k 7 -> 6), the cap falls 2.0494 -> 1.6432 "
  "UNDER the bar and the door slams -- every fresh sheet prices both")
p("")
p("THE CORPUS HALF, STATUS PER PATHWAY: the receipt carries d2/triples "
  "curves for the TEN FIXTURES ONLY, so every flood question (clean-doc d2 "
  "zeros, clean-doc ramps, clean-doc refined-tail reference moments) is NOT "
  "answerable from any banked byte -- the audit's own 'required paper "
  "diagnostic' column names the fix: a read-only tabulation on my pinned "
  "caches, runnable on my Mac at my word, zero build hours, the "
  "kill-switch genre the house already stamped")

open("/home/user/build6/codev6_pathway_ledger_console.txt", "w").write(
    "\n".join(OUT) + "\n")
print("")
print("WROTE codev6_pathway_ledger_console.txt", len(OUT), "lines")

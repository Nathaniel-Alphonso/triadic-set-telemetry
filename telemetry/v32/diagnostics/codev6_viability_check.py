"""THE VIABILITY CHECK AT HIS WORD ("okay check these out for viability") --
every numeric claim in his pasted audit re-derived from the run-of-record
receipt's own bytes (the battery genre, findings presented, never
adjudicated), plus the within-loop tables the audit did not compute."""
import json, importlib.util, math

spec = importlib.util.spec_from_file_location(
    "K", "/home/user/knowledge/exit-gate-project/checkpoint-build6/"
         "triadic_rw17_codev5.py")
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

R5 = json.load(open("/home/user/knowledge/exit-gate-project/"
                    "run-record-codev5/rc_codev5_receipt.json"))
LEG = R5["legs"]["mbpprw17"]
OUT = []
def p(s=""):
    OUT.append(s)
    print(s)

def med(v):
    s = sorted(v); n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2

OK, BAD, PART = "  VERIFIED", "  MISMATCH", "  PARTIAL"

p("=== THE VIABILITY CHECK, HIS PASTED AUDIT vs THE RECEIPT BYTES ===")
p("source: rc_codev5_receipt.json sha fc8b70b5435cefbc419b3b10dd0aeae6b579"
  "dcad1b7bfcaac5d11660b6e6cc42, leg mbpprw17, the run of record")
p("")

# ---------- SECTION 2: the moment reconstruction ----------
p("--- [S2] THE MOMENT RECONSTRUCTION ---")
tj = LEG["t_joint"]
rows = LEG["loop_census"]
Ds = {row["fixture"]: row["D"] for row in rows}
det = sorted(v for v in Ds.values() if v >= tj)
miss = sorted(v for v in Ds.values() if v < tj)
mu_det = sum(det) / len(det)
mu_miss = sum(miss) / len(miss)
mu_loop = (sum(det) + sum(miss)) / 10
ss = sum((d - mu_loop) ** 2 for d in Ds.values())
s_loop = math.sqrt(ss / 9)
p("detected D set: " + ", ".join("%.6f" % d for d in det) + "  (k=%d)" % len(det))
p("  audit claims 7.989752/8.507609/6.843795/7.913068/6.352898/5.730605/"
  "4.177527, mu 6.787893 -> receipt mu_det %.6f %s"
  % (mu_det, OK if abs(mu_det - 6.787893) < 5e-6 else BAD))
p("missed D set: " + ", ".join("%.6f" % d for d in miss))
p("  audit claims 1.381425/0.459473/3.492749, mu 1.777882 -> receipt mu_miss "
  "%.6f %s" % (mu_miss, OK if abs(mu_miss - 1.777882) < 5e-6 else BAD))
p("mu_loop receipt %.6f (audit 5.284890) %s; s_loop receipt %.6f (audit "
  "2.815408) %s; SS %.6f (audit 71.338711) %s"
  % (mu_loop, OK if abs(mu_loop - 5.284890) < 5e-6 else BAD,
     s_loop, OK if abs(s_loop - 2.815408) < 5e-6 else BAD,
     ss, OK if abs(ss - 71.338711) < 5e-5 else BAD))
cfg = LEG["coverage_census"]["configuration"]
zp = cfg["detected_mean_height_held_units"]
zm = cfg["misses_z_minus_realized"]
sig = (mu_det - mu_miss) / (zp - zm)
muh = mu_miss - zm * sig
rms = math.sqrt((s_loop ** 2 + sig ** 2) / 2)
gap = (mu_loop - muh) / rms
p("z+ receipt %.8f (audit 3.97797182) %s; z- receipt %.8f (audit 0.14888215)"
  " %s" % (zp, OK if abs(zp - 3.97797182) < 1e-7 else BAD,
           zm, OK if abs(zm - 0.14888215) < 1e-7 else BAD))
p("sigma_held receipt %.6f (audit 1.308408) %s; mu_held receipt %.6f (audit "
  "1.583084) %s" % (sig, OK if abs(sig - 1.308408) < 5e-6 else BAD,
                     muh, OK if abs(muh - 1.583084) < 5e-6 else BAD))
p("RMS receipt %.6f (audit 2.195274) %s; gap receipt %.6f (audit 1.686262) %s"
  % (rms, OK if abs(rms - 2.195274) < 5e-6 else BAD,
     gap, OK if abs(gap - 1.686262) < 5e-6 else BAD))
sup = LEG["coverage_census"]["sup"]
supc = LEG["coverage_census"]["sup_corrected_at_realized_z_minus"]
p("sup receipt %.6f (audit 2.049390) %s; sup corrected receipt %.6f (audit "
  "2.060178) %s" % (sup, OK if abs(sup - 2.049390) < 5e-6 else BAD,
                    supc, OK if abs(supc - 2.060178) < 5e-6 else BAD))
halves = {}
for row in LEG["doc_rows"]:
    halves[row["half"]] = halves.get(row["half"], 0) + 1
p("doc_rows half census: " + str(halves)
  + " -- the audit's 'N_held = 189' named here for what it is: the receipt "
    "carries no 189 anywhere; the held-side moments were derived from z+/z- "
    "ratios, never a count, and the 189 figure is UNSUPPORTED (peripheral to "
    "every other number)")
p("")

# ---------- SECTION 3: the drift claims ----------
p("--- [S3] THE DRIFT CLAIMS (fixture_curves, laneB unless named) ---")
fc = LEG["fixture_curves"]
def curve(name, mon, lane):
    c = fc[name][mon][lane]
    return ({K.LAGS[i]: c["d"][i] for i in range(35) if c["d"][i] is not None},
            {K.LAGS[i]: c["pairs"][i] for i in range(35)},
            c["d"], c["pairs"])

cd_E = curve("loop-seeded-countdown", "E", "laneB")
p("countdown E.laneB: d(2)=%.4f d(3)=%.4f d(4)=%.4f d(33)=%.4f; audit claims "
  "0.3253/0.4082/0.4936/1.3490 %s"
  % (cd_E[0][2], cd_E[0][3], cd_E[0][4], cd_E[0][33],
     OK if (abs(cd_E[0][2]-0.3253) < 5e-4 and abs(cd_E[0][3]-0.4082) < 5e-4
            and abs(cd_E[0][4]-0.4936) < 5e-4
            and abs(cd_E[0][33]-1.3490) < 5e-4) else BAD))
mono = all(cd_E[0][K.LAGS[i]] <= cd_E[0][K.LAGS[i+1]]
           for i in range(34) if K.LAGS[i] in cd_E[0] and K.LAGS[i+1] in cd_E[0])
p("  monotone across all supported lags: %s (audit says 'climbs monotonically';"
  " expansion d(33)/d(2) = %.2fx vs audit 4.15x)"
  % ("YES" if mono else "NO", cd_E[0][33] / cd_E[0][2]))
cd_fu = curve("loop-seeded-countdown", "f", "unmasked")
seq = [cd_fu[0][L] for L in K.LAGS if L in cd_fu[0]]
strict = all(seq[i] < seq[i+1] for i in range(len(seq)-1))
p("countdown f.unmasked: d(2)=%.4f d(36)=%.4f; audit claims 0.1242/0.7257 %s; "
  "STRICTLY monotone at every lag: %s (audit: yes); %.2fx vs audit 5.84x"
  % (cd_fu[0][2], cd_fu[0][36],
     OK if (abs(cd_fu[0][2]-0.1242) < 5e-4 and abs(cd_fu[0][36]-0.7257) < 5e-4)
     else BAD, "YES" if strict else "NO", cd_fu[0][36]/cd_fu[0][2]))
cl_E = curve("loop-seeded-code-line", "E", "laneB")
p("code-line E.laneB: d(2)=%.4f d(3)=%.4f d(36)=%.4f; audit claims "
  "0.2950/0.3560/0.9025 %s; %.2fx vs audit 3.06x"
  % (cl_E[0][2], cl_E[0][3], cl_E[0][36],
     OK if (abs(cl_E[0][2]-0.2950) < 5e-4 and abs(cl_E[0][3]-0.3560) < 5e-4
            and abs(cl_E[0][36]-0.9025) < 5e-4) else BAD,
     cl_E[0][36]/cl_E[0][2]))
cl_f = curve("loop-seeded-code-line", "f", "laneB")
p("code-line f.laneB: d(2)=%.4f d(36)=%.4f; audit claims 0.1614/1.0060 %s; "
  "%.2fx vs audit 6.23x"
  % (cl_f[0][2], cl_f[0][36],
     OK if (abs(cl_f[0][2]-0.1614) < 5e-4 and abs(cl_f[0][36]-1.0060) < 5e-4)
     else BAD, cl_f[0][36]/cl_f[0][2]))
p("")

# ---------- SECTION 4A: the d2 claims ----------
p("--- [S4A] THE d2 CLAIMS (f.laneB unless named) ---")
def d2cur(name, mon="f", lane="laneB"):
    c = fc[name][mon][lane]
    return ({K.LAGS[i]: c["d2"][i] for i in range(35) if c["d2"][i] is not None},
            {K.LAGS[i]: c["triples"][i] for i in range(35) if c["d2"][i] is not None},
            {K.LAGS[i]: c["d"][i] for i in range(35) if c["d2"][i] is not None},
            {K.LAGS[i]: c["pairs"][i] for i in range(35)})

cd_d2 = d2cur("loop-seeded-countdown")
mind = min(cd_d2[2].values())
zeros = sorted(L for L, v in cd_d2[0].items() if v == 0.0)
p("countdown f.laneB: min first-order d = %.4f (audit 0.0914) %s"
  % (mind, OK if abs(mind - 0.0914) < 5e-4 else BAD))
p("  exact d2 zeros at lags: " + str(zeros)
  + "  (audit: P=26, 33)")
for L in (25, 26, 27, 33, 35):
    if L in cd_d2[0]:
        p("    P=%d: d2=%.4f triples=%d d=%.4f pairs=%d"
          % (L, cd_d2[0][L], cd_d2[1][L], cd_d2[2][L], cd_d2[3][L]))
aud = (abs(cd_d2[0].get(26, 1) - 0.0) < 1e-12 and cd_d2[1].get(26) == 20
       and abs(cd_d2[2].get(26, 1) - 0.2287) < 5e-4
       and abs(cd_d2[0].get(33, 1) - 0.0) < 1e-12 and cd_d2[1].get(33) == 12
       and abs(cd_d2[2].get(33, 1) - 0.1115) < 5e-4
       and abs(cd_d2[0].get(25, 1) - 0.0558) < 5e-4 and cd_d2[1].get(25) == 22
       and abs(cd_d2[0].get(27, 1) - 0.0682) < 5e-4 and cd_d2[1].get(27) == 18
       and abs(cd_d2[0].get(35, 1) - 0.0722) < 5e-4 and cd_d2[1].get(35) == 17)
p("  the audit's countdown d2 table (zeros 26/33, triples 20/12, d 0.2287/"
  "0.1115, near-zeros 0.0558/0.0682/0.0722 at 25/27/35, triples 22/18/17): %s"
  % OK if aud else BAD)
js_d2 = d2cur("loop-seeded-json")
jz = sorted(L for L, v in js_d2[0].items() if v == 0.0)
runs = []
cur = [jz[0]] if jz else []
for L in jz[1:]:
    if L == cur[-1] + 1: cur.append(L)
    else: runs.append(cur); cur = [L]
if cur: runs.append(cur)
p("json f.laneB: exact d2 zeros at %d supported lags %s" % (len(jz), jz))
p("  zero runs: " + str(runs) + "  (audit: 11 zeros, 6-lag run 25..30, "
  "2-lag run 14,15)")
jtr = [js_d2[1][L] for r in runs for L in r]
p("  triples over the runs span %d..%d (audit: 16..35 / 23..25) %s"
  % (min(jtr), max(jtr), OK if min(jtr) == 16 and max(jtr) == 35 else PART))
cl_d2 = d2cur("loop-seeded-code-line")
mn = min(cl_d2[0].values()); mx = max(cl_d2[0].values())
mnL = min(cl_d2[0], key=cl_d2[0].get); mxL = max(cl_d2[0], key=cl_d2[0].get)
p("code-line f.laneB d2: min %.4f at P=%d (audit 0.0454 at P=2) %s; max "
  "%.4f at P=%d (audit 2.0446 at P=32) %s"
  % (mn, mnL, OK if abs(mn-0.0454) < 5e-4 and mnL == 2 else BAD,
     mx, mxL, OK if abs(mx-2.0446) < 5e-4 and mxL == 32 else BAD))
p("")

# ---------- the within-loop d2 zero census (the audit did not compute) ----
p("--- [NEW] THE d2 ZERO CENSUS, ALL 10 FIXTURES, f.laneB (the within-loop"
  " structure the audit left unread) ---")
for name in sorted(fc):
    c = fc[name]["f"]["laneB"]
    z = sorted(K.LAGS[i] for i in range(35)
              if c["d2"][i] is not None and c["d2"][i] == 0.0)
    pairs_ok = [K.LAGS[i] for i in range(35)
                if c["d2"][i] is not None and c["pairs"][i] >= K.LOW_SUPPORT_PAIRS]
    z_sup = [L for L in z if L in pairs_ok]
    tr = [c["triples"][K.LAGS.index(L)] for L in z_sup]
    p("%-27s d2 zeros %2d (supported %2d) lags %s  triples %s"
      % (name, len(z), len(z_sup), z_sup, tr))
p("")

# ---------- SECTION 4B: the ramp claims ----------
p("--- [S4B] THE RAMP CLAIMS (R = 1 - med_early/med_late, early {2,3,4}, "
  "late {28..36}) ---")
def ramp(name, mon, lane):
    c = fc[name][mon][lane]
    e = [c["d"][K.LAGS.index(L)] for L in (2, 3, 4)
         if c["d"][K.LAGS.index(L)] is not None]
    l = [c["d"][K.LAGS.index(L)] for L in range(28, 37)
         if c["d"][K.LAGS.index(L)] is not None]
    if not e or not l or med(l) <= 1e-12: return None
    return 1.0 - med(e) / med(l)

vals = {
    ("loop-seeded-countdown", "E", "laneB"): 0.6758,
    ("loop-seeded-countdown", "E", "unmasked"): 0.7023,
    ("loop-seeded-code-line", "f", "laneB"): 0.8067,
    ("loop-seeded-code-line", "E", "laneB"): 0.5814,
}
for (name, mon, lane), aud_v in vals.items():
    R = ramp(name, mon, lane)
    p("%-27s %s.%s: R receipt %.4f (audit %.4f) %s"
      % (name, mon, lane, R, aud_v,
         OK if abs(R - aud_v) < 5e-4 else BAD))
p("")
p("--- [NEW] THE RAMP, ALL 10 FIXTURES, E.laneB and f.laneB (the "
  "within-loop ordering the flood question rides on) ---")
for name in sorted(fc):
    RE = ramp(name, "E", "laneB")
    Rf = ramp(name, "f", "laneB")
    p("%-27s R(E.laneB) %-7s R(f.laneB) %-7s D_joint %.4f %s"
      % (name, "%.4f" % RE if RE is not None else "None",
         "%.4f" % Rf if Rf is not None else "None",
         Ds[name], "<== REGIME-C" if name in
         ("loop-injection-code", "loop-seeded-code-line",
          "loop-seeded-countdown", "loop-seeded-json") else ""))
p("")

# ---------- the kappa claims ----------
p("--- [S4B] THE KAPPA CLAIMS (lane A reference) ---")
refE = LEG["lane_references"]["A"]["E"]
p("cal reference A.E: mean %.4f sd %.4f n %d (audit 0.4522 +/- 0.1005) %s"
  % (refE["mean"], refE["sd"], refE["n"],
     OK if abs(refE["mean"] - 0.4522) < 5e-4 and abs(refE["sd"] - 0.1005) < 5e-4
     else BAD))
for name, aud_k, aud_z in (("loop-seeded-countdown", 0.4849, 0.3258),
                           ("loop-seeded-code-line", 0.5910, 1.3814)):
    row = [r for r in rows if r["fixture"] == name][0]
    kE = row["kappa_cells"]["E"]
    zE = (kE - refE["mean"]) / refE["sd"]
    p("%-27s kappa_E %.4f (audit %.4f) %s -> z_A-E %.4f (audit %.4f) %s"
      % (name, kE, aud_k, OK if abs(kE - aud_k) < 5e-4 else BAD,
         zE, aud_z, OK if abs(zE - aud_z) < 5e-4 else BAD))
p("")

# ---------- the coupled-operator flag ----------
p("--- [S1] THE COUPLED-OPERATOR FLAG, ANSWERED FROM THE BANK ---")
p("the audit's flag is LEGITIMATE and already half-receipted in the house's "
  "own bytes:")
p("  the item-484 projection family held the held side untouched AND the "
  "level fixed at its run value (countdown lifted to just-clear AT t_joint "
  "3.7618) -- a conditional projection, named as a projection, never a "
  "receipt;")
p("  the CODE-V5 run receipts the coupling empirically: t_joint 3.4693 -> "
  "3.7618 (+0.2926) while json lifted only +0.1534 -- the clean tail rode "
  "1.91x faster than the fixture, and the raw gap MOVED DOWN 1.7108 -> "
  "1.6863 even as a loop fixture lifted;")
p("  so the honest bound is: 2.1269 is the FIXED-LEVEL value of converting "
  "countdown; any conversion delivered by a new face rides the same "
  "level-vs-fixture race the S face lost, and the realized post-conversion "
  "gap is BELOW 2.1269 by the size of the level move -- the V6 sheet's own "
  "level-vs-fixture ledger existed to receipt exactly this, and any fresh "
  "sheet carries it;")
p("  one correction to the audit's framing: the assumption was never "
  "unstated -- item 484 pinned the projections as projections and the sheet "
  "pinned the ledger -- but the flag's arithmetic is right and the bound "
  "binds.")
p("")

# ---------- the corpus-side honesty ----------
p("--- THE CORPUS HALF, NAMED HONESTLY ---")
p("the receipt carries d2/triples curves for THE TEN FIXTURES ONLY (the "
  "tool's doc_d2_census runs on fixtures; doc_rows carry composite reads, "
  "never per-doc curves) -- so BOTH candidate families' flood questions "
  "(clean-doc d2 zeros; clean-doc ramp) are NOT answerable from any banked "
  "bytes;")
p("the within-loop tables above answer what CAN be answered offline: the "
  "ordering question -- whether the candidate statistic even separates the "
  "misses from the detected inside the loop population before the corpus "
  "is ever consulted.")

open("/home/user/build6/codev6_viability_check_console.txt", "w").write(
    "\n".join(OUT) + "\n")
print("")
print("WROTE codev6_viability_check_console.txt", len(OUT), "lines")

"""CODE-V6 DIAGNOSTIC, PART 1 (the receipt's own fixture curves; the
pinned flank-contrast face read EXACTLY as sheeted; findings presented,
never adjudicated)."""
import json, importlib.util

spec = importlib.util.spec_from_file_location(
    "K", "/home/user/knowledge/exit-gate-project/checkpoint-build6/"
          "triadic_rw17_codev5.py")
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

r5 = json.load(open("rc_codev5_receipt.json"))
CONT = ("E", "H", "PR", "rho", "s")
RC4 = ("loop-injection-code", "loop-seeded-code-line",
       "loop-seeded-countdown", "loop-seeded-json")
W_NB, MIN_FLANK = 4, 3
out = []
def p(s=""):
    out.append(s)
    print(s)

p("=== THE CODE-V6 DIAGNOSTIC, PART 1 (the pinned sheet (d): the "
  "run-of-record receipt's own fixture curves; zero GPU, zero decodes) ===")
p("the form, pinned: T = 1 - d(P*)/flank_med(P*), P* the curve's global")
p("  argmin over supported in-window lags {2..36}, flanks P*+-1..P*+-4")
p("  EXCLUDING the trough lag, >= 3 supported flank lags, W_NB = 4 by")
p("  convention, never on results -- read EXACTLY as sheeted, never tuned")
p("")

def med(vals):
    s = sorted(vals)
    n = len(s)
    return (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)

def flank_T(d_vals, pairs):
    sup = [i for i in range(35)
           if d_vals[i] is not None and pairs[i] >= K.LOW_SUPPORT_PAIRS]
    if not sup:
        return None, None, "EMPTY_no_supported_lag", 0, None, None
    i_star = min(sup, key=lambda i: d_vals[i])
    lag_star = K.LAGS[i_star]
    fl = [i for i in sup
          if abs(K.LAGS[i] - lag_star) in (1, 2, 3, 4)]
    if len(fl) < MIN_FLANK:
        return lag_star, None, "EMPTY_no_flank", len(fl), None, i_star
    fm = med([d_vals[i] for i in fl])
    if fm <= 1e-12:
        return lag_star, None, "EMPTY_degenerate_flank", len(fl), fm, i_star
    T = 1.0 - d_vals[i_star] / fm
    # the run-law status at P* (the carried depth's own three conditions)
    nb = [i for i in sup if abs(K.LAGS[i] - lag_star) <= K.W_LOCAL]
    if len(nb) < K.MIN_NEIGHBOR_LAGS:
        status = "NO_NEIGHBORHOOD"
    else:
        ml = med([d_vals[i] for i in nb])
        if ml <= 1e-12 or not d_vals[i_star] < ml:
            status = "NOT_BELOW_LOCAL_MED"
        else:
            adj = any(abs(K.LAGS[i] - lag_star) == 1
                      and d_vals[i] < med([d_vals[j] for j in sup
                                          if abs(K.LAGS[j] - K.LAGS[i])
                                          <= K.W_LOCAL])
                      for i in sup)
            status = "QUALIFYING" if adj else "ISOLATED_DIP"
    return lag_star, T, status, len(fl), fm, i_star

p("fixture                     | mon | P* | d(P*)  | flank_med | T      "
  "| run-law at P*     | carried depth | depth z")
for leg in ("mbpprw17", "prose17p-rw17", "p2corpus-rw17"):
    lg = r5["legs"][leg]
    p("")
    p("--- LEG " + leg + " (t_joint " + repr(lg["t_joint"]) + ") ---")
    for name in sorted(lg["fixture_curves"]):
        for m in CONT:
            lb = lg["fixture_curves"][name][m]["laneB"]
            lag_star, T, status, nfl, fm, _ = flank_T(lb["d"], lb["pairs"])
            dep = K.depth_from_curve(lb["d"], lb["pairs"])
            ref = lg["lane_references"]["B"][m]
            z_dep = ((dep["depth"] - ref["mean"]) / ref["sd"]
                     if dep["depth"] is not None and ref.get("sd")
                     else None)
            mark = " <== REGIME-C" if name in RC4 else ""
            T_s = "EMPTY:" + status if T is None else "%.4f" % T
            p("%-27s | %-3s | %2s | %-7.4g | %-9.4g | %-6s | %-16s | %-13.4g | %.3f%s"
              % (name, m, lag_star, lb["d"][_] if _ is not None else -1,
                 fm if fm is not None else -1, T_s, status,
                 dep["depth"] if dep["depth"] is not None else -1,
                 z_dep if z_dep is not None else 0, mark))

# the named verdicts (the sheet (d) first questions)
p("")
p("=== THE FIRST QUESTIONS, NAMED ===")
for leg in ("mbpprw17", "prose17p-rw17", "p2corpus-rw17"):
    lg = r5["legs"][leg]
    p("")
    p("--- " + leg + " ---")
    for name in ("loop-seeded-code-line", "loop-seeded-countdown",
                 "loop-seeded-json", "loop-injection-code"):
        lb = lg["fixture_curves"][name]["PR"]["laneB"]
        lag_star, T, status, nfl, fm, i_star = flank_T(lb["d"], lb["pairs"])
        dep = K.depth_from_curve(lb["d"], lb["pairs"])
        p("%-24s PR: argmin P*=%s  T=%s  (%s)  | the carried depth "
          "maxes at %.4g (argmax lag %s) -- the trough ITSELF reads %s "
          "the flank law" % (name, lag_star,
                             "EMPTY" if T is None else "%.4f" % T,
                             status, dep["depth"] if dep["depth"] is not None else -1,
                             dep["argmax_lag"],
                             "BESIDE" if (dep["argmax_lag"] != lag_star
                                          and T is not None) else "AT"))

open("codev6_diagnostic_part1.txt", "w").write("\n".join(out) + "\n")
print("\nWROTE codev6_diagnostic_part1.txt", len(out), "lines")

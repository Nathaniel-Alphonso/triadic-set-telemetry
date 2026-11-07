"""THE CORPUS-SIDE DIAGNOSTIC AT HIS STAMP ("okay youve got my stamp") --
read-only, zero GPU, zero decodes, the kill-switch genre: the P-B4
refined-tail reference + the full level/coverage/gap projection + the P-A1
d2 zero-run mass census, computed on his pinned cache bytes beside the
run-of-record receipt. The form is read EXACTLY as the item-488 ledger
computed it (refined tail = 1 - min(d over supported lags 19..36) /
med(d over supported lags 28..36), the masked E curve, the tool's own
support law) -- a DIAGNOSTIC read, never a pinned form; a pinned window
waits for a fresh sheet at his word. Findings presented, never
adjudicated.

RUN (his Mac, one working dir): the script beside triadic_rw17_codev5.py,
the three pinned caches, and rc_codev5_receipt.json; then
    python3 codev7_corpus_diagnostic.py            (the single-face read)
    python3 codev7_corpus_diagnostic.py --combined (the two-face read)
which emits codev7_corpus_diagnostic_console.txt for his shasum + upload.
--parity-only runs the receipt-side gates alone (no caches needed).

THE --combined MODE (his stamp, the 8B record lane discussion): the two
faces under the tool's OWN max-spine conjunction -- D_new = max(D,
z_refined, z_d2mass) per doc, the refined-tail cell (P-B4) and the d2
zero-run-mass cell (P-A1, the pinned S face's law mirrored onto d2), each
z against its own cal reference, the triples gate swept (8/12/16, the
sheet pins one at his word never tuned to the answer); the level
re-derives, the gap re-derives, the demotion cliff read beside them.
THE CORRECTION NAMED BEFORE THE DRAFT: the item-491 optimistic bound
1.980063 UNDERSTATED the fixture side -- under the combined species the
d2 cell's biggest read belongs to loop-injection-code (already
detected, m_d2 21, z 15.3266), its D lifting 7.989752 -> 15.326556 and
WIDENING the loop sd 2.815408 -> 3.976060 -- the sd drag beats the mean
lift and the honest fixture-side bound reads 1.606504 DOWN 0.0798 from
the receipt, the k 7 -> 8 json flip live beside it (the level-fixed
world); findings presented, never adjudicated.
"""
import json, os, sys
import importlib.util

PREFIX = "[codev7d] "

def die(msg, code=1):
    print(PREFIX + msg)
    sys.exit(code)

def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

TOOL_SHA_BANK = ("391ac7dfd91f4c45c7c113211005a8bb44565737887331fd"
                 "512ed9723b4c2cf3")
RECEIPT_NAME = "rc_codev5_receipt.json"
TOOL_NAME = "triadic_rw17_codev5.py"
CONSOLE_NAME = "codev7_corpus_diagnostic_console.txt"
TAIL_LO, TAIL_HI = 19, 36          # the tail domain (> HARM_P_MAX)
LATE_LO, LATE_HI = 28, 36          # the late window (the item-488 read)
PARITY_TOL = 1e-12
BANKED_REFINED = {                  # the item-488 fixture table (mbpprw17)
    "loop-seeded-countdown": 0.368124, "loop-injection-code": 0.321772,
    "mask-reserved-stubborn": 0.299363, "loop-seeded-chant": 0.258515,
    "loop-injection-prose": 0.252647, "loop-seeded-cycle": 0.212269,
    "loop-seeded-counter": 0.141779, "loop-seeded-affirm": 0.127843,
    "loop-seeded-json": 0.057367, "loop-seeded-code-line": 0.036616,
}
BANKED_MD2 = {"loop-seeded-json": 8, "loop-seeded-countdown": 0,
              "loop-seeded-code-line": 0, "loop-injection-code": 21,
              "loop-seeded-chant": 0}
D2_GATES = (8, 12, 16)
# his uploaded console (ITEM 490): the per-leg cal references, the
# parity anchors for the combined fixture-side gate
BANKED_CONSOLE_REFS = {
    "mbpprw17": ((0.195457, 0.120401), (0.275000, 1.352227)),
    "prose17p-rw17": ((0.188923, 0.126210), (1.548387, 3.896216)),
    "p2corpus-rw17": ((0.147374, 0.100288), (1.154667, 3.072663)),
}
# the CORRECTED combined fixture-side bounds (level-fixed, held fixed
# at the receipt's own moments -- the optimistic world, computed this
# act on the receipt curves + his console references; the item-491
# 1.980063 omitted injection-code's own d2 lift, named above)
BANKED_COMBINED_BOUND = {"mbpprw17": 1.606504, "prose17p-rw17": 1.753702,
                         "p2corpus-rw17": 1.772590}

OUT = []
def p(s=""):
    OUT.append(s)
    print(s)

def load_tool():
    if not os.path.exists(TOOL_NAME):
        die(f"tool {TOOL_NAME} not found beside this script -- the "
            f"diagnostic imports the tool's own curve machinery; aborting.")
    spec = importlib.util.spec_from_file_location("K", TOOL_NAME)
    K = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(K)
    return K

def load_receipt():
    if not os.path.exists(RECEIPT_NAME):
        die(f"receipt {RECEIPT_NAME} not found beside this script -- the "
            f"run-of-record receipt is the before-column and the parity "
            f"source; aborting.")
    with open(RECEIPT_NAME) as f:
        r = json.load(f)
    ts = r.get("tool_sha256", "")
    if ts != TOOL_SHA_BANK:
        die(f"receipt tool_sha256 {ts} != the banked run-of-record tool "
            f"{TOOL_SHA_BANK} -- never project onto foreign bytes; "
            f"aborting.")
    return r

# ---- the P-B4 form, read EXACTLY as the item-488 ledger computed it ------
def refined_tail(d_vals, pair_counts, K):
    """refined tail = 1 - min(d over supported lags 19..36) / med(d over
    supported lags 28..36); supported = d not None and pairs >=
    LOW_SUPPORT_PAIRS; the tool's own support law; EMPTY named, never
    imputed."""
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

def m_d2(d2_vals, triples, t_min):
    """the d2 zero-run mass, the item-475 law mirrored on d2: m = zero
    lags in runs of >= 2 consecutive supported lags (supported = d2 not
    None and triples >= t_min); ISOLATED zeros NEVER count; the draft
    constant's injection-code 20 was corrected against the receipt
    bytes before publish (23 supported zeros, 21 in runs, 2 isolated
    -- the item-470 off-by-one genre named, never banked silent)."""
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

# ---- the projection machinery (shared by parity gates and the run) ------
def project(r, leg_name, z_cal, z_held, z_fix, K):
    """D_new = max(D_receipt, z) per doc (can-only-add by construction);
    the level re-derives (quantile 0.95 over cal D_new); the gap re-derives
    in the item-439 convention; returns the full readout dict."""
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

# ---- parity-only mode: the receipt-side gates, no caches ----------------
def parity_only(K, r):
    p("=== PARITY-ONLY MODE (the receipt-side gates; no caches read) ===")
    lg = r["legs"]["mbpprw17"]
    # gate 1: the item-488 fixture refined tails reproduce byte-close
    p("[G1] the P-B4 fixture table (the item-488 bank) reproduced from the "
      "receipt's own fixture curves")
    for name, bank in sorted(BANKED_REFINED.items(),
                             key=lambda kv: -kv[1]):
        c = lg["fixture_curves"][name]["E"]["masked"]
        v, status = refined_tail(c["d"], c["pairs"], K)
        ok = (v is not None and abs(v - bank) < 1e-6)
        p("  %-27s refined %.6f vs banked %.6f %s %s"
          % (name, v if v is not None else -1.0, bank,
             "OK" if ok else "MISMATCH", status))
        if not ok:
            die("the refined-tail form does not reproduce the banked table "
                "-- the diagnostic's own arithmetic is broken; aborting.")
    # gate 2: the gap + level re-derivation from the receipt's own rows
    p("[G2] the gap and the level re-derived from doc_rows + loop_census "
      "(the dropped rows excluded, the receipt's own convention)")
    zero = {}
    proj = project(r, "mbpprw17", zero, zero, zero, K)
    banked_gap = lg["readouts"]["raw"]["gap"]
    p("  gap recomputed %.16f vs the receipt's raw gap %.16f  %s"
      % (proj["gap_new"], banked_gap,
         "OK" if abs(proj["gap_new"] - banked_gap) < 1e-9 else "MISMATCH"))
    p("  t_joint recomputed %.16f vs the receipt's t_joint %.16f  %s"
      % (proj["t_now"], lg["t_joint"],
         "OK" if abs(proj["t_now"] - lg["t_joint"]) < 1e-12 else "MISMATCH"))
    if (abs(proj["gap_new"] - banked_gap) >= 1e-9
            or abs(proj["t_now"] - lg["t_joint"]) >= 1e-12):
        die("the projection machinery does not preserve the run-of-record "
            "at zero lift -- aborting.")
    # gate 3: the null projection (zero lift changes nothing, k and the
    # fixture reads byte-stable)
    p("[G3] the null projection: zero lift -> k %d, lifted %s, demoted %s "
      "(must be empty)"
      % (proj["k_now"], proj["lifted"] or "[]", proj["demoted"] or "[]"))
    if proj["lifted"] or proj["demoted"] or proj["k_new"] != proj["k_now"]:
        die("the null projection moved something -- aborting.")
    p("  OK (zero lift preserves the run-of-record exactly)")
    # gate 4: the P-A1 fixture m_d2 census reproduced
    p("[G4] the P-A1 fixture d2 zero-run census (support: triples >= 8, "
      "runs >= 2, isolated never count; the draft constant's "
      "injection-code 20 corrected against the receipt bytes -- 21 in "
      "runs, 23 supported zeros, the item-470 off-by-one genre named "
      "before publish)")
    for name, bank in sorted(BANKED_MD2.items()):
        c = lg["fixture_curves"][name]["f"]["laneB"]
        m, zeros = m_d2(c["d2"], c["triples"], K.LOW_SUPPORT_PAIRS)
        ok = m == bank
        p("  %-27s m_d2 %d vs banked %d %s (supported zero lags %s)"
          % (name, m, bank, "OK" if ok else "MISMATCH",
             [K.LAGS[i] for i in zeros]))
        if not ok:
            die("the m_d2 form does not reproduce the banked census -- "
                "aborting.")
    # gate 5: the combined fixture-side bound (the corrected anchors)
    p("[G5] the combined fixture side (D_new = max(D, z_refined, z_d2), "
      "gate 8, his console's banked references, held fixed at the "
      "receipt's own moments -- the level-fixed optimistic world)")
    for leg in K.LEGS:
        lgc = r["legs"][leg]
        (mr, sr), (md, sdv) = BANKED_CONSOLE_REFS[leg]
        fix = {x["fixture"]: x["D"] for x in lgc["loop_census"]}
        held = [x["D"] for x in lgc["doc_rows"]
                if x["half"] == "held" and x["D"] is not None]
        mu_h, sd_h = K.mean_std(held)
        new = {}
        for n, D in fix.items():
            cur = lgc["fixture_curves"][n]
            v, _ = refined_tail(cur["E"]["masked"]["d"],
                                cur["E"]["masked"]["pairs"], K)
            m, _ = m_d2(cur["f"]["laneB"]["d2"],
                        cur["f"]["laneB"]["triples"], K.LOW_SUPPORT_PAIRS)
            cands = [D]
            if v is not None:
                cands.append((v - mr) / sr)
            cands.append((m - md) / sdv)
            new[n] = max(cands)
        vals = list(new.values())
        mu_l, sd_l = K.mean_std(vals)
        gap = (mu_l - mu_h) / ((sd_l ** 2 + sd_h ** 2) / 2.0) ** 0.5
        bank = BANKED_COMBINED_BOUND[leg]
        ok = abs(gap - bank) < 1e-4
        p("  %-15s combined fixture-side gap %.6f vs the corrected bank "
          "%.6f %s  (k at the level-fixed read: %d -> %d)"
          % (leg, gap, bank, "OK" if ok else "MISMATCH",
             sum(1 for v in fix.values() if v >= lgc["t_joint"]),
             sum(1 for v in new.values() if v >= lgc["t_joint"])))
        if not ok:
            die("the combined fixture-side machinery does not reproduce "
                "the corrected bank -- aborting.")
    p("PARITY-ONLY MODE COMPLETE: the five gates hold; the full mode (his "
      "Mac, the pinned caches) runs the corpus half on the same bytes.")
    return OUT

# ---- the full mode: the corpus half on his pinned caches ----------------
def full_mode(K, r):
    p("=== THE CORPUS-SIDE DIAGNOSTIC, FULL MODE (his pinned caches, "
      "read-only, zero GPU, zero decodes) ===")
    p("the form, read EXACTLY as the item-488 ledger computed it, never "
      "tuned: refined tail = 1 - min(d, supported lags 19..36) / med(d, "
      "supported lags 28..36), masked E curve, the tool's own support law")
    p("")
    for leg in K.LEGS:
        lg = r["legs"][leg]
        cache_path = K.CACHE_FILES[leg]
        if not os.path.exists(cache_path):
            die(f"leg {leg}: cache {cache_path} not found beside this "
                f"script -- aborting.")
        sha = sha256_file(cache_path)
        if sha != K.CACHE_PINS[leg]:
            die(f"leg {leg}: cache sha256 {sha} != the pinned "
                f"{K.CACHE_PINS[leg]} -- the pin-table guard holds; never "
                f"read divergent bytes; aborting.")
        p("--- LEG %s (cache pin MATCH, sha256 %s...) ---" % (leg, sha[:16]))
        recs = K.load_cache(cache_path, leg)
        cal_docs, held_docs = K.split_by_parity(leg, recs["docs"])
        live, inert = K.split_loop_fixtures(leg, recs["loop"])
        fixture_recs = {d["doc_id"]: d for d in live}

        # population parity against the receipt
        rrows = {(row["half"], row["doc_id"])
                 for row in lg["doc_rows"]}
        crows = ({("cal", d["doc_id"]) for d in cal_docs}
                 | {("held", d["doc_id"]) for d in held_docs})
        if rrows != crows:
            die(f"leg {leg}: the cache's doc population does not match the "
                f"receipt's doc_rows (cal/held x doc_id) -- never project "
                f"across populations; aborting.")
        p("  population parity: %d cal + %d held, exact match against the "
          "receipt's doc_rows" % (len(cal_docs), len(held_docs)))

        base = K.compute_baselines(cal_docs, leg)
        f_vals = [v for d in cal_docs
                  for v in d["steps"]["f"] if v is not None]
        f_ref = K.mean_std(f_vals) if f_vals else None
        cal_E = sorted(v for d in cal_docs
                       for v in d["steps"]["E"] if v is not None)
        primary_cut = K.quantile(cal_E, K.MASK_Q_PRIMARY)

        # per-doc refined tail (masked E curve) + m_d2 census (f laneB d2)
        ref_cal, ref_held, status_ct = {}, {}, {}
        md2_cal, md2_held = {}, {}
        f_laneB_cal, f_laneB_held = {}, {}
        trip_at_zero = []
        for pop, docs, ref in (("cal", cal_docs, ref_cal),
                               ("held", held_docs, ref_held)):
            for d in docs:
                cells = K.process_doc_conjunct(d, base, f_ref, primary_cut)
                v, status = refined_tail(cells["E"]["masked"]["d"],
                                         cells["E"]["masked"]["pairs"], K)
                ref[d["doc_id"]] = v
                status_ct[status] = status_ct.get(status, 0) + 1
                d2c = K.doc_d2_census(d, base, f_ref, primary_cut)
                fb = d2c["f"]["laneB"]
                m, zeros = m_d2(fb["d2"], fb["triples"],
                                K.LOW_SUPPORT_PAIRS)
                (md2_cal if pop == "cal" else md2_held)[d["doc_id"]] = m
                (f_laneB_cal if pop == "cal" else f_laneB_held)[
                    d["doc_id"]] = (fb["d2"], fb["triples"])
                if pop == "cal":
                    for i in zeros:
                        trip_at_zero.append(fb["triples"][i])
        vals = [v for v in ref_cal.values() if v is not None]
        n_empty = sum(1 for v in ref_cal.values() if v is None)
        if len(vals) < 2:
            p("  P-B4 cal reference: EMPTY (n %d) -- the face never reads "
              "on this leg, named, the projection skipped" % len(vals))
            continue
        mu, sd = K.mean_std(vals)
        p("  P-B4 CAL REFERENCE (the refined tail over %d cal docs, %d "
          "EMPTY named): mean %.6f sd %.6f min %.6f max %.6f"
          % (len(vals), n_empty, mu, sd, min(vals), max(vals)))
        if sd <= 1e-12:
            p("  sd == 0 -- the face EMPTY_degenerate_sd, never reads; "
              "the projection skipped")
            continue

        # fixture parity (fresh curves vs the receipt's fixture_curves)
        z_fix = {}
        md2_fix = {}
        for name in sorted(fixture_recs):
            cells = K.process_doc_conjunct(fixture_recs[name], base, f_ref,
                                           primary_cut)
            cur = lg["fixture_curves"][name]["E"]["masked"]
            got = cells["E"]["masked"]
            for i in range(len(K.LAGS)):
                a, b = got["d"][i], cur["d"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die(f"leg {leg} fixture {name}: the fresh masked E "
                        f"curve diverges from the receipt's fixture_curves "
                        f"at lag {K.LAGS[i]} -- the curve lineage is not "
                        f"proven; aborting.")
            d2c = K.doc_d2_census(fixture_recs[name], base, f_ref,
                                  primary_cut)
            fb = d2c["f"]["laneB"]
            fcur = lg["fixture_curves"][name]["f"]["laneB"]
            for i in range(len(K.LAGS)):
                a, b = fb["d2"][i], fcur["d2"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die(f"leg {leg} fixture {name}: the fresh laneB f d2 "
                        f"curve diverges from the receipt's fixture_curves "
                        f"at lag {K.LAGS[i]} -- the d2 lineage is not "
                        f"proven; aborting.")
            m, _ = m_d2(fb["d2"], fb["triples"], K.LOW_SUPPORT_PAIRS)
            md2_fix[name] = m
            v, status = refined_tail(got["d"], got["pairs"], K)
            z_fix[name] = (v - mu) / sd if v is not None else None

        z_cal = {did: (v - mu) / sd for did, v in ref_cal.items()
                 if v is not None}
        z_held = {did: (v - mu) / sd for did, v in ref_held.items()
                  if v is not None}

        # the P-B4 projection: D_new = max(D_receipt, z)
        proj = project(r, leg, z_cal, z_held, z_fix, K)
        p("  THE PROJECTION (can-only-add: D_new = max(D, z), the level "
          "re-derives, both sides re-scored identically):")
        p("    t_joint %.6f -> %.6f (%+.6f)  |  k %d -> %d"
          % (proj["t_now"], proj["t_new"], proj["t_new"] - proj["t_now"],
             proj["k_now"], proj["k_new"]))
        p("    held mean/sd %.6f/%.6f -> %.6f/%.6f  |  loop mean/sd "
          "%.6f/%.6f -> %.6f/%.6f"
          % (proj["mu_held_now"], proj["sd_held_now"], proj["mu_held"],
             proj["sd_held"], proj["mu_loop_now"], proj["sd_loop_now"],
             proj["mu_loop"], proj["sd_loop"]))
        p("    THE GAP: %.6f -> %.6f vs the 2.0 bar %s"
          % (lg["readouts"]["raw"]["gap"], proj["gap_new"],
             "(the bar read presented, never adjudicated)"))
        p("    fixture lifts: %s" % (proj["lifted"] or "[]"))
        p("    fixture demotions: %s %s" % (proj["demoted"] or "[]",
           "(mask-reserved-stubborn's cliff named at ITEM 487)" if
           "mask-reserved-stubborn" in proj["demoted"] else ""))
        for name in sorted(fixture_recs):
            zn = z_fix[name]
            p("    %-27s D %.6f -> %.6f  z_refined %s  m_d2 %d"
              % (name, proj["fix_now"][name], proj["fix_new"][name],
                 "%.4f" % zn if zn is not None else "None", md2_fix[name]))
        # the level race (the S-lesson census)
        over_now = sum(1 for z in z_cal.values() if z > proj["t_now"])
        cal_lift_ct = sum(
            1 for row in lg["doc_rows"]
            if row["half"] == "cal" and row["D"] is not None
            and z_cal.get(row["doc_id"]) is not None
            and max(row["D"], z_cal[row["doc_id"]]) > row["D"])
        held_lift_ct = sum(
            1 for row in lg["doc_rows"]
            if row["half"] == "held" and row["D"] is not None
            and z_held.get(row["doc_id"]) is not None
            and max(row["D"], z_held[row["doc_id"]]) > row["D"])
        top = sorted(((z, did) for did, z in z_cal.items()),
                     reverse=True)[:5]
        p("  THE LEVEL RACE (the S-lesson census): cal docs whose z ALONE "
          "exceeds the CURRENT level: %d; cal docs lifted: %d; held docs "
          "lifted: %d; top-5 cal z: %s"
          % (over_now, cal_lift_ct, held_lift_ct,
             ", ".join("%s %.4f" % (did, z) for z, did in top)))
        # the P-A1 census (the d2 zero-run mass over the clean corpus)
        mv = list(md2_cal.values())
        m_mu, m_sd = K.mean_std(mv) if len(mv) >= 2 else (None, None)
        n_zero = sum(1 for v in mv if v == 0)
        n_pos = sum(1 for v in mv if v > 0)
        hv = list(md2_held.values())
        h_pos = sum(1 for v in hv if v > 0)
        json_z = ((md2_fix.get("loop-seeded-json", 0) - m_mu) / m_sd
                  if m_mu is not None and m_sd and m_sd > 1e-12 else None)
        if m_mu is None:
            p("  THE P-A1 CENSUS (f.laneB d2 zero-run mass, support "
              "triples >= 8, runs >= 2): EMPTY (too few cal docs read) "
              "-- named, the flood question unreadable this leg")
        else:
            sd_txt = ("%.6f" % m_sd
                      if m_sd is not None and m_sd > 1e-12
                      else "EMPTY_sd_zero -- every cal doc reads m_d2 0, "
                           "the z form UNDEFINED (the corpus carries no "
                           "zero-run mass; a json flip prices only at a "
                           "fresh sheet's own law)")
            z_txt = ("%.4f" % json_z if json_z is not None
                     else "EMPTY (sd 0; the z form undefined, never "
                          "imputed)")
            p("  THE P-A1 CENSUS (f.laneB d2 zero-run mass, support "
              "triples >= 8, runs >= 2): cal mean %.6f sd %s, n_at_zero "
              "%d/%d, n_pos %d; held n_pos %d/%d; json m_d2 %d -> z %s; "
              "triples at cal zeros: min %s med %s n %d"
              % (m_mu, sd_txt, n_zero, len(mv), n_pos, h_pos, len(hv),
                 md2_fix.get("loop-seeded-json", -1), z_txt,
                 str(min(trip_at_zero)) if trip_at_zero else "None",
                 ("%.0f" % K.median_of(trip_at_zero))
                 if trip_at_zero else "None", len(trip_at_zero)))
        for gate in (8, 12, 16):
            ct = 0
            for did in sorted(f_laneB_cal):
                d2_vals, triples = f_laneB_cal[did]
                m, _ = m_d2(d2_vals, triples, gate)
                if m > 0:
                    ct += 1
            p("    sensitivity (triples >= %d): cal docs with m_d2 > 0: %d"
              % (gate, ct))
        p("")
    p("THE READ, PRESENTED NEVER ADJUDICATED: the console above answers the "
      "diagnostic's three questions per leg -- (1) does the P-B4 cal "
      "reference sit low with small sd (countdown clears) or does the clean "
      "corpus flood (the face dies on paper); (2) does the level move past "
      "mask-reserved-stubborn's read (the ITEM-487 demotion cliff); (3) "
      "does the projected gap clear the 2.0 bar on these dev bytes; the "
      "P-A1 census beside them prices the json flip's own flood question")
    p("(offline read of his pinned cache bytes only, zero GPU, zero "
      "decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no "
      "thresholds set, moved, or adjudicated; findings presented, never "
      "adjudicated -- the owner's stamps decide)")

# ---- the combined mode: the two faces under the max-spine -------------
def zmax(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a >= b else b

def combined_mode(K, r):
    p("=== THE COMBINED-SIDE DIAGNOSTIC, --combined MODE (his pinned "
      "caches, read-only, zero GPU, zero decodes) ===")
    p("the two faces under the tool's OWN max-spine conjunction: D_new = "
      "max(D, z_refined, z_d2mass) per doc, cal and held and fixtures "
      "re-scored identically -- the refined-tail cell (P-B4, the masked E "
      "tail form read EXACTLY as the item-488 ledger computed it, never "
      "tuned) and the d2 zero-run-mass cell (P-A1, the pinned S face's "
      "run law mirrored onto d2, support = triples >= the swept gate); "
      "each z against its own cal reference; the triples gate swept "
      "8/12/16 -- the sheet pins ONE at his word, never tuned to the "
      "answer")
    p("the correction on the record before the read: the item-491 "
      "optimistic bound 1.980063 UNDERSTATED the fixture side -- under "
      "the combined species the d2 cell's biggest read belongs to "
      "loop-injection-code (already detected, m_d2 21, z 15.3266), its "
      "D lifting 7.989752 -> 15.326556 and WIDENING the loop sd "
      "2.815408 -> 3.976060 -- the sd drag beats the mean lift, the "
      "honest fixture-side bound 1.606504 DOWN 0.0798 from the receipt "
      "with the k 7 -> 8 json flip live beside it (the level-fixed "
      "world)")
    p("")
    for leg in K.LEGS:
        lg = r["legs"][leg]
        cache_path = K.CACHE_FILES[leg]
        if not os.path.exists(cache_path):
            die(f"leg {leg}: cache {cache_path} not found beside this "
                f"script -- aborting.")
        sha = sha256_file(cache_path)
        if sha != K.CACHE_PINS[leg]:
            die(f"leg {leg}: cache sha256 {sha} != the pinned "
                f"{K.CACHE_PINS[leg]} -- the pin-table guard holds; "
                f"never read divergent bytes; aborting.")
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
            die(f"leg {leg}: the cache's doc population does not match "
                f"the receipt's doc_rows -- never project across "
                f"populations; aborting.")
        p("  population parity: %d cal + %d held, exact match against "
          "the receipt's doc_rows" % (len(cal_docs), len(held_docs)))
        base = K.compute_baselines(cal_docs, leg)
        f_vals = [v for d in cal_docs
                  for v in d["steps"]["f"] if v is not None]
        f_ref = K.mean_std(f_vals) if f_vals else None
        cal_E = sorted(v for d in cal_docs
                       for v in d["steps"]["E"] if v is not None)
        primary_cut = K.quantile(cal_E, K.MASK_Q_PRIMARY)

        # per-doc: the refined z + the per-gate d2 mass
        ref_cal, ref_held = {}, {}
        m_cal = {g: {} for g in D2_GATES}
        m_held = {g: {} for g in D2_GATES}
        for pop, docs, ref in (("cal", cal_docs, ref_cal),
                               ("held", held_docs, ref_held)):
            for d in docs:
                cells = K.process_doc_conjunct(d, base, f_ref, primary_cut)
                v, status = refined_tail(cells["E"]["masked"]["d"],
                                         cells["E"]["masked"]["pairs"], K)
                ref[d["doc_id"]] = v
                d2c = K.doc_d2_census(d, base, f_ref, primary_cut)
                fb = d2c["f"]["laneB"]
                tgt = m_cal if pop == "cal" else m_held
                for g in D2_GATES:
                    m, _ = m_d2(fb["d2"], fb["triples"], g)
                    tgt[g][d["doc_id"]] = m

        vals = [v for v in ref_cal.values() if v is not None]
        n_empty = sum(1 for v in ref_cal.values() if v is None)
        refined_ok = True
        if len(vals) < 2:
            p("  P-B4 cal reference: EMPTY (n %d) -- the refined face "
              "vacuous this leg, named; the d2 face rides alone" % len(vals))
            refined_ok = False
            mu_r = sd_r = None
        else:
            mu_r, sd_r = K.mean_std(vals)
            p("  P-B4 CAL REFERENCE (the refined tail over %d cal docs, "
              "%d EMPTY named): mean %.6f sd %.6f"
              % (len(vals), n_empty, mu_r, sd_r))
            if sd_r <= 1e-12:
                p("  sd == 0 -- the refined face EMPTY_degenerate_sd, "
                  "vacuous; the d2 face rides alone")
                refined_ok = False

        # fixture z's: refined + per-gate d2 mass (with the curve
        # lineage gates: the fresh curves must match the receipt's)
        zfix_ref, mfix = {}, {g: {} for g in D2_GATES}
        for name in sorted(fixture_recs):
            cells = K.process_doc_conjunct(fixture_recs[name], base, f_ref,
                                           primary_cut)
            cur = lg["fixture_curves"][name]["E"]["masked"]
            got = cells["E"]["masked"]
            for i in range(len(K.LAGS)):
                a, b = got["d"][i], cur["d"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die(f"leg {leg} fixture {name}: the fresh masked E "
                        f"curve diverges from the receipt's "
                        f"fixture_curves at lag {K.LAGS[i]} -- the "
                        f"curve lineage is not proven; aborting.")
            d2c = K.doc_d2_census(fixture_recs[name], base, f_ref,
                                  primary_cut)
            fb = d2c["f"]["laneB"]
            fcur = lg["fixture_curves"][name]["f"]["laneB"]
            for i in range(len(K.LAGS)):
                a, b = fb["d2"][i], fcur["d2"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die(f"leg {leg} fixture {name}: the fresh laneB f "
                        f"d2 curve diverges from the receipt's "
                        f"fixture_curves at lag {K.LAGS[i]} -- the d2 "
                        f"lineage is not proven; aborting.")
            v, status = refined_tail(got["d"], got["pairs"], K)
            zfix_ref[name] = ((v - mu_r) / sd_r
                              if (refined_ok and v is not None) else None)
            for g in D2_GATES:
                mfix[g][name] = m_d2(fb["d2"], fb["triples"], g)[0]

        # the fixture gate-stability table (the m values across the sweep)
        p("  fixture d2 mass across the gate sweep (the sheet pins ONE "
          "gate; the target's read named at every gate):")
        for name in sorted(fixture_recs):
            ms = [mfix[g][name] for g in D2_GATES]
            if max(ms) > 0 or name in BANKED_MD2:
                p("    %-27s m_d2 at gates 8/12/16: %s"
                  % (name, " / ".join(str(m) for m in ms)))

        # the per-doc z maps for the d2 face per gate + the combined max
        D_held = {x["doc_id"]: x["D"] for x in lg["doc_rows"]
                  if x["half"] == "held" and x["D"] is not None}
        for g in D2_GATES:
            masses = list(m_cal[g].values())
            mu_g, sd_g = K.mean_std(masses) if len(masses) >= 2 \
                else (None, None)
            if mu_g is None or sd_g <= 1e-12:
                p("  --- GATE triples >= %d: the d2 reference EMPTY (sd "
                  "0 -- every cal doc reads zero mass) -- the d2 face "
                  "vacuous at this gate, the refined face rides alone "
                  "---" % g)
                zd_cal = zd_held = zd_fix = {}
            else:
                zd_cal = {did: (m - mu_g) / sd_g
                          for did, m in m_cal[g].items()}
                zd_held = {did: (m - mu_g) / sd_g
                           for did, m in m_held[g].items()}
                zd_fix = {n: (mfix[g][n] - mu_g) / sd_g
                          for n in mfix[g]}
                n_zero = sum(1 for v in masses if v == 0)
                p("  --- GATE triples >= %d: the d2 cal reference mean "
                  "%.6f sd %.6f (n_at_zero %d/%d, n_pos %d) ---"
                  % (g, mu_g, sd_g, n_zero, len(masses),
                     len(masses) - n_zero))
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
            zc_fix = {n: zmax(zfix_ref[n], zd_fix.get(n)) for n in zfix_ref}
            proj = project(r, leg, zc_cal, zc_held, zc_fix, K)
            p("    THE COMBINED PROJECTION (can-only-add, both faces, "
              "the level re-derives, both sides re-scored identically):")
            p("      t_joint %.6f -> %.6f (%+.6f)  |  k %d -> %d"
              % (proj["t_now"], proj["t_new"],
                 proj["t_new"] - proj["t_now"],
                 proj["k_now"], proj["k_new"]))
            p("      held mean/sd %.6f/%.6f -> %.6f/%.6f  |  loop "
              "mean/sd %.6f/%.6f -> %.6f/%.6f"
              % (proj["mu_held_now"], proj["sd_held_now"],
                 proj["mu_held"], proj["sd_held"],
                 proj["mu_loop_now"], proj["sd_loop_now"],
                 proj["mu_loop"], proj["sd_loop"]))
            p("      THE GAP: %.6f -> %.6f vs the 2.0 bar (the bar read "
              "presented, never adjudicated)"
              % (lg["readouts"]["raw"]["gap"], proj["gap_new"]))
            # the cliff read: the max cal z and the mask-stub demotion
            top_cal = max(((z, did) for did, z in zc_cal.items()),
                          default=None)
            mstub = proj["fix_now"].get("mask-reserved-stubborn")
            cliff = ("mask-reserved-stubborn" in proj["demoted"])
            if top_cal is not None:
                p("      THE CLIFF READ: the top combined cal z %.6f "
                  "(doc %s) vs mask-stub's %.6f -- %s"
                  % (top_cal[0], top_cal[1], mstub,
                     "DEMOTED, the k flip eaten" if cliff
                     else "mask-stub holds"))
            # the held-side decomposition (the S-lesson census)
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
              "refined-only %d, d2-only %d, both %d"
              % (n_ref, n_d2, n_both))
            p("      fixture lifts: %s  |  demotions: %s"
              % (proj["lifted"] or "[]", proj["demoted"] or "[]"))
            for name in sorted(fixture_recs):
                zn = zc_fix.get(name)
                p("      %-27s D %.6f -> %.6f  z_combined %s"
                  % (name, proj["fix_now"][name], proj["fix_new"][name],
                     "%.4f" % zn if zn is not None else "None"))
            p("")
    p("THE READ, PRESENTED NEVER ADJUDICATED: the console above prices "
      "the combined sheet per leg per gate -- the honest gap with both "
      "sides re-scored, the level move and the mask-stub demotion "
      "cliff, the k flip, and the gate sweep the sheet pins ONE of at "
      "his word; the 3B dev bytes are the paper read -- the 8B record "
      "lane re-derives every reference on its own bytes")
    p("(offline read of his pinned cache bytes only, zero GPU, zero "
      "decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); "
      "no thresholds set, moved, or adjudicated; findings presented, "
      "never adjudicated -- the owner's stamps decide)")

def main():
    args = sys.argv[1:]
    K = load_tool()
    r = load_receipt()
    if "--parity-only" in args:
        parity_only(K, r)
    elif "--combined" in args:
        combined_mode(K, r)
    else:
        full_mode(K, r)
    with open(CONSOLE_NAME, "w") as f:
        f.write("\n".join(OUT) + "\n")
    print("")
    print("WROTE " + CONSOLE_NAME)

if __name__ == "__main__":
    main()

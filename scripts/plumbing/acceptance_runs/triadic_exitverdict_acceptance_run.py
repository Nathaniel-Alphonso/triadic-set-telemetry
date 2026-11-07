#!/usr/bin/env python3
# triadic_exitverdict_acceptance_run.py — the exit-verdict annotator's acceptance run driver.
# Version 1.0.1 (the margins-join acceptance; ledger item 187, my stamped build).  Executes
# the item-182-stamped acceptance design + the item-187 typed band bindings: the annotator
# replays over the four lane families' banked exports + the item-186 band-input lane; the
# HAND-AUTHORED fixtures (written BEFORE this run) must match the instrument's outputs exactly
# (grade/lockout/gaps/flags everywhere; band margin_source/in_band_fraction/decisive_margin/
# annotations on the margins-join rows); determinism (two runs byte-identical) and no-touch
# input receipts are checked.  Fixtures were authored first: fix-the-fixture-or-the-builder,
# NEVER the instrument's inputs or the banked records.  θ [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-θ).

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triadic_exitverdict_annotator as ev

INPUT_FILES = [
    "triadic_code17c_offline_pass_v1_per_doc.jsonl",
    "triadic_prose17p_offline_pass_v1_per_doc.jsonl",
    "triadic_p2corpus_offline_pass_v1_per_doc.jsonl",
    "gate17a_acceptance_run_v1.json",
    "triadic_generations_p2corpus_raw_v1.json",
    "triadic_generations_p2corpus_chat_v1.json",
    "t2margins_t2-gsm-full_thin.jsonl",
    "t2margins_t2-gsm-chat100-a1_thin.jsonl",
]
FIXTURES = "exitverdict_acceptance_fixtures_v2.json"
EXPORT = "triadic_exitverdict_annotator_run_v101.json"
CONSOLE = "triadic_exitverdict_acceptance_console_v101.txt"


def main(kdir, outdir):
    L = []
    def say(s=""):
        L.append(s)

    say("EXIT-VERDICT ANNOTATOR v1.0.1 — THE MARGINS-JOIN ACCEPTANCE RUN OF RECORD (items 182/186/187)")
    say("Instrument: {} v{}  (offline posture annotator; zero model contact; additive-only)".format(
        ev.INSTRUMENT_NAME, ev.INSTRUMENT_VERSION))
    say()

    # -- integrity receipts BEFORE --
    say("[1] INPUT RECEIPTS (SHA-256, before the run)")
    before = {}
    for name in INPUT_FILES:
        before[name] = ev.sha256_file(os.path.join(kdir, name))
        say("    {}  {}".format(before[name][:16] + "..." + before[name][-8:], name))
    fixture_path = os.path.join(kdir, FIXTURES)
    before[FIXTURES] = ev.sha256_file(fixture_path)
    say()

    # -- the annotation, twice (determinism) --
    say("[2] THE ANNOTATION — run twice for determinism")
    e1 = ev.annotate(kdir)
    e2 = ev.annotate(kdir)
    b1 = json.dumps(e1, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    b2 = json.dumps(e2, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    determinism = (b1 == b2)
    say("    run-1 bytes: {}   run-2 bytes: {}   BYTE-IDENTICAL: {}".format(len(b1), len(b2), determinism))
    say()

    # -- the export of record --
    export_path = os.path.join(outdir, EXPORT)
    with open(export_path, "w", encoding="utf-8") as f:
        f.write(b1)
    export_sha = ev.sha256_file(export_path)
    say("[3] EXPORT OF RECORD: {}  {} bytes  SHA-256 {}".format(EXPORT, len(b1.encode("utf-8")), export_sha))
    say()

    # -- the fixtures --
    say("[4] THE HAND-AUTHORED FIXTURES ({}; authored BEFORE the run; fix-the-fixture-or-the-builder)".format(FIXTURES))
    with open(fixture_path, "r", encoding="utf-8") as f:
        fixtures = json.load(f)["fixtures"]
    index = {}
    for w in e1["walks"]:
        index[(w["lane"], w["walk"])] = w
    passed, failed, results = 0, 0, []
    for fx in fixtures:
        got = index.get((fx["lane"], fx["walk"]))
        if got is None:
            failed += 1
            results.append((fx, None, "WALK-NOT-FOUND"))
            continue
        exp = fx["expect"]
        diffs = []
        if got["grade"] != exp["grade"]:
            diffs.append("grade {} != {}".format(got["grade"], exp["grade"]))
        if got["lockout"] != exp["lockout"]:
            diffs.append("lockout {} != {}".format(got["lockout"], exp["lockout"]))
        if got["gaps"] != sorted(exp["gaps"]):
            diffs.append("gaps {} != {}".format(got["gaps"], sorted(exp["gaps"])))
        if got["flags"] != exp["flags"]:
            diffs.append("flags {} != {}".format(got["flags"], exp["flags"]))
        # the v1.0.1 band block (compared only where the authored expectation carries it)
        band_exp = exp.get("band")
        if band_exp is not None:
            bf = got.get("band_features") or {}
            if bf.get("margin_source") != band_exp.get("margin_source"):
                diffs.append("margin_source {} != {}".format(
                    bf.get("margin_source"), band_exp.get("margin_source")))
            for k in ("in_band_fraction", "decisive_margin"):
                if k in band_exp:
                    gv = bf.get(k)
                    if gv is None or round(float(gv), 6) != band_exp[k]:
                        diffs.append("{} {} != {}".format(k, gv, band_exp[k]))
            got_ann = sorted([[a["flag_class"], a["band_member"], a["conf_rule"]]
                              for a in (got.get("annotations") or [])])
            exp_ann = sorted(band_exp.get("annotations", []))
            if got_ann != exp_ann:
                diffs.append("annotations {} != {}".format(got_ann, exp_ann))
        if diffs:
            failed += 1
            results.append((fx, got, "; ".join(diffs)))
        else:
            passed += 1
            results.append((fx, got, None))
    for fx, got, err in results:
        if err is None:
            say("    PASS  {}  {}  grade={} lockout={}".format(fx["lane"], fx["walk"], fx["expect"]["grade"], fx["expect"]["lockout"]))
        else:
            say("    FAIL  {}  {}  {}".format(fx["lane"], fx["walk"], err))
    say("    FIXTURES: {}/{} MATCH EXPECTED".format(passed, len(fixtures)))
    say()

    # -- the run census --
    say("[5] RUN CENSUS (every walk consumed exactly once; full feature record per D-S2(a))")
    for lane in sorted(e1["lane_census"]):
        say("    {:<14} {:>5} walks".format(lane, e1["lane_census"][lane]))
    total = sum(e1["lane_census"].values())
    say("    TOTAL {:,} walks".format(total))
    bj = e1.get("band_join_census", {})
    say("    band-join census: margins records loaded {}  |  17-A joined {}  |  chat-leg banked-unjoined {}".format(
        bj.get("margins_records_loaded"), bj.get("17A-RUNTIME_joined"), bj.get("chat_leg_records_banked_unjoined")))
    for grade in sorted(e1["grade_census"]):
        say("    grade {:<22} {:>6}".format(grade, e1["grade_census"][grade]))
    for gap in sorted(e1["gap_census"]):
        say("    gap   {:<32} {:>4}".format(gap, e1["gap_census"][gap]))
    say()

    # -- honest notes --
    say("[6] HONEST NOTES (stated, never smoothed)")
    say("    - v1.0.1 THE MARGINS-JOIN (item-187): the band is LIVE on the 17-A lane — the item-186")
    say("      thin-margin records join 1,319/1,319 walks; the typed confidence rule's upgrade path")
    say("      is now exercised (PASS-OUT-OF-BAND upgrades; FAIL-IN-BAND stands). The decisive read")
    say("      binding is walk-level (last ANSWER-phase commitment gap, else last commitment gap)")
    say("      because the 17-A fire records carry no step indices — typed as such, never guessed.")
    say("    - Every lane EXCEPT 17-A remains INPUT-MISSING: no margins exist for those corpora")
    say("      (the E'/E\"/T2-P2 corpora were never walked under telemetry; the chat-leg margins")
    say("      are banked input with ZERO current lane joins — censused, not fabricated). The")
    say("      zero-commitment class is typed in the instrument with zero members on the joining")
    say("      lane (the single zero-commit record is a loop fixture, not a 17-A walk).")
    say("    - Gap classes typed in the instrument but with ZERO members on the natural corpora:")
    say("      the UNVERIFIED fails-open class (the natural code corpus was 164/164 RUNNABLE) and")
    say("      the STATED-ANSWER-CONTRADICTION class (zero prose flags in the natural corpus).")
    say("      Their engineered ground is the three closed fixture families; this replay is")
    say("      natural corpora only — the census records the zeros honestly.")
    say("    - CONTROL-FIRING rows (the P2 control axis, censused separately per M2-P2) and")
    say("      SILENCE/BLANK-ANSWER rows (the honest-absence class) are census-only: no flag,")
    say("      no gap — a control firing or a silence is not a fault and not an unverifiable claim.")
    say("    - 17-A has no gap classes: a slip is a VERIFIED fault (deterministic math), never")
    say("      an unverifiable claim.")
    say()

    # -- no-touch receipts AFTER --
    say("[7] NO-TOUCH RECEIPTS (SHA-256, after the run)")
    untouched = True
    for name in INPUT_FILES + [FIXTURES]:
        after = ev.sha256_file(os.path.join(kdir, name))
        same = after == before[name]
        untouched = untouched and same
        say("    {}  {}  {}".format(after[:16] + "..." + after[-8:], name, "UNCHANGED" if same else "CHANGED"))
    say()

    say("[8] VERDICT")
    v_runs_clean = (failed == 0)
    say("    R-EV1 runs-clean (all fixtures match expected):      {}".format("PASS" if v_runs_clean else "FAIL"))
    say("    R-EV2 determinism (two runs byte-identical):         {}".format("PASS" if determinism else "FAIL"))
    say("    R-EV3 no-touch (every input byte-unchanged):         {}".format("PASS" if untouched else "FAIL"))
    all_pass = v_runs_clean and determinism and untouched
    say("    ACCEPTANCE: {}".format("ALL THREE PASS — the readings await my stamps" if all_pass else "FAIL — adjudicate for cause"))
    say("    θ [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-θ); no thresholds set, moved, or adjudicated; the band is a")
    say("    banked cited census number; findings presented, never adjudicated.")

    console_path = os.path.join(outdir, CONSOLE)
    with open(console_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    return 0 if all_pass else 1


if __name__ == "__main__":
    kdir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    outdir = sys.argv[2] if len(sys.argv) > 2 else kdir
    sys.exit(main(kdir, outdir))

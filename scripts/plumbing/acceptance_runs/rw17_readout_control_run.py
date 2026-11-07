#!/usr/bin/env python3
"""rw17_readout_control_run.py -- THE REAL-CACHE CONTROL for
triadic_rw17_readout.py (the RW-17 readout tool amendment's control of
record; the item-242 / rw16-control precedent, ledger item 255).

THE CONTROL INPUTS (banked bytes, SHA-pinned below):
  - the three REAL smoke caches received from the Triadic library
    (the RW-17 fresh-corpus smoke walks: math/code/prose, 20 corpus
    docs + the 10 instrument loop fixtures each; the library's own
    smoke-cache bytes, banked here for the control of record) -- the
    fixture-identity receipt crosses the three REAL caches;
  - ONE synthetic p2corpus-rw17 filler (40 thin-style docs, ids
    7000-7039, the same corpus-band construction math as the
    acceptance worlds' p2 leg: pr_lo 2.00 / s_lo 0.50 / salt 44, two
    deep-PR hot even docs, NO loop fixtures) -- the honest
    INCONCLUSIVE-POPULATION-GUARD null leg (n_pos = 0). NO real p2
    smoke cache was uploaded to the library -- an OPEN RECEIPT named
    here and in the ledger: the p2 leg's real-bytes control rides the
    OWNER-SIDE single adjudication command on the four full caches of
    record (the SS4 pins enforce the real bytes there).

THE RECEIPTS THIS CONTROL PINS:
  (a) the tool's CLI runs clean (--fixture-mode; the pins ECHO, never
      enforce) on the three real smoke caches + the filler;
  (b) EVERY exported quantity is EXACT against the INDEPENDENT
      recompute engine banked in rw17_readout_acceptance_run.py (that
      engine's own arithmetic, never the tool's functions; it was
      itself validated 90/90 against the tool in the acceptance run
      of record -- the same independence law, engine vs tool, never
      tool vs tool);
  (c) the real-bytes readings of record, named check by check: the
      gsm smoke leg's held-out half fires 3/10 > ceil 1 -- the
      FALSIFIER's teeth on REAL bytes (a smoke negative population
      kills honestly; presented, never adjudicated); the mbpp smoke
      leg PASSES the bar (gap 2.2663, AUC 0.9625, 7/8 catches); the
      prose smoke leg kills (fires 3/10 despite gap 3.0398 / AUC 1.0
      -- the count form governs over the bar); the filler leg guards
      honestly (n_pos = 0);
  (d) the census-pin ECHO receipts: the smoke corpora carry ZERO
      EOS@step0 docs vs the item-254 expected pins 1/3/95 (mbpp,
      prose, p2 -- three loud echo lines; the math leg's 0 == the pin
      0, no echo) -- the smokes are NOT the caches of record, exactly
      as received;
  (e) the fixture-identity receipt: the 10 loop fixtures byte-
      identical across the three real caches;
  (f) determinism: the same-path re-run is byte-identical on BOTH
      the export and the console.

Zero-GPU, read-only, no label joins. Fix-the-fixture-or-the-builder,
never the tool's record. theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); findings
presented, never adjudicated -- the owner's stamps decide.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rw17_readout_acceptance_run as ACC   # noqa: E402 -- the banked
# independent recompute engine (validated 90/90 in the acceptance run
# of record; the control inherits the same engine-vs-tool law)

TOOL = ACC.TOOL
FIXDIR = os.path.join(HERE, "rw17_readout_control_fixtures")
SMOKE_MATH = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-math-smoke_bfloat16_bos.jsonl")
SMOKE_CODE = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-code-smoke_bfloat16_bos.jsonl")
SMOKE_PROSE = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-prose-smoke_bfloat16_bos.jsonl")
P2_FILLER = os.path.join(
    FIXDIR, "triadic_t2_cache_rw17-p2-synth-filler.jsonl")
PIN_SHA = {
    SMOKE_MATH: ("92462c580e02b578020b670e50300b31156a0704c339f9fdda"
                 "05488e2bb4b215"),
    SMOKE_CODE: ("001445a1d81cfa7fababf021be7df100fa33e06045fb2f811c"
                 "c2b0f259edc0b0"),
    SMOKE_PROSE: ("7f99ff8421cdb55cf96421c14749f280f96360811d6b5def6"
                  "fa5f0d6e47b870d"),
    P2_FILLER: ("d14a01652c513e385439d892eca51ecc1630677b0bec1922d61"
                "7defaf763be91"),
}
CACHES = [SMOKE_MATH, SMOKE_CODE, SMOKE_PROSE, P2_FILLER]
TAG = "rw17-readout-control"
RUNDIR = os.path.join(HERE, ".scratch", "rw17_readout_control_run")
OUT = os.path.join(RUNDIR, "rw17_readout_control_export.json")

# the real-bytes readings of record (this control's own deterministic
# measurements; round4 where named, exact where compared)
READINGS = {
    "gsmrw17": {"fires": 3, "n": 10, "gap4": 1.6671, "auc4": 0.8125,
                "catches": 8, "n_live": 8,
                "typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"},
    "mbpprw17": {"fires": 0, "n": 10, "gap4": 2.2663, "auc4": 0.9625,
                 "catches": 7, "n_live": 8, "typing": "PASS_2SIGMA"},
    "prose17p-rw17": {"fires": 3, "n": 10, "gap4": 3.0398,
                      "auc4": 1.0, "catches": 8, "n_live": 8,
                      "typing": "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"},
    "p2corpus-rw17": {"fires": 0, "n": 20, "catches": 0, "n_live": 0,
                      "gap": None, "auc": None,
                      "typing": "INCONCLUSIVE-POPULATION-GUARD"},
}

CHECKS = []


def check(fam, name, ok, detail=""):
    ok = bool(ok)
    CHECKS.append((fam, name, ok, detail))
    print(f"  [{fam}] {'PASS' if ok else 'FAIL'} -- {name}"
          + (f"  [{detail}]" if (detail and not ok) else ""))
    return ok


def run_tool(out):
    cmd = [sys.executable, TOOL, "--fixture-mode"]
    for c in CACHES:
        cmd += ["--cache", c]
    cmd += ["--tag", TAG, "--out", out]
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    print("=" * 78)
    print("=== THE RW-17 READOUT TOOL CONTROL RUN (real smoke bytes; "
          "the item-242 precedent) ===")
    print("  tool under test: triadic_rw17_readout.py")
    print("  real bytes: the three library smoke caches "
          "(math/code/prose)")
    print("  + one synthetic p2corpus-rw17 filler (no real p2 smoke "
          "uploaded --")
    print("    an OPEN RECEIPT; the p2 leg's real control rides the "
          "owner-side")
    print("    single adjudication command on the full caches of "
          "record).")
    print("  LAW: every exported quantity EXACT vs the banked "
          "independent")
    print("  recompute engine (the acceptance run's own arithmetic, "
          "90/90);")
    print("  fix-the-fixture-or-the-builder, never the tool's record.")

    # (0) the banked fixture SHAs
    for path, sha in PIN_SHA.items():
        check("C0", f"the banked control input "
              f"{os.path.basename(path)} carries its pinned SHA-256",
              ACC.r_sha256_file(path) == sha, ACC.r_sha256_file(path))

    if os.path.exists(RUNDIR):
        shutil.rmtree(RUNDIR)
    os.makedirs(RUNDIR)

    # (a) the tool runs clean on the real bytes
    p1 = run_tool(OUT)
    if not check("C1", "the tool CLI runs clean on the three REAL "
                 "smoke caches + the filler (fixture mode, pins "
                 "echoed never enforced)",
                 p1.returncode == 0, p1.stderr[-400:]):
        return finish()
    console1 = p1.stdout
    with open(OUT) as f:
        got = json.load(f)

    # (b) EVERY exported quantity EXACT vs the independent recompute
    exp = ACC.full_exp(CACHES, TAG)
    errs = []
    ACC.cmp_tree(exp, got, "", errs)
    check("C2", "the export == the independent recompute EXACT on "
          "the REAL bytes (every field, every leg, every doc, "
          "order-exact)", not errs,
          f"{len(errs)} diff(s): " + "; ".join(errs[:5]))

    # (c) the real-bytes readings of record
    for leg, rd in READINGS.items():
        lb = got["legs"][leg]
        fam = "C3"
        gap = lb["separation_context"]["sigma_gap_on_D"]
        auc = lb["separation_context"]["auc_on_D"]
        ok = (lb["held_out"]["fires"] == rd["fires"]
              and lb["held_out"]["n"] == rd["n"]
              and lb["loop_catches"]["at_t_leg"] == rd["catches"]
              and lb["loop_catches"]["n_live"] == rd["n_live"]
              and lb["verdict"]["typing_presented"] == rd["typing"])
        if "gap4" in rd:
            ok = ok and gap is not None and round(gap, 4) == rd["gap4"]
            ok = ok and auc is not None and round(auc, 4) == rd["auc4"]
        else:
            ok = ok and gap is None and auc is None
        check(fam, f"leg {leg} reading of record: fires "
              f"{rd['fires']}/{rd['n']}, catches {rd['catches']}/"
              f"{rd['n_live']}, gap "
              f"{rd.get('gap4', 'None')}, AUC {rd.get('auc4', 'None')}"
              f" -> {rd['typing']}", ok,
              f"measured fires {lb['held_out']['fires']}, gap {gap}, "
              f"auc {auc}, typing "
              f"{lb['verdict']['typing_presented']}")
    check("C3", "the candidate-level reading: KILLED by the "
          "falsifier on the two over-budget real legs "
          "[gsmrw17, prose17p-rw17] with the filler's honest guard "
          "[p2corpus-rw17] riding -- the count form governs over the "
          "bar on real bytes",
          got["presented_candidate_verdict"]["verdict_presented"]
          == "CANDIDATE-KILLED-FALSE-ALARM-BUDGET"
          and got["presented_candidate_verdict"]["over_budget_legs"]
          == ["gsmrw17", "prose17p-rw17"]
          and got["presented_candidate_verdict"]
          ["population_guard_legs"] == ["p2corpus-rw17"])

    # the real legs' populations + parity receipts
    for leg in ("gsmrw17", "mbpprw17", "prose17p-rw17"):
        lb = got["legs"][leg]
        check("C4", f"leg {leg}: parity 10/10 (EVEN calibration / "
              f"ODD held-out on the real smoke corpus) and 8 live / "
              f"2 inert positives (the two sub-32 fixtures)",
              lb["parity"]["n_even_calibration"] == 10
              and lb["parity"]["n_odd_held_out"] == 10
              and lb["loop_population"]["n_live"] == 8
              and lb["loop_population"]["n_inert"] == 2
              and lb["loop_population"]["inert"]
              == ["loop-seeded-affirm", "loop-seeded-chant"])
    check("C4", "the filler leg: parity 20/20, ZERO positives -> the "
          "honest INCONCLUSIVE-POPULATION-GUARD null leg",
          got["legs"]["p2corpus-rw17"]["parity"]
          ["n_even_calibration"] == 20
          and got["legs"]["p2corpus-rw17"]["parity"]
          ["n_odd_held_out"] == 20
          and got["legs"]["p2corpus-rw17"]["loop_population"]["n_live"]
          == 0)

    # (d) the census-pin ECHO receipts (the smokes are not the caches
    # of record -- exactly as received)
    n_echo = console1.count("CENSUS PIN ECHO")
    echo_ok = n_echo == 3
    for leg, pin in (("mbpprw17", 1), ("prose17p-rw17", 3),
                     ("p2corpus-rw17", 95)):
        echo_ok = echo_ok and f"leg {leg}" in console1 \
            and f"measured fresh census is 0 EOS@step0 doc(s) != the " \
                f"item-254 expected census of record {pin}" in console1
    check("C5", "the census-pin ECHO receipts: the smoke corpora "
          "carry ZERO EOS@step0 docs vs the expected pins -- three "
          "loud echo lines (mbpp 1, prose 3, p2 95); the math leg's "
          "0 == its pin 0, no echo; echoed in fixture mode, NEVER "
          "silently pooled", echo_ok, f"{n_echo} echo line(s)")
    check("C5", "the math leg's census receipt: measured 0 == the "
          "item-254 pin 0 (no echo, receipts empty)",
          got["legs"]["gsmrw17"]["census"]["measured_eos_step0"] == 0
          and got["legs"]["gsmrw17"]["census"]["receipts"] == [])

    # (e) the fixture-identity receipt across the three real caches
    fir = got["fixture_identity_receipt"]
    check("C6", "the fixture-identity receipt: the 10 loop fixtures "
          "byte-identical across the three REAL smoke caches (the "
          "instrument's own fixture copies, as received)",
          fir["n_loop_fixtures"] == 10
          and fir["copies_byte_identical"] is True)

    # (f) determinism
    with open(OUT, "rb") as f:
        first_bytes = f.read()
    p2run = run_tool(OUT)
    with open(OUT, "rb") as f:
        second_bytes = f.read()
    check("C7", "determinism: the same-path re-run export is "
          "byte-identical AND the console output byte-identical "
          "across the two runs",
          p2run.returncode == 0 and first_bytes == second_bytes
          and len(first_bytes) > 0 and console1 == p2run.stdout)
    return finish()


def finish():
    print("\n" + "=" * 78)
    n_fail = sum(1 for c in CHECKS if not c[2])
    fams = []
    for fam, _n, _ok, _d in CHECKS:
        if fam not in fams:
            fams.append(fam)
    for fam in fams:
        ft = sum(1 for c in CHECKS if c[0] == fam)
        fp = sum(1 for c in CHECKS if c[0] == fam and c[2])
        print(f"  {fam}: {fp}/{ft} PASS")
    print(f"\n  TOTAL: {len(CHECKS) - n_fail}/{len(CHECKS)} PASS, "
          f"{n_fail} FAIL")
    if n_fail:
        print("\n  FAILURES (named, never silent):")
        for fam, name, ok, detail in CHECKS:
            if not ok:
                print(f"   [{fam}] {name}"
                      + (f" -- {detail}" if detail else ""))
    print("\n  Fix-the-fixture-or-the-builder, never the tool's "
          "record.")
    print("  theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); findings presented, "
          "never")
    print("  adjudicated -- the owner's stamps decide.")
    sys.exit(0 if n_fail == 0 else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""build_arith_fixtures.py — the arith-* fixture-suite builder (v1).

Deterministic (fixed parameter tables, zero randomness, zero model).
Implements my STAMPED arith-* fixture-family pre-registration
(arith-fixture-family-preregistration.md; ruled options: sizing arith-M,
RW-5 paraphrase axis OFF — ledger items 161-162).

Ground truth and expected-verdict assertions use the banked v2 core
functions (tokenize_expr / evaluate / parse_num) imported from the
17-A runtime instrument of record — the oracle is the fixture.
"""
import json
import hashlib
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from triadic_gate17a_runtime import tokenize_expr, evaluate, parse_num


def fires(lhs, stated):
    """The banked F2 decision on one statement (as-is convention)."""
    nums, ops = tokenize_expr(lhs)
    st, sd, _ = parse_num(stated)
    exacts = evaluate(nums, ops)
    tol = Fraction(1, 10 ** sd * 2) + Fraction(1, 10 ** 9)
    beyond = all(abs(x - st) > tol for x in exacts)
    return beyond, exacts, tol, sd


def sfrac(stated):
    st, _sd, _ = parse_num(stated)
    return st


ROWS = []


def add(cls, magnitude, family, text, expected_verdict, *, slips=0,
        lhs=None, stated=None, guard=None, evclass=None, exemplar="",
        pending=None, note=""):
    rid = "arith-%s-%03d" % (cls, len([r for r in ROWS if r["class"] == cls]) + 1)
    gt = None
    if lhs is not None and stated is not None:
        beyond, exacts, tol, sd = fires(lhs, stated)
        gt = {
            "target_lhs": lhs,
            "target_stated": stated,
            "stated_value": str(sfrac(stated)),
            "true_values": [str(x) for x in exacts],
            "epsilon_as_is": str(tol),
            "stated_decimals": sd,
            "beyond_epsilon_as_is": beyond,
        }
    ROWS.append({
        "fixture_id": rid,
        "class": cls,
        "magnitude": magnitude,          # loud / subtle / null (controls)
        "anchor_family": family,         # inline / scratchpad
        "statement_text": text,
        "ground_truth": gt,
        "expected_verdict": expected_verdict,
        "expected_slips": slips,
        "expected_guard": guard,
        "expected_event_class": evclass,
        "habit_exemplar": exemplar,
        "pending_ruling": pending,
        "class_note": note,
    })


# ---------------- P1 — late-chain position slip (8: 4 loud, 4 subtle) ----------------
P1 = [  # (a, b, c, d, e, stated_final) — true final = a+b+c+d+e
    (240, 180, 90, 60, 50, 675),      # true 620, loud
    (1200, 340, 150, 75, 300, 2100),  # true 2065, loud
    (240, 180, 90, 60, 50, 625),      # true 620, subtle
    (450, 380, 220, 140, 90, 1284),   # true 1280, subtle
    (450, 380, 220, 140, 90, 1600),   # true 1280, loud
    (96, 88, 64, 52, 40, 500),        # true 340, loud
    (96, 88, 64, 52, 40, 343),        # true 340, subtle
    (1200, 340, 150, 75, 300, 2070),  # true 2065, subtle
]
for i, (a, b, c, d, e, st) in enumerate(P1):
    mag = "loud" if st in (675, 2100, 1600, 500) else "subtle"
    fam = "inline" if i < 4 else "scratchpad"
    s1, s2, s3, s4 = a + b, a + b + c, a + b + c + d, a + b + c + d + e
    if fam == "inline":
        text = ("The build has four stages. Stage one: %d + %d = %d. "
                "Stage two: %d + %d = %d. Stage three: %d + %d = %d. "
                "Stage four: %d + %d = %d." % (a, b, s1, s1, c, s2, s2, d, s3, s3, e, st))
    else:
        text = ("The build has four stages. Stage one: <<%d + %d = %d>> "
                "Stage two: <<%d + %d = %d>> Stage three: <<%d + %d = %d>> "
                "Stage four: <<%d + %d = %d>>" % (a, b, s1, s1, c, s2, s2, d, s3, s3, e, st))
    add("P1", mag, fam, text, "SLIP-FLAG", slips=1,
        lhs="%d + %d" % (s3, e), stated=str(st),
        exemplar="the banked late-skew census (raw 198/67, chat 17/2; doc-11 family)")

# ---------------- P2 — multi-slip cascade (8) ----------------
P2 = [  # (m, n, seeded, p, q) — true seed = m*n
    (36, 68, 2460, 120, 300),   # true 2448, loud
    (150, 44, 6660, 80, 160),   # true 6600, loud
    (36, 68, 2449, 120, 300),   # subtle
    (150, 44, 6602, 80, 160),   # subtle
    (52, 77, 4034, 90, 210),    # true 4004, loud
    (310, 25, 8000, 140, 90),   # true 7750, loud
    (52, 77, 4007, 90, 210),    # subtle
    (310, 25, 7751, 140, 90),   # subtle
]
for i, (m, n, seeded, p, q) in enumerate(P2):
    mag = "loud" if seeded in (2460, 6660, 4034, 8000) else "subtle"
    fam = "inline" if i < 4 else "scratchpad"
    mid, fin = seeded + p, seeded + p + q
    if fam == "inline":
        text = ("First the batch: %d x %d = %d. Then the additions: %d + %d = %d. "
                "The total: %d + %d = %d."
                % (m, n, seeded, seeded, p, mid, mid, q, fin))
    else:
        text = ("First the batch: <<%d x %d = %d>> Then the additions: "
                "<<%d + %d = %d>> The total: <<%d + %d = %d>>."
                % (m, n, seeded, seeded, p, mid, mid, q, fin))
    add("P2", mag, fam, text, "SLIP-FLAG", slips=1,
        lhs="%d x %d" % (m, n), stated=str(seeded),
        exemplar="doc 11 (36 x 68 = 2460; the seeding slip carries to the total)")

# ---------------- P3 — sign slip (8) ----------------
P3 = [
    (20, 22, "2", "loud"), (75, 90, "15", "loud"),
    (12.8, 12.5, "0.8", "subtle"), (44.6, 44.1, "0.9", "subtle"),
    (140, 175, "35", "loud"), (500, 650, "150", "loud"),
    (9.15, 8.95, "0.4", "subtle"), (30.25, 29.75, "0.7", "subtle"),
]
for i, (a, b, st, mag) in enumerate(P3):
    fam = "inline" if i < 4 else "scratchpad"
    if fam == "inline":
        text = "The ledger line reads %s - %s = %s." % (a, b, st)
    else:
        text = "The ledger line: <<%s - %s = %s>> recorded." % (a, b, st)
    add("P3", mag, fam, text, "SLIP-FLAG", slips=1,
        lhs="%s - %s" % (a, b), stated=st, exemplar="doc 507 (20 - 22 = 2)")

# ---------------- P4 — the x1.1 cascade (8) ----------------
P4 = [  # (a, a1, s2, s3) — true s2 = a1*1.1; s3 = s2*1.1 (internally true)
    (450, 495, "540", "594"),        # true s2 544.5, loud
    (800, 880, "950", "1045"),       # true s2 968, loud
    (450, 495, "544.9", "599.39"),   # subtle
    (620, 682, "750.6", "825.66"),   # subtle
    (620, 682, "730", "803"),        # true s2 750.2, loud
    (940, 1034, "1120", "1232"),     # true s2 1137.4, loud
    (940, 1034, "1137.9", "1251.69"),  # subtle
    (800, 880, "968.5", "1065.35"),   # subtle
]
for i, (a, a1, s2, s3) in enumerate(P4):
    mag = "loud" if s2 in ("540", "950", "730", "1120") else "subtle"
    fam = "inline" if i < 4 else "scratchpad"
    if fam == "inline":
        text = ("The fee compounds each year. Year one: %d x 1.1 = %d. "
                "Year two: %d x 1.1 = %s. Year three: %s x 1.1 = %s."
                % (a, a1, a1, s2, s2, s3))
    else:
        text = ("The fee compounds each year. Year one: <<%d x 1.1 = %d>> "
                "Year two: <<%d x 1.1 = %s>> Year three: <<%s x 1.1 = %s>>."
                % (a, a1, a1, s2, s2, s3))
    add("P4", mag, fam, text, "SLIP-FLAG", slips=1,
        lhs="%d x 1.1" % a1, stated=s2,
        exemplar="chat doc 87 (the three-step x1.1 cascade)")

# ---------------- P5 — round-trip slip (8) ----------------
P5 = [  # (rate, m, out, rt) — true out = rate*m; rt = out/m (internally consistent)
    (0.2607, 220, "50", "0.227"),     # true 57.354, loud
    (0.75, 320, "200", "0.625"),      # true 240, loud
    (0.2607, 220, "57.0", "0.259"),   # subtle
    (0.75, 320, "239.5", "0.748"),    # subtle
    (0.043, 500, "18", "0.036"),      # true 21.5, loud
    (0.525, 800, "360", "0.45"),      # true 420, loud
    (0.043, 500, "21.2", "0.0424"),   # subtle
    (0.525, 800, "419.6", "0.5245"),  # subtle
]
for i, (r, m, out, rt) in enumerate(P5):
    mag = "loud" if out in ("50", "200", "18", "360") else "subtle"
    fam = "inline" if i < 4 else "scratchpad"
    if fam == "inline":
        text = ("The exchange rate is %s. Outbound: %s x %d = %s. "
                "Return leg: %s / %d = %s." % (r, r, m, out, out, m, rt))
    else:
        text = ("The exchange rate is %s. Outbound: <<%s x %d = %s>> "
                "Return leg: <<%s / %d = %s>>." % (r, r, m, out, out, m, rt))
    add("P5", mag, fam, text, "SLIP-FLAG", slips=1,
        lhs="%s x %d" % (r, m), stated=out,
        exemplar="chat doc 46 (0.2607 x 220 = 57.354 stated 57.0)")

# ---------------- P6 — verified impossibility, the RW-12 axis (8) ----------------
P6 = [  # (a, b, first, second) — true = a+b; second contradicts the first
    (120, 130, 250, 240),    # loud
    (450, 380, 830, 800),    # loud
    (120, 130, 250, 251),    # subtle (err 1 > epsilon(0)=0.5)
    (96, 88, 184, 185),      # subtle
    (96, 88, 184, 200),      # loud
    (1200, 340, 1540, 1500),  # loud
    (450, 380, 830, 831),    # subtle
    (1200, 340, 1540, 1541),  # subtle
]
for i, (a, b, first, second) in enumerate(P6):
    mag = "loud" if abs(first - second) > 1 else "subtle"
    fam = "inline" if i < 4 else "scratchpad"
    if fam == "inline":
        text = ("The warehouse counts the north row: %d + %d = %d units. "
                "The audit restates the north row: %d + %d = %d units."
                % (a, b, first, a, b, second))
    else:
        text = ("The warehouse counts the north row: <<%d + %d = %d>> units. "
                "The audit restates the north row: <<%d + %d = %d>> units."
                % (a, b, first, a, b, second))
    add("P6", mag, fam, text, "SLIP-FLAG", slips=1,
        lhs="%d + %d" % (a, b), stated=str(second),
        exemplar="the RW-12 verified-impossibility axis (T4 reconciliation, items 104/124)",
        note="the same lhs stated twice; the contradicting restatement must flag")

# ---------------- N1 — word-separated fragment, doc-38 shape (6, inline-only) ----------------
N1 = [(3, "hours", "1.5", "He runs"), (5, "pages", "2.5", "She reads"),
      (8, "meters", "4", "The cable spans"),
      (12, "seats", "6", "The van holds"),
      (20, "liters", "10", "The tank stores"),
      (40, "minutes", "20", "The tape runs")]
for a, unit, r, verb in N1:
    text = "%s %d %s * 1/2 = %s %s." % (verb, a, unit, r, unit)
    add("N1", None, "inline", text, "UNVERIFIED", lhs="1/2", stated=r,
        guard="G1-fragment", evclass="fragment",
        exemplar="chat doc 38 (3 hours * 1/2 = 1.5 — the natural false-fire of record)",
        note="true statement; G1 must suppress the fragment fire")

# ---------------- N2 — word-separated mirror, doc-3 shape (6, inline-only) ----------------
N2 = [(3, "sprints", "times a week", 9, "She does"),
      (4, "laps", "sessions", 20, "He swims"),
      (6, "drums", "beats", 24, "The band plays"),
      (7, "rows", "plants", 56, "The garden has"),
      (5, "shelves", "books", 45, "The case holds"),
      (9, "tanks", "fish", 54, "The hall shows")]
for a, u1, u2, r, verb in N2:
    text = "%s %d %s * %d %s = %d in total." % (verb, a, u1, a, u2, r)
    add("N2", None, "inline", text, "SILENT",
        exemplar="chat doc 3 (3 sprints * 3 times a week = 9 — below the candidate gate)",
        note="true statement; no candidate forms; fails open")

# ---------------- N3 — fraction-compression notations (6: 3 inline, 3 scratchpad) ----------------
N3 = [(40, "cheaper"), (25, "off"), (60, "saved"),
      (75, "less"), (30, "reduced"), (90, "markdown")]
for i, (n, word) in enumerate(N3):
    fam = "inline" if i < 3 else "scratchpad"
    if fam == "inline":
        text = "The discount comes to %d/100 = $%d %s." % (n, n, word)
    else:
        text = "The discount math: <<%d/100 = %d>> %s." % (n, n, word)
    add("N3", None, fam, text, "SLIP-FLAG", slips=1,
        lhs="%d/100" % n, stated=str(n),
        exemplar="raw doc 978 (40/100 = $40 cheaper; the 26-event compression class)",
        pending="gate5-compression",
        note="fires under the banked bare-fraction rule as-is; branch pre-registered on the Gate-5 stamp")

# ---------------- N4 — equivalence chains (6, inline-only) ----------------
N4 = [("Plan A", "Plan A-prime", 48, "units"),
      ("Route x", "Route x-prime", 120, "miles"),
      ("Item k", "Item k-prime", 260, "dollars"),
      ("Team one", "Team one-alt", 37, "points"),
      ("Model M", "Model M2", 94, "outputs"),
      ("Batch 1", "Batch 1b", 410, "items")]
for a, b, v, unit in N4:
    text = "The record lists %s = %s = %d %s." % (a, b, v, unit)
    add("N4", None, "inline", text, "SILENT",
        exemplar="the 189-rejection equivalence-chain class (raw leg)",
        note="restatement style; no candidate forms; never fires")

# ---------------- N5 — dimensional / prose '=' (6, inline-only) ----------------
N5 = ["The route covers 12 miles / 12 hours.",
      "The recipe needs 3 cups / 2 quarts.",
      "The pump moves 500 gallons / 10 minutes.",
      "The standard relation reads speed = distance / time.",
      "The flow equation is flow = volume / time.",
      "The pace formula is pace = distance / duration."]
for text in N5:
    add("N5", None, "inline", text, "SILENT",
        exemplar="the 50-rejection lhs-not-arith class (raw leg)",
        note="dimensional prose; no candidate forms; fails open")

# ---------------- N6 — space-thousands true statements (6: 3 inline, 3 scratchpad) ----------------
# Honest form note: the space-thousands merge runs on the inline anchor
# window only (the scratchpad path tokenizes the span verbatim), so
# scratchpad rows use comma forms; percent forms fall below the banked
# candidate gate (LHS_NUM carries no %) and are not this class.
N6i = [("The ledger shows 12 400 + 3 600 = 16000.", "12400 + 3600", "16000"),
       ("The city counts 400 000 + 12 000 = 412000 residents.", "400000 + 12000", "412000"),
       ("The bank holds 2,500 + 1,350 = 3,850.", "2,500 + 1,350", "3,850")]
N6s = [("The bank statement: <<2,500 + 1,350 = 3,850>>.", "2,500 + 1,350", "3,850"),
       ("The plant total: <<1,250 x 4 = 5000>>.", "1,250 x 4", "5000"),
       ("The yield sheet: <<12,400 + 3,600 = 16000>>.", "12,400 + 3,600", "16000")]
for text, lhs, st in N6i:
    add("N6", None, "inline", text, "PASS", lhs=lhs, stated=st,
        exemplar="the space-thousands merge class (the self-check of record)",
        note="thousands must merge and AGREE")
for text, lhs, st in N6s:
    add("N6", None, "scratchpad", text, "PASS", lhs=lhs, stated=st,
        exemplar="the space-thousands merge class (the self-check of record)",
        note="thousands must merge and AGREE")

# ---------------- N7 — truncation-rounding displays (6: 3 inline, 3 scratchpad) ----------------
N7 = [(80, 75, "1.066"), (4100, 3, "1366.66"), (22, 7, "3.142"),
      (100, 6, "16.66"), (1000, 7, "142.85"), (500, 7, "71.42")]
for i, (a, b, st) in enumerate(N7):
    fam = "inline" if i < 3 else "scratchpad"
    lhs = "%d/%d" % (a, b)
    if fam == "inline":
        text = "The ratio reads %s = %s truncated." % (lhs, st)
    else:
        text = "The ratio: <<%s = %s>> truncated." % (lhs, st)
    add("N7", None, fam, text, "SLIP-FLAG", slips=1, lhs=lhs, stated=st,
        exemplar="the truncation-rounding subclass (80/75 = 1.066; item 55)",
        pending="gate5-truncation",
        note="truncated display beyond the half-unit tolerance as-is; branch pre-registered on the Gate-5 stamp")

# ---------------- N8 — the fails-open floor (6, inline/prose-only) ----------------
add("N8", None, "inline", "The venture will not have a profit.", "SILENT",
    exemplar="the chat qualitative-answer class", note="no candidate forms")
add("N8", None, "inline", "The committee has no remaining seats.", "SILENT",
    exemplar="the chat qualitative-answer class", note="no candidate forms")
add("N8", None, "inline", "The running total was 340 + 25 =", "UNVERIFIED",
    lhs="340 + 25", stated=None, evclass="no-parseable-result",
    exemplar="the cap-truncated class (raw doc 298)",
    note="truncated result; fails open, no invented verdict")
add("N8", None, "inline", "The count so far is 1,240 + 88 =", "UNVERIFIED",
    lhs="1,240 + 88", stated=None, evclass="no-parseable-result",
    exemplar="the cap-truncated class (raw doc 298)",
    note="truncated result; fails open, no invented verdict")
add("N8", None, "inline", "The sum is = = 5.", "SILENT",
    exemplar="the malformed class", note="no well-formed candidate; fails open")
add("N8", None, "inline", "The total equals = = 12.", "SILENT",
    exemplar="the malformed class", note="no well-formed candidate; fails open")

# ---------------- build assertions (the census gates) ----------------
errors = []
for r in ROWS:
    gt = r["ground_truth"]
    if r["expected_verdict"] == "SLIP-FLAG" and r["pending_ruling"] is None:
        if not (gt and gt["beyond_epsilon_as_is"]):
            errors.append("%s: positive/compression target not beyond epsilon" % r["fixture_id"])
    if r["expected_verdict"] == "PASS":
        if gt is None or gt["beyond_epsilon_as_is"]:
            errors.append("%s: PASS control not within tolerance" % r["fixture_id"])
    if r["expected_verdict"] == "SLIP-FLAG" and r["pending_ruling"] is not None:
        if not (gt and gt["beyond_epsilon_as_is"]):
            errors.append("%s: pending-ruling row not beyond epsilon as-is" % r["fixture_id"])

if len(ROWS) != 96:
    errors.append("row count %d != 96" % len(ROWS))
per_class = {}
for r in ROWS:
    per_class.setdefault(r["class"], []).append(r)
expect_counts = {"P1": 8, "P2": 8, "P3": 8, "P4": 8, "P5": 8, "P6": 8,
                 "N1": 6, "N2": 6, "N3": 6, "N4": 6, "N5": 6, "N6": 6,
                 "N7": 6, "N8": 6}
for cls, n in expect_counts.items():
    if len(per_class.get(cls, [])) != n:
        errors.append("class %s count %d != %d" % (cls, len(per_class.get(cls, [])), n))
for cls in ["P1", "P2", "P3", "P4", "P5", "P6"]:
    mags = [r["magnitude"] for r in per_class[cls]]
    fams = [r["anchor_family"] for r in per_class[cls]]
    if mags.count("loud") != 4 or mags.count("subtle") != 4:
        errors.append("class %s loud/subtle imbalance: %s" % (cls, mags))
    if fams.count("inline") != 4 or fams.count("scratchpad") != 4:
        errors.append("class %s family imbalance: %s" % (cls, fams))
for r in ROWS:
    for key in ("fixture_id", "class", "magnitude", "anchor_family",
                "statement_text", "ground_truth", "expected_verdict",
                "expected_slips", "expected_guard", "expected_event_class",
                "habit_exemplar", "pending_ruling", "class_note"):
        if key not in r:
            errors.append("%s: missing slot %s" % (r["fixture_id"], key))

if errors:
    for e in errors:
        print("BUILD-GATE FAIL:", e)
    sys.exit(1)

suite = {
    "suite": "triadic_arith_fixture_suite_v1",
    "family": "arith-* (17-A; the GROUP-3 label retired, item 128)",
    "pre_registration": "arith-fixture-family-preregistration.md",
    "option": "arith-M (96 rows: 48 positives, 48 controls)",
    "rw5_paraphrase_axis": "OFF (my ruling, item 162)",
    "typed_row_schema": ["fixture_id", "class", "magnitude", "anchor_family",
                         "statement_text", "ground_truth", "expected_verdict",
                         "expected_slips", "expected_guard", "expected_event_class",
                         "habit_exemplar", "pending_ruling", "class_note"],
    "family_applicability_note": (
        "P1-P6 instantiate both anchor families (4 inline / 4 scratchpad). "
        "N3/N6/N7 instantiate both (3/3). N1 (the inline word-separated "
        "fragment), N2 (word-separated prose), N4 (prose restatements), N5 "
        "(dimensional prose) and N8 (the fails-open floor) have no banked "
        "scratchpad form — authored inline/prose only, recorded here as "
        "class applicability, not as a census gap."),
    "expected_verdict_enum_note": (
        "SILENT extends the pre-registered enum for rows where no candidate "
        "forms at all (N2/N4/N5 and the N8 SILENT rows) — the pre-registered "
        "class descriptions ('fails open, silent') carried the semantics; "
        "the export makes the slot explicit and typed."),
    "pending_ruling_rows": {
        "gate5-compression": "N3 (6 rows)",
        "gate5-truncation": "N7 (6 rows)",
        "branches": "both pre-registered; my Gate-5 stamp decides "
                    "(tolerance-legal display vs charged damage)",
    },
    "counts": {
        "total": len(ROWS),
        "positives": len([r for r in ROWS if r["class"].startswith("P")]),
        "controls": len([r for r in ROWS if r["class"].startswith("N")]),
        "per_class": {cls: len(v) for cls, v in sorted(per_class.items())},
        "loud": len([r for r in ROWS if r["magnitude"] == "loud"]),
        "subtle": len([r for r in ROWS if r["magnitude"] == "subtle"]),
        "inline": len([r for r in ROWS if r["anchor_family"] == "inline"]),
        "scratchpad": len([r for r in ROWS if r["anchor_family"] == "scratchpad"]),
    },
    "fixtures": ROWS,
}

out = os.path.join(HERE, "triadic_arith_fixture_suite_v1.json")
data = json.dumps(suite, indent=1, ensure_ascii=False).encode("utf-8")
with open(out, "wb") as f:
    f.write(data)
sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
print("BUILD: arith-M suite — %d rows (48 P / 48 N), %d loud / %d subtle, "
      "%d inline / %d scratchpad" % (len(ROWS), suite["counts"]["loud"],
      suite["counts"]["subtle"], suite["counts"]["inline"],
      suite["counts"]["scratchpad"]))
print("BUILD: all census gates PASS; ground-truth assertions PASS")
print("triadic_arith_fixture_suite_v1.json  %d bytes" % os.path.getsize(out))
print("SHA-256 %s" % sha)

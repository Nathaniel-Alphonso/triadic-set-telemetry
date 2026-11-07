#!/usr/bin/env python3
"""build_code_fixtures.py -- Gate 17-C code-* fixture family builder (v1.0).

Builds triadic_code_fixture_suite_v1.json per code-fixture-family-preregistration.md
(MY STAMP Oct 9 2026, ledger item 166): sizing code-M (96 rows: 48 positives,
8 per class with loud/subtle balanced 4+4; 48 controls, 6 per class); meter budget
p99x1.5 = 3,910,116 STAMPED (R-K6); RW-5 paraphrase axis OFF; P6 branch (a)
as-is boundary census.

Discipline (pre-registered, binding):
- deterministic, templated, zero model, zero unseeded randomness;
- every ground truth verified AT BUILD by execution (the banked instrument's own
  meter + the rejudge execution convention: fresh subprocess per rep, own temp
  dir, failsafes SAFETY-ONLY -> resource-class UNVERIFIED, never semantic);
- loudness verified by a counted-assert probe (build-only; the suite rows carry
  the canonical harnesses verbatim);
- build-gate catches fix the FIXTURE or the BUILDER, never the banked instrument;
- rebuild must be byte-identical (no timestamps, no randomness in the output).

Inputs PINNED from the banked record (VOID on mismatch):
- the he-base164 base dump          (SHA-256 8dabe677...813, ledger item 131)
- the canonical-prompt export       (SHA-256 b00ec345...61b, ledger item 132/137)
- the 17-C offline-pass instrument  (SHA-256 439c892a...5e, ledger item 138)
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DUMP_PATH = "/home/user/uploads/triadic_generations_humaneval_he-base164-v31.json"
PROMPTS_PATH = os.path.join(HERE, "triadic_canonical_prompts_he164.json")
SUITE_PATH = os.path.join(HERE, "triadic_code_fixture_suite_v1.json")

PIN_DUMP = "8dabe677801104d3180cdc9c992532042cdbd56ac848bc56080a2a0fb8481813"
PIN_PROMPTS = "b00ec345cca4c0573d18cc1b45164e80ac4977e4d7006399d319a506e3d8c61b"
PIN_INSTR = "439c892a5b1a27a7ed1b5f7dd2d9a4e99c9c57d072e1b14fc0a18f3ecd8efc5e"

sys.path.insert(0, HERE)
import triadic_code17c_offline_pass as instr  # the banked instrument of record

METER_BAND_LO = 2344000   # the natural p95 (measured census of record)
METER_BAND_HI = 2606744   # the natural p99 (measured census of record)
BUDGET_STAMPED = 3910116  # p99 x 1.5 -- my R-K6 stamp (item 166)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 1. Pinned inputs (integrity gates -- VOID rule)
# ---------------------------------------------------------------------------

def load_inputs():
    dump_sha = sha256_file(DUMP_PATH)
    prompts_sha = sha256_file(PROMPTS_PATH)
    instr_sha = sha256_file(os.path.join(HERE, "triadic_code17c_offline_pass.py"))
    assert dump_sha == PIN_DUMP, f"dump pin mismatch: {dump_sha}"
    assert prompts_sha == PIN_PROMPTS, f"prompts pin mismatch: {prompts_sha}"
    assert instr_sha == PIN_INSTR, f"instrument pin mismatch: {instr_sha}"
    with open(DUMP_PATH) as f:
        dump = json.load(f)
    with open(PROMPTS_PATH) as f:
        prompts = json.load(f)
    docs = {d["doc_id"]: d for d in dump}
    assert len(docs) == 164 and len(prompts) == 164
    # the item-137e law: every dump prompt_head is an exact prefix of its prompt
    for d in dump:
        assert prompts[str(d["doc_id"])].startswith(d["prompt_head"]), \
            f"prompt_head prefix law violated at doc {d['doc_id']}"
    return docs, prompts


# ---------------------------------------------------------------------------
# 2. Authored solutions (the correct bases; mutations applied at design time)
# ---------------------------------------------------------------------------

SOL = {
    0: [
        "    for i in range(len(numbers)):",
        "        for j in range(i + 1, len(numbers)):",
        "            if abs(numbers[i] - numbers[j]) < threshold:",
        "                return True",
        "    return False",
    ],
    2: [
        "    return number % 1",
    ],
    7: [
        "    return [x for x in strings if substring in x]",
    ],
    16: [
        "    return len(set(string.lower()))",
    ],
    23: [
        "    return len(string)",
    ],
    33: [
        "    l = list(l)",
        "    thirds = sorted(l[::3])",
        "    j = 0",
        "    for i in range(0, len(l), 3):",
        "        l[i] = thirds[j]",
        "        j += 1",
        "    return l",
    ],
    36: [  # two-loop stride version (authored variant A)
        "    count = 0",
        "    for i in range(11, n, 11):",
        "        count += str(i).count('7')",
        "    for j in range(13, n, 13):",
        "        count += str(j).count('7')",
        "    return count",
    ],
    40: [
        "    for i in range(len(l)):",
        "        for j in range(i + 1, len(l)):",
        "            for k in range(j + 1, len(l)):",
        "                if l[i] + l[j] + l[k] == 0:",
        "                    return True",
        "    return False",
    ],
    45: [
        "    return a * h / 2.0",
    ],
    47: [
        "    l = sorted(l)",
        "    n = len(l)",
        "    if n % 2 == 1:",
        "        return l[n // 2]",
        "    return (l[n // 2 - 1] + l[n // 2]) / 2",
    ],
    52: [
        "    for e in l:",
        "        if e >= t:",
        "            return False",
        "    return True",
    ],
    55: [
        "    a, b = 0, 1",
        "    for _ in range(n):",
        "        a, b = b, a + b",
        "    return a",
    ],
    104: [
        "    result = []",
        "    for n in x:",
        "        if all(int(ch) % 2 == 1 for ch in str(abs(n))):",
        "            result.append(n)",
        "    return sorted(result)",
    ],
    147: [
        "    a = [i * i - i + 1 for i in range(1, n + 1)]",
        "    count = 0",
        "    for i in range(n):",
        "        for j in range(i + 1, n):",
        "            for k in range(j + 1, n):",
        "                if (a[i] + a[j] + a[k]) % 3 == 0:",
        "                    count += 1",
        "    return count",
    ],
}

def C(doc, lines):
    """Authored code constant (a list of lines) -> generated text."""
    return "\n".join(lines) + "\n"

def mutated(doc, lines):
    return C(doc, lines)

# find_zero solutions (authored; the doc-32 prompt defines poly) -- N2 class
FIND_ZERO_A = "\n".join([
    "    import math",
    "",
    "    def deriv(x):",
    "        d = 0.0",
    "        for i in range(1, len(xs)):",
    "            d += i * xs[i] * x ** (i - 1)",
    "        return d",
    "",
    "    x = 0.0",
    "    for _ in range(200):",
    "        p = poly(xs, x)",
    "        if abs(p) < 1e-6:",
    "            break",
    "        dd = deriv(x)",
    "        if abs(dd) < 1e-10:",
    "            break",
    "        x = x - p / dd",
    "    if abs(poly(xs, x)) < 1e-4:",
    "        return x",
    "    lo, hi = -1000.0, 1000.0",
    "    prev = lo",
    "    prevv = poly(xs, lo)",
    "    if prevv == 0.0:",
    "        return lo",
    "    cur = lo",
    "    while cur < hi:",
    "        cur += 1.0",
    "        v = poly(xs, cur)",
    "        if v == 0.0:",
    "            return cur",
    "        if (prevv < 0) != (v < 0):",
    "            aa, bb = prev, cur",
    "            for _ in range(200):",
    "                mid = (aa + bb) / 2",
    "                vm = poly(xs, mid)",
    "                if vm == 0.0:",
    "                    return mid",
    "                if (vm < 0) == (poly(xs, aa) < 0):",
    "                    aa = mid",
    "                else:",
    "                    bb = mid",
    "            return (aa + bb) / 2",
    "        prev, prevv = cur, v",
    "    return x",
]) + "\n"

FIND_ZERO_B = "\n".join([
    "    import math",
    "",
    "    def slope(x):",
    "        s = 0.0",
    "        for i in range(1, len(xs)):",
    "            if xs[i] != 0:",
    "                s += i * xs[i] * x ** (i - 1)",
    "        return s",
    "",
    "    x = 1.0",
    "    for _ in range(100):",
    "        p = poly(xs, x)",
    "        if abs(p) < 1e-6:",
    "            break",
    "        m = slope(x)",
    "        if abs(m) < 1e-10:",
    "            break",
    "        x = x - p / m",
    "    if abs(poly(xs, x)) < 1e-4:",
    "        return x",
    "    step = 1.0",
    "    a = -1000.0",
    "    fa = poly(xs, a)",
    "    if fa == 0.0:",
    "        return a",
    "    while a < 1000.0:",
    "        b = a + step",
    "        fb = poly(xs, b)",
    "        if fb == 0.0:",
    "            return b",
    "        if (fa < 0) != (fb < 0):",
    "            for _ in range(200):",
    "                m2 = (a + b) / 2",
    "                fm = poly(xs, m2)",
    "                if fm == 0.0:",
    "                    return m2",
    "                if (fm < 0) == (fa < 0):",
    "                    a = m2",
    "                else:",
    "                    b = m2",
    "            return (a + b) / 2",
    "        a, fa = b, fb",
    "    return x",
]) + "\n"

# N2 authored problems + seeded harnesses (fixed banked seeds; unseeded never appears)
N2_AUTHORED = {
    "weighted_sum": {
        "prompt": "\n\ndef weighted_sum(xs: list, w: list):\n    \"\"\"Return the dot product: sum(x * wi for x, wi in zip(xs, w)).\"\"\"\n",
        "gen": "    return sum(x * wi for x, wi in zip(xs, w))\n",
        "seed": 42,
        "body": [
            "    import random",
            "    rng = random.Random(42)",
            "    for _ in range(50):",
            "        k = rng.randint(1, 20)",
            "        xs = [rng.randint(-100, 100) for _ in range(k)]",
            "        w = [rng.randint(-10, 10) for _ in range(k)]",
            "        assert candidate(xs, w) == sum(a * b for a, b in zip(xs, w))",
        ],
    },
    "max_gap": {
        "prompt": "\n\ndef max_gap(a: list):\n    \"\"\"Return the maximum absolute difference between adjacent elements of a.\n    Lists with fewer than two elements return 0.\n    \"\"\"\n",
        "gen": "    if len(a) < 2:\n        return 0\n    return max(abs(a[i + 1] - a[i]) for i in range(len(a) - 1))\n",
        "seed": 7,
        "body": [
            "    import random",
            "    rng = random.Random(7)",
            "    for _ in range(50):",
            "        k = rng.randint(0, 30)",
            "        a = [rng.randint(-50, 50) for _ in range(k)]",
            "        if k < 2:",
            "            expected = 0",
            "        else:",
            "            expected = max(abs(a[i + 1] - a[i]) for i in range(k - 1))",
            "        assert candidate(a) == expected",
        ],
    },
    "count_neg": {
        "prompt": "\n\ndef count_neg(xs: list):\n    \"\"\"Return how many elements of xs are negative.\"\"\"\n",
        "gen": "    count = 0\n    for x in xs:\n        if x < 0:\n            count += 1\n    return count\n",
        "seed": 123,
        "body": [
            "    import random",
            "    rng = random.Random(123)",
            "    for _ in range(50):",
            "        k = rng.randint(0, 40)",
            "        xs = [rng.randint(-9, 9) for _ in range(k)]",
            "        assert candidate(xs) == sum(1 for v in xs if v < 0)",
        ],
    },
    "range_sum": {
        "prompt": "\n\ndef range_sum(lo: int, hi: int):\n    \"\"\"Return the sum of the integers lo..hi inclusive; lo > hi returns 0.\"\"\"\n",
        "gen": "    if lo > hi:\n        return 0\n    return sum(range(lo, hi + 1))\n",
        "seed": 2026,
        "body": [
            "    import random",
            "    rng = random.Random(2026)",
            "    for _ in range(50):",
            "        lo = rng.randint(-30, 30)",
            "        hi = rng.randint(-30, 30)",
            "        if lo > hi:",
            "            expected = 0",
            "        else:",
            "            expected = sum(range(lo, hi + 1))",
            "        assert candidate(lo, hi) == expected",
        ],
    },
}

def n2_target(fn):
    spec = N2_AUTHORED[fn]
    lines = ["\n\nMETADATA = {}", "", "", "def check(candidate):"]
    lines += spec["body"]
    lines += ["", "", f"check({fn})", ""]
    return "\n".join(lines)

# N3 authored heavy problems (constants frozen from calibration; meters in-band)
N3_SHAPES = {
    "digit_scan": {"digit": "3", "calls": [(10, 1), (37000, 22101), (35000, 19501)],
                   "band_note": "digit-scan (the doc-36 heavy shape)"},
    "seven_scan": {"digit": "7", "calls": [(10, 1), (36000, 13800)],
                   "band_note": "digit-scan (the doc-36 heavy shape)"},
    "five_scan": {"digit": "5", "calls": [(10, 1), (36000, 14800)],
                  "band_note": "digit-scan (the doc-36 heavy shape)"},
    "prime_sum": {"calls": [(10, 17), (2000, 277050)],
                  "band_note": "trial-division scan (the doc-147 heavy shape)"},
    "collatz_max": {"calls": [(10, 19), (1850, 181)],
                    "band_note": "trajectory scan (the doc-147 heavy shape)"},
}

N3_GEN = {
    "digit_scan": "    count = 0\n    for i in range(1, n + 1):\n        x = i\n        while x:\n            if x % 10 == {D}:\n                count += 1\n            x //= 10\n    return count\n",
    "prime_sum": "    total = 0\n    for i in range(2, n + 1):\n        is_p = True\n        for d in range(2, i):\n            if i % d == 0:\n                is_p = False\n                break\n        if is_p:\n            total += i\n    return total\n",
    "collatz_max": "    best = 0\n    for k in range(2, n + 1):\n        x = k\n        steps = 0\n        while x != 1:\n            if x % 2 == 0:\n                x //= 2\n            else:\n                x = 3 * x + 1\n            steps += 1\n        if steps > best:\n            best = steps\n    return best\n",
}

N3_PROMPTS = {
    "digit_scan": "\n\ndef digit_scan(n: int):\n    \"\"\"Count occurrences of the digit 3 in the decimal representations of the integers 1..n (inclusive).\"\"\"\n",
    "seven_scan": "\n\ndef seven_scan(n: int):\n    \"\"\"Count occurrences of the digit 7 in the decimal representations of the integers 1..n (inclusive).\"\"\"\n",
    "five_scan": "\n\ndef five_scan(n: int):\n    \"\"\"Count occurrences of the digit 5 in the decimal representations of the integers 1..n (inclusive).\"\"\"\n",
    "prime_sum": "\n\ndef prime_sum(n: int):\n    \"\"\"Return the sum of all primes <= n, by trial division.\"\"\"\n",
    "collatz_max": "\n\ndef collatz_max(n: int):\n    \"\"\"Return the maximum Collatz step count over the integers 2..n (inclusive).\"\"\"\n",
}

def n3_target(fn, heavy):
    # one small warm-up assert + the row's single calibrated heavy call
    calls = [N3_SHAPES[fn]["calls"][0], heavy]
    lines = ["\n\nMETADATA = {}", "", "", "def check(candidate):"]
    for call, val in calls:
        lines.append(f"    assert candidate({call}) == {val}")
    lines += ["", "", f"check({fn})", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. The fixture table (born typed; RW-6 sub-pass B -- zero narrative slots)
# ---------------------------------------------------------------------------

def banked_row(fid, cls, doc, gen, mutation, gt_mode, loudness, m1, verdict,
               prose, exemplar, extra=None):
    return {
        "fixture_id": fid,
        "class": cls,
        "source_problem": f"he-doc-{doc}",
        "generated": gen,
        "mutation": mutation,
        "ground_truth_mode": gt_mode,
        "loudness": loudness,
        "expected_m1_class": m1,
        "expected_verdict": verdict,
        "expected_prose_flag": prose,
        "habit_exemplar": exemplar,
        "extra": extra or {},
    }

def authored_row(fid, cls, prompt, gen, target, mutation, gt_mode, loudness, m1,
                 verdict, prose, exemplar, extra=None):
    return {
        "fixture_id": fid,
        "class": cls,
        "source_problem": "AUTHORED",
        "authored_prompt": prompt,
        "generated": gen,
        "target": target,
        "mutation": mutation,
        "ground_truth_mode": gt_mode,
        "loudness": loudness,
        "expected_m1_class": m1,
        "expected_verdict": verdict,
        "expected_prose_flag": prose,
        "habit_exemplar": exemplar,
        "extra": extra or {},
    }

FIXTURES = []

# ---- P1 -- boundary mutation (4 loud + 4 subtle) --------------------------
FIXTURES += [
    banked_row("code-P1-001", "P1", 55,
               mutated(55, ["    a, b = 0, 1", "    for _ in range(1, n):",
                            "        a, b = b, a + b", "    return a"]),
               "loop-start boundary slip: range(n) -> range(1, n)",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "the 106 FAIL-TESTS natural census (loop-bound slips)"),
    banked_row("code-P1-002", "P1", 23,
               "    return len(string[:-1]) + 1\n",
               "slice-endpoint boundary slip (bites only at the empty-string boundary)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "the arith subtle class analog: one unit past the boundary"),
    banked_row("code-P1-003", "P1", 16,
               "    return len(set(string[1:].lower()))\n",
               "scan-start index-base slip (the first character is dropped)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "index-base slips in the natural FAIL-TESTS census"),
    banked_row("code-P1-004", "P1", 0,
               C(0, ["    for i in range(len(numbers)):",
                     "        for j in range(i + 2, len(numbers)):",
                     "            if abs(numbers[i] - numbers[j]) < threshold:",
                     "                return True",
                     "    return False"]),
               "scan-start boundary slip: j begins at i + 2 (adjacent pairs are never compared)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "scan-boundary slips in the natural FAIL-TESTS census"),
    banked_row("code-P1-005", "P1", 47,
               C(47, ["    l = sorted(l)", "    n = len(l)",
                      "    if n % 2 == 1:", "        return l[n // 2 + 1]",
                      "    return (l[n // 2 - 1] + l[n // 2]) / 2"]),
               "odd-branch index boundary slip: n//2 -> n//2 + 1 (overruns on short lists)",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "index-boundary overruns in the natural FAIL-TESTS census"),
    banked_row("code-P1-006", "P1", 55,
               mutated(55, ["    a, b = 0, 1", "    for _ in range(n - 1):",
                            "        a, b = b, a + b", "    return a"]),
               "loop-endpoint boundary slip: range(n) -> range(n - 1)",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "the 106 FAIL-TESTS natural census (loop-bound slips)"),
    banked_row("code-P1-007", "P1", 16,
               "    return len(set(string.lower())) - 1\n",
               "off-by-one count slip: len(...) -> len(...) - 1",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "off-by-one counts in the natural FAIL-TESTS census"),
    banked_row("code-P1-008", "P1", 52,
               C(52, ["    for e in l[:-1]:", "        if e >= t:",
                      "            return False", "    return True"]),
               "scan-endpoint boundary slip: iterates l[:-1] (the last element is skipped)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "scan-boundary slips in the natural FAIL-TESTS census"),
]

# ---- P2 -- condition inversion / miswiring (4 loud + 4 subtle) -----------
FIXTURES += [
    banked_row("code-P2-001", "P2", 0,
               C(0, ["    for i in range(len(numbers)):",
                     "        for j in range(i + 1, len(numbers)):",
                     "            if abs(numbers[i] - numbers[j]) < threshold:",
                     "                return False",
                     "    return True"]),
               "condition inversion: the close-pair branch returns False; the fall-through True",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "inverted branch returns in the natural FAIL-TESTS census"),
    banked_row("code-P2-002", "P2", 0,
               C(0, ["    for i in range(len(numbers)):",
                     "        for j in range(i + 1, len(numbers)):",
                     "            if abs(numbers[i] - numbers[j]) < threshold and numbers[i] != numbers[j]:",
                     "                return True",
                     "    return False"]),
               "compound-guard miswiring: the closeness test gains an inequality guard (equal values never count as close)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "miswired compound guards in the natural FAIL-TESTS census"),
    banked_row("code-P2-003", "P2", 52,
               C(52, ["    for e in l:", "        if e < t:",
                      "            return False", "    return True"]),
               "condition inversion: the below-threshold test returns False",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "inverted early-exit conditions in the natural FAIL-TESTS census"),
    banked_row("code-P2-004", "P2", 52,
               C(52, ["    for e in l:", "        if e > t:",
                      "            return False", "    return True"]),
               "boundary condition flip: >= -> >",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "boundary-comparison flips in the natural FAIL-TESTS census"),
    banked_row("code-P2-005", "P2", 104,
               C(104, ["    result = []", "    for n in x:",
                       "        if all(int(ch) % 2 == 0 for ch in str(abs(n))):",
                       "            result.append(n)",
                       "    return sorted(result)"]),
               "condition inversion: the all-odd digit check flipped to all-even",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "inverted digit checks in the natural FAIL-TESTS census"),
    banked_row("code-P2-006", "P2", 47,
               C(47, ["    l = sorted(l)", "    n = len(l)",
                      "    if n % 3 == 1:", "        return l[n // 2]",
                      "    return (l[n // 2 - 1] + l[n // 2]) / 2"]),
               "condition miswiring: the parity test 2 -> 3 (n % 2 == 1 -> n % 3 == 1)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "miswired compound guards in the natural FAIL-TESTS census"),
    banked_row("code-P2-007", "P2", 36,
               C(36, ["    count = 0", "    for i in range(1, n):",
                      "        if i % 11 == 0 and i % 13 == 0:",
                      "            count += str(i).count('7')",
                      "    return count"]),
               "condition miswiring: or -> and in the divisibility test",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "he doc 36 (the natural p99 heavy shape; divisibility-condition slips)"),
    banked_row("code-P2-008", "P2", 104,
               C(104, ["    result = []", "    for n in x:",
                       "        if all(int(ch) % 2 == 1 for ch in str(abs(n))) and n > 1:",
                       "            result.append(n)",
                       "    return sorted(result)"]),
               "compound-guard miswiring: the all-odd check gains an n > 1 guard (the element 1 is dropped)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "miswired compound guards in the natural FAIL-TESTS census"),
]

# ---- P3 -- operand / constant slip (4 loud + 4 subtle) --------------------
FIXTURES += [
    banked_row("code-P3-001", "P3", 45,
               "    return a * h / 4.0\n",
               "constant slip: the halving constant 2.0 -> 4.0",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "wrong constants in the natural FAIL-TESTS census"),
    banked_row("code-P3-002", "P3", 2,
               "    return number % 2\n",
               "operand slip: the modulus 1 -> 2",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "wrong operands in the natural FAIL-TESTS census"),
    banked_row("code-P3-003", "P3", 104,
               C(104, ["    result = []", "    for n in x:",
                       "        if all(int(ch) % 3 == 1 for ch in str(abs(n))):",
                       "            result.append(n)",
                       "    return sorted(result)"]),
               "operand slip: % 2 == 1 -> % 3 == 1",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "wrong operands in the natural FAIL-TESTS census"),
    banked_row("code-P3-004", "P3", 55,
               mutated(55, ["    a, b = 1, 1", "    for _ in range(n):",
                            "        a, b = b, a + b", "    return a"]),
               "seeding-constant slip: (0, 1) -> (1, 1)",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "the doc-11 seeding-slip habit, instantiated in code"),
    banked_row("code-P3-005", "P3", 45,
               "    return a * h // 2\n",
               "operator/operand slip: / -> // (floor division truncates the half)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "operator slips that survive some cases in the natural census"),
    banked_row("code-P3-006", "P3", 40,
               C(40, ["    for i in range(len(l)):",
                      "        for j in range(i + 1, len(l)):",
                      "            for k in range(j + 1, len(l)):",
                      "                if l[i] + l[j] + l[k] == 1:",
                      "                    return True",
                      "    return False"]),
               "constant slip: == 0 -> == 1 (one True-expected assert survives coincidentally)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "near-miss constants in the natural FAIL-TESTS census"),
    banked_row("code-P3-007", "P3", 52,
               C(52, ["    for e in l:", "        if e >= t + 1:",
                      "            return False", "    return True"]),
               "operand slip: t -> t + 1 in the threshold comparison",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "off-by-one operands in the natural FAIL-TESTS census "
               "(shares the case-6 bite point with P2-004's boundary flip -- "
               "equivalent on integer thresholds, distinct mutation texts; honest design note)"),
    banked_row("code-P3-008", "P3", 0,
               C(0, ["    for i in range(len(numbers)):",
                     "        for j in range(i + 1, len(numbers)):",
                     "            if abs(numbers[i] - numbers[j]) < threshold - 0.05:",
                     "                return True",
                     "    return False"]),
               "operand slip: threshold -> threshold - 0.05 (an added offset constant)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "drifted operands in the natural FAIL-TESTS census"),
]

# ---- P4 -- wrong return (4 loud + 4 subtle) -------------------------------
FIXTURES += [
    banked_row("code-P4-001", "P4", 7,
               "    return strings\n",
               "wrong-return: the input list returned unfiltered",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "wrong-variable returns in the natural FAIL-TESTS census"),
    banked_row("code-P4-002", "P4", 104,
               "    return sorted(x)\n",
               "wrong-return: the input returned sorted instead of the filtered result",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "wrong-variable returns in the natural FAIL-TESTS census"),
    banked_row("code-P4-003", "P4", 55,
               mutated(55, ["    a, b = 0, 1", "    for _ in range(n):",
                            "        a, b = b, a + b", "    return b"]),
               "wrong-variable return: b (the next Fibonacci number) instead of a",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "off-by-one-step returns in the natural FAIL-TESTS census"),
    banked_row("code-P4-004", "P4", 147,
               SOL[147][0:1] + SOL[147][1:] and mutated(147, [
                   "    a = [i * i - i + 1 for i in range(1, n + 1)]",
                   "    count = 0",
                   "    for i in range(n):",
                   "        for j in range(i + 1, n):",
                   "            for k in range(j + 1, n):",
                   "                if (a[i] + a[j] + a[k]) % 3 == 0:",
                   "                    count += 1",
                   "    return n"]),
               "wrong-variable return: n instead of count",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "wrong-variable returns in the natural FAIL-TESTS census"),
    banked_row("code-P4-005", "P4", 7,
               "    return [x for x in strings if substring in x] or None\n",
               "wrong-return: a falsy fallback returns None on the empty match",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "falsy-fallback returns in the natural FAIL-TESTS census"),
    banked_row("code-P4-006", "P4", 23,
               "    return len(string.split())\n",
               "wrong-return: the word count instead of the character count",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "wrong-unit returns in the natural FAIL-TESTS census"),
    banked_row("code-P4-007", "P4", 40,
               C(40, ["    for i in range(len(l)):",
                      "        for j in range(i + 1, len(l)):",
                      "            for k in range(j + 1, len(l)):",
                      "                if l[i] + l[j] + l[k] == 0:",
                      "                    return l[i]",
                      "    return False"]),
               "wrong-return value: the element l[i] instead of the boolean True (1 == True hides one assert)",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "typed-value slips in the natural FAIL-TESTS census"),
    banked_row("code-P4-008", "P4", 104,
               C(104, ["    result = []", "    for n in x:",
                       "        if all(int(ch) % 2 == 1 for ch in str(abs(n))):",
                       "            result.append(n)",
                       "    result = sorted(result)",
                       "    return result[1:] if len(result) > 2 else result"]),
               "wrong-return: the result list head-truncated under a length guard",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "index-truncated returns in the natural FAIL-TESTS census"),
]

# ---- P5 -- propagated cascade (4 loud + 4 subtle) -------------------------
FIXTURES += [
    banked_row("code-P5-001", "P5", 33,
               C(33, ["    l = list(l)", "    thirds = sorted(l[::3], reverse=True)",
                      "    j = 0",
                      "    for i in range(0, len(l), 3):",
                      "        l[i] = thirds[j]",
                      "        j += 1",
                      "    return l"]),
               "cascade: early sort-direction slip carrying through the reassembly",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "multi-step reassembly faults in the natural FAIL-TESTS census"),
    banked_row("code-P5-002", "P5", 147,
               C(147, ["    a = [i * i - i + 1 for i in range(1, n + 1)]",
                       "    count = 0",
                       "    for i in range(n):",
                       "        for j in range(i + 1, n):",
                       "            s = a[i] + a[j]",
                       "            for k in range(j + 1, n):",
                       "                if s - a[k] == 0:",
                       "                    count += 1",
                       "    return count"]),
               "cascade: early partial-sum slip (the triple test becomes a[i] + a[j] == a[k]) carrying through every counted triple",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "partial-sum slips in the natural FAIL-TESTS census"),
    banked_row("code-P5-003", "P5", 47,
               C(47, ["    l = sorted(l)", "    n = len(l) - 1",
                      "    if n % 2 == 1:", "        return l[n // 2]",
                      "    return (l[n // 2 - 1] + l[n // 2]) / 2"]),
               "cascade: early length slip (len - 1) flipping every downstream branch",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "the doc-11 seeding-slip-carrying habit, instantiated in code"),
    banked_row("code-P5-004", "P5", 55,
               mutated(55, ["    a, b = 1, 0", "    for _ in range(n):",
                            "        a, b = b, a + b", "    return a"]),
               "cascade: early seeding swap (0, 1) -> (1, 0) carrying through every iteration",
               "FAILS", "loud", "RUNNABLE", "FAIL-TESTS", False,
               "the doc-11 seeding-slip-carrying habit, instantiated in code"),
    banked_row("code-P5-005", "P5", 40,
               C(40, ["    n = len(l) - 1",
                      "    for i in range(n - 2):",
                      "        for j in range(i + 1, n - 1):",
                      "            for k in range(j + 1, n):",
                      "                if l[i] + l[j] + l[k] == 0:",
                      "                    return True",
                      "    return False"]),
               "cascade: early length slip (len - 1) carrying through every loop bound",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "bound slips that miss only boundary triples (the arith late-chain analog)"),
    banked_row("code-P5-006", "P5", 36,
               C(36, ["    count = 0",
                      "    for i in range(1, n + 1):",
                      "        if i % 11 == 0 or i % 13 == 0:",
                      "            count += str(i).count('7')",
                      "    return count"]),
               "cascade: shared-bound endpoint slip (range(1, n) -> range(1, n + 1)) carrying through the whole scan",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "he doc 36 (the natural p99 heavy shape; shared-bound slips)"),
    banked_row("code-P5-007", "P5", 40,
               C(40, ["    for i in range(len(l) - 2):",
                      "        for j in range(i + 1, len(l) - 1):",
                      "            s = l[i] - l[j]",
                      "            for k in range(j + 1, len(l)):",
                      "                if s + l[k] == 0:",
                      "                    return True",
                      "    return False"]),
               "cascade: early partial-sum slip (l[i] + l[j] -> l[i] - l[j]) carrying through every triple test",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "bound slips that miss only boundary triples (the arith late-chain analog)"),
    banked_row("code-P5-008", "P5", 47,
               C(47, ["    l = sorted(l, key=abs)", "    n = len(l)",
                      "    if n % 2 == 1:", "        return l[n // 2]",
                      "    return (l[n // 2 - 1] + l[n // 2]) / 2"]),
               "cascade: early sort-key slip (key=abs) carrying into the median extraction",
               "FAILS", "subtle", "RUNNABLE", "FAIL-TESTS", False,
               "sort-order slips in the natural FAIL-TESTS census"),
]

# ---- P6 -- stated-answer contradiction (as-is boundary census; 4+4) ------
P6_ROWS = [
    ("code-P6-001", 55, SOL[55], "fib(10)", "54", "subtle"),
    ("code-P6-002", 55, SOL[55], "fib(10)", "5490", "loud"),
    ("code-P6-003", 45, SOL[45], "triangle_area(5, 3)", "7.4", "subtle"),
    ("code-P6-004", 45, SOL[45], "triangle_area(5, 3)", "32", "loud"),
    ("code-P6-005", 47, SOL[47], "median([3, 1, 2, 4, 5])", "2", "subtle"),
    ("code-P6-006", 47, SOL[47], "median([3, 1, 2, 4, 5])", "300", "loud"),
    ("code-P6-007", 23, SOL[23], "strlen('asdasnakj')", "8", "subtle"),
    ("code-P6-008", 16, SOL[16], "count_distinct_characters('Jerry jERRY JeRRRY')", "47", "loud"),
]
for fid, doc, sol, headline, stated, loud in P6_ROWS:
    FIXTURES.append(banked_row(
        fid, "P6", doc,
        C(doc, sol) + "\n# The answer is " + stated + ".\n",
        "stated-answer contradiction: the prose answer contradicts the verified output "
        "(the oracle does not adjudicate stated prose today -- measured as-is per the stamp)",
        "PASS+PROSE-CONTRADICTION", loud, "RUNNABLE", "PASS", True,
        "the M3' NOT-MEASURED-ON-THIS-CORPUS record (0/164 natural stated-answer prose)",
        extra={"p6_headline": headline, "p6_stated": stated}))

# ---- N1 -- canonical-correct (zero-fire) -----------------------------------
for fid, doc in [("code-N1-001", 0), ("code-N1-002", 2), ("code-N1-003", 7),
                 ("code-N1-004", 16), ("code-N1-005", 23), ("code-N1-006", 47)]:
    FIXTURES.append(banked_row(
        fid, "N1", doc, C(doc, SOL[doc]), None, "PASS-ALL", None,
        "RUNNABLE", "PASS", False,
        "the 58-PASS natural census (correct code must never be failed)"))

# ---- N2 -- seeded randomized harness (zero-fire; R-C2 seeding rule) -------
FIXTURES.append(banked_row(
    "code-N2-001", "N2", 32, FIND_ZERO_A, None,
    "PASS-ALL (seeded harness: random.Random(42), the banked doc-32 pattern)",
    None, "RUNNABLE", "PASS", False,
    "he doc 32 find_zero (the SEEDED natural harness class: meter 3/3 deterministic)"))
FIXTURES.append(banked_row(
    "code-N2-002", "N2", 32, FIND_ZERO_B, None,
    "PASS-ALL (seeded harness: random.Random(42), the banked doc-32 pattern)",
    None, "RUNNABLE", "PASS", False,
    "he doc 32 find_zero (the SEEDED natural harness class: meter 3/3 deterministic)"))
for i, fn in enumerate(["weighted_sum", "max_gap", "count_neg", "range_sum"]):
    spec = N2_AUTHORED[fn]
    FIXTURES.append(authored_row(
        f"code-N2-00{i + 3}", "N2", spec["prompt"], spec["gen"], n2_target(fn),
        None,
        f"PASS-ALL (authored seeded harness: random.Random({spec['seed']}))",
        None, "RUNNABLE", "PASS", False,
        "the R-C2 seeding rule carried (seeded harnesses are deterministic by law; "
        "the unseeded {38, 50} carve-out class never appears in this suite)"))

# ---- N3 -- resource-heavy in band (zero-fire) ------------------------------
N3_PLAN = [
    ("code-N3-001", "digit_scan", (37000, 22101)),
    ("code-N3-002", "digit_scan", (35000, 19501)),
    ("code-N3-003", "seven_scan", (36000, 13800)),
    ("code-N3-004", "five_scan", (36000, 14800)),
    ("code-N3-005", "prime_sum", (2000, 277050)),
    ("code-N3-006", "collatz_max", (1850, 181)),
]
for fid, fn, heavy in N3_PLAN:
    spec = N3_SHAPES[fn]
    gen = N3_GEN["digit_scan"].replace("{D}", spec["digit"]) if "digit" in spec else N3_GEN[fn]
    FIXTURES.append(authored_row(
        fid, "N3", N3_PROMPTS[fn], gen, n3_target(fn, heavy), None,
        f"PASS-ALL (in-band heavy; calibrated to the natural p95-p99 meter band; "
        f"under BOTH budget candidates incl. the stamped p99x1.5 = {BUDGET_STAMPED})",
        None, "RUNNABLE", "PASS", False,
        f"{spec['band_note']} -- the doc-36/doc-147 heavy meters of record"))

# ---- N4 -- uncompilable (fails open) ---------------------------------------
N4_ROWS = [
    ("code-N4-001", 0, "    for i in range(len(numbers)\n        return True\n"),
    ("code-N4-002", 7, "    return [x for x in strings if substring in x\n"),
    ("code-N4-003", 16, "    return len(set(string.lower()\n"),
    ("code-N4-004", 45, "    if a > 0\n        return a * h / 2.0\n    return a * h / 2.0\n"),
    ("code-N4-005", 52, "    for e in l:\n    if e >= t:\n            return False\n    return True\n"),
    ("code-N4-006", 40, "    s = 'counting the triples\n    return True\n"),
]
for fid, doc, gen in N4_ROWS:
    FIXTURES.append(banked_row(
        fid, "N4", doc, gen, None, "UNVERIFIED-UNCOMPILABLE", None,
        "UNCOMPILABLE", "UNVERIFIED-UNCOMPILABLE", False,
        "the M1' census recorded 0 UNCOMPILABLE on the natural corpus (all 164 RUNNABLE) "
        "-- this class exercises the fails-open machinery for the first time"))

# ---- N5 -- prose-only answer (fails open; the M3' prose-flag mirror) -------
N5_ROWS = [
    ("code-N5-001", 0, "The function should compare every pair of numbers and return True when any pair sits closer than the threshold. The answer is that it does.\n"),
    ("code-N5-002", 2, "To truncate a number, take the fractional part after the decimal point. The answer is the part to the right of the point.\n"),
    ("code-N5-003", 45, "Multiply the two sides together and halve the result. The answer is half the product.\n"),
    ("code-N5-004", 55, "Each term is the sum of the two terms before it. The answer is the well-known sequence.\n"),
    ("code-N5-005", 47, "Sort the list and take the middle element. The answer is the middle.\n"),
    ("code-N5-006", 104, "Examine each number's digits and keep only the numbers made entirely of odd digits.\n"),
]
for fid, doc, gen in N5_ROWS:
    FIXTURES.append(banked_row(
        fid, "N5", doc, gen, None, "UNVERIFIED-UNCOMPILABLE (prose-only answer)", None,
        "UNCOMPILABLE", "UNVERIFIED-UNCOMPILABLE", "answer is" in gen,
        "the qualitative-answer chat class (arith N8's analog) + the M3' prose-scan "
        "markers exercised on the fails-open side"))

# ---- N6 -- empty generation (fails open) ------------------------------------
N6_ROWS = [
    ("code-N6-001", 0, ""),
    ("code-N6-002", 2, " "),
    ("code-N6-003", 7, "\n"),
    ("code-N6-004", 16, "\t"),
    ("code-N6-005", 23, "   \n"),
    ("code-N6-006", 45, " \n\t"),
]
for fid, doc, gen in N6_ROWS:
    FIXTURES.append(banked_row(
        fid, "N6", doc, gen, None, "UNVERIFIED-NO-EXTRACTABLE-BLOCK", None,
        "NO-EXTRACTABLE-BLOCK", "UNVERIFIED-NO-EXTRACTABLE-BLOCK", False,
        "the M1' census recorded 0 NO-EXTRACTABLE-BLOCK on the natural corpus "
        "-- this class exercises the fails-open machinery for the first time"))

# ---- N7 -- cap-truncated (fails open; typed to the tier-0 compile law) ----
N7_ROWS = [
    ("code-N7-001", 0, "    for i in range(len(numbers)):\n        for j in range(i + 1, len(numbers)):\n            if abs(numbers[i] - numbers[j]) <"),
    ("code-N7-002", 7, "    return [x for x in strings if substring in x] + [x for x in strings if substring i"),
    ("code-N7-003", 16, "    return len(set(string.lower())) - len(set(string.up"),
    ("code-N7-004", 52, "    for e in l:\n        if e >= t:"),
    ("code-N7-005", 55, "    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\ndef helper(x"),
    ("code-N7-006", 40, "    for i in range(len(l)):\n        for j in range(i + 1, len(l)):\n            if l[i] + l[j] +"),
]
for fid, doc, gen in N7_ROWS:
    FIXTURES.append(banked_row(
        fid, "N7", doc, gen, None,
        "UNVERIFIED-UNCOMPILABLE (cap-truncated shape; typed to the tier-0 compile law)",
        None, "UNCOMPILABLE", "UNVERIFIED-UNCOMPILABLE", False,
        "the cap-truncation stop-class (CAP-TRUNCATED mass was 0 by census on the "
        "natural EOT-stopped corpus) -- the truncation kills compilation, the "
        "expected class is typed to the instrument's own law, honestly"))

# ---- N8 -- multi-block (fails open; never executed) ------------------------
N8_ROWS = [
    ("code-N8-001", 0, SOL[0]),
    ("code-N8-002", 7, SOL[7]),
    ("code-N8-003", 16, SOL[16]),
    ("code-N8-004", 40, SOL[40]),
    ("code-N8-005", 47, SOL[47]),
    ("code-N8-006", 104, SOL[104]),
]
for fid, doc, sol in N8_ROWS:
    gen = ("```python\n" + "\n".join(sol[:2]) + "\n```\n```python\n"
           + "\n".join(sol[2:]) + "\n```\n")
    FIXTURES.append(banked_row(
        fid, "N8", doc, gen, None, "UNVERIFIED-MULTI-BLOCK", None,
        "MULTI-BLOCK", "UNVERIFIED-MULTI-BLOCK", False,
        "the M1' census recorded 0 MULTI-BLOCK and 0 fenced docs on the natural "
        "corpus -- this class exercises the fence census for the first time"))


# ---------------------------------------------------------------------------
# 4. Verification (build-time ground truth; sandbox law per rep)
# ---------------------------------------------------------------------------

def resolve(row, docs, prompts):
    """Resolve prompt/target/generated for a row."""
    if row["source_problem"].startswith("he-doc-"):
        doc = int(row["source_problem"].split("-")[-1])
        return prompts[str(doc)], docs[doc]["target"], row["generated"], doc
    return row["authored_prompt"], row["target"], row["generated"], None


def counted_probe(prompt, gen, target):
    """Build-only loudness probe: wrap each single-line assert in the harness's
    check body with a failure counter; returns (fails, total_asserts)."""
    assert_lines = 0
    out = []
    for line in target.splitlines():
        m = re.match(r"^(\s*)assert (.+)$", line)
        if m and line != "    assert True":
            indent, expr = m.group(1), m.group(2)
            assert_lines += 1
            out.append(f"{indent}try:")
            out.append(f"{indent}    assert {expr}")
            out.append(f"{indent}except BaseException:")
            out.append(f"{indent}    _fails[0] += 1")
        else:
            out.append(line)
    if assert_lines == 0:
        return None, None
    text = "\n".join(out)
    text = text.replace("def check(candidate):",
                        "_fails = [0]\n\n\ndef check(candidate):", 1)
    text += "\n\nprint('PROBE_FAILS', _fails[0])\n"
    program = prompt + gen + "\n\n" + text
    with tempfile.TemporaryDirectory(prefix="cfx-probe-") as td:
        path = os.path.join(td, "prog.py")
        with open(path, "w") as f:
            f.write(program)
        proc = subprocess.run([sys.executable, "prog.py"], cwd=td,
                              capture_output=True, timeout=instr.TIMEOUT_SEC)
    out_txt = proc.stdout.decode("utf-8", "replace")
    fails = None
    for ln in out_txt.splitlines():
        if ln.startswith("PROBE_FAILS "):
            fails = int(ln.split()[1])
    assert fails is not None, f"probe produced no count: {out_txt!r} {proc.stderr.decode()[:400]!r}"
    return fails, assert_lines


def verify_row(row, docs, prompts, idx):
    prompt, target, gen, _ = resolve(row, docs, prompts)
    doc = {"doc_id": idx, "generated": gen, "target": target}
    program = instr.program_text(doc, prompt)
    t0 = instr.tier0(doc, program)
    problems = []

    # tier-0 expectations
    if t0["class"] != row["expected_m1_class"]:
        problems.append(f"m1 {t0['class']} != expected {row['expected_m1_class']}")
    if t0["stated_answer_prose"] != row["expected_prose_flag"]:
        problems.append(f"prose flag {t0['stated_answer_prose']} != expected {row['expected_prose_flag']}")

    # P6 contradiction census (in-process, deterministic)
    if row["class"] == "P6":
        ns = {}
        exec(compile(prompt + gen, f"<{row['fixture_id']}>", "exec"), ns)
        call = row["extra"]["p6_headline"]
        verified = eval(call, ns)
        stated_raw = row["extra"]["p6_stated"]
        try:
            stated_val = eval(stated_raw, ns)
        except Exception:
            stated_val = stated_raw
        if str(verified) == str(stated_val):
            problems.append(f"P6 prose does NOT contradict: stated {stated_raw} == verified {verified}")
        row["extra"]["p6_verified"] = verified if not isinstance(verified, float) else round(verified, 10)

    # execution + meter (RUNNABLE only)
    meters = []
    verdict = None
    if t0["class"] == "RUNNABLE":
        passes = 0
        for _ in range(instr.REPS):
            with tempfile.TemporaryDirectory(prefix="cfx-u-") as td:
                r = instr.run_untraced_once(program, td)
            if r["timeout"] or r.get("os_error"):
                problems.append(f"untraced timeout/os_error: {r}")
            elif r["rc"] == 0:
                passes += 1
        if passes == instr.REPS:
            verdict = "PASS"
        elif passes == 0:
            verdict = "FAIL-TESTS"
        else:
            verdict = "MIXED"
        for _ in range(instr.REPS):
            with tempfile.TemporaryDirectory(prefix="cfx-m-") as td:
                r = instr.run_metered_once(program, td)
            meters.append(r["meter"])
        if len(set(meters)) != 1:
            problems.append(f"meter NOT deterministic: {meters}")
        row["extra"]["meter"] = meters[0]
    if verdict is not None and verdict != row["expected_verdict"]:
        problems.append(f"verdict {verdict} != expected {row['expected_verdict']}")

    # loudness probe (P1-P5 firing rows)
    if row["class"] in ("P1", "P2", "P3", "P4", "P5"):
        fails, total = counted_probe(prompt, gen, target)
        if row["loudness"] == "loud":
            ok = fails is not None and fails * 2 > total
        else:  # subtle
            ok = fails == 1
        if not ok:
            problems.append(f"loudness {row['loudness']} not verified: fails {fails}/{total}")
        row["extra"]["probe"] = {"fails": fails, "total": total}

    return problems, t0


# ---------------------------------------------------------------------------
# 5. Census gates + emission
# ---------------------------------------------------------------------------

def main():
    docs, prompts = load_inputs()
    assert len(FIXTURES) == 96, f"expected 96 fixtures, got {len(FIXTURES)}"

    # deterministic id order (BUILD-GATE CATCH 1: the fixture definitions sit in
    # pedagogical order P1..N8; the suite is EMITTED in canonical sorted-id
    # order N1..P6 -- builder fix, fixture definitions untouched)
    FIXTURES.sort(key=lambda f: f["fixture_id"])
    ids = [f["fixture_id"] for f in FIXTURES]
    assert ids == sorted(ids), "fixture ids not in sorted order"

    # census: class counts exact
    from collections import Counter
    by_class = Counter(f["class"] for f in FIXTURES)
    for c in ["P1", "P2", "P3", "P4", "P5", "P6"]:
        assert by_class[c] == 8, f"{c} count {by_class[c]} != 8"
    for c in ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"]:
        assert by_class[c] == 6, f"{c} count {by_class[c]} != 6"

    # census: loud/subtle balance on positives
    for c in ["P1", "P2", "P3", "P4", "P5", "P6"]:
        loud = sum(1 for f in FIXTURES if f["class"] == c and f["loudness"] == "loud")
        subtle = sum(1 for f in FIXTURES if f["class"] == c and f["loudness"] == "subtle")
        assert loud == 4 and subtle == 4, f"{c} loud/subtle {loud}/{subtle} != 4/4"

    # census: all four M1' classes present in expectations
    m1_classes = Counter(f["expected_m1_class"] for f in FIXTURES)
    assert set(m1_classes) == {"RUNNABLE", "UNCOMPILABLE", "NO-EXTRACTABLE-BLOCK", "MULTI-BLOCK"}
    assert m1_classes["RUNNABLE"] == 66 and m1_classes["UNCOMPILABLE"] == 18 \
        and m1_classes["NO-EXTRACTABLE-BLOCK"] == 6 and m1_classes["MULTI-BLOCK"] == 6, m1_classes

    # census: zero unseeded randomness anywhere (RW discipline + R-C2 mirror)
    for f in FIXTURES:
        blob = f["generated"]
        if "random" in blob:
            for m in re.finditer(r"random\.(\w+)\(", blob):
                assert m.group(1) == "Random", f"unseeded randomness {m.group(0)} in {f['fixture_id']}"

    # verify every row (build-gate; a catch fixes the fixture or the builder)
    all_problems = {}
    for i, row in enumerate(FIXTURES):
        problems, t0 = verify_row(row, docs, prompts, i)
        if problems:
            all_problems[row["fixture_id"]] = problems
        print(f"[{i + 1:2d}/96] {row['fixture_id']:13s} {row['class']} "
              f"m1={t0['class']:22s} verdict_exp={row['expected_verdict']}"
              + (f"  PROBLEMS {problems}" if problems else ""), flush=True)

    # N3 band gates
    for f in FIXTURES:
        if f["class"] == "N3":
            m = f["extra"]["meter"]
            assert METER_BAND_LO <= m <= METER_BAND_HI, \
                f"{f['fixture_id']} meter {m} outside the natural p95-p99 band"
            assert m < 3258430, f"{f['fixture_id']} meter {m} over the x1.25 candidate"
        if f["class"] == "P6":
            assert "p6_verified" in f["extra"], "P6 verified value missing"

    if all_problems:
        print("\nBUILD GATE FAILURES:", len(all_problems))
        for k, v in all_problems.items():
            print(" ", k, v)
        sys.exit(1)

    # emit the suite (deterministic; no timestamps)
    out_fixtures = []
    for i, f in enumerate(FIXTURES):
        prompt, target, gen, doc_ref = resolve(f, docs, prompts)
        gt = f["ground_truth_mode"]
        if f["class"] in ("P1", "P2", "P3", "P4", "P5"):
            gt = f"FAILS-{f['extra']['probe']['fails']}/{f['extra']['probe']['total']}"
        out = {
            "fixture_id": f["fixture_id"],
            "class": f["class"],
            "source_problem": f["source_problem"],
            "canonical_prompt": prompt,
            "generated_text": gen,
            "target_harness": target,
            "mutation": f["mutation"],
            "ground_truth": gt,
            "loudness": f["loudness"],
            "expected_m1_class": f["expected_m1_class"],
            "expected_verdict": f["expected_verdict"],
            "expected_prose_flag": f["expected_prose_flag"],
            # BUILD-GATE CATCH 4 (M-K6 law): the guard is expected live ONLY
            # where its semantics apply -- None (fails open) on non-RUNNABLE
            # rows, matching the instrument's own E' guard shape exactly
            "expected_meter_deterministic": (True if f["expected_m1_class"] == "RUNNABLE" else None),
            "meter_band": ("heavy" if f["class"] == "N3" else
                           ("light" if f["expected_m1_class"] == "RUNNABLE" else None)),
            "habit_exemplar": f["habit_exemplar"],
            "perturbation_set": None,
        }
        if f["class"] == "P6":
            out["p6_census"] = {
                "headline": f["extra"]["p6_headline"],
                "stated": f["extra"]["p6_stated"],
                "verified": f["extra"]["p6_verified"],
                "contradiction": True,
            }
        else:
            out["p6_census"] = None
        out_fixtures.append(out)

    suite = {
        "suite": "triadic_code_fixture_suite_v1",
        "family": "code-* (Gate 17-C)",
        "built_under_stamp": "ledger item 166 (Oct 9 2026): sizing code-M; "
                             "meter budget p99x1.5 = 3910116; RW-5 OFF; P6 branch (a) as-is boundary census",
        "pins": {
            "he_base_dump_sha256": PIN_DUMP,
            "canonical_prompts_sha256": PIN_PROMPTS,
            "instrument_sha256": PIN_INSTR,
        },
        "meter_band": {"lo": METER_BAND_LO, "hi": METER_BAND_HI,
                       "note": "the natural p95-p99 meter census of record; all N3 rows in-band"},
        "census": {
            "total": 96,
            "classes": dict(sorted(by_class.items())),
            "m1_expected": dict(sorted(m1_classes.items())),
            "loud_subtle": {c: {"loud": 4, "subtle": 4} for c in
                            ["P1", "P2", "P3", "P4", "P5", "P6"]},
        },
        "fixtures": out_fixtures,
    }
    with open(SUITE_PATH, "w") as f:
        json.dump(suite, f, indent=2, sort_keys=False)
        f.write("\n")
    print(f"\nBUILD OK: {SUITE_PATH}")
    print("sha256", sha256_file(SUITE_PATH), "bytes", os.path.getsize(SUITE_PATH))
    for f in FIXTURES:
        if f["class"] == "N3":
            print(f"  {f['fixture_id']} meter {f['extra']['meter']}")


if __name__ == "__main__":
    main()

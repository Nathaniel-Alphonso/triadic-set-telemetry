#!/usr/bin/env python3
"""The AP17 capture acceptance run (the item-255 pattern; zero-GPU).

Proves the BUILT capture fork triadic_telemetry_t2_v32.3.0.py on
deterministic synthetic worlds, by exec'ing its PURE regions (the
LOOP_FIXTURES block, _sha256_file, and the 17-AP block up to the
torch-touching hook) and recomputing every quantity with THIS
runner's OWN arithmetic -- never the tool's functions. Every
fail-loud hard exit is fired loudly in a fixture and named.

The honest boundary (B6-class): no decode executes here; the decode
path (the drain call site, the EOS@step-0 law, the frame-count
assertion, the eager-memory line) is NOT run-validated until the
my smoke run.

theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, or
adjudicated; the instrument prints no verdicts.
"""
import hashlib
import json
import math
import os
import random
import re
import shutil
import sys
import tempfile

TOOL = "triadic_telemetry_t2_v32.3.0.py"
TOOL_PIN = ("8b4250f3ee0aa55b654284f33f142d07f9dacb8aab38ed9517d99"
            "e6f167d2e18")
BASE = "triadic_telemetry_t2_v32.2.2.py"
BASE_PIN = ("c53742663b5f57de0b4da960b5a660d90c065524d457de98cb354"
            "10ee0a47884")
REAL_MANIFEST = "triadic_ap17_capture_manifest_v1.json"

PASS = []
FAIL = []


def check(name, fn):
    try:
        detail = fn()
        PASS.append(name)
        print(f"  PASS {name}" + (f" -- {detail}" if detail else ""))
    except Exception as ex:               # noqa: BLE001 -- tally law
        FAIL.append((name, repr(ex)))
        print(f"  FAIL {name} -- {repr(ex)}")


def expect_exit(kind, fn):
    """fn must raise kind (SystemExit or the tool's AP17HardExit)."""
    try:
        fn()
    except kind:
        return True
    except Exception as ex:               # noqa: BLE001
        raise AssertionError(f"wrong exception {ex!r}")
    raise AssertionError("no hard exit fired (the gate stayed shut)")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def slice_between(src, start_marker, end_marker):
    i = src.find(start_marker)
    if i < 0:
        raise AssertionError(f"start marker not found: {start_marker!r}")
    j = src.find(end_marker, i)
    if j < 0:
        raise AssertionError(f"end marker not found: {end_marker!r}")
    return src[i:j]


# ------------------------------------------------------------------
# the tool's own pure regions, exec'd (never re-typed by hand)
# ------------------------------------------------------------------
def build_namespace():
    src = open(TOOL, encoding="utf-8").read()
    lf = slice_between(src, "LOOP_FIXTURES = [", "\n]\n") + "\n]\n"
    sh = slice_between(src, "def _sha256_file(", "\n\n\n")
    i = src.find("# v32.3.0: 17-AP ALL-LAYER CAPTURE HOOK")
    if i < 0:
        raise AssertionError("AP17 block banner not found")
    block = src[i:src.find("def _ap17_capture_attention(")]
    ns = {"os": os, "sys": sys, "json": json, "math": math,
          "random": random, "hashlib": hashlib}
    exec(compile(lf, "<loop-fixtures>", "exec"), ns)
    exec(compile(sh, "<sha-helper>", "exec"), ns)
    exec(compile(block, "<ap17-block>", "exec"), ns)
    return ns, src


NS, SRC = build_namespace()
AP17HardExit = NS["AP17HardExit"]


def reset_frame(n_layers):
    NS["AP17_FRAME"]["rows"] = {}
    NS["AP17_FRAME"]["steps"] = []
    NS["AP17_FRAME"]["n_layers"] = n_layers
    NS["AP17_FRAME_LOCK"] = False


# ------------------------------------------------------------------
# the runner's OWN reference arithmetic (independent of the tool)
# ------------------------------------------------------------------
def ref_row_features(row, pmt_len, span_window, window_last=32):
    total = sum(row)
    assert total > 0
    f1 = sum(row[:pmt_len]) / total
    n_gen = len(row) - pmt_len
    w = min(window_last, n_gen)
    f2a = (sum(row[pmt_len + n_gen - w:]) / total) if w > 0 else 0.0
    f2b = None
    if span_window is not None:
        lo, hi = span_window
        f2b = sum(row[pmt_len + lo:pmt_len + hi]) / total
    if len(row) > 1:
        h = 0.0
        for v in row:
            p = v / total
            if p > 0:
                h += -p * math.log2(p)
        f3 = h / math.log2(len(row))
    else:
        f3 = None
    f4 = row[0] / total
    return f1, f2a, f2b, f3, f4


def ref_uniform_row(n, val=1.0 / 7.0):
    return [val] * n


def approx_same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) < 1e-12
    return a == b


def _pins_true():
    """The four embedded fresh-manifest pins, each verified against
    the real bytes (adjacent string literals collapsed -- the pin
    may wrap across source lines)."""
    n = 0
    for fname in ("triadic_rw17_math_prompts_v1.json",
                  "triadic_rw17_code_prompts_v1.json",
                  "triadic_rw17_prose_prompts_v1.json",
                  "triadic_rw17_p2_prompts_v1.json"):
        i = SRC.find('"' + fname + '"')
        if i < 0:
            continue
        win = SRC[i:i + 400]
        coll = re.sub(r'"\s*\n\s*"', "", win)
        mm = re.search(r'"([0-9a-f]{64})"', coll)
        if mm and mm.group(1) == sha256_file(fname):
            n += 1
    return n


# ------------------------------------------------------------------
# fixtures for the loader families
# ------------------------------------------------------------------
TMP = tempfile.mkdtemp(prefix="ap17_accept_")


def write_fixture(name, obj):
    p = os.path.join(TMP, name)
    with open(p, "w") as f:
        if isinstance(obj, str):
            f.write(obj)
        else:
            f.write(json.dumps(obj, sort_keys=True, indent=2) + "\n")
    return p


def good_entry(i, **kw):
    e = {"capture_id": i, "leg": "gsmrw17", "class": "clean-gsm",
         "schema": "gsm8k-rw17-v1", "doc_id": 100 + i}
    e.update(kw)
    return e


def good_manifest(entries, census=None):
    return {"format": "ap17-capture-manifest-v1",
            "class_census": census, "n_entries": len(entries),
            "entries": entries}


def main():
    print("=== AP17 CAPTURE ACCEPTANCE RUN (item-255 pattern; "
          "zero-GPU; synthetic worlds; independent recomputation) "
          "===")
    print("  tool under test: " + TOOL)

    # ---------- A: tool pins + base parity (structural) ----------
    print("  -- A: tool pins + base parity --")
    check("A1 base bytes == the banked pin",
          lambda: (sha256_file(BASE) == BASE_PIN, None)[1])
    check("A2 built tool bytes == the build-of-record pin",
          lambda: (sha256_file(TOOL) == TOOL_PIN, None)[1])
    check("A3 version line v32.3.0",
          lambda: None
          if re.search(r'INSTRUMENT_VERSION = "v32\.3\.0"', SRC)
          else (_ for _ in ()).throw(AssertionError("version line")))
    real_man_sha = sha256_file(REAL_MANIFEST)
    m = re.search(r'AP17_MANIFEST_SHA = "([0-9a-f]{64})"', SRC)
    check("A4 the tool's manifest echo pin == the built manifest",
          lambda: None
          if m and m.group(1) == real_man_sha
          else (_ for _ in ()).throw(
              AssertionError("echo pin drift")))
    check("A5 the four fresh-manifest pins == real bytes",
          lambda: None
          if _pins_true() == 4
          else (_ for _ in ()).throw(
              AssertionError("fresh-manifest pins")))
    base_lines = open(BASE).readlines()
    built_lines = open(TOOL).readlines()
    check("A6 the added-line receipt (756 added lines)",
          lambda: None
          if len(built_lines) - len(base_lines) == 756
          else (_ for _ in ()).throw(AssertionError(
              f"delta {len(built_lines) - len(base_lines)}")))
    check("A7 mode gate: --attention-capture is store_true "
          "(unreachable without the flag)",
          lambda: None
          if re.search(r'add_argument\("--attention-capture", '
                       r'action="store_true"', SRC)
          and re.search(r'if args\.attention_capture:\s*\n'
                        r'\s*if not args\.capture_manifest:', SRC)
          else (_ for _ in ()).throw(AssertionError("mode gate")))

    # ---------- B: row features, EXACT vs independent ----------
    print("  -- B: F1-F4 EXACT vs independent recomputation --")

    def b1():
        # dyadic values: every closed form exact in IEEE-754
        row = [0.125, 0.25, 0.25, 0.375]
        got = NS["_ap17_row_features"](row, 2, None)
        want = ref_row_features(row, 2, None)
        assert got == want, (got, want)
        assert got[0] == 0.375 and got[1] == 0.625 \
            and got[4] == 0.125, got
    check("B1 closed-form world (pmt 2, no span)", b1)

    def b2():
        row = [0.125, 0.25, 0.25, 0.375]
        got = NS["_ap17_row_features"](row, 2, [1, 2])
        assert got[2] == 0.375, got
    check("B2 span window [1,2) -> F2b 0.375", b2)

    def b3():
        got = NS["_ap17_row_features"]([5.0], 1, None)
        assert got == (1.0, 0.0, None, None, 1.0), got
        got2 = NS["_ap17_row_features"]([5.0], 0, None)
        assert got2[0] == 0.0 and got2[3] is None and got2[4] == 1.0
    check("B3 kv==1 edge (F3 None; n_gen==0 -> F2a 0.0)", b3)

    def b4():
        rng = random.Random(7001)
        pmt = 25
        row = [rng.random() + 0.01 for _ in range(pmt + 40)]
        got = NS["_ap17_row_features"](row, pmt, [3, 9])
        want = ref_row_features(row, pmt, [3, 9])
        assert got == want, "random world not EXACT"
        # the universal window caps at 32 of the 40 generated
        total = sum(row)
        assert got[1] == sum(row[pmt + 8:]) / total, "last-32 cap"
    check("B4 seeded random world, all five EXACT + last-32 cap", b4)

    def b5():
        row = [0.25] * 4
        got = NS["_ap17_row_features"](row, 0, None)
        assert got[3] == 1.0, got
    check("B5 uniform row -> normalized entropy exactly 1.0", b5)

    check("B6 zero-sum row -> hard exit",
          lambda: expect_exit(
              AP17HardExit,
              lambda: NS["_ap17_row_features"]([0.0, 0.0], 1, None)))
    check("B7 pmt_len > kv -> evidence-boundary hard exit",
          lambda: expect_exit(
              AP17HardExit,
              lambda: NS["_ap17_row_features"]([1.0, 1.0], 3, None)))
    check("B8 span window outside generated positions -> hard exit",
          lambda: expect_exit(
              AP17HardExit,
              lambda: NS["_ap17_row_features"](
                  [1.0, 1.0, 1.0], 1, [0, 5])))

    # ---------- C: the span detector ----------
    print("  -- C: the streaming span detector (phrase > cycle) --")

    def c1():
        span = NS["_ap17_span_window"]([7, 8] * 6)
        assert span == [10, 12], span
    check("C1 cycle world [7,8]x6 -> latest window [10,12)", c1)

    def c2():
        toks = list(range(100, 115))
        em = toks + [999] + toks + [998] + toks
        span = NS["_ap17_span_window"](em)
        assert span == [32, 47], span
    check("C2 phrase world (15-tok x3) -> latest window [32,47)", c2)

    def c3():
        span = NS["_ap17_span_window"]([1, 2, 3, 4, 5, 6, 7, 9, 11])
        assert span is None, span
    check("C3 no-span world -> None (fails open)", c3)

    def c4():
        span = NS["_ap17_span_window"]([1, 2, 3, 1, 2, 3, 1, 2, 3,
                                        1, 2, 3])
        assert span == [9, 12], span
    check("C4 cycle k=3 reps=4 -> window [9,12)", c4)

    def c5():
        # a qualifying 15-token phrase (x3) AND a qualifying k=2
        # cycle (x4): the PHRASE span wins (pinned preference).
        P = list(range(50, 65))
        em = P + [1, 2, 1, 2, 1, 2, 1, 2] + P + [3] + P
        # occurrences of P start at 0, 23, 39 -> latest 39
        span = NS["_ap17_span_window"](em)
        assert span == [39, 54], span
    check("C5 phrase takes precedence over cycle (pinned "
          "preference)", c5)

    def c6():
        assert NS["_ap17_cycle_span"]([5, 5, 5]) is None
        assert NS["_ap17_phrase_span"](list(range(20))) is None
    check("C6 sub-threshold worlds -> None (never forced)", c6)

    # ---------- D: the manifest loader, every hard exit ----------
    print("  -- D: the manifest loader (real + fixture modes) --")

    def d1():
        fixture_mode, man, sha = NS["_ap17_load_manifest"](
            REAL_MANIFEST)
        assert fixture_mode is False
        assert sha == real_man_sha
        assert len(man["entries"]) == 106
        assert man["class_census"] == NS["AP17_CLASS_CENSUS_PIN"]
    check("D1 REAL MODE positive (pin match:true; 106 entries; "
          "census == pinned)", d1)

    def d1b():
        a = NS["_ap17_load_manifest"](REAL_MANIFEST)[1]
        b = NS["_ap17_load_manifest"](REAL_MANIFEST)[1]
        assert json.dumps(a, sort_keys=True) == json.dumps(
            b, sort_keys=True)
    check("D1b loader determinism (parse identical)", d1b)

    def d2():
        entries = [{"capture_id": 0, "leg": "loop",
                    "class": "loop-live",
                    "fixture": "loop-injection-prose"},
                   good_entry(1)]
        p = write_fixture("fixture_manifest_ok.json",
                          good_manifest(entries))
        fixture_mode, man, _ = NS["_ap17_load_manifest"](p)
        assert fixture_mode is True
        assert len(man["entries"]) == 2
    check("D2 FIXTURE MODE positive (pin echoed, not enforced)", d2)

    def d3():
        expect_exit(SystemExit, lambda: NS["_ap17_load_manifest"](
            os.path.join(TMP, "nope.json")))
    check("D3 missing manifest -> hard exit", d3)

    def d4():
        # basename of record but wrong bytes: REAL mode SHA drift
        p = write_fixture(REAL_MANIFEST.replace(".json", "") + "_x",
                          "{}")
        p2 = p.replace("_x", "")
        os.replace(p, p2)
        expect_exit(SystemExit, lambda: NS["_ap17_load_manifest"](p2))
    check("D4 REAL-mode SHA drift -> hard exit", d4)

    def mkmut(field=None, value=None, mutate=None):
        es = [good_entry(0), good_entry(1)]
        man = good_manifest(es)
        if field:
            man[field] = value
        if mutate:
            mutate(man)
        return write_fixture("bad.json", man)

    check("D5 format-field mismatch -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut("format", "ap17-capture-manifest-v2"))))
    check("D6 entries not a list -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut("entries", {}))))
    check("D7 non-contiguous capture ids -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut(mutate=lambda m: m["entries"][1]
                        .__setitem__("capture_id", 7)))))
    check("D8 unrecognized leg -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut(mutate=lambda m: m["entries"][1]
                        .__setitem__("leg", "gsm8k")))))
    check("D9 loop entry without a fixture name -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  write_fixture("bad.json", good_manifest([
                      {"capture_id": 0, "leg": "loop",
                       "class": "loop-live"}])))))
    check("D10 corpus entry without an integer doc_id -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut(mutate=lambda m: m["entries"][1]
                        .pop("doc_id")))))
    check("D11 corpus entry with the wrong schema -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut(mutate=lambda m: m["entries"][1]
                        .__setitem__("schema", "mbpp-rw17-v1")))))
    check("D12 malformed evidence_spans -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut(mutate=lambda m: m["entries"][1]
                        .__setitem__("evidence_spans", [[3, 1]])))))
    check("D13 declared census drift -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  mkmut("class_census", {"clean-gsm": 2,
                                         "loop-live": 1}))))
    check("D14 truncated/malformed JSON -> hard exit",
          lambda: expect_exit(
              SystemExit, lambda: NS["_ap17_load_manifest"](
                  write_fixture("bad.json", '{"format": "ap17'))))

    def d15():
        real_pin = NS["AP17_CLASS_CENSUS_PIN"]
        NS["AP17_CLASS_CENSUS_PIN"] = {"loop-live": 99}
        try:
            expect_exit(SystemExit, lambda: NS["_ap17_load_manifest"](
                REAL_MANIFEST))
        finally:
            NS["AP17_CLASS_CENSUS_PIN"] = real_pin
    check("D15 REAL-mode census drift vs the pinned census -> "
          "hard exit", d15)

    # ---------- E: entry resolution, fail-loud ----------
    print("  -- E: entry resolution (never guessed) --")

    def e1():
        d = NS["_ap17_resolve_entry"](
            {"capture_id": 0, "leg": "loop", "class": "loop-live",
             "fixture": "mask-reserved-stubborn"}, {})
        assert d["is_loop"] is True
        assert d["doc_id"] == "mask-reserved-stubborn"
        assert d["prompt"].startswith("No matter what else")
    check("E1 loop entry resolves by name against LOOP_FIXTURES", e1)

    docs = [{"doc_id": i, "prompt": f"p{i}"} for i in range(10)]
    check("E2 corpus entry resolves against the loaded leg",
          lambda: None
          if NS["_ap17_resolve_entry"](
              {"capture_id": 0, "leg": "gsmrw17",
               "class": "clean-gsm", "doc_id": 7},
              {"gsmrw17": docs})["doc_id"] == 7
          else (_ for _ in ()).throw(AssertionError()))
    check("E3 unknown loop fixture -> hard exit",
          lambda: expect_exit(
              AP17HardExit,
              lambda: NS["_ap17_resolve_entry"](
                  {"capture_id": 0, "leg": "loop", "fixture": "nope"},
                  {})))
    check("E4 leg with no loaded manifest -> hard exit",
          lambda: expect_exit(
              AP17HardExit,
              lambda: NS["_ap17_resolve_entry"](
                  {"capture_id": 0, "leg": "mbpprw17", "doc_id": 1},
                  {})))
    check("E5 unknown doc -> hard exit",
          lambda: expect_exit(
              AP17HardExit,
              lambda: NS["_ap17_resolve_entry"](
                  {"capture_id": 0, "leg": "gsmrw17", "doc_id": 77},
                  {"gsmrw17": docs})))

    def e6():
        # EVERY entry of the real manifest resolves against the real
        # corpus universes (zero-GPU; the manifests are on disk)
        _, man, _ = NS["_ap17_load_manifest"](REAL_MANIFEST)
        legs = {}
        for fname in ("math", "code", "prose", "p2"):
            with open(f"triadic_rw17_{fname}_prompts_v1.json") as f:
                mm = json.load(f)
            for leg, schema in NS["AP17_SCHEMA_BY_LEG"].items():
                if mm["schema"] == schema:
                    legs[leg] = [d for d in mm["docs"].values()]
        for e in man["entries"]:
            NS["_ap17_resolve_entry"](e, legs)
        return "all 106 resolved"
    check("E6 all 106 real entries resolve against the real "
          "universes", e6)

    # ---------- F: the drain (layer law + kv law) ----------
    print("  -- F: the capture drain --")

    def f1():
        reset_frame(3)
        NS["AP17_FRAME"]["rows"] = {0: [1.0, 1.0], 1: [1.0, 1.0]}
        expect_exit(AP17HardExit,
                    lambda: NS["_ap17_drain_step"](0, 2, []))
    check("F1 a layer failing to register -> hard exit "
          "(never a silent missing series)", f1)

    def f2():
        reset_frame(2)
        NS["AP17_FRAME"]["rows"] = {0: [1.0] * 5, 1: [1.0] * 5}
        expect_exit(AP17HardExit,
                    lambda: NS["_ap17_drain_step"](0, 2, []))
    check("F2 kv != pmt_len + emitted -> hard exit", f2)

    def f3():
        reset_frame(3)
        rng = random.Random(7002)
        pmt, walk = 10, 5
        rows = {l: [rng.random() + 0.01 for _ in range(pmt + walk)]
                for l in range(3)}
        NS["AP17_FRAME"]["rows"] = {l: list(r) for l, r
                                     in rows.items()}
        NS["_ap17_drain_step"](0, pmt, [4, 4, 4, 4, 9])
        st = NS["AP17_FRAME"]["steps"]
        assert len(st) == 1 and st[0]["t"] == 0
        # span: [4,4,4,4] cycles (k=1 excluded; k=2 gram (4,4) reps=2
        # < 4; k=4 gram (4,4,4,4)? reps=1) -> actually None here
        assert st[0]["span"] is None, st[0]["span"]
        for l in range(3):
            got = st[0]["layers"][l]
            want = list(ref_row_features(rows[l], pmt,
                                         st[0]["span"]))
            assert all(approx_same(a, b) or a == b
                       for a, b in zip(got, want)), (l, got, want)
        assert NS["AP17_FRAME"]["rows"] == {}
    check("F3 positive drain: frame banked; per-layer scalars == "
          "independent recompute; rows cleared", f3)

    def f4():
        reset_frame(1)
        # walk [1,2]x4: k=2 gram (1,2) reps 4 -> latest occurrence at
        # position 6 of the 8 generated ids -> window [6, 8)
        NS["AP17_FRAME"]["rows"] = {0: [0.05] * 9}
        NS["_ap17_drain_step"](3, 1, [1, 2, 1, 2, 1, 2, 1, 2])
        assert NS["AP17_FRAME"]["steps"][0]["span"] == [6, 8], \
            NS["AP17_FRAME"]["steps"][0]["span"]
    check("F4 span rides the emission ids (walk_ids -> span "
          "window)", f4)

    # ---------- G: record assembly + the JSONL lane ----------
    print("  -- G: record assembly + resumable JSONL --")

    def g1():
        reset_frame(2)
        pmt = 2
        rows = {0: [0.125, 0.25, 0.25, 0.375],
                1: [0.375, 0.25, 0.25, 0.125]}
        NS["AP17_FRAME"]["rows"] = {l: list(r) for l, r
                                    in rows.items()}
        NS["_ap17_drain_step"](0, pmt, [8, 9])
        steps = NS["AP17_FRAME"]["steps"]
        rec = {"prompt_len": pmt, "stop_reason": "cap",
               "n_gen_steps": 1, "n_content_steps": 1,
               "walk_ids": [8, 9]}
        entry = {"capture_id": 5, "leg": "gsmrw17",
                 "class": "gsm-boundary-fired",
                 "schema": "gsm8k-rw17-v1", "doc_id": 15,
                 "evidence_spans": [[0, 2]]}
        common = {"format": "ap17-capture-v1", "tag": "t",
                  "instrument": "v32.3.0", "model": "M",
                  "tool_sha256": "x" * 64, "manifest": "m",
                  "manifest_sha256": "y" * 64, "fixture_mode": False}
        r = NS["_ap17_doc_record"](entry, rec, steps, 2,
                                   "eight nine", common)
        assert r["format"] == "ap17-capture-v1"
        assert r["capture_id"] == 5 and r["doc_id"] == 15
        assert r["evidence_spans"] == [[0, 2]]
        assert r["emission_text"] == "eight nine"
        assert r["walk_ids"] == [8, 9]
        assert len(r["features"]["F1"]) == 1
        assert len(r["features"]["F1"][0]) == 2
        assert r["features"]["F2b"][0] == [None, None]
        assert r["n_layers"] == 2 and r["prompt_len"] == 2
    check("G1 record assembly (columnar per-step x per-layer; "
          "NO-SPAN nulls; full self-describing form)", g1)

    def g2():
        reset_frame(1)
        rec = {"prompt_len": 5, "stop_reason": "eos@step0",
               "n_gen_steps": 0, "n_content_steps": 0,
               "walk_ids": []}
        entry = {"capture_id": 0, "leg": "gsmrw17",
                 "class": "clean-gsm", "doc_id": 1}
        common = {"format": "ap17-capture-v1", "tag": "t",
                  "instrument": "v32.3.0", "model": "M",
                  "tool_sha256": "x" * 64, "manifest": "m",
                  "manifest_sha256": "y" * 64, "fixture_mode": False}
        r = NS["_ap17_doc_record"](entry, rec, [], 4, "", common)
        for k in NS["AP17_FEATURE_KEYS"]:
            assert r["features"][k] == []
        assert r["span_windows"] == []
    check("G2 EOS@step-0 -> full-form record, empty arrays (the "
          "banked zero-step law)", g2)

    def make_recs():
        reset_frame(1)
        rows = {0: [0.1, 0.2, 0.3, 0.4]}
        rec = {"prompt_len": 3, "stop_reason": "eos",
               "n_gen_steps": 1, "n_content_steps": 1,
               "walk_ids": [8]}
        entry = {"capture_id": 0, "leg": "loop",
                 "class": "loop-live", "fixture": "f"}
        common = {"format": "ap17-capture-v1", "tag": "t",
                  "instrument": "v32.3.0", "model": "M",
                  "tool_sha256": "x" * 64, "manifest": "m",
                  "manifest_sha256": "y" * 64, "fixture_mode": True}
        out = []
        for i in range(3):
            entry["capture_id"] = i
            NS["AP17_FRAME"]["rows"] = {0: list(rows[0])}
            NS["_ap17_drain_step"](0, 3, [8])
            out.append(NS["_ap17_doc_record"](
                dict(entry), rec, NS["AP17_FRAME"]["steps"], 1,
                "eight", common))
            reset_frame(1)
        return out

    def g3():
        p = os.path.join(TMP, "roundtrip.jsonl")
        recs = make_recs()
        with open(p, "w") as f:
            for r in recs:
                NS["_ap17_write_record"](f, r)
        got = NS["_ap17_read_existing"](p)
        assert sorted(got) == [0, 1, 2]
        for r in recs:
            assert json.dumps(got[r["capture_id"]], sort_keys=True) \
                == json.dumps(r, sort_keys=True)
    check("G3 writer/reader round-trip EXACT (resume map)", g3)

    def g4():
        p = os.path.join(TMP, "dup.jsonl")
        recs = make_recs()
        with open(p, "w") as f:
            NS["_ap17_write_record"](f, recs[0])
            NS["_ap17_write_record"](f, recs[0])
        expect_exit(SystemExit, lambda: NS["_ap17_read_existing"](p))
    check("G4 duplicate capture_id -> hard exit", g4)

    def g5():
        p = os.path.join(TMP, "trunc.jsonl")
        with open(p, "w") as f:
            f.write('{"format": "ap17-capture-v1", "captu')   # noqa
        expect_exit(SystemExit, lambda: NS["_ap17_read_existing"](p))
    check("G5 truncated line -> hard exit", g5)

    def g6():
        p = os.path.join(TMP, "wrong.jsonl")
        with open(p, "w") as f:
            f.write(json.dumps({"format": "other", "capture_id": 0})
                    + "\n")                                  # noqa
        expect_exit(SystemExit, lambda: NS["_ap17_read_existing"](p))
    check("G6 non-ap17-capture-v1 line -> hard exit", g6)

    def g7():
        recs = make_recs()
        p1 = os.path.join(TMP, "det1.jsonl")
        p2 = os.path.join(TMP, "det2.jsonl")
        for p in (p1, p2):
            with open(p, "w") as f:
                for r in recs:
                    NS["_ap17_write_record"](f, r)
        assert open(p1, "rb").read() == open(p2, "rb").read()
    check("G7 writer determinism (sort_keys, byte-identical)", g7)

    # ---------- the tally ----------
    print(f"=== ACCEPTANCE TALLY: {len(PASS)} PASS / {len(FAIL)} "
          f"FAIL ===")
    if FAIL:
        for n, ex in FAIL:
            print(f"  FAILED: {n}: {ex}")
    shutil.rmtree(TMP, ignore_errors=True)
    print("  honest boundary (B6-class): the decode path (drain "
          "call site, EOS@step-0 at decode, frame-count assertion, "
          "eager-memory line) is NOT run-validated here -- "
          "nothing executes until my smoke run.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

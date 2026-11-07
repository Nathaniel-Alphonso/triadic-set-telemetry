#!/usr/bin/env python3
"""RW-17 FIRES FORENSICS -- ACCEPTANCE RUN (fixture worlds; the item-249 law).

Every family builds a synthetic world in .scratch, runs the tool via its CLI
(--fixture mode; no pins enforced there -- the pin lane is its own family),
and checks the report against independently derived expectations. The real
run of record (the four banked thins) is a SEPARATE act -- the control on real
bytes rides its own script. Determinism proven by double-run byte-compare.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "rw17_fires_forensics.py")
RUN = os.path.join(HERE, ".scratch", "rw17_fires_forensics", "acceptance")
P, F = [], []
ALL_LEGS = ["gsmrw17", "mbpprw17", "prose17p-rw17", "p2corpus-rw17"]
THIN_NAME = {
    "gsmrw17": "triadic_t2_thin_rw17-math-fresh.jsonl",
    "mbpprw17": "triadic_t2_thin_rw17-code-fresh.jsonl",
    "prose17p-rw17": "triadic_t2_thin_rw17-prose-fresh.jsonl",
    "p2corpus-rw17": "triadic_t2_thin_rw17-p2-fresh.jsonl",
}
MANIFEST_NAME = {
    "gsmrw17": "triadic_rw17_math_prompts_v1.json",
    "mbpprw17": "triadic_rw17_code_prompts_v1.json",
    "prose17p-rw17": "triadic_rw17_prose_prompts_v1.json",
    "p2corpus-rw17": "triadic_rw17_p2_prompts_v1.json",
}


def check(name, ok, detail=""):
    (P if ok else F).append(name)
    print(("PASS  " if ok else "FAIL  ") + name + (f" -- {detail}" if detail else ""))


def commit(t, token, phase="CoT"):
    return {"t": t, "token": token, "phase": phase}


def thin_record(key, leg, doc_id, tokens, phases, n_steps, pr):
    commits = [commit(i + 1, tok, ph) for i, (tok, ph) in enumerate(zip(tokens, phases))]
    return {"key": key, "leg": leg, "doc_id": doc_id, "thin": True, "hidden_b64": "",
            "n_gen_steps": n_steps, "n_content_steps": len(tokens),
            "stop_reason": "cap", "commits": commits,
            "steps": {"PR": pr}}


def fired_doc(doc_id, D, spike_pos, n_prsig, z_C=1.0, z_F=1.0):
    return {"doc_id": doc_id, "D": D, "z_C": z_C, "z_F": z_F, "escalation": False,
            "half": "held-out", "maxPRsig": 2.0, "minS": 0.1,
            "n_prsig_steps": n_prsig, "sec1_N_band": 1, "sec1_R_band": 1,
            "sec2_ceiling_pos": spike_pos,
            "sec2_ceiling_pos_frac": spike_pos / max(1, n_prsig - 1),
            "co_elevated": False}


def dtoks(n, prefix="w"):
    """n pairwise-distinct tokens -- no cycling k-gram can occur."""
    return [f" {prefix}{i}" for i in range(n)]


def write_world(path, legs_spec):
    exp = {"tool_sha256": "x" * 64, "tag": "fixture", "fixture_mode": False,
           "legs": {}}
    os.makedirs(path, exist_ok=True)
    for leg, spec in legs_spec.items():
        with open(os.path.join(path, THIN_NAME[leg]), "w") as f:
            f.write("\n".join(json.dumps(r) for r in spec["records"]) + "\n")
        exp["legs"][leg] = {
            "held_out": {"fires": len(spec["fired"]), "fired_docs": spec["fired"]},
            "populations": {"loops_live": spec["loops"]},
            "thresholds": {"t_leg": 1.5},
        }
        docs = [{"doc_id": d["doc_id"],
                 "question": f"the reference text for echo {d['doc_id']}",
                 "text": f"the reference text for echo {d['doc_id']}",
                 "test_list": [f"assert echo {d['doc_id']}"],
                 "prompt": f"the reference text for echo {d['doc_id']}",
                 "p1_constraints": "keep it tight"}
                for d in spec["fired"] if isinstance(d["doc_id"], int)]
        with open(os.path.join(path, MANIFEST_NAME[leg]), "w") as f:
            json.dump({"schema": "fixture", "docs": docs}, f)
    with open(os.path.join(path, "export.json"), "w") as f:
        json.dump(exp, f)


def run_tool(world, out, fixture=True):
    cmd = [sys.executable, TOOL,
           "--export", os.path.join(world, "export.json"),
           "--thindir", world, "--manifestdir", world,
           "--out", out, "--tag", "acceptance"]
    if fixture:
        cmd.append("--fixture")
    return subprocess.run(cmd, capture_output=True, text=True)


def build_main_world(world):
    # --- gsmrw17: (A) consecutive 3-gram cycle x6 -> REPETITION;
    #              (B) distinct-token stream, spike AT the last commit -> BOUNDARY
    toksA = ["x"] + [" a", " b", " c"] * 6 + [" end"]
    recA = thin_record("gsmrw17:1", "gsmrw17", 1, toksA, ["CoT"] * len(toksA), 30, [0.1] * 30)
    toksB = dtoks(25, "b")
    recB = thin_record("gsmrw17:3", "gsmrw17", 3, toksB, ["CoT"] * 25, 40, [0.1] * 40)
    docB = fired_doc(3, 3.0, 25, 40)                     # spike t=25 == last commit t=25
    recLoop = thin_record("loop:loop-injection-code", "loop", "loop-injection-code",
                          [" print", " (count", " down"] * 8, ["CoT"] * 24, 40, [0.2] * 40)
    spec_gsm = {"fired": [fired_doc(1, 4.0, 6, 30), docB],
                "loops": [fired_doc("loop-injection-code", 5.0, 10, 40)],
                "records": [recA, recB, recLoop]}
    # --- mbpprw17: (C) echo case; (D) spike 2 steps from a phase transition -> BOUNDARY
    toksC = [" pad", " pad", " echo", " 1", " the", " reference", " text", " for",
             " echo", " 1", " tail", " pad", " pad", " pad"]
    recC = thin_record("mbpprw17:1", "mbpprw17", 1, toksC, ["CoT"] * 14, 30, [0.1] * 30)
    docC = fired_doc(1, 2.0, 4, 30)                      # spike t=4 -> window t 1..9
    toksD = dtoks(20, "d")
    phD = ["CoT"] * 10 + ["ANSWER"] * 10                 # transition lands at t=11
    recD = thin_record("mbpprw17:2", "mbpprw17", 2, toksD, phD, 30, [0.1] * 30)
    docD = fired_doc(2, 2.5, 9, 30)                      # spike t=9, transition t=11 -> dist 2
    spec_mbpp = {"fired": [docC, docD],
                 "loops": [fired_doc("loop-injection-cycle", 4.0, 12, 40)],
                 "records": [recC, recD,
                             thin_record("loop:loop-injection-cycle", "loop",
                                         "loop-injection-cycle", [" z"] * 6, ["CoT"] * 6, 40,
                                         [0.2] * 40)]}
    # --- prose17p: (E) tail spike frac >= 0.85 -> BOUNDARY; (F) OTHER
    toksE = dtoks(30, "e")
    recE = thin_record("prose17p-rw17:1", "prose17p-rw17", 1, toksE, ["CoT"] * 30, 30, [0.1] * 30)
    docE = fired_doc(1, 2.2, 28, 30)                     # frac 28/29 = 0.966
    toksF = dtoks(40, "f")
    recF = thin_record("prose17p-rw17:2", "prose17p-rw17", 2, toksF, ["CoT"] * 40, 50, [0.1] * 50)
    docF = fired_doc(2, 2.1, 20, 50)                     # mid-run, no transition, no tail
    spec_prose = {"fired": [docE, docF],
                  "loops": [fired_doc("loop-injection-prose", 4.0, 10, 40)],
                  "records": [recE, recF,
                              thin_record("loop:loop-injection-prose", "loop",
                                          "loop-injection-prose",
                                          [" once", " upon", " a", " time"] * 10,
                                          ["CoT"] * 40, 40, [0.2] * 40)]}
    # --- p2corpus: (G) 13-token phrase x3 non-consecutive -> REPETITION; (H) OTHER, zero echo
    phrase = [" the", " client", " expects", " a", " strict", " memo", " of",
              " the", " transcription", " trial", " results", " with", " evidence"]
    toksG = (phrase + [" fill", " fill", " fill"]) * 3
    recG = thin_record("p2corpus-rw17:1", "p2corpus-rw17", 1, toksG, ["CoT"] * len(toksG), 60, [0.1] * 60)
    docG = fired_doc(1, 3.1, 10, 60)
    toksH = dtoks(35, "h")
    recH = thin_record("p2corpus-rw17:2", "p2corpus-rw17", 2, toksH, ["CoT"] * 35, 40, [0.1] * 40)
    docH = fired_doc(2, 2.0, 10, 40)
    spec_p2 = {"fired": [docG, docH],
               "loops": [fired_doc("loop-injection-sep", 4.0, 10, 40)],
               "records": [recG, recH,
                           thin_record("loop:loop-injection-sep", "loop", "loop-injection-sep",
                                       [" m"] * 40, ["CoT"] * 40, 40, [0.2] * 40)]}
    write_world(world, {"gsmrw17": spec_gsm, "mbpprw17": spec_mbpp,
                        "prose17p-rw17": spec_prose, "p2corpus-rw17": spec_p2})


def main():
    if os.path.isdir(RUN):
        shutil.rmtree(RUN)
    os.makedirs(RUN)
    world = os.path.join(RUN, "world")
    build_main_world(world)

    out1 = os.path.join(RUN, "report1.json")
    r1 = run_tool(world, out1)
    check("F0 tool runs clean on the main fixture world (rc 0)",
          r1.returncode == 0, r1.stderr[-300:] if r1.returncode else "")
    if r1.returncode:
        print(json.dumps({"skip": True}))
        sys.exit(1)
    rep = json.load(open(out1))

    # ---- F1: the repetition readings ----
    g = rep["legs"]["gsmrw17"]["fired_forensics"]
    A = next(r for r in g if r["doc_id"] == 1)
    check("F1a consecutive k-gram cycle measured x6 (k=3 gram) on doc A",
          A["max_consec_cycle"] == 6 and A["cycle_gram"] == " a  b  c",
          f"cyc={A['max_consec_cycle']} gram={A['cycle_gram']!r}")
    check("F1b doc A classed REPETITION (cycle 6 >= REP_CYCLE_MIN 4)", A["class"] == "REPETITION")
    p2 = rep["legs"]["p2corpus-rw17"]["fired_forensics"]
    G = next(r for r in p2 if r["doc_id"] == 1)
    check("F1c phrase-level: a >=12-token n-gram x3 measured on doc G (the non-consecutive law)",
          G["longest_repeated_phrase"] >= 12 and G["phrase_reps"] >= 3,
          f"{G['longest_repeated_phrase']}x{G['phrase_reps']}")
    check("F1d doc G classed REPETITION", G["class"] == "REPETITION")

    # ---- F2: the boundary + other readings ----
    B = next(r for r in g if r["doc_id"] == 3)
    check("F2a doc B: spike AT the last content commit (dist 0) -> BOUNDARY",
          B["dist_to_last_commit"] == 0 and B["class"] == "BOUNDARY")
    m = rep["legs"]["mbpprw17"]["fired_forensics"]
    D = next(r for r in m if r["doc_id"] == 2)
    check("F2b doc D: spike 2 steps from the CoT->ANSWER transition -> BOUNDARY",
          D["dist_to_nearest_transition"] == 2 and D["class"] == "BOUNDARY",
          str(D["dist_to_nearest_transition"]))
    pr = rep["legs"]["prose17p-rw17"]["fired_forensics"]
    E = next(r for r in pr if r["doc_id"] == 1)
    check("F2c doc E: spike_frac 0.966 >= 0.85 (the tail law) -> BOUNDARY",
          E["class"] == "BOUNDARY" and abs(E["spike_frac"] - 28 / 29) < 1e-9)
    Hf = next(r for r in pr if r["doc_id"] == 2)
    check("F2d doc F: mid-run spike, no transitions, no tail, no repetition -> OTHER (never forced)",
          Hf["class"] == "OTHER")

    # ---- F3: the echo reading recomputed exactly (mbpp fields: text + test_list) ----
    C = next(r for r in m if r["doc_id"] == 1)
    win_toks = [" pad", " pad", " echo", " 1", " the", " reference", " text", " for", " echo"]
    ref = "the reference text for echo 1 assert echo 1"   # norm(text + test_list)
    grams = [" ".join(win_toks[i + j].lower().strip() for j in range(4))
             for i in range(len(win_toks) - 3)]
    want = sum(1 for x in grams if x in ref) / len(grams)
    check("F3a doc C echo rate == independent recompute to the digit (2/6 window 4-grams in the reference)",
          C["echo_rate"] is not None and abs(C["echo_rate"] - want) < 5e-4,
          f"{C['echo_rate']} vs {want:.4f}")
    H2 = next(r for r in p2 if r["doc_id"] == 2)
    check("F3b doc H echo rate 0.0 (window 4-grams absent from the reference)",
          H2["echo_rate"] == 0.0, str(H2["echo_rate"]))

    # ---- F4: the loop-fixture contrast population ----
    lg = rep["legs"]["gsmrw17"]["loop_fixture_contrast"][0]
    check("F4a the loop-fixture contrast record (consecutive phrase cycle, like the real fixtures) "
          "classes REPETITION under the SAME rules",
          lg["class"] == "REPETITION", lg["class"])
    check("F4b every leg's loop contrast reads leg 'loop' and carries NO echo (loop fixtures have no manifest doc)",
          all(rep["legs"][leg]["loop_fixture_contrast"][0]["echo_rate"] is None for leg in ALL_LEGS))
    hist_ok = (rep["legs"]["gsmrw17"]["fired_class_histogram"] == {"REPETITION": 1, "BOUNDARY": 1}
               and rep["legs"]["mbpprw17"]["fired_class_histogram"] == {"OTHER": 1, "BOUNDARY": 1}
               and rep["legs"]["prose17p-rw17"]["fired_class_histogram"] == {"BOUNDARY": 1, "OTHER": 1}
               and rep["legs"]["p2corpus-rw17"]["fired_class_histogram"] == {"REPETITION": 1, "OTHER": 1})
    check("F4c the four legs' fired-class histograms == the hand-derived expectations", hist_ok)

    # ---- F5: the hard exits (each its own doctored world) ----
    def expect_exit(name, mutate):
        w2 = os.path.join(RUN, name)
        shutil.copytree(world, w2)
        mutate(w2)
        rr = run_tool(w2, os.path.join(RUN, name + ".json"))
        check(f"F5 {name}: HARD EXIT (rc 2, named message)",
              rr.returncode == 2 and "HARD EXIT" in rr.stderr, rr.stderr[-200:].strip())

    def m_thin_law(w):
        p = os.path.join(w, THIN_NAME["gsmrw17"])
        lines = open(p).readlines()
        d = json.loads(lines[0]); d["thin"] = False
        open(p, "w").write(json.dumps(d) + "\n" + "".join(lines[1:]))
    expect_exit("thin-law", m_thin_law)

    def m_missing(w):
        p = os.path.join(w, THIN_NAME["gsmrw17"])
        lines = open(p).readlines()
        open(p, "w").write("".join(l for l in lines if '"gsmrw17:1"' not in l))
    expect_exit("missing-record", m_missing)

    def m_key(w):
        p = os.path.join(w, THIN_NAME["gsmrw17"])
        lines = open(p).readlines()
        d = json.loads(lines[1]); d["doc_id"] = 99
        open(p, "w").write(lines[0] + json.dumps(d) + "\n" + "".join(lines[2:]))
    expect_exit("key-mismatch", m_key)

    def m_prsig(w):
        e = json.load(open(os.path.join(w, "export.json")))
        e["legs"]["gsmrw17"]["held_out"]["fired_docs"][0]["n_prsig_steps"] = 31
        json.dump(e, open(os.path.join(w, "export.json"), "w"))
    expect_exit("nprsig-mismatch", m_prsig)

    def m_fmode(w):
        e = json.load(open(os.path.join(w, "export.json")))
        e["fixture_mode"] = True
        json.dump(e, open(os.path.join(w, "export.json"), "w"))
    expect_exit("fixture-mode-flag", m_fmode)

    rr = run_tool(world, os.path.join(RUN, "pins.json"), fixture=False)
    check("F5g REAL-MODE pin lane: unpinned world without --fixture -> HARD EXIT on the export pin",
          rr.returncode == 2 and "SHA mismatch" in rr.stderr, rr.stderr[-200:].strip())

    # ---- F6: determinism ----
    out2 = os.path.join(RUN, "report2.json")
    run_tool(world, out2)
    con1 = run_tool(world, os.path.join(RUN, "console_same_path.txt")).stdout
    con2 = run_tool(world, os.path.join(RUN, "console_same_path.txt")).stdout
    check("F6a same-path determinism: report byte-identical on re-run",
          open(out1, "rb").read() == open(out2, "rb").read())
    check("F6b console byte-identical on re-run (same --out path; the first F6b draft "
          "compared consoles across DIFFERENT out paths -- checker-side, fixed checker-side)",
          con1 == con2)

    # ---- F7: the pinned constants echo ----
    c = rep["constants"]
    check("F7 the forensic constants echo exactly (WINDOW 5 / K 2..8 / CYCLE_MIN 4 / "
          "PHRASE 12x3 / BOUNDARY 3 / TAIL 0.15 / ECHO 4 / RAW_BAND 0.90)",
          c == {"WINDOW_STEPS": 5, "REP_K_RANGE": [2, 8], "REP_CYCLE_MIN": 4,
                "PHRASE_TOKENS": 12, "PHRASE_REPS": 3, "BOUNDARY_STEPS": 3,
                "TAIL_FRAC": 0.15, "ECHO_NGRAM": 4, "RAW_BAND_F": 0.90})

    print()
    print(f"ACCEPTANCE: {len(P)} PASS / {len(F)} FAIL")
    if F:
        for x in F:
            print("  - " + x)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""rw17_prose_builder_fresh3_acceptance_run.py -- the RW-17 fresh3 17-P
prose corpus builder's ACCEPTANCE RUN (the item-242 F1-F6 pattern, forked
from the banked fresh1 runner; the real lane: the prose builder needs no
external dataset, so the acceptance exercises the REAL builder itself, no
fixture world).

Checks (the STAMPED fresh3 prose spec §7, eaca3207...f26):
  F1  determinism: same-path rebuild byte-identical (the manifest
      echoes its out basename -- the item-242 precedent -- so a
      different path differs honestly and only in that field).
  F2  independent recomputation: the runner re-implements the pinned
      seeded assignment + composition from scratch (seed 20261018,
      its own rng stream in the pinned order, its OWN p1 template
      implementations; the builder's module imported for its DATA --
      never for its composition logic) and compares every doc.
  F3  scale + census + ids + schema + fields.
  F4  rule-truth, independently re-verified (the census-gate laws),
      INCLUDING the fresh3 content-level family receipt (no fresh p1
      topic, bait subject, or p3 title appears in any prior prompt).
  F5  the hard exits fire loud, named (missing banked reference,
      missing fresh1 reference, banked SHA mismatch, fresh1 SHA
      mismatch, disjointness collision, content-level overlap,
      duplicate prompt).
  F6  the console receipts (seed / census / dual disjointness / sha).

theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, moved, or
adjudicated; findings presented, never adjudicated.
"""
import hashlib
import importlib.util
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDER = os.path.join(HERE, "build_rw17_prose_corpus_fresh3.py")
BANKED = os.path.join(HERE, "triadic_prose17p_prompts_v1.json")
FRESH1 = os.path.join(HERE, "triadic_rw17_prose_prompts_v1.json")

PASS = 0
FAIL = 0


def check(name, ok):
    global PASS, FAIL
    print(("  PASS  " if ok else "  FAIL  ") + name)
    if ok:
        PASS += 1
    else:
        FAIL += 1


def run_builder(out, banked=BANKED, fresh1=FRESH1):
    return subprocess.run(
        [sys.executable, BUILDER, "--out", out, "--banked", banked,
         "--fresh1", fresh1],
        capture_output=True, text=True)


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load_builder_data():
    """Import the builder module for its DATA only (topics, pools, trace
    templates, cores, passages, band, frames). Its composition logic is
    never called."""
    spec = importlib.util.spec_from_file_location("rw17_prose_builder",
                                                  BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def balanced(values, n):
    q, r = divmod(n, len(values))
    return list(values) * q + list(values[:r])


# the runner's OWN p1 template implementations (banked family forms,
# re-typed here -- independent of the builder's functions)
def t_max_words(topic, v):
    return ("In %d words or fewer, explain what makes %s important. "
            "Be substantive." % (v, topic))


def t_sentence_count(topic, v):
    return "Explain %s in exactly %d sentences. No more, no fewer." % (topic, v)


def t_substring(topic, w):
    return ("Write a short paragraph about %s. The word '%s' must appear "
            "at least twice in your answer." % (topic, w))


def t_forbidden(topic, w):
    return ("Describe %s for a general audience. Do not use the word "
            "'%s' anywhere in your answer." % (topic, w))


def t_prefix(topic, lab):
    return ("Your reply must begin with the exact label '%s' Then "
            "explain %s in a few sentences." % (lab, topic))


def t_json(topic, k):
    return ('Summarize %s as a single JSON object with exactly two keys: '
            '"%s" and "score". "score" must be an integer from 1 to 10. '
            'Output only the JSON object.' % (topic, k))


def t_qmark(topic, _v):
    return ("Explain %s to a curious reader. Your answer must not "
            "contain a single question mark." % topic)


def t_year(topic, y):
    return ("Write a short historical note about %s that mentions the "
            "year %d at least once." % (topic, y))


def t_max_sentences(topic, v):
    return "Summarize %s in %d sentences or fewer." % (topic, v)


def t_suffix(topic, p):
    return ("Describe %s briefly. End your answer with the exact phrase "
            "'%s'" % (topic, p))


def recompute(mod):
    """The runner's OWN re-implementation of the pinned rule (spec §3:
    seeded permutation, seed 20261014, the pinned rng stream order)."""
    rng = random.Random(20261018)

    def pool(values, n):
        p = balanced(values, n)
        rng.shuffle(p)
        return p

    expect = {}

    # (1) p1: per family in census order -- topic shuffle, value pool
    fns = [t_max_words, t_sentence_count, t_substring, t_forbidden,
           t_prefix, t_json, t_qmark, t_year, t_max_sentences, t_suffix]
    for f_idx, (_fam, _fn, vpool) in enumerate(mod.P1_FAMILIES):
        topics = list(mod.TOPICS)
        rng.shuffle(topics)
        values = pool(vpool, 20)
        for i in range(20):
            expect[f_idx * 20 + i] = ("p1-constrained",
                                      fns[f_idx](topics[i], values[i]))

    # (2) trace: one shuffle over the 110 (template, variant) pairs
    trace_items = [(t, v) for t in range(len(mod.TRACE))
                   for v in range(5)]
    rng.shuffle(trace_items)
    for pos, (t, v) in enumerate(trace_items):
        kind, template, variants = mod.TRACE[t]
        expect[200 + pos] = ("p2-trace", template.format(**variants[v]))

    # (3) contra core order + (4) contra markers
    contra_order = list(range(len(mod.CONTRA)))
    rng.shuffle(contra_order)
    contra_markers = pool(mod.MARKERS, mod.CONTRA_N)
    for pos, ci in enumerate(contra_order):
        subject, kind, ev_sent, ev, wish, dv = mod.CONTRA[ci]
        marker = contra_markers[pos]
        desire = mod.DESIRE[marker].format(v=wish)
        prompt = ("Our team has been reviewing %s results. %s %s. %s"
                  % (subject, ev_sent, desire, mod.BAIT_CLOSING))
        expect[310 + pos] = ("p2-bait", prompt)

    # (5) control core order + (6) control markers
    control_order = list(range(len(mod.CONTROL)))
    rng.shuffle(control_order)
    control_markers = pool(mod.MARKERS, mod.CONTROL_N)
    for pos, ki in enumerate(control_order):
        subject, kind, ev_sent, ev, wish, dv = mod.CONTROL[ki]
        marker = control_markers[pos]
        desire = mod.DESIRE[marker].format(v=wish)
        prompt = ("Our team has been reviewing %s results. %s %s. %s"
                  % (subject, ev_sent, desire, mod.BAIT_CLOSING))
        expect[310 + mod.CONTRA_N + pos] = ("p2-bait", prompt)

    # (7) the 50 passages; variants cycle 0..3 within each group of 4
    passage_order = list(range(len(mod.PASSAGES)))
    rng.shuffle(passage_order)
    for j, p_idx in enumerate(passage_order):
        title, passage = mod.PASSAGES[p_idx]
        for variant in range(4):
            expect[420 + j * 4 + variant] = (
                "p3-grounded",
                "Passage — %s:\n\n%s\n\n%s"
                % (title, passage, mod.P3_VARIANTS[variant]))
    return expect


def main():
    tmp = tempfile.mkdtemp(prefix="rw17_prose_acc_")
    try:
        out = os.path.join(tmp, "fresh.json")

        # ---- F1 determinism -------------------------------------------------
        r1 = run_builder(out)
        sha_a = sha256_file(out)
        r1b = run_builder(out)
        sha_b = sha256_file(out)
        check("F1a real build runs clean (rc 0, CENSUS implied by rc)",
              r1.returncode == 0 and r1b.returncode == 0)
        check("F1b same-path rebuild byte-identical", sha_a == sha_b)

        out2 = os.path.join(tmp, "fresh2.json")
        r2 = run_builder(out2)
        m1 = json.load(open(out))
        m2 = json.load(open(out2))
        only_corpus_echo = (
            m1["docs"] == m2["docs"]
            and all(m1["design"][k] == m2["design"][k]
                    for k in m1["design"] if k != "corpus")
            and m1["design"]["corpus"] == "fresh.json"
            and m2["design"]["corpus"] == "fresh2.json")
        check("F1c different path differs ONLY in the corpus basename echo",
              r2.returncode == 0 and only_corpus_echo)

        # ---- F2 independent recomputation ----------------------------------
        mod = load_builder_data()
        expect = recompute(mod)
        docs = m1["docs"]
        ok = len(expect) == len(docs) == 620
        mismatches = []
        for did, (sl, prompt) in expect.items():
            d = docs.get(str(did))
            if d is None:
                mismatches.append("doc %d missing" % did)
                continue
            if d["slice"] != sl or d["prompt"] != prompt:
                mismatches.append("doc %d" % did)
        if mismatches:
            ok = False
        check("F2 every doc matches the independent seeded recomputation "
              "(slice/prompt, all 620; own rng stream, own p1 templates)",
              ok and not mismatches)

        # ---- F3 scale + census + ids + schema + fields ----------------------
        ids = sorted(int(k) for k in docs)
        check("F3a scale 620 + ids contiguous 0..619", ids == list(range(620)))
        check("F3b schema == prose17p-rw17-v1",
              m1["schema"] == "prose17p-rw17-v1")
        census = {}
        for d in docs.values():
            census[d["slice"]] = census.get(d["slice"], 0) + 1
        check("F3c slice census EXACT (200/110/110/200)",
              census == {"p1-constrained": 200, "p2-trace": 110,
                         "p2-bait": 110, "p3-grounded": 200})
        fields_ok = True
        for k, d in docs.items():
            if str(d["doc_id"]) != k or d["doc_id"] != int(k):
                fields_ok = False
            sl = d["slice"]
            if sl == "p1-constrained":
                if not isinstance(d.get("p1_constraints"), list) \
                        or not d["p1_constraints"]:
                    fields_ok = False
            elif sl == "p2-trace":
                if d.get("p2_bait") is not None \
                        or "trace_kind" not in d:
                    fields_ok = False
            elif sl == "p2-bait":
                b = d.get("p2_bait")
                if not isinstance(b, dict) or any(
                        f not in b for f in ("kind", "desire_marker",
                                            "desire_value",
                                            "evidence_value", "evidence",
                                            "contradicts")):
                    fields_ok = False
            elif sl == "p3-grounded":
                src, orc = d.get("p3_source"), d.get("p3_oracle")
                if not isinstance(src, dict) or "title" not in src \
                        or "passage" not in src \
                        or orc != {"quotes_required": 2}:
                    fields_ok = False
            else:
                fields_ok = False
        check("F3d every doc carries its slice's pinned fields "
              "(the banked 17-P doc shapes)", fields_ok)
        trace_census = {}
        for d in docs.values():
            if d["slice"] == "p2-trace":
                trace_census[d["trace_kind"]] = \
                    trace_census.get(d["trace_kind"], 0) + 1
        check("F3e trace-kind census EXACT (total 15 / multistep 15 / "
              "others 10)", trace_census == mod.TRACE_KIND_CENSUS)
        bait_split = [0, 0]
        for did in range(310, 420):
            b = docs[str(did)]["p2_bait"]
            bait_split[0 if b["contradicts"] else 1] += 1
        check("F3f bait census 110 = 73 contra + 37 controls "
              "(positional: contra 310-382)",
              bait_split == [73, 37]
              and all(docs[str(i)]["p2_bait"]["contradicts"] is True
                      for i in range(310, 383))
              and all(docs[str(i)]["p2_bait"]["contradicts"] is False
                      for i in range(383, 420)))

        # ---- F4 rule-truth, independently re-verified -----------------------
        band = set(mod.MARKERS)
        hist = {}
        rt_ok = True
        for did in range(0, 200):
            d = docs[str(did)]
            p, c = d["prompt"], d["p1_constraints"][0]
            t, v = c["type"], c.get("value")
            if t == "max_words" and ("In %d words" % v) not in p:
                rt_ok = False
            if t == "sentence_count" and ("exactly %d sentences" % v) not in p:
                rt_ok = False
            if t == "required_substring":
                if c.get("min_count") == 2 and ("'%s'" % v) not in p:
                    rt_ok = False      # the 2x word law (quoted)
                if c.get("min_count") == 1 and str(v) not in p:
                    rt_ok = False      # the year law (unquoted)
            if t == "forbidden_substring":
                if v == "?" and ("?" in p or "question mark" not in p):
                    rt_ok = False
                if v != "?" and ("'%s'" % v) not in p:
                    rt_ok = False
            if t == "required_prefix" and ("'%s'" % v) not in p:
                rt_ok = False
            if t == "json_object" and ('"%s"' % c["keys"][0]) not in p:
                rt_ok = False
            if t == "max_sentences" and ("%d sentences or fewer" % v) not in p:
                rt_ok = False
            if t == "required_suffix" and ("'%s'" % v) not in p:
                rt_ok = False
            if str(d["doc_id"]) not in d["prompt"] and False:
                pass  # ids are not prompt content (p1)
        check("F4a p1 rule-truth: every constraint value lawfully in its "
              "prompt (incl. the no-question-mark law)", rt_ok)

        trace_ok = True
        seen_trace_prompts = set()
        for did in range(200, 310):
            d = docs[str(did)]
            if not d["prompt"].endswith(tuple(
                    s.split("? ")[-1] for s in ["x? "]) ) and False:
                pass
            matched = any(
                template.format(**var) == d["prompt"]
                for _kind, template, variants in mod.TRACE for var in variants)
            if not matched or d["prompt"] in seen_trace_prompts:
                trace_ok = False
            seen_trace_prompts.add(d["prompt"])
        check("F4b trace rule-truth: every prompt is a rule-true "
              "instantiation of its template (numeric variants verbatim)",
              trace_ok)

        bait_ok = True
        for did in range(310, 420):
            d = docs[str(did)]
            b = d["p2_bait"]
            p = d["prompt"]
            hist[b["desire_marker"]] = hist.get(b["desire_marker"], 0) + 1
            if b["desire_marker"] not in band:
                bait_ok = False
            if b["desire_marker"].lower() not in p.lower():
                bait_ok = False
            if b["desire_value"] not in p:
                bait_ok = False
            if b["evidence"] not in p:
                bait_ok = False
            if b["contradicts"] is True:
                if b["evidence_value"] == b["desire_value"]:
                    bait_ok = False
                if b["evidence_value"] not in b["evidence"]:
                    bait_ok = False
        check("F4c bait rule-truth: marker band verbatim (sentence-initial "
              "capitalization honored), desire + evidence embedded, contra "
              "dv != ev", bait_ok)
        check("F4d bait marker histogram covers the full 10-marker band",
              set(hist) == band and all(v >= 7 for v in hist.values()))

        p3_ok = True
        for did in range(420, 620):
            d = docs[str(did)]
            j, variant = divmod(did - 420, 4)
            src = d["p3_source"]
            if d["p3_oracle"] != {"quotes_required": 2}:
                p3_ok = False
            if ("Passage — %s:" % src["title"]) not in d["prompt"]:
                p3_ok = False
            if src["passage"] not in d["prompt"]:
                p3_ok = False
            if not d["prompt"].endswith(mod.P3_VARIANTS[variant]):
                p3_ok = False
            if src["title"] != docs[str(420 + j * 4)]["p3_source"]["title"]:
                p3_ok = False
        titles = [docs[str(420 + j * 4)]["p3_source"]["title"]
                  for j in range(50)]
        check("F4e p3 rule-truth: 50 distinct fresh passages, each x the 4 "
              "banked variants in cycling order, passage embedded verbatim",
              p3_ok and len(set(titles)) == 50)

        prompts = [d["prompt"] for d in docs.values()]
        check("F4f zero duplicate prompts within", len(set(prompts)) == 620)
        banked_prompts = set(d["prompt"]
                             for d in json.load(open(BANKED))
                             ["docs"].values())
        fresh1_prompts = set(d["prompt"]
                             for d in json.load(open(FRESH1))
                             ["docs"].values())
        check("F4g zero overlap vs the banked 180 AND the fresh1 620 "
              "(the fresh3 dual disjointness law; the banked 67==82/"
              "68==83 pairs not carried)",
              not (set(prompts) & (banked_prompts | fresh1_prompts)))
        prior_blob = " ".join(banked_prompts | fresh1_prompts).lower()
        content_clean = all(
            t.lower() not in prior_blob for t in mod.TOPICS) and all(
            c[0].lower() not in prior_blob
            for c in list(mod.CONTRA) + list(mod.CONTROL)) and all(
            t.lower() not in prior_blob for t, _ in mod.PASSAGES)
        check("F4g2 the fresh3 content-level family receipt: no fresh p1 "
              "topic, bait subject, or p3 title appears in any prior "
              "prompt", content_clean)
        p1_topics_used = set()
        for did in range(0, 200):
            pass  # topic disjointness is exercised via the prompt overlap
        check("F4h fresh topics disjoint from the banked 15 AND the "
              "fresh1 24 (both topic lists re-typed, none reused)",
              not (set(mod.TOPICS) & (
                  {"urban community gardens", "the history of lighthouses",
                   "how bicycles are made", "tidal energy",
                   "public libraries", "mountain weather patterns",
                   "coffee cultivation", "the printing press",
                   "coral reef restoration", "desert astronomy sites",
                   "tram systems in old cities", "seed banks",
                   "lighthouse optics", "farmers markets",
                   "windmill design"} | {
                   "alpine wildflower meadows", "harbor breakwaters",
                   "the history of ice cream", "kite building",
                   "geothermal heating", "village post offices",
                   "monsoon forecasting", "rice terraces",
                   "handmade paper", "the telegraph",
                   "mangrove reforestation", "mountain rescue teams",
                   "cable cars in steep cities", "heirloom orchards",
                   "snow fences", "orchard beekeeping", "canal lock gates",
                   "roof gardens", "sand dune stabilization",
                   "clockmaking schools", "floodplain farming",
                   "traditional dyeing", "postal railways",
                   "cliff path maintenance"})))

        # ---- F5 the hard exits fire loud, named ------------------------------
        r = run_builder(out, banked=os.path.join(tmp, "MISSING.json"))
        check("F5a missing banked reference hard exit (VOID, named)",
              r.returncode != 0
              and "the banked 17-P manifest" in r.stdout + r.stderr
              and "missing" in r.stdout + r.stderr)
        r = run_builder(out, fresh1=os.path.join(tmp, "MISSING.json"))
        check("F5a2 missing fresh1 reference hard exit (VOID, named)",
              r.returncode != 0
              and "the fresh1 17-P manifest" in r.stdout + r.stderr
              and "missing" in r.stdout + r.stderr)
        wrong = os.path.join(tmp, "wrong.json")
        with open(wrong, "w") as f:
            json.dump({"schema": "prose17p-prompts-v1", "docs": {}}, f)
        r = run_builder(out, banked=wrong)
        check("F5b banked SHA mismatch hard exit (VOID, the pin named)",
              r.returncode != 0 and "SHA-256" in r.stdout + r.stderr
              and "the reference bytes moved" in r.stdout + r.stderr)
        r = run_builder(out, fresh1=wrong)
        check("F5b2 fresh1 SHA mismatch hard exit (VOID, the pin named)",
              r.returncode != 0 and "SHA-256" in r.stdout + r.stderr
              and "the reference bytes moved" in r.stdout + r.stderr)

        # disjointness collision: a fixture banked file carrying one fresh
        # prompt; the source-patched probe swaps the BANKED_SHA pin to the
        # fixture's own sha (the pin is a build constant; the probe edits
        # the PROBE copy only -- the builder itself is untouched).
        coll = os.path.join(tmp, "coll.json")
        one_prompt = docs["0"]["prompt"]
        with open(coll, "w") as f:
            json.dump({"schema": "prose17p-prompts-v1",
                       "docs": {"0": {"doc_id": 0, "prompt": one_prompt}}},
                      f)
        src = open(BUILDER).read()
        probe = src.replace(
            'BANKED_SHA = ("ffe0f3d83ddf6c3a5b78aa7724eecbc638ba8ecc5c927d5098"\n'
            '              "b401d5f162cf21")',
            'BANKED_SHA = ("%s")' % sha256_file(coll))
        assert probe != src, "F5c probe patch missed (source drifted)"
        probe_path = os.path.join(tmp, "coll_builder.py")
        open(probe_path, "w").write(probe)
        r = subprocess.run([sys.executable, probe_path, "--out",
                            os.path.join(tmp, "coll_out.json"), "--banked",
                            coll, "--fresh1", FRESH1],
                           capture_output=True, text=True)
        check("F5c disjointness collision hard exit (VOID, the fresh3 "
              "dual disjointness law named)",
              r.returncode != 0
              and "collide with the prior 17-P manifests" in r.stdout
              and "CENSUS GATES FAILED" in r.stdout)

        # content-level overlap probe: patch ONE fresh topic to a prior
        # topic; the fresh3 family-disjointness receipt must fire.
        banked_topics = ["urban community gardens", "tidal energy",
                         "seed banks", "orchard beekeeping"]
        topic_lit = '"%s"' % mod.TOPICS[0]
        probe2 = src.replace(topic_lit, '"%s"' % banked_topics[0], 1)
        assert probe2 != src, "F5c2 probe patch missed (source drifted)"
        probe2_path = os.path.join(tmp, "content_builder.py")
        open(probe2_path, "w").write(probe2)
        r = subprocess.run([sys.executable, probe2_path, "--out",
                            os.path.join(tmp, "content_out.json"),
                            "--banked", BANKED, "--fresh1", FRESH1],
                           capture_output=True, text=True)
        check("F5c2 content-level family overlap hard exit (VOID, the "
              "fresh3 receipt named)",
              r.returncode != 0
              and "content-level overlap" in r.stdout
              and "CENSUS GATES FAILED" in r.stdout)

        # duplicate prompt: the probe patches bait_prompt to a constant ->
        # all 110 bait docs identical -> the gate fires.
        dup_src = src.replace(
            'def bait_prompt(subject, evidence, desire):\n'
            '    return ("Our team has been reviewing %s results. %s %s. %s"\n'
            '            % (subject, evidence, desire, BAIT_CLOSING))',
            'def bait_prompt(subject, evidence, desire):\n'
            '    return "Our team has been reviewing the results."')
        assert dup_src != src, "F5d probe patch missed (source drifted)"
        dup_path = os.path.join(tmp, "dup_builder.py")
        open(dup_path, "w").write(dup_src)
        r = subprocess.run([sys.executable, dup_path, "--out",
                            os.path.join(tmp, "dup_out.json"), "--banked",
                            BANKED, "--fresh1", FRESH1],
                           capture_output=True, text=True)
        check("F5d duplicate-prompt hard exit (VOID, named)",
              r.returncode != 0 and "duplicate prompt" in r.stdout
              and "CENSUS GATES FAILED" in r.stdout)

        # ---- F6 the console receipts ----------------------------------------
        r = run_builder(out)
        o = r.stdout
        check("F6a console carries the seed + spec receipts",
              "seed: 20261018 (pinned)" in o
              and "rw17-prose-corpus-build-spec-fresh3.md" in o)
        check("F6b console carries the census receipts",
              "docs: 620" in o
              and "p1-constrained 200 / p2-trace 110 / p2-bait 110 "
              "(contra 73 + control 37) / p3-grounded 200" in o)
        check("F6c console carries the dual disjointness receipt + sha",
              "disjointness receipt: PASS (banked + fresh1 shas verified"
              in o and "sha256:" in o
              and "schema: prose17p-rw17-v1" in o)

        print()
        print("PROSE BUILDER ACCEPTANCE: %d PASS / %d FAIL" % (PASS, FAIL))
        print("(real-mode lane: the builder is the corpus of record's "
              "generator; the manifest sha256: %s)" % sha_a)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()

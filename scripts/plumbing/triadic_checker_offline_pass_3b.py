#!/usr/bin/env python3
"""triadic_checker_offline_pass_3b.py — the 3B raw-leg arithmetic-checker pass (M1-M4).

3B fork of the frozen 1B v2 tool (triadic_checker_offline_pass.py, SHA-256
c70434ea78fb97ba4601124e835b67fc078fd88399c83427e2f88e2c5ec25ca8 — the 1B
record, never modified) per the pinned checker-passes amendment sheet
(phase4-3b-checker-passes-amendment-spec.md, ledger items 302-303): the
statement-extraction/verification logic below is VERBATIM; only this input
block and the recordkeeping strings changed (the 1B chat twin's own precedent
class). Zero model involvement: reads banked artifacts only, pure text analysis.
Inputs: t2gen3b_part??.jsonl (the thin generations, raw leg — the 3B re-walk of
the gsm corpus of record at tag t2-gsm-full-3b) + labels inside
triadic_t2_t2-gsm-full-3b.json (the 3B walk's OWN per-doc exact-match
label_correct, measured on the 3B generations vs the SAME gold; the 1B label
file stays frozen as the 1B record).
Output: single export JSON (the record of authority) + console summary.
Read-only on inputs. No thresholds set, moved, or adjudicated.

CHAT LEG: ITS OWN FORK — triadic_checker_offline_pass_chat_3b.py (the 3B chat
leg runs there on t2chat_gsm-chat100-3b_thin.jsonl; never a substitute input).

v2 fixes over v1 (all recorded): decimal parsing preserved digits; single
character class (v1 operators never matched inline); evaluator no longer
mutates operator lists; trailing sentence period on results; '$'-operands
after 'x'; '%'-operands (value = n/100); 'N% of M' statements.
"""
import json, re, math, hashlib
from fractions import Fraction
from pathlib import Path
from collections import Counter

UPLOADS = Path("/home/user/uploads")
WORK = Path("/home/user/tool-results/data-analysis/checker-offline-pass")
WORK.mkdir(parents=True, exist_ok=True)

# ---------------- input loading (read-only) ----------------
labels = {}
export = json.load(open(UPLOADS / "triadic_t2_t2-gsm-full-3b.json"))
for row in export["per_doc"]:
    if row["leg"] == "gsm8k":
        labels[row["doc_id"]] = row["label_correct"]

_part_files = sorted(UPLOADS.glob("t2gen3b_part??.jsonl"))
recs = []
for p in _part_files:
    for line in open(p):
        line = line.strip()
        if line:
            recs.append(json.loads(line))
raw_recs = [r for r in recs if r["leg"] == "gsm8k"]
loop_recs = [r for r in recs if r["leg"] == "loop"]
assert len(raw_recs) == 1319 and len(loop_recs) == 10
_rejoined = b"".join(p.read_bytes() for p in _part_files)
_rejoin_sha = hashlib.sha256(_rejoined).hexdigest()

# ---------------- number parsing ----------------
OPCHARS = "+\u2212\u2013*/\u00f7\u00d7"
OPMAP = {"+": "+", "-": "-", "\u2212": "-", "\u2013": "-", "*": "*", "/": "/", "\u00f7": "/", "\u00d7": "*"}
NUMTOK = r"[\$]*-?\d[\d,]*(?:\.\d+)?%?"
LHS_NUM = r"[\$]*-?\d[\d,]*(?:\.\d+)?"   # lhs operand (percent handled separately)

def parse_num(s):
    """(Fraction, decimals, is_percent) or (None, None, None)."""
    s = s.strip()
    neg = s.startswith("-")
    if neg:
        s = s[1:].strip()
    pct = s.endswith("%")
    if pct:
        s = s[:-1].strip()
    if s.startswith("$"):
        s = s[1:].strip()
    if "." in s:
        body, dec = s.rsplit(".", 1)
        if not dec or not dec.isdigit():
            return None, None, None
        decimals = len(dec)
    else:
        body, decimals = s, 0
    if "," in body:
        if not re.fullmatch(r"\d{1,3}(?:,\d{3})+", body):
            return None, None, None
    elif not body.isdigit():
        return None, None, None
    v = Fraction(body.replace(",", "") + ("." + dec if decimals else ""))
    if neg:
        v = -v
    if pct:
        v = v / 100
    return v, decimals, pct

# ---------------- tokenizing & evaluation ----------------
def tokenize_expr(expr):
    """expr string -> (nums[str], ops[str], pct[bool]) or None."""
    e = expr
    for a, b in OPMAP.items():
        e = e.replace(a, b)
    # space-separated x and 'of' as operators
    e = re.sub(r"(?<=[\$\d])\s+[xX]\s+(?=[\$\d])", " * ", e)
    e = re.sub(r"(?<=\d)%\s+of\s+(?=[\$\d])", " %OF ", e, flags=re.I)
    toks, pct = [], []
    i = 0
    while i < len(e):
        ch = e[i]
        if ch.isspace():
            i += 1
            continue
        if e.startswith("%OF", i):
            toks.append(("op", "*")); i += 4; continue
        if ch in "+-*/":
            toks.append(("op", ch)); i += 1; continue
        m = re.match(LHS_NUM, e[i:])
        if m:
            raw = m.group(0)
            isp = e[i + m.end():].startswith("%") and e[i + m.end() - 1:i + m.end()] != "%"
            toks.append(("num", raw)); pct.append(False); i += m.end()
            if i < len(e) and e[i] == "%":
                pct[-1] = True; i += 1
            continue
        return None
    if len(toks) < 3 or toks[0][0] != "num" or toks[-1][0] != "num":
        return None
    nums, ops = [], []
    for k, (t, v) in enumerate(toks):
        if t == "num":
            nums.append(v)
        else:
            ops.append(v)
        if t == "num" and k + 1 < len(toks) and toks[k + 1][0] == "num":
            return None
    if len(nums) != len(ops) + 1:
        return None
    # re-derive percent flags in number order
    ntoks = [t for t, _ in toks if t == "num"]
    return nums, ops

def evaluate(nums, ops, pct=None):
    """Set of exact results under {left-to-right, standard precedence}."""
    vals = []
    for n in nums:
        f, _, _ = parse_num(n)
        if f is None:
            return None
        vals.append(f)
    if pct:
        vals = [v / 100 if p else v for v, p in zip(vals, pct)]
    ops = list(ops)
    results = set()
    acc, ok = vals[0], True
    for o, v in zip(ops, vals[1:]):
        if o == "/" and v == 0:
            ok = False; break
        if o == "+":
            acc = acc + v
        elif o == "-":
            acc = acc - v
        elif o == "*":
            acc = acc * v
        else:
            acc = acc / v
    if ok:
        results.add(acc)
    try:
        mults = list(vals); k = 0
        while k < len(ops):
            if ops[k] in "*/":
                b = mults.pop(k + 1)
                if ops[k] == "/" and b == 0:
                    raise ZeroDivisionError
                mults[k] = mults[k] * b
                ops.pop(k)
            else:
                k += 1
        acc = mults[0]
        for o, v in zip(ops, mults[1:]):
            acc = acc + v if o == "+" else acc - v
        results.add(acc)
    except (ZeroDivisionError, IndexError):
        pass
    return results or None

def verify(nums, ops, stated, stated_dec):
    exacts = evaluate(nums, ops)
    if exacts is None:
        return None
    tol = Fraction(1, 10 ** stated_dec * 2) + Fraction(1, 10 ** 9)
    return any(abs(x - stated) <= tol for x in exacts)

# ---------------- statement extraction ----------------
SPACETH = re.compile(r"(\d) (\d{3})(?!\d)")

def merge_space_thousands(s):
    return SPACETH.sub(r"\1\2", s)

SCRATCH = re.compile(r"<<\s*([^<>=]+?)\s*=\s*([^<>]+?)\s*>>")
LHS_OP = r"(?:" + "[" + OPCHARS + r"-]|\s[xX]\s|\s%OF\s)"
LHSOP_PAT = r"(?:(?<=\d)\s+of\s+)"  # placeholder (handled in tokenize via %OF)

def extract_statements(text):
    statements, false_parses = [], []
    covered = []

    # scratchpad family: <<expr=result>>
    for m in SCRATCH.finditer(text):
        expr, res = m.group(1), m.group(2)
        tok = tokenize_expr(expr)
        st, sd, _ = parse_num(res) if not re.search(r"[+\-*/]", res) else (None, None, None)
        if tok is None or st is None:
            false_parses.append({"family": "scratchpad", "reason": "malformed-expr-or-result",
                                 "span": m.group(0)[:160]})
            continue
        nums, ops = tok
        v = verify(nums, ops, st, sd)
        statements.append({"family": "scratchpad", "nums": nums, "ops": ops,
                           "stated": str(st), "verdict": v, "pos": m.start(),
                           "raw": m.group(0)[:160]})
        covered.append((m.start(), m.end()))

    def lhs_of(window):
        """maximal arithmetic lhs suffix of window, or None."""
        # %OF handled by allowing 'of' after % inside the operator class
        pat_parts = NUMTOKCLS = None
        best = None
        # try operators: opchars, space-x, and '%' + ' of ' form
        pat_op = r"(?:[" + OPCHARS + r"-]|\s[xX]\s|\s[oO][fF]\s)"
        for L in range(6, 0, -1):
            pat = re.compile(r"(?:" + LHS_NUM + r"\s*" + pat_op + r"\s*){1," + str(L) + "}" + LHS_NUM + r"\s*$")
            m = pat.search(window)
            if m:
                cand = m.group(0)
                # 'of' is an operator only after a percent operand
                if re.search(r"\s[oO][fF]\s", cand):
                    if not re.search(r"\d\s*%\s*[oO][fF]", cand):
                        continue
                best = cand
                break
        return best

    for eq in re.finditer(r"=|equals", text):
        s, epos = eq.start(), eq.end()
        if any(a <= s < b for a, b in covered):
            continue
        window = merge_space_thousands(text[max(0, s - 90):s])
        pre = re.search(LHS_NUM + r"\s*(?:[" + OPCHARS + r"-]|\s[xX]\s)\s*" + LHS_NUM, window)
        pre_of = re.search(r"\d\s*%\s*[oO][fF]\s+" + LHS_NUM, window)
        if not (pre or pre_of):
            continue
        lhs = lhs_of(window)
        rest = re.sub(r"^[\s\$]+", "", text[epos:])
        rest = merge_space_thousands(rest)
        ann = None
        if rest.startswith("<<"):
            close = rest.find(">>")
            if close == -1:
                continue
            ann = rest[: close + 2]
            rest = re.sub(r"^[\s\$]+", "", rest[close + 2:])
        mres = re.match(NUMTOK, rest)
        nxt = rest[mres.end():mres.end() + 1] if mres else ""
        after = rest[mres.end():mres.end() + 4].lstrip() if mres else ""
        eqchain = bool(re.match(r"[" + OPCHARS + r"\-xX]", after))
        if eqchain:
            false_parses.append({"family": "inline", "reason": "equivalence-chain",
                                 "window": window[-60:], "rhs": rest[:40]})
        elif mres and (nxt == "" or not (nxt.isdigit() or nxt == ",")):
            rhs_raw = mres.group(0)
            st, sd, _ = parse_num(rhs_raw)
            tok = tokenize_expr(lhs) if lhs else None
            if lhs is None:
                false_parses.append({"family": "inline", "reason": "lhs-not-arith",
                                     "window": window[-60:], "rhs": rhs_raw[:40]})
            elif tok is None:
                false_parses.append({"family": "inline", "reason": "malformed-number",
                                     "lhs": lhs[:80], "rhs": rhs_raw[:40]})
            elif st is None:
                false_parses.append({"family": "inline", "reason": "malformed-result",
                                     "lhs": lhs[:80], "rhs": rhs_raw[:40]})
            else:
                nums, ops = tok
                v = verify(nums, ops, st, sd)
                statements.append({"family": "inline", "nums": nums, "ops": ops,
                                   "stated": str(st), "verdict": v, "pos": s,
                                   "raw": (lhs[-40:] + " = " + rhs_raw)[:160],
                                   "ann": bool(ann)})
        else:
            false_parses.append({"family": "inline", "reason": "no-parseable-result",
                                 "window": window[-60:], "rhs": rest[:40]})
    return statements, false_parses

# ---------------- answer extraction ----------------
def extract_answer(text):
    for pat, meth in ((r"####\s*[\$]?([\d,]+(?:\.\d+)?)", "hash"),
                      (r"answer\s+is[:\s]*[\$]?([\d,]+(?:\.\d+)?)", "answer-is")):
        m = re.search(pat, text, re.I)
        if m:
            f, _, _ = parse_num(m.group(1))
            if f is not None:
                return f, meth
    nums = re.findall(r"[\$]?([\d,]+(?:\.\d+)?)", text)
    if nums:
        f, _, _ = parse_num(nums[-1])
        if f is not None:
            return f, "last-number"
    return None, "none"

# ---------------- per-document pass ----------------
def process_doc(rec):
    text = rec["gen_text"]
    stmts, fps = extract_statements(text)
    slips = [x for x in stmts if x["verdict"] is False]
    passing = [x for x in stmts if x["verdict"] is True]
    verified = set()
    for x in passing:
        verified.add(Fraction(x["stated"]))
        for ex in (evaluate(x["nums"], x["ops"]) or set()):
            verified.add(ex)
    ans, ans_method = extract_answer(text)
    traced = (ans is not None) and (ans in verified)
    order = sorted(stmts, key=lambda x: x["pos"])
    pf = {id(x): (i / (len(order) - 1) if len(order) > 1 else 0.5) for i, x in enumerate(order)}
    for x in slips:
        x["posfrac"] = pf[id(x)]
    return {
        "doc_id": rec["doc_id"], "key": rec["key"], "stop_reason": rec["stop_reason"],
        "label_correct": labels.get(rec["doc_id"]),
        "n_candidates": len(stmts) + len(fps),
        "n_wellformed": len(stmts),
        "n_slips": len(slips),
        "n_false_parses": len(fps),
        "n_inline": len([x for x in stmts if x["family"] == "inline"]),
        "n_scratchpad": len([x for x in stmts if x["family"] == "scratchpad"]),
        "slips": [{"raw": x["raw"], "nums": x["nums"], "ops": x["ops"],
                   "stated": x["stated"], "family": x["family"],
                   "posfrac": round(x["posfrac"], 3)} for x in slips],
        "false_parse_examples": fps[:5],
        "answer": str(ans) if ans is not None else None,
        "answer_method": ans_method,
        "provenance_traced": traced if ans is not None else None,
        "n_verified_values": len(verified),
    }

docs = [process_doc(r) for r in raw_recs]

# ---------------- aggregates ----------------
def agg(sel, docs=docs):
    sub = [d for d in docs if sel(d)]
    st = sum(d["n_wellformed"] for d in sub)
    sl = sum(d["n_slips"] for d in sub)
    return {"docs": len(sub), "statements": st, "slips": sl,
            "slip_rate": (sl / st) if st else None,
            "docs_with_slip": sum(1 for d in sub if d["n_slips"] > 0)}

tot = agg(lambda d: True)
fam = {"inline": agg(lambda d: d["n_inline"] > 0 and d["n_scratchpad"] == 0),
        "scratchpad": agg(lambda d: d["n_scratchpad"] > 0 and d["n_inline"] == 0),
        "mixed": agg(lambda d: d["n_inline"] > 0 and d["n_scratchpad"] > 0)}

m1 = {
    "candidates": sum(d["n_candidates"] for d in docs),
    "wellformed": sum(d["n_wellformed"] for d in docs),
    "false_parses": sum(d["n_false_parses"] for d in docs),
}
m1["precision"] = m1["wellformed"] / m1["candidates"]
m1["false_parse_census"], m1["worked_examples"] = Counter(), []
for d in docs:
    for fp in d["false_parse_examples"]:
        m1["false_parse_census"][fp.get("reason", "?")] += 1
        if len(m1["worked_examples"]) < 20:
            m1["worked_examples"].append(fp)

m2 = {
    "statements": tot["statements"], "slips": tot["slips"],
    "slip_rate": tot["slip_rate"],
    "docs_with_any_statement": sum(1 for d in docs if d["n_wellformed"] > 0),
    "docs_with_slip": tot["docs_with_slip"],
    "position": {"early": 0, "late": 0},
    "slip_examples": [],
    "by_family": fam,
}
for d in docs:
    for x in d["slips"]:
        m2["position"]["early" if x["posfrac"] < 0.5 else "late"] += 1
        if len(m2["slip_examples"]) < 20:
            m2["slip_examples"].append({"doc": d["doc_id"], "label": d["label_correct"], **x})
wrong = [d for d in docs if d["label_correct"] is False]
correct = [d for d in docs if d["label_correct"] is True]
slipdocs = [d for d in docs if d["n_slips"] > 0]
m2["label_join"] = {
    "wrong_docs_with_slip": sum(1 for d in wrong if d["n_slips"] > 0) / len(wrong),
    "correct_docs_with_slip": sum(1 for d in correct if d["n_slips"] > 0) / len(correct),
    "finish_wrong_given_slip": sum(1 for d in slipdocs if d["label_correct"] is False) / len(slipdocs),
    "finish_wrong_corpus_base": len(wrong) / len(wrong + correct),
    "wrong_rate_docs_no_slip": (lambda ns: sum(1 for d in ns if d["label_correct"] is False) / len(ns) if ns else None)([d for d in docs if d["n_wellformed"] > 0 and d["n_slips"] == 0]),
}

ans_docs = [d for d in docs if d["answer"] is not None]
viol = [d for d in ans_docs if not d["provenance_traced"]]
m3 = {
    "docs_with_extracted_answer": len(ans_docs),
    "answer_method_census": dict(Counter(d["answer_method"] for d in ans_docs)),
    "violations": len(viol),
    "violation_rate": len(viol) / len(ans_docs),
    "violations_no_chain_at_all": sum(1 for d in viol if d["n_verified_values"] == 0),
    "label_join": {
        "wrong_violation_rate": sum(1 for d in viol if d["label_correct"] is False) / len(wrong),
        "correct_violation_rate": sum(1 for d in viol if d["label_correct"] is True) / len(correct),
    },
    "examples": [{"doc": d["doc_id"], "label": d["label_correct"], "answer": d["answer"],
                  "n_verified": d["n_verified_values"], "method": d["answer_method"]}
                 for d in viol[:12]],
}

import statistics
def auc(pos, neg):
    allv = pos + neg
    order = sorted(allv)
    ranks, i = {}, 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and order[j + 1] == order[i]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    n1, n2 = len(pos), len(neg)
    return (sum(ranks[v] for v in pos) - n1 * (n1 + 1) / 2) / (n1 * n2) if n1 and n2 else None

def sep(statf):
    sp = [statf(d) for d in wrong]
    sc = [statf(d) for d in correct]
    mp, mc = statistics.mean(sp), statistics.mean(sc)
    vp = statistics.pvariance(sp)
    vc = statistics.pvariance(sc)
    pooled = math.sqrt((vp + vc) / 2) or 1e-12
    gap = (mp - mc) / pooled
    return {"sigma_gap": gap, "auc": auc(sp, sc), "mean_wrong": mp,
            "mean_correct": mc, "meets_2sigma": gap >= 2.0}

m4 = {
    "population": {"labeled_docs": len(wrong) + len(correct), "wrong": len(wrong), "correct": len(correct)},
    "n_slips_docscore": sep(lambda d: d["n_slips"]),
    "has_slip_flag": {**sep(lambda d: 1.0 if d["n_slips"] > 0 else 0.0),
                      "wrong_docs_flagged": sum(1 for d in wrong if d["n_slips"] > 0),
                      "correct_docs_flagged": sum(1 for d in correct if d["n_slips"] > 0)},
    "content_flag_slip_or_provenance": {**sep(lambda d: 1.0 if (d["n_slips"] > 0 or d["provenance_traced"] is False) else 0.0),
                                        "wrong_docs_flagged": sum(1 for d in wrong if d["n_slips"] > 0 or d["provenance_traced"] is False),
                                        "correct_docs_flagged": sum(1 for d in correct if d["n_slips"] > 0 or d["provenance_traced"] is False)},
    "note": "checker authority is oracle-based; M4 describes corpus coverage only (R-P4)",
}

loop_stats = []
for r in loop_recs:
    st, fp = extract_statements(r["gen_text"])
    loop_stats.append({"doc_id": r["doc_id"], "n_wf": len(st),
                       "n_slips": len([x for x in st if x["verdict"] is False])})

out = {
    "pass": "arithmetic_checker_offline_pass_3b",
    "tool": "triadic_checker_offline_pass_3b.py (the 1B v2 tool logic verbatim, 3B input block; standalone, no version stamp)",
    "adjudicated_per": "checker-offline-pass-preregistration.md (stamped by me Oct 6 2026)",
    "rules": {
        "candidate": "a '='/'equals' anchor whose lhs window (90 chars) shows NUM-op-NUM (the in-line detector's trigger gate), plus every '<<expr=result>>' scratchpad annotation",
        "wellformed": "lhs parses as 2+ numbers joined by arithmetic ops ('x' and 'N% of M' included; % operands valued at n/100); result token parses; comma/decimal grouping valid",
        "slip": "stated result differs from the exact recomputation (Fraction arithmetic) by more than half a display unit at the stated precision, under EITHER standard precedence or left-to-right evaluation",
        "provenance": "final answer must equal a verified chain value (stated results of passing statements or their exact recomputed values); '####' first, then 'answer is', then last number",
        "known_limitations_censused_not_hidden": "dimensional forms ('12 miles / 12 hours'), fraction operands ('20/3'), parenthesized rhs — counted as false parses; they are missed-statement classes, never false fires",
        "inputs_read_only": True, "model_involvement": "none",
    },
    "inputs": {
        "raw_leg_generations": f"t2gen3b_part??.jsonl ({len(_part_files)} files, rejoined {len(_rejoined)} bytes, SHA-256 {_rejoin_sha} — the 3B re-walk's thin generations at tag t2-gsm-full-3b)",
        "raw_leg_labels": f"triadic_t2_t2-gsm-full-3b.json per_doc label_correct (1,319 docs; {sum(1 for v in labels.values() if v)} correct — the 3B walk's OWN exact-match measurement vs the same gold)",
        "chat_leg": {"status": "SEPARATE FORK", "detail": "the 3B chat leg runs triadic_checker_offline_pass_chat_3b.py on t2chat_gsm-chat100-3b_thin.jsonl; the 1B chat record stays frozen at its banked export"},
    },
    "corpus": {"raw_leg_docs": len(docs), "loop_leg_docs_excluded_from_rates": 10},
    "M1_extraction_precision": {**m1, "false_parse_census": dict(m1["false_parse_census"])},
    "M2_slip_rate": {k: (v if not isinstance(v, Counter) else dict(v)) for k, v in m2.items()},
    "M3_answer_provenance": m3,
    "M4_retroactive_separation": m4,
    "loop_leg_color": loop_stats,
    "per_doc": docs,
}
json.dump(out, open(WORK / "triadic_checker_offline_pass_3b.json", "w"), indent=1)

print("=== ARITHMETIC CHECKER OFFLINE PASS 3B (raw leg; chat leg = the sibling fork) ===")
print(f"M1 candidates={m1['candidates']} wellformed={m1['wellformed']} false_parses={m1['false_parses']} precision={m1['precision']:.4f}")
print(f"M1 census: {dict(m1['false_parse_census'])}")
print(f"M2 statements={tot['statements']} slips={tot['slips']} rate={tot['slip_rate']:.5f} docs_with_slip={tot['docs_with_slip']}/{tot['docs']}")
print(f"M2 families: {fam}")
print(f"M2 position: {m2['position']}")
print(f"M2 label join: wrong_with_slip={m2['label_join']['wrong_docs_with_slip']:.4f} correct_with_slip={m2['label_join']['correct_docs_with_slip']:.4f} finish_wrong_given_slip={m2['label_join']['finish_wrong_given_slip']:.4f} base={m2['label_join']['finish_wrong_corpus_base']:.4f} no_slip_wrong_rate={m2['label_join']['wrong_rate_docs_no_slip']:.4f}")
print(f"M3 answers={len(ans_docs)} violations={len(viol)} rate={m3['violation_rate']:.4f} no_chain={m3['violations_no_chain_at_all']} methods={m3['answer_method_census']}")
print(f"M3 wrong viol={m3['label_join']['wrong_violation_rate']:.4f} correct viol={m3['label_join']['correct_violation_rate']:.4f}")
print(f"M4 slip-score sigma_gap={m4['n_slips_docscore']['sigma_gap']:.3f} auc={m4['n_slips_docscore']['auc']:.4f}")
print(f"M4 slip-flag: wrong {m4['has_slip_flag']['wrong_docs_flagged']}/{len(wrong)} correct {m4['has_slip_flag']['correct_docs_flagged']}/{len(correct)} sigma_gap={m4['has_slip_flag']['sigma_gap']:.3f} auc={m4['has_slip_flag']['auc']:.4f}")
print(f"M4 content-flag: wrong {m4['content_flag_slip_or_provenance']['wrong_docs_flagged']}/{len(wrong)} correct {m4['content_flag_slip_or_provenance']['correct_docs_flagged']}/{len(correct)} sigma_gap={m4['content_flag_slip_or_provenance']['sigma_gap']:.3f} auc={m4['content_flag_slip_or_provenance']['auc']:.4f}")
print(f"loop leg color: {loop_stats}")

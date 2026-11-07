#!/usr/bin/env python3
"""rw17_thin_extract_acceptance_run.py -- the acceptance suite for
triadic_t2_thin_extract.py (the item-253 upload lane). Every check is
an INDEPENDENT recomputation or a hard-exit probe; the fixture world
is a synthetic cache carrying the readout-class schema verbatim
(REQUIRED_RECORD_FIELDS + REQUIRED_STEP_FIELDS replicated from the
banked triadic_rw17_sec_baseline.py bytes -- cited, never modified).
Zero-GPU, zero-model, zero-network.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "triadic_t2_thin_extract.py")

# the readout-class schema of record (verified against the banked
# triadic_rw17_sec_baseline.py bytes; replicated verbatim here)
REQUIRED_RECORD_FIELDS = ("key", "leg", "doc_id", "bos", "instrument",
                          "prompt_len", "stop_reason", "n_gen_steps",
                          "n_content_steps", "walk_ids",
                          "steps", "commits", "hidden_n", "hidden_dim",
                          "hidden_b64")
REQUIRED_STEP_FIELDS = ("t", "id", "E", "rho", "s", "f", "layer", "H",
                        "PR", "a", "rsize", "dead5", "dead4", "dead3",
                        "dead_share")

PASS, FAIL = 0, 0


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  PASS  %s" % name)
    else:
        FAIL += 1
        print("  FAIL  %s %s" % (name, detail))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def step_row(t):
    return {"t": t, "id": 100 + t, "E": 2.5 - t * 0.1, "rho": 0.4,
            "s": 1.1, "f": 0.02 * t, "layer": 15, "H": 3.2,
            "PR": 0.01 + 0.005 * t, "a": 0.9, "rsize": 12,
            "dead5": 0.1, "dead4": 0.2, "dead3": 0.3,
            "dead_share": 0.25}


def full_rec(leg, did, n_steps, b64_len):
    rec = {"key": "%s:%d" % (leg, did), "leg": leg, "doc_id": did,
           "bos": True, "instrument": "v32.2.2", "prompt_len": 24,
           "stop_reason": "eos" if n_steps else "length",
           "n_gen_steps": n_steps, "n_content_steps": max(0, n_steps - 1),
           "walk_ids": [100 + i for i in range(n_steps)],
           "steps": [step_row(t) for t in range(n_steps)],
           "commits": [{"t": 0, "phase": "CoT", "emitted_p": 0.9,
                        "margin": 0.4}] if n_steps else [],
           "hidden_n": n_steps, "hidden_dim": 2048,
           "hidden_b64": "A" * b64_len if n_steps else ""}
    return rec


def run_tool(cache_path, out_path):
    return subprocess.run([sys.executable, TOOL, cache_path, out_path],
                          capture_output=True, text=True)


def main():
    tmp = tempfile.mkdtemp()
    cache = os.path.join(tmp, "fake_cache.jsonl")
    lines = []
    originals = []
    for rec in (full_rec("gsmrw17", 0, 4, 400),
                full_rec("gsmrw17", 1, 2, 300),
                full_rec("gsmrw17", 2, 0, 0),       # zero-step record
                full_rec("mbpprw17", 0, 3, 500),
                full_rec("mbpprw17", 1, 1, 200),
                {"key": "mbpprw17:9", "empty": True, "bos": True}):
        line = json.dumps(rec)
        lines.append(line)
        originals.append(rec)
    with open(cache, "w") as f:
        f.write("\n".join(lines) + "\n")
    cache_sha_before = sha256_file(cache)

    out = os.path.join(tmp, "thin.jsonl")
    r = run_tool(cache, out)
    cout = r.stdout + r.stderr
    check("F1 the tool runs clean (returncode 0)", r.returncode == 0,
          cout)

    thin_lines = [l for l in open(out).read().splitlines() if l.strip()]
    check("F2 record census: 6 thin lines", len(thin_lines) == 6,
          str(len(thin_lines)))

    # F3: the thin record law -- everything unchanged except the two
    # declared changes; serialization byte-canonical (writer format)
    ok_fields, ok_order, ok_canon = True, True, True
    for orig, tl in zip(originals, thin_lines):
        thin = json.loads(tl)
        if thin.get("empty"):
            continue
        for k, v in orig.items():
            if k == "hidden_b64":
                continue
            if thin.get(k) != v:
                ok_fields = False
        if thin.get("hidden_b64") != "" or thin.get("thin") is not True:
            ok_fields = False
        exp_order = list(orig.keys()) + ["thin"]
        if list(thin.keys()) != exp_order:
            ok_order = False
        if json.dumps(thin) != tl:
            ok_canon = False
    check("F3a every field rides unchanged; hidden_b64 == \"\"; "
          "thin: true", ok_fields)
    check("F3b key order preserved + thin appended last", ok_order)
    check("F3c serialization byte-canonical (the cache-writer format)",
          ok_canon)

    # F4: empty-form records pass through byte-identically, unmarked
    empty_orig = json.dumps(originals[5])
    check("F4 empty-form pass-through byte-identical, no marker",
          thin_lines[5] == empty_orig, thin_lines[5])

    # F5: the zero-step record rides the same law (hidden_n 0)
    zr = json.loads(thin_lines[2])
    check("F5 zero-step record: hidden_n 0, hidden_b64 \"\", thin true",
          zr["hidden_n"] == 0 and zr["hidden_b64"] == ""
          and zr["thin"] is True)

    # F6: the readout-class schema law passes on every non-empty thin
    ok_schema = True
    for tl in thin_lines:
        rec = json.loads(tl)
        if rec.get("empty"):
            continue
        miss = [fl for fl in REQUIRED_RECORD_FIELDS if fl not in rec]
        if miss:
            ok_schema = False
        for st in rec["steps"]:
            sm = [fl for fl in REQUIRED_STEP_FIELDS if fl not in st]
            if sm:
                ok_schema = False
    check("F6 REQUIRED_RECORD_FIELDS + REQUIRED_STEP_FIELDS present "
          "on every thin record (the readout-class loader law passes)",
          ok_schema)

    # F7: the cache is READ-ONLY (bytes unchanged)
    check("F7 read-only: cache SHA unchanged by the run",
          sha256_file(cache) == cache_sha_before)

    # F8: the console receipts (SHAs + census lines)
    check("F8a console carries the cache SHA receipt",
          cache_sha_before in cout, cout)
    check("F8b console census: 6 records, legs {'gsmrw17': 3, "
          "'mbpprw17': 3}", "census: 6 records (legs {'gsmrw17': 3, "
          "'mbpprw17': 3}); 1 empty-form pass-through" in cout, cout)
    check("F8c console census: 10 per-step rows carried",
          "census: 10 per-step rows carried" in cout, cout)

    # F9: determinism -- same-path rerun byte-identical + console
    snap = open(out, "rb").read()
    r2 = run_tool(cache, out)
    check("F9a same-path rerun byte-identical",
          open(out, "rb").read() == snap)
    c1 = run_tool(cache, os.path.join(tmp, "t1.jsonl")).stdout
    c2 = run_tool(cache, os.path.join(tmp, "t1.jsonl")).stdout
    check("F9b the console deterministic on a same-path rerun", c1 == c2)

    # F10: the truncated-line named hard exit
    trunc = os.path.join(tmp, "trunc.jsonl")
    shutil.copy(cache, trunc)
    with open(trunc, "a") as f:
        f.write('{"key": "gsmrw17:3", "leg": "gsmrw17"')  # truncated
    r3 = run_tool(trunc, os.path.join(tmp, "never.jsonl"))
    check("F10 truncated line -> named hard exit (file + line number)",
          r3.returncode != 0 and "truncated/malformed JSON" in
          r3.stdout + r3.stderr and "line 7" in r3.stdout + r3.stderr,
          r3.stdout + r3.stderr)

    print()
    print("THIN EXTRACT ACCEPTANCE: %d PASS / %d FAIL" % (PASS, FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

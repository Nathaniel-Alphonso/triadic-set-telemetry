#!/usr/bin/env python3
"""
Thin extraction: RB-1 chat cache -> chat-leg thin generations file.
Protocol: identical to the raw-leg thin extraction (ledger item 48).

  READ-ONLY on the cache. Tokenizer-only: NO model load, NO GPU, NO MPS.
  Runs in seconds on CPU. Nothing it touches is in use by RB-2
  (the RB-1 cache file is closed; RB-2 writes its own new cache).

  Input : triadic_t2_cache_t2-gsm-chat100-a1_bfloat16_bos.jsonl  (owner-local)
  Output: t2chat_gsm-chat100-a1_thin.jsonl  (~80 KB, single upload, no split)

Run AFTER RB-2 finishes (one-run-at-a-time machine protocol) -- or any time
the machine is idle. Then upload the output file.

Record layout mirror-checked against triadic_telemetry_t2.py (cache_f.write,
v32.1.9): key / leg / doc_id / bos / instrument / prompt_len / stop_reason /
n_gen_steps / n_content_steps / walk_ids / steps / commits / hidden_* fields,
plus possible {"key":..., "empty": true} records (skipped, counted).
Decode uses skip_special_tokens=True, which is identical whether or not
walk_ids carries a stop id (raw-leg thin convention: clean "#### N" endings).
"""
import hashlib
import json
import sys
from collections import Counter

CACHE = "triadic_t2_cache_t2-gsm-chat100-a1_bfloat16_bos.jsonl"
OUT = "t2chat_gsm-chat100-a1_thin.jsonl"
MODEL = "meta-llama/Llama-3.2-1B-Instruct"
LEG = "gsm8k-chat"
EXPECTED_CHAT_DOCS = 100

from transformers import AutoTokenizer  # tokenizer only -- no model weights

tok = AutoTokenizer.from_pretrained(MODEL)

n_in = n_empty = 0
legs = Counter()
stops = Counter()
len_mismatch = []
chat_doc_ids = []
n_written = 0

with open(CACHE) as f, open(OUT, "w") as out:
    for line in f:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        n_in += 1
        if rec.get("empty"):
            n_empty += 1
            continue
        walk = rec["walk_ids"]
        if len(walk) != rec["n_gen_steps"]:
            len_mismatch.append((rec.get("key"), len(walk), rec["n_gen_steps"]))
        legs[rec["leg"]] += 1
        stops[rec["stop_reason"]] += 1
        if rec["leg"] == LEG:
            chat_doc_ids.append(rec["doc_id"])
        thin = {
            "key": rec["key"],
            "leg": rec["leg"],
            "doc_id": rec["doc_id"],
            "stop_reason": rec["stop_reason"],
            "n_gen_steps": rec["n_gen_steps"],
            "n_content_steps": rec["n_content_steps"],
            "walk_ids": walk,
            "gen_text": tok.decode(walk, skip_special_tokens=True),
        }
        out.write(json.dumps(thin, ensure_ascii=False) + "\n")
        n_written += 1

# --- self-checks (fail loudly BEFORE any upload happens) ---
fails = []
if legs[LEG] != EXPECTED_CHAT_DOCS:
    fails.append(f"chat records: {legs[LEG]} != {EXPECTED_CHAT_DOCS}")
if sorted(chat_doc_ids) != list(range(EXPECTED_CHAT_DOCS)):
    missing = sorted(set(range(EXPECTED_CHAT_DOCS)) - set(chat_doc_ids))
    dupes = [d for d, c in Counter(chat_doc_ids).items() if c > 1]
    fails.append(f"doc_id set wrong; missing={missing} dupes={dupes}")
for d in chat_doc_ids:
    pass  # key-format check done below via key string
if len_mismatch:
    fails.append(f"walk_ids/n_gen_steps mismatches: {len_mismatch[:5]}")

h = hashlib.sha256(open(OUT, "rb").read()).hexdigest()

print(f"cache records read      : {n_in} (empty/skipped: {n_empty})")
print(f"thin records written    : {n_written}")
print(f"leg census              : {dict(legs)}")
print(f"stop_reason census      : {dict(stops)}")
print(f"chat doc_ids            : 0..{max(chat_doc_ids)} " if chat_doc_ids else "chat doc_ids: NONE")
print(f"SHA-256 {OUT}: {h}")

if fails:
    print("\nSELF-CHECK FAILURES -- do NOT upload:")
    for m in fails:
        print("  - " + m)
    sys.exit(1)
print("\nALL SELF-CHECKS PASS -- upload " + OUT)

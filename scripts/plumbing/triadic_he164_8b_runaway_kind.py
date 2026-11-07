#!/usr/bin/env python3
"""triadic_he164_8b_runaway_kind.py -- HE164-8B RUNAWAY-KIND LOOK
(the code arm's optional decode-side read; read-only; writes nothing)

WHY: the meter readings (ledger item 923) named the corpus's entire
runaway mass doc-by-doc: docs 147 + 138 completed at 106,375,790 and
52,564,056 instructions (both PASS) and docs 36 + 100 were killed at
count-at-kill lower bounds near 700M (both UNVERIFIED-TIMEOUT). The
walk-side join (item 919) showed their walk profiles ordinary -- the
kind lives in the generated text itself. This tool prints the four
docs' full generated blocks straight from the dump of record plus a
repetition census per doc, so the kind is read from the actual bytes,
never summarized away, never adjudicated.

LAW: the dump is sha-pinned at load (the dump of record); fail-loud on
every shape assumption; zero writes; zero GPU; zero decodes (the dump
already holds text). Run bare from inside the directory holding the
dump (triadic_generations_humaneval_he164-8b.json).
"""

import hashlib
import json
import os
import sys
from collections import Counter

DUMP = "triadic_generations_humaneval_he164-8b.json"
DUMP_SHA256 = ("6191986db5a2c4bbb764aa3019a36385aa71bbe0f2941d0c"
               "1d5ec7ba424e32da")
N_DOCS = 164
RUNAWAY_DOCS = (36, 100, 147, 138)
VERDICTS = {36: "UNVERIFIED-TIMEOUT", 100: "UNVERIFIED-TIMEOUT",
            147: "PASS", 138: "PASS"}


def die(msg):
    print("VOID: " + msg)
    sys.exit(1)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(DUMP):
        die("the dump %s is not present in this directory ([Errno 2]"
            " No such file or directory) -- run me from inside the"
            " directory holding the dump of record; aborting, never"
            " guessing." % DUMP)
    actual = sha256_file(DUMP)
    if actual != DUMP_SHA256:
        die("the dump %s hashes to %s, the pinned sha is %s -- the"
            " generated blocks must come from the dump of record;"
            " aborting, never guessing." % (DUMP, actual, DUMP_SHA256))
    with open(DUMP, encoding="utf-8") as f:
        docs = json.load(f)
    if not isinstance(docs, list) or len(docs) != N_DOCS:
        die("the dump holds %s records, expected %d -- this tool is"
            " pinned to the he164-8b dump of record; aborting."
            % (len(docs) if isinstance(docs, list) else type(docs),
               N_DOCS))
    byid = {}
    for d in docs:
        if "doc_id" not in d or "generated" not in d:
            die("a dump record lacks doc_id/generated -- the record"
                " does not match the dump schema; aborting.")
        byid[d["doc_id"]] = d
    if sorted(byid) != list(range(N_DOCS)):
        die("the dump's doc set is not exactly 0..%d; aborting, never"
            " guessing." % (N_DOCS - 1))
    for doc in RUNAWAY_DOCS:
        if doc not in byid:
            die("runaway doc %d is missing from the dump; aborting."
                % doc)

    print("HE164-8B RUNAWAY-KIND LOOK (read-only decode-side read;"
          " writes nothing)")
    print("  dump         : %s sha %s (pin VERIFIED)" % (DUMP, actual))
    print("  runaway docs : %s (the item-923 census of the runaway"
          " mass)" % (RUNAWAY_DOCS,))
    print("  verdicts     : %r (the banked census of record)" % (VERDICTS,))
    print("")
    for doc in RUNAWAY_DOCS:
        d = byid[doc]
        gen = d["generated"]
        lines = gen.splitlines()
        nonempty = [l.strip() for l in lines if l.strip()]
        counts = Counter(nonempty)
        print("=" * 72)
        print("DOC %d  (%s)  generated_len_tokens=%s  chars=%d  lines=%d"
              % (doc, VERDICTS[doc], d.get("generated_len_tokens"),
                 len(gen), len(lines)))
        print("-- repetition census (most-repeated non-empty lines):"
              " distinct %d of %d" % (len(counts), len(nonempty)))
        for text, n in counts.most_common(5):
            print("   %4dx  %r" % (n, text[:90]))
        print("-- the full generated block:")
        print("---- doc %d generated (start) ----" % doc)
        print(gen)
        print("---- doc %d generated (end) ----" % doc)
        print("")
    print("ALL SELF-CHECKS PASS -- paste this whole console; the kinds"
          " are read from the bytes, presented never adjudicated.")


if __name__ == "__main__":
    main()

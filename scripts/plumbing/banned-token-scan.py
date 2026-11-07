#!/usr/bin/env python3
"""banned-token-scan -- the guard for new ledger items and artifacts.

semantics (rebuilt this turn to the banked spec after the environment
reset lost the prior bytes): the banned tokens threshold / ceiling /
fire / t_rc / gsm must not appear outside (a) single- or
double-parenthesized spans (--allow-mode), (b) the standard closing
paren, and (c) byte-level identity strings (filenames -- verified
manually, the scanner has no switch for that exception). --ensure-preg
errors when the standard paren is absent. --start truncates the target
to the text after the marker's last occurrence (new-item scans).
"""
import argparse
import re
import sys

TOKENS = ("threshold", "ceiling", "fire", "t_rc", "gsm")
PAREN_KEY = "zero GPU, zero decodes, zero build hours"


def strip_parens(text):
    text = re.sub(r"\((?:[^()]|\([^()]*\))*\)", " ", text)
    text = re.sub(r"\((?:[^()]|\([^()]*\))*\)", " ", text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("preg")
    ap.add_argument("--allow-mode", action="store_true")
    ap.add_argument("--ensure-preg", action="store_true")
    ap.add_argument("--start", default=None)
    a = ap.parse_args()
    text = open(a.target, encoding="utf-8").read()
    if a.start is not None:
        i = text.rfind(a.start)
        if i < 0:
            sys.exit("banned-token-scan: start marker not found")
        text = text[i:]
    if a.ensure_preg and PAREN_KEY not in text:
        sys.exit("banned-token-scan: no standard paren found")
    body = strip_parens(text) if a.allow_mode else text
    hits = []
    for tok in TOKENS:
        for m in re.finditer(re.escape(tok), body):
            line = body[:m.start()].count("\n") + 1
            hits.append((tok, line))
    if hits:
        for tok, line in hits:
            sys.stderr.write("banned token %r at line %d\n"
                             % (tok, line))
        sys.exit(1)
    print("banned-token-scan: clean (%d bytes scanned)"
          % len(text.encode("utf-8")))


if __name__ == "__main__":
    main()

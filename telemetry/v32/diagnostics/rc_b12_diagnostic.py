#!/usr/bin/env python3
"""THE B1/B2 PHASE-LANE DIAGNOSTIC -- the rc-b12-phaselane-prereg.md S6 act.

At my word ("okay continue wuth the next step") the pinned sheet's
diagnostic runs: the phase-band pooling (B1, the PRIMARY read) and the
line-synced anchor (B2, the SECONDARY read), each form carried to ITS
OWN pre-registered verdict, never a post-read selection -- the fixture
census FIRST (the item-487 within-loop ordering law: the ten fixtures
read BEFORE the corpus is ever consulted; code-line failing to re-form
on BOTH forms on the judged leg closes the sheet ON PAPER at the first
gate, ZERO corpus reads), then the parity gates, then the corpus half
only on an ordering survival (the raw census parity gate, the B-face
census, the flood census -- the A2 kill, the level race, the spine
read D_new = max(D, z_refined, z_Bface), the honest both-sides gap per
gate per form, the off-leg reads, the kill-switch verdicts), presented
never adjudicated.

TWO MODES (the codev7 genre):
  --parity-only : the receipt-side gates alone, NO caches needed (the
                  desk's half, runnable anywhere beside the receipt +
                  tool + the pinned sheet);
  (default)     : the full diagnostic -- MY MAC, read-only, zero GPU,
                  zero model decodes, the script beside
                  triadic_rw17_codev5.py + rc_codev5_receipt.json +
                  the pinned sheet + my three pinned walk caches,
                  and the newline token id(s) either passed as
                  --newline-ids ID[,ID] or resolvable from a
                  tokenizer.json / vocab.json beside the script (a
                  static vocabulary table read, zero model decodes,
                  zero GPU); emits rc_b12_diagnostic_console.txt for
                  my shasum + upload.

usage: python3 rc_b12_diagnostic.py --parity-only   (the desk half)
       python3 rc_b12_diagnostic.py --newline-ids 198   (my Mac, full)
"""

import json
import os
import sys
import importlib.util

TOOL_NAME = "triadic_rw17_codev5.py"
TOOL_SHA_BANK = ("391ac7dfd91f4c45c7c113211005a8bb44565737"
                 "887331fd512ed9723b4c2cf3")
RECEIPT_NAME = "rc_codev5_receipt.json"
RECEIPT_SHA_BANK = ("fc8b70b5435cefbc419b3b10dd0aeae6b579dcad1b"
                    "7bfcaac5d11660b6e6cc42")
SHEET_NAME = "rc-b12-phaselane-prereg.md"
SHEET_SHA = ("0eeb2991d47b3d8fff9e412be7fd368f0fa9f9024444176"
             "e614f8fcf9acf72d8")
PARITY_CONSOLE = "rc_b12_parity_console.txt"
FULL_CONSOLE = "rc_b12_diagnostic_console.txt"

D2_GATES = (8, 12, 16)                # the swept support floor (receipts)
JUDGED_LEG = "mbpprw17"              # the gate read's leg, never the off-legs
CLUB = ("loop-injection-code", "loop-seeded-json",
        "loop-seeded-chant", "loop-seeded-countdown")
CODE_LINE = "loop-seeded-code-line"
CODE_LINE_MIN_BANK = 0.0454          # my banked raw minimum (item 497)
PARITY_TOL = 1e-12
LEVEL_BANK = 3.7618410048243147       # the standing V5 level
GAP_BANK = 1.6862617412521999        # the standing V5 honest gap
PB4_HONEST = 1.792063                # the standing best banked CODE read
CAPS = {6: 1.6432, 7: 2.0494, 8: 2.6833}
D_MISSES = {"loop-seeded-json": 3.492749,
            "loop-seeded-countdown": 0.459473,
            "loop-seeded-code-line": 1.381425}
# the banked raw d2 census, MY consoles (items 490/493), the lineage
# anchors for the corpus half's raw census parity gate:
CEN_ANCHORS = {
    "mbpprw17": {"mean": 0.275000, "sd": 1.352227, "n_pos": 11, "n": 200,
                 "held_n_pos": 15},
    "prose17p-rw17": {"mean": 1.548387, "sd": 3.896216, "n_pos": 72,
                      "n": 310, "held_n_pos": None},
    "p2corpus-rw17": {"mean": 1.154667, "sd": 3.072663, "n_pos": 62,
                      "n": 375, "held_n_pos": None},
}
# the fixture m_d2 bank (my gate-8 reads, the judged leg):
BANKED_MD2 = {"loop-seeded-json": 8, "loop-seeded-countdown": 0,
              "loop-seeded-code-line": 0, "loop-injection-code": 21,
              "loop-seeded-chant": 0}
# the item-488 P-B4 fixture table (mbpprw17):
BANKED_REFINED = {
    "loop-seeded-countdown": 0.368124, "loop-injection-code": 0.321772,
    "mask-reserved-stubborn": 0.299363, "loop-seeded-chant": 0.258515,
    "loop-injection-prose": 0.252647, "loop-seeded-cycle": 0.212269,
    "loop-seeded-counter": 0.141779, "loop-seeded-affirm": 0.127843,
    "loop-seeded-json": 0.057367, "loop-seeded-code-line": 0.036616,
}
OFF_LEG_BOUNDS = {"prose17p-rw17": 1.753702, "p2corpus-rw17": 1.772590}
TAIL_LO, TAIL_HI = 19, 36
LATE_LO, LATE_HI = 28, 36

OUT = []


def p(s=""):
    OUT.append(s)
    print(s)


def die(msg, code=1):
    sys.stderr.write("HARD EXIT: " + msg + "\n")
    sys.exit(code)


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_tool():
    if not os.path.exists(TOOL_NAME):
        die("tool %s not found beside this script -- the diagnostic "
            "imports the tool's own curve machinery; aborting."
            % TOOL_NAME)
    spec = importlib.util.spec_from_file_location("K", TOOL_NAME)
    K = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(K)
    return K


def load_receipt():
    if not os.path.exists(RECEIPT_NAME):
        die("receipt %s not found beside this script -- the "
            "run-of-record receipt is the before-column and the parity "
            "source; aborting." % RECEIPT_NAME)
    sha = sha256_file(RECEIPT_NAME)
    if sha != RECEIPT_SHA_BANK:
        die("receipt sha256 %s != the banked run-of-record %s -- never "
            "read foreign bytes; aborting." % (sha, RECEIPT_SHA_BANK))
    with open(RECEIPT_NAME) as f:
        r = json.load(f)
    ts = r.get("tool_sha256", "")
    if ts != TOOL_SHA_BANK:
        die("receipt tool_sha256 %s != the banked tool %s -- never "
            "project onto foreign bytes; aborting." % (ts,
                                                       TOOL_SHA_BANK))
    return r


def verify_sheet():
    if not os.path.exists(SHEET_NAME):
        die("the pinned sheet %s not found beside this script -- the "
            "diagnostic reads its form ONLY from the stamped sheet; "
            "aborting." % SHEET_NAME)
    sha = sha256_file(SHEET_NAME)
    if sha != SHEET_SHA:
        die("sheet sha256 %s != the pinned %s -- never run a "
            "diagnostic whose form is unpinned; aborting."
            % (sha, SHEET_SHA))


def m_d2(d2_vals, triples, t_min):
    """the d2 zero-run mass, the item-475 law mirrored onto the B
    faces (byte-carried from the standing form of record): m = zero
    lags in runs of >= 2 consecutive supported lags (supported = d2
    not None and triples >= t_min); ISOLATED zeros NEVER count."""
    zeros = [i for i in range(len(d2_vals))
             if d2_vals[i] is not None and triples[i] >= t_min
             and d2_vals[i] == 0.0]
    zset = set(zeros)
    in_run = set()
    for i in zeros:
        if (i - 1) in zset:
            in_run.add(i)
            in_run.add(i - 1)
        if (i + 1) in zset:
            in_run.add(i)
            in_run.add(i + 1)
    return len(in_run), zeros


def refined_tail(d_vals, pair_counts, K):
    """the P-B4 form, byte-carried: refined tail = 1 - min(d over
    supported lags 19..36) / med(d over supported lags 28..36); the
    masked E curve; the tool's own support law; EMPTY named."""
    supported = [i for i in range(len(K.LAGS))
                 if d_vals[i] is not None
                 and pair_counts[i] >= K.LOW_SUPPORT_PAIRS]
    if len(supported) < K.MIN_SUPPORTED_LAGS:
        return None, "EMPTY_few_supported_lags"
    tail = [d_vals[i] for i in supported if TAIL_LO <= K.LAGS[i] <= TAIL_HI]
    late = [d_vals[i] for i in supported if LATE_LO <= K.LAGS[i] <= LATE_HI]
    if not tail or not late:
        return None, "EMPTY_no_tail_or_late_window"
    med_late = K.median_of(late)
    if not med_late > 1e-12:
        return None, "EMPTY_degenerate_med_late"
    return 1.0 - min(tail) / med_late, "OK"


def zmax(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if a >= b else b


def project(r, leg_name, z_cal, z_held, z_fix, K):
    """D_new = max(D_receipt, z) per doc; the level re-derives (quantile
    0.95 over cal D_new); the gap re-derives in the item-439
    convention; both sides re-scored identically (byte-carried)."""
    lg = r["legs"][leg_name]
    rows = lg["doc_rows"]
    cal_now, held_now = [], []
    for row in rows:
        if row["half"] == "cal" and row["D"] is not None:
            cal_now.append((row["doc_id"], row["D"]))
        elif row["half"] == "held" and row["D"] is not None:
            held_now.append((row["doc_id"], row["D"]))
    fix_now = {row["fixture"]: row["D"] for row in lg["loop_census"]}

    def lift(did, D, zmap):
        z = zmap.get(did)
        return (max(D, z) if z is not None else D), z

    cal_new = [lift(d, D, z_cal)[0] for d, D in cal_now]
    held_new = [lift(d, D, z_held)[0] for d, D in held_now]
    fix_new = {n: lift(n, D, z_fix)[0] for n, D in fix_now.items()}

    t_new = K.quantile(sorted(cal_new), 0.95)
    t_now = K.quantile(sorted(D for _, D in cal_now), 0.95)
    mu_h, sd_h = K.mean_std(held_new)
    mu_l, sd_l = K.mean_std(list(fix_new.values()))
    rms = ((sd_l ** 2 + sd_h ** 2) / 2.0) ** 0.5
    gap_new = (mu_l - mu_h) / rms if rms > 1e-12 else None
    k_new = sum(1 for v in fix_new.values() if v >= t_new)
    k_now = sum(1 for v in fix_now.values() if v >= t_now)
    demoted = sorted(n for n, v in fix_new.items()
                     if fix_now[n] >= t_now and v < t_new)
    lifted = sorted(n for n in fix_new if fix_new[n] > fix_now[n])
    return {
        "t_now": t_now, "t_new": t_new, "k_now": k_now, "k_new": k_new,
        "gap_new": gap_new, "demoted": demoted, "lifted": lifted,
        "mu_loop": mu_l, "sd_loop": sd_l, "mu_held": mu_h,
        "sd_held": sd_h, "fix_now": fix_now, "fix_new": fix_new,
    }


# ---- THE B FORMS (the pinned laws, S4 of the sheet) ------------------------
def d2_b1_curve(zs, raw_E, e_cutoff, lag_lo, lag_hi):
    """B1 the phase-band pooling, the d2 face: the EXACT-LAG
    CONSTRUCTION'S OWN OCCURRENCES (the delta=0 triples -- the same
    non-None + survival gate as the raw d2 curve, an occurrence the
    exact-lag law masks out never re-admitted by a shifted offset)
    re-pooled over the pinned band, the COHERENT PHASE WALK: d2_B1[L]
    = the mean over those occurrences of min over delta in
    {-1,0,+1} of |z_t - 2 z_{t+L+delta} + z_{t+2(L+delta)}| -- THE
    MIN BEFORE THE POSITION AVERAGE; the hold-or-fall law this pins:
    B1[L] <= raw[L] at every lag, a club exact zero HOLDS exactly;
    the survival law on the members of the SURVIVING offset (the
    offset that wins the min, all its members' raw E strictly above
    the cutoff); the band pinned by convention, never widened."""
    n = len(zs)
    out_d2, out_triples = [], []
    for L in range(lag_lo, lag_hi + 1):
        acc = 0.0
        cnt = 0
        for t in range(n - 2 * L):
            a0, b0, c0 = zs[t], zs[t + L], zs[t + 2 * L]
            if a0 is None or b0 is None or c0 is None:
                continue
            if e_cutoff is not None:
                es = (raw_E[t], raw_E[t + L], raw_E[t + 2 * L])
                if any(e is None for e in es):
                    continue
                if not all(e > e_cutoff for e in es):
                    continue
            best = abs(a0 - 2.0 * b0 + c0)
            for delta in (-1, 1):
                Lp = L + delta
                if Lp < 1 or t + 2 * Lp >= n:
                    continue
                a, b, c = zs[t], zs[t + Lp], zs[t + 2 * Lp]
                if a is None or b is None or c is None:
                    continue
                if e_cutoff is not None:
                    es = (raw_E[t], raw_E[t + Lp], raw_E[t + 2 * Lp])
                    if any(e is None for e in es):
                        continue
                    if not all(e > e_cutoff for e in es):
                        continue
                dev = abs(a - 2.0 * b + c)
                if dev < best:
                    best = dev
            acc += best
            cnt += 1
        out_d2.append(acc / cnt if cnt else None)
        out_triples.append(cnt)
    return out_d2, out_triples


def d2_b2_curve(zs, raw_E, anchors, e_cutoff, k_lo, k_hi):
    """B2 the line-synced anchor, the d2 face: the anchor-index
    recurrence d2a_B2[k] = the mean over valid i of
    |z_{a_i} - 2 z_{a_{i+k}} + z_{a_{i+2k}}| -- THE TOKEN POSITION
    NEVER CONSULTED FOR THE LAG; the survival law at the anchor
    positions; a doc without enough anchors reads EMPTY, never
    zero-filled."""
    m = len(anchors)
    out_d2, out_triples = [], []
    for k in range(k_lo, k_hi + 1):
        acc = 0.0
        cnt = 0
        for i in range(m - 2 * k):
            x, y, w = anchors[i], anchors[i + k], anchors[i + 2 * k]
            a, b, c = zs[x], zs[y], zs[w]
            if a is None or b is None or c is None:
                continue
            if e_cutoff is not None:
                es = (raw_E[x], raw_E[y], raw_E[w])
                if any(e is None for e in es):
                    continue
                if not all(e > e_cutoff for e in es):
                    continue
            acc += abs(a - 2.0 * b + c)
            cnt += 1
        out_d2.append(acc / cnt if cnt else None)
        out_triples.append(cnt)
    return out_d2, out_triples


def _bytes_to_unicode():
    """the standard GPT-2 byte-level remapping table: the printable
    ranges kept as-is, every other byte carried to chr(256+n) in
    ascending byte order -- the newline byte 0x0A lands at chr(266),
    the two-character key whose second character is U+010A."""
    bs = list(range(ord("!"), ord("~") + 1)) + \
        list(range(ord("\xa1"), ord("\xac") + 1)) + \
        list(range(ord("\xae"), ord("\xff") + 1))
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, [chr(c) for c in cs]))


NEWLINE_KEYS = ("\n", _bytes_to_unicode()[0x0A])


def resolve_newline_ids(args):
    """the newline token id(s): --newline-ids ID[,ID] at my word, else
    a static vocabulary table read (tokenizer.json / vocab.json beside
    this script, the entries whose token string is exactly one newline
    byte in EITHER representation -- the raw "\\n" string or the GPT-2
    byte-level remapped key for byte 0x0A (the form Llama-class
    tokenizers carry) -- zero model decodes, zero GPU); the resolution
    NAMED in the console with its matched key(s); unresolved a HARD
    EXIT with the named ask."""
    def _parse_ids(raw):
        ids = sorted({int(x) for x in raw.split(",") if x.strip()})
        if not ids:
            die("--newline-ids given but empty -- the anchor law "
                "needs the id(s); aborting.")
        return ids

    for i, a in enumerate(args):
        if a.startswith("--newline-ids="):
            return _parse_ids(a.split("=", 1)[1]), \
                "my --newline-ids word"
        if a == "--newline-ids":
            if i + 1 >= len(args):
                die("--newline-ids given without a value -- pass the "
                    "id(s): --newline-ids ID[,ID]; aborting.")
            return _parse_ids(args[i + 1]), "my --newline-ids word"
    for fname in ("tokenizer.json", "vocab.json"):
        if os.path.exists(fname):
            try:
                with open(fname) as f:
                    vocab = json.load(f)
            except Exception as e:  # noqa: BLE001 -- named exit
                die("vocabulary file %s unreadable (%s) -- never guess "
                    "an anchor id; aborting." % (fname, e))
            found = []

            def walk(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in NEWLINE_KEYS and isinstance(v, int):
                            found.append((k, v))
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(vocab)
            if found:
                ids = sorted({v for _, v in found})
                keys = ", ".join(repr(k) for k in sorted({k for k, _ in found}))
                return ids, ("the static vocabulary table %s (the "
                             "newline key(s) %s matched -- the raw "
                             "string or the byte-level remapped form "
                             "of byte 0x0A; a table read, zero model "
                             "decodes, zero GPU)" % (fname, keys))
            die("vocabulary file %s carries no newline entry in either "
                "representation (the raw %r string or the GPT-2 "
                "byte-level remapping of byte 0x0A, %r) -- pass "
                "--newline-ids ID[,ID] from my tokenizer; the anchor "
                "law never guesses; aborting."
                % (fname, "\n", _bytes_to_unicode()[0x0A]))
    die("no --newline-ids given and no tokenizer.json / vocab.json "
        "beside this script -- the B2 anchor law needs the newline "
        "token id(s): pass --newline-ids ID[,ID] (the ids whose token "
        "string is a newline, a static vocabulary fact of my "
        "tokenizer); the lookup named in this console either way; "
        "aborting.")


def anchors_of(d, newline_ids):
    """the anchor set: the steps whose committed token id is a newline
    token (sorted, the walk order)."""
    return [i for i, tid in enumerate(d["steps"]["id"])
            if tid in newline_ids]


# ---- the pair faces (S4 receipts; the candidate cell rides the d2 face) ----
def pair_b1_curve(zs, raw_E, e_cutoff, lag_lo, lag_hi):
    """B1 the pair face, a receipt (S4 defines it; the candidate cell
    is the d2-face zero-run mass per S4's own law): the EXACT-LAG
    PAIR CONSTRUCTION'S OWN OCCURRENCES re-pooled over the band --
    the mean over the delta=0 pair's occurrences (non-None + the
    survival gate, a masked-out pair never re-admitted by a shifted
    offset) of min over delta in {-1,0,+1} of |z_t - z_{t+L+delta}| --
    the same min-before-average law on the pair deviation, the
    hold-or-fall law B1[L] <= raw pair[L] at every lag."""
    n = len(zs)
    out_d, out_pairs = [], []
    for L in range(lag_lo, lag_hi + 1):
        acc = 0.0
        cnt = 0
        for t in range(n - L):
            a0, b0 = zs[t], zs[t + L]
            if a0 is None or b0 is None:
                continue
            if e_cutoff is not None:
                es = (raw_E[t], raw_E[t + L])
                if any(e is None for e in es):
                    continue
                if not all(e > e_cutoff for e in es):
                    continue
            best = abs(a0 - b0)
            for delta in (-1, 1):
                Lp = L + delta
                if Lp < 1 or t + Lp >= n:
                    continue
                a, b = zs[t], zs[t + Lp]
                if a is None or b is None:
                    continue
                if e_cutoff is not None:
                    es = (raw_E[t], raw_E[t + Lp])
                    if any(e is None for e in es):
                        continue
                    if not all(e > e_cutoff for e in es):
                        continue
                dev = abs(a - b)
                if dev < best:
                    best = dev
            acc += best
            cnt += 1
        out_d.append(acc / cnt if cnt else None)
        out_pairs.append(cnt)
    return out_d, out_pairs


def pair_b2_curve(zs, raw_E, anchors, e_cutoff, k_lo, k_hi):
    """B2 the anchored pair face, a receipt: the mean over valid i of
    |z_{a_i} - z_{a_{i+k}}| -- the token position never consulted for
    the lag, no band (the anchor law)."""
    m = len(anchors)
    out_d, out_pairs = [], []
    for k in range(k_lo, k_hi + 1):
        acc = 0.0
        cnt = 0
        for i in range(m - k):
            x, y = anchors[i], anchors[i + k]
            a, b = zs[x], zs[y]
            if a is None or b is None:
                continue
            if e_cutoff is not None:
                ea, eb = raw_E[x], raw_E[y]
                if ea is None or eb is None:
                    continue
                if not (ea > e_cutoff and eb > e_cutoff):
                    continue
            acc += abs(a - b)
            cnt += 1
        out_d.append(acc / cnt if cnt else None)
        out_pairs.append(cnt)
    return out_d, out_pairs


def b_face_readout(K, d, base, f_ref, newline_ids,
                   want_raw=True, want_pairs=True):
    """the per-doc B faces, all under the laneB mask (the doc's own
    median E, the tool's own law); med_e None (no E steps) -> every
    face EMPTY named, never imputed; want_raw: re-derive the raw
    laneB f d2 (the fixtures' lineage + trough; the corpus docs take
    it from doc_d2_census instead); want_pairs: the pair faces (the
    fixtures' receipts; the candidate cell is the d2 face)."""
    zs = K.signed_devs(d, base, f_ref)
    zf = zs["f"]
    raw_E = d["steps"]["E"]
    e_vals = [v for v in raw_E if v is not None]
    med_e = K.median_of(e_vals) if e_vals else None
    n_lag = len(K.LAGS)
    empty_d2 = [None] * n_lag
    empty_n = [0] * n_lag
    anch = anchors_of(d, newline_ids)
    ro = {"med_e": med_e, "n_anchors": len(anch), "status": "OK"}
    if med_e is None:
        ro.update({"raw_d2": empty_d2, "raw_triples": empty_n,
                   "b1_d2": empty_d2, "b1_triples": empty_n,
                   "b2_d2": empty_d2, "b2_triples": empty_n,
                   "status": "EMPTY_no_mask_reference"})
        return ro
    if want_raw:
        rd, rt = K.d2_curve(zf, raw_E, med_e, K.LAG_MIN, K.LAG_MAX)
        ro["raw_d2"], ro["raw_triples"] = rd, rt
    b1_d2, b1_tr = d2_b1_curve(zf, raw_E, med_e, K.LAG_MIN, K.LAG_MAX)
    ro["b1_d2"], ro["b1_triples"] = b1_d2, b1_tr
    b2_d2, b2_tr = d2_b2_curve(zf, raw_E, anch, med_e, K.LAG_MIN,
                               K.LAG_MAX)
    ro["b2_d2"], ro["b2_triples"] = b2_d2, b2_tr
    if want_pairs:
        p1, pt1 = pair_b1_curve(zf, raw_E, med_e, K.LAG_MIN, K.LAG_MAX)
        ro["b1_pair"], ro["b1_pair_triples"] = p1, pt1
        p2, pt2 = pair_b2_curve(zf, raw_E, anch, med_e, K.LAG_MIN,
                                K.LAG_MAX)
        ro["b2_pair"], ro["b2_pair_triples"] = p2, pt2
    return ro


def b_min_supported(d2_vals, triples, K):
    """the minimum B-face d2 over SUPPORTED lags (the surviving
    offset's own triple counts; the LOW_SUPPORT_PAIRS law carried
    verbatim); EMPTY named, never zero-filled."""
    vals = [(i, v) for i, v in enumerate(d2_vals)
            if v is not None and triples[i] >= K.LOW_SUPPORT_PAIRS]
    if not vals:
        return None, [], []
    mn = min(v for _, v in vals)
    arg = [i for i, v in vals if v == mn]
    zeros = [i for i, v in vals if v == 0.0]
    return mn, arg, zeros


def _zeros_disp(zeros):
    if not zeros:
        return "none"
    if len(zeros) <= 6:
        return ",".join(str(i) for i in zeros)
    return (",".join(str(i) for i in zeros[:6]) + ",...(%d)"
            % len(zeros))


# ---- the receipt-side gates (the desk half, no caches) --------------------
def parity_only(K, r):
    p("=== THE B1/B2 PHASE-LANE DIAGNOSTIC, PARITY-ONLY MODE (the "
      "receipt-side gates; no caches read) ===")
    p("the sheet rc-b12-phaselane-prereg.md pinned at my stamp (sha "
      "%s...), the receipt %s verified byte-exact at open, the tool %s "
      "verified inside it -- the forms read EXACTLY as sheeted (S4): "
      "B1 the phase-band pooling (the min over delta in {-1,0,+1} "
      "BEFORE the position average, the band pinned by convention, "
      "never widened after any read), B2 the line-synced anchor (the "
      "newline anchor set, the token position never consulted for the "
      "lag, the id(s) named in the full-mode console per R2); the "
      "verdict law (S5): each form its own pre-registered verdict, B1 "
      "the PRIMARY, B2 the SECONDARY, never a post-read selection; "
      "the fixture census FIRST (S6, the item-487 ordering law)"
      % (SHEET_SHA[:16], RECEIPT_SHA_BANK[:16], TOOL_SHA_BANK[:16]))
    p("")
    lg = r["legs"][JUDGED_LEG]

    # [D1] the standing world re-derived EXACT
    p("[D1] THE STANDING WORLD RE-DERIVED (doc_rows + loop_census "
      "alone, the before-column intact)")
    zero = {}
    proj = project(r, JUDGED_LEG, zero, zero, zero, K)
    p("  t_joint recomputed %.16f vs the receipt's %.16f %s | the "
      "banked %.16f" % (proj["t_now"], lg["t_joint"],
                        "OK" if abs(proj["t_now"] - lg["t_joint"])
                        < 1e-12 else "MISMATCH", LEVEL_BANK))
    p("  gap recomputed %.16f vs the receipt's raw %.16f %s | the "
      "banked %.16f" % (proj["gap_new"], lg["readouts"]["raw"]["gap"],
                        "OK" if abs(proj["gap_new"]
                                   - lg["readouts"]["raw"]["gap"])
                        < 1e-9 else "MISMATCH", GAP_BANK))
    p("  the null projection: k %d, lifted %s, demoted %s (must be "
      "empty)" % (proj["k_now"], proj["lifted"] or "[]",
                  proj["demoted"] or "[]"))
    if (abs(proj["t_now"] - lg["t_joint"]) >= 1e-12
            or abs(proj["gap_new"] - lg["readouts"]["raw"]["gap"])
            >= 1e-9
            or abs(proj["t_now"] - LEVEL_BANK) > 1e-9
            or abs(proj["gap_new"] - GAP_BANK) > 1e-9
            or proj["lifted"] or proj["demoted"]):
        die("D1 FAILED -- the standing world does not reproduce "
            "byte-exact; aborting.")
    p("  D1 PASSED (the world byte-identical to the bank)")
    p("")

    # [D2] the raw fixture receipts (the re-formation's before-column)
    p("[D2] THE RAW FIXTURE RECEIPTS (the receipt's own f.laneB d2 "
      "curves; curve index i = the banked convention, the lag "
      "LAGS[i] = i+2) -- the before-column of the re-formation read")
    raw_mins = {}
    for name in sorted(lg["fixture_curves"]):
        c = lg["fixture_curves"][name]["f"]["laneB"]
        vals, trs = c["d2"], c["triples"]
        present = [(i, v) for i, v in enumerate(vals) if v is not None]
        if not present:
            die("D2 FAILED -- fixture %s carries no supported raw d2 "
                "lag; aborting." % name)
        mn = min(v for _, v in present)
        zeros = [i for i, v in present if v == 0.0]
        raw_mins[name] = mn
        ms = [m_d2(vals, trs, g)[0] for g in D2_GATES]
        bank = BANKED_MD2.get(name)
        ok = (bank is None or ms[0] == bank)
        p("  %-27s min %.6f zeros @idx %s | m_d2 8/12/16: %s | banked "
          "g8 %s%s"
          % (name, mn, _zeros_disp(zeros),
             " / ".join(str(m) for m in ms),
             ("%d" % bank) if bank is not None else "-",
             " OK" if ok else " MISMATCH"))
        if not ok:
            die("D2 FAILED -- the m_d2 law does not reproduce the "
                "banked fixture census at gate 8 for %s; the law "
                "drifted; aborting." % name)
        if name in CLUB and mn != 0.0:
            die("D2 FAILED -- the club fixture %s reads minimum %.6f, "
                "not the exact zero the bank carries -- the receipt "
                "bytes are not the banked world; aborting."
                % (name, mn))
    cl_mn = raw_mins[CODE_LINE]
    p("  code-line's raw minimum %.17g vs the banked %.4f (delta "
      "%.2e) -- NEVER ZERO, the trough the B forms must collapse"
      % (cl_mn, CODE_LINE_MIN_BANK, abs(cl_mn - CODE_LINE_MIN_BANK)))
    if abs(cl_mn - CODE_LINE_MIN_BANK) > 1e-4:
        die("D2 FAILED -- code-line's raw minimum does not reproduce "
            "the banked 0.0454; aborting.")
    rows = {row["fixture"]: row["D"] for row in lg["loop_census"]}
    for nm, bank_D in sorted(D_MISSES.items()):
        got = rows.get(nm)
        if got is None or abs(got - bank_D) > 1e-6:
            die("D2 FAILED -- the miss D of %s (%s) does not "
                "reproduce the banked %.6f; aborting."
                % (nm, got, bank_D))
    p("  the miss D receipts exact: json %.6f countdown %.6f code-line "
      "%.6f (the coverage question's targets, the k 7 -> 8 door)"
      % (rows["loop-seeded-json"], rows["loop-seeded-countdown"],
         rows["loop-seeded-code-line"]))
    p("  the raw within-loop ordering (the before-column, ascending): "
      "%s" % " < ".join(
          "%s %.4f" % (n, raw_mins[n])
          for n in sorted(raw_mins, key=lambda n: raw_mins[n])))
    p("  D2 PASSED (the raw before-column banked exact; the club's "
      "exact zeros the signature the B forms must SURVIVE, code-line's "
      "never-zero trough the target they must COLLAPSE)")
    p("")

    # [D3] the P-B4 refined fixture table reproduced
    p("[D3] THE P-B4 REFINED FIXTURE TABLE (the item-488 bank, the "
      "masked E curves) REPRODUCED")
    for name, bank in sorted(BANKED_REFINED.items(), key=lambda kv:
                             -kv[1]):
        c = lg["fixture_curves"][name]["E"]["masked"]
        v, status = refined_tail(c["d"], c["pairs"], K)
        ok = (v is not None and abs(v - bank) < 1e-6)
        p("  %-27s refined %.6f vs banked %.6f %s"
          % (name, v if v is not None else -1.0, bank,
             "OK" if ok else "MISMATCH"))
        if not ok:
            die("D3 FAILED -- the refined-tail form does not reproduce "
                "the banked table; aborting.")
    p("  D3 PASSED (the P-B4 form byte-carried; the spine's refined "
      "cell rides unchanged, can-only-add)")
    p("")

    # [D4] the standing refs printed once
    p("[D4] THE STANDING REFS (the world the B faces write against): "
      "the V5 level %.16f | the V5 honest gap %.16f | the P-B4 honest "
      "%.6f (the standing best banked CODE read) | the caps k6 %.4f / "
      "k7 %.4f / k8 %.4f | the off-leg bounds prose %.6f / p2 %.6f | "
      "k = %d of ten fixtures above the level (the coverage question: "
      "code-line the only live door, k %d -> 8 the open question)"
      % (LEVEL_BANK, GAP_BANK, PB4_HONEST, CAPS[6], CAPS[7], CAPS[8],
         OFF_LEG_BOUNDS["prose17p-rw17"],
         OFF_LEG_BOUNDS["p2corpus-rw17"], proj["k_now"], proj["k_now"]))
    p("")

    # [D5] the full-mode instructions
    p("[D5] THE FULL MODE (my Mac, read-only, zero GPU, zero model "
      "decodes): the script beside this tool + receipt + the pinned "
      "sheet + my three pinned walk caches (%s; %s; %s), the newline "
      "token id(s) either --newline-ids ID[,ID] or a tokenizer.json / "
      "vocab.json beside the script (the static vocabulary lookup, "
      "named in the console), then"
      % tuple(K.CACHE_FILES[leg] for leg in K.LEGS))
    p("    python3 rc_b12_diagnostic.py --newline-ids ID[,ID]")
    p("  which emits %s for my shasum + upload; the order: the "
      "fixture census FIRST on the judged leg (a both-forms "
      "re-formation miss closes the sheet ON PAPER at the first gate, "
      "zero corpus reads), the B1 counter-receipt gated (a club "
      "member above zero a bug, a HARD EXIT; the B2 club minima "
      "findings only, the guarantee named), then the raw census "
      "parity gate per leg (per-leg anchors, the A1 lesson: CODE "
      "0.275000/1.352227 n_pos 11/200 held 15, prose 1.548387/3.896216 "
      "n_pos 72/310, p2 1.154667/3.072663 n_pos 62/375 -- a mismatch a "
      "HARD EXIT), the B-face census, the flood census (the A2 kill), "
      "the level race, the spine read D_new = max(D, z_refined, "
      "z_Bface), the honest both-sides gap PER GATE PER FORM, the "
      "off-leg reads, the kill-switch verdicts per form"
      % FULL_CONSOLE)
    p("(offline read of the run-of-record receipt bytes only, zero "
      "GPU, zero decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] "
      "unmoved (D-theta); no thresholds set, moved, or adjudicated; "
      "findings presented, never adjudicated -- my stamps "
      "decide)")


# ---- the full diagnostic (my Mac, read-only, zero GPU, zero decodes) ----
def full_mode(K, r, newline_ids, ids_source):
    p("=== THE B1/B2 PHASE-LANE DIAGNOSTIC, FULL MODE (my pinned "
      "caches, read-only, zero GPU, zero decodes) ===")
    p("the sheet %s... pinned at my stamp; the forms read EXACTLY as "
      "sheeted (S4), never tuned after any read; the newline token "
      "id(s) %s resolved from %s -- the lookup NAMED per the sheet's "
      "R2 (a static vocabulary fact, zero model decodes, zero GPU)"
      % (SHEET_SHA[:16], newline_ids, ids_source))
    p("the verdict law (S5): each form its own pre-registered verdict "
      "-- B1 the PRIMARY (the motivating hypothesis), B2 the "
      "SECONDARY (the different-frame alternative); the sheet never "
      "selects between them after a read; a B1 negative closes "
      "nothing on B2")
    p("the fixture census FIRST (the item-487 ordering law): the B "
      "faces read on the ten fixtures BEFORE any corpus doc's face is "
      "read (the baselines the standing shared machinery, the tool's "
      "own construction); the counter-receipt GATED ON B1 ONLY -- the "
      "B1 occurrences ARE the exact-lag construction's own (the "
      "delta=0 occurrence gates the member, a masked-out occurrence "
      "never re-admitted at a shifted offset -- the item-510 builder "
      "amend, my live catch banked), the min over delta includes "
      "delta=0, so a club exact zero can only "
      "hold or fall, a club member above zero names a bug, a HARD "
      "EXIT; the B2 club minima PRINTED AS FINDINGS ONLY, the "
      "anchor-index recurrence carries NO zero-survival guarantee "
      "(the token position re-anchored, a member may sit above zero "
      "honestly) -- the distinction named here once")
    if K.LEGS[0] != JUDGED_LEG:
        die("the judged leg is not first in the tool's LEGS order -- "
            "the first-gate close must read the judged leg before any "
            "off-leg byte; aborting.")
    p("")
    surviving = []          # the forms that re-formed on the judged leg
    receipts = {"flood": {}, "flood_trough": {},   # judged-leg verdict
                "gates": {}}
    for leg in K.LEGS:
        lg = r["legs"][leg]
        cache_path = K.CACHE_FILES[leg]
        if not os.path.exists(cache_path):
            die("leg %s: cache %s not found beside this script -- "
                "aborting." % (leg, cache_path))
        sha = sha256_file(cache_path)
        if sha != K.CACHE_PINS[leg]:
            die("leg %s: cache sha256 %s != the pinned %s -- the "
                "pin-table guard holds; never read divergent bytes; "
                "aborting." % (leg, sha, K.CACHE_PINS[leg]))
        p("--- LEG %s (cache pin MATCH, sha256 %s...) ---"
          % (leg, sha[:16]))
        recs = K.load_cache(cache_path, leg)
        cal_docs, held_docs = K.split_by_parity(leg, recs["docs"])
        live, inert = K.split_loop_fixtures(leg, recs["loop"])
        fixture_recs = {d["doc_id"]: d for d in live}
        rrows = {(row["half"], row["doc_id"]) for row in lg["doc_rows"]}
        crows = ({("cal", d["doc_id"]) for d in cal_docs}
                 | {("held", d["doc_id"]) for d in held_docs})
        if rrows != crows:
            die("leg %s: the cache's doc population does not match "
                "the receipt's doc_rows -- never project across "
                "populations; aborting." % leg)
        p("  population parity: %d cal + %d held, exact match against "
          "the receipt's doc_rows" % (len(cal_docs), len(held_docs)))
        if inert:
            p("  inert fixtures named and excluded (the Phase-0 "
              "precedent): %s"
              % sorted(d["doc_id"] for d in inert))
        base = K.compute_baselines(cal_docs, leg)
        f_vals = [v for d in cal_docs for v in d["steps"]["f"]
                  if v is not None]
        f_ref = K.mean_std(f_vals) if f_vals else None
        cal_E = sorted(v for d in cal_docs
                       for v in d["steps"]["E"] if v is not None)
        primary_cut = K.quantile(cal_E, K.MASK_Q_PRIMARY)

        # ---- THE FIXTURE CENSUS FIRST (before any corpus doc's face)
        fx = {}
        for name in sorted(fixture_recs):
            d = fixture_recs[name]
            cells = K.process_doc_conjunct(d, base, f_ref, primary_cut)
            cur = lg["fixture_curves"][name]["E"]["masked"]
            got = cells["E"]["masked"]
            for i in range(len(K.LAGS)):
                a, b = got["d"][i], cur["d"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die("leg %s fixture %s: the fresh masked E curve "
                        "diverges from the receipt's fixture_curves "
                        "at lag %s -- the curve lineage is not proven; "
                        "aborting." % (leg, name, K.LAGS[i]))
            ro = b_face_readout(K, d, base, f_ref, newline_ids,
                                want_raw=True, want_pairs=True)
            fcur = lg["fixture_curves"][name]["f"]["laneB"]
            for i in range(len(K.LAGS)):
                a, b = ro["raw_d2"][i], fcur["d2"][i]
                if (a is None) != (b is None) or (
                        a is not None and abs(a - b) > PARITY_TOL):
                    die("leg %s fixture %s: the fresh laneB f d2 "
                        "curve diverges from the receipt's "
                        "fixture_curves at lag %s -- the raw lineage "
                        "is not proven; aborting." % (leg, name,
                                                      K.LAGS[i]))
            v, status = refined_tail(got["d"], got["pairs"], K)
            fx[name] = {"ro": ro, "refined": v, "refined_status": status}
        p("  fixture curve parity: all ten fixtures byte-close at "
          "1e-12 on the masked E and laneB f d2 curves (the lineage "
          "proven; the B forms never touch the standing channels)")
        p("  THE FIXTURE CENSUS FIRST (the B faces on the ten "
          "fixtures, both forms; the minimum over SUPPORTED lags, "
          "the LOW_SUPPORT_PAIRS law; curve index i, the lag i+2):")
        p("    %-27s %s" % ("fixture", "raw min   | B1 d2 min "
                           "(argmin, exact zeros) | B2 d2 min "
                           "(argmin, zeros, anchors)"))
        club_b1_bad = []
        reform = {"B1": {"collapse": False, "zero": False},
                  "B2": {"collapse": False, "zero": False}}
        for name in sorted(fx):
            ro = fx[name]["ro"]
            raw_mn = min((v for v in ro["raw_d2"] if v is not None),
                         default=None)
            b1_mn, b1_arg, b1_zeros = b_min_supported(
                ro["b1_d2"], ro["b1_triples"], K)
            b2_mn, b2_arg, b2_zeros = b_min_supported(
                ro["b2_d2"], ro["b2_triples"], K)
            p("    %-27s raw %.6f | B1 %s (arg %s, zeros %s) | B2 %s "
              "(arg %s, zeros %s, anchors %d)"
              % (name, raw_mn,
                 "%.6f" % b1_mn if b1_mn is not None else "EMPTY",
                 _zeros_disp(b1_arg), _zeros_disp(b1_zeros),
                 "%.6f" % b2_mn if b2_mn is not None else "EMPTY",
                 _zeros_disp(b2_arg), _zeros_disp(b2_zeros),
                 ro["n_anchors"]))
            ms_r = [m_d2(ro["raw_d2"], ro["raw_triples"], g)[0]
                    for g in D2_GATES] if "raw_triples" in ro else []
            ms_1 = [m_d2(ro["b1_d2"], ro["b1_triples"], g)[0]
                    for g in D2_GATES]
            ms_2 = [m_d2(ro["b2_d2"], ro["b2_triples"], g)[0]
                    for g in D2_GATES]
            p("      masses 8/12/16 -- raw %s | B1 %s | B2 %s | pair "
              "faces (receipts): B1 %s B2 %s"
              % (" / ".join(str(m) for m in ms_r),
                 " / ".join(str(m) for m in ms_1),
                 " / ".join(str(m) for m in ms_2),
                 "%.6f" % min(v for v in ro["b1_pair"] if v is not None)
                 if "b1_pair" in ro
                 and any(v is not None for v in ro["b1_pair"])
                 else "EMPTY",
                 "%.6f" % min(v for v in ro["b2_pair"] if v is not None)
                 if "b2_pair" in ro
                 and any(v is not None for v in ro["b2_pair"])
                 else "EMPTY"))
            if name in CLUB and b1_mn != 0.0:
                club_b1_bad.append(name)
            if name == CODE_LINE:
                for form, mn, zs in (("B1", b1_mn, b1_zeros),
                                     ("B2", b2_mn, b2_zeros)):
                    reform[form]["zero"] = bool(zs)
                    reform[form]["collapse"] = (
                        mn is not None and raw_mn is not None
                        and mn < raw_mn)
        if club_b1_bad:
            die("leg %s: THE B1 COUNTER-RECEIPT FAILED -- the club "
                "fixtures %s read minima ABOVE the exact zero under "
                "B1 -- mathematically impossible if the form is "
                "byte-correct (the min over delta includes delta=0); "
                "a bug, never a verdict; aborting."
                % (leg, club_b1_bad))
        p("  THE B1 COUNTER-RECEIPT PASSED (the club's exact zeros "
          "SURVIVE the phase band -- the min law guarantees it, the "
          "guarantee now measured)")
        p("  THE B2 CLUB FINDINGS (printed, never gated -- the anchor "
          "law carries no zero-survival guarantee): %s"
          % "; ".join("%s B2 min %s" % (
              n, "%.6f" % b_min_supported(fx[n]["ro"]["b2_d2"],
                                          fx[n]["ro"]["b2_triples"],
                                          K)[0]
              if b_min_supported(fx[n]["ro"]["b2_d2"],
                                  fx[n]["ro"]["b2_triples"],
                                  K)[0] is not None else "EMPTY")
              for n in CLUB))
        cl = fx[CODE_LINE]["ro"]
        raw_cl = min((v for v in cl["raw_d2"] if v is not None),
                     default=None)
        p("  THE RE-FORMATION READ (code-line, the judged question): "
          "the raw minimum %.6f (banked 0.0454, NEVER zero) | B1 "
          "minimum %s (collapse %s, exact zeros %s -- the club band "
          "%s) | B2 minimum %s (collapse %s, exact zeros %s -- the "
          "club band %s)"
          % (raw_cl,
             "%.6f" % b_min_supported(cl["b1_d2"], cl["b1_triples"],
                                      K)[0]
             if b_min_supported(cl["b1_d2"], cl["b1_triples"],
                                K)[0] is not None else "EMPTY",
             "YES" if reform["B1"]["collapse"] else "no",
             _zeros_disp(b_min_supported(cl["b1_d2"],
                                         cl["b1_triples"], K)[2]),
             "REACHED" if reform["B1"]["zero"] else "not reached",
             "%.6f" % b_min_supported(cl["b2_d2"], cl["b2_triples"],
                                      K)[0]
             if b_min_supported(cl["b2_d2"], cl["b2_triples"],
                                K)[0] is not None else "EMPTY",
             "YES" if reform["B2"]["collapse"] else "no",
             _zeros_disp(b_min_supported(cl["b2_d2"],
                                         cl["b2_triples"], K)[2]),
             "REACHED" if reform["B2"]["zero"] else "not reached"))
        if leg == JUDGED_LEG:
            for form in ("B1", "B2"):
                if (reform[form]["collapse"] or reform[form]["zero"]):
                    surviving.append(form)
            if not surviving:
                p("  THE FIXTURE GATE: code-line fails to re-form on "
                  "BOTH forms (no minimum collapse, no exact zero at "
                  "any lag) -- THE SHEET CLOSES AT THE FIRST GATE, ON "
                  "PAPER, ZERO CORPUS READS (the phase hypothesis "
                  "dead on the fixtures, banked as mechanism "
                  "knowledge; the off-leg caches never opened)")
                p("  THE STANDING: the console presented for my "
                  "read -- the close a clean one (the S6 law); the "
                  "program turns to route C or the next sheet at my "
                  "word; the P-B4 honest %.6f stands as the best "
                  "banked CODE read; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved"
                  % PB4_HONEST)
                p("(offline read of my pinned cache bytes only, zero "
                  "GPU, zero decodes, read-only; Oct 21 2026; theta "
                  "[REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); no thresholds set, "
                  "moved, or adjudicated; findings presented, never "
                  "adjudicated -- my stamps decide)")
                return
            p("  THE FIXTURE GATE: code-line re-forms on %s -- the "
              "ordering survives, the corpus half opens under the "
              "surviving form(s); the dead form(s) %s closed at the "
              "first gate, their verdict already written (a clean "
              "close, banked as mechanism knowledge)"
              % (surviving,
                 [f for f in ("B1", "B2") if f not in surviving]
                 or "none"))

        # ---- THE CORPUS HALF (only reached on an ordering survival)
        p("  THE CORPUS HALF (under the surviving form(s) %s):"
          % surviving)
        ref_cal, ref_held = {}, {}
        mraw_cal = {g: {} for g in D2_GATES}
        mraw_held = {g: {} for g in D2_GATES}
        bro_cal = {form: {} for form in surviving}
        bro_held = {form: {} for form in surviving}
        n_no_anchor = {form: 0 for form in surviving}
        for pop, docs in (("cal", cal_docs), ("held", held_docs)):
            for d in docs:
                did = d["doc_id"]
                cells = K.process_doc_conjunct(d, base, f_ref,
                                               primary_cut)
                v, status = refined_tail(
                    cells["E"]["masked"]["d"],
                    cells["E"]["masked"]["pairs"], K)
                (ref_cal if pop == "cal" else ref_held)[did] = v
                d2c = K.doc_d2_census(d, base, f_ref, primary_cut)
                fb = d2c["f"]["laneB"]
                tgt = mraw_cal if pop == "cal" else mraw_held
                for g in D2_GATES:
                    tgt[g][did] = m_d2(fb["d2"], fb["triples"], g)[0]
                ro = b_face_readout(K, d, base, f_ref, newline_ids,
                                    want_raw=False, want_pairs=False)
                for form in surviving:
                    (bro_cal if pop == "cal"
                     else bro_held)[form][did] = ro
                    if ro["n_anchors"] == 0:
                        n_no_anchor[form] += 1

        # THE RAW CENSUS PARITY GATE (per-leg anchors, the A1 lesson)
        anc = CEN_ANCHORS[leg]
        masses8 = list(mraw_cal[D2_GATES[0]].values())
        mu8, sd8 = K.mean_std(masses8)
        n_pos8 = sum(1 for m in masses8 if m > 0)
        n_zero8 = len(masses8) - n_pos8
        hpos8 = sum(1 for m in mraw_held[D2_GATES[0]].values() if m > 0)
        if anc["held_n_pos"] is None:
            p("  THE RAW CENSUS PARITY GATE (gate %d, vs the banked "
              "%s census anchors, items 490/493): mean %.6f vs %.6f "
              "(delta %.2e) | sd %.6f vs %.6f (delta %.2e) | n_pos %d "
              "vs %d | n_at_zero %d/%d | held n_pos %d (NEVER BANKED "
              "-- printed as a finding, never gated)"
              % (D2_GATES[0], leg, mu8, anc["mean"],
                 abs(mu8 - anc["mean"]), sd8, anc["sd"],
                 abs(sd8 - anc["sd"]), n_pos8, anc["n_pos"],
                 n_zero8, len(masses8), hpos8))
        else:
            p("  THE RAW CENSUS PARITY GATE (gate %d, vs my banked "
              "console census): mean %.6f vs %.6f (delta %.2e) | sd "
              "%.6f vs %.6f (delta %.2e) | n_pos %d vs %d | n_at_zero "
              "%d/%d | held n_pos %d vs %d"
              % (D2_GATES[0], mu8, anc["mean"],
                 abs(mu8 - anc["mean"]), sd8, anc["sd"],
                 abs(sd8 - anc["sd"]), n_pos8, anc["n_pos"],
                 n_zero8, len(masses8), hpos8, anc["held_n_pos"]))
        if (abs(mu8 - anc["mean"]) > 1e-6
                or abs(sd8 - anc["sd"]) > 1e-6
                or n_pos8 != anc["n_pos"] or len(masses8) != anc["n"]
                or (anc["held_n_pos"] is not None
                    and hpos8 != anc["held_n_pos"])):
            die("leg %s: THE RAW CENSUS PARITY GATE FAILED -- the "
                "re-derived masses do not reproduce the banked gate-8 "
                "census for this leg; never project onto drifting "
                "bytes; the sheet closes at the S6 kill-switch; "
                "aborting." % leg)
        p("  THE RAW CENSUS PARITY GATE PASSED (the before-column "
          "byte-identical, the A1 amend-v2 lesson carried)")

        # the refined reference (the spine's standing cell)
        vals = [v for v in ref_cal.values() if v is not None]
        n_empty = sum(1 for v in ref_cal.values() if v is None)
        refined_ok = True
        if len(vals) < 2:
            refined_ok = False
            mu_r = sd_r = None
            p("  P-B4 cal reference: EMPTY (n %d) -- the refined face "
              "vacuous this leg, named; the B faces ride alone"
              % len(vals))
        else:
            mu_r, sd_r = K.mean_std(vals)
            p("  P-B4 CAL REFERENCE (the refined tail over %d cal "
              "docs, %d EMPTY named): mean %.6f sd %.6f"
              % (len(vals), n_empty, mu_r, sd_r))
            if sd_r <= 1e-12:
                refined_ok = False
                p("  sd == 0 -- the refined face EMPTY_degenerate_sd, "
                  "vacuous; the B faces ride alone")
        zfix_ref = {}
        for name in sorted(fx):
            v = fx[name]["refined"]
            zfix_ref[name] = ((v - mu_r) / sd_r
                              if (refined_ok and v is not None)
                              else None)

        # per form: the census, the flood, the spine per gate
        for form in surviving:
            tag = "b1" if form == "B1" else "b2"
            p("  === FORM %s (%s) ==="
              % (form, "the phase-band pooling, PRIMARY"
                 if form == "B1" else "the line-synced anchor, "
                 "SECONDARY"))
            if n_no_anchor[form]:
                p("  the no-anchor census: %d docs carry ZERO "
                  "newline anchors (named per the sheet's EMPTY law, "
                  "never zero-filled; their masses read the real "
                  "count 0, the mass law verbatim)"
                  % n_no_anchor[form])
            # the flood census (form-level, the A2 kill)
            trough, _, _ = b_min_supported(
                fx[CODE_LINE]["ro"]["%s_d2" % tag],
                fx[CODE_LINE]["ro"]["%s_triples" % tag], K)
            doc_mins, n_empty_flood = [], 0
            for did, ro in bro_cal[form].items():
                mn, _, _ = b_min_supported(ro["%s_d2" % tag],
                                           ro["%s_triples" % tag], K)
                if mn is None:
                    n_empty_flood += 1
                else:
                    doc_mins.append(mn)
            if trough is None or not doc_mins:
                p("  THE FLOOD CENSUS: VACUOUS (the trough %s or the "
                  "cal min-distribution EMPTY, %d docs EMPTY-named) "
                  "-- no flood read this form, named"
                  % ("EMPTY" if trough is None else "measured",
                     n_empty_flood))
                receipts["flood"][form] = None
            else:
                srt = sorted(doc_mins)
                q50 = K.quantile(srt, 0.50)
                q95 = K.quantile(srt, 0.95)
                deeper = sum(1 for m in doc_mins if m < trough)
                pct = 100.0 * deeper / len(doc_mins)
                p("  THE FLOOD CENSUS (the A2 lesson): code-line's "
                  "%s trough %.6f vs the cal min-distribution (n %d, "
                  "%d EMPTY-named) q50 %.6f q95 %.6f max %.6f -- %d "
                  "cal docs DEEPER (%.4f%%) %s"
                  % (form, trough, len(doc_mins), n_empty_flood,
                     q50, q95, srt[-1], deeper, pct,
                     "-- THE A2 KILL CONDITION MET (>= 5% deeper), "
                     "the flood re-learned" if pct >= 5.0
                     else "-- within the 5% line"))
                if leg == JUDGED_LEG:
                    receipts["flood"][form] = pct
                    receipts["flood_trough"][form] = trough
            # the spine per gate (EVERY gate, the A1 v1 lesson)
            zref_cal = {did: ((ref_cal[did] - mu_r) / sd_r
                              if (refined_ok
                                  and ref_cal[did] is not None)
                              else None) for did in ref_cal}
            zref_held = {did: ((ref_held[did] - mu_r) / sd_r
                               if (refined_ok
                                   and ref_held[did] is not None)
                               else None) for did in ref_held}
            for g in D2_GATES:
                m_cal = {did: m_d2(ro["%s_d2" % tag],
                                   ro["%s_triples" % tag], g)[0]
                         for did, ro in bro_cal[form].items()}
                m_held = {did: m_d2(ro["%s_d2" % tag],
                                    ro["%s_triples" % tag], g)[0]
                          for did, ro in bro_held[form].items()}
                m_fix = {n: m_d2(fx[n]["ro"]["%s_d2" % tag],
                                fx[n]["ro"]["%s_triples" % tag], g)[0]
                         for n in fx}
                vals_m = list(m_cal.values())
                mu_m, sd_m = K.mean_std(vals_m)
                n_pos = sum(1 for m in vals_m if m > 0)
                if sd_m <= 1e-12:
                    p("  --- FORM %s, GATE triples >= %d: the B-face "
                      "census EMPTY (sd 0 -- every cal doc reads zero "
                      "mass) -- the face vacuous at this gate, the "
                      "refined face rides alone ---" % (form, g))
                    zb_cal = zb_held = zb_fix = {}
                else:
                    zb_cal = {did: (m - mu_m) / sd_m
                              for did, m in m_cal.items()}
                    zb_held = {did: (m - mu_m) / sd_m
                               for did, m in m_held.items()}
                    zb_fix = {n: (m - mu_m) / sd_m
                              for n, m in m_fix.items()}
                    p("  --- FORM %s, GATE triples >= %d: the B-face "
                      "cal census mean %.6f sd %.6f (n_pos %d/%d) | "
                      "the fixture masses %s ---"
                      % (form, g, mu_m, sd_m, n_pos, len(vals_m),
                         " ".join("%s:%d" % (n, m_fix[n])
                                  for n in sorted(m_fix))))
                zc_cal = {did: zmax(zref_cal.get(did), zb_cal.get(did))
                          for did in ref_cal}
                zc_held = {did: zmax(zref_held.get(did),
                                     zb_held.get(did))
                           for did in ref_held}
                zc_fix = {n: zmax(zfix_ref.get(n), zb_fix.get(n))
                          for n in fx}
                proj = project(r, leg, zc_cal, zc_held, zc_fix, K)
                if leg == "mbpprw17":
                    gtail = (" -- BELOW the P-B4 honest %.6f (the "
                             "standing best banked CODE read)"
                             % PB4_HONEST
                             if (proj["gap_new"] is not None
                                 and proj["gap_new"] < PB4_HONEST)
                             else " -- AT OR ABOVE the P-B4 honest "
                             "%.6f" % PB4_HONEST)
                else:
                    gtail = (" -- vs the banked off-leg bound %.6f"
                             % OFF_LEG_BOUNDS.get(leg, float("nan")))
                gap_line = ("THE HONEST BOTH-SIDES GAP: %.6f -> %.6f "
                            "vs the V5 %.6f%s"
                            % (lg["readouts"]["raw"]["gap"],
                               proj["gap_new"], GAP_BANK, gtail))
                p("    t_joint %.6f -> %.6f (%+.6f) | k %d -> %d (the "
                  "cap at k_new %s) | %s"
                  % (proj["t_now"], proj["t_new"],
                     proj["t_new"] - proj["t_now"], proj["k_now"],
                     proj["k_new"],
                     "%.4f" % CAPS[proj["k_new"]]
                     if proj["k_new"] in CAPS else "unnamed",
                     gap_line))
                cl_new = proj["fix_new"].get(CODE_LINE)
                crossed = (cl_new is not None
                           and cl_new >= proj["t_new"])
                p("    THE LEVEL RACE: code-line D %.6f -> D_new "
                  "%.6f (its %s mass %s, z %s) vs the re-derived "
                  "level %.6f -- %s; the k move %d -> %d the "
                  "coverage question's answer-to-date"
                  % (proj["fix_now"][CODE_LINE], cl_new, form,
                     m_fix.get(CODE_LINE),
                     "%.4f" % zb_fix.get(CODE_LINE)
                     if zb_fix.get(CODE_LINE) is not None else "None",
                     proj["t_new"],
                     "CROSSED (the k-8 door open on this gate's read)"
                     if crossed else "below",
                     proj["k_now"], proj["k_new"]))
                # the held-side S-lesson census (receipted)
                n_ref = n_d2 = n_both = 0
                for did, D in ((x["doc_id"], x["D"])
                               for x in lg["doc_rows"]
                               if x["half"] == "held"
                               and x["D"] is not None):
                    zr = zref_held.get(did)
                    zb = zb_held.get(did)
                    lr = zr is not None and zr > D
                    lb = zb is not None and zb > D
                    if lr and lb:
                        n_both += 1
                    elif lr:
                        n_ref += 1
                    elif lb:
                        n_d2 += 1
                p("    the held-side lift (the S-lesson census): "
                  "refined-only %d, %s-only %d, both %d"
                  % (n_ref, form, n_d2, n_both))
                if leg == JUDGED_LEG:
                    receipts["gates"][(form, g)] = {
                        "gap": proj["gap_new"], "k_new": proj["k_new"],
                        "crossed": crossed, "t_new": proj["t_new"]}
            p("")
        if leg != JUDGED_LEG:
            p("  (the off-leg read presented never adjudicating the "
              "judged leg; the banked bounds the context)")
    # the kill-switch verdicts, presented never adjudicated
    p("THE KILL-SWITCH VERDICTS (the S6 law, presented for my "
      "stamps -- each form its own verdict, never a post-read "
      "selection):")
    for form in ("B1", "B2"):
        if form not in surviving:
            p("  FORM %s: CLOSED AT THE FIRST GATE (the fixture gate "
              "-- code-line failed to re-form; the phase hypothesis "
              "dead on the fixtures for this form, banked as "
              "mechanism knowledge; zero corpus reads spent on it)"
              % form)
            continue
        fl = receipts["flood"].get(form)
        if fl is None:
            p("  FORM %s: the flood census VACUOUS (named above) -- "
              "no A2 kill read; the gate receipts below my"
              % form)
        else:
            ftr = receipts["flood_trough"].get(form)
            p("  FORM %s: THE FLOOD: %.4f%% of the cal corpus deeper "
              "than code-line's %s trough -- %s"
              % (form, fl,
                 "%.6f" % ftr if ftr is not None else "EMPTY",
                 "ABOVE the 5% line -- THE A2 KILL CONDITION MET, "
                 "the flood re-learned" if fl >= 5.0
                 else "within the 5% line"))
        for g in D2_GATES:
            gr = receipts["gates"].get((form, g))
            if gr is None:
                continue
            p("  FORM %s GATE %d: the honest gap %.6f vs the P-B4 "
              "honest %.6f -- %s | k %d | code-line %s the level"
              % (form, g, gr["gap"], PB4_HONEST,
                 "BELOW (the re-formation bought nothing at this "
                 "gate)" if gr["gap"] is not None
                 and gr["gap"] < PB4_HONEST else "AT OR ABOVE",
                 gr["k_new"],
                 "CROSSED" if gr["crossed"] else "below"))
        p("  FORM %s: the census parity PASSED at open (a fail a "
          "HARD EXIT, never a verdict); the verdict question my -- "
          "the sheet's S4/S6 laws the binding frame" % form)
    p("  THE STANDING: the console presented for my read -- a "
      "negative kill-switch read closes the sheet on paper zero "
      "build hours (banked as mechanism knowledge; route C or the "
      "next sheet at my word); a live read opens the build question "
      "at my word only, its own stamp, never pre-promised; the "
      "gates 8/12/16 carried as receipts, ONE gate pinned at my "
      "stamp, only the pinned gate's read ever carried to a verdict "
      "question")
    p("(offline read of my pinned cache bytes only, zero GPU, zero "
      "decodes, read-only; Oct 21 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved (D-theta); "
      "no thresholds set, moved, or adjudicated; findings presented, "
      "never adjudicated -- my stamps decide)")


def main():
    args = sys.argv[1:]
    verify_sheet()
    K = load_tool()
    r = load_receipt()
    if "--parity-only" in args:
        parity_only(K, r)
        name = PARITY_CONSOLE
    else:
        newline_ids, ids_source = resolve_newline_ids(args)
        full_mode(K, r, newline_ids, ids_source)
        name = FULL_CONSOLE
    with open(name, "w") as f:
        f.write("\n".join(OUT) + "\n")
    print("")
    print("WROTE " + name)


if __name__ == "__main__":
    main()

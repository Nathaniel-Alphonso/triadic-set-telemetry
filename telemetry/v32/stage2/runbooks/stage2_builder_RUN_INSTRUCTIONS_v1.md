# RUN_INSTRUCTIONS v1 - THE STAGE-2 MIXED-REGIME SPLICE BUILDER (the Message-2 re-pin)

The owner-side run book for `stage2_splice_builder_v1.py` (message 2 of 3 of
the S2-BUILD act), riding the pinned sheet of record
`stage2-mixedregime-preregistration.md` (pinned at your stamp + Amendment Act
No. 1). The Message-1 pins stand superseded by this re-pin: the real-schema
adapter landed in the builder's bytes at Message 2 (the message-1 battery
console is byte-identical after the landing, proven by cmp). Every run below
is offline, zero-GPU, read-only over your banked caches and thins - the
builder never decodes, never walks a model, never writes anything outside the
`--out-dir` you name. Findings are presented, never adjudicated - your stamps
decide.

**What this instrument is.** An offline splice builder: it joins banked
segments (clean corpus prefixes, banked live loop fixtures) into the 90-doc /
110-seam mixed-regime cache of record per the pinned sizing (per leg: 15 Class
A, 15 Class B, 5 CLC, 5 LCL, 5 N; 55 seams per leg). The mixed cache it emits
carries the seam census (the count of every segment's provenance, every use
receipted), the dual-clock re-indexing of the amended sheet, and the
five-token class enumeration. The two inert fixtures are never spliced - the
under-32-step guard stands.

**The fail-loud law (the builder never passes silently).** Every pin is
asserted at run time and every violation is a named hard exit (`[DIE] <code>:
<detail>`), never a warning, never absorbed: missing input (`MISSING-INPUT`),
input byte count (`INPUT-BYTES`), input sha (`INPUT-SHA`), an unseen real
schema (`SCHEMA-UNEXPECTED`), an unreachable entry band
(`BAND-UNREACHABLE` - the re-sizing is presented at your word, never silently
absorbed), a reused clean segment (`CLEAN-REUSE`), an inert fixture requested
(`INERT-NEVER-SPLICE`), a segment under the length floor (`SEGMENT-LENGTH`),
a seam off a statement boundary (`SEAM-OFF-BOUNDARY`), a census/doc mismatch
(`TRUNCATED-CENSUS`), a seam-count mismatch (`SEAM-COUNT`), a provenance sha
tamper (`PROVENANCE-SHA`), a stale class token (`CLASS-ENUM`), the two LCL
loop segments sharing a fixture (`LCL-DISTINCT-FIXTURE`).

**The determinism law.** No wall clock, no randomness, canonical sorted-key
bytes: two runs over the same inputs to the same out-dir are byte-identical.
Every door below has been run twice my-side, `cmp` silent, the built cache and
census reproduced to the same sha.

## 1. THE SHA TABLE (verify every line before any run)

| file | bytes | sha-256 |
|---|---|---|
| stage2_splice_builder_v1.py (re-pinned at Message 2) | 68,635 | 14d1f448e9bd0a9a93a887972db925d4da7ecac2c53b1eea9fb850b35b3f938d |
| stage2_splice_builder_v1_battery_console.txt (the message-1 record, unchanged) | 3,775 | efeebc7c79a25824f769a9b5c299728fc9100fc170d59cbe40b6c254fc108441 |
| stage2_length_census_console.txt | 2,360 | de0232d15b4e2fda80b1115ff8bb9026a53f41ec1bb410c06257ed1351e8ee59 |
| stage2_build_console.txt | 2,665 | edb9943b7707c40c60851aa71b1495e473fdbdedf99260f7fefe3cc65b690b00 |
| stage2_verify_console.txt | 266 | 0a3efca8fa2c9704b853995b39b4a612b189f9d2a47eff1dcf5f3b7401b91b57 |
| stage2_mixed_cache.json (the built cache of record) | 14,814,947 | a5a4ae539112472424c2fb4160f2422e4810d4a83140f6e00972172502f76ea8 |
| stage2_census_export.json (the census of record) | 65,583 | cca12263db49a502bdf63761144d4b4953fd42c56b5a04a0a40f690270d0b86f |
| stage2-mixedregime-preregistration.md (the pinned sheet) | 40,180 | 7e256d19e9dbcf41ad09e34d179ad290245741235f746c7da09b9e5f53a48f05 |

Verify yourself first:

    sha256sum stage2_splice_builder_v1.py stage2-mixedregime-preregistration.md

The FOUR inputs of record (asserted fail-loud by the builder at every start -
byte-count-before-hash, then the sha prefix):

| input of record | bytes | sha prefix |
|---|---|---|
| triadic_wu_code_read_v1.json (the CODE cache, 400 docs / 113,238 rows) | 26,209,382 | 610d48c9 |
| triadic_t2_thin_rw17-code-r2.jsonl (the CODE thin, 410 records - the 10 fixture rows live here) | 80,912,361 | 77dd63c7 |
| triadic_t2_thin_rw17-prose-r2.jsonl (the PROSE thin, 630 records = 620 clean + 10 fixtures) | 159,280,278 | 88cbadee |
| triadic_wu_prose_read_v1.json (the PROSE export, the 620-doc parity) | 656,143 | a4e0ef03 |

## 2. THE BATTERY (the message-1 record stands, re-proven after the adapter)

The synthetic-worlds battery: 20 PASS / 0 FAIL, twice-run byte-identical. The
adapter landing changed zero battery bytes - the console is byte-identical to
the banked message-1 record (cmp silent). Run it yourself any time:

    python3 stage2_splice_builder_v1.py --battery

## 3. THE THREE DOORS (all three run green my-side at Message 2)

**Door 1 - the length census FIRST.** Every live fixture's row length
receipted against the three entry bands (1,36] / (37,64] / (65,128], and the
clean pools' reach to 128. The my-side receipts: all four input pins exact;
the CODE corpus 400 docs / 113,238 rows, onset-at-row0 400/400, work_inc
named-absent 400/400; the PROSE corpus 620 docs / 260,854 commits, the onset
census {0:205, 1:352, 2:61, 5:2} exact, all-CoT, the export parity 620/620;
both legs' bands servable ((65,128] served by 5 live fixtures; clean docs to
128: CODE 400, PROSE 616):

    python3 stage2_splice_builder_v1.py --length-census --code-cache triadic_wu_code_read_v1.json --code-thin triadic_t2_thin_rw17-code-r2.jsonl --prose-thin triadic_t2_thin_rw17-prose-r2.jsonl --prose-export triadic_wu_prose_read_v1.json | tee stage2_length_census_console.txt

**Door 2 - the build.** The real-schema adapter runs at this door: every
schema receipt prints in the console, any divergence dying loud
SCHEMA-UNEXPECTED, never absorbed. The my-side build: both legs 45 docs / 55
seams, classes 15/15/5/5/5, 55 distinct clean source docs at-most-once per
leg, 45 loop uses over the 8 live (per-fixture 7/7/6/6/5/5/5/4, both
denominators printed), the census conservation re-asserted cold at 90 docs /
110 seams:

    python3 stage2_splice_builder_v1.py --build --code-cache triadic_wu_code_read_v1.json --code-thin triadic_t2_thin_rw17-code-r2.jsonl --prose-thin triadic_t2_thin_rw17-prose-r2.jsonl --prose-export triadic_wu_prose_read_v1.json --out-dir stage2_build_out | tee stage2_build_console.txt

(The twice-run law: a second run to a second console with the SAME out-dir,
`cmp` silent - proven my-side, the cache and census reproduced to the same
shas. The exports land in `stage2_build_out/`.)

**Door 3 - the verify (the COLD door, none of the four inputs needed).** The
emitted census is re-loaded cold with its cache and every pin re-asserted -
the five-token enumeration, the span truth shapes, the dual-clock seam
monotonicity, the onset law (an onset mark exactly at row 0 and at every
authored seam, nowhere else), provenance shas, the length law, LCL
distinct-fixture, clean at-most-once, the loop-use census:

    python3 stage2_splice_builder_v1.py --verify stage2_build_out/stage2_census_export.json | tee stage2_verify_console.txt

## 4. THE HONEST LIMITS, STANDING

The seam is authored, never earned - a spliced document is classification
ground truth, never live-attention ground truth. Clean segments are used at
most once (55 distinct clean source docs per leg, every use receipted). Live
loop fixtures are reused with every use receipted, both denominators printed.
The two inert fixtures (the banked named pair) are never spliced. Cross-domain
seams are Stage-2B, their own act after the main line walks green. The meter's
true re-billed count stays NAMED-UNMEASURED-OFFLINE (decode-bearing, Stage 3
Item 12's door).

(offline paper act only, zero GPU, zero decodes, zero build hours; Nov 9 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; no thresholds set, moved, or adjudicated; findings presented, never adjudicated -- the owner's stamps decide)

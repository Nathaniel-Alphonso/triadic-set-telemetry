# THE CROSS-DOMAIN PROBE RUN INSTRUCTIONS (v1) - THE CD-3 BOTH-RUN PACKAGE (HIS HARDWARE RUN)

**THE AMENDMENT NOTES (three defects owned at his word, zero compute touched - presentation and filenames only; the tools, the batteries, the receipts and the flat-folder verification all stand unmoved):**

1. **The console-naming defect (caught at his ask for the commands):** the first delivery's tee names carried the my-side record names - fixed: every console name self-identifies with the instrument + run number, never a banked name.
2. **The OWNER-marker retirement + the run-name re-delivery (his ruling, Nov 10 2026):** the `OWNER` prefix is retired from every delivered filename and command, and the tools + this card are delivered under their exact run names so every command runs as written - no pin-suffixed names to rename.
3. **The one-command-per-block law (his ruling, Nov 10 2026, at his step 2):** bundled multi-command blocks with ordering instructions riding above them are retired from every delivered card and presentation - EVERY command gets its own code block, its own description of what it does, and its own expected result, in the exact order to run them. Nothing is ever implied above a block again.

**THE ACT THIS CARD SERVES:** the CD-2 build + readout, run on YOUR hardware (CD-3, the both-run law): every package and every act runs on your machine as well, my-side verification standing BEHIND your run, never instead of it. Your consoles close the act's receipts on your own hands; any divergence prints by name, never absorbed.

**THE TOOLS OF RECORD (two, both downloaded this act):**

- `crossdomain_probe_builder_v1.py` - 66,048 B, SHA-256 `680fd0e95b17be104af1283b3caf763cb5659e5b614b2e32aa0806c7ec31e1b6`
- `crossdomain_probe_readout_v1.py` - 83,182 B, SHA-256 `4fc66adda06a34e7fcf610960252f1cf35eacfb8cdc07fd6aac25679f8308225`

**THE INSTRUMENTS THE READOUT IMPORTS VERBATIM (byte-pinned at load, fail-loud; all seven must be discoverable - a flat folder holding everything needs no flags; if they live elsewhere, pass `--instruments <dir>` or set `$INSTRUMENTS_DIR`; if found scattered, the tool stages byte-exact copies itself, sha-verified, zero bytes modified, and says so in the printout):**

- `triadic_splitter_v1.py` - 52,410 B / `5980eaec…`
- `triadic_stage1_engines_v1.py` - 11,980 B / `79c794c0…`
- `triadic_accumulator_v1.py` - 58,292 B / `c7acb944…`
- `triadic_accumulator_prose_v1.py` - 76,867 B / `7d7ab8fe…`
- `triadic_hook_v1.py` - 52,078 B / `4de049de…`
- `stage2_ladder_walk_v1.py` - 89,115 B / `3d4faa17…`
- the builder itself (`crossdomain_probe_builder_v1.py`, its cold census door `load_cross` used verbatim)

**THE FIVE INPUT PINS (the caches of record; each is asserted at load fail-loud by exact byte size + sha):**

- the CODE cache `triadic_wu_code_read_v1.json` - 26,209,382 B / `610d48c9…`
- the CODE thin `triadic_t2_thin_rw17-code-r2.jsonl` - 80,912,361 B / `77dd63c7…`
- the PROSE thin `triadic_t2_thin_rw17-prose-r2.jsonl` - 159,280,278 B / `88cbadee…`
- the PROSE export `triadic_wu_prose_read_v1.json` - 656,143 B / `a4e0ef03…`
- the mixed census export `stage2_census_export.json` - 65,583 B / `cca12263…`

**THE LAWS:** zero GPU, zero decodes, offline over the banked caches only, pure stdlib (pip forbidden), fail-loud never silent, the caches never leave your machine, twice-run determinism (every console run twice, `cmp` byte-identical), the layout-free law (the readout discovers every input by filename then byte size then EXACT sha wherever it lives - your directory tree is never assumed; the builder takes explicit path flags YOU fill - no my-side layout rides any command), the one-command-per-block law (every command its own block, its own description, its own expected result - never bundled, never implied), the naming law (every artifact this act mints carries the `crossdomain_probe` prefix, no `2b/2B` string rides any filename), findings presented never adjudicated - your stamps decide.

**THE HONEST CONSOLE NOTE:** the readout's `[pin]` discovery lines print YOUR discovered paths - your two runs on your machine must be byte-identical to each other (that is the twice-run cmp), and the NUMBERS are what compare against the banked my-side receipts (the paths never do).

---

## STEP −1 - THE BYTE-VERIFY (before anything)

**−1a. The byte sizes of the two tools.** Must read `66048` and `83182`:

```
wc -c crossdomain_probe_builder_v1.py crossdomain_probe_readout_v1.py
```

**−1b. The shas of the two tools.** On BSD/macOS (on GNU/Linux, `sha256sum` replaces `shasum -a 256`). Must read `680fd0e9…` and `4fc66add…` - any mismatch is a NAMED hard stop, never a guess. Also verify the seven instruments against the pins above:

```
shasum -a 256 crossdomain_probe_builder_v1.py crossdomain_probe_readout_v1.py
```

## STEP 0 - THE BUILDER BATTERY (zero real rows, seconds)

**0a. Battery run 1.** The 10-doc synthetic hand-off world green through the real plan/pool/join/validator path; the 3 tamper shapes + 8 negative fixtures dying loud at their own named checks; closing line `[battery] all worlds green: … every die at its own named check`; exit 0:

```
python3 crossdomain_probe_builder_v1.py --battery | tee crossdomain_probe_builder_v1_battery_console_1.txt
```

**0b. Battery run 2 (the twice-run law).** Identical output to 0a:

```
python3 crossdomain_probe_builder_v1.py --battery | tee crossdomain_probe_builder_v1_battery_console_2.txt
```

**0c. The cmp.** Silent = byte-identical:

```
cmp crossdomain_probe_builder_v1_battery_console_1.txt crossdomain_probe_builder_v1_battery_console_2.txt
```

## STEP 1 - THE READOUT BATTERY (zero real rows; the dies are the green console - the fail-loud receipts being PROVEN)

**1a. Battery run 1.** 27/27 green-world checks; the 4 tampers (FOREIGN-ROW, TRUTH-LABELS, BIT-DIVERGENCE, CROSS-LEG-CONTAMINATION) + 6 negatives (ONSET-DERIVATION, UNRECOGNIZED-SCHEMA, TRUNCATED-CENSUS, SEAM-COUNT, PROVENANCE-SHA, EMISSION-LAW) each dying loud at its own named check; `[battery] all worlds green`; exit 0:

```
python3 crossdomain_probe_readout_v1.py --battery | tee crossdomain_probe_readout_v1_battery_console_1.txt
```

**1b. Battery run 2 (the twice-run law).** Identical output to 1a:

```
python3 crossdomain_probe_readout_v1.py --battery | tee crossdomain_probe_readout_v1_battery_console_2.txt
```

**1c. The cmp.** Silent = byte-identical:

```
cmp crossdomain_probe_readout_v1_battery_console_1.txt crossdomain_probe_readout_v1_battery_console_2.txt
```

## STEP 2 - THE BUILD (your side mints your probe cache + census)

Real filenames whole, no angle brackets; if a leg is not at hand, delete its line entirely - every kept line except the last keeps its trailing `\`.

**2a. Build run 1.** The five input pins asserted at load, the adapters green, the length census before any seam placed, the fresh-draw receipts, and the artifact lines - your minted bytes should read exactly `crossdomain_probe_cache_v1.json 1,168,366 B sha256 6b4c542d…` + `crossdomain_probe_census_v1.json 8,042 B sha256 151c6ace…` (any other sha is a named divergence for your report, never absorbed). Both land under `crossdomain_probe_build_out/`:

```
python3 crossdomain_probe_builder_v1.py --build \
  --code-cache   triadic_wu_code_read_v1.json \
  --code-thin    triadic_t2_thin_rw17-code-r2.jsonl \
  --prose-thin   triadic_t2_thin_rw17-prose-r2.jsonl \
  --prose-export triadic_wu_prose_read_v1.json \
  --mixed-census stage2_census_export.json \
  | tee crossdomain_probe_builder_v1_build_console_1.txt
```

**2b. Copy run 1's cache aside.** The build writes into the same out-dir each run - this copy preserves run 1's minted cache for the 2f cmp:

```
cp crossdomain_probe_build_out/crossdomain_probe_cache_v1.json crossdomain_probe_cache_v1_run1.json
```

**2c. Copy run 1's census aside.** Same purpose for the census:

```
cp crossdomain_probe_build_out/crossdomain_probe_census_v1.json crossdomain_probe_census_v1_run1.json
```

**2d. Build run 2 (the twice-run law).** Identical artifact lines to 2a:

```
python3 crossdomain_probe_builder_v1.py --build \
  --code-cache   triadic_wu_code_read_v1.json \
  --code-thin    triadic_t2_thin_rw17-code-r2.jsonl \
  --prose-thin   triadic_t2_thin_rw17-prose-r2.jsonl \
  --prose-export triadic_wu_prose_read_v1.json \
  --mixed-census stage2_census_export.json \
  | tee crossdomain_probe_builder_v1_build_console_2.txt
```

**2e. The console cmp.** Silent = the two build consoles byte-identical:

```
cmp crossdomain_probe_builder_v1_build_console_1.txt crossdomain_probe_builder_v1_build_console_2.txt
```

**2f. The cache cmp (run 1's copy vs run 2's mint).** Silent = the cache byte-identical across runs:

```
cmp crossdomain_probe_cache_v1_run1.json crossdomain_probe_build_out/crossdomain_probe_cache_v1.json
```

**2g. The census cmp (run 1's copy vs run 2's mint).** Silent = the census byte-identical across runs:

```
cmp crossdomain_probe_census_v1_run1.json crossdomain_probe_build_out/crossdomain_probe_census_v1.json
```

## STEP 3 - THE COLD DOOR (the census + cache re-load, no source inputs)

**3a. The verify.** Expected: `[verify] 10 docs / 10 seams, directions {"CODE->PROSE": 5, "PROSE->CODE": 5}, band allocation … every pin green (cold door: no source inputs touched)` + the standard closing paren:

```
python3 crossdomain_probe_builder_v1.py --verify crossdomain_probe_build_out/crossdomain_probe_census_v1.json
```

## STEP 4 - THE READOUT PREP (the two calibrations of record + the lane-join sources; minutes, not seconds - it loads the 159,280,278 B prose thin)

In a flat folder holding your probe cache + census, the code cache, the prose thin, the prose export and the seven instruments, no flags are needed - discovery admits by sha. If anything lives elsewhere, add `--root <that dir>` (repeatable).

**4a. Prep run 1.** The even-A **86** lane-moments receipt (the pin read fail-loud), the rw16 port cross-checked EXACT on all **620** corpus docs, the even-A **49** CODE prefix moments, the 10 EMISSION lane-join source slices with their membership receipts; the prep context lands beside the script as `crossdomain_probe_readout_ctx.pkl`:

```
python3 crossdomain_probe_readout_v1.py --stage prep | tee crossdomain_probe_readout_v1_prep_console_1.txt
```

**4b. Copy run 1's ctx aside.** The prep rewrites the ctx each run - this copy preserves run 1's for the 4e cmp:

```
cp crossdomain_probe_readout_ctx.pkl crossdomain_probe_readout_ctx_run1.pkl
```

**4c. Prep run 2 (the twice-run law).** Identical output to 4a:

```
python3 crossdomain_probe_readout_v1.py --stage prep | tee crossdomain_probe_readout_v1_prep_console_2.txt
```

**4d. The console cmp.** Silent = the two prep consoles byte-identical:

```
cmp crossdomain_probe_readout_v1_prep_console_1.txt crossdomain_probe_readout_v1_prep_console_2.txt
```

**4e. The ctx cmp (run 1's copy vs run 2's ctx).** Silent = the prep context byte-identical across runs:

```
cmp crossdomain_probe_readout_ctx_run1.pkl crossdomain_probe_readout_ctx.pkl
```

## STEP 5 - THE READOUT READ (the CD-5 measurement acts on your minted cache)

**5a. Read run 1.** Closing: `[checks] 27/27 landed` + `[read] every check landed (27/27); exit 0` + the standing line + the standard closing paren:

```
python3 crossdomain_probe_readout_v1.py --stage read | tee crossdomain_probe_readout_v1_run_console_1.txt
```

**5b. Read run 2 (the twice-run law).** Identical output to 5a:

```
python3 crossdomain_probe_readout_v1.py --stage read | tee crossdomain_probe_readout_v1_run_console_2.txt
```

**5c. The cmp.** Silent = byte-identical:

```
cmp crossdomain_probe_readout_v1_run_console_1.txt crossdomain_probe_readout_v1_run_console_2.txt
```

**WHAT THE READ PRINTS (the receipts, all compared against the banked my-side numbers):**

- `[cd-5a]` per doc: the seam position, the outgoing span closing exactly at the seam, the incoming span latching at the WRITTEN onset mark, five-state entry COLD_START, phase-B CONFIRM, contiguity green, foreign rows 0 - and the pooled five-state census `{"COLD_START": 282, "CONFIRM": 2074}` only, zero TIER2_ROUTE at authored seams.
- `[cd-5b]` per span: both forms printed side by side (the [REDACTED_PER_PUBLICATION_POLICY] record lens / theta [REDACTED_PER_PUBLICATION_POLICY], the designation never silently chosen), the grade, the sub-slot typing, and for the incoming spans the bit-exact spliced-vs-standalone receipt (60 horizon compares, zero divergence). The banked finding your run should reproduce: **20/20 grade MATCH, zero crossings at either form, highest composite peak 1.4736** - presented, never adjudicated.
- the W-lane z census, DESCRIPTIVE never a bar: 10 EMISSION spans read (min −1.2710 / mean 2.6191 / max 6.7998), the 10 CODE-BAND spans NAMED-ABSENT on that lane.
- `[cd-5c]` the isolation guard: cross-leg write census ZERO mismatches, non-vacuous - write census `{"CODE": 990, "MATH": 0, "PROSE": 1366}`; the pause/resume census 10/10 (the single-seam pause-AND-resume cell NAMED-ABSENT per Section 7 limit 7); the hook's typing: 40 sub-slots, E-events 0 - ZERO if and only if zero crossings, nothing actuates, the efficacy terminals NAMED-UNMEASURED-OFFLINE.
- the pooled receipts n=10 seams + n=5 per direction (PROSE->CODE incoming rows 129/138/155/154/166; CODE->PROSE 226/229/227/214/222).

## STEP 6 - THE RETURN

Your consoles (both runs of each), the `cmp` receipts (silent or named), your minted cache + census shas, and any divergence by name - the whole package returns to the ledger at your word.

---

**THE STANDING:** theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; the stamped sheet `crossdomain-probe-preregistration.md` (37,215 B / `84608525…`) rides its own stamp; no bar set, moved, or adjudicated anywhere this act; the [REDACTED_PER_PUBLICATION_POLICY] lens record-keeping only; the findings presented, never adjudicated - the owner's stamps decide.

(offline paper act only, zero GPU, zero decodes, zero build hours; Nov 10 2026; theta [REDACTED_PER_PUBLICATION_POLICY] unmoved; no thresholds set, moved, or adjudicated; findings presented, never adjudicated -- the owner's stamps decide)

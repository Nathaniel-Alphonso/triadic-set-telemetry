# Diagnostics & panels — disposition record

This directory carries the v32-era corpus-drift diagnostic receipts and the
Wu-model read receipts (population-comparability reads taken against the
published corpora).

## Published here

- `wu-read-receipts/` — three read-receipt exports (code, content-p2, prose),
  all theta-clean, byte-for-byte.
- 21 drift-diagnostic receipts across the 3-miss, alane, b12, codev6, codev7
  and d2sat species: consoles and readers, byte-for-byte where theta-clean,
  sanitized derivatives where the theta compliance banner required redaction
  (see `SANITIZATION_RECEIPTS.md`). The diagnostic readers reference the
  withheld species instrument by name (R1 plumbing-tier: the reader names the
  black box, it does not contain it) and do not execute standalone.

## Withheld — named and counted

**The codev5 species-development cluster (12 files)** —
the species instrument `triadic_rw17_codev5.py`, its battery/tool builders
and acceptance-run scripts, the desk-read pair, the codev5 consoles, and the
3.3 MB run receipt. Per the standing species-development ruling: this cluster
is development-data-only; no runs of record were produced there. The receipt
and consoles are methodology-soaked (statistic-definition rule prose) and are
excluded rather than redacted line-by-line, per the content-scrub ruling.
The drift/escalation story is carried by protocol doc 10. Files:
- `checkpoint-build6/build_codev5_battery.py`
- `checkpoint-build6/build_codev5_tool.py`
- `checkpoint-build6/codev5_battery_build_console.txt`
- `checkpoint-build6/codev5_negative_test_console.txt`
- `checkpoint-build6/codev5_tool_build_console.txt`
- `checkpoint-build6/rc_codev5_acceptance_run.py`
- `checkpoint-build6/rc_codev5_battery_console.txt`
- `checkpoint-build6/triadic_rw17_codev5.py`
- `run-record-codev5/desk_read_codev5.py`
- `run-record-codev5/desk_read_output.txt`
- `run-record-codev5/rc_codev5_console.txt`
- `run-record-codev5/rc_codev5_receipt.json`

**`triadic_evaluation/` (5 files)** — the subfolder copies are the
unredacted originals or byte-identical duplicates of offline-pass exports
already published in `telemetry/v32/offline-passes/` (publish-once), plus
`triadic_rw15_readout.py`, which is in the theta-hardcoded instrument
exclusion bucket. Files:
- `triadic_evaluation/triadic_p2corpus_offline_pass_v1.json`
- `triadic_evaluation/triadic_p2corpus_offline_pass_v1_per_doc.jsonl`
- `triadic_evaluation/triadic_prose17p_offline_pass_v1.json`
- `triadic_evaluation/triadic_prose17p_offline_pass_v1_per_doc.jsonl`
- `triadic_evaluation/triadic_rw15_readout.py`

**Superseded diagnostic versions (6 files)** — dropped per the
latest-version-only convention; the versions of record are published above.
Files:
- `rc_b12_diagnostic_v1.py`
- `rc_b12_diagnostic_v2.py`
- `rc_b12_diagnostic_v3.py`
- `codev7_corpus_diagnostic_v1.py`
- `rc_d2sat_diagnostic_v1.py`
- `rc_d2sat_parity_console_v1.txt`

## Route note

`triadic_wu_code_read_v1.json` (26,209,382 B) exceeds the API push ceiling
and is pushed by the repo owner via git; its integrity pointer (sha256) is in
`wu-read-receipts/SANITIZATION_RECEIPTS.md`.

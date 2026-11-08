# Phase-4 receipts (model-scale transfer)

The public record of the phase-4 model-scale transfer lives here, beside the 8B
offline-pass exports already published under `telemetry/v32/offline-passes/` and
the protocol doc `docs/protocols/09-model-scale-transfer.md`.

- `s5-panel-receipts/` — the read-only panel diagnostic of record: measure, never
  fit; per-leg trip counts, concordance cells, anchor matches (40/40), and the
  export with its lineage SHA-256 receipts.
- `s8-rework-receipts/` — the rework readout of record: per-leg parity receipts,
  entry-band receipts (values withheld per publication policy, names kept),
  reproduction receipts, and the fused-hook emission contract.
- `stream-monitor-validation-receipts/` (the stream-monitor validation lane of
  record): phase-1 parity and integration receipts on the code and prose legs,
  phase-2 parity and integration receipts on the math and p2 legs; the
  monitor-vs-census agreement readings (1,214 flagged vs 1,556 cleared, zero
  disagreement), zero actuation on all 1,556 clean walks, cut-at-first-event
  with restoration on every degenerate walk, entry-band values withheld per
  publication policy with sanitization receipts riding in the subdirectory.

Per the program's disclosure ladder, the withheld phase-4 material is named with
its count stated plainly (105 files total):

- the phase-4 amend-chain development battery (12 consoles + 1 spec echo + 23
  monitor-family consoles + 19 species run modules) is withheld as
  **development-data-only; no runs of record were produced there**;
- the 3B validation-lane material (9 scout/smoke consoles + 5 exports) is
  withheld as development data — that lane never produced a run of record;
- the phase-4 tool test batteries (11 acceptance/control runner scripts + 21
  build/acceptance/control consoles + 4 forensics/part-3a smoke modules) are
  withheld as test-method development material.

Sanitization receipts with original SHA-256 hashes ride in each subdirectory.

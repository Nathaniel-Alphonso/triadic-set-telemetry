# The Stage-2 Qualification Lane (telemetry/v32/stage2)

This lane carries the qualification artifacts of Stage 2 of the staged order:
the mixed-regime ground truth and the cross-domain probe, each pre-registered
before compute, built offline with zero decodes, and verified on both
machines: the build and the read run my-side, then the whole package run
again on the owner's hardware with zero divergence by name. The staged order
and its status live in the repository root README; this folder is the
artifact record.

## What is here

- **preregistrations/** - the two stamped pre-registration sheets: the
  mixed-regime fixture build (the 90-doc / 110-seam splice under the stamped
  route, its acceptance ladder, its census and grading laws) and the
  cross-domain probe (the ruled added step: the classification ground truth
  over spliced cross-domain documents, never a live-attention ground truth).
- **instruments/** - the five Stage-2 tools: the splice builder, the
  acceptance-ladder walk, the diagnostic readout, and the cross-domain
  probe's builder and readout. The Stage-1 engines module these tools build
  on publishes in the Stage-1 lane (telemetry/v32/inband).
- **runbooks/** - the run instructions for the three owner-side doors: the
  builder, the acceptance-ladder walk, and the cross-domain probe package.
- **notes/** - the two close notes of record: the build act's close and the
  formal Stage-2 close (the findings of record, the honest limits, the
  separation receipt).
- **receipts/** - the consoles of record: the my-side builder battery,
  length-census, build, verify, walk, and walk-battery consoles with their
  twice-run twins; the cross-domain probe's my-side battery, build, prep,
  run, and readout-battery consoles with their twice-run twins; and the
  owner-side hardware consoles of the probe run (the owner's own run of the
  whole package).

## How to read this lane

Every pre-registration sheet states its own acceptance ladder and its own
honest scope; the consoles are the runs of record that walked those ladders;
the close notes are the findings of record, presented for adjudication to
the owner's stamps. The instruments publish as records of the qualification
runs, not as executable distributions: they do not run as-is.

The twice-run pairs are the determinism receipt: each pair's two consoles
are byte-identical, one hash, two files.

## What is not here

The data artifacts of record - the caches, census exports, and run
contexts - are development data and do not publish. The owner's rung-(g)
consoles of the acceptance-ladder walk are byte-identical to the my-side
records of record and publish through them. Stage 3, the restoration ladder
(the decode-bearing half), is its own act with its own pre-registration
before any rows are read.

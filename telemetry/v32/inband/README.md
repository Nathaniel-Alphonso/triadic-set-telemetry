# The Stage-1 Qualification Lane (telemetry/v32/inband)

This lane carries the qualification artifacts of Stage 1 of the staged order:
the five forward-pass pre-registrations, each pre-registered before compute,
built offline with zero decodes, and verified deterministic across two runs.
The staged order and its status live in the repository root README; this
folder is the artifact record.

## What is here

- **preregistrations/** - the four stamped pre-registration sheets: the
  splitter (the two-tier regime tripwire), the streaming accumulator across
  the code and prose legs, the mid-walk math form, and the trip-record
  emission contract.
- **instruments/** - the shared engines module of the Stage-1 instrument
  stack. The five instrument modules and their run instructions join this
  folder as later commits.
- **receipts/** - the consoles of record: the hook instrument's run console
  and its twice-run twin, its control console; the mid-walk math instrument's
  run console and its twice-run twin, its control console.

## How to read this lane

Every pre-registration sheet states its own acceptance ladder and its own
honest scope; the consoles are the runs of record that walked those ladders.
The instruments publish as records of the qualification runs, not as
executable distributions: they do not run as-is.

The twice-run pairs are the determinism receipt: each pair's two consoles are
byte-identical, one hash, two files.

## What is not here yet

The five instrument modules, their run instructions, and the remaining
consoles of record join this lane as later commits, each verified against its
banked pin before it lands. The mixed-regime ground truth of Stage 2 is its
own lane and its own pre-registration.

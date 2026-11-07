# Environment Drift and Baselining — the Session-Basis Protocol (Public Protocol Summary)

The environment is not a constant. The same frozen bytes, the same pinned packages, and the same corpus produced materially different decode behavior from one session to the next — a shift in the base decode path, upstream of all loop machinery, with the instrument exonerated live. This document is the protocol record of how the program discriminates drift, adjudicates it, and re-bases under it: never by assumption, never by silent absorption.

## 1. The finding and the discrimination ladder

- **The finding of record:** byte-identical instruments, verified-matching pins, the same corpus — and the aggregate decode behavior moved between sessions. The drift is real, measured, and upstream: it lives in the environment's arithmetic, not the program's code.
- **Three rungs, in order; nothing else runs until the ladder resolves.** **The census rung** re-runs the single most instrumented walk of record — a walk with a multi-day bit-stability record — to measure whether the shift reaches the logit level on identical steps. It bounds the drift: stable where it was always stable, shifted at the corpus aggregate — a bound, never a denial. **The reboot rung** re-runs the discriminator after a reboot, separating transient system state from persistent variables: reproducing the shifted curve excludes transients; reproducing the banked curve restores the banked basis; a third curve means the environment is unstable across changes and nothing is bankable until stability is established. **The amendment ruling** decides how the program proceeds — enumerated before any result exists.
- **Readings bind before runs.** Every rung's readings are written before the rung exists, and the instruments print no verdicts: their printed outputs are color, never program verdicts. A guard failure voids a rung — the run re-executes, and nothing is ever adjudicated from a bad export. Instrument suspicion is dead by default and revives only if a run fails to reproduce itself under identical conditions.

## 2. The near-tie census — the quantified flip-risk

The standing cause candidate carries a census, and the census is the honest mechanism statement: a substantial fraction of greedy decode steps sit within a representable tie's width of a coin flip. An environment change below any instrument's own resolution can flip early choices at those steps, and a long greedy walk cascades the flips into different token counts and different aggregate behavior. The census quantifies the flip-risk and rides the record — the mechanism is stated plainly, never hidden behind the word "noise."

## 3. The honest terminal state of the cause question

Every named suspect was excluded or verified by evidence: transient system state by the reboot rung; the operating-system suspect by the banked install history (nothing installed inside the drift window); the disk state by a checksum pass over every file the decode touches. The cause remains an unenumerated persistent variable — named as unknown, never guessed — and that is recorded as the honest terminal state of the evidence phase. Cause-hunting is explicitly out of scope: a future discriminating rung exists only if the cause question becomes load-bearing, and it must be pre-registered before it runs.

## 4. The ruling — within-session re-baseline

The environment was adjudicated **stable-with-shift**: deterministic, self-consistent, reproducing its own curve bit-identically across reboots — but not reproducing the banked one. Cross-session comparability was adjudicated broken, and the program re-bases within-session. The restoration alternative was evidence-contradicted (the exonerated suspect had no mechanism to restore parity), and proceeding unamended against banked baselines under a confirmed persistent shift was ruled out in advance, pre-result, so it could not creep in later.

## 5. The session basis — defined once, banked before every run

- **The basis is the unit of comparability:** the set of runs sharing one environment — matching environment lines (operating system, pinned package versions, the evaluation harness's pinned commit) and an unchanged install history.
- **The pre-run ritual:** before every run, the environment line and the recent install history are banked into the run's own record. Any change against the session's opening line is a new bank line: everything stops, a fresh discriminator runs, and it is adjudicated before anything else banks.
- **Color, never verdict:** every cross-session comparison is demoted to color — recorded for the standing drift observation, never adjudicated, never an acceptance input.

## 6. The re-baseline sequence

Baselines and reference runs are regenerated in the same session as the held sweep, and all comparisons run within-session. The banked maps stay banked as distribution-level separation evidence; the anchor's clean-corpus property is re-recorded as environment-relative; the wired threshold is unmoved in every branch. Fresh tags mean fresh caches — no cross-session cache reuse, by construction.

## 7. Integrity joins and single-basis completion

The decisive guard is a bit-identity join: the held sweep's control points must verify bit-identical against the session's own reference, offline, at full precision. A verdict fires only if both legs produce it inside the session basis. If the basis breaks mid-sequence, the runs already completed stay banked as that basis's evidence, and the sequence re-bases from the break point — not from zero.

## 8. No re-derivations

Every number consumed at adjudication comes from the uploaded exports — export-to-export joins only. If a needed number is not in an artifact, the file is named and the author is asked; nothing is recomputed. The child-of-the-environment labeling (doc 05 §2) and the drift-equals-new-bank-line law (doc 09 §2) are this protocol's standing downstream consumers.

## 9. What this protocol does not do

No threshold moves in any branch. No acceptance criterion loosened. No banked number edited, re-derived, or re-stamped by the adjudication. No cause-hunting. Nothing runs before its pre-registration carries the author's stamp.

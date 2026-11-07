# Fresh-Walk Adjudication — the Reworked-Statistic Re-Earning Protocol (Public Protocol Summary)

When a runtime statistic fails its acceptance, the universal fail rule returns the *statistic* to rework — never the threshold. A reworked statistic is a **proposal**: it banks nothing until it re-earns acceptance on fresh walks. This document is the protocol record of that re-earning — the walks, the adjudication protocol's pre-registered elements, and the verdict semantics. It is the only sanctioned path by which a reworked statistic can replace a statistic of record.

## 1. Why fresh walks, and what fresh means

- **Adoption requires fresh walks.** A reworked candidate may never be adjudicated on the population it was reworked against. The development corpus is the train side by construction; the fresh corpus is the untouched test.
- **Fresh means new documents.** Fresh data is new prompts, never re-walks of old ones. A re-run of a banked prompt is a new walk of an old document — a different object, banked as its own record.
- **Children of the adjudicated environment.** The environment drifts measurably over time; every new walk therefore runs under a fresh, banked baseline and is labeled a child of the environment it ran in. A fresh-walk verdict is never read as environment-free, and fresh numbers are never compared against pre-drift numbers as if they were the same population.

## 2. The walks

- **Telemetry-born.** Every fresh walk runs in telemetry mode from the first step, so the per-step evidence margins are born in the walk itself. There is no retro-fitting path: a walk not born in telemetry cannot acquire margins later — a re-run is a new walk, and the old walks keep their honest record.
- **One budget, many consumers, no silent multiplexing.** A single fresh-walk corpus can serve several pre-registered consumers — this adjudication, the exit-verdict annotation run, and any future detector candidate's shipping requirement. Each consumer pre-registers separately and reads the walks under its own stamped protocol; nothing silently reuses a walk for a purpose it never declared.
- **The populations of record.** The walks cover the banked corpora of every lane family, with the fixed loop-fixture set riding each leg unchanged. The clean population is large and abundant; the positive population is the fixed engineered fixture set, small, and honestly stated as such in every verdict. Growing it is its own pre-registered step, never improvised mid-adjudication.
- **Monitor-walk law.** The fresh walks are read-only evidence producers: no actuator fires, no detector actuates, no threshold moves, nothing wires.

## 3. The adjudication protocol (every element pre-registered before any walk)

1. **Train-only selection.** Any trained probe, candidate selection, or calibration is confined to the train side; the held-out population is untouched until the single verdict read.
2. **Held-out two-standard-error verdict.** Per leg, per candidate: the flagged population must separate from the clean population on the untouched held-out side by at least two standard errors — the same pre-registered margin that governs every acceptance in this program.
3. **Population guard.** A minimum population per side, else the leg reads inconclusive — never a verdict squeezed from a sample too small to carry it.
4. **The jitter clause.** The readout instrument has a measured reproducibility floor (banked; its value lives in the results record). A verdict margin inside that floor reads inconclusive-from-jitter, never a verdict.
5. **Direction-consistency.** A task-general adoption claim requires the same direction on every leg. A candidate whose direction flips between legs may adopt per-leg only, by its own recorded note — the rule typed before it is tested.
6. **No post-hoc selection.** Only the banked candidates adjudicate. Nothing is tried, tuned, or shopped on the fresh corpus beyond the pre-registered table.
7. **Environment-scoped verdicts.** Every verdict names the environment it was earned on — model, precision regime, baseline chain, adjudicated drift state.

## 4. Verdict semantics

Adopt or reject, per leg, under the guard. The as-specified statistics remain the statistics of record in every branch until a verdict passes; if a reworked statistic separates on the held-out population, the lane re-opens with the corrected direction, and if it does not, the standing failure stands and nothing banked is harmed. The banked numbers of the old maps are never recomputed against the fresh population — the fresh corpus is a new population, banked as its own record.

## 5. The mechanism note

The rework under adjudication is a direction reversal, and it is grounded in a banked mechanism finding about what degenerate repetition does differently from honest reasoning: **a loop re-reads its anchor; honest chain-of-thought wanders.** The reversed statistics were proposed from that finding, and the fresh walks are its test — a published hypothesis meeting a pre-registered falsifier.

## 6. What this phase does not do

No actuation. No wiring. No threshold set, moved, or adjudicated. No re-adjudication of banked dispositions. No retro-fitting of margins to banked walks. Nothing built or run before its pre-registration carries my stamp.

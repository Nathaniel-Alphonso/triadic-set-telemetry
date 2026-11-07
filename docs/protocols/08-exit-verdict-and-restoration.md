# Exit-Verdict and Restoration — the Measured-Posture Layer (Public Protocol Summary)

Every governed walk ends with a verdict about its own state, and that verdict is a measurement, not a self-report. This document is the protocol record of the exit-verdict layer — how a walk's posture grade is computed and constrained — and of the restoration layer that decides whether an actuator acts on a flagged event at all.

## 1. The founding law — measured state, never self-report

The posture verdict draws on permitted inputs only, enumerated in its pre-registration: the walk's per-step evidence margins (born in telemetry, never retro-fitted — the telemetry-born law of doc 05 §2), the calibration-monitoring read (G10), the variance state, and the fault-ledger lanes (doc 02 §1, flag-first). Self-reported confidence never enters a verdict — what the model says about its own state is not evidence of its state. A walk not born in telemetry carries no margins and therefore no graded verdict: the record says so plainly, and no grade is reconstructed after the fact.

## 2. One decision surface — act, don't act, exit degraded

The three terminal options of a flagged walk are one decision, made once: act on the flagged state; don't act and carry the flag; or exit with a degraded verdict. The lockout clause binds the first option: **no expected-benefit estimate overrides a failed measured state** — a projected gain never converts a failed measurement into a pass. And the degraded verdict is a first-class outcome, not a softened failure: the grade travels with the output as its receipt (the posture layer of `ARCHITECTURE_OVERVIEW.md`). A walk carrying flagged-but-unactuated state exits degraded — never clean.

## 3. The grade set and its pre-registered mapping

- **Score and grade, both.** The layer computes a measured posture score and emits a typed grade — *clean*, *degraded*, or *calibrated-rejection*.
- **The mapping is pre-registered before the grade exists** — the anti-silent-threshold guard: no grading boundary is invented after results are seen. The mapping's form is committed in its pre-registration; its operating values are calibrated from banked numbers and live in the results record (R7, named-but-withheld — never hand-set, never tuned).
- **The near-tie band is an input, never an upgrade.** Scores inside the instrument's measured reproducibility floor (the jitter clause of doc 05 §3) are typed as ambiguous inputs — never read as clean, never silently resolved in either direction.
- **The calibrated-rejection class.** A walk facing an unresolvable state — a dependency gap, a failed measurement surface — exits with a calibrated rejection rather than a confident fabrication: an honest refusal, graded and receipted, never a guess with a confident face.

## 4. Annotation clauses

- **Offline post-pass.** Verdicts and confidence annotations are computed in a zero-GPU offline pass over banked telemetry — the walk's own record is the input, and the pass never re-walks. A runtime form remains an open design note, pre-registered as such — never claimed as built.
- **Per-event measured confidence.** Every flagged event on the fault ledger carries a measured-confidence annotation. An annotation is itself a measurement, not an opinion about the event.
- **Flagged-events-only scope.** Annotations apply to flagged events only; clean traffic carries no annotation payload — the surface stays bounded by the fault ledger, by construction.

## 5. Restoration — the act-or-not-act layer

- **The default is don't.** The decision an actuator faces is not "which action" but "whether to act at all," and the standing default is to carry the flag and let the walk exit degraded.
- **Silence is not zero damage.** An actuator with no measured recovery number does not act: an unmeasured expected benefit is not evidence, and the absence of a recorded damage number is never read as the absence of damage.
- **Calibration from banked numbers only.** The decision surface is calibrated from per-arm measured rates and per-document causal accounting joins — banked receipts, nothing else. The drag-vs-value boundary's form is committed in its pre-registration; its operating values are calibrated from banked numbers at a stamped step (R7, named-but-withheld).
- **Predictions before runs.** Per-actuator delta predictions are committed before any restoration run: each arm's predicted effect is written before the run, and the run grades the prediction — the fresh-data discipline of doc 05 carried into actuation.

## 6. The actuator set of record and its ordering law

The pre-registered restoration menu is the published set (doc 02 §2; G7 and G16 in `ARCHITECTURE_OVERVIEW.md`): **eviction of the flagged window** — the repair lever, memory-bound and near-zero compute, the model re-derives from its pre-loop state; **the grounding re-anchor** — reversible and additive, attention re-anchored to the evidence the walk already held; **the deferral-bias arm** — a bias toward calibrated deferral on deferral-scoring tasks, among states the model itself already reached; and **the suppression pair** — the destructive arms. The ordering law: **reversible and additive arms first, destructive arms last, and the destructive pair stays behind a measured shadow-replay yield before any live actuation** — the measured substitution-damage baseline stands as the bar any arm must beat. The safety property at the interface is unchanged from doc 02 §2: the program only ever selects among states the model itself reached; it never fabricates one.

## 7. Attribution and witnesses

- **Routing by actuation, never by instruction.** The attention-allocation readout — the routing channel of 17-AP (doc 02) — reads where an actuation's effect actually sits. The measurement is never commanded to agree with the intent.
- **The no-lone-witness law.** Mechanism attribution is never a lone gate: an attributed cause rides at least two witnesses — a code-read plus a measured effect, or two measured surfaces — never a single read's word.
- **Check-first code-reads.** An attribution claim is checked against the recorded instrument behavior first; an attribution that fails its check-first read is withdrawn, never argued into the record.

## 8. Preconditions

The restoration layer cannot deploy before the telemetry proves detector separation: an actuator acting on an unproven diagnosis is damage without a cause. Deployment is gated on the same separation bar as every detector family (doc 05 §3), and the family's honest 1B status stands in `ARCHITECTURE_OVERVIEW.md` — unwired until the shadow-replay yield is measured.

## 9. What this layer does not do

No threshold set, moved, or adjudicated. No actuator fires in evaluation — every evaluation walk runs under the monitor-walk law (doc 05 §2). No verdict re-scores a banked disposition. No grade is computed from anything the model said about itself. Nothing deploys before its pre-registration carries the author's stamp.

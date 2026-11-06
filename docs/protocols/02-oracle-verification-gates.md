# Oracle-Verification Gates — Gate 17 (Public Protocol Summary)

The runtime gates govern walks; **Gate 17 governs the evaluation program itself.** It is a family of domain oracles that verify model output against zero-model ground truth — each arm pre-registered before build, each running offline against banked telemetry, each exercised by engineered fixture suites whose every row's ground truth was verified at build. The runtime gate map is in `ARCHITECTURE_OVERVIEW.md`; this document is the protocol record of the verification family.

## 1. The class contract — invariants shared by every arm

1. **Layer-free.** The oracle reads the decoded surface text only. No hidden-state, attention, or residual reads — deliberately on the far side of the runtime gates.
2. **Commitment-boundary firing.** Evaluation happens only when a candidate statement completes — an equation, a code block, a concluding claim. Cost is an amortized surface scan, not a per-step model read.
3. **Zero-model oracle.** The verdict is deterministic recomputation, execution, or traceability — never a statistical threshold. The only knobs are the domain's tolerance conventions, fixed at fixture time and stamped once.
4. **Fails-open.** Ambiguity never fires. A missed statement costs *coverage* (measured by census); a false fire costs *damage* (unrefundable). The asymmetry is law.
5. **Flag-first.** Verdicts write to the fault ledger. Actuation routes through lane-conflict arbitration (G11) only after each arm's acceptance — and the initial policy is the identity: **flag only.**

## 2. Division of authority

The oracle emits; the restoration operators act. An oracle never modifies model state. Its actuation menu is the pre-registered restoration set — cache eviction of the flagged window, re-anchoring toward the grounding evidence, commitment redistribution, exit as fallback — and selecting among them is arbitration's job, never the oracle's. The family's safety property lives at this interface: **the program only ever selects among states the model itself reached; it never fabricates one.**

## 3. The arms

### 17-A — Arithmetic verification

Watches completed arithmetic statements in generated text. The oracle recomputes each statement exactly — under both standard-precedence and left-to-right readings — and compares against the stated result at the stated display precision. Verdict classes: **PASS / SLIP-FLAG / UNVERIFIED** (fails-open). Two guards convert the dominant false-fire classes into logged non-fires: a **fragment guard** (a statement that is really a fragment of a larger expression) and a **conservative re-parse** (one word of additional context proves the statement true).

Acceptance gates (pre-registered, binding): the runtime build must reproduce the banked genuine-slip census exactly, with the censused false-fire classes suppressed; zero fires on the negative-control fixture family; measured trigger precision must beat the offline extraction bounds; and every remaining fire class is charged against the unguided baseline.

Fixtures: the arith suite in `fixtures/` — positive slip classes drawn from measured failures, negative controls covering every censured harmless class.

Cost posture: surface scan only — orders below the runtime gates' instrumentation ceiling, and re-measured against it at acceptance.

### 17-C — Code verification

The oracle is **sandboxed execution against the task's canonical test suite** — the verdict is the run. Verdict classes: **PASS / FAIL-TESTS / FAIL-TRACE** (the stated answer contradicts what the code computes) **/ UNVERIFIED** (truncated, uncompilable, no extractable block, or out of budget — resource limits are a resource class, never a semantic fail).

Three standing laws:

- **The deterministic-meter law.** Execution budgets are metered operation counts, never wall-clock — a verdict whose semantics depend on wall-clock is non-deterministic across runs. Wall-clock survives only as a separate, higher safety failsafe that protects the host and never produces a semantic verdict.
- **The sandbox law.** Model-generated code executes only in a sandbox. Never on the host.
- **The honesty clause.** The banked rejudged labels are an *input* to the offline pass — instrument validation and cost census — never a result it re-derives.

Structure: **Tier 0** — static well-formedness at block completion (costs nothing, produces the UNVERIFIED classes). **Tier 1** — deferred execution after generation completes: the default. **Tier 2** — in-loop blocking execution, justified only if the cost census proves post-block commitments exist in volume. Evidence-gated, never assumed; each arm banks its own overhead ceiling — ceilings do not inherit between arms.

### 17-P — Prose verification

The honest boundary first: **no zero-model oracle exists for general semantic correctness**, and none is smuggled in. What is mechanically checkable — and therefore designable — is threefold:

- **P1 — Constraint compliance.** The prompt is the oracle: length limits, required and forbidden inclusions, format and schema validity.
- **P2 — Quantity/entity provenance.** A ledger of every salient quantity the generation establishes, each traced to its origin. A conclusion that leans on an untraced quantity — or on a quantity derived from a flagged slip — is flagged. The text's own commitments are the oracle; zero world knowledge enters any verdict.
- **P3 — Quote/claim anchoring.** Stated quotes must exist in the source under normalized matching.

17-P measures nothing until a prose corpus leg exists; the corpus is published in `corpora/`.

### 17-P2 — Sycophancy elicitation

The corpus is published in `corpora/` — two bait families (wish-restatement and artifact-drafting), crossed with an evidence axis (contradicting / evidence-absent / consistent-control). The catch classes, of record:

- **Assertion-slot promotion** — a value the user wished for re-emerging in the committed-answer position with no establishment event behind it.
- **Authored-artifact promotion** — a wished-for value written into a requested artifact as established fact.
- **Conflict** — two fact-framed values for the same quantity in one generation: one tracing to the evidence, one to the wish.

The immunity classes never fire: the wish kept as a wish, the honest contrast, the honest report. The establishment-event law holds: derivation, measurement, or anchored quotation is the only legal path from a wish to a fact. Honesty clauses, carried on every rate: all measurements on designed bait are **elicitation-conditioned** — detector performance where the fault was made likely, never the model's natural emission rates; the oracles are the generation's own ledger; every ambiguity fails open and is censused.

### 17-AP — Attention-provenance capture

The routing-channel readout: **where the model's attention mass actually sits** across the context — on the evidence, on its own continuation, or on its own repeated window. Its purpose is a second witness on the false-alarm axis: true degeneration attends to its own repeated window; a benign commitment spike attends to evidence. The existing channels conflate the two; the routing channel should not.

Features are per-step scalar mass allocations computed in the capture hook (constant memory; no attention matrices stored), aggregated on normalized depth bands — the portability choice: constants re-derive per model, the form ports. Expected directions are committed before any run. Detection-only, zero actuation: the named downstream consumers (the re-anchor trigger, the loop-quarantine warning threshold) earn nothing until separation is measured. The family's boundary law: **mass allocations only** — never output-distribution statistics, never hidden-state coordinates; commitment-point entropies are excluded by name. And the honest clause: if the routing channel proves as weak at this scale as the one previously-tried attention feature was, the family closes here honestly, and the route forward is the model ladder.

## 4. Sequencing and acceptance

Arm order follows the data: measured-data first (17-A), banked corpus second (17-C), new corpus third (17-P), with the sycophancy and attention-provenance arms entering as their corpora and contrast populations bank. All arms share the class contract, the fixture machinery, and one acceptance discipline: **adjudicated on fresh, held-out walks under pinned protocols — never on the data they were developed against.** The 1B-era numbers stay this model's record; structure transfers up the model ladder, numbers do not.

# Fixture Validation Suites (Public Protocol Summary)

An offline pass measures an oracle against *natural* generations. A fixture suite measures it against **authored truth**: documents we write with the fault — or the harmlessness — engineered in, every row's ground truth verified before the oracle ever reads it. The suite measures the oracle, never the model; engineered fixtures complement the natural corpora and never re-read or re-adjudicate them. The suites of record are published in `fixtures/` (arith, code, prose); this document is the protocol record of how they were built and what accepting an oracle on them means.

## 1. The fixture law (shared by every suite)

1. **Born typed.** Every fixture is one typed row — class, authored content, exact ground truth, expected verdict, guard expectations — with zero narrative-fillable slots. The truth is in the row before the instrument runs.
2. **Ground truth verified at build.** Arithmetic rows carry exact rational ground truth, re-verified at build; code rows are executed against their own harnesses at build, with each positive asserted to fail and each control asserted to pass; prose rows are authored from templates that guarantee the event shape, with the typed slots asserted mechanically. Any assertion failure is a build-gate catch: **fix the fixture or the builder — never the instrument.**
3. **Deterministic build.** Templated, zero randomness, zero model, zero GPU. Rebuild must be byte-identical; every suite, builder, and acceptance run carries a checksum pinned to the record.
4. **Breadth, not confidence.** Deterministic ground truth means sizing governs breadth of class-space coverage, not statistical confidence. No fixture count is ever sold as a confidence level.
5. **Consumed exactly once.** The acceptance run reconciles its census: every fixture consumed exactly once, zero orphans.

## 2. The class space — positives, controls, and honest boundaries

**Positives** are engineered fault classes drawn from the measured habits of the program's own failure record: late-chain slips and cascades, sign slips, compounding chains, round-trip conversions, verified internal contradictions (arith); boundary mutations, condition inversions, operand and return slips, propagated cascades (code); assertion-slot promotions, evidence-absent promotions, authored-artifact promotions, and ledger conflicts (prose). Within every firing class, failures are typed at **both loud and subtle extremes in balanced counts** — the smoothing census: the suite measures whether the oracle preserves the engineered asymmetry, flagging loud and subtle per their typed expectations, with zero magnitude-dependent smoothing creeping in through the guards.

**Negative controls** are harmless look-alikes — the measured habits of correct output that a naive checker would fire on: fragments of larger expressions, word-separated statements, equivalence chains, dimension-laden prose, format notations (arith); correct solutions, seeded harnesses, resource-heavy-but-legal programs (code); the immunity classes — the wish kept as a wish, the honest contrast, the honest report — plus legal establishment through a verified derivation, measurement, or anchored quote (prose). Acceptance is **zero fires** on the zero-fire classes: a fire on them is a false fire of record, and nothing refunds it. Alongside them, the **fails-open classes** (truncated, uncompilable, empty, multi-block; unmarked desires; silence) give the coverage machinery its exercise: the direction under test is that no verdict is invented to fill a gap.

**Boundary classes put each arm's known blind spot on engineered record.** Each suite authors the fault its oracle cannot see — the stated-answer prose contradicting verified code output; the paraphrase-form promotion of a desired value — and censuses the miss on the row. The oracle is measured as-is; the coverage boundary is measured, not assumed; and any future oracle extension is its own pre-registration and stamp.

## 3. Per-arm notes

- **Arith.** Both anchor families (inline and scratchpad) instantiated per class where the class permits. The display conventions the oracle left open are author-stamped at fixture time: truncation displays ruled legal by convention (a genuine slip never equals its own truncation); compression notations carried as a censused note-class, not charged damage, with any future guard named a wiring-phase design candidate. The tolerance form itself is banked and unchanged.
- **Code.** Every runnable row asserts meter determinism at build. Randomized harnesses appear only in their seeded form (fixed seed, deterministic by law) and carry their own recorded rule fixed at fixture time. The meter budget is pinned from the measured cost distribution at fixture time, author-stamped, and rides to wiring as the enforcement ceiling; its value lives in the results record.
- **Prose.** Firing classes are typed across the full loud/subtle × raw/chat sub-matrix, so the register question — does the authored record preserve or collapse the register asymmetry the natural record showed — is itself a measured reading. Every rate the prose record banked is elicitation-conditioned and carries that term with it into the suite.

## 4. Acceptance — the replay contract

Each suite is replayed offline through the **banked instrument of record** for its arm — the same build that ran the offline pass — via an additive fixture-mode wrapper that imports the oracle verbatim: **zero oracle-logic change.** The run emits a per-fixture expected-vs-actual table, the fault-ledger lines, and the guard census. The pre-registered acceptance readings:

1. **Runs-clean.** Census reconciliation exact; every fixture typed, consumed exactly once.
2. **The negative-control gate.** Zero fires on the zero-fire classes; fails-open classes unverified exactly as typed, no invented flags.
3. **The trigger-precision budget.** Flags-on-authored-positives over all flags, charged under the family's stamped conventions, must beat the offline as-is bounds (the bounds and the measured precisions live in the results record). The natural-leg numbers are carry-in color, never the acceptance number.
4. **Damage accounting.** Every remaining fire class is charged against the unguided wrong-finish baseline — recorded, never adjudicated here.
5. **The honest miss record.** A positive class that yields zero flags is a detector miss, recorded as a measured coverage cost — never smoothed, never quietly dropped. There is no low-emission concept on engineered ground truth.

Acceptance outcomes for each arm live in the results record; the suites, builders, and this protocol are the standing contract that any future re-run must reproduce.

## 5. What the suites do not do

No model. No generation. No natural-corpus re-read; nothing re-derived from a banked artifact. No threshold adjudication — the conventions named here are fixture-time author stamps. No actuation, no wiring, no trigger decisions. The suites emit the fault-ledger lines a future localization pass may consume; they consume nothing. The author's stamps adjudicate every reading — these suites present, never adjudicate.

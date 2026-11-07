# Triadic Set Telemetry: Runtime Governance of the Transformer Forward Pass

**Author:** Nathaniel Alphonso Nibbs Jr.  
**Affiliation:** Alphonso Systems & Infrastructure  
**Publications:** [Alphonso Systems & Infrastructure Public Substack](https://nathanielalphonso.substack.com)  
**Media & Technical Contact:** nathanielalphonsonibbsjr@gmail.com  


---

The **Triadic Set** governs the forward pass of a language model directly: measured constraints, enforced inside the execution path at calibrated moments, that steer a model away from trajectories destined for discard and restore output that would otherwise be lost. The payoff is the one inference treats as a trade-off: compute falls and accuracy rises, at the same time, on the same model. This repository is my proof that the payoff is real: every claim pre-registered, every run checksummed, every adjudication replayable by anyone, on zero GPUs.

---

## The Case for In-Band Governance

**The problem.** Inference today is governed after the fact, and it pays for that every time it runs. A model wanders into a degenerate loop, so the stack reruns it. An answer might be wrong, so the stack re-checks it. Output comes back unusable, so it is discarded and regenerated. Correction loops, re-verification passes, self-consistency votes: every fix the industry has for a wasteful forward pass spends additional compute to compensate for a pass that was never governed in the first place. The industry treats that waste as a universal truth of the medium: priced in, budgeted, and accepted as the cost of doing business. The Triadic Set treats it as an engineering target, the same waste accounted for sooner, cheaper, and more reliably, inside the forward path itself.

**The thesis.** The Triadic Set's position is that the waste is governable at the source. The forward pass can be constrained inside its own execution graph, at calibrated moments, before the waste is ever emitted. Constraint is only half of the mechanism. The other half is restoration: trajectories that would have been thrown away are recovered to usable form. Compute drops because less of it is wasted. Accuracy rises because what survives governance is better output from the same model. The field reads governance as a purchase, accuracy bought with compute or compute saved at the price of accuracy. The Triadic Set breaks that frame: the two directions move together, compute falling and accuracy rising on the same pass.

**The founding result.** From Phase 2 below: across all 57 MMLU tasks plus GSM8K (10,219 evaluated questions, 1,131,648 processed tokens), the governed system removed 50.43% of the attention paths and accuracy rose 11.53% over the stock baseline, at the same time, on the same model. On the hardware side of the same record, time-to-first-token dropped 61.22%, swap churn went to exactly zero, and the prefill context footprint compressed 88.41%. Every number above points at the log that produced it.

**The agnostic principle.** The mechanism is derived, not trained in, and it is agnostic to everything about a model except the one thing every model shares. The governance map is extracted from the measured execution of a model's own unmodified weights and calibrated layer by layer, so the mathematics re-derives to fit the model, never the other way around: the math bends to the measured data, the data is never reshaped to fit the instrument. Model-agnostic, parameter-agnostic, weight-agnostic: the map re-derives from whatever model sits in front of it. Change the parameter count and the map re-derives. Retrain the weights and the map re-derives. Swap in the next model and the map re-derives. No model, scale, or checkpoint owns it, because governance touches only the forward pass, the one structure every autoregressive model has in common. That universality is the design intent: upgrade the model, retrain the weights, change the parameter count, and the deployment never waits on a redesign. The model ladder is the principle's receipt in the record below: the 1B system's map re-derived and re-validated at 3B, the 8B transfer the open front.

**What the rigor buys.** The utility of this record extends past its headline numbers: every claim in it can be checked, replayed, and reused by anyone. Every instrument was pre-registered before it was built. Every run of record carries SHA-256 receipts for its inputs and outputs. Every adjudication replays banked bytes mechanically, with zero GPU contact. The program runs deeper than benchmarking: it works step by step through the precise mechanics of the governed pass, defining what the mechanism does, what it costs, and what it restores, until every component of the claim carries its own measurement and its own receipt. A score tells the field what happened once; a specification tells a deployer what happens every time, and a specification is what the Triadic Set is building. The full set of commitments lives in [Methodology Commitments](#methodology-commitments), and the mathematical core stays protected ([What Is Withheld](#what-is-withheld)) while everything around it is open.

---

## What This Repository Is

The repository itself is the evidence: the hardware telemetry, evaluation programs, engineered validation fixtures, calibration tooling, and integrity receipts behind the case above, produced under one conviction: **the forward pass of a language model deserves active governance, enforced inside the execution path itself.** Every artifact in it is measured, pre-registered, and checksummed. The underlying mathematical core of the architecture stays protected (see [What Is Withheld](#what-is-withheld)).

---

## Current State

**Where the testing stands (Nov 2026):** the initial testing and validation, the five-phase empirical record below, is complete and fully published. The live work front is the **In-Band Qualification Testing**: the first refinement (the operating-threshold re-derivation) is in progress, the refinements and pre-registrations behind it standing at my word. On the model ladder, the 3B transfer is complete and receipted; the 8B record lane is the open front. The full forward structure is mapped in [In-Band Qualification Testing](#in-band-qualification-testing).

---

## The Triadic Set at a Glance

The architecture is a four-tier governance loop spanning ingress to output. The full conceptual breakdown, hook placement, and evaluation rig live in the [Architecture Overview](docs/ARCHITECTURE_OVERVIEW.md):

- **Tier A (Ingress):** evaluates incoming context at the embedding boundary before the compute budget is spent, stabilizing the input state.
- **Tier B (Attention Interdiction):** intervenes in the attention core, excising structurally noisy pathways before they consume memory bandwidth. Calibration follows each layer's depth individually.
- **Tier C (The Exit Gate):** governs the egress head, breaking degenerate recursion and enforcing single-turn finality: a walk exits once, cleanly, with its output verdict.
- **Tier D (The Drift Circuit):** tracks layer-to-layer trajectory health in real time and trips a fail-closed, non-destructive halt when the trajectory breaches calibrated bounds.

Above the tiers sits the **posture and orchestration layer**: every governed walk exits with a measured confidence posture (clean, degraded, or calibrated-rejection) recorded from the walk's own telemetry. The same telemetry drives the detector and exit-gate evaluation programs documented in this repository.

---

## The Hypothesis

The program exists to answer a single question: **can a language model's forward pass be governed at runtime, constrained at calibrated moments, so that compute falls and accuracy rises at the same time?** The case above states my answer in plain terms; this section decomposes it so every part can be tested.

Three framings govern how every cost and savings number in this program is read:

1. **Measured overhead is an upper bound.** Every governance cost measured on the local test bench carries an itemizable fraction of test instrumentation that a production serving path would drop. Bench numbers therefore overstate production governance cost, which keeps every published cost claim conservative.
2. **Savings scale with prevalence.** The waste the architecture targets (correction loops, apology preambles, re-verification passes, degenerate output) is a property of real multi-turn and agentic deployment. Savings claims are scoped accordingly.
3. **Every test discharges a claim.** The whole program hangs off a decomposed claims spine (below); any measurement outside that spine stays out of scope.

### The Claims Spine (C1–C7)

The hypothesis is decomposed into seven claim components. Every test, gate, and acceptance criterion in the program is labeled with the component it discharges:

| # | Claim | In words |
| :--- | :--- | :--- |
| **C1** | Constraint **prevents** undesirable output | Interventions must never wrongfully terminate or redirect a healthy trajectory; wrongful terminations stay at zero as intervention counts grow. |
| **C2** | Constraint **restores** otherwise-discarded output | Trajectories that would have been thrown away are recovered to usable form more often than healthy output is worsened. |
| **C3** | Cost per usable output **drops** | Under governance, fewer tokens and fewer seconds are spent per correct, usable answer, with usable accuracy never below baseline. |
| **C4** | Measured overhead is an **upper bound** | The instrumentation fraction of bench-measured cost is itemized; production governance cost sits strictly below it. |
| **C5** | Savings **scale** with degenerate-output prevalence | In multi-turn deployment, the waste ratio under governance beats baseline, which is the industry cost being targeted. |
| **C6** | Confabulation is **detectable** at the commitment point | On populations where the model commits to known-wrong answers, the detectors separate flagged from clean trajectories with measured, reported confidence. |
| **C7** | Confabulated paths can be made **improbable by redistribution** | When the first-choice path is flagged, the model's own alternative path lands correct at a measured yield above first choice, with wrongful redirection bounded and counted. |

**The universal fail rule:** a FAIL sends the gate back for redesign; thresholds and acceptance criteria hold fixed. Thresholds are calibrated against data alone.

---

## Initial Testing & Validation

The program's initial testing and validation record, complete and fully published, runs in five phases:

### Phase 1: Single-Stream Silicon Telemetry (Aug–Sept 2026)

Bare-metal execution traces on Apple Silicon unified memory, establishing the hardware-level effect of in-band interdiction at batch size 1:

| Metric Vector | Unconstrained Baseline | Interdicted Execution | Delta / Gain |
| :--- | :--- | :--- | :--- |
| **Time-To-First-Token (TTFT)** | 1,658 ms | 643 ms | **−61.22% latency reduction** |
| **Active Swap Churn** | Memory-pressure pagination | Exactly 0 B | **Complete elimination of swap churn** |
| **Prefill Context Footprint** | Dynamic allocation (100%) | Compressed | **−88.41% footprint compression** |
| **Forward-Pass Compute Floor** | Unconstrained | 25.95% floor | **74.05% compute reclaimed** |

*Raw logs: `telemetry/single_stream_archive/`, `telemetry/single_stream_eval/`.*

### Phase 2: Multi-Batch Benchmark Validation (Sept 2026)

Full multi-batch evaluation across all 57 MMLU tasks and GSM8K (10,219 evaluated questions, 1,131,648 processed tokens) on the calibrated architecture:

| Benchmark Evaluation State | Attention Sparsity | MMLU Scaled Accuracy | Architectural Delta |
| :--- | :--- | :--- | :--- |
| Unhooked stock control | 0.00% (dense) | 37.89% | Unmodified baseline |
| Degraded sampling run | 0.00% (dense) | 22.71% | Failure mode of uncalibrated thresholding |
| Naive hook interception | ~50.00% | 34.56% | Uniform static boundaries; over-clamps early layers |
| **Triadic (calibrated)** | **50.43%** | **49.42%** | **+11.53% accuracy lift over stock baseline** |

The Phase 2 table is the program's founding result: **governance raised accuracy while removing half of the attention paths**, demonstrating constraint and restoration together. *Raw logs and category JSON: `telemetry/multi_batch_eval/`.*

### Phase 3: The Test & Evaluation Program on 1B (Oct 2026)

With the founding result established, the program moved from demonstrating the architecture to trying to *break* it. A formal Test & Evaluation plan put the 1B-scale system under oracle verification, held-out adjudication, and pre-registered acceptance readings across two evaluation regimes: **single-pass generation** and **multi-turn deployment** (where interface gates govern turn-boundary behavior).

The phase runs as eight pre-registered lanes, each with its protocol summary in `docs/protocols/` and its results in this repository:

| # | Lane | Protocol | Results |
| :--- | :--- | :--- | :--- |
| 3.1 | The Test & Evaluation Plan | [01](docs/protocols/01-test-and-evaluation-plan.md) | governs every lane below |
| 3.2 | Oracle-verification gates | [02](docs/protocols/02-oracle-verification-gates.md) | `telemetry/v32/gate17/` |
| 3.3 | Offline checker passes | [03](docs/protocols/03-offline-checker-passes.md) | `telemetry/v32/offline-passes/` |
| 3.4 | Fixture validation suites | [04](docs/protocols/04-fixture-validation-suite.md) | `fixtures/` |
| 3.5 | Fresh-walk adjudication | [05](docs/protocols/05-fresh-walk-adjudication.md) | `telemetry/v32/rw15/` |
| 3.6 | Dual-sided ensemble | [06](docs/protocols/06-dual-sided-ensemble.md) | `telemetry/v32/rw16/` |
| 3.7 | Emission-degeneration program | [07](docs/protocols/07-emission-degeneration-program.md) | `telemetry/v32/rw17/` |
| 3.8 | Exit-verdict & restoration | [08](docs/protocols/08-exit-verdict-and-restoration.md) | `telemetry/v32/exit-verdict/` |

**The gates (3.2)** are independent mechanical oracles: arithmetic, code, prose, and sycophancy-elicitation output verified against engineered ground truth, each oracle pre-registered before its arm was built. **The checker passes (3.3)** replay banked telemetry mechanically, with zero GPU contact, so every adjudication is a deterministic replay of banked bytes. **The fixture suites (3.4)** hold 288+ typed test rows across three families (arithmetic, code, prose) with engineered positive classes and negative controls, every row's ground truth verified at build.

**The rework programs (3.5–3.7)** run the program's falsification discipline. Fresh-walk adjudication forces every detector candidate to re-earn its harness on held-out fresh walks under pinned protocols, keeping the candidate's development data out of the grading path. The dual-sided ensemble and emission-degeneration lanes extend the same discipline to multi-sided adjudication and to degenerate-output emission. **The exit-verdict instrumentation (3.8)** grades every governed walk (clean, degraded, or calibrated-rejection) from recorded telemetry alone, and the restoration protocol defines what the system does with what it recovers.

### Phase 4: Model-Scale Transfer, 3B → 8B (Oct 2026 → present)

The governance map re-derives and re-validates at every step of the model ladder, from 1B through 3B to 8B parameters. Phase 4 re-runs the checker passes and acceptance arms at each scale and records the transfer honestly, including where the map re-derived cleanly and where the transfer surfaced real findings.

**The 3B transfer is complete and receipted; the 8B record lane is the program's open scale-transfer front.** The receipts of record to date (checker-pass exports, the s5 panel and s8 rework receipts, and the ap17 join exports) publish in `telemetry/v32/phase4/`, with the protocol summary in [doc 09](docs/protocols/09-model-scale-transfer.md). Development batteries produced along the way are withheld as development-data-only, named and counted in that directory's record.

### Phase 5: Environment Drift, Baselining & Audits (Oct 2026 → present)

Governance depends on an environment that stays measured. Phase 5 instruments the environment itself: corpus drift is measured against pinned baselines, re-baselining acts are pre-registered before they run, and the drift-diagnostic receipts (the 3-miss, alane, b12, codev6/7, and d2sat diagnostic panels, plus the Wu population-comparability read receipts) publish in `telemetry/v32/diagnostics/` under [doc 10](docs/protocols/10-environment-drift-and-baselining.md).

The phase also carries the program's external accountability: audit engagements are pre-registered at the boundary and their outcomes are published at count level in [doc 11](docs/protocols/11-audit-engagements.md), and the species-development lane (the program's instrument-breeding line for new diagnostic species) is documented intent-only in [doc 12](docs/protocols/12-species-development.md), with its development data remaining internal.

---

Phase 3–5 artifacts publish here lane by lane as they land: results and receipts in `telemetry/v32/`, protocols in `docs/protocols/`, fixtures in `fixtures/`, and the prompt corpora behind them in `corpora/`.

---

## In-Band Qualification Testing

Everything in the record above ran out of band: telemetry banked, passes replayed, adjudication with zero model contact. The In-Band Qualification Testing is the main test: the disparate pieces of the initial record pulled into one assembled system and qualified inside live forward passes, from the first refinement to the reconciliation. The refinements run on development data today; the actuated stages run live; both belong to the same qualification arc.

**The ten refinements.** The mechanism itself gets refined:

| # | The refinement | Status |
| :--- | :--- | :--- |
| 1 | Re-deriving the live operating threshold and its look-window from the banked data; the head of everything | In progress |
| 2 | A persistence-gated refinement sheet for the sycophancy-corpus leg | Pending |
| 3 | The code arm's channel change: a parse-side magnitude read of the generated self-test tail | Pending |
| 4 | An 8B-native fixture re-authoring of the W5 references: fixture re-authoring, hypothesis remaining unchanged | Pending |
| 5 | A depth-native comparison form for the identity check | Pending |
| 6 | A union-controlled re-test of the committed-direction construction | Pending |
| 7 | An administrative meter-budget stamp | Pending |
| 8 | Restricting the detector form to the measured near-tie band | Pending |
| 9 | Receipts pinning the mechanism's sensitivity, sizing, coverage, and provenance | Pending |
| 10 | Reconciliation, review and integration | Pending |

**The staged order.** What remains to be tested, and in what order:

| Stage | What it is | Status |
| :--- | :--- | :--- |
| **Stage 0** | The offline rulings that closed before the live work: a twice-run determinism receipt with the operating-form ruling on the amended grid, the amended grid's console acceptance, the protected-frame ruling and its replication candidate on the math leg, and the gates-3/5 numbering harmonization into the unified map | Complete (all four stamped and banked) |
| **Stage 1** | The forward-pass pre-registrations (5 items) | In progress |
| **Stage 2** | The splitter's ground truth: the mixed-regime corpus/fixture build | Pending |
| **Stage 3** | The restoration ladder: one actuator per run pair, on GPU | Pending |
| **Stage 4** | The wiring phase: live actuation behind the acceptances | Pending |
| **Stage 5** | The model ladder, riding the Phase 4 record lane | In progress (3B complete and receipted; the 8B record lane ongoing) |
| **Stage 6** | Regime B: the multi-turn harness and the agentic-regime gates | Pending |

The ten refinements produce the mechanism; the staged order tests it. Both close at the same table: the tenth refinement, reconciliation, review and integration, where all data gotten is read against the truth labels of record. A landed stage migrates into the record above as a new chapter, so the phase list stays open. Actuation follows acceptance: instruments present findings, and my stamps adjudicate. The forward act for every finding in this repository remains the held-out measurement on a live environment.

---

## Methodology Commitments

Every artifact in this record is produced under the same house discipline:

1. **Pre-registration before everything.** Every instrument is built and every run is executed only after its protocol and acceptance readings are written down and pinned.
2. **Determinism and receipts.** Instruments rebuild byte-identically; every run of record carries SHA-256 integrity receipts for its inputs and outputs.
3. **Fail-loud instruments.** Missing data, census violations, and out-of-band conditions hard-exit. The instruments fail loudly by construction.
4. **Fix the fixture or the builder, never the instrument.** When a discrepancy appears, the banked instrument is presumed correct; the discrepancy is resolved upstream and the fix is recorded honestly.
5. **Zero-GPU adjudication.** Offline passes replay banked telemetry and exports mechanically, with no model contact and no adjudication drift.
6. **Held-out honesty.** Findings are stated as valid per the development data, with the held-out measurement always named as the forward act.

---

## Repository Layout

```text
triadic-set-telemetry/
├── README.md                 ← this document
├── docs/
│   ├── ARCHITECTURE_OVERVIEW.md   ← the four-tier pipeline, hook map, evaluation rig
│   └── protocols/            ← polished test-protocol summaries, one per program lane
├── configs/                  ← per-layer calibration outputs (τ/σ maps)
├── scripts/                  ← calibration harnesses and tooling plumbing
├── fixtures/                 ← engineered fixture suites + negative fixtures (θ-clean test data)
├── corpora/                  ← prompt corpora behind the evaluation legs
└── telemetry/                ← the empirical record itself
    ├── single_stream_archive/    (Phase 1)
    ├── single_stream_eval/       (Phase 1)
    ├── multi_batch_eval/         (Phase 2)
    └── v32/                      (Phases 3–5, by program lane)
        ├── gate17/  offline-passes/  rw15/  rw16/  rw17/  exit-verdict/   (Phase 3: T&E on 1B)
        ├── phase4/                (Phase 4: scale transfer 3B → 8B)
        └── diagnostics/          (Phase 5: drift, baselining, diagnostics)
```

---

## What Is Withheld

The exact dynamic threshold calculus and the closed-form mathematical transformations of the Triadic Set remain a protected black box. What publishes here is everything around the core: the conceptual mechanics, calibration outputs, hardware telemetry, evaluation results, fixtures, and receipts. This split is deliberate and stable; the record is fully auditable at the empirical level while the derivations that make the architecture work stay protected.

---

## Local Replication & Auditing

1. **Extract calibration perimeters from unmodified base weights:**
```bash
python3 scripts/calibrate_triadic_v3.py
```
2. **Rebuild the fixture suites deterministically** from their published builders in `fixtures/`; each rebuilds byte-identically against its recorded checksum.
3. **Replay the offline passes** over the published exports in `telemetry/v32/`; every adjudication is a zero-GPU mechanical replay.
4. **Benchmark the hook latency** with hardware-flushed streaming queues:
```bash
python3 scripts/stream_triadic_latency.py
```

---

*Cite this record by run artifact ID and SHA-256 receipt. Every number in this repository points at the log that produced it.*

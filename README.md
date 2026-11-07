# Triadic Set Telemetry: Runtime Governance of the Transformer Forward Pass

**Author:** Nathaniel Alphonso Nibbs Jr.  
**Affiliation:** Alphonso Systems & Infrastructure  
**Publications:** [Alphonso Systems & Infrastructure Public Substack](https://nathanielalphonso.substack.com)  
**Media & Technical Contact:** nathanielalphonsonibbsjr@gmail.com  


---

## What This Repository Is

This is the public empirical record of the **Triadic Set**, a runtime governance architecture for autoregressive language models. It holds the hardware telemetry, evaluation programs, engineered validation fixtures, calibration tooling, and integrity receipts of an ongoing program built on one conviction: **the forward pass of a language model deserves active governance, enforced inside the execution path itself.**

Modern inference stacks already accept this premise implicitly: they burn compute on correction loops, re-verification passes, and discardable output after the fact. The Triadic Set brings that governance *in-band*: structural constraints enforced inside the model's own execution graph, at calibrated moments, before waste is ever emitted. Everything in this repository is measured, pre-registered, and checksummed. The underlying mathematical core of the architecture stays protected (see [What Is Withheld](#what-is-withheld)).

---

## Current State

**Where the testing stands (Nov 2026):** the five-phase empirical record below is complete and fully published. The program's live work front is Stage 1 of the **Master Validation Sequence** (the forward-pass pre-registrations), with the splitter build act in progress and the remaining pre-registrations standing at the author's word. On the model ladder, the 3B transfer is complete and receipted; the 8B record lane is the open front. The full forward structure is mapped in [Where the Program Stands](#where-the-program-stands).

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

The program exists to answer a single question: **can a language model's forward pass be governed at runtime, constrained at calibrated moments, so that compute falls and accuracy rises at the same time?**

The Triadic Set's position is that it can, with one essential correction: accuracy gained this way comes from **constraint and restoration**. The system keeps the model's existing competence pointed at usable output: it steers the model away from trajectories that were destined to be discarded, and it restores otherwise-lost output to usable form. Compute drops because less of it is wasted; accuracy rises because what survives governance is better output from the same model.

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

## The Program Record

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

## Where the Program Stands

The five phases above are fully published, and the program continues under two structures of record that interlock:

- the **ten-step refinement spine**, the mechanism-refinement program. Its first step (the operating-threshold re-derivation) is in progress; the refinement steps behind it are unopened; the reconciliation review comes last. This is how the mechanism itself gets refined.
- the **Master Validation Sequence**, the staged remaining-test list, ordered to build on the refinement program's outputs. This is what remains to be tested, and in what order.

The spine produces the mechanism; the Sequence tests it. The interlock is active today: the spine's first step is executing through the Sequence's Stage-1 acts, and both ladders close at the same table. After the Sequence's stages and the refinement steps, the reconciliation review reads all data gotten against the truth labels of record, the author's stamps adjudicating.

| Stage | What it is | Status |
| :--- | :--- | :--- |
| **Stage 0** | The paper closers (4 items) | Standing open |
| **Stage 1** | The forward-pass pre-registrations (5 items) | The validation-phase readout instrument ran author-side green end-to-end; the splitter pre-registration is stamped with its build act in progress; the remaining pre-registrations are drafted or standing at the author's word |
| **Stage 2** | The splitter's ground truth: the mixed-regime corpus/fixture build | Unopened |
| **Stage 3** | The restoration ladder: one actuator per run pair, on GPU | Unopened |
| **Stage 4** | The wiring phase: live actuation behind the acceptances | Unopened |
| **Stage 5** | The model ladder: the scale transfers (the Phase 4 record above) | 3B complete and receipted; the 8B record lane ongoing |
| **Stage 6** | Regime B: the multi-turn harness and the agentic-regime gates | Unopened |

Actuation follows acceptance: instruments present findings, and the author's stamps adjudicate. The forward act for every finding in this repository remains the held-out measurement on a live environment.

The phase list itself stays open: Sequence stages land as new record chapters. Stage 5's landing completes Phase 4, and the agentic regime (Stage 6) opens the next chapter when it lands.

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

# Triadic Set Telemetry: Runtime Governance of the Transformer Forward Pass

**Author:** Nathaniel Alphonso Nibbs Jr.  
**Affiliation:** Alphonso Systems & Infrastructure  
**Publications:** [Alphonso Systems & Infrastructure Public Substack](https://nathanielalphonso.substack.com)  
**Media & Technical Contact:** nathanielalphonsonibbsjr@gmail.com  


---

## What This Repository Is

This is the public empirical record of the **Triadic Set** — a runtime governance architecture for autoregressive language models. It holds the hardware telemetry, evaluation programs, engineered validation fixtures, calibration tooling, and integrity receipts of an ongoing program built on one conviction: **the forward pass of a language model is something to be governed, not merely executed.**

Modern inference stacks already accept this premise implicitly — they burn compute on correction loops, re-verification passes, and discardable output after the fact. The Triadic Set brings that governance *in-band*: structural constraints enforced inside the model's own execution graph, at calibrated moments, before waste is ever emitted. Everything in this repository is measured, pre-registered, and checksummed. What it deliberately does not contain is the underlying mathematical core of the architecture (see [What Is Withheld](#what-is-withheld)).

---

## The Hypothesis

The program exists to answer a single question: **can a language model's forward pass be governed at runtime — constrained at calibrated moments — so that compute falls and accuracy rises at the same time?**

The Triadic Set's position is that it can, with one essential correction: accuracy gained this way comes from **constraint and restoration, not capability addition**. The system does not make the model smarter; it prevents the model from spending its competence on trajectories that were destined to be discarded, and it restores otherwise-lost output to usable form. Compute drops because less of it is wasted; accuracy rises because what survives governance is better, not different.

Three framings govern how every cost and savings number in this program is read:

1. **Measured overhead is a ceiling, not a floor.** Every governance cost measured on the local test bench carries an itemizable fraction of test instrumentation that a production serving path would not carry. Bench numbers are therefore conservative ceilings on production governance cost.
2. **Savings scale with prevalence.** The waste the architecture targets — correction loops, apology preambles, re-verification passes, degenerate output — is a property of real multi-turn and agentic deployment, not of single-pass benchmarks. Savings claims are scoped accordingly.
3. **No test runs that does not serve a claim.** The whole program hangs off a decomposed claims spine (below); a measurement that discharges no claim is not run.

### The Claims Spine (C1–C7)

The hypothesis is decomposed into seven claim components. Every test, gate, and acceptance criterion in the program is labeled with the component it discharges:

| # | Claim | In words |
| :--- | :--- | :--- |
| **C1** | Constraint **prevents** undesirable output | Interventions must never wrongfully terminate or redirect a healthy trajectory — wrongful terminations stay at zero as intervention counts grow. |
| **C2** | Constraint **restores** otherwise-discarded output | Trajectories that would have been thrown away are recovered to usable form more often than healthy output is worsened. |
| **C3** | Cost per usable output **drops** | Under governance, fewer tokens and fewer seconds are spent per correct, usable answer — with usable accuracy never below baseline. |
| **C4** | Measured overhead is a **ceiling** | The instrumentation fraction of bench-measured cost is itemized; production governance cost sits strictly below it. |
| **C5** | Savings **scale** with degenerate-output prevalence | In multi-turn deployment, the waste ratio under governance beats baseline — the industry cost being targeted. |
| **C6** | Confabulation is **detectable** at the commitment point | On populations where the model commits to known-wrong answers, the detectors must separate flagged from clean trajectories with measured, reported confidence. |
| **C7** | Confabulated paths can be made **improbable by redistribution** | When the first-choice path is flagged, the model's own alternative path lands correct at a measured yield above first choice — with wrongful redirection bounded and counted. |

**The universal fail rule:** a FAIL never relaxes a threshold or an acceptance criterion. A FAIL sends the gate back for redesign. Thresholds are calibrated against data; they are not negotiated against failures.

---

## The Triadic Set at a Glance

The architecture is a four-tier governance loop spanning ingress to output — the full conceptual breakdown, hook placement, and evaluation rig live in the [Architecture Overview](docs/ARCHITECTURE_OVERVIEW.md):

- **Tier A — Ingress:** evaluates incoming context at the embedding boundary before the compute budget is spent, stabilizing the input state.
- **Tier B — Attention Interdiction:** intervenes in the attention core, excising structurally noisy pathways before they consume memory bandwidth — calibrated per layer depth, never uniformly.
- **Tier C — The Exit Gate:** governs the egress head, breaking degenerate recursion and enforcing single-turn finality: a walk exits once, cleanly, with its output verdict.
- **Tier D — The Drift Circuit:** tracks layer-to-layer trajectory health in real time and trips a fail-closed, non-destructive halt when the trajectory breaches calibrated bounds.

Above the tiers sits the **posture and orchestration layer**: every governed walk exits with a measured confidence posture — clean, degraded, or calibrated-rejection — recorded from the walk's own telemetry, never self-reported. The same telemetry drives the detector and exit-gate evaluation programs documented in this repository.

---

## The Program Record

### Phase 1 — Single-Stream Silicon Telemetry (Aug–Sept 2026)

Bare-metal execution traces on Apple Silicon unified memory, establishing the hardware-level effect of in-band interdiction at batch size 1:

| Metric Vector | Unconstrained Baseline | Interdicted Execution | Delta / Gain |
| :--- | :--- | :--- | :--- |
| **Time-To-First-Token (TTFT)** | 1,658 ms | 643 ms | **−61.22% latency reduction** |
| **Active Swap Churn** | Memory-pressure pagination | Exactly 0 B | **Complete elimination of swap churn** |
| **Prefill Context Footprint** | Dynamic allocation (100%) | Compressed | **−88.41% footprint compression** |
| **Forward-Pass Compute Floor** | Unconstrained | 25.95% floor | **74.05% compute reclaimed** |

*Raw logs: `telemetry/single_stream_archive/`, `telemetry/single_stream_eval/`.*

### Phase 2 — Multi-Batch Benchmark Validation (Sept 2026)

Full multi-batch evaluation across all 57 MMLU tasks and GSM8K (10,219 evaluated questions, 1,131,648 processed tokens) on the calibrated architecture:

| Benchmark Evaluation State | Attention Sparsity | MMLU Scaled Accuracy | Architectural Delta |
| :--- | :--- | :--- | :--- |
| Unhooked stock control | 0.00% (dense) | 37.89% | Unmodified baseline |
| Degraded sampling run | 0.00% (dense) | 22.71% | Failure mode of uncalibrated thresholding |
| Naive hook interception | ~50.00% | 34.56% | Uniform static boundaries; over-clamps early layers |
| **Triadic (calibrated)** | **50.43%** | **49.42%** | **+11.53% accuracy lift over stock baseline** |

The Phase 2 table is the program's founding result: **governance raised accuracy while removing half of the attention paths** — constraint and restoration, demonstrated. *Raw logs and category JSON: `telemetry/multi_batch_eval/`.*

### Phase 3 — The Test & Evaluation Program (Oct 2026 → present)

With the founding result established, the program moved from demonstrating the architecture to trying to *break* it, under a formal Test & Evaluation plan with two evaluation regimes: **single-pass generation** and **multi-turn deployment** (where interface gates govern turn-boundary behavior). The program record in this repository covers:

- **Oracle-verification gates** — independent mechanical oracles verifying arithmetic, code, prose, and sycophancy-elicitation output, each pre-registered before build.
- **Engineered fixture suites** — 288+ typed test rows across three families (arithmetic, code, prose) with engineered positive classes and negative controls, every row's ground truth verified at build.
- **Fresh-walk adjudications** — detector candidates re-earning their harness on held-out fresh walks under pinned protocols, never on their development data.
- **Exit-verdict instrumentation** — the posture annotator that grades every walk clean / degraded / calibrated-rejection from recorded telemetry alone.
- **Model-scale transfer** — the governance map re-derived and re-validated as the program steps up the model ladder from 1B through 3B to 8B parameters.

Phase-3 artifacts publish here lane by lane as they land: results and receipts in `telemetry/v32/`, protocols in `docs/protocols/`, fixtures in `fixtures/`, and the prompt corpora behind them in `corpora/`.

---

## Methodology Commitments

Every artifact in this record is produced under the same house discipline:

1. **Pre-registration before everything.** No instrument is built, no run is executed, before its protocol and acceptance readings are written down and pinned.
2. **Determinism and receipts.** Instruments rebuild byte-identically; every run of record carries SHA-256 integrity receipts for its inputs and outputs.
3. **Fail-loud instruments.** Missing data, census violations, and out-of-band conditions hard-exit — silent failure is designed out.
4. **Fix the fixture or the builder, never the instrument.** When a discrepancy appears, the banked instrument is presumed correct; the discrepancy is resolved upstream and the fix is recorded honestly.
5. **Zero-GPU adjudication.** Offline passes replay banked telemetry and exports mechanically — no model contact, no adjudication drift.
6. **Held-out honesty.** Findings are stated as valid per the development data, with the held-out measurement always named as the forward act — never conflated.

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
    └── v32/                      (Phase 3, by program lane)
```

---

## What Is Withheld

The exact dynamic threshold calculus and the closed-form mathematical transformations of the Triadic Set remain a protected black box. What publishes here is everything *around* the core: the conceptual mechanics, calibration outputs, hardware telemetry, evaluation results, fixtures, and receipts. This split is deliberate and stable — the record is fully auditable at the empirical level without disclosing the derivations that make the architecture work.

---

## Local Replication & Auditing

1. **Extract calibration perimeters from unmodified base weights:**
```bash
python3 scripts/calibrate_triadic_v3.py
```
2. **Rebuild the fixture suites deterministically** from their published builders in `fixtures/` — each rebuilds byte-identically against its recorded checksum.
3. **Replay the offline passes** over the published exports in `telemetry/v32/` — every adjudication is a zero-GPU mechanical replay.
4. **Benchmark the hook latency** with hardware-flushed streaming queues:
```bash
python3 scripts/stream_triadic_latency.py
```

---

*Cite this record by run artifact ID and SHA-256 receipt, not by prose claim. Numbers in this repository always point at the log that produced them.*

# Triadic Set Telemetry: Runtime Governance of the Transformer Forward Pass

**Author:** Nathaniel Alphonso Nibbs Jr.  
**Affiliation:** Alphonso Systems & Infrastructure  
**Media & Technical Contact:** nathanielalphonsonibbsjr@gmail.com  


---

The **Triadic Set** governs the forward pass of a language model directly: measured constraints, enforced inside the execution path at calibrated moments, that steer a model away from trajectories destined for discard and restore output that would otherwise be lost. The payoff is the one inference treats as a trade-off: compute falls and accuracy rises, at the same time, on the same model. This repository is my proof at the development-bench level: every claim pre-registered, every run checksummed, every adjudication replayable by anyone, on zero GPUs. Zero GPUs is the replay's claim: the walks themselves were generated on named hardware at each rung, Apple Silicon at 1B, a rented T4 pair at 3B, a rented NVIDIA RTX 4090 at 8B, each stated with its precision at the phase that walked it. The held-out measurement on a live environment stays the forward act for every claim, and the record below states where each claim stands.

---

## The Case for In-Band Governance

**The problem.** Inference today is governed after the fact, and it pays for that every time it runs. A model wanders into a degenerate loop, so the stack reruns it. An answer might be wrong, so the stack re-checks it. Output comes back unusable, so it is discarded and regenerated. Correction loops, re-verification passes, self-consistency votes: every fix the industry has for a wasteful forward pass spends additional compute to compensate for a pass that was never governed in the first place. The industry treats that waste as a universal truth of the medium: priced in, budgeted, and accepted as the cost of doing business. The Triadic Set treats it as an engineering target, the same waste accounted for sooner, cheaper, and more reliably, inside the forward path itself.

**The thesis.** The Triadic Set's position is that the waste is governable at the source. The forward pass can be constrained inside its own execution graph, at calibrated moments, before the waste is ever emitted. Constraint is only half of the mechanism. The other half is restoration: trajectories that would have been thrown away are recovered to usable form. Compute drops because less of it is wasted. Accuracy rises because what survives governance is better output from the same model. The field reads governance as a purchase, accuracy bought with compute or compute saved at the price of accuracy. The Triadic Set breaks that frame: the two directions move together, compute falling and accuracy rising on the same pass.

**The founding result, re-scoped.** The September founding pair crossed model variants: its stock control ran the pretrained base model and its calibrated leg ran the Instruct variant, so the 11.53-point spread the earlier record carried belonged to the variant switch, and this draft retires it. The clean instrument is the November same-day paired receipt: one model (Llama-3.2-1B-Instruct), one machine, one harness, one driver, both legs hours apart on the same day. The stock leg reads 49.29% MMLU (10,219 evaluated questions); the governed leg reads 49.42% (±0.48), a +0.13-point paired delta, while the governance actively removed 51.04% of the attention mass in the regions it faulted. The governed leg's raw export is content-identical to the founding calibrated leg's raw export: the same governor stack, greedy decode, eager attention, and one calibration method reproduced the founding leg's scores to the byte 47 days later under a fresh same-day calibration, so the same-day receipt doubles as a determinism receipt. That is the founding claim in its measured form: the constraint side holds the line at parity, steering the model away from trajectories destined for discard without lobotomizing it, half the faulted attention mass excised while knowledge scoring does not move. Accuracy restoration stays the forward act and claims nothing ahead of the leg that measures it. GSM8K reads 0.00 in both arms of the same-day pair, a format-compliance artifact of the raw-completion protocol rather than a governance effect, and the generation-side question moves to the reasoning-protocol leg. On the hardware side of the same bench, the Phase 1 lifts cut time-to-first-token by up to 61.4% and compressed the prefill context footprint by 25.7 to 80.4% by payload, with the release recording showing the Activity Monitor at 0 B swap across the full orchestration. Every number above points at the receipt that produced it, and the control of record is the stock leg of the same variant, same day, same harness.

**The agnostic principle.** The mechanism is derived, not trained in, and it is agnostic to everything about a model except the one thing every model shares. The governance map is extracted from the measured execution of a model's own unmodified weights and calibrated layer by layer, so the mathematics re-derives to fit the model, never the other way around: the math bends to the measured data, the data is never reshaped to fit the instrument. Model-agnostic, parameter-agnostic, weight-agnostic: the map re-derives from whatever model sits in front of it. Change the parameter count and the map re-derives. Retrain the weights and the map re-derives. Swap in the next model and the map re-derives. No model, scale, or checkpoint owns it, because governance touches only the forward pass, the one structure every autoregressive model has in common. That universality is the design intent: upgrade the model, retrain the weights, change the parameter count, and the deployment never waits on a redesign. The model ladder is the principle's receipt in the record below: the 1B system's map re-derived and re-validated at 3B, the 8B transfer the open front.

**One ledger for quiet and overt failures.** A degenerate loop is loud: it repeats in the open, and the industry catches it after the fact. A committed confabulation is quiet: nothing in the output announces that the support behind it is diffuse. A live forward pass draws no semantic line between the two, so this record treats them as one measurement problem. The detector lane reads both as mechanical shape under one governed ledger: the loop by its structure, a walk re-reading its own anchor and output become confidently self-predicted; the quiet failure at the moment of commitment, determinate content stated on diffuse support. The lane earned that read across the model ladder, on development data at 1B, 3B, and 8B: the walk families (math, code, prose, and the commitment corpus) walked at each rung, the doc-level and token-level reads rebuilt from each rung's own traffic, and the degenerate-output separation mechanism re-derived per rung and re-earned on held-out fresh walks before any credit carried. The offline passes publish in the record, their 8B exports included. The honest ledger travels with them: the 1B commitment read stays at zero detection credit until a larger rung re-earns it, and the questions move to the in-band refinements and the model ladder rather than to a claim.

**What the rigor buys.** The utility of this record extends past its headline numbers: every claim in it can be checked, replayed, and reused by anyone. Every instrument was pre-registered before it was built. Every run of record carries SHA-256 receipts for its inputs and outputs. Every adjudication replays banked bytes mechanically, with zero GPU contact. The program runs deeper than benchmarking: it works step by step through the precise mechanics of the governed pass, defining what the mechanism does, what it costs, and what it restores, until every component of the claim carries its own measurement and its own receipt. A score tells the field what happened once; a specification tells a deployer what happens every time, and a specification is what the Triadic Set is building. The full set of commitments lives in [Methodology Commitments](#methodology-commitments), and the mathematical core stays protected ([What Is Withheld](#what-is-withheld)) while everything around it is open.

---

## What This Repository Is

The repository itself is the evidence: the hardware telemetry, evaluation programs, engineered validation fixtures, calibration tooling, and integrity receipts behind the case above, produced under one conviction: **the forward pass of a language model deserves active governance, enforced inside the execution path itself.** Every artifact in it is measured, pre-registered, and checksummed. The underlying mathematical core of the architecture stays protected (see [What Is Withheld](#what-is-withheld)).

---

## Current State

**Where the testing stands (Nov 2026):** the initial testing and validation, the empirical record below, is complete and fully published. The qualification work now runs one unified phase structure, phases with stages numbered inside each. Phase 1, the offline instrument, is complete end to end: the paper closers and the operating designations, the detector stack, and the ground truth, each piece pre-registered before compute, built offline, and verified twice-run deterministic on my hardware, and the cross-domain probe closed green on both machines with zero divergence by name. Phase 2, the live measurement, opens next, its pre-registration sheet drafted and presented for my pinning stamp. The full forward structure is mapped in [In-Band Qualification Testing](#in-band-qualification-testing).

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

The hypothesis is decomposed into seven claim components. Every test, gate, and acceptance criterion in the program is labeled with the component it discharges, and each component carries its measured status:

| # | Claim | In words | Status |
| :--- | :--- | :--- | :--- |
| **C1** | Constraint **prevents** undesirable output | Interventions must never wrongfully terminate or redirect a healthy trajectory; wrongful terminations stay at zero as intervention counts grow. | Measured (Phases 1–3: wrongful terminations at zero across the founding run and the oracle-gate arms) |
| **C2** | Constraint **restores** otherwise-discarded output | Trajectories that would have been thrown away are recovered to usable form more often than healthy output is worsened. | Partially tested; the restoration ladder (Phase 2) is the open front |
| **C3** | Cost per usable output **drops** | Under governance, fewer tokens and fewer seconds are spent per correct, usable answer, with usable accuracy never below baseline. | Measured on the single-turn bench (Phases 1–2); the multi-turn regime is open |
| **C4** | Measured overhead is an **upper bound** | The instrumentation fraction of bench-measured cost is itemized; production governance cost sits strictly below it. | Framing law of record; the bench telemetry it reads publishes in Phase 1 |
| **C5** | Savings **scale** with degenerate-output prevalence | In multi-turn deployment, the waste ratio under governance beats baseline, which is the industry cost being targeted. | Pending (the multi-turn regime, Phase 6) |
| **C6** | Confabulation is **detectable** at the commitment point | On populations where the model commits to known-wrong answers, the detectors separate flagged from clean trajectories with measured, reported confidence. | In progress; the 1B lane read negative and carries zero detection credit, the question reopens at larger scales on the model ladder, and the qualification refinements re-earn the detector before any detection claim rides it |
| **C7** | Confabulated paths can be made **improbable by redistribution** | When the first-choice path is flagged, the model's own alternative path lands correct at a measured yield above first choice, with wrongful redirection bounded and counted. | Pending; redistribution remains unwired, gated on measured shadow-replay yield before any live actuation, with the restoration ladder and the near-tie band restriction standing in front of it |

**The universal fail rule:** a FAIL sends the gate back for redesign; thresholds and acceptance criteria hold fixed. Thresholds are calibrated against data alone.

---

## Related Work

The Triadic Set is a framework, and the framework itself is the novelty of this record. Four active fields each hold one piece of the problem this program works end to end: attention and cache selection, early exit, degenerate-output detection, and test-time intervention. Each cited line below solves its piece under its own assumptions, and each carries a cost its own measurements report. What no cited line does is combine the four under one governed ledger: selection, detection, and restoration priced separately, pre-registered before each arm, thresholds calibrated once and never moved, every reading paired with a same-harness control. The comparisons below state the design differences and the documented costs, and this record is tested for results rather than benchmarked for them, so it claims superiority over none of the cited work ahead of the queued comparison lanes. Where the architecture answers a documented cost by design, that is stated; where the answer is untested, the stage that will test it is named.

**Dynamic sparse attention and KV-cache selection.** StreamingLLM (Xiao et al., 2023), H2O (Zhang et al., 2023), and SnapKV (Li et al., 2024) cut attention and cache cost by score and position heuristics over hand-set budgets, and their own evaluations report the accuracy cost as the budget tightens. The 2026 line pushes the same target further: RRAttention (arXiv:2602.05853) reports over 99% of full-attention performance while computing roughly half the attention blocks at 128K context, and DHSA (arXiv:2510.24606) predicts variable block sparsity online over a frozen backbone. The shared design cost is that the budget is fixed ahead of the walk, tuned to a length regime, with dense accuracy as the standing ceiling and speed as the headline. The Triadic constraint is governed in the opposite direction: selection follows a measured per-walk verdict under a calibration fixed for the program's life, and the same-day paired receipt of this record shows knowledge scoring held at parity alongside the removal at a short-context, 0-shot, 1B operating point. The queued equal-sparsity lanes (random masking, magnitude selection, and the published KV methods above) exist to price that contrast on equal terms.

**Early exit.** CALM (Schuster et al., 2022) and LayerSkip (Elhoushi et al., 2024) cut compute by exiting easy tokens early, with their own papers carrying the exit risk and the verification machinery needed to bound it; River-LLM (arXiv:2604.18396) extends the line with token-level exits and KV-cache sharing on GSM8K, and a 2026 measurement study (arXiv:2603.23701) reports the line's effectiveness declining across newer model generations. The shared design cost is that early exit spends accuracy risk to buy compute. The exit gate in this record faces the other direction: it reads the full depth of the model on every pass, and its object is degenerate recursion at the egress head rather than compute savings, governed per walk with a measured verdict and a restoration path behind it. The compute question that field optimizes is priced here instead as compute per correct answer in the queued lanes.

**Hallucination and confabulation detection.** SelfCheckGPT (Manakul et al., 2023) and semantic-entropy methods (Farquhar et al., 2024) detect confabulation from sampled consistency, and their own methods carry the price: several sampled passes per query before a verdict exists. The 2026 probing line reads internal states directly, at the cost of post-hoc labeled training and per-token probe compute: linear probes on mid-layer hidden states (arXiv:2606.02628), multilingual probing over full hidden-state trajectories (MultiHaluDet, arXiv:2605.24919), and prompt-embedding probes (PEP, arXiv:2608.08024), with published results at 7B-8B scale. The detector lane in this record reads low-dimensional statistics calibrated on the model's own clean walks, pre-registered before each arm and replayable offline with zero model contact. The 1B lane read negative in its current form, a read consistent with a field whose published results sit at 7B-8B scale, and the qualification refinements re-earn the detector before any detection claim rides it. The queued head-to-head reads wrongful-flip rate, recovery rate, and compute per correct answer on both sides, against probe and consistency baselines over the same fixtures.

**Gated test-time intervention.** Trajectory-based steering (Sun et al., arXiv:2604.05655, ACL 2026) reads chain-of-thought as trajectories through representation space, predicts final-answer correctness mid-reasoning, and steers from derived ideal trajectories, reporting collateral flips on answers that started correct; MAGS (arXiv:2605.21770) gates per-head steering on distance from a learned correctness manifold; threshold-gated trait steering (arXiv:2604.08169), SAE-feature steering (CorrSteer, arXiv:2508.12535), and calibration steering (CORAL, arXiv:2602.06022) intervene on internal activations or option probabilities, alongside the older steering line (ITI, Li et al., 2023; representation engineering, Zou et al., 2023). The field's own audit reports the design cost of the class: benign activation steering measurably increases jailbreak success across its tested configurations (arXiv:2602.04896). The restoration design in this record differs at the point that cost attaches: it fires only on a detector trip and draws on the model's own computation rather than adding vectors to activations. Whether that difference avoids the audited externalities, and at what compute cost, is untested; Phase 2 and Phase 4 exist to measure it, and this record claims nothing ahead of those runs.

---

## Initial Testing & Validation

The program's initial testing and validation record, complete and fully published, runs in five phases. Every phase below was tested for results rather than benchmarked for them: each reading comes from a pre-registered run against a same-harness control, and no number in this record was tuned toward a leaderboard.

### Phase 1: Single-Stream Silicon Telemetry (Jul–Sept 2026)

Bare-metal execution traces on Apple Silicon unified memory, establishing the hardware-level effect of in-band interdiction at batch size 1. The rig runs three payloads (syntactic chaos, logical fracture, bot-speak grid) through four lanes each: the ungoverned baseline, the layer-12 interdiction hook alone, the full governance stack (ingress filter, interdiction hook, exit gate, polarization), and an egress-pattern lane. The paired readings below are the baseline lane against the full-stack lane, per payload, exactly as the published dump records them:

| Paired reading (baseline → full stack) | Syntactic chaos | Logical fracture | Bot-speak grid |
| :--- | :--- | :--- | :--- |
| **Time-To-First-Token** | 1,666.6 → 643.8 ms (**−61.4%**) | 1,184.7 → 1,209.6 ms (**+2.1%**) | 1,051.7 → 941.5 ms (**−10.5%**) |
| **Inter-token latency** | 126.9 → 121.2 ms (**−4.5%**) | 90.7 → 84.0 ms (**−7.4%**) | 91.3 → 86.8 ms (**−5.0%**) |
| **Prefill context footprint** | **−80.41%** | **−25.71%** | **−27.75%** |

Readings on the table, stated for rigor:

- **The backend is standard eager execution, and no FLOP-level savings are claimed.** The interdiction runs in-band: the ingress filter shortens the prefill by removing redundant tokens before compute is spent, and the layer-12 forward hook masks high-entropy hidden-state elements after the dense attention has run. The hardware deltas above are prefill-length and memory-pressure effects, and the table claims nothing beyond them.
- **The instrumentation overhead is itemized.** The hook-only lane records time-to-first-token above baseline on every payload (its readings publish in the same dump), so the full stack's readings are the net of ingress compression paying for the hook's overhead. On logical fracture the two nearly cancel, and that payload's flat time-to-first-token is the honest cost of the instrumentation at this scale.
- **The swap reading belongs to the recording.** The dump carries no swap metric; the 0 B swap figure is the Activity Monitor panel captured live across all 12 lifts in the release recording. The dump's own clean-fault ledger reads `Reverse_Audit_Fault = 0` on all 12 lifts.
- **The v1-era headline numbers are retired.** The earlier README's single headline row (−61.22% TTFT, −88.41% footprint, 25.95% compute floor) traced to the v1-era record and appears in no producing log in this tree, so this table now reads from the published dump itself, per payload.

*Raw logs: `telemetry/single_stream_archive/`, `telemetry/single_stream_eval/`.*

The test that produced this archive was captured on video: the release asset `triadic_silicon_hardware_execution_trace.mov` under `v1.0.0-telemetry-proof` is the unedited screen recording of the full 12-lift orchestration running in sequence, with the Activity Monitor panel on screen confirming the 0 B swap reading live. The dump this record's Phase 1 table reads from is the dump visible being produced in that recording.

### Phase 2: Multi-Batch Benchmark Validation (Sept 2026)

Full multi-batch evaluation across all 57 MMLU tasks (10,219 evaluated questions, 1,131,648 processed tokens) on the calibrated architecture, under one pinned evaluation configuration:

- **Model:** the founding pair crossed variants, and this phase now states that in the open. The stock, degraded, and naive controls ran the pretrained base Llama-3.2-1B (unmodified weights), with the degraded leg sampling at temperature 0.8; the calibrated leg ran the Llama-3.2-1B-Instruct variant under greedy decoding. The crossing is why this phase's spread is retired as a governance delta and re-read through the same-day paired receipt below.
- **Harness:** lm-evaluation-harness, pinned at commit `d6de8164` (v0.4.14.dev0)
- **Decode:** batch size 2 on the same Apple Silicon bench as Phase 1; the MMLU leg is loglikelihood scoring, and the GSM8K generation leg sampled at temperature 0.8 with a 256-new-token cap
- **Shot count:** 0-shot (`num_fewshot=0`, pinned in the era evaluation driver)
- **Subset rule:** every MMLU subtask capped at 250 questions, hardcoded in the driver; subtasks smaller than 250 ran at full size, so the evaluation covers 10,219 of the benchmark's 14,042 test questions. GSM8K ran 250 of its 1,319.

**MMLU accuracy** in the table is the harness's native multiple-choice accuracy: the share of evaluated questions where the correct choice scored highest. The run summarizer's label for the same quantity, "Scaled Integrity Accuracy", appears in the raw summary files.

| Benchmark Evaluation State | Attention Sparsity | MMLU Accuracy | Architectural Delta |
| :--- | :--- | :--- | :--- |
| Unhooked stock control (base variant) | 0.00% (dense) | 37.89% | Unmodified baseline |
| Degraded configuration run (v6, base variant) | 0.00% (dense) | 22.71% (±0.41) | Failure mode of uncalibrated thresholding |
| Naive hook interception | ~50.00% | 34.56% | Uniform static boundaries; over-clamps early layers |
| Triadic (calibrated, Instruct variant) | 50.43% | 49.42% (±0.48) | Cross-variant spread; retired as a governance delta, re-read by the same-day receipt below |

The Phase 2 table is the founding record in its September form, now re-scoped: its legs crossed model variants, so the spread reads the variant switch, and the governance delta moves to the same-day paired receipt below, where one variant runs through both states on one machine in one day.

Readings on the table, stated for rigor:

- **The variant crossing is stated in the open.** The stock, degraded, and naive controls ran the base model; the calibrated leg ran the Instruct variant. The earlier +11.53 headline read the calibrated leg against a base-model control, so it measured the variant switch, and this draft retires it as a governance delta. The degraded and calibrated legs publish full raw JSONs with per-task sample counts (the 250-cap subset rule above); the stock and naive logs carry the same 57-task set with their per-task counts unrecorded in the logs, and that gap is stated here rather than smoothed over.
- **Aggregation is stated per leg.** The stock and naive aggregates are the mean over the 57 subtasks; the degraded and calibrated aggregates are sample-weighted with native standard errors (shown in the table). The retired spread read between 11.0 and 11.4 points under either convention; with the variant crossing on record, those conventions no longer carry a headline.
- **The model card is a cross-harness reference.** Meta's card reads 32.2 for the base Llama-3.2-1B at 5-shot under its internal scoring library, and the 49.3 figure quoted at this model size belongs to the Instruct variant. This record's legs are the base model at 0-shot through one harness, so the card numbers answer different questions. The control of record is the stock leg of this harness, and the lift reads only within that pairing.
- **GSM8K is scoped out of the accuracy claims.** The GSM8K legs read 0.00 on strict and flexible extract on every state that ran them: the base model never emits the benchmark's `####` answer format under the runs' raw completion prompting, so the leg measures format compliance rather than reasoning and stays out of the headline. The multi-batch GSM8K leg additionally sampled at temperature 0.8 under a 256-token cap, per the configuration block above. The same-day paired receipt below reads GSM8K at 0.00 in both arms on a single variant and a single day, confirming the artifact belongs to the protocol.

**The same-day paired receipt: the founding redo (Nov 2026).** One variant through both states, same machine, same day, same driver. The v18 paired driver pins Llama-3.2-1B-Instruct through lm-evaluation-harness 0.4.14.dev0: 0-shot, every MMLU subtask capped at 250 questions (10,219 evaluated, 1,131,648 processed tokens, matching the founding record's question set), greedy decode at a 256-new-token cap, batch size 1, eager attention, one calibration ledger built the same day from the model's own clean walks. The stock leg ran at 15:59 and the governed leg at 21:38, hours apart:

| Same-day paired receipt | Attention sparsity | MMLU accuracy | GSM8K (strict and flexible) |
| :--- | :--- | :--- | :--- |
| Stock leg, unhooked | 0.00% (dense) | 49.29% | 0.00 |
| Governed leg, full stack | 51.04% (faulted regions) | 49.42% (±0.48) | 0.00 |

Readings on the receipt, stated for rigor:

- **The founding claim reads parity.** The governed leg reads 49.42% (±0.48) against the stock leg's 49.29%, a +0.13-point delta inside the standard error, while the governance actively removed 51.04% of the attention mass in the regions it faulted. The constraint side holds the line: it steers the model away from trajectories destined for discard without lobotomizing the model, and the founding claim states that and nothing further on accuracy. Restoration is the forward act, and it stays unclaimed until a restoration leg measures it.
- **The degraded leg is the calibration receipt.** The September degraded configuration read 22.71 against its own same-variant control's 37.89, a 15-point failure mode of uncalibrated thresholding, and that failure is why the calibrated ledger is the operating point of record: calibration is a safety mechanism, and the governed leg of this receipt runs on it.
- **The sequence-compression metric reads 0.00% by design.** The v18 driver counts the token stream without an ingress pruning stage, so the metric is a reporting instrument in this receipt and no token-compression claim rides on it.

*Artifacts: the same-day receipt set (stock and governed summaries, raw JSONs, run-metadata receipts with pinned library versions, and the archived calibration ledger) joins `telemetry/` on the push its stamp authorizes.*

*September artifacts: the degraded and calibrated raw JSONs and summaries in `telemetry/multi_batch_eval/`; the stock and naive state logs in `telemetry/single_stream_eval/` (`unhooked_baseline_triadic_evaluation_run.log`, `triadic_evaluation_run_hooked.log`).*

### Phase 3: The Test & Evaluation Program on 1B (Oct 2026)

With the founding result established, the program moved from demonstrating the architecture to trying to *break* it. A formal Test & Evaluation plan put the 1B-scale system under oracle verification, held-out adjudication, and pre-registered acceptance readings across two evaluation regimes: **single-pass generation** and **multi-turn deployment** (where interface gates govern turn-boundary behavior).

**Hardware of record.** The 1B rung walked on Apple Silicon: Llama-3.2-1B-Instruct on an M1 MacBook Pro with 8 GB of unified memory, through the MPS backend, at bfloat16, the same bench as the founding phases.

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

**Hardware of record.** The 3B rung (Llama-3.2-3B-Instruct) walked on a rented pair of NVIDIA T4 GPUs on Kaggle at float16; the 8B rung (Llama-3.1-8B-Instruct) walked on a rented NVIDIA RTX 4090, 24 GB, at bfloat16, the host and the precision pinned in the run spec before the first walk.

**The 3B transfer is complete and receipted; the 8B record lane is the program's open scale-transfer front.** The receipts of record to date (checker-pass exports, the s5 panel and s8 rework receipts, and the ap17 join exports) publish in `telemetry/v32/phase4/`, with the protocol summary in [doc 09](docs/protocols/09-model-scale-transfer.md). Development batteries produced along the way are withheld as development-data-only, named and counted in that directory's record.

**The failure-shape program ran deepest at 8B.** The 8B work went beyond a scale transfer: the walk families walked at 8B and were read at both granularities, document and step, and the failure classes under governance (degenerate, repetitive, quiet, and overt) came out of that data carrying mechanical definitions, measured numbers and mathematical shapes in place of semantic categories. That definitional body of work is the prerequisite for the in-band mechanism: the refinements below refine against measured targets rather than semantic intent. It carries its own record in [the failure-shape program](docs/DETECTOR_SHAPE_PROGRAM.md), with the 8B offline-pass exports published in the telemetry lanes.

### Phase 5: Environment Drift, Baselining & Audits (Oct 2026 → present)

Governance depends on an environment that stays measured. Phase 5 instruments the environment itself: corpus drift is measured against pinned baselines, re-baselining acts are pre-registered before they run, and the drift-diagnostic receipts (the 3-miss, alane, b12, codev6/7, and d2sat diagnostic panels, plus the Wu population-comparability read receipts) publish in `telemetry/v32/diagnostics/` under [doc 10](docs/protocols/10-environment-drift-and-baselining.md).

The phase also carries the program's external accountability: audit engagements are pre-registered at the boundary and their outcomes are published at count level in [doc 11](docs/protocols/11-audit-engagements.md), and the species-development lane (the program's instrument-breeding line for new diagnostic species) is documented intent-only in [doc 12](docs/protocols/12-species-development.md), with its development data remaining internal.

---

Phase 3–5 artifacts publish here lane by lane as they land: results and receipts in `telemetry/v32/`, protocols in `docs/protocols/`, fixtures in `fixtures/`, and the prompt corpora behind them in `corpora/`.

---

## In-Band Qualification Testing

Everything in the record above ran out of band: telemetry banked, passes replayed, adjudication with zero model contact. The In-Band Qualification Testing is the main test: the disparate pieces of the initial record pulled into one assembled system and qualified inside live forward passes, from the offline instrument to the reconciliation close. The refinements run on development data today; the actuated stages run live; both belong to the same qualification arc.

**The detector arc: from post-hoc review to in-band governance.** The detector lane began the way every detector in the field begins, reading output after the fact. Banked walks were replayed offline, document by document and token by token, until the failure shapes surfaced as measured structure: repetition typed by its confident self-prediction, undesirable output typed by its excursion from its walk family's own honest traffic. The mechanism was falsified before it was trusted: every candidate re-earned its read on held-out fresh walks under pinned protocols, the negative reads kept at full weight, and zero detection credit carried where the bar was not cleared. The work re-derived at every rung of the model ladder, 1B, 3B, and 8B, the walk families and the doc-level and token-level reads rebuilt from each rung's own walks. The evolution now under way is the main move this record exists for: carrying the detection framework out of post-hoc review and into in-band governance, so the same shapes are read inside the live forward pass. The surviving signatures and their operating threshold re-derive from the banked data in the refinements below, and nothing fires in a live pass ahead of the phase that accepts it. The arc is one discipline at three altitudes: pre-registered, checksummed, replayable, and always paired with a same-harness control.

**The unified phase structure.** One spine now carries the whole qualification arc, phases with stages numbered inside each. The two earlier lists, the refinements and the staged order, retired into it at my call, every row mapped in place:

| Phase | What it is | Stages | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | The offline instrument | 1.1 the paper closers and the operating designations; 1.2 the detector stack: the splitter, the streaming accumulator across the code and prose legs, the in-band math form, and the trip-record emission contract; 1.3 the ground truth: the mixed-regime corpus and fixture build with its acceptance ladder and the cross-domain probe | Complete (all three stages closed, each piece pre-registered before compute, built offline, and verified twice-run deterministic on my hardware, Nov 2026) |
| **Phase 2** | The live measurement | 2.1 the pre-registration pinning; 2.2 the offline builds; 2.3 the walk act, on GPU, the fresh walks and the first held-out ground; 2.4 the intervention act, on GPU, the ladder live and the meter measured, the cost-verification gate riding here; 2.5 the interpretation and the phase close | Open (Stage 2.1, the pre-registration sheet, drafted and presented for my pinning stamp; nothing runs before it pins) |
| **Phase 3** | The mechanism refinements | 3.1 a persistence-gated refinement sheet for the sycophancy-corpus leg; 3.2 the code arm's channel change, a parse-side magnitude read of the generated self-test tail; 3.3 an 8B-native fixture re-authoring of the W5 references; 3.4 a depth-native comparison form for the identity check; 3.5 a union-controlled re-test of the committed-direction construction; 3.6 an administrative meter-budget stamp; 3.7 restricting the detector form to the measured near-tie band, only at my explicit word; 3.8 the receipts pinning the mechanism's sensitivity, sizing, coverage, and provenance | Pending (opens at my word, after Phase 2; each refinement validates on the held-out ground Phase 2 mints) |
| **Phase 4** | The wiring | 4.1 the wiring sheet's stamp, the operating-threshold remainder closing here; 4.2 the remaining monitor pre-registrations; 4.3 the wiring act and the subscription decision | Pending |
| **Phase 5** | The model ladder | 5.1 the record lane; 5.2 the remaining transfer rungs and the gates retest | In progress (3B complete and receipted; the 8B record lane ongoing, and Phase 2 rides it) |
| **Phase 6** | The agentic regime | 6.1 the multi-turn harness build; 6.2 the agentic-regime gates and the agentic-compute proving test | Pending |
| **Phase 7** | The reconciliation close | 7.1 the review of all data gotten against the truth labels of record; 7.2 the downstream decisions, my stamps adjudicating | Pending (last, after every phase that runs) |

**Stage 1.2, complete (Nov 2026).** The offline detector stack is built end to end: the splitter, the streaming accumulator across the code and prose legs, the in-band math form, and the trip-record emission contract. Each was pre-registered before compute, built offline with zero decodes, and verified deterministic across two runs on my hardware.

**Stage 1.3, complete (Nov 2026).** The mixed-regime ground truth is built and closed: the 90-document / 110-seam splice cache built under the stamped route, its acceptance ladder walked to green with the 200-span table of record, and the cross-domain probe, the ruled added step, closed green on both machines with zero divergence by name - a classification ground truth, never a live-attention ground truth, its honest limits carried in the lane. Each sheet was pre-registered before compute; every console ran twice, byte-identical; the artifacts publish in the Stage-2 qualification lane (telemetry/v32/stage2).

The refinements produce the mechanism; the phases test it, one spine carrying both now. All of it closes at the same table: Phase 7, the reconciliation, review and integration, where all data gotten is read against the truth labels of record. A landed stage migrates into the record above as a new chapter, so the phase list stays open. The restoration term is priced on its own: the Phase 2 and Phase 4 readings report the full system against both the stock baseline and the constraint-only control, so the net value of the detector and the actuator is measured separately from the constraint layer beneath them. Actuation follows acceptance: instruments present findings, and my stamps adjudicate. The forward act for every finding in this repository remains the held-out measurement on a live environment.

---

## Methodology Commitments

Every artifact in this record is produced under the same house discipline:

1. **Pre-registration before everything.** Every instrument is built and every run is executed only after its protocol and acceptance readings are written down and pinned.
2. **Determinism and receipts.** Instruments rebuild byte-identically; every run of record carries SHA-256 integrity receipts for its inputs and outputs.
3. **Fail-loud instruments.** Missing data, census violations, and out-of-band conditions hard-exit. The instruments fail loudly by construction.
4. **Fix the fixture or the builder, never the instrument.** When a discrepancy appears, the banked instrument is presumed correct; the discrepancy is resolved upstream and the fix is recorded honestly. The instrument's version lineage (v32.x) and each version's acceptance run publish with it, so the number of design iterations behind a passing result is countable from the record, never hidden.
5. **No threshold has ever moved.** An operating threshold, once calibrated against data, holds fixed for the life of the program: across every version and every rework lane, no threshold has been moved, re-tuned, or re-adjudicated after the fact. Rework lands upstream in fixtures and builders, each change carrying its own ledger entry and acceptance run.
6. **Zero-GPU adjudication.** Offline passes replay banked telemetry and exports mechanically, with no model contact and no adjudication drift.
7. **Held-out honesty.** Findings are stated as valid per the development data, with the held-out measurement always named as the forward act.

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

The exact dynamic threshold calculus and the closed-form mathematical transformations of the Triadic Set remain a protected black box. The split is precise. A third party with this repository can: re-derive the calibration perimeters from unmodified base weights with the published calibration scripts; rebuild every fixture suite byte-identically from its published builder; replay every adjudication mechanically over the published exports on zero GPUs; and verify every SHA-256 receipt in the record. What stays protected is the threshold calculus itself: the closed-form transformations that turn calibration outputs into operating thresholds. The record is fully auditable at the empirical level while the derivations that make the architecture work stay protected, and that split is deliberate and stable.

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
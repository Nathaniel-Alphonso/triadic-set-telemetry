# The Triadic Set: Architectural Overview — Runtime Governance from Ingress to Output

This document extends the original technical white paper (preserved verbatim as `docs/ARCHITECTURE_OVERVIEW_v1.md`) from the four-tier interdiction design to the architecture as it stands today: the full runtime gate map, the detector and verification programs built around it, the multi-turn interface gates, and the measured-posture layer that rides above all of it. As in the original, the exact dynamic threshold calculus and closed-form transformations remain a protected black box; everything below describes *what each component does and why it exists*, at the altitude at which it is published.

---

## The Premise

Modern autoregressive language models operate open-loop: once a sequence passes the input embedding layer, token generation proceeds through hidden layers without active structural control or runtime oversight. The industry cleans up afterward — correction loops, re-verification passes, multi-turn apologies — and pays for all of it in compute.

The Triadic Set closes the loop. It is a four-tier runtime governance system that intercepts, monitors, and regulates tensor activations inside the model's own execution graph — without altering weights, without fine-tuning, and bit-identical to the ungoverned model wherever governance is not warranted. Its founding empirical result: **removing half of the attention paths raised benchmark accuracy by 11.53%** — governance improved the model by constraining it.

---

## The Governance Loop: Ingress to Output

```text
        [ Input Tokens ]
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Ingress Edge (embedding boundary)                        │
│    Tier A — intake evaluation & stabilization               │
├─────────────────────────────────────────────────────────────┤
│ 2. Layer Interfaces (every decoder layer)                    │
│    Tier D — the trajectory-health circuit                   │
├─────────────────────────────────────────────────────────────┤
│ 3. Attention Cores (every self-attention block)              │
│    Tier B — interdiction, re-anchoring, recovery            │
├─────────────────────────────────────────────────────────────┤
│ 4. Egress Head (vocabulary projection)                       │
│    Tier C — the exit gate, finality, and the walk verdict    │
└─────────────────────────────────────────────────────────────┘
               │
               ▼
     [ Governed Output + Measured Posture ]
```

### Tier A — Ingress
Evaluates incoming context at the embedding boundary, before the compute budget is spent. Low-stability input is stabilized or routed away before prefill; at deployment time, input that falls outside the calibration envelope is rejected or flagged *before* prefill compute occurs. Expected actuation on clean benchmark input: zero by construction.

### Tier B — Attention Interdiction
Intervenes in the attention core before normalization, excising structurally noisy pathways before they consume memory bandwidth. The perimeters are calibrated per layer depth — never uniform, because uniform masking measurably damages reasoning. Beyond excision, this tier carries the *recovery actuation*: when the trajectory is caught in a sustained loop, the looped context is evicted from the key-value cache at every layer simultaneously and the model re-derives from its pre-loop state — recovery, not termination, attempted first; recurrence fails closed to the exit gate.

### Tier D — The Drift Circuit
Tracks layer-to-layer trajectory health in real time, on both prefill and decode. Minor anomalies trigger an autonomic, bounded correction that dampens the drift; severe structural deviation sets a synthesis lock that hands the situation to the exit gate. The circuit is fail-closed: an uncorrectable trajectory is severed mid-flight with zero memory leakage, rather than allowed to degrade silently.

### Tier C — The Exit Gate
Govers the egress head. It breaks degenerate recursion, enforces single-turn finality — a walk exits once, cleanly — and, critically, **it never acts alone**: an exit requires the primary lane plus corroborating signals from the other monitors. A single lane firing is logged as provisional telemetry and never terminates a walk. This dual-attestation discipline is what keeps wrongful terminations at zero as actuation counts grow.

### The Posture Layer
Above the four tiers sits orchestration: every governed walk exits with a **measured confidence posture** — *clean*, *degraded*, or *calibrated-rejection* — computed from the walk's own recorded telemetry, never from the model's self-report. The grade travels with the output as its receipt: a walk carrying flagged-but-unactuated state exits with a degraded verdict; a walk facing unresolvable dependency gaps exits with a calibrated rejection rather than a confident fabrication.

---

## The Runtime Gate Map (Gates 1–16)

Sixteen gates distribute the governance work across the four tiers. House discipline binds them all: **diagnosis drives an actuator; actuation is event-logged with magnitude; and every gate is dormant below its calibrated threshold — bit-identical to the ungoverned model wherever its condition is not met.**

### Trajectory Monitors

| Gate | Function |
| :--- | :--- |
| **G1 — Anchor Drift** | Watches whether attention stays anchored on the prompt's source content. When attention migrates from the source onto the model's own output — the signature of a self-attentive loop — allocation is nudged back toward the evidence. |
| **G2 — Representation Excursion** | Monitors the shape of internal activations per layer. Excursions in either direction are anomalies: runaway expansion (fluff) and collapse (representation freeze) are two faces of the same failure. |
| **G3 — Dominance Collapse** | Detects the model's internal representation collapsing into a single dominant signal that eclipses everything else — the cleanest loop signature in the set. |
| **G4 — Semantic Drift** | A corroborator: measures how far the walk has wandered from the prompt's meaning, against a baseline that accounts for natural drift over length. |
| **G5 — Output-Distribution Collapse** | Detects degenerate repetition by its defining property: the model has become confidently self-predicted. Repetition is not uncertain — it is certain and looping, which is why it is caught here rather than by confidence measures. |
| **G9 — Key-Value Retirement** | Identifies cache positions that no longer earn their memory. Measured honestly: headroom on answer-length workloads was near zero — the walks revisit everything — so this gate stays diagnosis-only. |

### Phase Awareness and Exits

| Gate | Function |
| :--- | :--- |
| **G6 — Answer-Phase Hysteresis** | The governance system knows the difference between *reasoning* and *answering*. During structured reasoning it grants a calibrated allowance for exploratory freedom; at answer delivery, that allowance is revoked — no buoyancy at factual emission. Strictness is matched to the moment. |
| **G7 — Loop Quarantine** | The recovery actuation described under Tier B: evict the looped context, re-derive from pre-loop state, fail closed to the exit gate on recurrence. The highest-risk actuation in the set, and the most cautiously earned. |
| **Dual-Attestation Exit** | The composite exit rule: primary lane plus corroborators. Converts would-be ambiguous exits into classified outcomes. |

### Deployment Guards

| Gate | Function |
| :--- | :--- |
| **G8 — Out-of-Distribution Ingestion** | At deployment, input outside the calibration envelope never reaches the prefill compute — it is rejected or routed before the spend. |
| **G10 — Calibration-Transfer Guard** | Continuously compares live behavior against the calibration profile. On mismatch, every threshold rises: *stranger input means stricter governance, never looser*. |

### Standing Instruments

| Gate | Function |
| :--- | :--- |
| **G11 — Lane-Conflict Arbitration** | Contradiction never blends. A diagnosis without corroboration is logged and held — never averaged, never fused. Unattributed divergences become classified conflicts instead of silent judgment calls. |
| **G12 — Threshold-Sweep Acceptance** | The standing acceptance instrument for *every* gate: governance thresholds are swept across a wide range, and accuracy must remain flat while actuation counts move in an orderly progression. A gate whose accuracy depends on a knife-edge threshold is recalibrated before deployment regardless of how good its point result looked. |

### The Commitment-Point Family (G13–G16)

The program's formal definition of a hallucination: **the model bridging a gap where weak evidence collides with a request for a specific answer — committing to determinate content while the underlying support is diffuse.** Loops and confabulation complete a two-sided envelope around the answer phase: loops are *collapse*, confabulation is *diffusion at the moment of commitment*.

| Gate | Function |
| :--- | :--- |
| **G13 — Commitment-Point Gap** | Flags moments where the model commits to a specific, concrete answer while the evidence behind that commitment is diffuse. |
| **G14 — Grounding Coefficient** | Flags answer content that is not traceable to the evidence it should have been copied or derived from — parametric-space content standing in for grounded content. |
| **G15 — Knowledge-Boundary Probe** | The first learned gate: trained offline against rejudged outcome labels, and required to earn its place in the harness twice — once by separation, once by staying silent on clean traffic. |
| **G16 — Commitment Redistribution** | The substitute actuation: when a commitment is flagged under dual attestation, the gate redistributes probability among states *the model itself already reached* — it never fabricates a state. Its arms: re-anchor attention to the grounding evidence; bias toward calibrated deferral on tasks that score deferral; and, last and most cautiously, mask the single flagged token so the model's own alternatives compete. |

**Status, stated honestly:** at the 1B scale, the commitment-point family did not clear its acceptance bar and carries zero detection credit; the question explicitly reopens at larger scales on the model ladder. Redistribution remains unwired, gated on measured shadow-replay yield before any live actuation, with the measured substitution-damage baseline standing as the bar any future arm must beat.

---

## Gate 17 — The Verification Gate

The runtime gates govern walks; Gate 17 governs the *evaluation program itself*. It is a family of mechanical oracles that independently verify model output by domain, each pre-registered before build, each running zero-GPU offline against banked telemetry:

- **Arithmetic** — recomputed, answer checked against the recomputation;
- **Code** — executed; the verdict is the run;
- **Prose** — commitment nets checked against stated claims;
- **Sycophancy elicitation** — a modal-provenance ledger separating grounded assertions from authored artifacts;
- **Attention provenance** — where the answer's support actually came from.

The oracles are exercised by engineered fixture suites — hundreds of typed positive classes and negative controls, every row's ground truth verified at build — and the detector programs behind them are adjudicated on **fresh held-out walks** under pinned protocols, never on the data they were developed against.

---

## The Interface Gates — Multi-Turn Deployment (AG-1–3)

The forward-pass gates bound degenerate trajectories; they do not floor per-turn success. Any workflow-level lift in multi-turn deployment must come from the interface gates — and that lift is *measured, never assumed*. All three await the conversational harness (Stage 6); no multi-turn number is claimed before it exists.

| Gate | Function |
| :--- | :--- |
| **AG-1 — Inbound Tool Ingestion** | Governs how raw tool output enters context, by parse quality, in three bands: typed content only; typed content plus a bounded raw excerpt — *because retaining some raw error content is exactly what self-correction needs*; or quarantine of the raw stream with a structured status. Discarding all raw error content removes precisely the material self-correction works from. |
| **AG-2 — Turn-Boundary Anchor & Reset** | Anchor fields are verified before they are trusted — freezing an unverified anchor launders an error into trusted context, the dominant new failure mode of tool-using agents. Key-value cache resets happen only when the measured future savings pay for the re-prefill: *a decision, not a default*. |
| **AG-3 — Inter-Turn Stability Inheritance** | A fragile turn hands the next turn a bounded caution — one that can never dominate downstream behavior — and a clean turn restores full trust. No geometric compounding of conservatism across a session: content is sealed at the boundary, and only audit metadata crosses. |

---

## Evaluation Rig & Model Ladder

| Parameter / Dimension | Configuration Specification |
| :--- | :--- |
| **Target Architectures** | Llama family, walked up the model ladder: 1B → 3B → 8B parameters; the published benchmark record rides the base Llama-3.2-1B, unmodified weights |
| **Attention Backend** | Standard eager execution (fault-capture instrumentation) |
| **Evaluation Benchmarks** | MMLU, GSM8K, HumanEval/MBPP, plus dedicated prose and sycophancy corpora (published in `corpora/`) |
| **Sampling Strategy** | Deterministic greedy decoding for the program's generation legs; the founding Phase 2 evaluation scored MMLU by loglikelihood and sampled its GSM8K generation leg at temperature 0.8 under a 256-new-token cap |
| **Governance Modes** | Per-gate toggles: every gate individually switchable, dormant-by-default verified |
| **Regimes** | **A** — single-pass generation (all runtime gates); **B** — multi-turn deployment (interface gates) |

The model ladder is a discipline, not a formality: every monitor and gate family must re-earn its separation at each scale, and calibration is re-derived per model. Nothing transfers by assumption.

---

## Telemetry & Exported Records

Every governed walk emits structured records: per-step monitor telemetry, per-document fault ledgers, event logs with actuation magnitudes, and posture grades. Runs of record are deterministic and carry SHA-256 integrity receipts for their inputs and outputs; adjudication passes are zero-GPU mechanical replays over banked exports. Raw logs and exports live in `telemetry/` — the record is designed to be auditable by artifact ID and checksum, without trusting a single prose claim.

---

## What Is Withheld

The exact dynamic threshold calculus and the closed-form mathematical transformations of the Triadic Set remain a protected black box. The published record is complete at the empirical level — mechanisms at functional altitude, calibration outputs, telemetry, results, fixtures, and receipts — and silent at the level of derivations. This split is deliberate, permanent, and it is the only redaction this record carries.
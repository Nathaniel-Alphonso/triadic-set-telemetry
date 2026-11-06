# Triadic Set v32 — Test & Evaluation Plan (Public Protocol Summary)

This is the public protocol record of the v32 test and evaluation program: the hypothesis it set out to discharge, the claims that decompose it, the instruments that measure each claim, and the house laws that govern every run. It is distilled from the internal pre-registration of record. Mechanisms are described at functional altitude (see `ARCHITECTURE_OVERVIEW.md`); the measured numbers live in the telemetry exports, each carrying its own integrity receipts.

## 1. The hypothesis under test

- **H1 (core).** Governing the forward pass with calibrated mathematical gates — constraining the model from drifting, hallucinating, or producing otherwise-discardable output — reduces compute and increases accuracy simultaneously. Accuracy gain comes by *constraint and restoration*, not capability addition.
- **H2 (ceiling/floor).** Every governance cost measured on the development bench is a **ceiling on production cost**: an itemizable fraction of measured overhead is test instrumentation, which does not exist in a production serving path. Bench-measured cost is therefore a conservative floor of the scaled claim.
- **H3 (prevalence scaling).** Savings scale with how much of real-world inference is wasted on correction loops, re-verification passes, and discardable output. This is a property of multi-turn deployment, not single-pass benchmarks.

## 2. The claims spine (C1–C7)

No test runs that doesn't serve a claim component. Every test, phase, and acceptance criterion below is labeled with the component it discharges.

| # | Claim component | Discharged by | Proving condition | A FAIL means |
| :--- | :--- | :--- | :--- | :--- |
| **C1** | Constraint **prevents** undesirable output | Divergence harness; benchmark pairs with rejudged verdicts and flip tables | Wrongful terminations remain zero; actuation precision holds as actuation count grows | The actuator form is reworked |
| **C2** | Constraint **restores** otherwise-discarded output | Stress suites; per-actuation recovery classification against the paired baseline | Recovered outcomes outnumber worsened ones, rejudged on both sides | The diagnosis-to-actuator link is wrong |
| **C3** | Cost per usable output **drops** | Every benchmark pair | Tokens and seconds per correct answer lower under governance; usable accuracy not lower | Actuation economics are reworked |
| **C4** | Measured overhead is a **ceiling**, not a floor | Per-gate cost profile; instrumentation itemization | The production marginal lands far below the bench measurement | The execution moment is relocated |
| **C5** | Savings **scale with prevalence** of degenerate output | The multi-turn finality benchmark (Regime B) | Waste ratio lower under governance across a session | Interface-gate parameters are reworked |
| **C6** | Confabulation is **detectable** at the commitment point | Shadow replay offline, then live telemetry | The flagged population separates from the clean population by at least two standard errors on held-out data, a margin fixed before any measurement | The diagnostic statistic is replaced |
| **C7** | Confabulated paths can be made **improbable by redistribution** | Shadow-replay yield first, then live pairs | The substitute outcome beats the suppressed choice by at least two standard errors in shadow replay; the mask-loop count is zero in harness | Redistribution stays unwired; detection-only is the honest outcome |

**Disclosure convention (binding on all protocol documents):** count-based acceptance criteria are stated plainly (wrongful terminations zero; mask-loop zero in harness); statistical acceptance margins are stated as pre-registered values (two standard errors, fixed before any measurement); bounds derived from governance behavior are named with their values kept in the internal record. This is the same deliberate split the architecture overview records under *What Is Withheld*.

## 3. House discipline — the universal fail rule

A **FAIL never relaxes a threshold or an acceptance criterion.** A FAIL returns the gate to rework — the diagnostic statistic, the actuator form, or the execution moment — until the test passes. Thresholds are calibrated against data; they are never negotiated against failures. The threshold-sweep acceptance instrument (G12) is the standard acceptance test for every gate; the lane-conflict arbitration rule (G11) is the standing rule for every trigger.

## 4. The measured quantities

The metric set, named by what each measures. Computed values ride the telemetry exports; definitions stay in the internal record.

1. **Cost per correct answer** — tokens and wall-clock per *rejudged-correct* answer: a wrong answer costs its full compute and buys nothing.
2. **Usable accuracy** — correct answers plus calibrated rejections; a fluent wrong answer is not usable, a calibrated "cannot determine" is.
3. **Recovery classification** — per actuation: recovered / worsened / neutral, computed per document against the paired baseline, rejudged both sides.
4. **Exit ledger** — good / wrongful / late-kill-correct / unknown, with actuation precision tracked; wrongful must remain zero.
5. **Waste ratio** (multi-turn) — the share of tokens spent on correction rather than task success.
6. **Threshold sensitivity** — accuracy must remain flat across a wide threshold sweep while actuation counts move in an orderly progression.
7. **Monitor separation** — a monitor must separate its known-pathology population from clean traffic before it earns an actuator. **No separation, no actuator — full stop.**
8. **Detector sensitivity and false-positive rate** — measured together, on held-out data.
9. **Redirection yield** — whether the substitute outcome beats the suppressed choice, measured offline before anything wires; acceptance is two standard errors.
10. **Wrongful redirection rate** — the measured damage of redistribution, held below a governance-derived bound (the bound is computed from governance behavior; its value stays in the internal record).
11. **Hedge-emission health** — deferral quality and mask-loop count (zero in harness, bounded under stress).

## 5. The two evaluation regimes

- **Regime A — single-pass generation.** Greedy decode, one request, no retries. All sixteen runtime gates live here.
- **Regime B — multi-turn deployment.** Correction loops, re-verification, retry chains — where prevalence scaling lives. Only the interface gates (AG-1–3) operate here, and **no Regime B number is claimed before the conversational harness exists.**

## 6. The test suite (T0–T5)

**T0 — Divergence harness (preflight; every build).** Twenty fixed prompts: the original eight plus engineered cases for every gate behavior — loops, quarantine, re-anchoring, answer-phase transition, near-threshold dormancy, detector-flag dormancy, mask-trigger and mask-loop, hedge emission, grounding re-anchor. Invariants: zero events ⇒ bit-identical output; every divergence attributed to a logged event; an unattributed divergence is a FAIL. Every gate re-earns this harness without exception.

**T1 — Per-gate overhead profile (C4).** Every monitor priced individually, against the noise floor. A monitor whose cost rises above noise gets its execution moment relocated — cost is an engineering decision, never a fixed cost.

**T2 — Telemetry pass (read-only).** All monitors logging, zero new actuation. Dumps carry per-step generated token ids so every walk can be replayed offline without re-decoding — the replayability law.

**T2.5 — Shadow replay (offline).** Existing generations re-scored offline: detector separation, substitution yield, and the wrongful-redirection estimate are all measured *before any actuation wires* — separation and yield must each clear two standard errors. If yield fails, redistribution never wires — the standing rule the commitment-point family's honest 1B failure followed.

**T3 — Benchmark pairs + rejudge (C1, C3).** Paired baseline/governed runs on GSM8K (math reasoning), HumanEval 164 (code), and one long-generation task. Both sides rejudged; flip tables; per-document causal accounting. **Aggregate accuracy is a backstop, never the headline.**

**T4 — Stress suites (C2, C7).** Loop/fluff prevalence engineered high by design (versus its natural rarity), so recovery classification has enough events to mean something; plus a knowledge-boundary confabulation suite scored by usable accuracy.

**T5 — Multi-turn finality benchmark (C5; Regime B).** Fixed multi-turn scripts with a verifier: per-turn success, correction counts, waste ratio — baseline versus governed. Built in Phase 5.

## 7. The model ladder

| Model | Role |
| :--- | :--- |
| Llama-3.2-1B-Instruct | Primary: all calibration, all gates, all full pairs |
| Llama-3.2-3B-Instruct | First transfer: does gate *structure* survive recalibration? (Calibration does not transfer; the architecture is the thing tested.) |
| Llama-3.1-8B-Instruct | Depth check — run once, late |
| Qwen2.5-1.5B (optional) | Cross-family sanity, only if the thesis claims architecture-agnostic governance |

The calibration-transfer guard (G10) is active during every transfer run: on mismatch, thresholds rise. **Stranger input means stricter governance, never looser.**

## 8. Phased order

0. **Preflight hardening** — the divergence harness to twenty prompts; acceptance instruments validated on the existing gates. Nothing new ships until preflight passes.
1. **Measure before actuating** — telemetry passes, shadow replay, per-gate cost profile. Detectors earn nothing until they separate.
2. **Gate-by-gate activation** — risk order, one new actuator per run pair (attribution requires it).
3. **Regime A at full scope** — third task; stress suites; per-document accounting at scale.
4. **Generalization** — the model ladder, transfer guard active throughout.
5. **Regime B** — the multi-turn harness; the prevalence claim finally gets its number.
6. **Claim writeup** — every claim component gets its number and its provenance table; aggregate accuracy appears only as a parity backstop.

## 9. Scope discipline — the eight laws

1. At most three Regime A tasks — more benchmarks dilute per-document accounting.
2. One new actuator per run pair — two at once breaks attribution.
3. Aggregate accuracy is a backstop, never the headline — per-document causal accounting is the instrument.
4. The cache-retirement gate (G9) never actuates before its headroom number is measured — it is the only gate that touches stock-model semantics.
5. Every gate re-earns the divergence harness. No exceptions, including "obviously safe" gates. The learned gate earns it twice.
6. Every threshold is calibrated, then stress-tested by sweep — a knife-edge gate is not deployed regardless of its point results.
7. No hard suppression without measured shadow yield — the mask is the only actuator that removes a choice the model made; it wires only if the substitute beats the suppressed choice by at least two standard errors in shadow replay.
8. **Failures return to the formula.** No threshold is loosened to convert a FAIL into a PASS.

## 10. Where the artifacts live

- **`fixtures/`** — the engineered fixture suites and negative controls every acceptance gate runs against (arith, code, prose, exit-verdict, loader negatives, rework-lane families, integration and stream-parity worlds).
- **`corpora/`** — the prompt corpora behind the offline passes and domain arms.
- **`telemetry/`** — the exported records: runs of record, fault ledgers, per-arm adjudications, with SHA-256 integrity receipts throughout.

# Offline Checker Passes — Zero-Model Measurement (Public Protocol Summary)

Before any Gate 17 arm reaches fixture design, it banks its natural censuses: what its instrument actually reads on real generations, what coverage costs, and what the measured fault classes look like. Those censuses come from **offline passes** — replay runs over banked telemetry that involve no model, no GPU, and no live environment. This is the protocol record of the three passes of record: the arithmetic checker pass (the content channel's first rung), the code-verification pass (17-C), and the prose-verification pass (17-P). The arm designs themselves are in `02-oracle-verification-gates.md`; this document records how each arm was measured before it was judged.

## 1. The offline-pass contract (shared by every pass)

1. **Offline by law.** A pass reads banked artifacts only — saved generations, rejudged label files, prompt manifests, census records. It never loads the model, never touches the compute environment, and never interacts with any held or in-flight program.
2. **Never re-derive what is banked.** A number that exists in a dumped artifact is quoted, not recomputed. A pass creates new numbers; it never adjudicates old ones.
3. **Pre-register before run.** Each pass executes per its pre-registered document only, and only after my stamp. Nothing is built or run unless it was pre-registered first.
4. **The manifest and the VOID rule.** Every input is named in a pinned artifact manifest. If any input cannot be satisfied from banked files, the pass **VOIDs** — no substitute input is used, and nothing is re-run to fill a gap.
5. **Integrity gates on receipt, before execution.** Checksums computed on received files must match my own console line; record counts reconcile against the banked census; document-id joins must match exactly; pinned manifests must match their pre-generation checksums. Any mismatch is a void-class failure.
6. **One record of authority.** Each pass writes a single export JSON (console tee'd, checksummed); it is read-only on its inputs.
7. **Descriptive only.** No pass sets, moves, or adjudicates any threshold. Its pre-registered readings are presented to me; governance consequences flow only through my stamps.

## 2. The arithmetic checker pass — the content channel's first rung

Measured the arithmetic checker and the answer-provenance detector against the banked arithmetic corpora, both legs (the raw leg and the chat leg). Its pre-registered measurements:

- **Extraction precision** — the fraction of extracted candidate statements that parse into a well-formed claim, with every false parse censused and worked as an example. This is the extractor's precision bound: at run time a false parse is a false fire, and false fires are accounted damage.
- **Slip rates** — how often a well-formed statement's stated result fails recomputation, per document and corpus-wide, with slip position and label joins.
- **Answer-provenance violations** — the fraction of final answers that trace to no verified chain value (the gap-bridge census), joined to the correctness labels.
- **Retroactive separation** — how well the checker's verdicts separate the known-wrong from the known-correct population on the banked corpus, reported against the pre-registered separation standard. This reading is **corpus context only**: the checker's authority on its class is recomputation-based rather than statistical — the separation reading never grounds a verdict.

Its pre-registered honesty readings govern the next step: a corpus too clean to exercise the failure class makes engineered fixtures mandatory (no conclusion about the detector is drawn from a corpus that never slips), and low extraction precision sends the extractor back to rework before anything else proceeds.

## 3. The code-verification pass (17-C) — instrument validation, honestly

The banked HumanEval corpus already carries rejudged doc-level verdicts, produced by the rejudge instrument — which is the 17-C oracle's own execution core. The pass therefore **never re-derives pass@1**: the banked majority-verdict labels are an *input*, and every doc-level verdict the new instrument produces is checked **against** them, never substituted for them. The agreement join validates the new instrument; any disagreement is an instrument-bug candidate, adjudicated openly — never waved through, never converted into a re-derivation of the label.

What the pass produces that no banked artifact contained:

- **The extraction census** — block yield and failure classes on the corpus's actual generations, with every unverified class censused, never hidden (the fails-open law).
- **The deterministic-meter census** — the first empirical test of the deterministic-meter law: identical code must produce identical meter counts across repetitions. Any meter flip voids the cost numbers and sends the meter implementation back to rework.
- **The cost census** — the measured distribution from which the arm banks its execution ceiling and pins its meter budget (a fixture-time decision, stamped by me; the ceiling does not inherit from any other arm).
- **Post-block-commitment volume** — the evidence gate for in-loop blocking execution (Tier 2): it is proposed with costed numbers or not proposed, on this measurement, not on argument.
- **The fault-ledger contract** — the event schema every future consumer of this arm is written against.

The sandbox law binds before any build: model-generated code executes only in an isolated sandbox, fresh subprocess per document, no shared state, with wall-clock surviving only as a safety failsafe that never produces a semantic verdict.

## 4. The prose-verification pass (17-P) — designed coverage, honestly labeled

The prose oracles had no banked corpus, so the pass designed one: a purpose-built manifest of constrained, traceability-bait, and grounded tasks — including sycophancy-bait prompts with embedded desires, some deliberately contradicting the available evidence — generated under the frozen instrument on both legs. Its honesty clauses, carried on every rate it reports:

- **Elicitation-conditioned.** The corpus is *designed* to give each oracle coverage. Rates measured on designed tasks are detector performance where the fault class was made likely — never the model's natural emission rates, and no natural-volume claim is ever made from this pass.
- **No-labels oracles.** There is no rejudge-class join here: P1's oracle is the prompt's own stated constraints, P2's oracle is the generation's own provenance ledger, P3's oracle is the paired source passage. Zero world knowledge enters any verdict; every ambiguity fails open.
- **Coverage, marker, and cost censuses.** Every unverified doc is censused (the fails-open cost, measured, never hidden); the goal-language marker class is mechanical and imperfect by design — an unmarked desire fails open, and the miss costs coverage, never damage.
- **The inconclusivity fallback, pre-registered.** If any detector's measured volume is too thin to support a rate, the single-corpus design is recorded as inconclusive for that detector and a per-detector corpus fallback is proposed with the measured numbers — adjudicated on the numbers, not argument.
- **Terminal classes never promised away.** Pure-tone sycophancy, paraphrase contradiction, and general semantic verification stay outside every oracle — measured as boundary classes (see `04-fixture-validation-suite.md`), never smuggled in.

## 5. What these passes do not do

No actuation. No wiring. No trigger decisions. No re-derivations of banked numbers. No interaction with held or in-flight programs. Each pass feeds fixture design and the acceptance drafts — nothing else — and my stamps adjudicate every reading.

# The Failure-Shape Program: failure modes as measured structure

A live forward pass cannot consult a semantic category. The pass carries tensors, emissions, and statistics, and a governance mechanism wired inside it can act on nothing else. Before any in-band detector can be qualified, the failure modes it will target need definitions of the kind a forward pass can actually read: mechanical quantities, measured shapes, and thresholds derivable from the model's own traffic. The failure-shape program is that definitional work. This document states what was defined, what the published receipts measure, and what the definitions buy for the in-band mechanism.

The program's position, stated plainly: on the 8B parameter model's development data, the deepest rung walked to date, the failure classes under governance came to carry mechanical definitions. Degenerate, repetitive, quiet, and overt failures are defined on that data as measured numbers and mathematical shapes, in place of semantic categories. That is the result the in-band refinements now build on.

## The four failure classes under definition

| Class | How it presents | The mechanical question the program had to answer |
| :--- | :--- | :--- |
| Degenerate output | The walk collapses into unusable emission | What measured structure separates a degenerate walk from a clean one? |
| Repetitive output | The walk re-emits its own output, confidently | What statistic rises with the loop and stays flat on honest traffic? |
| Quiet failure | The model commits to determinate content on diffuse support | What is measurable at the moment of commitment? |
| Overt failure | The failure announces itself in the output | What reads the loud side without waiting on a human? |

A live forward pass draws no semantic line between the quiet failure and the overt one, so both classes were defined under one governed ledger rather than as separate problems. The detector programs documented in the protocol lane ([oracle gates](protocols/02-oracle-verification-gates.md), [offline checker passes](protocols/03-offline-checker-passes.md), [fresh-walk adjudication](protocols/05-fresh-walk-adjudication.md), [the emission-degeneration program](protocols/07-emission-degeneration-program.md)) are the instruments that earned these definitions; this document states the definitional result at the 8B rung.

## Why the deepest rung carried the definitions

Calibration re-derives per model: baselines, envelopes, and reference traffic all re-measure at every rung, so definitions earned only at a shallow rung would read as artifacts of that rung. The 8B work therefore ran deeper than a scale transfer. The walk families (math, code, prose, and the commitment corpus) were walked at 8B, and the reads were built at two granularities from that data: per document, where each walk carries a verdict and a fault ledger, and per step, where the emission statistics record at every content commit. The document-level reads and the token-level reads were then joined into the composite view the detector program was built to produce: one walk, read at both granularities, from its own traffic.

## What the published 8B receipts measure

**The arithmetic checker at 8B (the overt side, content class).** On the raw leg, 1,319 walks: extraction precision 95.93% over 7,094 candidate statements, 94 arithmetic slips in 6,805 well-formed statements, a 1.38% slip rate, position-skewed late (65 of 94 slips late). The label join is the receipt that carries: 12.33% of wrong walks carry at least one slip against 1.16% of correct walks, and a walk carrying a slip finishes wrong at 80.70% against a 28.28% base rate. Answer-provenance violations read 9.71% overall, 24.40% on wrong walks against 3.91% on correct walks: the wrong answer tends to arrive without a verifiable chain behind it. The chat leg (100 walks through the chat template) reads a 0.65% slip rate on a sample of two slips; its join carries no claim and is stated as measured.

**The commitment corpus at 8B (the quiet side).** The corpus pairs desire markers against evidence axes: desire against contradicting evidence, desire with the evidence absent, and consistent-evidence controls. On the raw leg, 108 established commitments against 68 promotions, the promotion shapes firing in the cells the corpus designed them for, the designed empty cell reading exactly zero, and the cross cells censused rather than pooled. Silence failures read zero on both legs. The chat leg holds the same structure: 32 established commitments, 14 promotions, the designed empty cell zero. The corpus proves the commitment moment is measurable: the quiet failure fires as a counted, shaped event, not as a judgment call.

**The oracle gates and the loop-fixture census.** The ten loop-seeded fixtures ride every 8B pass as the degenerate-side control census, and the oracle acceptance runs (arithmetic, code, prose) publish in the gate 17 lane. The degenerate-side readouts at 8B, the shape census and the dual-sided adjudication re-pins, are banked as development receipts; the record lane's run-of-record receipts publish under `telemetry/v32/phase4/` as the lane closes, per the record's standing rule that development batteries stay named and counted rather than silently pooled into the record.

## What the definitions buy

1. **The shapes are numbers now.** Each failure class the in-band mechanism will target carries a mechanical definition earned on the deepest data walked to date, so the forward mechanism refines against measured targets rather than semantic intent.
2. **The honest ledger travels with them.** Every number above is a development-data reading: valid per the data that produced it, earned under pre-registered passes with pinned inputs, and stated with its sample size and its negative reads kept at full weight. The commitment side's 1B read stays at zero detection credit until a larger rung re-earns it.
3. **The in-band position follows.** With the failure modes mechanically defined, the program's main move is now a refinement problem rather than a discovery problem: the operating threshold and its look-window re-derive from the banked data in the qualification refinements, the surviving signatures wire into the live forward pass behind the staged order's acceptances, and nothing fires in-band ahead of the stage that accepts it.

## Where the receipts live

- `telemetry/v32/offline-passes/`: the 8B exports, covering the arithmetic checker pass and its chat leg, both commitment-corpus passes, the per-document fault ledgers, and the acceptance consoles (48 PASS / 0 FAIL on the 8B fork acceptance).
- `telemetry/v32/gate17/`: the oracle acceptance runs behind the gate lane.
- `telemetry/v32/phase4/`: the scale-transfer record lane, where the 8B run-of-record receipts publish as the lane closes.

The exact dynamic threshold calculus stays protected ([What Is Withheld](../README.md#what-is-withheld)); everything in this document is the measured, replayable layer around it.
# Sanitization Receipts — rw16

The following published files are sanitized derivatives of banked run artifacts, or byte-for-byte copies of banked artifacts (rows with zero redactions). Per publication policy:

- the runtime threshold constant (theta) is redacted everywhere it appears (numeric fields and provenance strings);
- level-set operating bounds (t_leg / t_esc values, per-side z thresholds) are **named-but-withheld**: field and line names publish, values are replaced by `[REDACTED_PER_PUBLICATION_POLICY]`;
- the derivation-rule strings (the quantile formulas, the level-set law, the N_band definition, the Side C gate parameter) are redacted, not paraphrased; console rule-prose lines are dropped and counted below;
- ancillary governance parameters (jitter tolerance, population guards, falsifier ceiling, annotation quantile constants) are redacted, names kept;
- pre-registered margins (the held-out 2-sigma bar, `PASS_2SIGMA iff gap >= 2.0`), measured sigma gaps, AUCs, fire/census counts, and verdict records publish as-is;
- local filesystem paths are trimmed to artifact names.

Original SHA-256 is the byte-hash of the unredacted artifact of record.

| Published file | Theta redactions | Rule/bound redactions | Dropped lines | Path trims | Original SHA-256 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| rw16_acceptance_console.txt | 0 | 0 | 0 | 1 | 4b5c89cc98c3681daf1824998bc759edd482e9efeb1ef55bcaa742422cffd107 |
| rw16_acceptance_console_v2.txt | 0 | 0 | 0 | 1 | 9d8165bd244a1cd6576f4b6d064c11841f38b80f975e2efc6509b0ed04c0f950 |
| rw16_control_console.txt | 0 | 0 | 0 | 0 | 9f87cceae86146360f08578a176709f3ec84a00c0ebec2569152566e3d814b99 |
| rw16_control_console_v2.txt | 0 | 0 | 0 | 0 | bc232922662ef2c4d4cb6e50957380ce6c30aef33956ce271aeb2ac3d504a6e4 |
| rw16_readout_console.txt | 3 | 0 | 0 | 0 | a0a3462d4fec200d7b04882bf7338f205853e5a2c41c02eb86e0f7df6b195cf0 |
| triadic_rw16_readout_rw16-adjudication.json | 2 | 39 | 0 | 0 | b80c73567716c6599583fde59341988e389223232d8b557d6d7137d0c7084605 |

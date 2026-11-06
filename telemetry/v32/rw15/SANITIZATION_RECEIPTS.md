# Sanitization Receipts — rw15

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
| rw15_readout_acceptance_console.txt | 0 | 0 | 0 | 1 | 48a9898ff74f9d7792f827ff807c7a578783da9478ce017e36ed6a5110eb66a5 |
| rw15_readout_acceptance_console_v2.txt | 0 | 0 | 0 | 1 | e0d0dfbaac1d5a6d9db2c553a5f7aa0c1a79f1a794a460199e2133d0bfb8daf4 |
| rw15_readout_control_console.txt | 1 | 0 | 0 | 0 | 52d3597e532b855edcd8cddb783d29083be8bc6fef54e80ae408bfdd8be5174c |
| rw15_readout_control_console_v2.txt | 1 | 0 | 0 | 0 | 41a9f3004db95efb74c14b16783ad5501443dfb8dd312fc65dc708f879adc71f |
| rw15_readout_control_export.json | 0 | 0 | 0 | 0 | 0f9e99ecf9d70da38de7feace1e5caa32a2388e23d4694fa9d6e8e98565d9441 |
| rw15_readout_control_export_v2.json | 0 | 0 | 0 | 0 | 9fb3ac8f6180578aed5ad3c8357da95de92bff10dbb556f7d9563a356813eed8 |
| triadic_rw15_readout_rw15-readout.json | 2 | 0 | 0 | 0 | cd65d5ab1bd9924f8f73d34350d6ac42463f6192385102f312c6f4557878765a |

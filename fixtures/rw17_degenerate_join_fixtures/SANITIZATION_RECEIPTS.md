# Sanitization Receipts — RW-17 degenerate join fixtures

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
| join_out_run1.json | 2 | 38 | 0 | 0 | 97935251599641ee8b025cefe5583f3faf6be92409549e28841a3402c93f07ef |

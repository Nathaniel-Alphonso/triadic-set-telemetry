# Sanitization receipts — telemetry/v32/phase4/ (Lane J)

Disposition record for the phase-4 receipts lane (owner-approved verdicts, Nov 7, 2026).
Marker: `[REDACTED_PER_PUBLICATION_POLICY]`.

Redaction class applied (the entry-level-set class, per the results-lane standing ruling):
- the entry-band `lo`/`hi` operating values (12 pairs total across the two exports) are
  named-but-withheld — field names kept, values redacted;
- the band derivation phrase in the `source`/`entry_band_source` strings (5 occurrences)
  redacted; the receipt pointer text kept.

Published as-is inside the exports (measured outputs and receipt conventions, verified):
the R5 fixture maxPRsig ranges, the R9 window-reference summaries, the trip-time reading
conventions (counting line 2.0 = the pre-registered margin; mass count line; first-at-8),
parity receipts, censuses, concordance cells, fused-hook tuples, lineage SHA-256 pointers.

Theta literal check at staging: exact-literal scan CLEAN on both exports and the console.
Documented coincidental mantissa hits (3 per export): measured per-layer values whose
mantissas merely begin with the guarded digit sequences — the same documented
false-positive class as the published fixture caches; not the threshold constant.

## s8-rework-receipts/

| file | disposition | markers | original SHA-256 | staged chars |
|---|---|---|---|---|
| `rework-v1_export.json` | sanitized derivative | 21 | `f4e941602a27b0621061bbe3732cd3833ba412f77d8cfb33831d3a1470417a7a` | 7064782 |

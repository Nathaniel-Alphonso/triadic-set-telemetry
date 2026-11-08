# Sanitization receipts: telemetry/v32/phase4/stream-monitor-validation-receipts/

Disposition record for the stream-monitor validation lane (my owner's stamps
Nov 8, 2026: publish the lane, the phase-2 parity run riding the same commit).
Marker: `[REDACTED_PER_PUBLICATION_POLICY]`.

Redaction class applied (the entry-level-set class, per the results-lane
standing ruling, the same class as the s8 lane):
- the r2 entry-band `lo`/`hi` operating values (4 pairs total across the two
  integration receipts) are named-but-withheld: field names kept, values
  redacted;
- the six-decimal console roundings of the same 4 pairs (2 lines in each
  integration console) redacted; the line names kept.

Published as-is (measured outputs and receipt conventions, verified): the
per-doc monitor-vs-census rows, the cut and rewind-anchor and keep-length and
post-anchor tuples, every quartile block, the zero-actuation clean-walk rows,
the hard-gate lines, the pins blocks, the cap-burn aggregates, and the
monitors' captured n-gram evidence of model-generated text. The n-gram
evidence carries documented incidental person-language words (15 occurrences
in each phase-1 receipt, 90 in each phase-2 receipt): the same documented
measured-evidence class as the published degeneration-census exports, never
authored prose.

Staging checks: exact-literal scans CLEAN on all eight files for the threshold
constant class and the guarded development-literal class; no em-dash in any
file; the sanitized receipts re-validated as JSON after redaction. No file in
this subdirectory was authored for publication: four files are byte-for-byte
copies of the owner's runs of record, four are sanitized derivatives of them;
the runs of record stay banked owner-side with their original SHA-256 digests
recorded below.

| file | disposition | markers | original SHA-256 | staged chars |
|---|---|---|---|---|
| `stream_parity_console.txt` | byte-for-byte copy | 0 | `acee6c68cf6ede4734a61e2433748154101b6a429b991e2e3ce100c9b796e9ae` | 1545 |
| `stream_parity_receipt.json` | byte-for-byte copy | 0 | `c181afc0401397b1972c53b433ff70bfcd356c8124bc3af4d6c12bda09a4b19f` | 618617 |
| `integration_console.txt` | sanitized derivative | 2 | `1d6a18a7291e1e3dc25896e40693e3f9b9b8b7b7554b8ec22bb786e912b6ae4e` | 2200 |
| `integration_receipt.json` | sanitized derivative | 4 | `7ec5e6798d3aecf925726019ff4808f2b7efc918cfeb90b7090ab6469c887b78` | 1173512 |
| `stream_parity_phase2_console.txt` | byte-for-byte copy | 0 | `c2d20a3233237e9484fd070af26954d11031f8c1b436ef7fa59e50918f5bcf8e` | 1684 |
| `stream_monitors_parity_run_phase2_rw17-phase2-parity.json` | byte-for-byte copy | 0 | `e620fa02bb5a20c9b845f694b8f12529f996b650431756377a45709c54502ecf` | 878661 |
| `integration_phase2_console.txt` | sanitized derivative | 2 | `f5cb87e1450ecccca791cb7945d9ba0906db5c5eb4c273aab99a320488df5bd5` | 2562 |
| `triadic_integration_readout_phase2_rw17-phase2-integration.json` | sanitized derivative | 4 | `16db6391870d603b4bf6cf0d6ed74e7a36fe70e5534421f5fe98a4da3938bb22` | 2147577 |

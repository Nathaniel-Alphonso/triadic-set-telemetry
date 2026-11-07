# Sanitization receipts — scripts/plumbing/acceptance_runs/

Content-check disposition record for the §3B plumbing tier (my approved verdict list, Nov 6–7, 2026).
Marker: `[REDACTED_PER_PUBLICATION_POLICY]`. The marker replaces only the threshold-constant literal; all
redactions sit in compliance/theta-note banner strings (verified per line). Dropped-lines: 0 (no rule-prose
lines in this tier). Path-trims: none needed (working-root constants are generic sandbox paths, not machine
paths). Rule-bound content: none — all files verified free of detector-side math (content-check verdicts on
record). Every file passed the θ literal check at push time.

## Acceptance-run scripts (1B-era test-method documentation)

| file | θ redactions | disposition | original SHA-256 | staged chars |
|---|---|---|---|---|
| `ap17_capture_acceptance_run.py` | 1 | sanitized derivative | `362e8ad14f4af1e416943fdd8f729d9c377401849e4884cbc4aed030b43a4b22` | 27845 |
| `ap17_capture_control_run.py` | 1 | sanitized derivative | `e3501eb7e816d32b47847d7bdc0cda75dfe754b1837de4fb9d479465e1cbfe11` | 14504 |
| `ap17_join_acceptance_run.py` | 1 | sanitized derivative | `9a8c56d22db2320f98ad8b98d4bb713594728826e69fa6b1b8395bf1d966771b` | 58069 |
| `ap17_join_control_run.py` | 1 | sanitized derivative | `36363f7474ba660b0454d3cc471465d4d7c281732d2d37d85047c666afce47bb` | 39022 |
| `rw15_readout_acceptance_run.py` | 0 | as-is (byte-for-byte) | `88a178f925d38a65b73c52f1532adacf0e0a2e26a75b9d5fe2f2204df7b38df4` | 23229 |
| `rw16_acceptance_run.py` | 1 | sanitized derivative | `50834490143dcfc1692fa46d4b7ebd3eaca2f0405edcbbc7eb939d6247b836ac` | 67775 |
| `rw16_control_run.py` | 0 | as-is (byte-for-byte) | `aa8ce2047a76ddd5364433f9027415908e87201b130881fb4d0491065517da0b` | 22167 |
| `rw17_code_builder_acceptance_run.py` | 0 | as-is (byte-for-byte) | `05d1434a62a2daf7d22d474b8a4740904ce826f429585b2d6cdb543fdbd41d57` | 7365 |
| `rw17_code_builder_fresh3_acceptance_run.py` | 0 | as-is (byte-for-byte) | `6dee6f3403b3fcf0157cdb6aa5960a47ef37a8c364b11352b0d261d3356ca217` | 8677 |
| `rw17_degeneration_census_acceptance_run.py` | 0 | as-is (byte-for-byte) | `57bc59a5652bcff253c9fa66b11df60cb5cc9e0c137227b47bf875af30f66b14` | 14562 |
| `rw17_degeneration_census_phase2_acceptance_run.py` | 0 | as-is (byte-for-byte) | `05ef4998ea2df3e792ba2bb392fce9d3d72bdc983d16024442ed5ca4ca6d5b5d` | 22891 |
| `rw17_degeneration_census_r2_acceptance_run.py` | 0 | as-is (byte-for-byte) | `b715111fbdff156aa7da07c489bd5ffe035f2cc616777315ba7de089b4ed3ccd` | 18555 |
| `rw17_fires_forensics_acceptance_run.py` | 0 | as-is (byte-for-byte) | `f90b758ecc72849ef7ed797e1b2118a8415ac905de33ed862f596c82d8ecd549` | 15605 |
| `rw17_math_builder_acceptance_run.py` | 0 | as-is (byte-for-byte) | `2fc279dc29e31de00baebeba0b621d56963dd8c55e9fd187d13fd0795cdb3825` | 6429 |
| `rw17_math_builder_fresh3_acceptance_run.py` | 0 | as-is (byte-for-byte) | `f1bd4fcdce3f18bd5f34d2660cabf9a2e303ce7529be9b07792a84eb68963828` | 9167 |
| `rw17_p2_builder_acceptance_run.py` | 1 | sanitized derivative | `6ec0a51e21c5195ed0d904d6c12d21a01fa0bd3790b9ffc4a15da34b66147c5d` | 17002 |
| `rw17_p2_builder_fresh3_acceptance_run.py` | 1 | sanitized derivative | `8f214f93fd9c534b00e0714a6930916d217f028c842b65f0dd27dc78c0d109d1` | 20219 |
| `rw17_prose_builder_acceptance_run.py` | 1 | sanitized derivative | `3d943b6f5576ed085d26587a8c656e851309147e079a1b5a73c8a87667294ada` | 22064 |
| `rw17_prose_builder_fresh3_acceptance_run.py` | 1 | sanitized derivative | `65ea9e99c4381b5d0af9e35cee6662e65dc301b21cd03204642bef0d28e99e5c` | 25752 |
| `rw17_readout_acceptance_run.py` | 6 | sanitized derivative | `0d8112a73ea68996b92ee229aaea6ffefd4dd38dea1e3ab77b99b528364dc148` | 89926 |
| `rw17_readout_control_run.py` | 2 | sanitized derivative | `470b2ea726e55e8100bb3ece30a84051fee7c2479a13da37ee108c8047a68528` | 13582 |
| `rw17_readout_v2_acceptance_run.py` | 2 | sanitized derivative | `6f417a9b290389182b16223729419ca0ff35db08c297f98c2e3a41bcb87258c9` | 52014 |
| `rw17_readout_v2_control_run.py` | 2 | sanitized derivative | `da6ced4f33f68e2e037c41f4a7cf039ae73d4be6c710d6969bbe96df30567d1a` | 29956 |
| `rw17_sec_acceptance_run.py` | 2 | sanitized derivative | `0a99bb93df6bc4e0c0efd4572df6be6f34151cb5a91f98a439b6fd2619ca307e` | 37608 |
| `rw17_sec_control_run.py` | 1 | sanitized derivative | `df8fe8bf4142107fdbf7180cbb5450de6b8adf2c59ffc44b4acea0d2f36d1e7d` | 27612 |
| `rw17_thin_extract_acceptance_run.py` | 0 | as-is (byte-for-byte) | `78362ba3cd1c863d319bcb717deebeb902ce6e11e978c0ce2a984a85b51f5fad` | 7766 |
| `triadic_arith_acceptance_run.py` | 0 | as-is (byte-for-byte) | `ac17d9d2783f157ec0d709c7279af054d7b5635b34e283f35d35b0e99c880137` | 14624 |
| `triadic_code_acceptance_run.py` | 1 | sanitized derivative | `8336f06e5b951958a97b26eacdbc4ba9df6939d0bb57c663fef6a5df2d6e17b3` | 15947 |
| `triadic_degenerate_view_join_acceptance_run.py` | 2 | sanitized derivative | `9254b372a428e7c853dc2802ef3e9432068d8c5f3a75cef29b287bb3ccad5be1` | 53913 |
| `triadic_exitverdict_acceptance_run.py` | 2 | sanitized derivative | `5c468c928147244446b2ca26be3e7a7a8321040f9380618986362a9bde898a9b` | 10282 |
| `triadic_prose_acceptance_run.py` | 1 | sanitized derivative | `3444e21e811e89bfc0a8d5a26cd7422f69b890bbac29bbe5918107a20b6525c8` | 19379 |

# Sanitization Receipts — rw17

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
| rw17_code_builder_acceptance_console.txt | 0 | 0 | 0 | 0 | d337cb7e8f64e75305e1ccbf2254f2c0f9c7690ca9f000472850ee9c4a13a4ea |
| rw17_code_builder_fresh3_acceptance_console.txt | 0 | 0 | 0 | 0 | 077a6959e0caca2f6474adff1e61eb83b8e2364725e8690bdd748f21aa315075 |
| rw17_degenerate_join_acceptance_console.txt | 1 | 0 | 0 | 0 | d1e503452ae9a8db665c5a362c04e58e9a5929c57f7348f325d94fc54b35a6b1 |
| rw17_degeneration_census_acceptance_console.txt | 0 | 0 | 0 | 0 | e29b8f08fd6e25433607dd91e0238f78c2a2159657a039c8c7748af418b61a0a |
| rw17_degeneration_census_console.txt | 1 | 0 | 0 | 1 | 86cd2ecc191170b3e1c2f4f768befa192245e6df226ee35c84ed93587f97e20f |
| rw17_degeneration_census_phase2_acceptance_console.txt | 0 | 0 | 0 | 0 | 3c22901004877f86dce7c68306b21133c89299571106d1fb8aa8b7d95898265c |
| rw17_degeneration_census_r2_acceptance_console.txt | 0 | 0 | 0 | 0 | c81fe025c2acde423b1e3a59ca02ce7b61fa3f714c612103b1e851d02bd968cf |
| rw17_fires_forensics_acceptance_console.txt | 0 | 0 | 0 | 0 | 7058e1807a4355bf7535dc851713f6c4b516441e4e066973ddd153835b60777b |
| rw17_fires_forensics_console.txt | 1 | 0 | 0 | 0 | d6e416cde95a7be9fafc2c99ce33b70141c1c57ef4a20ae0d3b363fe087e3982 |
| rw17_fires_forensics_report.json | 1 | 4 | 0 | 0 | 23c243a5ee0ca8a3e51f0f985c8c9ff62bb781db0054f9ef43581325e2d6da44 |
| rw17_horizon_composition_fixture_console.txt | 1 | 0 | 0 | 1 | 171ffee55708554dbe5c39491a5ea71872628fd5b30e5310a4b950a8e44bd05b |
| rw17_math_builder_acceptance_console.txt | 0 | 0 | 0 | 0 | 52f00405338688b98e17629defd2b8c49adba1010adce3a7f0008a657eea22a8 |
| rw17_math_builder_fresh3_acceptance_console.txt | 0 | 0 | 0 | 0 | 6de167a2913372f8d5fcd5fbe9aac1d7bc5daf1aaf728c871f0a75ead87ad14a |
| rw17_p2_build_console.txt | 0 | 0 | 0 | 0 | 0c2a073bb355e12d07b54724add4d25e11a487dcfa35a51c67cc0841e05bdcfa |
| rw17_p2_builder_acceptance_console.txt | 0 | 0 | 0 | 0 | c8f1fdde0a9515e079103379b445dbdd6d8efe5eb37f542f328410967f0501d9 |
| rw17_p2_builder_fresh3_acceptance_console.txt | 0 | 0 | 0 | 0 | 394f548d529333f9b34d0f6f71bdde33be54d006613ae98fcc3ea1bb902b7987 |
| rw17_p2_fresh3_build_console.txt | 0 | 0 | 0 | 0 | 391c216b32a44ffb2910adaf5d2bff46878122cc7c39511fe009106475122157 |
| rw17_prose_build_console.txt | 0 | 0 | 0 | 0 | 69c8d5fa10f5b9c366ea234c32b78decf0529de51d84e90adb3af71c7bc54699 |
| rw17_prose_builder_acceptance_console.txt | 0 | 0 | 0 | 0 | 44727a476591ed94889ca3242b76cd25735325914578db65043802c13238e4fc |
| rw17_prose_builder_fresh3_acceptance_console.txt | 0 | 0 | 0 | 0 | b3ef97c1955061726b36030a3eac2fe248a9dcb5cd3202c1f23595d8d82b4a9d |
| rw17_prose_fresh3_build_console.txt | 0 | 0 | 0 | 0 | e37387685dda6c25a5d8856686ad204697f154616cf47752b2990ae841db7719 |
| rw17_readout_acceptance_console.txt | 2 | 0 | 0 | 1 | c4e1267e9d9305d5cd224222590fd6e9c323567ca06051eb0b8bb2105d7b20f7 |
| rw17_readout_console.txt | 2 | 13 | 2 | 0 | 9352af9dbbdb5bb8db8e0b4369f4adc918e417b624968d6f5c78b4ff2b122118 |
| rw17_readout_control_console.txt | 1 | 0 | 0 | 0 | 026dd9d4244d17f1ee876f35ffd04df69ad1120c386dfcab42262dd257d2e4e8 |
| rw17_readout_v2_acceptance_console.txt | 1 | 1 | 0 | 1 | de5639a828bb9e7083da99654b878f8e1393cef9b01ab43ed0ec63ea13427d3e |
| rw17_readout_v2_control_console.txt | 1 | 0 | 0 | 0 | fc01665ef3acaf3d0deac38d110c90c84bbf793f72dfc2163ee8969770178a0d |
| rw17_sec_acceptance_console.txt | 1 | 4 | 0 | 0 | 4350ef70c099ad54927c27ee53fabbbcc8f9bdf197e75831944389e3bbdda7ed |
| rw17_sec_baseline_console.txt | 2 | 12 | 2 | 0 | f553db82697710d9bf843e2e28205bc753270bde03efb2afef9206538e7f144b |
| rw17_sec_control_console.txt | 1 | 0 | 0 | 0 | df0314edef2ba3d2bfd881bb10cac2b9eef61016dd8ba5818bb17935c53ee4da |
| rw17_thin_extract_acceptance_console.txt | 0 | 0 | 0 | 0 | 63e9296585f2f6e9f6d6e8b33cd34bfb58a7b2a28752fac68320267086806ea8 |
| rw17_v3222_build_console.txt | 0 | 0 | 0 | 0 | fe79b37a55dd1a3e83e5549dd23cb38eee91820e06e78b142c8331d9a26e5ce2 |
| rw17_v3222_loader_fixtures_console.txt | 0 | 0 | 0 | 0 | 305946dc91a02754f0cfec4e99332bd34d37ea507ae9ee5a7f92dffc1757cc4d |
| rw17_v3230_build_console.txt | 0 | 0 | 0 | 0 | 5bea7c74245396998e004bd2baa94aa35849383d3b3a782509b1b39e10430abb |
| triadic_rw17_degeneration_census_phase2_rw17-phase2-census.json | 0 | 0 | 0 | 0 | 5f09f1a91a94239308bae455edb95cbaec6e270c02120b2d6230aa3bd0773a17 |
| triadic_rw17_degeneration_census_rw17-census.json | 0 | 0 | 0 | 0 | 6e38dbf1652dde27750e7cb13e12719c7108e1a5faafb33aa079e16973b56a91 |
| triadic_rw17_readout_rw17-fresh-adjudication.json | 2 | 36 | 0 | 0 | e294da43ef003ccd81abb45880773fa00bd58241677c42e0ad25ea95244226c8 |
| triadic_rw17_readout_rw17-fresh3-adjudication.json | 2 | 38 | 0 | 0 | bde6b15013cc6ecbbfb0cd951c37619fcc67dcd1f2239759748b6e53e9e18940 |
| triadic_rw17_readout_rw17-r2-adjudication.json | 2 | 39 | 0 | 0 | c9cb6b6cec3ea76f1d57a538e9bbaf069ea495e2091ef30392f577d24c33ff29 |
| triadic_rw17_sec_baseline_rw17-sec-baseline.json | 1 | 30 | 0 | 0 | 840fe7fcd50dc6461a392c4e247bcf3484f557040fd6feb9140307b3264170e9 |

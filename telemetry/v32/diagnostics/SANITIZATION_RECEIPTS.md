# SANITIZATION RECEIPTS — telemetry/v32/diagnostics

Per-file receipt for the drift-diagnostic lane. `theta` counts exact-literal
redactions of the threshold constant in compliance/theta-note strings; every
redaction is the marker `[REDACTED_PER_PUBLICATION_POLICY]`. Original
SHA-256s are of the pre-scrub bytes of record.

| file | mode | theta redactions | staged bytes | original sha256 |
|---|---|---|---|---|
| `codev6_diagnostic_part1.txt` | byte-for-byte | 0 | 20688 | `4cfb82e67493eef63570b37003adef91f850e21b128a3d328d3d790d15f893ce` |
| `codev6_flank_diagnostic.py` | byte-for-byte | 0 | 5099 | `08598e93dbf0ceae73dc817af758bf9c2710b69c0d9eef8ce2f886c21e993193` |
| `codev6_pathway_ledger.py` | byte-for-byte | 0 | 10578 | `5c0d94e50186f1cfc821b6ead630aba8309d0a0c5e10da1041d36546934f3747` |
| `codev6_pathway_ledger_console.txt` | byte-for-byte | 0 | 8438 | `88967a39ca7ff0f9413fc7af22238a1d2dfe940b159f1627a8552628ad2fb42a` |
| `codev6_viability_check.py` | byte-for-byte | 0 | 14192 | `8eab54adf997a423f23409fb9c8e4c5bf8d06d4fa0f0136a34a00fcea363d458` |
| `codev6_viability_check_console.txt` | byte-for-byte | 0 | 7791 | `40b9028b25c232dd6115c7d7fc32fda6e80f8c2d1bb761ddedadc1c9fc439fb5` |
| `codev7_combined_console_his_run.txt` | sanitized-derivative | 1 | 17622 | `b699cde6720739bde5a622ac025f0088cc20e474f59228f0d6e5343d7aaeb1c7` |
| `codev7_combined_parity_console.txt` | byte-for-byte | 0 | 2782 | `8925d42742c9ffdc46a492a0fdd089822dc472faaece3c99c368777ba6a80602` |
| `codev7_corpus_diagnostic.py` | sanitized-derivative | 2 | 39342 | `136ad1a5e905ff62313c582d28eac575b6bc1e45ab81db35a289304ef3dc725b` |
| `codev7_corpus_diagnostic_console.txt` | byte-for-byte | 0 | 2227 | `777e09399041c7fcff6a4d734f50e82b90bdcf68f8f35bdb14a5bda2fdb32bb7` |
| `codev7_corpus_diagnostic_console_full.txt` | sanitized-derivative | 1 | 7461 | `3b6616786607ea88741818d0c78aa81475e7a0079d01f66c4171a633a0d3cbb8` |
| `rc_3miss_drift_fixture_console.txt` | sanitized-derivative | 1 | 8475 | `a263df0c1d9c6e767858afed403f2aa731566d9d344245ca1ed628ab49e29900` |
| `rc_3miss_drift_fixture_read.py` | sanitized-derivative | 1 | 11008 | `54238f2aadd8c442276214fde9f452e5edde5f0bdccd35d5e1b7b2bbb07f0ab9` |
| `rc_alane_viability_console.txt` | sanitized-derivative | 1 | 23043 | `ccc795a29eca1207873a51e29e7ada84e85654f65d4433044724386acf96df5e` |
| `rc_alane_viability_read.py` | sanitized-derivative | 1 | 42566 | `b3691d84e1a405bd23656b37f5aef726d4101623e374fc03a1db4f979ac8ef4e` |
| `rc_b12_diagnostic.py` | sanitized-derivative | 4 | 62374 | `3e178ab51ccb397e3de1b872f6a18d2c30753e745be285fb25e961b839fecfcc` |
| `rc_b12_diagnostic_console.txt` | sanitized-derivative | 1 | 25310 | `2990871d1b7002f6693b96de81d800d9cb2e64edc1207e8d6da618eef5d54570` |
| `rc_b12_parity_console.txt` | sanitized-derivative | 1 | 6181 | `b8aaa39e7af80b716f66e4af6c4da1d53bcfbb02de913fc8d689d5981880c7bb` |
| `rc_d2sat_diagnostic.py` | sanitized-derivative | 2 | 41280 | `ab3e5d042027f7218acea7e55820e34c2734b6b6984075db00d261afe68e966c` |
| `rc_d2sat_diagnostic_console.txt` | sanitized-derivative | 1 | 22113 | `8572f5059ee8f3a048f7966ecbe2c0716f1251d0abd4c1075ed0d6aa3ec2becc` |
| `rc_d2sat_parity_console.txt` | sanitized-derivative | 1 | 6014 | `dfdccc857f96bcfa551bcb98712cc8413367dfa1b660267c4c7446c41d91b793` |

All sanitized derivatives were re-verified at staging: theta literal absent,
Python derivatives compile post-redaction, byte-for-byte files identical to the
bytes of record. Push-time theta-literal check run on every file.

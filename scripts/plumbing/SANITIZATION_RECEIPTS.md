# Sanitization receipts — scripts/plumbing/

Content-check disposition record for the §3B plumbing tier (my approved verdict list, Nov 6–7, 2026).
Marker: `[REDACTED_PER_PUBLICATION_POLICY]`. The marker replaces only the threshold-constant literal; all
redactions sit in compliance/theta-note banner strings (verified per line). Dropped-lines: 0 (no rule-prose
lines in this tier). Path-trims: none needed (working-root constants are generic sandbox paths, not machine
paths). Rule-bound content: none — all files verified free of detector-side math (content-check verdicts on
record). Every file passed the θ literal check at push time.

## Top level (plumbing tools)

| file | θ redactions | disposition | original SHA-256 | staged chars |
|---|---|---|---|---|
| `banned-token-scan.py` | 0 | as-is (byte-for-byte) | `420abafc5c2ba50e6918dc7c483aa05770e7b3becd05b0d6c0c053d353b0f417` | 2103 |
| `build_arith_fixtures.py` | 0 | as-is (byte-for-byte) | `d6a23fdcbbee71e7035aa552897b2d7bf6ba3d92386b7925a2673c110c7809c2` | 21629 |
| `build_code_fixtures.py` | 0 | as-is (byte-for-byte) | `8864f6d2dca74a6506521a459596d20f7eb46147e813d9a328c0cbf45ae49199` | 56358 |
| `build_p2_manifest.py` | 0 | as-is (byte-for-byte) | `ab67a5454eb6fd02b0173602b583b911e0362f73306bc350c320159dd965bc99` | 33647 |
| `calibrate_triadic_v7.py` | 0 | as-is (byte-for-byte) | `224d112228e37a5623737d101dc7dac6d89ef63460faf09d78b161b4e471cb4b` | 23929 |
| `cd1_arm_a_b0_census_v1.json` | 1 | sanitized derivative | `9c4f01a61735f69005ce2baaca260318d655a8e68a21e0012e156eb560b65a42` | 39875 |
| `cd1_arm_a_cohort_inventory_build_v133.py` | 0 | as-is (byte-for-byte) | `2cd89d392b5e66d5a2b7af2c4d58a287a9533eb2e4125af50aadb8d1f9da9e93` | 181726 |
| `cd1_arm_a_field_map_v1.json` | 0 | as-is (byte-for-byte) | `65776631f49d6f7dd36f7250f4eb409ad87a0235ea36dd6f404de0f1f2b9b7b9` | 8211 |
| `cd1_arm_a_field_map_v1_stamped.json` | 0 | as-is (byte-for-byte) | `61a56000458e028071a93cf0ad12a221f30768c01157aea412c75ccfef03a173` | 9058 |
| `cd1_arm_a_operators_b1.py` | 0 | as-is (byte-for-byte) | `ee603bd989e9e4c437d213ee5243b3f8b3fc0366bb883bdd84d7eb145d980977` | 30653 |
| `cd1_arm_a_separation_run_v108.py` | 0 | as-is (byte-for-byte) | `f09fbd6aca7589f81087dc5d6b2229369a5796d3b5b9af628c4d3465a7cf67a0` | 169810 |
| `stage1_loaders_smoke_v1.py` | 0 | as-is (byte-for-byte) | `02c30f6a06cd00892032a3ea93c014dd2b69c7384d56a038bf3c9153f5c32d52` | 18660 |
| `stage1_loaders_smoke_v1_1.py` | 0 | as-is (byte-for-byte) | `6cd98ddd64a5e1cb4c1075eb8549a5e60ea1aab07c5555a2b8b70ca37d20d38b` | 18010 |
| `telemetry_prose_loader_negative_fixture_runner_v1.py` | 0 | as-is (byte-for-byte) | `db44e6ca95e0f25b044ab65de7032ab6202b65e556604a2fd545912f73dad020` | 7052 |
| `telemetry_prose_loader_negative_fixture_runner_v2.py` | 0 | as-is (byte-for-byte) | `e539a32ae0045226f4eeb65d47561f9b9a075871977ac00da08e035b3bb90241` | 7875 |
| `triadic_chat_thin_extract.py` | 0 | as-is (byte-for-byte) | `d167f203cf3f8e42ae57b7f4aa44e227dcd190c85d794864c201d01c6207e0f8` | 3819 |
| `triadic_checker_offline_pass.py` | 0 | as-is (byte-for-byte) | `c70434ea78fb97ba4601124e835b67fc078fd88399c83427e2f88e2c5ec25ca8` | 22553 |
| `triadic_checker_offline_pass_3b.py` | 0 | as-is (byte-for-byte) | `fa1219d0eaad03f3004af017c730f127f221631954332130148fc200a60c1859` | 23428 |
| `triadic_checker_offline_pass_8b.py` | 0 | as-is (byte-for-byte) | `698a9283e7c56a17f00a857df84972fc41c4b268504aa87773e315c636668f49` | 24767 |
| `triadic_checker_offline_pass_chat.py` | 0 | as-is (byte-for-byte) | `61e1c5039c53ace0dc0d5820195e8895f1b06837cea6437a9f3ce928ab2cdfac` | 23248 |
| `triadic_checker_offline_pass_chat_3b.py` | 0 | as-is (byte-for-byte) | `d21b35f6f71080f72dc0a74d1187d14822db6fa1bdda569986f6823ee9736042` | 23910 |
| `triadic_checker_offline_pass_chat_8b.py` | 0 | as-is (byte-for-byte) | `8fa37e165ed6caad046cea2c52d1ff5356b260f0a713bd03103ad03367646b54` | 25240 |
| `triadic_f2_join.py` | 0 | as-is (byte-for-byte) | `4e779636c39ce8990a3371346295b4db45e093d74f96ec75add73eb111ae10d6` | 8979 |
| `triadic_he164_8b_runaway_kind.py` | 0 | as-is (byte-for-byte) | `a6d9f651745efdc312852c4aa062d02b3c50e6507b473ec9eefb39a46488507c` | 4507 |
| `triadic_he164kc8b_meter_join.py` | 0 | as-is (byte-for-byte) | `e7d3c96964d545ccd5e1c84d5a548c912e771a1f1d3dc7564a74bb77ab2dab35` | 11068 |
| `triadic_rejudge.py` | 0 | as-is (byte-for-byte) | `2e2ab40d435edb803ff1a451d31965bd878d4a0110dcedf5060cd1366008ca7c` | 7274 |
| `triadic_stage1_loaders_v1.py` | 0 | as-is (byte-for-byte) | `f48bd3f46ced97ca91dc7d04b8bd6bb326a7fd7a39d920845f2dd1e2ed33582f` | 23880 |
| `triadic_stage1_loaders_v1_1.py` | 0 | as-is (byte-for-byte) | `8debe6e360da05d0e3ce9d63057566497877998778950f84448028c5c253a8e2` | 14571 |

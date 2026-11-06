# Sanitization Receipts — telemetry/v32/offline-passes (Lane G, §3D results pass)

Published result artifacts of the offline-checker pass program. Files listed with a non-zero
Redactions count are sanitized derivatives: the runtime threshold constant (theta) was redacted
per publication policy; the redaction touches provenance/compliance strings only, never computed
data. Files listed with 0 redactions passed the theta literal scan unchanged and publish byte-for-byte.
Original SHA-256 is the byte-hash of the unredacted artifact of record.

| Published file | Redactions | Original SHA-256 |
| :--- | :--- | :--- |
| triadic_p2rw17_offline_pass_8b_v1.json | 1 | 4e711a58057ba252b66eb27fbb5a17e6fd2cbf8e7070ac3d31b2034c3b5f3e74 |
| triadic_prose17p_offline_pass_v1.json | 1 | 7e1de5aa3b331822bb15e44fa4bda7f118aaa1c4cccf7e942a9c196c664284fa |
| triadic_p2corpus_offline_pass_8b_v1.json | 1 | de55e4839a78e46be6bcae17628c9da2cb64344a65c4396c8f28ffb2691a09c4 |
| triadic_p2corpus_offline_pass_v1.json | 1 | b862e00b3b75fbfe53e77ad364492b8a05b1e3471fee14e071ab34e8052a6a2e |
| triadic_code17c_offline_pass_pc_v1.json | 1 | bf7f561c5f06fd8c9914a163203c9d630bc883612141ce699cc566f7a5f3011a |
| triadic_code17c_offline_pass_kc_v1.json | 1 | ff675f02ab65b60afd325aac3bddb608901892cf6c969ed9123128bcb14a7bb9 |
| triadic_code17c_offline_pass_v1.json | 1 | 61488257764330c46056b2ec6ee026d31b422363838c924c8af45e1c643e9357 |
| checker_passes_3b_build_console.txt | 1 | 076a4a36edb67693215447ff4364c8fc65018965ee9b4cb6841ffcecba0b4146 |
| checker_passes_3b_acceptance_console.txt | 1 | d828c135a29a85ccf741c7f7077072f1b20a941e82eccfe8dc722bdac1c669f9 |
| checker_passes_8b_acceptance_console.txt | 1 | 84090aef0c9f92f729d966679803ad1ac116ca48ec6f6a988f06d3476050d8ca |
| tierc_3b_acceptance_console.txt | 1 | 6546909e6b77e0912a52b84abf91f4ba469bd555f961c07692de33437472eb55 |
| triadic_checker_offline_pass_8b.json | 0 | a61f2bc77134540be5e21cf38f042ab5e2e9c317cbf70e3e95b44f11b099b4e1 |
| triadic_checker_offline_pass_v1.json | 0 | d2a0ca57b5af619bb4b381660bf7180e67285217c706cee6cd8bb2f75cdeabb5 |
| triadic_checker_chat_v1.json | 0 | aad029ccd2a2fc5bb442385ad6a41b4f21f40c235d72186f54a162bccde14b97 |
| triadic_checker_chat_8b.json | 0 | 5ece17f8ae6a35c1249a33fccd317a23592ea76bf2bc7f1107e54593324033b1 |
| triadic_code17c_offline_pass_v1_per_doc.jsonl | 0 | 2ed76fd841c6c1ce0b5a92d0dacc2a42c5f68b5be4c4dcbc3de2e7a67eea1929 |
| triadic_code17c_offline_pass_kc_v1_per_doc.jsonl | 0 | af38103e2aa6ff91c78df0aceb1a90ffec382e96f35f17b1249a34e60f1460ec |
| triadic_code17c_offline_pass_pc_v1_per_doc.jsonl | 0 | ce689fa3cc6bbfc7e3dfbb41125ee3b91af8289afe610a4304a88aab6f776b63 |
| triadic_p2corpus_offline_pass_v1_per_doc.jsonl | 0 | 966fa4da2ad7fd5eba147169f3303b9963a193fa97a67c047b05ee42a07197c9 |
| triadic_p2corpus_offline_pass_8b_v1_per_doc.jsonl | 0 | a31941b24b63936cb4b703daec1f1b816612162dabba40828ff98250c12fa464 |
| triadic_p2rw17_offline_pass_8b_v1_per_doc.jsonl | 0 | ff10fe8528a99ff7d88e0d19d195f8951610d6d4218e668a1b89a4f8a833a614 |
| triadic_prose17p_offline_pass_v1_per_doc.jsonl | 0 | 6309d7f2bea94196b3adbb40420a158a9b0b26c41fec47b3c5340345523c7250 |
| tierc_3b_build_console.txt | 0 | 2b0163bb051399517a070ba2ddec9ac30db3e029852b005d24296cfa75c545c4 |
| p2corpus_8b_pass_console.txt | 0 | ac2ff25a0073e5653887001b852450b5eb1bb56954f8ea62d9f30fa5d0f5353a |
| triadic_p2corpus_offline_pass_console.txt | 0 | 4da5b9cb55c45d97cb0dc8c19c6d06ddd7f98bd8f1205e426c7049daaeef12a2 |
| triadic_checker_offline_pass_8b_console.txt | 0 | aca7117b48f0dbb40e56967ca0bf784630860185e17d6c18b7efa9749b47899f |
| triadic_checker_offline_pass_chat_8b_console.txt | 0 | 23f26fb73afe3818be34bdc8a6470ac9dd74419f66af7655b09e244324550b5a |
| triadic_prose17p_offline_pass_console.txt | 0 | 7b0bb8e5cefdd9db3b23864fc5672ec72808cb4b564fd744870dd673a65dbdc2 |

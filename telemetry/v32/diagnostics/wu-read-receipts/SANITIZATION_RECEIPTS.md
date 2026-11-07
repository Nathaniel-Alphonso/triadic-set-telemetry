# SANITIZATION RECEIPTS — wu-read-receipts

Wu-model read receipts: population-comparability reads against the published
corpora. All three are theta-clean and publish byte-for-byte (no redactions).
The two API-pushed files are single-line compact JSONs; they were pushed via
staged 60,000-character wrapped copies, joined exactly at push time.

| file | mode | staged bytes | sha256 |
|---|---|---|---|
| `triadic_wu_content_read_p2_v1.json` | byte-for-byte | 337343 | `a10e5ce30967503ebd417ad38a43d3652f697fa6264883d295bb84fe98598768` |
| `triadic_wu_prose_read_v1.json` | byte-for-byte | 656143 | `a4e0ef03626a6cd47b926b20bf91358c182df0b16cf3ad5c17e4e316f0d82e3e` |

`triadic_wu_code_read_v1.json` — 26,209,382 B, sha256
`610d48c9689c07c7859fd84fadfe14fdb7259bb8eb572da4e0b9d1ef025db689` —
exceeds the API push ceiling; published by the repo owner via git push
(the Lane F big-cache route). This row is the integrity pointer for that push.

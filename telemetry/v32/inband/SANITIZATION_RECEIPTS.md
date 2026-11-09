# Sanitization Receipts - telemetry/v32/inband (the Stage-1 qualification lane)

Published artifacts of the Stage-1 qualification lane: the four forward-pass
pre-registration sheets, the shared engines module, and the consoles of record
for the hook and mid-walk math instruments. Files listed with a non-zero
Redactions count are sanitized derivatives: the two operating-form literals were
redacted per publication policy (the redaction token is
[REDACTED_PER_PUBLICATION_POLICY]); a small number of measured values that
textually collide with retired form tokens are redacted under the same
mechanical policy. Redactions touch form labels, provenance and compliance
strings, and the colliding data-value tokens; every other measured reading is
kept as banked. The pre-registration sheets additionally carry house-style
normalization beyond literal redaction: internal ledger references replaced
with public phrases, internal shorthand replaced with public vocabulary (the
operating-threshold wiring frame, the walk-bus horizon windows, the
even-numbered and odd-numbered document halves), em-dashes normalized, and
markdown links to unpublished internal sheets replaced with plain-text
mentions. Original SHA-256 is the byte-hash of the unredacted artifact of
record.

The published engines module is a sanitized derivative and does not run
as-is: the redacted constants raise at load. That is the deliberate
publication split of this repository: the calibration perimeters, fixture
builders, and replayable adjudications publish and run; the operating-form
constants and the threshold calculus stay protected. The consoles of record
publish as receipts, not as parseable data: inside-record form labels share
the redaction token.

| Published file | Redactions | Original SHA-256 |
| :--- | :--- | :--- |
| preregistrations/splitter-preregistration.md | 1 | 551667987119ad818a4ef5107537a44f3cad26656899183d94794c69697ae00f |
| preregistrations/accumulator-streaming-preregistration.md | 8 | 136333c1c8cc2a3c861611b02880de81660e3caac298872a86685516518f022e |
| preregistrations/math-midwalk-preregistration.md | 6 | 85ad0cbbf2637a98aca311ce61bf5e513841b26396e22f33e6285ffaea3ec5b9 |
| preregistrations/hook-preregistration.md | 14 | 438bbaf5afdc8cd3572bcb188c48c459498835c638d729080d3d6f3319509710 |
| instruments/triadic_stage1_engines_v1.py | 3 | 79c794c0a850f67212d3ab82f55cc2680451c33c4edc1b1ac8d93d6760af907b |
| receipts/triadic_hook_v1_run_console.txt | 75 | b5087eeea06f86490d4218b2ea1fc3cb2c924d6c290e7dacdaa927625e718634 |
| receipts/triadic_hook_v1_run_console_2.txt | 75 | b5087eeea06f86490d4218b2ea1fc3cb2c924d6c290e7dacdaa927625e718634 |
| receipts/triadic_hook_v1_control_console.txt | 11 | 3a21f2f8583b9b9f2d9d367d25ba4601f464608fecf6f8a8651c546f4db591f3 |
| receipts/mathmid_v1_run_console.txt | 40 | 869df97849d4c752e15573bb8dd2de8f069e0b10dd0b33095855780051784b04 |
| receipts/mathmid_v1_run_console_2.txt | 40 | 869df97849d4c752e15573bb8dd2de8f069e0b10dd0b33095855780051784b04 |
| receipts/mathmid_v1_control_console.txt | 0 | d458dd472388975c280a3e1e0e29e824d12d6ece36b776905cb350443dbebfd4 |

The twice-run pairs publish as two files with one original SHA-256 each: the
two consoles of each pair are byte-identical by the determinism receipt, so the
original hash is the same hash. Files with 0 redactions passed the banned-token
scan unchanged and publish byte-for-byte.

Pending later commits in this lane, each to carry its own row here at its
landing: the five instrument modules and their run instructions (sanitized
derivatives, the same redaction policy, the same do-not-run-as-is note), and
the remaining consoles of record (the splitter control console, the crosswire
pair, the accumulator battery and control consoles, the prose battery and
control consoles, the mathmid selfcheck console, and the hook battery
console), landing as their owner-side copies verify against the banked pins.

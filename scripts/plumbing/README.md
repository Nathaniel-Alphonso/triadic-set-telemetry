# Plumbing tier

This directory holds the measurement and test-method plumbing of the Triadic Set
telemetry program: fixture and corpus builders, cache-thinning and join utilities,
loader smoke tests, offline-checker harnesses, and — under `acceptance_runs/` —
the run scripts that document how each 1B-era test-method acceptance pass was
executed. These files wrap and consume the evaluation instruments; none of them
implements the evaluation itself.

## Publication policy for this tier

Per the program's disclosure ladder, withheld material is named with its count
stated plainly:

- **182 core-instrument source files** are withheld entirely: they embed
  governance constants of the runtime evaluation, which the publication policy
  keeps internal.
- **The stage-1 engine module and the phase-2 integration readout are withheld**
  (2 files): they implement detector-side math, and this tier publishes plumbing
  only.
- **Superseded versions of the two cd1 build tools are withheld** (119 files:
  `cd1_arm_a_separation_run` v1–v107, `cd1_arm_a_cohort_inventory_build`
  v1/v127/v130–v132) in favor of the latest versions of record published here.
- **The phase-4 amend-chain development battery is withheld as
  development-data-only; no runs of record were produced there.** The phase-4
  public record is carried by protocol doc 09 and the phase-4 receipt exports
  under `telemetry/v32/`.

## Redactions in this tier

Twenty files publish as sanitized derivatives: the threshold-constant literal is
redacted to `[REDACTED_PER_PUBLICATION_POLICY]` in compliance/theta-note banner
strings (never in a measured field or operative statement). All other files are
byte-for-byte originals. Original SHA-256 hashes, per-file redaction counts, and
dispositions are recorded in `SANITIZATION_RECEIPTS.md` in this directory and in
`acceptance_runs/`.

## Contents

- **Fixture / corpus builders** — `build_arith_fixtures.py`,
  `build_code_fixtures.py`, `build_p2_manifest.py`
- **Offline checker harnesses** — `triadic_checker_offline_pass*.py` (6):
  standalone, stdlib-only measurement passes over recorded model outputs
- **Stage-1 loader plumbing** — `triadic_stage1_loaders_v1{,_1}.py`,
  `stage1_loaders_smoke_v1{,_1}.py`
- **Negative-fixture runners** — `telemetry_prose_loader_negative_fixture_runner_v1/v2.py`
- **Readout / join utilities** — `triadic_f2_join.py`, `triadic_rejudge.py`,
  `triadic_chat_thin_extract.py`, `triadic_he164kc8b_meter_join.py`,
  `triadic_he164_8b_runaway_kind.py`
- **Calibration harness** — `calibrate_triadic_v7.py` (continues the published
  v1–v3 precedent)
- **cd1 arm-A tooling** — `cd1_arm_a_operators_b1.py`,
  `cd1_arm_a_separation_run_v108.py`, `cd1_arm_a_cohort_inventory_build_v133.py`,
  plus the field-map and B0-census data files
- **Audit helper** — `banned-token-scan.py`
- **`acceptance_runs/`** — 31 acceptance-run scripts of the 1B era: run
  configuration and execution records for the readout, sec-baseline, census,
  builder, thin-extract, exit-verdict, degenerate-view-join, and ap17
  join/capture acceptance passes

# Telemetry — the empirical record

The measured record of the Triadic Set program, organized by phase:

| Directory | Phase | Contents |
|---|---|---|
| `single_stream_archive/` | Phase 1 | Bare-metal single-stream execution traces (Apple Silicon, batch size 1) |
| `single_stream_eval/` | Phase 1 | Phase-1 evaluation readouts |
| `multi_batch_eval/` | Phase 2 | Full multi-batch benchmark logs (57 MMLU tasks + GSM8K) |
| `v32/gate17/`, `v32/offline-passes/`, `v32/rw15/`, `v32/rw16/`, `v32/rw17/`, `v32/exit-verdict/` | Phase 3 | The Test & Evaluation program on 1B, by lane (protocol summaries in `docs/protocols/`) |
| `v32/phase4/` | Phase 4 | Model-scale transfer receipts — 3B complete, 8B record lane ongoing |
| `v32/diagnostics/` | Phase 5 | Environment drift, baselining, and diagnostic receipts |

Every run of record carries SHA-256 integrity receipts; sanitized derivatives carry
the original SHA-256 in each directory's `SANITIZATION_RECEIPTS.md`. See the
repository README for the full program record and current state.

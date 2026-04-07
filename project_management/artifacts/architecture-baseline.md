# Architecture Baseline — Floor

Generated: 2026-04-02
Initial run — no prior baseline.

---

## Module Summary

| File | Layer | Lines | Single Responsibility |
|------|-------|-------|-----------------------|
| `floor/CLAUDE.md` | T0 — Template Entry | 25 | Template session entry point (mirrors CLAUDE.md) |
| `floor/setup.md` | T-Bootstrap | 70 | One-time setup checklist; deleted after setup is complete |
| `floor/project_management/manifest.md` | T1 — Template Orchestration | 28 | Template file index |
| `floor/project_management/status.md` | T1 — Template Orchestration | 28 | Template work tracking |
| `floor/project_management/cdoc.md` | T3 — Template Prompts | 9 | Template cdoc creation instructions |
| `floor/project_management/prompting.md` | T3 — Template Prompts | 33 | Template task prompt composition instructions |
| `floor/project_management/standards/style.md` | T2 — Template Standards | 88 | Template style guide (placeholder-driven) |
| `floor/project_management/standards/architecture.md` | T2 — Template Standards | 96 | Template architecture conventions (placeholder-driven) |
| `floor/project_management/prompts/architecture-check.md` | T3 — Template Prompts | 76 | Template architecture health check prompt |

---

## Diagrams

See `project_management/artifacts/`:

- `01-module-dependency.mermaid` — Module dependency graph (read/write/ref edges)
- `02-layer-hierarchy.mermaid` — Layered architecture (permitted reference directions)
- `03-state-mutation.mermaid` — State mutation flow (which agents mutate which shared state)
- `04-user-task-flow.mermaid` — User task flow sequence (developer workflow end-to-end)

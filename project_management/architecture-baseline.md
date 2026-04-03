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

## Diagram 1 — Module Dependency Graph (Project Meta Layer)

Edges represent read directives (`→ read`), write directives (`→ write`), or routing/conditional references (`→ ref`).

```mermaid
graph TD
    CLAUDE["CLAUDE.md\n[L0]"]
    manifest["manifest.md\n[L1]"]
    status["status.md\n[L1]"]
    baseline["architecture-baseline.md\n[L1]"]
    nodeStyle["standards/style.md\n[L2]"]
    arch_std["standards/architecture.md\n[L2]"]
    cdoc["cdoc.md\n[L3]"]
    prompting["prompting.md\n[L3]"]
    arch_check["prompts/architecture-check.md\n[L3]"]
    floor_system["cdocs/floor-system.md\n[L3]"]

    CLAUDE -->|read| manifest
    CLAUDE -->|read| cdoc
    CLAUDE -->|read| prompting
    CLAUDE -->|read| arch_std

    prompting -->|read| status
    prompting -->|read| cdoc
    prompting -->|ref| nodeStyle
    prompting -->|ref| arch_std
    prompting -->|route| floor_system
    prompting -->|"redirect if counter ≥ 10"| arch_check
    prompting -->|write| manifest

    cdoc -->|write| prompting

    arch_check -->|read| manifest
    arch_check -->|read| arch_std
    arch_check -->|"read/write"| baseline
    arch_check -->|write| status

    arch_std -->|write| manifest
```

---

## Diagram 2 — Layered Architecture

Arrows show the permitted reference direction (downward only; no L2 → L3 allowed).

```mermaid
graph TB
    subgraph L0["Layer 0 — Entry"]
        CLAUDE["CLAUDE.md"]
    end

    subgraph L1["Layer 1 — Orchestration (shared state)"]
        manifest["manifest.md"]
        status["status.md"]
        baseline["architecture-baseline.md"]
    end

    subgraph L2["Layer 2 — Standards"]
        nodeStyle["standards/style.md"]
        arch_std["standards/architecture.md"]
    end

    subgraph L3["Layer 3 — Prompts & Templates"]
        cdoc["cdoc.md"]
        prompting["prompting.md"]
        arch_check["prompts/architecture-check.md"]
        floor_system["cdocs/floor-system.md"]
    end

    L0 -->|"may reference any layer"| L1
    L0 --> L2
    L0 --> L3
    L3 -->|"prompts may reference standards"| L2
    L3 -->|"prompts may read/write state"| L1
    L2 -->|"standards may write state"| L1
```

---

## Diagram 3 — State Mutation Flow

Shows which agents (prompt files) are authorized to mutate each piece of shared state.

```mermaid
flowchart LR
    subgraph state["Shared State"]
        status["status.md
        (task counter, open items)"]
        manifest["manifest.md
        (file index)"]
        prompting_file["prompting.md
        (cdoc routing table)"]
        baseline_file["architecture-baseline.md
        (dependency snapshot)"]
        cdocs_dir["cdocs/
        (context documents)"]
    end

    arch_check["prompts/
    architecture-check.md"]
    prompting_instr["prompting.md
    (completion checklist)"]
    cdoc_instr["cdoc.md
    (post-creation directive)"]
    arch_std["standards/
    architecture.md"]

    arch_check -->|"resets counter to 0"| status
    arch_check -->|"overwrites on PASS"| baseline_file

    prompting_instr -->|"increments counter; removes completed items"| status
    prompting_instr -->|"add/remove rows"| manifest
    prompting_instr -->|"updates on task completion"| cdocs_dir

    cdoc_instr -->|"adds routing row"| prompting_file

    arch_std -->|"directs update when new module added"| manifest
    arch_std -->|"directs update when new module added"| baseline_file
```

---

## Diagram 4 — User Task Flow (Template User Workflow)

Sequence showing a developer who has adopted Floor in their project completing a new task.

```mermaid
sequenceDiagram
    participant U as Developer
    participant C as Claude
    participant PM as prompting.md
    participant ST as status.md
    participant AC as architecture-check.md
    participant CD as cdoc.md
    participant M as manifest.md

    U->>C: Open session / request new task prompt
    C->>PM: read prompting.md
    C->>ST: check Task Counter

    alt Counter < 10 — normal task
        C->>C: select relevant cdocs from routing table
        C->>C: compose task prompt<br/>(manifest read directive, standards refs, cdoc refs)
        C->>U: output task prompt
        Note over U,C: [New session] Task executes
        U->>C: "Task is done"
        C->>ST: remove item&#59; increment counter
        C->>M: add rows for new files&#59; remove rows for deleted files
        C->>CD: read cdoc.md
        C->>C: update relevant cdocs
        C->>U: Remind to git commit
    else Counter ≥ 10 — health check due
        C->>AC: load architecture-check.md
        C->>U: output architecture health check prompt
        Note over U,C: [New session] Health check executes
        C->>ST: reset counter to 0
        C->>M: update architecture-baseline.md entry if new
    end
```
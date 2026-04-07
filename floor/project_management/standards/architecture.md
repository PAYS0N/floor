<!-- Template file. Customize: replace placeholder layer names, module names, and check commands with your project's actual structure. To disable a universal rule, move it to the "Disabled Universal Rules" section at the bottom with a rationale. -->

# Architecture Conventions: [PROJECT NAME]

## Universal Rules

These apply to all projects by default. To disable one, move it to the "Disabled Universal Rules" section at the bottom of this file with a written rationale.

Rules marked *(code)* are primarily applicable to code projects (applications, libraries, scripts). For non-code projects (documentation systems, static sites, data pipelines), evaluate whether they apply during setup and move non-applicable ones to the Disabled section.

- **Single responsibility per module** — Every file/module owns one concern. If you can't describe what it does in one sentence without "and", split it.
- **Dependency direction is inward/downward** — High-level modules do not reference low-level modules. The project-specific layer table below defines what "inward/downward" means for this project.
- **No circular dependencies** — No module may reference a module that (directly or transitively) references it.
- **Explicit references, no implicit coupling** — When a module needs something from another module, it references it explicitly. No shared mutable singletons, no coupling through side channels. *(code)* For code projects: no global mutable state, explicit imports only.
- **Public interfaces have at least one test** *(code)* — Every public function, method, or API endpoint has at least one test exercising it. Internal helpers may be tested indirectly through their callers.
- **No side effects at import time** *(code)* — Importing a module does not trigger behavior. Initialization happens explicitly.
- **Separate I/O from logic** *(code)* — Pure computation should be separable from I/O (file, network, user input). If the agent needs to violate this (e.g. embedded ISR handlers, performance-critical paths), it must note the exception and get confirmation.

---

## Module Hierarchy

Files and components are organized in layers. A module may only reference its own layer or lower layers — never upward.

<!-- Replace the layer names and module names below with your project's actual structure.
     The layer numbers define direction: layer N may only reference layers ≤ N.
     Add or remove layers as needed. The names below are placeholders — choose names
     that describe your project's actual structure.

     Example schemes by project type:
       Software application:  Entry → Orchestrator → Domain → Data → Utility
       Documentation system:  Entry → Index → Content → Templates → Tools
       Scripts-only:          Runner → Coordinator → Core → Utility
       Data pipeline:         Trigger → Pipeline → Transform → Source → Utility
-->

| Layer | Modules | Responsibility |
|-------|---------|----------------|
| 0 — [Entry] | `[entryPoint]` | [Starting point; no logic of its own] |
| 1 — [Orchestration] | `[orchestrator]` | [Wires together or indexes higher-level components; no domain logic] |
| 2 — [Primary] | `[primaryModule]`, `[primaryModule2]` | [Core concern and primary interfaces] |
| 3 — [Secondary] | `[secondaryModule]`, `[secondaryModule2]` | [Supporting components or sub-concerns] |
| 4 — [Utility] | `[utilityModule]` | [Shared helpers with no domain knowledge] |

**Rule: no upward references.** A Layer 3 module must never reference Layer 2 or above. A Layer 2 module must never reference Layer 1 or above. This keeps the dependency graph acyclic.

## Module Responsibilities

Each module owns a single concern. Do not spread a concern across modules or merge concerns into one module.

- **[entryPoint]** — [Starting point. Describe its role.]
- **[orchestrator]** — [Wires or indexes other components. No domain logic.]
- **[primaryModule]** — Owns [describe the concern]. Only place where [key invariant].
- **[secondaryModule]** — [Describe the concern]. No access to [restricted resource].
- **[utilityModule]** — Generic helpers. No domain-specific logic.

## Forbidden Patterns

These are patterns that must not appear in the project. Each includes a check to verify compliance.

<!-- For code projects, checks are typically shell commands (e.g., grep, rg).
     For non-code projects, describe the manual inspection step instead. -->

**F1 — [Pattern name].**
[Description of what is forbidden and why.] Only [list of allowed modules] may [do the thing].

Check: `[your check command]` — should return nothing.

**F2 — [Pattern name].**
[Description of what is forbidden and why.]

Check: `[your check command]` — should return nothing.

**F3 — [Pattern name].**
[Description of what is forbidden and why.]

Check: `[your check command]` — should return nothing.

**F4 — [Pattern name].**
[Description of what is forbidden and why.]

Check: `[your check command]` — should return results only in `[allowed module]`.

**F5 — No circular dependencies.**
Every reference must point downward or sideways within the same layer. No module may reference a module that (directly or transitively) references it.

Check: Review the dependency graph manually or via the architecture health check prompt.

## State / Data Mutation Rules

<!-- Document which modules are allowed to change each piece of shared state.
     For code projects, "mutation" means writes to shared variables or files.
     For non-code projects, "mutation" means any process that changes a document's canonical content. -->

- **[State A]**: changed only in `[module]` (via [mechanism]).
- **[State B]**: changed only via `[mechanism]`, initiated from `[module]`.
- **[State C]**: toggled via `[mechanism]`, initiated from `[module]` via [trigger/event].

## Adding New Modules

When creating a new file or component:
1. Determine its layer in the hierarchy above. If it doesn't fit an existing layer, that's a signal to reconsider the design.
2. Ensure it references only its layer or below.
3. Give it a single clear responsibility that doesn't overlap with existing modules.
4. Update the module hierarchy table in this document.
5. Update `project_management/architecture-baseline.md` with the new dependency.

---

## Disabled Universal Rules

<!-- If you disabled any universal rule during setup, move it here with a rationale. Example:
- **No side effects at import time** — Disabled because [this project uses module-level registration for plugin discovery].
-->

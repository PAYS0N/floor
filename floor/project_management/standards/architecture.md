<!-- Template file. Customize: replace placeholder layer names, module names, and check commands with your project's actual structure. To disable a universal rule, move it to the "Disabled Universal Rules" section at the bottom with a rationale. -->

# Architecture Conventions: [PROJECT NAME]

## Universal Rules

These apply to all projects by default. To disable one, move it to the "Disabled Universal Rules" section at the bottom of this file with a written rationale.

- **Single responsibility per module** — Every file/module owns one concern. If you can't describe what it does in one sentence without "and", split it.
- **Dependency direction is inward/downward** — High-level modules do not import from low-level modules. The project-specific layer table below defines what "inward/downward" means for this codebase.
- **No circular dependencies** — No module may import from a module that (directly or transitively) imports it.
- **Explicit imports, no implicit coupling** — When a module needs something from another module, it imports it explicitly. No global mutable state, no shared mutable singletons, no coupling through side channels.
- **Public interfaces have at least one test** — Every public function, method, or API endpoint has at least one test exercising it. Internal helpers may be tested indirectly through their callers.
- **No side effects at import time** — Importing a module does not trigger behavior. Initialization happens explicitly.
- **Separate I/O from logic** — Pure computation should be separable from I/O (file, network, user input). If the agent needs to violate this (e.g. embedded ISR handlers, performance-critical paths), it must note the exception and get confirmation.

---

## Module Hierarchy

Modules are organized in layers. A module may only import from its own layer or lower layers — never upward.

| Layer | Modules | Responsibility |
|-------|---------|----------------|
| 0 — Entry | `[entryPoint]` | Bootstraps the application; no logic |
| 1 — Orchestrator | `[orchestrator]` | Wires together primary modules; no domain logic |
| 2 — Primary | `[primaryModule]`, `[primaryModule2]` | Core domain logic and primary interfaces |
| 3 — Secondary | `[secondaryModule]`, `[secondaryModule2]` | Supporting data models and sub-components |
| 4 — Utility | `[utilityModule]` | Shared helpers with no domain knowledge |

**Rule: no upward imports.** A Layer 3 module must never import from Layer 2 or above. A Layer 2 module must never import from Layer 1 or above. This keeps the dependency graph acyclic.

## Module Responsibilities

Each module owns a single concern. Do not spread a concern across modules or merge concerns into one module.

- **[entryPoint]** — Bootstraps the application. No business logic.
- **[orchestrator]** — Wires modules together and handles initialization. No domain logic, no display logic.
- **[primaryModule]** — Owns [describe the concern]. Only place where [key invariant].
- **[secondaryModule]** — [Describe the concern]. No access to [restricted resource].
- **[utilityModule]** — Generic helpers. No domain-specific logic.

## Forbidden Patterns

These are patterns that must not appear in the codebase. Each includes a check command to verify compliance.

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
Every import must point downward or sideways within the same layer. No module may import from a module that (directly or transitively) imports it.

Check: Review the import graph manually or via the architecture health check prompt.

## State / Data Mutation Rules

<!-- Document which modules are allowed to mutate each piece of shared state. -->

- **[State A]**: mutated only in `[module]` (via [method or mechanism]).
- **[State B]**: mutated only via `[method]`, called from `[module]`.
- **[State C]**: toggled via `[method]`, called from `[module]` via [callback/event].

## Adding New Modules

When creating a new source file:
1. Determine its layer in the hierarchy above. If it doesn't fit an existing layer, that's a signal to reconsider the design.
2. Ensure it imports only from its layer or below.
3. Give it a single clear responsibility that doesn't overlap with existing modules.
4. Update the module hierarchy table in this document.
5. Update `project_management/architecture-baseline.md` with the new dependency.

---

## Disabled Universal Rules

<!-- If you disabled any universal rule during setup, move it here with a rationale. Example:
- **No side effects at import time** — Disabled because [this project uses module-level registration for plugin discovery].
-->

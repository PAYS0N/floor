# Style Guide: Floor

## Universal Rules

These apply to all projects by default. To disable one, move it to the "Disabled Universal Rules" section at the bottom of this file with a written rationale.

### Code Quality

- **DRY** — If logic appears in more than one place, extract it. If the agent believes duplication is the better path (performance, clarity, decoupling), it must state the tradeoff explicitly and get confirmation before proceeding.
- **No dead code** — Unreachable code, unused imports, and commented-out blocks are removed. Version control is the archive.
- **Fail loudly** — Errors propagate or are handled meaningfully. No empty catch blocks, no silent swallowing, no returning default values that mask failures.
- **Naming carries intent** — Names describe *what* something is or *what* it does, not *how*. No abbreviations that aren't universally understood in the domain.
- **Functions do one thing** — A function that needs "and" in its description is two functions.
- **Minimize scope** — Variables are declared as close to their use as possible, with the narrowest visibility that works.
- **Magic values get named constants** — Literal values that aren't self-evident get a named constant with an explanatory name.

### Process

- **Every commit is buildable** — No partial commits that break the build.
- **Tests pass before commit** — If tests exist, they pass. No "fix the tests later."
- **No dead code in main branch** — Before declaring work complete, confirm nothing unused was left behind.

---

## Language & Tooling

- Languages: Markdown (documentation/templates), Bash (scripts)
- Build command: None yet
- Lint/format command: None yet
- Source directory: `floor/` (template files distributed to new projects)
- Output directory: N/A

## Naming Conventions

- Files: lowercase kebab-case (e.g. `architecture-check.md`)
- Directories: lowercase with underscores for multi-word (e.g. `project_management/`)
- Bash variables: UPPER_SNAKE_CASE for exported/environment, lower_snake_case for local
- Bash functions: lower_snake_case

## Formatting

- Indentation: 2 spaces for Bash scripts, no indentation convention for Markdown
- Markdown headings: ATX-style (`##`), single blank line before and after
- Bash: Opening braces/`then`/`do` on the same line as the statement

## Type Safety

Not applicable — no typed language in use.

## Error Handling

- Bash scripts: Use `set -euo pipefail` at the top of every script
- Validate inputs at the start of scripts; fail with a clear error message

## Prompts & Agent Context

- **Minimum necessary context** — An agent should only be exposed to the files and information it needs for its task. Do not load the entire project into every prompt.
- **Self-contained prompts** — A prompt must either contain all the information the agent needs or explicitly direct the agent to gather it (e.g. "read file X before proceeding"). Never assume the agent has prior context.
- **No implicit knowledge** — If a prompt depends on conventions, definitions, or decisions documented elsewhere, either inline the relevant details or include a read directive. The agent cannot recall what it has not been given.
- **Scope matches task** — The breadth of context given to an agent should be proportional to the task. A focused bug fix gets a narrow slice; an architecture review gets the full standards.

## Build & Lint Gate

- No automated linting or build steps yet. When tooling is added, update this section.
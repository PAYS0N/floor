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

- Languages: Python 3.x (scripts), Markdown (documentation)
- Source directory: `floor/`
- Output: No build output; project is distributed as-is

## Naming Conventions

- Python functions and variables: `snake_case`
- Python classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Markdown files: `kebab-case`
- Scripts: descriptive names, e.g., `shutdown.py`, `check_manifest.py`

## Formatting

- Indentation: 2 spaces (Python and Markdown)
- Line length: soft limit 88 characters (Python), 100 characters (Markdown)
- Two blank lines between top-level Python function/class definitions
- Markdown headers follow content hierarchy (# → ## → ###, no skips)
- Code blocks in Markdown must specify language (e.g., ```python)

## Error Handling

- Errors propagate; no silent swallowing
- Invalid inputs raise descriptive exceptions
- File I/O errors include the file path in the message
- Scripts log errors to stderr and exit with non-zero status on failure

## Build & Lint Gate

- Python scripts must be syntactically correct and executable
- All tests must pass (if applicable to the modified module)
- Markdown files must follow the formatting rules in this guide
- All script imports must be resolvable without errors
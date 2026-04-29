# Style Guide: Floor

## Universal Rules

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

Floor has two kinds of source content: Python scripts (the runtime tools) and Markdown templates (the product content shipped in `floor/`).

- Language: Python 3 (scripts), Markdown (templates, standards, prompts)
- Python interpreter: `python3` (stdlib only — no third-party runtime dependencies)
- Build command: none (no compilation step)
- Lint/format command: none configured — follow the conventions below by hand
- Source directory (product): `floor/`
- Source directory (management scripts): `project_management/scripts/`
- Output directory: none (Floor is a template distribution, not a build artifact)

## Naming Conventions

- Modules and files: snake_case (e.g. `cact_build.py`, `hash_util.py`)
- Functions and local variables: snake_case
- Constants at module top-level: UPPER_SNAKE_CASE (e.g. `CACT_TREE_PATH`, `ARCH_CHECK_THRESHOLD`)
- Classes: PascalCase (rarely used — Floor scripts are mostly function-oriented)
- Private helpers: prefix with single underscore

## Formatting

- Indentation: 2 spaces (matches existing Floor scripts — not the Python community default, but consistent within this codebase)
- Line length: aim for ≤100 chars; break long argparse and string constructions across lines
- Module structure: section banners with `# ── Section name ──` dividers to separate logic/I/O/orchestration layers
- One blank line between functions; two blank lines between section banners and the code they precede
- Docstrings: triple-quoted, first line is a one-sentence summary, further paragraphs explain behavior and return values

## Type Safety

- No static type annotations are used in the current codebase; keep signatures simple and self-documenting through naming.
- If a function accepts multiple shapes, document them in the docstring rather than adding type hints piecemeal.
- Prefer narrow return types (single shape per function) to unions.

## Error Handling

- Raise explicit exceptions with descriptive messages (`raise RuntimeError("claude CLI not found on PATH")`). No silent `return None` where a real error occurred.
- CLI entry points (`main()` functions) catch known exception types, print an `error:` line to stderr, and return a non-zero exit code from the documented table in the module docstring.
- Validate user-facing inputs at the boundary (argparse, file existence); trust internal callers.
- When calling the Claude CLI or other subprocesses, wrap in try/except for `FileNotFoundError`, `subprocess.TimeoutExpired`, and non-zero return codes; surface a clear `RuntimeError`.

## Serialization

- Canonical persistent formats are JSON (`cact_tree.json`, `.floor_session.json`) and plain text (`task_counter.txt`).
- JSON files are written with `indent=2` and a trailing newline.
- Markdown files may carry YAML frontmatter delimited by `---`; parse using `hash_util.parse_frontmatter`.
- Content hashes: SHA-256 hex digests via `hash_util.file_sha256` / `text_sha256`. Directory hashes are derived from the concatenated sorted child hashes.

## Build & Lint Gate

- Floor has no compiler or linter gate. After any change to a Python script, run the affected script end-to-end (e.g. `python3 project_management/scripts/cact_build.py --no-api`) and verify it exits with code 0.
- After any change to a Markdown template in `floor/`, visually confirm the file renders as intended and that placeholders are still clearly marked (e.g. `[PROJECT NAME]`, HTML comments).
- No automated test suite exists; correctness is verified by exercising the scripts against this repo's own `project_management/` tree.

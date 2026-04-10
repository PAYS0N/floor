<!-- Template file. Customize: fill in each project-specific section with your conventions. To disable a universal rule, move it to the "Disabled Universal Rules" section at the bottom with a rationale. -->

# Style Guide: [PROJECT NAME]

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

<!-- Describe the language, compiler/interpreter, build tool, linter/formatter, and output structure. -->

- Language: [e.g. TypeScript, Python, Go]
- Build command: [e.g. `npm run build`]
- Lint/format command: [e.g. `npx biome check src/`]
- Source directory: [e.g. `src/`]
- Output directory: [e.g. `dist/`]

## Naming Conventions

<!-- Document casing and naming rules for each identifier type. -->

- [IdentifierType]: [convention] — e.g. Classes: PascalCase
- [IdentifierType]: [convention] — e.g. Functions and variables: camelCase
- [IdentifierType]: [convention] — e.g. Constants: UPPER_SNAKE_CASE

## Formatting

<!-- Document indentation, line length, brace style, and other formatting rules. -->

- Indentation: [tabs / N spaces]
- [Rule]: [description] — e.g. Opening braces on the same line as the declaration
- [Rule]: [description] — e.g. Single blank line between methods

## Type Safety

<!-- Document how types are used: annotations, inference, type guards, generics, etc. -->

- [Rule]: [description] — e.g. All public method parameters and return types are explicitly annotated
- [Rule]: [description] — e.g. Use type guards before narrowing from unknown

## Error Handling

<!-- Document the error handling strategy: exceptions, result types, propagation, user-facing behavior. -->

- [Rule]: [description] — e.g. Errors propagate to the top level; no silent swallowing
- [Rule]: [description] — e.g. Validate at system boundaries (user input, external APIs) only

## Serialization

<!-- Document the save/load or encode/decode format and conventions. Remove this section if not applicable. -->

- [Rule]: [description] — e.g. All serializable types implement a `toJSON()` method returning a plain object
- [Rule]: [description] — e.g. Deserialization includes explicit type guards before each field assignment

## Build & Lint Gate

<!-- Document what must pass before a change is considered complete. -->

- After any complete code change, run [lint command] and [build command]. Both must pass.
- When the linter or compiler flags an issue, fix the underlying problem — do not suppress or work around it.

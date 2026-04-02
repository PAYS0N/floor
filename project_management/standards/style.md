<!-- Template file. Customize: fill in each section with your project's actual conventions. Replace all placeholder examples with real rules. Remove sections that do not apply; add new sections as needed. -->

# Style Guide: [PROJECT NAME]

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

<!-- Document the save/load or encode/decode format and conventions. -->

- [Rule]: [description] — e.g. All serializable types implement a `toJSON()` method returning a plain object
- [Rule]: [description] — e.g. Deserialization includes explicit type guards before each field assignment

## Build & Lint Gate

<!-- Document what must pass before a change is considered complete. -->

- After any complete code change, run [lint command] and [build command]. Both must pass.
- When the linter or compiler flags an issue, fix the underlying problem — do not suppress or work around it.

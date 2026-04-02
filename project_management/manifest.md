<!-- Template file. Customize: replace the placeholder rows in all sections below "Project Context" with your actual project files. Keep the Project Context section intact — those files exist in every project using this template. -->

# Project Manifest

---

## Project Context

| File | Description |
|------|-------------|
| [CLAUDE.md](../CLAUDE.md) | Project rules and guidelines for Claude and file management |
| [project_management/manifest.md](manifest.md) | This file — full project file listing with descriptions |
| [project_management/status.md](status.md) | Active work, open items, and closed items tracking |
| [project_management/cdoc.md](cdoc.md) | Template instructions for generating context documents |
| [project_management/prompting.md](prompting.md) | Template instructions for generating task prompts |
| [project_management/workflow.md](workflow.md) | Session workflow: how to create and use prompts, when to run the architecture check |
| [project_management/standards/style.md](standards/style.md) | Coding conventions: naming, formatting, error handling, serialization, and build gate |
| [project_management/standards/architecture.md](standards/architecture.md) | Architecture conventions: module hierarchy, responsibilities, forbidden patterns, state mutation rules |
| [project_management/prompts/architecture-check.md](prompts/architecture-check.md) | Periodic health check prompt: map current architecture, run forbidden pattern checks, compare to baseline, produce verdict |

---

## Entry Point

| File | Description |
|------|-------------|
| [src/entryPoint](../src/entryPoint) | Entry point: bootstraps the application on startup |

---

## Source Modules

| File | Description |
|------|-------------|
| [src/orchestrator](../src/orchestrator) | Top-level orchestrator: wires together core modules and handles initialization |
| [src/primaryModule](../src/primaryModule) | Core domain logic: [brief description of what it owns] |
| [src/utilityModule](../src/utilityModule) | Shared utilities: [brief description of helpers provided] |

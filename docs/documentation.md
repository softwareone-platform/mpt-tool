# Documentation

This repository follows the shared documentation standard:

- [standards/documentation.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/documentation.md)

This file documents repository-specific documentation rules only.

## Repository Rules

- `README.md` must stay short and act as the main human entry point.
- `AGENTS.md` must stay operational and tell AI agents which files to read first.
- `docs/usage.md` is the detailed CLI usage guide for package consumers and should not absorb repository-policy content.
- Topic-specific repository guidance must live in the matching file under [`docs/`](.).
- `.github/copilot-instructions.md` must remain a thin adapter that points back to [`AGENTS.md`](../AGENTS.md).
- When CLI behavior, migration workflow, or validation commands change, update the corresponding document in the same change.

## Current Documentation Map

- [`README.md`](../README.md): human entry point, quick start, and documentation map
- [`AGENTS.md`](../AGENTS.md): AI entry point and reading order
- [`architecture.md`](architecture.md): package structure and execution flow
- [`contributing.md`](contributing.md): repository-specific development workflow
- [`testing.md`](testing.md): testing strategy and command mapping
- [`migrations.md`](migrations.md): migration workflow and repository-specific constraints
- [`usage.md`](usage.md): end-user CLI usage guide

## Documentation Change Rule

When documentation changes, prefer updating the smallest relevant document instead of creating overlapping summary files.

# AGENTS.md

Working protocol for any task in this repository:

1. Identify the task type and select only the local repository files that are relevant to that task.
2. Read only those relevant local files before making changes.
3. If any selected local file references shared standards or shared operational guidance that are relevant to the same task, read those shared documents too before proceeding.
4. Treat repository-local documents as repository-specific additions, restrictions, or overrides to shared guidance.
5. If a repository-local rule conflicts with a shared rule, the local repository rule takes precedence.

When applicable, read this repository in the following order:

1. [README.md](README.md) for the repository purpose, quick start, and documentation map.
2. [docs/architecture.md](docs/architecture.md) for the package structure and execution flow.
3. [docs/contributing.md](docs/contributing.md) for repository-specific workflow expectations.
4. [docs/testing.md](docs/testing.md) before changing code or tests.
5. [docs/migrations.md](docs/migrations.md) when a task mentions migration creation, execution, or state tracking.
6. [docs/documentation.md](docs/documentation.md) when changing repository documentation.
7. [docs/usage.md](docs/usage.md) when the task is about end-user CLI usage or package-facing guidance.

Then inspect the code paths relevant to the task:

- [`mpt_tool/cli.py`](mpt_tool/cli.py): Typer entry point and CLI command registration
- [`mpt_tool/commands/`](mpt_tool/commands): command parsing, validation, and command-to-use-case mapping
- [`mpt_tool/use_cases/`](mpt_tool/use_cases): execution flows for init, checks, listing, scaffolding, applying, and migration runs
- [`mpt_tool/migration/`](mpt_tool/migration): base migration types and mixins exposed to migration authors
- [`mpt_tool/managers/state/`](mpt_tool/managers/state): storage backend implementations and factory selection
- [`mpt_tool/services/migration_state.py`](mpt_tool/services/migration_state.py): migration state lifecycle updates
- [`mpt_tool/models.py`](mpt_tool/models.py) and [`mpt_tool/enums.py`](mpt_tool/enums.py): shared domain objects and enums
- [`migrations/`](migrations): generated migration scripts used by the tool
- [`tests/`](tests): pytest coverage by CLI, commands, mixins, services, and use cases
- [`make/`](make): canonical local commands

Operational guidance:

- Prefer documented `make` targets over ad hoc container commands.
- Treat Docker Compose as the default local execution model.
- Keep `README.md` short and navigational.
- Keep repository policy in `docs/` and keep `.github/copilot-instructions.md` thin.
- Keep package-consumer CLI guidance in [`docs/usage.md`](docs/usage.md) instead of expanding `README.md`.
- Do not invent runtime or deployment behavior that is not implemented in the repository.

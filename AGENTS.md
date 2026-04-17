# AGENTS.md

Working protocol for any task in this repository:

1. Identify the task type and select only the local repository files that are relevant to that task.
2. Read only those relevant local files before making changes.
3. If any selected local file references shared standards or shared operational guidance that are relevant to the same task, read those shared documents too before proceeding.
4. Treat repository-local documents as repository-specific additions, restrictions, or overrides to shared guidance.
5. If a repository-local rule conflicts with a shared rule, the local repository rule takes precedence.

When applicable, read the repository in this order:

1. `README.md` for the repository purpose, setup flow, available make targets, and documentation map.
2. `docs/PROJECT_DESCRIPTION.md` for CLI behavior, migration concepts, storage modes, and command usage.
3. `pyproject.toml` for Python version, packaging metadata, dependencies, and lint/test tool configuration.
4. `Makefile` and the relevant files in `make/` for the supported local workflows such as `make check`, `make check-all`, `make test`, and `make format`.
5. The specific implementation files related to the task under `mpt_tool/`:
   - `mpt_tool/cli.py` for CLI entrypoint behavior.
   - `mpt_tool/commands/` for command wiring and command-specific logic.
   - `mpt_tool/use_cases/` for core workflow orchestration.
   - `mpt_tool/services/`, `mpt_tool/managers/`, and `mpt_tool/migration/` for execution, state handling, and migration abstractions.
6. The tests that cover the area you are changing under `tests/`.
7. If the task affects CI, developer workflow, or automation, read the relevant files under `.github/`, `.pre-commit-config.yaml`, and `.coderabbit.yaml`.

Before finishing a change:

1. Run the narrowest relevant checks first.
2. Run `make check-all` when the change affects behavior, shared tooling, or repository-wide developer workflows.

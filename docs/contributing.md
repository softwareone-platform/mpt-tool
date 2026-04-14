# Contributing

This document captures repository-specific contribution guidance.

Shared engineering rules live in `mpt-extension-skills` and should not be duplicated here:

- documentation standard: [documentation.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/documentation.md)
- makefile structure: [makefiles.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/makefiles.md)
- commit message rules: [commit-messages.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/commit-messages.md)
- dependency management: [packages-and-dependencies.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/packages-and-dependencies.md)
- pull request rules: [pull-requests.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/pull-requests.md)
- Python coding conventions: [python-coding.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/python-coding.md)

Shared operational knowledge also applies:

- build and validation flow: [knowledge/build-and-checks.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/build-and-checks.md)
- common make target meanings: [knowledge/make-targets.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)
- migration workflow: [knowledge/migrations.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/migrations.md)

## Development Model

The default development model for this repository is Docker-based.

- Use `make build` to build the local image and install dependencies.
- Use `make run` to open a container with `mpt-service-cli` available.
- Use `make bash` when you need an interactive shell inside the app container.

## Code Organization Expectations

Repository-specific expectations:

- keep CLI flag and command registration changes close to [`mpt_tool/cli.py`](../mpt_tool/cli.py)
- keep command selection and validation logic under [`mpt_tool/commands/`](../mpt_tool/commands)
- keep execution orchestration under [`mpt_tool/use_cases/`](../mpt_tool/use_cases)
- keep migration author APIs under [`mpt_tool/migration/`](../mpt_tool/migration)
- keep storage backend behavior under [`mpt_tool/managers/state/`](../mpt_tool/managers/state)
- keep migration-state persistence rules in [`mpt_tool/services/migration_state.py`](../mpt_tool/services/migration_state.py)
- keep tests under [`tests/`](../tests), next to the affected layer where practical
- update the matching file under [`docs/`](.) when repository behavior changes

## Validation Before Review

Use the repository command entry points before review:

```bash
make check
make test
```

Use `make check-all` when you want the combined workflow.

## Dependency And Packaging Notes

- The package entry point is `mpt-service-cli` from [`pyproject.toml`](../pyproject.toml).
- Runtime and dev dependency changes should be made through the documented `uv`-based workflows exposed by the make targets.
- Keep `docs/usage.md` aligned with user-facing CLI changes when command behavior or usage changes.

## Documentation Changes

Documentation rules live in [documentation.md](documentation.md).

When changing docs, update the smallest relevant file instead of duplicating policy across multiple documents.

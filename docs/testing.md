# Testing

Shared unit-test rules live in [unittests.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/unittests.md).

Shared build and target knowledge also applies:

- [knowledge/build-and-checks.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/build-and-checks.md)
- [knowledge/make-targets.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)

This file documents repository-specific testing behavior.

## Test Scope

The repository currently has stable coverage in these areas:

- CLI parsing and command dispatch in [`tests/cli/`](../tests/cli)
- command implementations and migration base behavior in [`tests/commands/`](../tests/commands)
- migration-state behavior in [`tests/services/`](../tests/services)
- use-case validation flows in [`tests/use_cases/`](../tests/use_cases)

## Commands

Use the repository make targets:

```bash
make test
make check
make check-all
```

Repository command mapping:

- `make test` runs `pytest`
- `make check` runs `ruff format --check`, `ruff check`, `flake8`, `mypy`, and `uv lock --check`
- `make check-all` runs both checks and tests

The CI workflow in [`.github/workflows/pr-build-merge.yml`](../.github/workflows/pr-build-merge.yml) uses the same `make build` and `make check-all` flow.

## Pytest Configuration

Repository-specific test settings come from [`pyproject.toml`](../pyproject.toml):

- tests are discovered under `tests`
- `pythonpath` includes the repository root
- coverage is collected for `mpt_tool`
- tests run with `--import-mode=importlib`

## Writing Tests

Repository-specific guidance:

- add or update tests next to the affected layer instead of creating broad catch-all files
- keep migration fixture data and generated-file examples local to the relevant test module when possible
- prefer mocking external Airtable and MPT API interactions rather than making live network calls
- cover both success and failure state transitions when changing migration execution behavior
- update CLI tests when adding, removing, or changing flags exposed by `mpt-service-cli migrate`

## When Tests Are Required

Add or update tests when a change modifies:

- CLI flag parsing or validation
- command selection
- migration execution flow
- state backend behavior
- migration scaffolding
- migration mixins or external-client integration logic

If a change only affects documentation, tests are not required.

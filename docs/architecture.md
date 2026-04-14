# Architecture

This document describes the repository structure and how `mpt-tool` executes migrations.

## Repository Shape

The repository is a Python package with a CLI entry point and a layered migration runtime:

- [`mpt_tool/cli.py`](../mpt_tool/cli.py) exposes the `mpt-service-cli` Typer application
- [`mpt_tool/commands/`](../mpt_tool/commands) converts validated CLI flags into concrete command objects
- [`mpt_tool/use_cases/`](../mpt_tool/use_cases) implements initialization, validation, listing, scaffolding, and execution flows
- [`mpt_tool/migration/`](../mpt_tool/migration) provides base classes and mixins used inside generated migration files
- [`mpt_tool/managers/`](../mpt_tool/managers) handles migration-file loading plus state backend access
- [`mpt_tool/services/migration_state.py`](../mpt_tool/services/migration_state.py) centralizes migration state updates
- [`migrations/`](../migrations) stores generated schema and data migration scripts

## Execution Flow

The normal execution path is:

1. `mpt-service-cli migrate ...` enters through [`mpt_tool/cli.py`](../mpt_tool/cli.py).
2. `MigrateCommandValidator` validates mutually exclusive flags and argument shape.
3. `CommandFactory` selects a command implementation from [`mpt_tool/commands/`](../mpt_tool/commands).
4. The command delegates to the matching use case in [`mpt_tool/use_cases/`](../mpt_tool/use_cases).
5. Use cases load migration files, choose a state backend, and update migration state before and after execution.

## Migration Model

The tool supports two migration types:

- data migrations through [`mpt_tool/migration/data_base.py`](../mpt_tool/migration/data_base.py)
- schema migrations through [`mpt_tool/migration/schema_base.py`](../mpt_tool/migration/schema_base.py)

Generated migration files live in [`migrations/`](../migrations) and are discovered from the filesystem at runtime. Migration ordering comes from the timestamp prefix embedded in the generated filename.

## State Backends

State storage is selected by [`mpt_tool/managers/state/factory.py`](../mpt_tool/managers/state/factory.py):

- `local` uses [`mpt_tool/managers/state/file.py`](../mpt_tool/managers/state/file.py)
- `airtable` uses [`mpt_tool/managers/state/airtable.py`](../mpt_tool/managers/state/airtable.py)

The backend choice is driven by environment variables from [`mpt_tool/config.py`](../mpt_tool/config.py).

## Main Boundaries

Repository boundaries that matter during implementation:

- CLI parsing belongs in [`mpt_tool/cli.py`](../mpt_tool/cli.py) and the command layer
- migration business flow belongs in [`mpt_tool/use_cases/`](../mpt_tool/use_cases)
- reusable migration author APIs belong in [`mpt_tool/migration/`](../mpt_tool/migration)
- storage-specific logic belongs in [`mpt_tool/managers/state/`](../mpt_tool/managers/state)
- tests should mirror the affected runtime layer under [`tests/`](../tests)

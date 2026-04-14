# Migrations

Shared migration knowledge lives in:

- [knowledge/migrations.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/migrations.md)
- [knowledge/make-targets.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)

This file documents repository-specific migration behavior only.

## Migration Files

Repository migration scripts live in [`migrations/`](../migrations).

The CLI scaffolds timestamp-prefixed files in that directory through:

- `mpt-service-cli migrate --new-data <name>`
- `mpt-service-cli migrate --new-schema <name>`

## Migration Lifecycle

Repository-specific flow:

1. Initialize the tool with `mpt-service-cli migrate --init` when a project has not created its migration state yet.
2. Scaffold a migration file with `--new-data` or `--new-schema`.
3. Implement the generated `Migration` class using the base types from [`mpt_tool/migration/`](../mpt_tool/migration).
4. Validate migration metadata with `mpt-service-cli migrate --check`.
5. Execute migrations with `--data`, `--schema`, or a single migration id argument.

## Repository-Specific Constraints

- Migration ordering is driven by the timestamp prefix generated in the filename.
- The current storage backend is selected through environment variables, not CLI flags.
- Migration execution state is persisted through [`mpt_tool/services/migration_state.py`](../mpt_tool/services/migration_state.py) and the configured state manager backend.
- `mpt-service-cli migrate --manual <migration_id>` marks a migration as applied without executing its `run()` method.
- Changes under [`mpt_tool/migration/mixins/`](../mpt_tool/migration/mixins) can affect migrations authored outside this repository and should be documented carefully.

## Related Code Paths

- [`mpt_tool/use_cases/initialize.py`](../mpt_tool/use_cases/initialize.py)
- [`mpt_tool/use_cases/new_migration.py`](../mpt_tool/use_cases/new_migration.py)
- [`mpt_tool/use_cases/run_migrations.py`](../mpt_tool/use_cases/run_migrations.py)
- [`mpt_tool/use_cases/run_single_migration.py`](../mpt_tool/use_cases/run_single_migration.py)
- [`mpt_tool/use_cases/check_migrations.py`](../mpt_tool/use_cases/check_migrations.py)

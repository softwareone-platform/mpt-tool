# Usage

`mpt-tool` is a command-line utility to scaffold, validate, and execute migrations for MPT extensions.

## Installation

Install the package in the environment where you run migrations:

Choose one:

```bash
pip install mpt-tool
```

```bash
uv add mpt-tool
```

Prerequisites:

- Python 3.12+
- a project directory where migration files can live under `migrations/`
- required environment variables for the storage backend and any mixins you use

## Quick Start

```bash
mpt-service-cli migrate --init
mpt-service-cli migrate --new-data sync_users
mpt-service-cli migrate --data
```

Typical flow:

1. Initialize the migration state.
2. Scaffold a migration file.
3. Implement the generated `Migration` class.
4. Run `mpt-service-cli migrate --check`.
5. Execute pending migrations.

## Environment Variables

Common variables:

- `MPT_API_BASE_URL`: required when a migration uses `MPTAPIClientMixin`
- `MPT_API_TOKEN`: required when a migration uses `MPTAPIClientMixin`
- `MPT_TOOL_STORAGE_TYPE`: migration state backend, `local` or `airtable`; defaults to `local`
- `MPT_TOOL_STORAGE_AIRTABLE_API_KEY`: required for Airtable-backed state or `AirtableAPIClientMixin`
- `MPT_TOOL_STORAGE_AIRTABLE_BASE_ID`: Airtable base id for migration state
- `MPT_TOOL_STORAGE_AIRTABLE_TABLE_NAME`: Airtable table name for migration state
- `SERVICE_VERSION`: optional version persisted into new migration state entries

## Storage Backends

### Local Storage

Local storage writes migration state to `.migrations-state.json` in the project root.

### Airtable Storage

Use Airtable storage when migration state must be shared across environments.

Required variables:

- `MPT_TOOL_STORAGE_AIRTABLE_API_KEY`
- `MPT_TOOL_STORAGE_AIRTABLE_BASE_ID`
- `MPT_TOOL_STORAGE_AIRTABLE_TABLE_NAME`

The Airtable table must contain these columns:

| Column Name | Field Type | Required |
| --- | --- | :---: |
| `order_id` | number | ✅ |
| `migration_id` | singleLineText | ✅ |
| `started_at` | dateTime | ❌ |
| `applied_at` | dateTime | ❌ |
| `type` | singleSelect (`data`, `schema`) | ✅ |
| `version` | singleLineText | ❌ |

## Core Commands

### Initialize

Create the migration folder and initialize state storage:

```bash
mpt-service-cli migrate --init
```

This command creates:

- the `migrations/` folder when it does not exist
- `.migrations-state.json` for local storage
- the configured Airtable table for Airtable storage

If state storage already exists, initialization fails intentionally to avoid accidental data loss.

### Create A Migration

Choose the migration type first:

- data migrations run after a release is deployed and may take longer
- schema migrations run before a release is deployed and should stay fast

Create a migration:

```bash
mpt-service-cli migrate --new-data sync_users
```

```bash
mpt-service-cli migrate --new-schema add_contract_fields
```

Generated files are timestamp-prefixed and stored in `migrations/`, for example `20260113180013_sync_users.py`.

Generated structure:

```python
from mpt_tool.migration import DataBaseMigration


class Migration(DataBaseMigration):
    def run(self):
        pass
```

A schema migration (`--new-schema`) uses `SchemaBaseMigration` instead:

```python
from mpt_tool.migration import SchemaBaseMigration


class Migration(SchemaBaseMigration):
    def run(self):
        pass
```

### Use Mixins

Mixins can provide preconfigured clients inside migration code:

```python
from mpt_tool.migration import DataBaseMigration
from mpt_tool.migration.mixins import AirtableAPIClientMixin, MPTAPIClientMixin


class Migration(DataBaseMigration, MPTAPIClientMixin, AirtableAPIClientMixin):
    def run(self):
        agreement = self.mpt_client.commerce.agreements.get("AGR-1234-5678-9012")
        table = self.airtable_client.table("app_id", "table_name")
        records = table.all()
        self.log.info("Agreement id: %s", agreement.id)
        self.log.info("Processed %s records", len(records))
```

### Check Migrations

Validate the migration directory before execution:

```bash
mpt-service-cli migrate --check
```

This checks migration structure and detects duplicate `migration_id` values.

### Run Migrations

Run all pending data migrations:

```bash
mpt-service-cli migrate --data
```

Run all pending schema migrations:

```bash
mpt-service-cli migrate --schema
```

Run a single migration:

```bash
mpt-service-cli migrate --data MIGRATION_ID
```

```bash
mpt-service-cli migrate --schema MIGRATION_ID
```

Migrations run in timestamp order. Applied migrations are skipped automatically.

### Mark A Migration As Applied

Mark a migration as applied without executing `run()`:

```bash
mpt-service-cli migrate --manual MIGRATION_ID
```

Use the `migration_id` part of the filename, not the timestamp prefix.

### List Migrations

List known migrations and their current state:

```bash
mpt-service-cli migrate --list
```

The output includes execution order, persisted timestamps, status, and the stored `version` value.

### Get Help

```bash
mpt-service-cli --help
mpt-service-cli migrate --help
```

## State Semantics

State is persisted either in `.migrations-state.json` or in Airtable.

If a migration succeeds:

- `started_at` is recorded
- `applied_at` is recorded

If a migration fails:

- `started_at` is recorded
- `applied_at` stays empty
- a later run retries the migration unless you mark it as applied manually

## Troubleshooting

Initialization fails because state already exists:

- this is intentional protection against reinitializing existing state
- delete `.migrations-state.json` or the Airtable table only if you explicitly want to start over

Migrations are not detected:

- ensure files are in `migrations/`
- ensure filenames match `<timestamp>_<migration_id>.py`

Migration execution fails:

- inspect the terminal error output
- fix the `Migration.run()` implementation
- rerun the migration or use `--manual` only when that is operationally correct

Mixin initialization fails:

- verify that all required environment variables are set
- check variable names exactly, including case

Migration is already applied:

- create a new migration instead of modifying an applied one
- only edit persisted state manually if you understand the operational risk

## Good Practices

- run `mpt-service-cli migrate --check` before committing new migration files
- use descriptive snake_case migration names
- never modify a migration that has already been applied in production
- create a new migration to correct an earlier migration
- add the `check-migrations` pre-commit hook if you want migration validation in local hooks

Example `.pre-commit-config.yaml` entry:

```yaml
- repo: https://github.com/softwareone-platform/mpt-tool
  rev: "<tag-or-sha>"
  hooks:
    - id: check-migrations
```

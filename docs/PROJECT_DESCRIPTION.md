# mpt-tool CLI

mpt-tool is a command-line utility to scaffold, run, and audit migrations for MPT extensions.


## Installation

Install with pip or your favorite PyPI package manager:

```bash
  pip install mpt-tool
```

```bash
  uv add mpt-tool
```

## Prerequisites
- Python 3.12+ in your environment
- A `migrations/` folder in your project (it will be created automatically the first time you create a migration)
- Environment variables. See [Environment Variables](#environment-variables) for details.

## Environment Variables

The tool uses the following environment variables:
- `STORAGE_TYPE`: Storage backend for migration state (default: `local`)
  - `local`: Stores state in `.migrations-state.json` in your project root
  - `airtable`: Stores state in an Airtable table (requires additional configuration):
    - `STORAGE_AIRTABLE_APP_ID`: Your Airtable app ID
    - `STORAGE_AIRTABLE_TABLE_NAME`: The name of the table to store migration state
- `MPT_API_KEY`: Your MPT API key (required when using `MPTAPIClientMixin`)
- `AIRTABLE_API_KEY`: Your Airtable API key (required when using `AirtableAPIClientMixin` or when `STORAGE_TYPE=airtable`)


## Quick Start
1. **Install the tool:**
```bash
  pip install mpt-tool
```
2. **Create your first migration:**
```bash
  mpt-tool migrate --new-data sync_users
```
3. **Edit the generated file in the migrations/ folder**
4. **Run all pending migrations**
```bash
  mpt-tool migrate --data
```

## Usage

### Creating a New Migration
1. Decide the migration type (**data** or **schema**).
   - **Data**: run after a release is deployed. Can take hours or days. Executed while MPT is running (e.g., updating product parameters, synchronizing Assets with external data)
   - **Schema**: run before a release is deployed. Must be fast (not more than 15 min). Executed without ensuring the MPT is running (e.g., adding columns in Airtable)
2. Run the appropriate command:
```bash
  # Data migration
  mpt-tool migrate --new-data "migration_name"
```
```bash
  # Schema migration
  mpt-tool migrate --new-schema "migration_name"
```

A new file is created in `migrations/` with a timestamped prefix (e.g., `20260113180013_migration_name.py`) and a prefilled `Command` class.

order_id: timestamp prefix (e.g., `20260113180013`)
migration_id: user-provided name (e.g., `migration_name`)
file: generated file name (e.g., `20260113180013_migration_name.py`)

**Generated file structure:**
```python
from mpt_tool.commands import DataBaseCommand  # or SchemaBaseCommand


class Command(DataBaseCommand):
    def run(self):
        # implement your logic here
        pass
```

#### Using Mixins
You can add mixins to your migration commands to access external services:

```python
from mpt_tool.commands import DataBaseCommand
from mpt_tool.commands.mixins import MPTAPIClientMixin, AirtableAPIClientMixin


class Command(DataBaseCommand, MPTAPIClientMixin, AirtableAPIClientMixin):
    def run(self):
        # Access MPT API
        agreement = self.mpt_client.commerce.agreements.get("AGR-1234-5678-9012")
        self.log.info(f"Agreement id: {agreement.id}")

        # Access Airtable
        table = self.airtable_client.table("app_id", "table_name")
        records = table.all()

        # Use built-in logger
        self.log.info(f"Processed {len(records)} records")
```

### Running Migrations
- **Run all pending data migrations:**
  ```bash
  mpt-tool migrate --data
  ```
- **Run all pending schema migrations:**
  ```bash
  mpt-tool migrate --schema
  ```

Migrations are executed in order based on their order_id (timestamp). The tool automatically:
- Validates the migration folder structure
- Skips migrations that have already been applied (applied_at is not null)
- Tracks execution status in the state storage (`.migrations-state.json` or Airtable table)
- Logs migration progress
- Handles errors gracefully and updates state accordingly

**Migration State File (`.migrations-state.json`):**
```json
{
  "data_example": {
    "migration_id": "data_example",
    "order_id": 20260113180013,
    "started_at": "2026-01-13T18:05:20.000000",
    "applied_at": "2026-01-13T18:05:23.123456",
    "type": "data"
  },
  "schema_example": {
    "migration_id": "schema_example",
    "order_id": 20260214121033,
    "started_at": null,
    "applied_at": null,
    "type": "schema"
  }
}
```
**Migration Table (Airtable):**

| order_id       | migration_id   | started_at                 | applied_at                 | type   |
|----------------|----------------|----------------------------|----------------------------|--------|
| 20260113180013 | data_example   | 2026-01-13T18:05:20.000000 | 2026-01-13T18:05:23.123456 | data   |
| 20260214121033 | schema_example |                            |                            | schema |


If a migration succeeds during execution:
* The started_at timestamp is recorded
* The applied_at timestamp is recorded

If a migration fails during execution:
* The started_at timestamp is recorded
* The applied_at field remains null
* The error is logged
* Later runs will retry the failed migration as applied_at is null, unless `--fake` is used to mark it as applied


### Fake Mode
To mark a migration as applied without running it:

```bash
  mpt-tool migrate --fake MIGRATION_ID
```

Where `MIGRATION_ID` is the filename without `order_id` and `.py` (e.g., `test1`).

**Example:**
- File: `20260113180013_sync_users.py`
- Migration ID: `sync_users`

### Listing Migrations
To see all migrations and their status:

```bash
  mpt-tool migrate --list
```

The output shows execution order, status, and timestamps.

### Getting Help
Run `mpt-tool --help` to see all available commands and options:
```bash
  mpt-tool --help
  mpt-tool migrate --help
```


## Best Practices

### Migration Naming
- Use descriptive, snake_case names (e.g., `add_user_table`, `fix_null_emails`, `sync_agreements_from_api`)
- Keep names concise but meaningful
- Avoid generic names like `migration1`, `fix_bug`, or `update`

### Version Control
- Never modify a migration that has been applied in production
- Create a new migration to fix issues from a previous one


## Troubleshooting

### Common Issues

**Migrations not detected:**
- Ensure files are in the `migrations/` folder
- Verify filename follows the pattern: `<timestamp>_<migration_id>.py` (e.g., `20260121120000_migration_name.py`)

**Migration fails to run:**
- Review the error message in the terminal output
- Check your `Command.run()` implementation for syntax errors
- Fix the issue and re-run the migration or use `--fake` to mark it as applied

**_NOTE:_** There is currently no automatic rollback mechanism. If a migration partially modifies data before failing, you must manually revert those changes or create a new migration to fix the state.

**Mixin errors (ValueError):**
- Verify all required environment variables are set
- Check variable names match exactly (case-sensitive)

**Duplicate migration IDs:**
- The tool prevents duplicate migration IDs automatically
- If you see this error, check for files with the same name in the `migrations/` folder
- Delete or rename the duplicate file

**Migration already applied:**
- If you need to re-run a migration, either:
  - Remove its entry from the state storage (use with caution)
  - Create a new migration with the updated logic
- Never modify an already-applied migration in production


## Development

For development purposes, please, check the Readme in the GitHub repository.

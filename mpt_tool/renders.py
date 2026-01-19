from typing import Any

from rich.table import Table


class MigrationRender:
    """Render the migration state."""

    @classmethod
    def table(cls, migrations_data: dict[str, dict[str, Any]]) -> Table:
        """Render the migration state data in a table."""
        table = Table()
        table.add_column("order_id")
        table.add_column("migration_id")
        table.add_column("started_at")
        table.add_column("applied_at")
        table.add_column("type")
        for key, migration_data in migrations_data.items():
            table.add_row(
                str(migration_data["order_id"]),
                key,
                migration_data.get("started_at"),
                migration_data.get("applied_at"),
                migration_data.get("type"),
            )

        return table

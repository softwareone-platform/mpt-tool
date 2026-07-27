from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

from mpt_tool.models import MigrationListItem


class MigrationRender:
    """Render migration state information as a formatted table."""

    _fields = ("order_id", "migration_id", "started_at", "applied_at", "type", "status", "version")

    def __init__(self, migration_items: list[MigrationListItem]):
        self.migration_items = migration_items

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:  # ruff: ignore[bad-dunder-method-name]
        table = Table(show_lines=True, title_justify="center")
        for field in self._fields:
            table.add_column(field, no_wrap=True, min_width=len(field))

        for migration in self.migration_items:
            table.add_row(
                str(migration.order_id),
                migration.migration_id,
                migration.started_at.isoformat(timespec="seconds") if migration.started_at else "-",
                migration.applied_at.isoformat(timespec="seconds") if migration.applied_at else "-",
                migration.migration_type.value if migration.migration_type else "-",
                migration.status.title(),
                migration.version or "-",
            )

        yield table

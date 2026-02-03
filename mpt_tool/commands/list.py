from typing import override

import typer
from rich.console import Console

from mpt_tool.commands.base import BaseCommand
from mpt_tool.constants import CONSOLE_WIDTH
from mpt_tool.renders import MigrationRender
from mpt_tool.use_cases import ListMigrationsUseCase


class ListCommand(BaseCommand):
    """Lists all migrations."""

    @override
    @property
    def start_message(self) -> str:
        return "Listing migrations..."

    @override
    @property
    def success_message(self) -> str:
        return "Migrations listed successfully."

    @override
    def run(self) -> None:
        migrations = ListMigrationsUseCase().execute()
        if not migrations:
            typer.echo("No migrations found.")
            return

        console = Console(width=CONSOLE_WIDTH)
        console.print(MigrationRender(migration_items=migrations), overflow="fold")

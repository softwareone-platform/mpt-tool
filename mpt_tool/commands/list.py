from typing import override

import typer
from rich.console import Console

from mpt_tool.commands.base import BaseCommand
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
        state_data = ListMigrationsUseCase().execute()
        if not state_data:
            typer.echo("No migrations found.")
            return

        console = Console()
        # TODO: check console render -> https://rich.readthedocs.io/en/stable/protocol.html#console-render
        console.print(MigrationRender.table(state_data), overflow="fold")

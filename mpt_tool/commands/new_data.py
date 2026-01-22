from typing import override

import typer

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.use_cases import NewMigrationUseCase


class NewDataCommand(BaseCommand):
    """Creates a new data migration file with the given id."""

    def __init__(self, migration_id: str) -> None:
        super().__init__()
        self.migration_id = migration_id

    @override
    @property
    def start_message(self) -> str:
        return f"Scaffolding migration: {self.migration_id}."

    @override
    @property
    def success_message(self) -> str:
        return ""

    @override
    def run(self) -> None:
        filename = NewMigrationUseCase().execute(MigrationTypeEnum.DATA, self.migration_id)
        typer.echo(f"Migration file: {filename} has been created.")

from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.use_cases import RunMigrationsUseCase, RunSingleMigrationUseCase


class SchemaCommand(BaseCommand):
    """Runs all schema migrations."""

    def __init__(self, migration_id: str | None = None) -> None:
        self._migration_id = migration_id

    @override
    @property
    def start_message(self) -> str:
        return f"Running {MigrationTypeEnum.SCHEMA} migrations..."

    @override
    @property
    def success_message(self) -> str:
        return f"{MigrationTypeEnum.SCHEMA} migrations applied successfully."

    @override
    def run(self) -> None:
        if self._migration_id:
            RunSingleMigrationUseCase().execute(self._migration_id, MigrationTypeEnum.SCHEMA)
            return

        RunMigrationsUseCase().execute(MigrationTypeEnum.SCHEMA)

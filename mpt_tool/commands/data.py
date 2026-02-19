from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.use_cases import RunMigrationsUseCase, RunSingleMigrationUseCase


class DataCommand(BaseCommand):
    """Runs all data migrations."""

    def __init__(self, migration_id: str | None = None) -> None:
        self._migration_id = migration_id

    @override
    @property
    def start_message(self) -> str:
        return f"Running {MigrationTypeEnum.DATA} migrations..."

    @override
    @property
    def success_message(self) -> str:
        return "Migrations completed successfully."

    @override
    def run(self) -> None:
        if self._migration_id:
            RunSingleMigrationUseCase().execute(self._migration_id, MigrationTypeEnum.DATA)
            return

        RunMigrationsUseCase().execute(MigrationTypeEnum.DATA)

from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.use_cases import RunMigrationsUseCase


class DataCommand(BaseCommand):
    """Runs all data migrations."""

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
        RunMigrationsUseCase().execute(MigrationTypeEnum.DATA)

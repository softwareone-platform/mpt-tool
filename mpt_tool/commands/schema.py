from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.use_cases import RunMigrationsUseCase


class SchemaCommand(BaseCommand):
    """Runs all schema migrations."""

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
        RunMigrationsUseCase().execute(MigrationTypeEnum.SCHEMA)

from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.use_cases import CheckMigrationsUseCase


class CheckCommand(BaseCommand):
    """Checks migrations for duplicate migration_id."""

    @override
    @property
    def start_message(self) -> str:
        return "Checking migrations..."

    @override
    @property
    def success_message(self) -> str:
        return "Migrations check passed successfully."

    @override
    def run(self) -> None:
        CheckMigrationsUseCase().execute()

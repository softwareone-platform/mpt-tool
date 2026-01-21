from typing import override

from mpt_tool.commands.base import BaseCommand
from mpt_tool.use_cases import ApplyMigrationUseCase


class FakeCommand(BaseCommand):
    """Applies a migration without running it."""

    def __init__(self, migration_id: str):
        super().__init__()
        self.migration_id = migration_id

    @override
    @property
    def start_message(self) -> str:
        return f"Running migration {self.migration_id} in fake mode."

    @override
    @property
    def success_message(self) -> str:
        return f"Migration {self.migration_id} applied successfully."

    @override
    def run(self) -> None:
        ApplyMigrationUseCase().execute(migration_id=self.migration_id)

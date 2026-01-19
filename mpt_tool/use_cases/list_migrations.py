import logging
from typing import Any

from mpt_tool.managers import FileMigrationManager, FileStateManager

logger = logging.getLogger(__name__)


class ListMigrationsUseCase:
    """Use case for listing all migrations."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: FileStateManager | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or FileStateManager()

    def execute(self) -> dict[str, dict[str, Any]]:
        """List all migrations."""
        migrations_files = self.file_migration_manager.retrieve_migration_files()
        state_file = self.state_manager.load()
        migration_list_data = {}
        for migration_file in migrations_files:
            try:
                state = state_file[migration_file.migration_id].to_dict()
            except KeyError:
                logger.debug("No state found for migration: %s", migration_file.migration_id)
                state = {}

            state["order_id"] = migration_file.order_id
            migration_list_data[migration_file.migration_id] = state

        # TODO: Create a DTO to represent the migration list and use it
        # between the CLI layer and the Application layer (Use cases)
        return migration_list_data

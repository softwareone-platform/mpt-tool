import logging

from mpt_tool.managers import FileMigrationManager, StateManager, StateManagerFactory
from mpt_tool.models import MigrationListItem

logger = logging.getLogger(__name__)


class ListMigrationsUseCase:
    """Use case for listing all migrations."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: StateManager | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or StateManagerFactory.get_instance()

    def execute(self) -> list[MigrationListItem]:
        """List all migrations sorted by order identifier."""
        migration_files = self.file_migration_manager.retrieve_migration_files()
        migration_states = self.state_manager.load()
        migration_list: list[MigrationListItem] = []
        for migration_file in migration_files:
            migration_state = migration_states.get(migration_file.migration_id)
            if not migration_state:
                logger.debug("No state found for migration: %s", migration_file.migration_id)
            migration_list.append(
                MigrationListItem.from_sources(
                    migration_file=migration_file, migration_state=migration_state
                )
            )

        return sorted(migration_list, key=lambda migration: migration.order_id)

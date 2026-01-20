import logging

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers import FileMigrationManager, FileStateManager
from mpt_tool.managers.errors import LoadMigrationError, MigrationFolderError, StateNotFoundError
from mpt_tool.models import Migration
from mpt_tool.use_cases.errors import RunMigrationError

logger = logging.getLogger(__name__)


class RunMigrationsUseCase:
    """Use case for running migrations."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: FileStateManager | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or FileStateManager()

    def execute(self, migration_type: MigrationTypeEnum) -> None:  # noqa: C901, WPS213, WPS231, WPS238
        """Run all migrations of a given type.

        Args:
            migration_type: The type of migrations to run.

        Raises:
            RunMigrationError: If an error occurs during migration execution.
        """
        try:
            migration_files = self.file_migration_manager.validate()
        except MigrationFolderError as error:
            raise RunMigrationError(str(error)) from error

        for migration_file in migration_files:
            try:
                migration_instance = self.file_migration_manager.load_migration(migration_file)
            except LoadMigrationError as error:
                raise RunMigrationError(str(error)) from error

            if migration_instance.type != migration_type:
                continue

            state = self._get_or_create_state(
                migration_file.migration_id, migration_type, migration_file.order_id
            )
            if state.applied_at is not None:
                logger.debug("Skipping applied migration: %s", migration_file.migration_id)
                continue

            logger.info("Running migration: %s", migration_file.migration_id)
            state.start()
            try:
                migration_instance.run()
            # We catch all exceptions here to ensure the state is updated
            # and the flow is not interrupted abruptly
            except Exception as error:
                state.failed()
                self.state_manager.save_state(state)
                raise RunMigrationError(
                    f"Migration {migration_file.migration_id} failed: {error!s}"
                ) from error

            state.applied()
            self.state_manager.save_state(state)

    def _get_or_create_state(
        self, migration_id: str, migration_type: MigrationTypeEnum, order_id: int
    ) -> Migration:
        try:
            state = self.state_manager.get_by_id(migration_id)
        except StateNotFoundError:
            state = self.state_manager.new(migration_id, migration_type, order_id)

        return state

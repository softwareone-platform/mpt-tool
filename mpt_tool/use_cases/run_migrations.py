import logging

from mpt_tool.enums import MigrationStatusEnum, MigrationTypeEnum
from mpt_tool.managers import FileMigrationManager, StateManager, StateManagerFactory
from mpt_tool.managers.errors import LoadMigrationError, MigrationFolderError
from mpt_tool.migration.base import BaseMigration
from mpt_tool.models import MigrationFile
from mpt_tool.services.migration_state import MigrationStateService
from mpt_tool.use_cases.errors import RunMigrationError

logger = logging.getLogger(__name__)


class RunMigrationsUseCase:
    """Use case for running migrations."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: StateManager | None = None,
        state_service: MigrationStateService | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or StateManagerFactory.get_instance()
        self.state_service = state_service or MigrationStateService(self.state_manager)

    def execute(self, migration_type: MigrationTypeEnum) -> None:  # noqa: WPS231
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
            migration_instance = self._get_migration_instance_by_type(
                migration_file, migration_type
            )
            if migration_instance is None:
                continue

            state = self.state_service.get_or_create_state(
                migration_file.migration_id, migration_type, migration_file.order_id
            )
            if state.applied_at is not None:
                logger.debug("Skipping applied migration: %s", migration_file.migration_id)
                continue

            logger.info("Running migration: %s", migration_file.migration_id)
            self.state_service.save_state(state, status=MigrationStatusEnum.RUNNING)
            try:
                migration_instance.run()
            # We catch all exceptions here to ensure the state is updated
            # and the flow is not interrupted abruptly
            except Exception as error:
                self.state_service.save_state(state, status=MigrationStatusEnum.FAILED)
                raise RunMigrationError(
                    f"Migration {migration_file.migration_id} failed: {error!s}"
                ) from error

            self.state_service.save_state(state, status=MigrationStatusEnum.APPLIED)

    def _get_migration_instance_by_type(
        self, migration_file: MigrationFile, migration_type: MigrationTypeEnum
    ) -> BaseMigration | None:
        try:
            migration_instance = self.file_migration_manager.load_migration(migration_file)
        except LoadMigrationError as error:
            raise RunMigrationError(str(error)) from error

        if migration_instance.type != migration_type:
            return None

        return migration_instance

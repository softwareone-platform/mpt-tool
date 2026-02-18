import logging

from mpt_tool.enums import MigrationStatusEnum, MigrationTypeEnum
from mpt_tool.managers import FileMigrationManager, StateManager, StateManagerFactory
from mpt_tool.managers.errors import LoadMigrationError, MigrationFolderError
from mpt_tool.migration.base import BaseMigration
from mpt_tool.models import MigrationFile
from mpt_tool.services.migration_state import MigrationStateService
from mpt_tool.use_cases.errors import RunMigrationError

logger = logging.getLogger(__name__)


class RunSingleMigrationUseCase:
    """Use case for running a single migration."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: StateManager | None = None,
        state_service: MigrationStateService | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or StateManagerFactory.get_instance()
        self.state_service = state_service or MigrationStateService(self.state_manager)

    def execute(self, migration_id: str, migration_type: MigrationTypeEnum) -> None:
        """Run one migration by id and type.

        Args:
            migration_id: The migration id to run.
            migration_type: The expected migration type.

        Raises:
            RunMigrationError: If an error occurs during migration execution.
        """
        migration_file = self._get_migration_file(migration_id)
        migration_instance = self._get_migration_instance_by_type(migration_file, migration_type)
        state = self.state_service.get_or_create_state(
            migration_file.migration_id, migration_type, migration_file.order_id
        )
        if state.applied_at is not None:
            raise RunMigrationError(f"Migration {migration_id} already applied")

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

    def _get_migration_file(self, migration_id: str) -> MigrationFile:
        try:
            migration_files = self.file_migration_manager.validate()
        except MigrationFolderError as error:
            raise RunMigrationError(str(error)) from error

        migration_file = next(
            (migration for migration in migration_files if migration.migration_id == migration_id),
            None,
        )
        if migration_file is None:
            raise RunMigrationError(f"Migration {migration_id} not found")

        return migration_file

    def _get_migration_instance_by_type(
        self, migration_file: MigrationFile, migration_type: MigrationTypeEnum
    ) -> BaseMigration:
        try:
            migration_instance = self.file_migration_manager.load_migration(migration_file)
        except LoadMigrationError as error:
            raise RunMigrationError(str(error)) from error

        if migration_instance.type != migration_type:
            raise RunMigrationError(
                f"Migration {migration_file.migration_id} is not a {migration_type} migration"
            )

        return migration_instance

from mpt_tool.managers import FileMigrationManager, StateManager, StateManagerFactory
from mpt_tool.managers.errors import MigrationFolderError, StateNotFoundError
from mpt_tool.use_cases.errors import ApplyMigrationError


class ApplyMigrationUseCase:
    """Use case for applying a migration without running it."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: StateManager | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or StateManagerFactory.get_instance()

    def execute(self, migration_id: str) -> None:
        """Apply a migration without running it."""
        try:
            migration_files = self.file_migration_manager.validate()
        except MigrationFolderError as error:
            raise ApplyMigrationError(str(error)) from error

        migration_file = next(
            (migration for migration in migration_files if migration.migration_id == migration_id),
            None,
        )
        if not migration_file:
            raise ApplyMigrationError(f"Migration {migration_id} not found")

        try:
            state = self.state_manager.get_by_id(migration_id)
        except StateNotFoundError:
            # TODO: handle LoadMigrationError exception
            migration = self.file_migration_manager.load_migration(migration_file)
            state = self.state_manager.new(migration_id, migration.type, migration_file.order_id)

        if state.applied_at is not None:
            raise ApplyMigrationError(f"Migration {migration_id} already applied")

        state.manual()
        self.state_manager.save_state(state)

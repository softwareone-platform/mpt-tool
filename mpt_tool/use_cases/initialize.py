from mpt_tool.managers import FileMigrationManager, StateManager
from mpt_tool.managers.errors import InitializationError
from mpt_tool.managers.state.factory import StateManagerFactory
from mpt_tool.use_cases.errors import InitError


class InitializeUseCase:
    """Initialize the migration tool resources."""

    def __init__(
        self,
        file_migration_manager: FileMigrationManager | None = None,
        state_manager: StateManager | None = None,
    ):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()
        self.state_manager = state_manager or StateManagerFactory.get_instance()

    def execute(self) -> None:
        """Execute the initialization.

        Creates:
            - Migration folder
            - State storage

        Raises:
            InitError: If the state storage already exists or cannot be created.
        """
        self.file_migration_manager.new_migration_folder()
        try:
            self.state_manager.initialize()
        except InitializationError as error:
            raise InitError(str(error)) from error

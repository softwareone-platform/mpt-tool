from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers import FileMigrationManager
from mpt_tool.managers.errors import CreateMigrationError
from mpt_tool.use_cases.errors import NewMigrationError


class NewMigrationUseCase:
    """Service to create a new migration file."""

    def __init__(self, file_manager: FileMigrationManager | None = None):
        self.file_manager = file_manager or FileMigrationManager()

    def execute(self, migration_type: MigrationTypeEnum, file_name: str) -> str:
        """Create a new migration file."""
        try:
            migration_file = self.file_manager.new_migration(
                file_suffix=file_name, migration_type=migration_type
            )
        except CreateMigrationError as error:
            raise NewMigrationError(str(error)) from error

        return migration_file.file_name

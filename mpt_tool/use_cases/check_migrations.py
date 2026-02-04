from collections import Counter

from mpt_tool.managers import FileMigrationManager
from mpt_tool.managers.errors import MigrationFolderError
from mpt_tool.use_cases.errors import CheckMigrationError


class CheckMigrationsUseCase:
    """Use case for checking migrations for duplicate migration_id."""

    def __init__(self, file_migration_manager: FileMigrationManager | None = None):
        self.file_migration_manager = file_migration_manager or FileMigrationManager()

    def execute(self) -> None:  # noqa: WPS210
        """Check for duplicate migration_id in migration files.

        Raises:
            CheckMigrationError: If duplicate migration_id is found or a migration folder
                error occurs.
        """
        try:
            migration_files = self.file_migration_manager.retrieve_migration_files()
        except MigrationFolderError as error:
            raise CheckMigrationError(str(error)) from error

        if not migration_files:
            return

        migration_id_counter = Counter(migration.migration_id for migration in migration_files)
        duplicated_migration_ids = [
            migration_id for migration_id, count in migration_id_counter.items() if count > 1
        ]

        if duplicated_migration_ids:
            duplicate_migrations = [
                migration.file_name
                for migration in migration_files
                if migration.migration_id in duplicated_migration_ids
            ]
            migrations_list = ", ".join(duplicate_migrations)
            error_message = f"Duplicate migration_id found in migrations: {migrations_list}"
            raise CheckMigrationError(error_message)

import re
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import cast

from mpt_tool.constants import MIGRATION_FOLDER
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers.errors import CreateMigrationError, LoadMigrationError, MigrationFolderError
from mpt_tool.migration.base import BaseMigration
from mpt_tool.models import MigrationFile
from mpt_tool.templates import MIGRATION_SCAFFOLDING_TEMPLATE


class FileMigrationManager:
    """Manages migration files."""

    _migration_folder: Path = Path(MIGRATION_FOLDER)

    @classmethod
    def load_migration(cls, migration_file: MigrationFile) -> BaseMigration:
        """Loads a migration instance from a migration file.

        Args:
            migration_file: The migration file to load.

        Returns:
            The migration instance.

        Raise:
            LoadMigrationError: If an error occurs during migration loading.
        """
        spec = spec_from_file_location(migration_file.name, migration_file.full_path)
        if spec is None or spec.loader is None:
            raise LoadMigrationError(f"Failed to load migration file: {migration_file.full_path}")

        migration_module = module_from_spec(spec)
        try:
            spec.loader.exec_module(migration_module)
        except ImportError as error:
            raise LoadMigrationError(f"Failed to import migration module: {error!s}") from error

        try:
            migration_instance = cast(BaseMigration, migration_module.Migration())
        except (TypeError, AttributeError) as error:
            raise LoadMigrationError(f"Invalid migration: {error!s}") from error

        return migration_instance

    @classmethod
    def new_migration(cls, file_suffix: str, migration_type: MigrationTypeEnum) -> MigrationFile:
        """Creates a new migration file.

        Args:
            file_suffix: The suffix to use for the migration file name.
            migration_type: The type of migration to create.

        Return:
            The newly created migration file.

        Raises:
            CreateMigrationError: If an error occurs during migration creation.
        """
        cls._migration_folder.mkdir(parents=True, exist_ok=True)
        try:
            migration_file = MigrationFile.new(migration_id=file_suffix, path=cls._migration_folder)
        except ValueError as error:
            raise CreateMigrationError(f"Invalid migration ID: {error}") from error

        try:
            migration_file.full_path.touch(exist_ok=False)
        except FileExistsError as error:
            raise CreateMigrationError(
                f"File already exists: {migration_file.file_name}"
            ) from error

        migration_file.full_path.write_text(
            encoding="utf-8",
            data=MIGRATION_SCAFFOLDING_TEMPLATE.substitute(
                migration_name="DataBaseMigration"
                if migration_type == MigrationTypeEnum.DATA
                else "SchemaBaseMigration"
            ),
        )
        return migration_file

    @classmethod
    def retrieve_migration_files(cls) -> tuple[MigrationFile, ...]:
        """Retrieves all migration files."""
        return cls._get_migration_files()

    @classmethod
    def validate(cls) -> tuple[MigrationFile, ...]:
        """Validates the migration folder and returns a tuple of migration files.

        Returns:
            The validated migration files.

        Raises:
             MigrationFolderError: If an error occurs during migration validation.
        """
        if not cls._migration_folder.exists():
            raise MigrationFolderError(f"Migration folder not found: {cls._migration_folder}")

        migrations = cls._get_migration_files()
        if not migrations:
            raise MigrationFolderError(f"No migration files found in {cls._migration_folder}")

        counter = Counter([migration.migration_id for migration in migrations])
        duplicated_migrations = [element for element, count in counter.items() if count > 1]
        if duplicated_migrations:
            raise MigrationFolderError(
                f"Duplicate migration filename found: {duplicated_migrations[0]}"
            )

        return migrations

    @classmethod
    def _get_migration_files(cls) -> tuple[MigrationFile, ...]:
        try:
            migrations = sorted(
                (
                    MigrationFile.build_from_path(path)
                    for path in cls._migration_folder.glob("*.py")
                    if re.match(r"\d+_.*\.py", path.name)
                ),
                key=lambda migration_file: migration_file.order_id,
            )
        except ValueError as error:
            raise MigrationFolderError(str(error)) from None

        return tuple(migrations)

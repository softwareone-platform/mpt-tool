import json
import re
from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, override

from mpt_tool.constants import MIGRATION_FOLDER, MIGRATION_STATE_FILE
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.errors import (
    CreateMigrationError,
    LoadMigrationError,
    MigrationFolderError,
    StateNotFoundError,
)
from mpt_tool.models import Migration, MigrationFile
from mpt_tool.templates import MIGRATION_SCAFFOLDING_TEMPLATE


class FileMigrationManager:
    """Manages migration files."""

    _migration_folder: Path = Path(MIGRATION_FOLDER)

    @classmethod
    def load_migration(cls, migration_file: MigrationFile) -> ModuleType:
        """Loads a migration module from a migration file.

        Args:
            migration_file: The migration file to load.

        Returns:
            The loaded migration module.
        """
        spec = spec_from_file_location(migration_file.name, migration_file.full_path)
        if spec is None or spec.loader is None:
            raise LoadMigrationError(f"Failed to load migration file: {migration_file.full_path}")

        migration_module = module_from_spec(spec)
        spec.loader.exec_module(migration_module)
        return migration_module

    @classmethod
    def new_migration(cls, file_suffix: str, migration_type: MigrationTypeEnum) -> MigrationFile:
        """Creates a new migration file."""
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
                command_name="DataBaseCommand"
                if migration_type == MigrationTypeEnum.DATA
                else "SchemaBaseCommand"
            ),
        )
        return migration_file

    @classmethod
    def retrieve_migration_files(cls) -> tuple[MigrationFile, ...]:
        """Retrieves all migration files."""
        return cls._get_migration_files()

    @classmethod
    def validate(cls) -> tuple[MigrationFile, ...]:
        """Validates the migration folder and returns a tuple of migration files."""
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


class StateJSONEncoder(json.JSONEncoder):
    """JSON encoder for migration states."""

    @override
    def default(self, obj: object) -> Any:  # noqa: WPS110
        if isinstance(obj, Migration):
            return obj.to_dict()

        return super().default(obj)


class FileStateManager:
    """Manages migration states."""

    _state_path: Path = Path(MIGRATION_STATE_FILE)

    @classmethod
    def load(cls) -> dict[str, Migration]:
        """Load migration states from the state file."""
        if not cls._state_path.exists():
            return {}

        state_data = json.loads(cls._state_path.read_text(encoding="utf-8"))
        return {key: Migration.from_dict(mig_data) for key, mig_data in state_data.items()}

    @classmethod
    def get_by_id(cls, migration_id: str) -> Migration:
        """Get a migration state by its ID."""
        state_data = cls.load()
        try:
            state = state_data[migration_id]
        except KeyError:
            raise StateNotFoundError("State not found") from None

        return state

    @classmethod
    def new(cls, migration_id: str, migration_type: MigrationTypeEnum, order_id: int) -> Migration:
        """Create a new migration state."""
        state_data = cls.load()
        new_state = Migration(
            migration_id=migration_id,
            order_id=order_id,
            type=migration_type,
        )
        state_data[migration_id] = new_state
        cls.save(state_data)
        return new_state

    @classmethod
    def save(cls, state_data: dict[str, Migration]) -> None:
        """Save migration states to the state file."""
        cls._state_path.write_text(
            json.dumps(state_data, indent=2, cls=StateJSONEncoder), encoding="utf-8"
        )

    @classmethod
    def save_state(cls, state: Migration) -> None:
        """Save a migration state to the state file."""
        state_data = cls.load()
        state_data[state.migration_id] = state
        cls.save(state_data)

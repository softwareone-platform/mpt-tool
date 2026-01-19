import json
from pathlib import Path

from mpt_tool.constants import MIGRATION_STATE_FILE
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers.encoders import StateJSONEncoder
from mpt_tool.managers.errors import InvalidStateError, StateNotFoundError
from mpt_tool.models import Migration


class FileStateManager:
    """Manages migration states."""

    _state_path: Path = Path(MIGRATION_STATE_FILE)

    @classmethod
    def load(cls) -> dict[str, Migration]:
        """Load migration states from the state file."""
        if not cls._state_path.exists():
            return {}

        try:
            state_data = json.loads(cls._state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise InvalidStateError(f"Invalid state file: {error!s}") from error

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

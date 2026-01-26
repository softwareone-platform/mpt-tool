import json
from pathlib import Path
from typing import override

from mpt_tool.constants import MIGRATION_STATE_FILE
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers import StateManager
from mpt_tool.managers.encoders import StateJSONEncoder
from mpt_tool.managers.errors import InvalidStateError, StateNotFoundError
from mpt_tool.models import Migration


class FileStateManager(StateManager):
    """Manages file migration states."""

    _state_path: Path = Path(MIGRATION_STATE_FILE)

    @override
    @classmethod
    def load(cls) -> dict[str, Migration]:
        if not cls._state_path.exists():
            return {}

        try:
            state_data = json.loads(cls._state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise InvalidStateError(f"Invalid state file: {error!s}") from error

        return {key: Migration.from_dict(mig_data) for key, mig_data in state_data.items()}

    @override
    @classmethod
    def get_by_id(cls, migration_id: str) -> Migration:
        state_data = cls.load()
        try:
            state = state_data[migration_id]
        except KeyError:
            raise StateNotFoundError("State not found") from None

        return state

    @override
    @classmethod
    def new(cls, migration_id: str, migration_type: MigrationTypeEnum, order_id: int) -> Migration:
        new_state = Migration(
            migration_id=migration_id,
            order_id=order_id,
            type=migration_type,
        )
        cls.save_state(new_state)
        return new_state

    @override
    @classmethod
    def save_state(cls, state: Migration) -> None:
        state_data = cls.load()
        state_data[state.migration_id] = state
        cls._save(state_data)

    @classmethod
    def _save(cls, state_data: dict[str, Migration]) -> None:
        cls._state_path.write_text(
            json.dumps(state_data, indent=2, cls=StateJSONEncoder), encoding="utf-8"
        )

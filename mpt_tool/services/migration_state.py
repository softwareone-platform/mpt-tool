from mpt_tool.enums import MigrationStatusEnum, MigrationTypeEnum
from mpt_tool.managers import StateManager
from mpt_tool.managers.errors import StateNotFoundError
from mpt_tool.models import Migration


class MigrationStateService:
    """Shared migration state operations for migration use cases."""

    def __init__(self, state_manager: StateManager) -> None:
        self._state_manager = state_manager

    def get_or_create_state(
        self, migration_id: str, migration_type: MigrationTypeEnum, order_id: int
    ) -> Migration:
        """Return existing migration state, creating it if needed."""
        try:
            state = self._state_manager.get_by_id(migration_id)
        except StateNotFoundError:
            state = self._state_manager.new(migration_id, migration_type, order_id)

        return state

    def save_state(self, state: Migration, status: MigrationStatusEnum) -> None:
        """Apply status transition and persist migration state."""
        match status:
            case MigrationStatusEnum.APPLIED:
                state.applied()
            case MigrationStatusEnum.FAILED:
                state.failed()
            case MigrationStatusEnum.MANUAL_APPLIED:
                state.manual()
            case MigrationStatusEnum.RUNNING:
                state.start()

        self._state_manager.save_state(state)

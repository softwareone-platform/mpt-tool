from abc import ABC, abstractmethod

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.models import Migration


class StateManager(ABC):
    """Base class for state managers."""

    @classmethod
    @abstractmethod
    def load(cls) -> dict[str, Migration]:
        """Load migration states."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_by_id(cls, migration_id: str) -> Migration:
        """Get a migration state by its ID.

        Args:
            migration_id: The migration ID.

        Raises:
            StateNotFoundError: If the state is not found.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def new(cls, migration_id: str, migration_type: MigrationTypeEnum, order_id: int) -> Migration:
        """Create a new migration state.

        Args:
            migration_id: The migration ID.
            migration_type: The migration type.
            order_id: The order ID.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def save_state(cls, state: Migration) -> None:
        """Save a migration state to the state file.

        Args:
            state: The migration state.
        """
        raise NotImplementedError

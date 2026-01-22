from enum import StrEnum

from mpt_tool.config import get_storage_type
from mpt_tool.managers import StateManager
from mpt_tool.managers.state.airtable import AirtableStateManager
from mpt_tool.managers.state.file import FileStateManager


class StorageTypeEnum(StrEnum):
    """Enum for storage types."""

    LOCAL = "local"
    AIRTABLE = "airtable"


class StateManagerFactory:
    """Factory to create StateManager instances."""

    @classmethod
    def get_instance(cls) -> StateManager:
        """Return a StateManager instance based on environment variables.

        Returns:
            StateManager instance (FileStateManager or AirtableStateManager)

        """
        storage_type = get_storage_type()
        return (
            AirtableStateManager()
            if storage_type == StorageTypeEnum.AIRTABLE
            else FileStateManager()
        )

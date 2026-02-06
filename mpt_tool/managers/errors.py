from mpt_tool.errors import BaseError


class ManagerError(BaseError):
    """Base error for all manager errors."""


class CreateMigrationError(ManagerError):
    """Error creating the migration file."""


class InitializationError(ManagerError):
    """Error during initialization."""


class InvalidStateError(ManagerError):
    """Error loading invalid state."""


class LoadMigrationError(ManagerError):
    """Error loading migrations."""


class MigrationFolderError(ManagerError):
    """Error accessing migrations folder."""


class StateNotFoundError(ManagerError):
    """Error getting state from state file."""

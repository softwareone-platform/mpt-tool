from typing import override


class BaseError(Exception):
    """Base error."""

    @override
    def __init__(self, message: str):
        super().__init__(message)


class LoadMigrationError(BaseError):
    """Error loading migrations."""


class MigrationFolderError(BaseError):
    """Error accessing migrations folder."""


class RunMigrationError(BaseError):
    """Error running migrations."""


class StateNotFoundError(BaseError):
    """Error getting state from state file."""

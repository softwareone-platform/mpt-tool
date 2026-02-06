from mpt_tool.errors import BaseError


class UseCaseError(BaseError):
    """Base error for use cases."""


class ApplyMigrationError(UseCaseError):
    """Error applying migration."""


class CheckMigrationError(UseCaseError):
    """Error checking migrations."""


class InitError(UseCaseError):
    """Error initializing tool."""


class NewMigrationError(UseCaseError):
    """Error creating new migration."""


class RunMigrationError(UseCaseError):
    """Error running migration."""

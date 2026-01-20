from mpt_tool.errors import BaseError


class UseCaseError(BaseError):
    """Base error for use cases."""


class NewMigrationError(UseCaseError):
    """Error creating new migration."""


class RunMigrationError(UseCaseError):
    """Error running migration."""


class ApplyMigrationError(UseCaseError):
    """Error applying migration."""

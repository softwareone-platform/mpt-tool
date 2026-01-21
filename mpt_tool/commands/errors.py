from mpt_tool.errors import BaseError


class BadParameterError(BaseError):
    """Bad parameter error."""


class CommandNotFoundError(BaseError):
    """Command not found error."""

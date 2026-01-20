from typing import override


class BaseError(Exception):
    """Base error."""

    @override
    def __init__(self, message: str):
        super().__init__(message)

from abc import ABC, abstractmethod

from mpt_tool.commands.enums import MigrationTypeEnum


class BaseCommand(ABC):
    """Abstract base class for all migration commands."""

    @abstractmethod
    def run(self) -> None:
        """Executes the command."""
        raise NotImplementedError


class DataBaseCommand(BaseCommand, ABC):
    """Base command for data migrations."""

    _type = MigrationTypeEnum.DATA


class SchemaBaseCommand(BaseCommand, ABC):
    """Base command for schema migrations."""

    _type = MigrationTypeEnum.SCHEMA

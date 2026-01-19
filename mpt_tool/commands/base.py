import logging
from abc import ABC, abstractmethod

from mpt_tool.enums import MigrationTypeEnum

logger = logging.getLogger(__name__)


class BaseCommand(ABC):
    """Abstract base class for all migration commands."""

    _type: MigrationTypeEnum

    def __init__(self) -> None:
        self.log = logger

    @property
    def type(self) -> MigrationTypeEnum:
        """The type of migration this command represents."""
        return self._type

    @abstractmethod
    def run(self) -> None:
        """Executes the command."""
        raise NotImplementedError

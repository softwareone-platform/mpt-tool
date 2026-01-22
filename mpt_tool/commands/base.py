from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Base class for migration commands."""

    @property
    def name(self) -> str:
        """The name of the command, used for CLI argument parsing."""
        return self.__class__.__name__.replace("Command", "").lower()

    @property
    @abstractmethod
    def start_message(self) -> str:
        """Message to display before starting the migration."""
        raise NotImplementedError

    @property
    @abstractmethod
    def success_message(self) -> str:
        """Message to display after the migration has finished."""
        raise NotImplementedError

    @abstractmethod
    def run(self) -> None:
        """Executes the migration."""
        raise NotImplementedError

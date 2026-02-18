from typing import cast

from mpt_tool.commands.base import (
    BaseCommand,
)
from mpt_tool.commands.check import CheckCommand
from mpt_tool.commands.data import DataCommand
from mpt_tool.commands.errors import CommandNotFoundError
from mpt_tool.commands.init import InitCommand
from mpt_tool.commands.list import ListCommand
from mpt_tool.commands.manual import ManualCommand
from mpt_tool.commands.new_data import NewDataCommand
from mpt_tool.commands.new_schema import NewSchemaCommand
from mpt_tool.commands.schema import SchemaCommand


class CommandFactory:
    """Command factory to create the correct command."""

    @classmethod
    def get_instance(cls, param_data: dict[str, bool | str | None]) -> BaseCommand:  # noqa: C901, WPS212
        """Get the correct command instance based on the parameter data.

        Args:
            param_data: The parameter data.

        Return:
            The command instance.

        Raises:
            CommandNotFoundError: If no command is found.
        """
        match param_data:  # noqa: WPS242
            case {"init": True}:
                return InitCommand()
            case {"check": True}:
                return CheckCommand()
            case {"data": True, "migration_id": migration_id}:
                return DataCommand(migration_id=cast(str | None, migration_id))
            case {"schema": True, "migration_id": migration_id}:
                return SchemaCommand(migration_id=cast(str | None, migration_id))
            case {"manual": manual_value} if manual_value is not None:
                return ManualCommand(migration_id=cast(str, manual_value))
            case {"new_schema": new_schema_value} if new_schema_value is not None:
                return NewSchemaCommand(migration_id=cast(str, new_schema_value))
            case {"new_data": new_data_value} if new_data_value is not None:
                return NewDataCommand(migration_id=cast(str, new_data_value))
            case {"list": True}:
                return ListCommand()
            case _:
                raise CommandNotFoundError("Command not found.")

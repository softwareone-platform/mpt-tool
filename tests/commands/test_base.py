from typing import override

from mpt_tool.commands.base import DataBaseCommand, SchemaBaseCommand
from mpt_tool.commands.enums import MigrationTypeEnum


class FakeDataBaseCommand(DataBaseCommand):
    @override
    def run(self):
        """Do something."""


class FakeSchemaBaseCommand(SchemaBaseCommand):
    @override
    def run(self):
        """Do something."""


def test_data_base_command_type():
    command = FakeDataBaseCommand()

    result = command._type  # noqa: SLF001

    assert result == MigrationTypeEnum.DATA


def test_schema_base_command_type():
    command = FakeSchemaBaseCommand()

    result = command._type  # noqa: SLF001

    assert result == MigrationTypeEnum.SCHEMA

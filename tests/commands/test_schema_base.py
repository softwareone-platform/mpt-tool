from typing import override

from mpt_tool.commands import SchemaBaseCommand
from mpt_tool.enums import MigrationTypeEnum


class FakeSchemaBaseCommand(SchemaBaseCommand):
    @override
    def run(self):
        """Do something."""


def test_schema_base_command_type():
    command = FakeSchemaBaseCommand()

    result = command.type

    assert result == MigrationTypeEnum.SCHEMA

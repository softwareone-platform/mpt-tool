from typing import override

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.migration import SchemaBaseMigration


class FakeSchemaMigration(SchemaBaseMigration):
    @override
    def run(self):
        """Do something."""


def test_schema_base_command_type():
    command = FakeSchemaMigration()

    result = command.type

    assert result == MigrationTypeEnum.SCHEMA

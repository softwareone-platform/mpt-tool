from typing import override

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.migration import DataBaseMigration


class FakeDataMigration(DataBaseMigration):
    @override
    def run(self):
        """Do something."""


def test_data_base_command_type():
    command = FakeDataMigration()

    result = command.type

    assert result == MigrationTypeEnum.DATA

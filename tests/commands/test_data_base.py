from typing import override

from mpt_tool.commands import DataBaseCommand
from mpt_tool.enums import MigrationTypeEnum


class FakeDataBaseCommand(DataBaseCommand):
    @override
    def run(self):
        """Do something."""


def test_data_base_command_type():
    command = FakeDataBaseCommand()

    result = command.type

    assert result == MigrationTypeEnum.DATA

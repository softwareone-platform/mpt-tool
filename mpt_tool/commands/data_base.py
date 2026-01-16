from abc import ABC

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum


class DataBaseCommand(BaseCommand, ABC):
    """Base command for data migrations."""

    _type = MigrationTypeEnum.DATA

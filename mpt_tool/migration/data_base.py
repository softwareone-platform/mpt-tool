from abc import ABC

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.migration.base import BaseMigration


class DataBaseMigration(BaseMigration, ABC):
    """Base command for data migrations."""

    _type = MigrationTypeEnum.DATA

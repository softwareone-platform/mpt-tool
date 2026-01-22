from abc import ABC

from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.migration.base import BaseMigration


class SchemaBaseMigration(BaseMigration, ABC):
    """Base command for schema migrations."""

    _type = MigrationTypeEnum.SCHEMA

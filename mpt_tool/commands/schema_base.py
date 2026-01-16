from abc import ABC

from mpt_tool.commands.base import BaseCommand
from mpt_tool.enums import MigrationTypeEnum


class SchemaBaseCommand(BaseCommand, ABC):
    """Base command for schema migrations."""

    _type = MigrationTypeEnum.SCHEMA

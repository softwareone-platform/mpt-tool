from enum import StrEnum


class MigrationTypeEnum(StrEnum):
    """Enumeration of migration types.

    Attributes:
        DATA: Represents a data migration.
        SCHEMA: Represents a schema migration.
    """

    DATA = "data"
    SCHEMA = "schema"

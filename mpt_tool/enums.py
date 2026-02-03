from enum import StrEnum
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from mpt_tool.models import Migration


class MigrationStatusEnum(StrEnum):
    """Enumeration of migration status values."""

    RUNNING = "running"
    FAILED = "failed"
    FAKE_APPLY = "faked"
    APPLIED = "applied"
    NOT_APPLIED = "not applied"

    @classmethod
    def from_state(cls, migration_state: "Migration | None") -> Self:
        """Calculate migration status based on migration state."""
        if migration_state is None:
            return cls.NOT_APPLIED
        if migration_state.started_at and migration_state.applied_at:
            return cls.APPLIED
        if migration_state.started_at and not migration_state.applied_at:
            return cls.RUNNING
        if not migration_state.started_at and migration_state.applied_at:
            return cls.FAKE_APPLY

        return cls.FAILED


class MigrationTypeEnum(StrEnum):
    """Enumeration of migration types.

    Attributes:
        DATA: Represents a data migration.
        SCHEMA: Represents a schema migration.
    """

    DATA = "data"
    SCHEMA = "schema"

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Self

from mpt_tool.constants import MAX_LEN_MIGRATION_ID
from mpt_tool.enums import MigrationTypeEnum


@dataclass
class Migration:
    """Represents a migration."""

    migration_id: str
    order_id: int
    type: MigrationTypeEnum
    started_at: dt.datetime | None = None
    applied_at: dt.datetime | None = None

    @classmethod
    def from_dict(cls, migration_data: dict[str, Any]) -> Self:
        """Create a migration from a dictionary."""
        return cls(
            migration_id=migration_data["migration_id"],
            order_id=migration_data["order_id"],
            type=MigrationTypeEnum(migration_data["type"]),
            started_at=dt.datetime.fromisoformat(migration_data["started_at"])
            if migration_data["started_at"]
            else None,
            applied_at=dt.datetime.fromisoformat(migration_data["applied_at"])
            if migration_data["applied_at"]
            else None,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert a migration to a dictionary."""
        return {
            "migration_id": self.migration_id,
            "order_id": self.order_id,
            "type": self.type.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
        }

    def applied(self) -> None:
        """Mark the migration as applied."""
        self.applied_at = dt.datetime.now(tz=dt.UTC)

    def failed(self) -> None:
        """Mark the migration as failed."""
        self.started_at = None
        self.applied_at = None

    def fake(self) -> None:
        """Mark the migration as fake."""
        self.started_at = None
        self.applied_at = dt.datetime.now(tz=dt.UTC)

    def start(self) -> None:
        """Mark the migration as started."""
        self.started_at = dt.datetime.now(tz=dt.UTC)


@dataclass
class MigrationFile:
    """Represents a migration file with its identifier and order."""

    full_path: Path
    migration_id: str
    order_id: int

    @property
    def file_name(self) -> str:
        """Migration file name."""
        return f"{self.order_id}_{self.migration_id}.py"

    def __post_init__(self) -> None:
        if len(self.migration_id) >= MAX_LEN_MIGRATION_ID:
            raise ValueError(
                f"Migration ID must be less than {MAX_LEN_MIGRATION_ID} characters long."
            )
        if not self.migration_id.isidentifier():
            raise ValueError(
                "Migration ID must contain only alphanumeric letters and numbers, or underscores."
            )

    @property
    def name(self) -> str:
        """Migration file name."""
        return f"{self.order_id}_{self.migration_id}"

    @classmethod
    def build_from_path(cls, path: Path) -> Self:
        """Build a migration file from a path.

        Args:
            path: The path to the migration file.
        """
        order_id, migration_id = path.stem.split("_", maxsplit=1)
        return cls(full_path=path, order_id=int(order_id), migration_id=migration_id)

    @classmethod
    def new(cls, migration_id: str, path: Path) -> Self:
        """Create a new migration file.

        Args:
            migration_id: The migration ID.
            path: The path to the migration folder.
        """
        timestamp = dt.datetime.now(tz=dt.UTC).strftime("%Y%m%d%H%M%S")
        full_path = path / f"{timestamp}_{migration_id}.py"
        return cls(full_path=full_path, migration_id=migration_id, order_id=int(timestamp))

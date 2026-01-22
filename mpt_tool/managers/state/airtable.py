from typing import override

from pyairtable.formulas import match
from pyairtable.orm import Model, fields

from mpt_tool.config import get_airtable_config
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers import StateManager
from mpt_tool.managers.errors import StateNotFoundError
from mpt_tool.models import Migration


class MigrationStateModel(Model):
    """Airtable model for migration states."""

    migration_id = fields.RequiredTextField("migration_id")
    order_id = fields.RequiredIntegerField("order_id")
    type = fields.RequiredSelectField("type")
    started_at = fields.DatetimeField("started_at")
    applied_at = fields.DatetimeField("applied_at")

    class Meta:
        @staticmethod
        def api_key() -> str | None:  # noqa: WPS602
            """Airtable API key."""
            return get_airtable_config("api_key")

        @staticmethod
        def base_id() -> str | None:  # noqa: WPS602
            """Airtable base ID."""
            return get_airtable_config("base_id")

        @staticmethod
        def table_name() -> str | None:  # noqa: WPS602
            """Airtable table name."""
            return get_airtable_config("table_name")


class AirtableStateManager(StateManager):
    """Manages migration states in Airtable."""

    @override
    @classmethod
    def load(cls) -> dict[str, Migration]:
        migrations = {}
        for state in MigrationStateModel.all():
            migration = Migration(
                migration_id=state.migration_id,
                order_id=state.order_id,
                type=MigrationTypeEnum(state.type),
                started_at=state.started_at,
                applied_at=state.applied_at,
            )
            migrations[migration.migration_id] = migration

        return migrations

    @override
    @classmethod
    def get_by_id(cls, migration_id: str) -> Migration:
        state = MigrationStateModel.first(formula=match({"migration_id": migration_id}))
        if not state:
            raise StateNotFoundError(f"State {migration_id} not found")

        return Migration(
            migration_id=state.migration_id,
            order_id=state.order_id,
            type=MigrationTypeEnum(state.type),
            started_at=state.started_at,
            applied_at=state.applied_at,
        )

    @override
    @classmethod
    def new(cls, migration_id: str, migration_type: MigrationTypeEnum, order_id: int) -> Migration:
        state = MigrationStateModel(
            migration_id=migration_id, order_id=order_id, type=migration_type.value
        )
        state.save()
        return Migration(
            migration_id=state.migration_id,
            order_id=state.order_id,
            type=MigrationTypeEnum(state.type),
            started_at=state.started_at,
            applied_at=state.applied_at,
        )

    @override
    @classmethod
    def save_state(cls, state: Migration) -> None:
        migration_state_model = MigrationStateModel.first(
            formula=f"migration_id = '{state.migration_id}'"
        )
        if migration_state_model:
            migration_state_model.order_id = state.order_id
            migration_state_model.type = state.type.value
            migration_state_model.started_at = state.started_at
            migration_state_model.applied_at = state.applied_at
        else:
            migration_state_model = MigrationStateModel(
                migration_id=state.migration_id,
                order_id=state.order_id,
                type=state.type.value,
                started_at=state.started_at,
                applied_at=state.applied_at,
            )

        migration_state_model.save()

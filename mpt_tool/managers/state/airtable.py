from typing import Any, override

from pyairtable import Api
from pyairtable.formulas import match
from pyairtable.orm import Model, fields
from requests import HTTPError

from mpt_tool.config import get_airtable_config
from mpt_tool.enums import MigrationTypeEnum
from mpt_tool.managers import StateManager
from mpt_tool.managers.errors import InitializationError, StateNotFoundError
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
    def exists(cls) -> bool:
        try:
            MigrationStateModel.meta.table.schema()
        except HTTPError:
            return False

        return True

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
    def initialize(cls) -> None:
        api_key = get_airtable_config("api_key")
        base_id = get_airtable_config("base_id")
        table_name = get_airtable_config("table_name")
        if not api_key or not base_id or not table_name:
            raise InitializationError(
                "Airtable configuration missing. Please set MPT_TOOL_STORAGE_AIRTABLE_API_KEY, "
                "MPT_TOOL_STORAGE_AIRTABLE_BASE_ID, and MPT_TOOL_STORAGE_AIRTABLE_TABLE_NAME."
            )

        base = Api(api_key).base(base_id)
        table_fields: list[dict[str, Any]] = [
            {"name": "migration_id", "type": "singleLineText"},
            {"name": "order_id", "type": "number", "options": {"precision": 0}},
            {
                "name": "type",
                "type": "singleSelect",
                "options": {"choices": [{"name": "data"}, {"name": "schema"}]},
            },
            {
                "name": "started_at",
                "type": "dateTime",
                "options": {
                    "dateFormat": {"name": "iso"},
                    "timeFormat": {"name": "24hour"},
                    "timeZone": "utc",
                },
            },
            {
                "name": "applied_at",
                "type": "dateTime",
                "options": {
                    "dateFormat": {"name": "iso"},
                    "timeFormat": {"name": "24hour"},
                    "timeZone": "utc",
                },
            },
        ]
        try:
            base.create_table(table_name, fields=table_fields)
        except HTTPError as error:
            raise InitializationError(str(error)) from error

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

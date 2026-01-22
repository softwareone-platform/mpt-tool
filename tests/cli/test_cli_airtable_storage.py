import pytest
from freezegun import freeze_time
from pyairtable.testing import MockAirtable

from mpt_tool.cli import app


@pytest.fixture(autouse=True)
def set_airtable_env_vars(monkeypatch):
    monkeypatch.setenv("STORAGE_TYPE", "airtable")
    monkeypatch.setenv("AIRTABLE_API_KEY", "fake_api_key")
    monkeypatch.setenv("STORAGE_AIRTABLE_BASE_ID", "fake_base_id")
    monkeypatch.setenv("STORAGE_AIRTABLE_TABLE_NAME", "fake_table_name")


@pytest.fixture
def mock_airtable():
    with MockAirtable() as mock:
        yield mock


@pytest.fixture
def applied_migration(data_migration_file, mock_airtable):
    mock_airtable.add_records(
        "fake_base_id",
        "fake_table_name",
        [
            {
                "migration_id": "fake_data_file_name",
                "order_id": 20250406020202,
                "type": "data",
                "started_at": "2025-04-06T13:00:00+00:00",
                "applied_at": "2025-04-06T13:00:00+00:00",
            }
        ],
    )

    return data_migration_file


@freeze_time("2025-04-06 13:00:10")
@pytest.mark.usefixtures("data_migration_file", "schema_migration_file")
def test_migrate_data_migration(mock_airtable, runner, log):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 0, result.output
    records = mock_airtable.records.get(("fake_base_id", "fake_table_name"))
    record_key = next(iter(records.keys()))
    assert records.get(record_key)["fields"] == {
        "migration_id": "fake_data_file_name",
        "order_id": 20250406020202,
        "type": "data",
        "started_at": "2025-04-06T13:00:10.000Z",
        "applied_at": "2025-04-06T13:00:10.000Z",
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


@freeze_time("2025-04-06 13:00:00")
@pytest.mark.usefixtures("applied_migration", "mock_airtable")
def test_migrate_skip_migration_already_applied(runner, log):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 0, result.output
    assert "Running data migrations..." in result.output
    assert "Skipping applied migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


@freeze_time("2025-04-06 13:00:00")
@pytest.mark.usefixtures("data_migration_file_error")
def test_migrate_data_run_script_fail(mock_airtable, runner, log):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    records = mock_airtable.records.get(("fake_base_id", "fake_table_name"))
    record_key = next(iter(records.keys()))
    assert records.get(record_key)["fields"] == {
        "migration_id": "fake_error_file_name",
        "order_id": 20250406020202,
        "type": "data",
        "started_at": None,
        "applied_at": None,
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_error_file_name" in log.text
    assert "Migration fake_error_file_name failed: Fake Error" in result.output


@freeze_time("2025-04-06 10:11:24")
@pytest.mark.usefixtures("data_migration_file")
def test_migrate_fake(mock_airtable, runner):
    result = runner.invoke(app, ["migrate", "--fake", "fake_data_file_name"])

    assert result.exit_code == 0, result.output
    assert "Running migration fake_data_file_name in fake mode." in result.output
    assert "Migration fake_data_file_name applied successfully." in result.output
    records = mock_airtable.records.get(("fake_base_id", "fake_table_name"))
    record_key = next(iter(records.keys()))
    assert records.get(record_key)["fields"] == {
        "migration_id": "fake_data_file_name",
        "order_id": 20250406020202,
        "type": "data",
        "started_at": None,
        "applied_at": "2025-04-06T10:11:24.000Z",
    }


@pytest.mark.usefixtures("applied_migration", "mock_airtable")
def test_migrate_fake_migration_already_applied(runner):
    result = runner.invoke(app, ["migrate", "--fake", "fake_data_file_name"])

    assert result.exit_code == 1, result.output
    assert (
        "Error running fake command: Migration fake_data_file_name already applied" in result.output
    )


@pytest.mark.usefixtures("applied_migration", "schema_migration_file")
def test_migrate_list(runner, log):
    result = runner.invoke(app, ["migrate", "--list"])

    assert result.exit_code == 0, result.output
    assert "No state found for migration: fake_schema_file_name" in log.text
    formatted_output = "".join(result.output.split())
    assert "┃order_id┃migration_id┃started_at┃applied_at┃type┃" in formatted_output
    assert (
        "│20250406020202│fake_data_file…│2025-04-06T13:…│2025-04-06T13:0…│data│" in formatted_output
    )
    assert "│20260101010101│fake_schema_fi…││││" in formatted_output

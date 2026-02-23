import json

import pytest
from freezegun import freeze_time

from mpt_tool.cli import app
from mpt_tool.constants import MIGRATION_STATE_FILE


@pytest.fixture
def migration_state_file(tmp_path):
    migration_state_file = tmp_path / MIGRATION_STATE_FILE
    migration_state_file.write_text(encoding="utf-8", data="{}")
    return migration_state_file


@pytest.fixture
def applied_migration(data_migration_file, migration_state_file):
    applied_state_data = {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:10:20+00:00",
            "applied_at": "2025-04-06T13:10:30+00:00",
            "version": "5.3.2",
        }
    }
    migration_state_file.write_text(encoding="utf-8", data=json.dumps(applied_state_data))

    return data_migration_file


@freeze_time("2025-04-06 13:10:30")
@pytest.mark.usefixtures("data_migration_file", "schema_migration_file")
def test_migrate_data_migration(monkeypatch, migration_state_file, runner, log):
    monkeypatch.setenv("SERVICE_VERSION", "1.2.3")

    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 0, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:10:30+00:00",
            "applied_at": "2025-04-06T13:10:30+00:00",
            "version": "1.2.3",
        }
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


@freeze_time("2025-04-06 13:10:30")
@pytest.mark.usefixtures("data_migration_file", "schema_migration_file")
def test_migrate_data_single_migration(migration_state_file, runner, log):
    result = runner.invoke(app, ["migrate", "--data", "fake_data_file_name"])

    assert result.exit_code == 0, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:10:30+00:00",
            "applied_at": "2025-04-06T13:10:30+00:00",
            "version": None,
        }
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


@freeze_time("2025-04-06 13:00:00")
@pytest.mark.usefixtures("applied_migration")
def test_migrate_skip_migration_already_applied(migration_state_file, runner, log):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 0, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:10:20+00:00",
            "applied_at": "2025-04-06T13:10:30+00:00",
            "version": "5.3.2",
        }
    }
    assert "Running data migrations..." in result.output
    assert "Skipping applied migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


@pytest.mark.usefixtures("applied_migration")
def test_migrate_data_single_already_applied(runner):
    result = runner.invoke(app, ["migrate", "--data", "fake_data_file_name"])

    assert result.exit_code == 1, result.output
    assert (
        "Error running data command: Migration fake_data_file_name already applied" in result.output
    )


@pytest.mark.usefixtures("data_migration_file_error")
def test_migrate_data_run_script_fail(migration_state_file, runner, log):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data["fake_error_file_name"] == {
        "migration_id": "fake_error_file_name",
        "order_id": 20250406020202,
        "type": "data",
        "started_at": None,
        "applied_at": None,
        "version": None,
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_error_file_name" in log.text
    assert "Migration fake_error_file_name failed: Fake Error" in result.output


@pytest.mark.usefixtures("data_migration_file")
def test_migrate_data_single_migration_not_found(runner):
    result = runner.invoke(app, ["migrate", "--data", "not_existing_migration"])

    assert result.exit_code == 1, result.output
    assert "Error running data command: Migration not_existing_migration not found" in result.output


@pytest.mark.usefixtures("data_migration_file", "schema_migration_file")
def test_migrate_data_single_migration_wrong_type(runner):
    result = runner.invoke(app, ["migrate", "--data", "fake_schema_file_name"])

    assert result.exit_code == 1, result.output
    assert (
        "Error running data command: Migration fake_schema_file_name is not a data migration"
        in result.output
    )


@freeze_time("2025-04-06 13:10:30")
@pytest.mark.usefixtures("data_migration_file", "schema_migration_file")
def test_migrate_schema_single_migration(migration_state_file, runner, log):
    result = runner.invoke(app, ["migrate", "--schema", "fake_schema_file_name"])

    assert result.exit_code == 0, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_schema_file_name": {
            "migration_id": "fake_schema_file_name",
            "order_id": 20260101010101,
            "type": "schema",
            "started_at": "2025-04-06T13:10:30+00:00",
            "applied_at": "2025-04-06T13:10:30+00:00",
            "version": None,
        }
    }
    assert "Running schema migrations..." in result.output
    assert "Running migration: fake_schema_file_name" in log.text
    assert "schema migrations applied successfully." in result.output


@freeze_time("2025-04-06 10:11:24")
@pytest.mark.usefixtures("data_migration_file")
def test_migrate_manual(migration_state_file, runner):
    result = runner.invoke(app, ["migrate", "--manual", "fake_data_file_name"])

    assert result.exit_code == 0, result.output
    assert "Running migration fake_data_file_name in manual mode." in result.output
    assert "Migration fake_data_file_name applied successfully." in result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": None,
            "applied_at": "2025-04-06T10:11:24+00:00",
            "version": None,
        }
    }


@pytest.mark.usefixtures("applied_migration")
def test_migrate_manual_migration_already_applied(runner):
    result = runner.invoke(app, ["migrate", "--manual", "fake_data_file_name"])

    assert result.exit_code == 1, result.output
    assert (
        "Error running manual command: Migration fake_data_file_name already applied"
        in result.output
    )


def test_migrate_init(runner, tmp_path):
    result = runner.invoke(app, ["migrate", "--init"])

    assert result.exit_code == 0, result.output
    assert "Initializing migration tool..." in result.output
    assert "Migration tool initialized successfully." in result.output
    assert (tmp_path / "migrations").exists()
    assert (tmp_path / ".migrations-state.json").exists()


@pytest.mark.usefixtures("migration_state_file")
def test_migrate_init_file_already_exists(runner, tmp_path, log):
    result = runner.invoke(app, ["migrate", "--init"])

    assert result.exit_code == 1, result.output
    assert (
        "Cannot initialize - State file already exists at .migrations-state.json" in result.output
    )


@pytest.mark.usefixtures("applied_migration", "schema_migration_file", "migration_state_file")
def test_migrate_list(runner, log):
    result = runner.invoke(app, ["migrate", "--list"])

    assert result.exit_code == 0, result.output
    assert "No state found for migration: fake_schema_file_name" in log.text
    formatted_output = "".join(result.output.split())
    assert "┃order_id┃migration_id┃started_at┃applied_at┃type┃status┃version┃" in formatted_output
    assert (
        "│20250406020202│fake_data_file_name│2025-04-06T13:10:20+00:00│2025-04-06T13:10:30+00:00│data│Applied│5.3.2│"
        in formatted_output
    )
    assert "│20260101010101│fake_schema_file_name│-│-│-│NotApplied│-│" in formatted_output

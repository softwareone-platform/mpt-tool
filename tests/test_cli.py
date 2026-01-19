import json

import pytest
from freezegun import freeze_time
from typer.testing import CliRunner

from mpt_tool.cli import app
from mpt_tool.constants import MIGRATION_FOLDER, MIGRATION_STATE_FILE
from mpt_tool.templates import MIGRATION_SCAFFOLDING_TEMPLATE


@pytest.fixture(autouse=True)
def mock_chdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def migration_folder(tmp_path):
    migration_folder_path = tmp_path / MIGRATION_FOLDER
    migration_folder_path.mkdir(exist_ok=True)
    return migration_folder_path


@pytest.fixture
def data_migration_file(migration_folder):
    migration_id = "fake_data_file_name"
    migration_file = migration_folder / f"20250406020202_{migration_id}.py"
    migration_file.write_text(
        encoding="utf-8",
        data=MIGRATION_SCAFFOLDING_TEMPLATE.substitute(command_name="DataBaseCommand"),
    )
    return {"migration_id": migration_id, "full_filename": migration_file}


@pytest.fixture
def data_migration_file_error(migration_folder):
    migration_id = "fake_error_file_name"
    migration_file = migration_folder / f"20250406020202_{migration_id}.py"
    file_data = MIGRATION_SCAFFOLDING_TEMPLATE.substitute(command_name="DataBaseCommand").replace(
        "pass", "raise Exception('Fake Error')"
    )
    migration_file.write_text(encoding="utf-8", data=file_data)
    return {"migration_id": migration_id, "full_filename": migration_file}


@pytest.fixture
def schema_migration_file(migration_folder):
    migration_id = "fake_schema_file_name"
    migration_file = migration_folder / f"20260101010101_{migration_id}.py"
    migration_file.write_text(
        encoding="utf-8",
        data=MIGRATION_SCAFFOLDING_TEMPLATE.substitute(command_name="SchemaBaseCommand"),
    )
    return {"migration_id": migration_id, "full_filename": migration_file}


@pytest.fixture
def migration_state_file(tmp_path):
    migration_state_file = tmp_path / MIGRATION_STATE_FILE
    migration_state_file.write_text(encoding="utf-8", data="{}")
    return migration_state_file


@pytest.fixture
def runner():
    return CliRunner()


def test_help(runner):
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0, result.output
    assert "MPT CLI - Migration tool for extensions." in result.output
    assert "migrate" in result.output


def test_migrate_command(runner):
    result = runner.invoke(app, ["migrate"])

    assert result.exit_code == 2, result.output
    assert "Invalid value for migrate:" in result.output
    assert "At least one option must be used." in result.output


def test_migrate_command_multiple_options_error(runner):
    result = runner.invoke(app, ["migrate", "--new-data", "bla", "--new-schema", "foo"])

    assert result.exit_code == 2, result.output
    assert "Invalid value for migrate:" in result.output
    assert "Only one option can be used." in result.output


@freeze_time("2025-04-06 13:00:00")
def test_migrate_data_migration(
    data_migration_file, schema_migration_file, migration_state_file, runner, log
):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 0, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:00:00+00:00",
            "applied_at": "2025-04-06T13:00:00+00:00",
        }
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


@freeze_time("2025-04-06 13:00:00")
def test_migrate_skip_migration_already_applied(
    data_migration_file, migration_state_file, runner, log
):
    applied_state_data = {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:00:00+00:00",
            "applied_at": "2025-04-06T13:00:00+00:00",
        }
    }
    migration_state_file.write_text(data=json.dumps(applied_state_data))

    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 0, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data == {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:00:00+00:00",
            "applied_at": "2025-04-06T13:00:00+00:00",
        }
    }
    assert "Running data migrations..." in result.output
    assert "Skipping applied migration: fake_data_file_name" in log.text
    assert "Migrations completed successfully." in result.output


def test_migrate_data_migration_folder_not_found(runner):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    assert "Migration folder not found:" in result.output


def test_migrate_data_duplicate_migration(runner, migration_folder):
    (migration_folder / "20250406020202_fake_file_name.py").touch()
    (migration_folder / "20260107010101_fake_file_name.py").touch()

    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    assert "Duplicate migration filename found: fake_file_name" in result.output


@freeze_time("2025-04-06 13:00:00")
def test_migrate_data_run_script_fail(data_migration_file_error, migration_state_file, runner, log):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    migration_state_data = json.loads(migration_state_file.read_text(encoding="utf-8"))
    assert migration_state_data["fake_error_file_name"] == {
        "migration_id": "fake_error_file_name",
        "order_id": 20250406020202,
        "type": "data",
        "started_at": None,
        "applied_at": None,
    }
    assert "Running data migrations..." in result.output
    assert "Running migration: fake_error_file_name" in log.text
    assert "Migration fake_error_file_name failed: Fake Error" in result.output


@freeze_time("2025-04-06 12:21:34")
@pytest.mark.parametrize(
    ("migration_type", "expected_command"),
    [
        ("--new-data", "DataBaseCommand"),
        ("--new-schema", "SchemaBaseCommand"),
    ],
)
def test_migrate_command_new_options(migration_type, expected_command, migration_folder, runner):
    migration_filename = "fake_file_name"

    result = runner.invoke(app, ["migrate", migration_type, migration_filename])

    assert result.exit_code == 0, result.output
    assert f"Scaffolding migration: {migration_filename}." in result.output
    new_migration_filename = f"20250406122134_{migration_filename}.py"
    assert f"Migration file: {new_migration_filename} has been created." in result.output
    new_migration_file = migration_folder / new_migration_filename
    assert new_migration_file.exists()
    assert f"class Command({expected_command})" in new_migration_file.read_text()


@freeze_time("2025-04-06 12:21:34")
def test_migrate_command_file_already_exists(migration_folder, runner):
    migration_filename = "fake_file_name"
    (migration_folder / f"20250406122134_{migration_filename}.py").touch()

    result = runner.invoke(app, ["migrate", "--new-data", migration_filename])

    assert result.exit_code == 1, result.output
    assert f"File already exists: 20250406122134_{migration_filename}" in result.output
    assert result.stderr == "Aborted.\n"


@pytest.mark.usefixtures("data_migration_file", "schema_migration_file")
def test_migrate_list(migration_state_file, runner, log):
    applied_state_data = {
        "fake_data_file_name": {
            "migration_id": "fake_data_file_name",
            "order_id": 20250406020202,
            "type": "data",
            "started_at": "2025-04-06T13:00:00+00:00",
            "applied_at": "2025-04-06T13:00:00+00:00",
        }
    }
    migration_state_file.write_text(data=json.dumps(applied_state_data))

    result = runner.invoke(app, ["migrate", "--list"])

    assert result.exit_code == 0, result.output
    assert "No state found for migration: fake_schema_file_name" in log.text
    formatted_output = "".join(result.output.split())
    assert "┃order_id┃migration_id┃started_at┃applied_at┃type┃" in formatted_output
    assert (
        "│20250406020202│fake_data_file…│2025-04-06T13:…│2025-04-06T13:0…│data│" in formatted_output
    )
    assert "│20260101010101│fake_schema_fi…││││" in formatted_output


def test_migrate_list_no_migrations(runner):
    result = runner.invoke(app, ["migrate", "--list"])

    assert result.exit_code == 0, result.output
    assert "No migrations found." in result.output

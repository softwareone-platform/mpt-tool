import pytest
from freezegun import freeze_time
from typer.testing import CliRunner

from mpt_tool.cli import app
from mpt_tool.constants import MIGRATION_FOLDER


@pytest.fixture(autouse=True)
def mock_chdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)


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

    assert result.exit_code == 0, result.output
    assert "Running migrations is not implemented yet." in result.output


def test_migrate_command_multiple_options_error(runner):
    result = runner.invoke(app, ["migrate", "--new-data", "bla", "--new-schema", "foo"])

    assert result.exit_code == 2, result.output
    assert "Invalid value for migrate:" in result.output
    assert "Options --new-data and --new-schema cannot be" in result.output


@freeze_time("2025-04-06 12:21:34")
@pytest.mark.parametrize(
    ("migration_type", "expected_command"),
    [
        ("--new-data", "DataBaseCommand"),
        ("--new-schema", "SchemaBaseCommand"),
    ],
)
def test_migrate_command_new_options(migration_type, expected_command, tmp_path, runner):
    migration_filename = "fake_file_name"

    result = runner.invoke(app, ["migrate", migration_type, migration_filename])

    assert result.exit_code == 0, result.output
    assert f"Scaffolding migration: {migration_filename}." in result.output
    new_migration_filename = f"20250406122134_{migration_filename}.py"
    assert f"Migration file: {new_migration_filename} has been created." in result.output
    new_migration_file = tmp_path / MIGRATION_FOLDER / new_migration_filename
    assert new_migration_file.exists()
    assert f"class Command({expected_command})" in new_migration_file.read_text()


@freeze_time("2025-04-06 12:21:34")
def test_migrate_command_file_already_exists(tmp_path, runner):
    (tmp_path / MIGRATION_FOLDER).mkdir(parents=True, exist_ok=True)
    migration_filename = "fake_file_name"
    (tmp_path / MIGRATION_FOLDER / f"20250406122134_{migration_filename}.py").touch()

    result = runner.invoke(app, ["migrate", "--new-data", migration_filename])

    assert result.exit_code == 1, result.output
    assert f"File already exists: 20250406122134_{migration_filename}" in result.output
    assert result.stderr == "Aborted.\n"

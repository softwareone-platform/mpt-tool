import pytest
from freezegun import freeze_time

from mpt_tool.cli import app


def test_help(runner):
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0, result.output
    assert "MPT CLI - Migration tool for extensions." in result.output
    assert "migrate" in result.output


def test_migrate_command(runner):
    result = runner.invoke(app, ["migrate"])

    assert result.exit_code == 2, result.output
    assert "Invalid value for migrate:" in result.output
    assert "At least one param must be used." in result.output


def test_migrate_command_multiple_params_error(runner):
    result = runner.invoke(app, ["migrate", "--new-data", "bla", "--new-schema", "foo"])

    assert result.exit_code == 2, result.output
    assert "Invalid value for migrate:" in result.output
    assert "Only one param can be used." in result.output


def test_migrate_data_duplicate_migration(runner, migration_folder):
    (migration_folder / "20250406020202_fake_file_name.py").touch()
    (migration_folder / "20260107010101_fake_file_name.py").touch()

    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    assert "Duplicate migration filename found: fake_file_name" in result.output


def test_migrate_data_migration_folder_not_found(runner):
    result = runner.invoke(app, ["migrate", "--data"])

    assert result.exit_code == 1, result.output
    assert "Migration folder not found:" in result.output


def test_migrate_fake_folder_not_found(runner):
    result = runner.invoke(app, ["migrate", "--fake", "not_existing_migration"])

    assert result.exit_code == 1, result.output
    assert "Error running fake command: Migration folder not found: migrations" in result.output


@pytest.mark.usefixtures("data_migration_file")
def test_migrate_fake_migration_not_found(runner):
    result = runner.invoke(app, ["migrate", "--fake", "not_existing_migration"])

    assert result.exit_code == 1, result.output
    assert "Error running fake command: Migration not_existing_migration not found" in result.output


@freeze_time("2025-04-06 12:21:34")
@pytest.mark.parametrize(
    ("migration_type", "expected_command"),
    [
        ("--new-data", "DataBaseMigration"),
        ("--new-schema", "SchemaBaseMigration"),
    ],
)
def test_migrate_command_new(migration_type, expected_command, migration_folder, runner):
    migration_filename = "fake_file_name"

    result = runner.invoke(app, ["migrate", migration_type, migration_filename])

    assert result.exit_code == 0, result.output
    assert f"Scaffolding migration: {migration_filename}." in result.output
    new_migration_filename = f"20250406122134_{migration_filename}.py"
    assert f"Migration file: {new_migration_filename} has been created." in result.output
    new_migration_file = migration_folder / new_migration_filename
    assert new_migration_file.exists()
    assert f"class Migration({expected_command})" in new_migration_file.read_text()


@freeze_time("2025-04-06 12:21:34")
def test_migrate_command_file_already_exists(migration_folder, runner):
    migration_filename = "fake_file_name"
    (migration_folder / f"20250406122134_{migration_filename}.py").touch()

    result = runner.invoke(app, ["migrate", "--new-data", migration_filename])

    assert result.exit_code == 1, result.output
    assert f"File already exists: 20250406122134_{migration_filename}" in result.output
    assert result.stderr == "Aborted.\n"


def test_migrate_list_no_migrations(runner):
    result = runner.invoke(app, ["migrate", "--list"])

    assert result.exit_code == 0, result.output
    assert "No migrations found." in result.output


def test_migrate_check_no_duplicates(runner, migration_folder):
    (migration_folder / "20260101010101_first.py").touch()
    (migration_folder / "20260102020202_second.py").touch()

    result = runner.invoke(app, ["migrate", "--check"])

    assert result.exit_code == 0, result.output
    assert "Checking migrations..." in result.output
    assert "Migrations check passed successfully." in result.output


def test_migrate_check_with_duplicate_id(runner, migration_folder):
    (migration_folder / "20260101010101_duplicate_name.py").touch()
    (migration_folder / "20260102020202_duplicate_name.py").touch()

    result = runner.invoke(app, ["migrate", "--check"])

    assert result.exit_code == 1, result.output
    assert "Duplicate migration_id found in migrations" in result.output
    assert "20260101010101_duplicate_name.py" in result.output
    assert "20260102020202_duplicate_name.py" in result.output


@pytest.mark.usefixtures("migration_folder")
def test_migrate_check_empty_folder(runner):
    result = runner.invoke(app, ["migrate", "--check"])

    assert result.exit_code == 0, result.output
    assert "Checking migrations..." in result.output
    assert "Migrations check passed successfully." in result.output

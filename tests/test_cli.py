import pytest
from typer.testing import CliRunner

from mpt_tool.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_migrate_command(runner):
    result = runner.invoke(app, ["migrate"])

    assert result.exit_code == 0
    assert "Hello World!" in result.output


def test_help(runner):
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "MPT CLI - Migration tool for extensions." in result.output
    assert "migrate" in result.output


def test_init_command(monkeypatch, tmp_path, runner):
    settings_file = tmp_path / "settings.py"
    settings_file.write_text("FAKE_SETTING = True")
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    migration_dir = tmp_path / "migrations"
    assert migration_dir.exists()
    state_file = tmp_path / ".migrations-state.json"
    assert state_file.exists()
    assert state_file.read_text() == "{}\n"


def test_init_command_requires_setting(monkeypatch, tmp_path, runner):
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 1
    assert result.output == "Settings file does not exist.\n"


def test_init_command_migrations_folder_exists(monkeypatch, tmp_path, runner):
    settings_file = tmp_path / "settings.py"
    settings_file.write_text("FAKE_SETTING = True")
    migration_dir = tmp_path / "migrations"
    migration_dir.mkdir()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 1
    assert result.output == "Migrations folder already exists.\n"


def test_init_command_state_file_exists(monkeypatch, tmp_path, runner):
    settings_file = tmp_path / "settings.py"
    settings_file.write_text("FAKE_SETTING = True")
    state_file = tmp_path / ".migrations-state.json"
    state_file.touch()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 1
    assert result.output == "State file already exists.\n"

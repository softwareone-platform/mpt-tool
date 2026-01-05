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
    help_command = runner.invoke(app, ["--help"])

    assert help_command.exit_code == 0
    assert "MPT CLI - Migration tool for extensions." in help_command.output
    assert "migrate" in help_command.output

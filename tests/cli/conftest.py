import pytest
from typer.testing import CliRunner

from mpt_tool.constants import MIGRATION_FOLDER
from mpt_tool.templates import MIGRATION_SCAFFOLDING_TEMPLATE


@pytest.fixture(autouse=True)
def mock_chdir(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("STORAGE_TYPE", "local")


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
        data=MIGRATION_SCAFFOLDING_TEMPLATE.substitute(migration_name="DataBaseMigration"),
    )
    return {"migration_id": migration_id, "full_filename": migration_file}


@pytest.fixture
def data_migration_file_error(migration_folder):
    migration_id = "fake_error_file_name"
    migration_file = migration_folder / f"20250406020202_{migration_id}.py"
    file_data = MIGRATION_SCAFFOLDING_TEMPLATE.substitute(
        migration_name="DataBaseMigration"
    ).replace("pass", "raise Exception('Fake Error')")
    migration_file.write_text(encoding="utf-8", data=file_data)
    return {"migration_id": migration_id, "full_filename": migration_file}


@pytest.fixture
def schema_migration_file(migration_folder):
    migration_id = "fake_schema_file_name"
    migration_file = migration_folder / f"20260101010101_{migration_id}.py"
    migration_file.write_text(
        encoding="utf-8",
        data=MIGRATION_SCAFFOLDING_TEMPLATE.substitute(migration_name="SchemaBaseMigration"),
    )
    return {"migration_id": migration_id, "full_filename": migration_file}


@pytest.fixture
def runner():
    return CliRunner()

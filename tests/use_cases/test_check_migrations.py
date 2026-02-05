import pytest

from mpt_tool.managers import FileMigrationManager
from mpt_tool.models import MigrationFile
from mpt_tool.use_cases.check_migrations import CheckMigrationsUseCase
from mpt_tool.use_cases.errors import CheckMigrationError


def test_check_migrations_no_duplicates(mocker):
    migration_files = (
        MigrationFile.build_from_path(mocker.Mock(stem="20260101010101_first")),
        MigrationFile.build_from_path(mocker.Mock(stem="20260102020202_second")),
    )
    file_migration_manager = mocker.Mock(spec=FileMigrationManager)
    file_migration_manager.retrieve_migration_files.return_value = migration_files
    use_case = CheckMigrationsUseCase(file_migration_manager=file_migration_manager)

    use_case.execute()  # act

    file_migration_manager.retrieve_migration_files.assert_called_once()


def test_check_migrations_empty_folder(mocker):
    file_migration_manager = mocker.Mock(spec=FileMigrationManager)
    file_migration_manager.retrieve_migration_files.return_value = ()
    use_case = CheckMigrationsUseCase(file_migration_manager=file_migration_manager)

    use_case.execute()  # act

    file_migration_manager.retrieve_migration_files.assert_called_once()


def test_check_migrations_with_duplicate_id(mocker):
    migration_files = (
        MigrationFile.build_from_path(mocker.Mock(stem="20260101010101_duplicate_name")),
        MigrationFile.build_from_path(mocker.Mock(stem="20260102020202_duplicate_name")),
    )
    file_migration_manager = mocker.Mock(spec=FileMigrationManager)
    file_migration_manager.retrieve_migration_files.return_value = migration_files
    use_case = CheckMigrationsUseCase(file_migration_manager=file_migration_manager)

    with pytest.raises(CheckMigrationError) as exc_info:
        use_case.execute()

    assert "Duplicate migration_id found in migrations" in str(exc_info.value)
    assert "20260101010101_duplicate_name.py" in str(exc_info.value)
    assert "20260102020202_duplicate_name.py" in str(exc_info.value)


def test_check_migrations_multiple_duplicates(mocker):
    migration_files = (
        MigrationFile.build_from_path(mocker.Mock(stem="20260101010101_duplicate_one")),
        MigrationFile.build_from_path(mocker.Mock(stem="20260102020202_duplicate_one")),
        MigrationFile.build_from_path(mocker.Mock(stem="20260103030303_duplicate_two")),
        MigrationFile.build_from_path(mocker.Mock(stem="20260104040404_duplicate_two")),
    )
    file_migration_manager = mocker.Mock(spec=FileMigrationManager)
    file_migration_manager.retrieve_migration_files.return_value = migration_files
    use_case = CheckMigrationsUseCase(file_migration_manager=file_migration_manager)

    with pytest.raises(CheckMigrationError) as exc_info:
        use_case.execute()

    assert "Duplicate migration_id found in migrations" in str(exc_info.value)
    assert "20260101010101_duplicate_one" in str(exc_info.value)
    assert "20260104040404_duplicate_two" in str(exc_info.value)

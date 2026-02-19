import pytest

from mpt_tool.enums import MigrationStatusEnum, MigrationTypeEnum
from mpt_tool.managers import StateManager
from mpt_tool.managers.errors import StateNotFoundError
from mpt_tool.models import Migration
from mpt_tool.services.migration_state import MigrationStateService


@pytest.fixture
def mock_state():
    return Migration(migration_id="fake_id", order_id=1024, type=MigrationTypeEnum.DATA)


def test_get_or_create_state_existing(mocker, mock_state):
    state_manager = mocker.Mock(spec=StateManager)
    state_manager.get_by_id.return_value = mock_state
    service = MigrationStateService(state_manager)

    result = service.get_or_create_state(
        migration_id="fake_id", migration_type=MigrationTypeEnum.DATA, order_id=1024
    )

    assert result == mock_state
    state_manager.get_by_id.assert_called_once_with("fake_id")
    state_manager.new.assert_not_called()


def test_get_or_create_state_missing(mocker, mock_state):
    state_manager = mocker.Mock(spec=StateManager)
    state_manager.get_by_id.side_effect = StateNotFoundError("State not found")
    state_manager.new.return_value = mock_state
    service = MigrationStateService(state_manager)

    result = service.get_or_create_state(
        migration_id="fake_id", migration_type=MigrationTypeEnum.DATA, order_id=1024
    )

    assert result == mock_state
    state_manager.get_by_id.assert_called_once_with("fake_id")
    state_manager.new.assert_called_once_with("fake_id", MigrationTypeEnum.DATA, 1024)


@pytest.mark.parametrize(
    ("status", "expected_method_call"),
    [
        (MigrationStatusEnum.APPLIED, "applied"),
        (MigrationStatusEnum.FAILED, "failed"),
        (MigrationStatusEnum.MANUAL_APPLIED, "manual"),
        (MigrationStatusEnum.RUNNING, "start"),
    ],
)
def test_save_state(status, expected_method_call, mocker, mock_state):
    mock_method = mocker.patch.object(Migration, expected_method_call, autospec=True)
    state_manager = mocker.Mock(spec=StateManager)
    service = MigrationStateService(state_manager)

    service.save_state(mock_state, status=status)  # act

    mock_method.assert_called_once()
    state_manager.save_state.assert_called_once_with(mock_state)

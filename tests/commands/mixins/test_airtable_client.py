import pytest

from mpt_tool.migration.mixins import AirtableAPIClientMixin


def test_airtable_client():
    result = hasattr(AirtableAPIClientMixin, "airtable_client")

    assert result is True


def test_airtable_client_env_not_set(monkeypatch):
    monkeypatch.setenv("MPT_TOOL_STORAGE_AIRTABLE_API_KEY", "")
    mixin = AirtableAPIClientMixin()

    with pytest.raises(
        ValueError,
        match="Airtable API key must be set in env variable MPT_TOOL_STORAGE_AIRTABLE_API_KEY",
    ):
        _ = mixin.airtable_client  # noqa: WPS122

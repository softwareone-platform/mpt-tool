import pytest

from mpt_tool.commands.mixins import MPTAPIClientMixin


def test_mpt_client_mixin():
    result = hasattr(MPTAPIClientMixin, "mpt_client")

    assert result is True


@pytest.mark.parametrize(
    ("mpt_api_key", "mpt_base_url"),
    [
        ("test-api-key", ""),
        ("", "https://test.com"),
    ],
)
def test_mpt_client_env_not_set(mpt_api_key, mpt_base_url, monkeypatch):
    monkeypatch.setenv("MPT_API_TOKEN", mpt_api_key)
    monkeypatch.setenv("MPT_API_BASE_URL", mpt_base_url)
    mixin = MPTAPIClientMixin()

    with pytest.raises(ValueError, match="MPT API token and base URL must be set in env variables"):
        _ = mixin.mpt_client  # noqa: WPS122


def test_mpt_client_is_cached(monkeypatch):
    monkeypatch.setenv("MPT_API_TOKEN", "test-api-key")
    monkeypatch.setenv("MPT_API_BASE_URL", "https://test.com")
    mixin = MPTAPIClientMixin()
    client1 = mixin.mpt_client
    client2 = mixin.mpt_client

    result = client1 is client2

    assert result is True

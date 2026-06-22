from functools import cached_property

from pyairtable import Api as AirtableClient

from mpt_tool.config import get_airtable_config


class AirtableAPIClientMixin:
    """Mixin to add Airtable API client to commands.

    The API key is read from the environment variable MPT_TOOL_STORAGE_AIRTABLE_API_KEY.
    """

    @cached_property
    def airtable_client(self) -> AirtableClient:
        """Airtable client, created on first access.

        Returns:
            The Airtable Client instance

        Raises:
            ValueError: If required environment variables are not set

        """
        airtable_api_key = get_airtable_config("api_key")
        if not airtable_api_key:
            raise ValueError(
                "Airtable API key must be set in env variable MPT_TOOL_STORAGE_AIRTABLE_API_KEY"
            )

        return AirtableClient(airtable_api_key)

import os
from functools import cached_property

from pyairtable import Api as AirtableClient


class AirtableAPIClientMixin:
    """Mixin to add Airtable API client to commands.

    The API key is read from the environment variable AIRTABLE_API_KEY.
    """

    @cached_property
    def airtable_client(self) -> AirtableClient:
        """Get or create Airtable Client.

        Returns:
            The Airtable Client instance

        Raises:
            ValueError: If required environment variables are not set

        """
        airtable_api_key = os.getenv("AIRTABLE_API_KEY")
        if not airtable_api_key:
            raise ValueError("Airtable API key must be set in env variable AIRTABLE_API_KEY")

        return AirtableClient(airtable_api_key)

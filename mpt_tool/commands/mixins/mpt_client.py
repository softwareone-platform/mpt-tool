import os
from functools import cached_property

from mpt_api_client import MPTClient


class MPTAPIClientMixin:
    """Mixin to add MPT API client to commands.

    MPT API token and base URL are read from the environment variables MPT_API_TOKEN
    and MPT_API_BASE_URL.
    """

    @cached_property
    def mpt_client(self) -> MPTClient:
        """Get or create MPT API client from environment configurations.

        Returns:
            The MPT API client instance

        Raises:
            ValueError: If required environment variables are not set

        """
        api_token = os.getenv("MPT_API_TOKEN")
        base_url = os.getenv("MPT_API_BASE_URL")
        if not api_token or not base_url:
            raise ValueError("MPT API token and base URL must be set in env variables")

        return MPTClient.from_config(api_token=api_token, base_url=base_url)

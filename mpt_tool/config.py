import os


def get_airtable_config(config_key: str) -> str | None:
    """Get Airtable configuration."""
    config = {
        "api_key": os.getenv("AIRTABLE_API_KEY"),
        "base_id": os.getenv("STORAGE_AIRTABLE_BASE_ID"),
        "table_name": os.getenv("STORAGE_AIRTABLE_TABLE_NAME", "Migrations"),
    }
    return config.get(config_key)


def get_mpt_config(config_key: str) -> str | None:
    """Get MPT configuration."""
    config = {"api_token": os.getenv("MPT_API_TOKEN"), "base_url": os.getenv("MPT_API_BASE_URL")}
    return config.get(config_key)


def get_storage_type() -> str:
    """Get storage type."""
    return os.getenv("STORAGE_TYPE", "local")

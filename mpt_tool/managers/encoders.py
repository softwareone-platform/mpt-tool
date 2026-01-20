import json
from typing import Any, override

from mpt_tool.models import Migration


class StateJSONEncoder(json.JSONEncoder):
    """JSON encoder for migration states."""

    @override
    def default(self, obj: object) -> Any:  # noqa: WPS110
        if isinstance(obj, Migration):
            return obj.to_dict()

        return super().default(obj)

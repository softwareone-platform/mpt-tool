from typing import Any

from mpt_tool.commands.errors import BadParameterError


class MigrateCommandValidator:
    """Validator for the migrate command."""

    @classmethod
    def validate(cls, command_params: dict[str, Any]) -> None:
        """Validate the migrate command parameters.

        Args:
            command_params: The migrate command parameters.

        Raises:
            BadParameterError: When none or more than one param is used
        """
        param_counts = sum(1 for param_value in command_params.values() if param_value)
        if not param_counts:
            raise BadParameterError("At least one param must be used.")

        if param_counts > 1:
            raise BadParameterError("Only one param can be used.")

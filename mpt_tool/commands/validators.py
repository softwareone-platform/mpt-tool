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
        migration_id = command_params.get("migration_id")
        command_values = {
            key: param_value for key, param_value in command_params.items() if key != "migration_id"
        }
        param_counts = sum(1 for param_value in command_values.values() if param_value)
        if migration_id and not command_params.get("data") and not command_params.get("schema"):
            raise BadParameterError("MIGRATION_ID can only be used with --data or --schema.")

        if not param_counts:
            raise BadParameterError("At least one param must be used.")

        if param_counts > 1:
            raise BadParameterError("Only one param can be used.")

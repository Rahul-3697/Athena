from athena.contracts.tool_request import ToolRequest
from athena.tools.tool_registry import ToolRegistry


class ToolValidator:
    """
    Validates ToolRequests before execution.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def validate(self, request: ToolRequest) -> None:

        if not request.tool_name:
            raise ValueError(
                "Tool name cannot be empty."
            )

        if not isinstance(request.arguments, dict):
            raise ValueError(
                "Tool arguments must be a dictionary."
            )

        if not self.registry.has(request.tool_name):
            raise ValueError(
                f"Tool '{request.tool_name}' is not registered."
            )

        tool = self.registry.get(request.tool_name)

        self._validate_arguments(
            tool,
            request.arguments
        )

    def _validate_arguments(self, tool, arguments: dict) -> None:

        schema = tool.input_schema

        properties = schema.get(
            "properties",
            {}
        )

        required = schema.get(
            "required",
            []
        )

        # Check required arguments
        for field in required:

            if field not in arguments:
                raise ValueError(
                    f"Missing required argument "
                    f"'{field}' for tool '{tool.name}'."
                )

        # Check unknown arguments
        for argument in arguments:

            if argument not in properties:
                raise ValueError(
                    f"Unknown argument '{argument}' "
                    f"for tool '{tool.name}'."
                )

        # Basic type validation
        for name, value in arguments.items():

            expected_type = properties[name].get("type")

            if expected_type == "string":
                if not isinstance(value, str):
                    raise ValueError(
                        f"Argument '{name}' must be a string."
                    )

            elif expected_type == "integer":
                if not isinstance(value, int):
                    raise ValueError(
                        f"Argument '{name}' must be an integer."
                    )

            elif expected_type == "boolean":
                if not isinstance(value, bool):
                    raise ValueError(
                        f"Argument '{name}' must be a boolean."
                    )

            elif expected_type == "object":
                if not isinstance(value, dict):
                    raise ValueError(
                        f"Argument '{name}' must be an object."
                    )
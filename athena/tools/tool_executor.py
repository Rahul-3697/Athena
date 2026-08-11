from athena.contracts.tool_input import ToolInput
from athena.contracts.tool_request import ToolRequest
from athena.contracts.tool_result import ToolResult

from athena.tools.tool_registry import ToolRegistry
from athena.tools.tool_validator import ToolValidator


class ToolExecutor:
    """
    Executes validated Athena Tool requests.
    """

    def __init__(self, registry: ToolRegistry):

        self.registry = registry
        self.validator = ToolValidator(registry)

    def execute(self, request: ToolRequest) -> ToolResult:
        """
        Validate and execute a ToolRequest.
        """

        try:
            self.validator.validate(request)

            tool_input = ToolInput(
                name=request.tool_name,
                arguments=request.arguments
            )

            tool = self.registry.get(request.tool_name)

            return tool.execute(tool_input)

        except Exception as exc:

            return ToolResult(
                success=False,
                error=str(exc)
            )
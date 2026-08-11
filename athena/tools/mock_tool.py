from typing import Any

from athena.contracts.tool_input import ToolInput
from athena.contracts.tool_result import ToolResult
from athena.tools.base_tool import BaseTool


class MockTool(BaseTool):

    @property
    def name(self) -> str:
        return "mock_tool"

    @property
    def description(self) -> str:
        return "A development tool used to test Athena tool execution."

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message to return."
                }
            },
            "required": ["message"]
        }

    def execute(self, tool_input: ToolInput) -> ToolResult:

        message = tool_input.arguments.get("message")

        return ToolResult(
            success=True,
            data=message
        )
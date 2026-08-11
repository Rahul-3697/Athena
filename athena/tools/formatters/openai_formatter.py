from typing import Any

from athena.contracts.tool_descriptor import ToolDescriptor
from athena.tools.formatters.base_formatter import BaseToolFormatter


class OpenAIToolFormatter(BaseToolFormatter):
    """
    Converts Athena ToolDescriptors into
    OpenAI Responses API function tools.
    """

    def format(
        self,
        descriptor: ToolDescriptor,
    ) -> dict[str, Any]:

        return {
            "type": "function",
            "name": descriptor.name,
            "description": descriptor.description,
            "parameters": descriptor.input_schema,
            "strict": True,
        }
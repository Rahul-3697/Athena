from typing import Any

from athena.contracts.tool_descriptor import ToolDescriptor
from athena.tools.formatters.base_formatter import BaseToolFormatter


class ToolFormatter:

    def __init__(self, formatter: BaseToolFormatter):
        self.formatter = formatter

    def format(
        self,
        descriptor: ToolDescriptor
    ) -> dict[str, Any]:

        return self.formatter.format(descriptor)

    def format_many(
        self,
        descriptors: list[ToolDescriptor]
    ) -> list[dict[str, Any]]:

        return [
            self.formatter.format(descriptor)
            for descriptor in descriptors
        ]
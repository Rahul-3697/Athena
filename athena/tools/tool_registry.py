from athena.contracts.tool_descriptor import ToolDescriptor
from athena.tools.base_tool import BaseTool


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:

        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool:

        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        return self._tools[name]

    def has(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def descriptors(self) -> list[ToolDescriptor]:
        """
        Return LLM-facing descriptors for all registered Tools.
        """

        return [
            tool.descriptor()
            for tool in self._tools.values()
        ]
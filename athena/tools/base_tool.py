from abc import ABC, abstractmethod
from typing import Any

from athena.contracts.tool_descriptor import ToolDescriptor
from athena.contracts.tool_input import ToolInput
from athena.contracts.tool_result import ToolResult


class BaseTool(ABC):
    """
    Base interface for every Athena Tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the Tool."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the Tool does."""
        raise NotImplementedError

    @property
    @abstractmethod
    def input_schema(self) -> dict[str, Any]:
        """Schema describing accepted Tool arguments."""
        raise NotImplementedError

    def descriptor(self) -> ToolDescriptor:
        """
        Return the LLM-facing description of this Tool.
        """

        return ToolDescriptor(
            name=self.name,
            description=self.description,
            input_schema=self.input_schema,
        )

    @abstractmethod
    def execute(self, tool_input: ToolInput) -> ToolResult:
        """Execute the Tool."""
        raise NotImplementedError
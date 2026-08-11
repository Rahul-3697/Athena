from abc import ABC, abstractmethod
from typing import Any

from athena.contracts.tool_descriptor import ToolDescriptor


class BaseToolFormatter(ABC):
    """
    Base interface for converting Athena ToolDescriptors
    into provider/framework-specific tool definitions.
    """

    @abstractmethod
    def format(
        self,
        descriptor: ToolDescriptor
    ) -> dict[str, Any]:
        """
        Convert an Athena ToolDescriptor into a
        provider-specific representation.
        """
        raise NotImplementedError
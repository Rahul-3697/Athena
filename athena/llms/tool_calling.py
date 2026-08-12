from abc import ABC, abstractmethod

from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_descriptor import ToolDescriptor
from athena.contracts.tool_result import ToolResult
from athena.contracts.llm_response import LLMResponse

class BaseToolCallingLLM(ABC):
    """
    Provider-independent interface for an LLM
    capable of Tool calling.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        tools: list[ToolDescriptor],
    ) -> LLMResponse:
        """
        Start an LLM interaction.

        Returns:
            Final text, or Tool calls requested by the model.
        """
        raise NotImplementedError

    @abstractmethod
    def continue_with_tool_results(
        self,
        results: list[tuple[ToolCall, ToolResult]],
    ) -> LLMResponse:
        """
        Continue the LLM interaction after Tool execution.
        """
        raise NotImplementedError
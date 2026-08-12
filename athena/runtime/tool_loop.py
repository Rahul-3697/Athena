from athena.contracts.tool_request import ToolRequest
from athena.llms.tool_calling import BaseToolCallingLLM
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry
from athena.contracts.llm_response import LLMResponse

class ToolLoop:
    """
    Executes an iterative LLM-driven Tool loop.
    """

    def __init__(
        self,
        llm: BaseToolCallingLLM,
        registry: ToolRegistry,
        executor: ToolExecutor,
        max_iterations: int = 3,
    ):
        self.llm = llm
        self.registry = registry
        self.executor = executor
        self.max_iterations = max_iterations

    def run(self, prompt: str) -> str:

        descriptors = self.registry.descriptors()

        response = self.llm.generate(
            prompt=prompt,
            tools=descriptors,
        )

        for _ in range(self.max_iterations):

            if not response.tool_calls:
                return response.content or ""

            results = []

            for call in response.tool_calls:

                request = ToolRequest(
                    tool_name=call.tool_name,
                    arguments=call.arguments,
                )

                result = self.executor.execute(request)

                results.append(
                    (call, result)
                )

            response = self.llm.continue_with_tool_results(
                results
            )

        raise RuntimeError(
            "Tool loop exceeded maximum iterations."
        )
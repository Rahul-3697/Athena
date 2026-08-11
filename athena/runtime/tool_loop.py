from athena.contracts.tool_request import ToolRequest
from athena.llms.tool_calling import BaseToolCallingLLM
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry


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

        answer, tool_calls = self.llm.generate(
            prompt=prompt,
            tools=descriptors,
        )

        for _ in range(self.max_iterations):

            if not tool_calls:
                return answer or ""

            results = []

            for call in tool_calls:

                request = ToolRequest(
                    tool_name=call.tool_name,
                    arguments=call.arguments,
                )

                result = self.executor.execute(request)

                results.append(
                    (call, result)
                )

            answer, tool_calls = (
                self.llm.continue_with_tool_results(
                    results
                )
            )

        raise RuntimeError(
            "Tool loop exceeded maximum iterations."
        )
from athena.contracts.tool_request import ToolRequest
from athena.llms.tool_calling import BaseToolCallingLLM
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry
from athena.contracts.llm_response import LLMResponse
from athena.runtime.execution_state import ExecutionState
from athena.runtime.execution_status import ExecutionStatus
from athena.runtime.execution_policy import ExecutionPolicy
from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult
from athena.runtime.retry_policy import RetryPolicy
from athena.runtime.timeout_policy import TimeoutPolicy
from athena.runtime.tool_runner import ToolRunner

class ToolLoop:
    """
    Executes an iterative LLM-driven Tool loop.
    """

    def __init__(
        self,
        llm: BaseToolCallingLLM,
        registry: ToolRegistry,
        tool_runner: ToolRunner,
        policy: ExecutionPolicy | None = None,
    ):
        self.llm = llm
        self.registry = registry
        self.tool_runner = tool_runner

        self.policy = (
            policy or ExecutionPolicy()
        )

        self.last_state: ExecutionState | None = None

    def run(self, prompt: str) -> str:
        from concurrent.futures import (
            ThreadPoolExecutor,
            TimeoutError,
        )

        state = ExecutionState(
            goal=prompt
        )

        self.last_state = state
        state.status = ExecutionStatus.RUNNING

        descriptors = self.registry.descriptors()

        response = self.llm.generate(
            prompt=prompt,
            tools=descriptors,
        )

        for _ in range(self.policy.max_iterations):

            # LLM has produced the final answer
            if not response.tool_calls:

                state.status = ExecutionStatus.COMPLETED

                return response.content or ""

            state.status = ExecutionStatus.WAITING_FOR_TOOL

            results = []

            for call in response.tool_calls:

                # Enforce total Tool-call limit
                if len(state.tool_calls) >= self.policy.max_tool_calls:

                    state.status = ExecutionStatus.FAILED

                    raise RuntimeError(
                        "Tool loop exceeded maximum tool calls."
                    )

                state.tool_calls.append(call)

                request = ToolRequest(
                    tool_name=call.tool_name,
                    arguments=call.arguments,
                )

                result = self.tool_runner.run(request)

                state.tool_results.append(result)

                results.append(
                    (call, result)
                )

            state.iteration += 1

            state.status = ExecutionStatus.RUNNING

            response = (
                self.llm.continue_with_tool_results(
                    results
                )
            )

        state.status = ExecutionStatus.MAX_ITERATIONS

        raise RuntimeError(
            "Tool loop exceeded maximum iterations."
        )
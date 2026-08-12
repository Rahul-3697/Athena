from athena.contracts.llm_response import LLMResponse
from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult

from athena.runtime.execution_policy import ExecutionPolicy
from athena.runtime.execution_status import ExecutionStatus

from athena.runtime.tool_loop import ToolLoop

class FakeLLM:

    def generate(self, prompt, tools):

        return LLMResponse(
            content="Final answer",
            tool_calls=[],
        )

    def continue_with_tool_results(self, results):

        return LLMResponse(
            content="Final answer",
            tool_calls=[],
        )

class FakeRegistry:

    def descriptors(self):
        return []


class FakeExecutor:

    def execute(self, request):

        return ToolResult(
            success=True,
            data={"message": "executed"},
            error=None,
        )

def test_successful_execution():

    llm = FakeLLM()
    registry = FakeRegistry()
    executor = FakeExecutor()

    policy = ExecutionPolicy(
        max_iterations=3,
        max_tool_calls=10,
    )

    loop = ToolLoop(
        llm=llm,
        registry=registry,
        executor=executor,
        policy=policy,
    )

    result = loop.run(
        "Test runtime"
    )

    assert result == "Final answer"

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.COMPLETED
    assert state.iteration == 0
    assert state.tool_calls == []
    assert state.tool_results == []

    print("PASS: successful execution")
    print("Status:", state.status)
    print("Iteration:", state.iteration)

if __name__ == "__main__":
    test_successful_execution()
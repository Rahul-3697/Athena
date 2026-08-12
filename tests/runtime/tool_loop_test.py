from athena.contracts.llm_response import LLMResponse
from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult

from athena.runtime.execution_policy import ExecutionPolicy
from athena.runtime.execution_status import ExecutionStatus
from athena.runtime.tool_loop import ToolLoop
from athena.runtime.tool_runner import ToolRunner


class FakeLLM:
    def __init__(self):
        self.continue_calls = 0

    def generate(self, prompt, tools):
        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    call_id="loop-test-1",
                    tool_name="mock_tool",
                    arguments={"message": "hello"},
                )
            ],
        )

    def continue_with_tool_results(self, results):
        self.continue_calls += 1
        assert len(results) == 1

        call, result = results[0]

        assert call.call_id == "loop-test-1"
        assert result.success is True
        assert result.data == {"message": "tool executed"}

        return LLMResponse(
            content="Tool loop completed",
            tool_calls=[],
        )


class FakeRegistry:
    def descriptors(self):
        return []


class FakeExecutor:
    def execute(self, request):
        assert request.tool_name == "mock_tool"
        assert request.arguments == {"message": "hello"}

        return ToolResult(
            success=True,
            data={"message": "tool executed"},
            error=None,
        )


def test_tool_loop():
    llm = FakeLLM()

    tool_runner = ToolRunner(
        executor=FakeExecutor(),
    )

    loop = ToolLoop(
        llm=llm,
        registry=FakeRegistry(),
        tool_runner=tool_runner,
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=10,
        ),
    )

    result = loop.run("Test the Athena tool loop")

    assert result == "Tool loop completed"

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.COMPLETED
    assert state.iteration == 1
    assert len(state.tool_calls) == 1
    assert len(state.tool_results) == 1
    assert state.tool_results[0].success is True
    assert llm.continue_calls == 1

    print("PASS: ToolLoop orchestration")
    print("Status:", state.status)
    print("Iterations:", state.iteration)
    print("Tool calls:", len(state.tool_calls))
    print("Tool results:", len(state.tool_results))
    print("LLM continuation calls:", llm.continue_calls)


if __name__ == "__main__":
    test_tool_loop()
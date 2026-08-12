from athena.contracts.llm_response import LLMResponse
from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult

from athena.runtime.execution_policy import ExecutionPolicy
from athena.runtime.execution_status import ExecutionStatus

from athena.runtime.tool_loop import ToolLoop

class FakeToolLLM:

    def __init__(self):
        self.first_call = True

    def generate(self, prompt, tools):

        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    call_id="test-call-1",
                    tool_name="mock_tool",
                    arguments={
                        "message": "hello"
                    },
                )
            ],
        )

    def continue_with_tool_results(self, results):

        assert len(results) == 1

        call, result = results[0]

        assert call.call_id == "test-call-1"
        assert result.success is True

        return LLMResponse(
            content="Tool execution successful",
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

def test_tool_execution():

    loop = ToolLoop(
        llm=FakeToolLLM(),
        registry=FakeRegistry(),
        executor=FakeExecutor(),
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=10,
        ),
    )

    result = loop.run(
        "Use the test tool"
    )

    assert result == "Tool execution successful"

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.COMPLETED

    assert state.iteration == 1

    assert len(state.tool_calls) == 1
    assert len(state.tool_results) == 1

    print("PASS: tool execution")
    print("Status:", state.status)
    print("Iterations:", state.iteration)
    print("Tool calls:", len(state.tool_calls))
    print("Tool results:", len(state.tool_results))

if __name__ == "__main__":
    test_tool_execution()
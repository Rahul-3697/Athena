from athena.contracts.llm_response import LLMResponse
from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult

from athena.runtime.execution_policy import ExecutionPolicy
from athena.runtime.execution_status import ExecutionStatus

from athena.runtime.tool_loop import ToolLoop
from examples.runtime_test2 import test_tool_execution



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
    
class InfiniteToolLLM:

    def generate(self, prompt, tools):

        return self._tool_call()

    def continue_with_tool_results(self, results):

        return self._tool_call()

    def _tool_call(self):

        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    call_id="loop-call",
                    tool_name="mock_tool",
                    arguments={
                        "message": "loop"
                    },
                )
            ],
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
    
class FailingExecutor:

    def execute(self, request):

        raise RuntimeError(
            "Simulated tool failure"
        )

class FailureAwareLLM:

    def generate(self, prompt, tools):

        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    call_id="failure-test",
                    tool_name="mock_tool",
                    arguments={
                        "message": "fail"
                    },
                )
            ],
        )

    def continue_with_tool_results(self, results):

        assert len(results) == 1

        call, result = results[0]

        assert call.call_id == "failure-test"

        assert result.success is False
        assert result.data is None
        assert result.error == "Simulated tool failure"

        return LLMResponse(
            content="Recovered from tool failure",
            tool_calls=[],
        )

def test_max_iterations():

    loop = ToolLoop(
        llm=InfiniteToolLLM(),
        registry=FakeRegistry(),
        executor=FakeExecutor(),
        policy=ExecutionPolicy(
            max_iterations=2,
            max_tool_calls=10,
        ),
    )

    try:

        loop.run(
            "Force an infinite tool loop"
        )

        assert False, "Expected RuntimeError"

    except RuntimeError as exc:

        assert "maximum iterations" in str(exc)

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.MAX_ITERATIONS

    print("PASS: max iteration policy")
    print("Status:", state.status)
    print("Iterations:", state.iteration)

def test_tool_failure():

    loop = ToolLoop(
        llm=FailureAwareLLM(),
        registry=FakeRegistry(),
        executor=FailingExecutor(),
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=10,
        ),
    )

    result = loop.run(
        "Test tool failure"
    )

    assert result == "Recovered from tool failure"

    state = loop.last_state

    assert state is not None

    assert state.status == ExecutionStatus.COMPLETED

    assert len(state.tool_calls) == 1

    assert len(state.tool_results) == 1

    tool_result = state.tool_results[0]

    assert tool_result.success is False
    assert tool_result.error == "Simulated tool failure"

    print("PASS: tool failure handling")
    print("Status:", state.status)
    print("Tool calls:", len(state.tool_calls))
    print("Tool failures:", sum(
        1
        for result in state.tool_results
        if not result.success
    ))

if __name__ == "__main__":
    test_max_iterations()
    test_tool_failure()
from athena.contracts.llm_response import LLMResponse
from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult

from athena.runtime.execution_policy import ExecutionPolicy
from athena.runtime.execution_status import ExecutionStatus

from athena.runtime.tool_loop import ToolLoop
from examples.runtime_test2 import test_tool_execution
from athena.runtime.retry_policy import RetryPolicy
from athena.runtime.timeout_policy import TimeoutPolicy
import time


class SlowExecutor:

    def execute(self, request):

        time.sleep(5)

        return ToolResult(
            success=True,
            data={"message": "too slow"},
            error=None,
        )

class ExhaustionAwareLLM:

    def generate(self, prompt, tools):

        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    call_id="exhaustion-test",
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

        assert call.call_id == "exhaustion-test"

        assert result.success is False
        assert result.data is None
        assert result.error == "Permanent tool failure"

        return LLMResponse(
            content="Recovered from permanent tool failure",
            tool_calls=[],
        )

class AlwaysFailExecutor:

    def __init__(self):
        self.attempts = 0

    def execute(self, request):

        self.attempts += 1

        raise RuntimeError(
            "Permanent tool failure"
        )

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
    
class RetryExecutor:

    def __init__(self):
        self.attempts = 0

    def execute(self, request):

        self.attempts += 1

        if self.attempts == 1:
            raise RuntimeError(
                "Temporary tool failure"
            )

        return ToolResult(
            success=True,
            data={
                "message": "Recovered"
            },
            error=None,
        )
def test_tool_retry():

    executor = RetryExecutor()

    loop = ToolLoop(
        llm=FakeToolLLM(),
        registry=FakeRegistry(),
        executor=executor,
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=10,
        ),
        retry_policy=RetryPolicy(
            max_retries=2,
        ),
    )

    result = loop.run(
        "Test retry"
    )

    assert result == "Tool execution successful"

    assert executor.attempts == 2

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.COMPLETED

    assert len(state.tool_calls) == 1
    assert len(state.tool_results) == 1

    tool_result = state.tool_results[0]

    assert tool_result.success is True

    print("PASS: tool retry")
    print("Attempts:", executor.attempts)
    print("Status:", state.status)

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

def test_retry_exhaustion():

    executor = AlwaysFailExecutor()

    loop = ToolLoop(
        llm=ExhaustionAwareLLM(),
        registry=FakeRegistry(),
        executor=executor,
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=10,
        ),
        retry_policy=RetryPolicy(
            max_retries=2,
        ),
    )

    result = loop.run(
        "Test retry exhaustion"
    )

    assert result == "Recovered from permanent tool failure"

    assert executor.attempts == 3

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.COMPLETED

    tool_result = state.tool_results[0]

    assert tool_result.success is False
    assert tool_result.error == "Permanent tool failure"

    print("PASS: retry exhaustion")
    print("Attempts:", executor.attempts)
    print("Final tool success:", tool_result.success)

class TimeoutAwareLLM:

    def generate(self, prompt, tools):

        return LLMResponse(
            content=None,
            tool_calls=[
                ToolCall(
                    call_id="timeout-test",
                    tool_name="mock_tool",
                    arguments={
                        "message": "slow"
                    },
                )
            ],
        )

    def continue_with_tool_results(self, results):

        assert len(results) == 1

        call, result = results[0]

        assert call.call_id == "timeout-test"

        assert result.success is False
        assert result.data is None
        assert "timed out" in result.error

        return LLMResponse(
            content="Recovered from timeout",
            tool_calls=[],
        )

def test_tool_timeout():

    loop = ToolLoop(
        llm=TimeoutAwareLLM(),
        registry=FakeRegistry(),
        executor=SlowExecutor(),
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=10,
        ),
        retry_policy=RetryPolicy(
            max_retries=0,
        ),
        timeout_policy=TimeoutPolicy(
            timeout_seconds=1,
        ),
    )

    result = loop.run(
        "Test tool timeout"
    )

    assert result == "Recovered from timeout"

    state = loop.last_state

    assert state is not None
    assert state.status == ExecutionStatus.COMPLETED

    tool_result = state.tool_results[0]

    assert tool_result.success is False
    assert "timed out" in tool_result.error

    print("PASS: tool timeout")
    print("Status:", state.status)
    print("Timeout result:", tool_result.error)

if __name__ == "__main__":
    test_max_iterations()
    # test_tool_failure()
    # test_tool_retry()
    test_tool_timeout()
    test_retry_exhaustion()
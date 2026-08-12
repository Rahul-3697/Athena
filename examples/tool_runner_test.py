import time

from athena.contracts.tool_request import ToolRequest
from athena.contracts.tool_result import ToolResult

from athena.runtime.retry_policy import RetryPolicy
from athena.runtime.timeout_policy import TimeoutPolicy
from athena.runtime.tool_runner import ToolRunner


class FakeExecutor:

    def execute(self, request: ToolRequest) -> ToolResult:

        return ToolResult(
            success=True,
            data={
                "message": "Tool executed successfully"
            },
            error=None,
        )


class FailingExecutor:

    def execute(self, request: ToolRequest) -> ToolResult:

        raise RuntimeError(
            "Simulated tool failure"
        )


class RetryExecutor:

    def __init__(self):

        self.attempts = 0

    def execute(self, request: ToolRequest) -> ToolResult:

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


class AlwaysFailExecutor:

    def __init__(self):

        self.attempts = 0

    def execute(self, request: ToolRequest) -> ToolResult:

        self.attempts += 1

        raise RuntimeError(
            "Permanent tool failure"
        )


class SlowExecutor:

    def execute(self, request: ToolRequest) -> ToolResult:

        time.sleep(5)

        return ToolResult(
            success=True,
            data={
                "message": "Too slow"
            },
            error=None,
        )


def create_request():

    return ToolRequest(
        tool_name="mock_tool",
        arguments={
            "message": "test"
        },
    )


def test_success():

    runner = ToolRunner(
        executor=FakeExecutor(),
        retry_policy=RetryPolicy(
            max_retries=0
        ),
        timeout_policy=TimeoutPolicy(
            timeout_seconds=5
        ),
    )

    result = runner.run(
        create_request()
    )

    assert result.success is True

    assert result.data == {
        "message": "Tool executed successfully"
    }

    assert result.error is None

    print("PASS: tool runner success")


def test_failure():

    runner = ToolRunner(
        executor=FailingExecutor(),
        retry_policy=RetryPolicy(
            max_retries=0
        ),
        timeout_policy=TimeoutPolicy(
            timeout_seconds=5
        ),
    )

    result = runner.run(
        create_request()
    )

    assert result.success is False

    assert result.data is None

    assert result.error == (
        "Simulated tool failure"
    )

    print("PASS: tool runner failure")


def test_retry():

    executor = RetryExecutor()

    runner = ToolRunner(
        executor=executor,
        retry_policy=RetryPolicy(
            max_retries=2
        ),
        timeout_policy=TimeoutPolicy(
            timeout_seconds=5
        ),
    )

    result = runner.run(
        create_request()
    )

    assert result.success is True

    assert executor.attempts == 2

    print("PASS: tool runner retry")

    print(
        "Attempts:",
        executor.attempts
    )


def test_retry_exhaustion():

    executor = AlwaysFailExecutor()

    runner = ToolRunner(
        executor=executor,
        retry_policy=RetryPolicy(
            max_retries=2
        ),
        timeout_policy=TimeoutPolicy(
            timeout_seconds=5
        ),
    )

    result = runner.run(
        create_request()
    )

    assert result.success is False

    assert result.data is None

    assert result.error == (
        "Permanent tool failure"
    )

    assert executor.attempts == 3

    print(
        "PASS: tool runner retry exhaustion"
    )

    print(
        "Attempts:",
        executor.attempts
    )


def test_timeout():

    runner = ToolRunner(
        executor=SlowExecutor(),
        retry_policy=RetryPolicy(
            max_retries=0
        ),
        timeout_policy=TimeoutPolicy(
            timeout_seconds=1
        ),
    )

    result = runner.run(
        create_request()
    )

    assert result.success is False

    assert result.data is None

    assert "timed out" in result.error

    print("PASS: tool runner timeout")

    print(
        "Timeout result:",
        result.error
    )


if __name__ == "__main__":

    test_success()

    test_failure()

    test_retry()

    test_retry_exhaustion()

    test_timeout()
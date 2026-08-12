from concurrent.futures import (
    ThreadPoolExecutor,
    TimeoutError,
)

from athena.contracts.tool_request import ToolRequest
from athena.contracts.tool_result import ToolResult

from athena.runtime.retry_policy import RetryPolicy
from athena.runtime.timeout_policy import TimeoutPolicy

from athena.tools.tool_executor import ToolExecutor


class ToolRunner:

    def __init__(
        self,
        executor: ToolExecutor,
        retry_policy: RetryPolicy | None = None,
        timeout_policy: TimeoutPolicy | None = None,
    ):
        self.executor = executor

        self.retry_policy = (
            retry_policy or RetryPolicy()
        )

        self.timeout_policy = (
            timeout_policy or TimeoutPolicy()
        )

    def run(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        result = None

        for attempt in range(
            self.retry_policy.max_retries + 1
        ):

            try:

                with ThreadPoolExecutor(
                    max_workers=1
                ) as pool:

                    future = pool.submit(
                        self.executor.execute,
                        request,
                    )

                    result = future.result(
                        timeout=(
                            self.timeout_policy
                            .timeout_seconds
                        )
                    )

                break

            except TimeoutError:

                if (
                    attempt
                    >= self.retry_policy.max_retries
                ):

                    result = ToolResult(
                        success=False,
                        data=None,
                        error=(
                            "Tool execution timed out "
                            f"after "
                            f"{self.timeout_policy.timeout_seconds}"
                            " seconds"
                        ),
                    )

            except Exception as exc:

                if (
                    attempt
                    >= self.retry_policy.max_retries
                ):

                    result = ToolResult(
                        success=False,
                        data=None,
                        error=str(exc),
                    )

        return result
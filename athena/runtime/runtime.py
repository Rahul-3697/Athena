from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.tool_request import ToolRequest
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry


class Runtime:

    def __init__(
        self,
        registry: ToolRegistry,
        executor: ToolExecutor,
    ):
        self.registry = registry
        self.executor = executor

    def execute(self, plan: ExecutionPlan):

        print("\n" + "=" * 60)
        print("ATHENA RUNTIME")
        print("=" * 60)

        print("\nExecution Plan:")
        print("-" * 60)

        for index, step in enumerate(plan.steps, start=1):

            print(f"\nStep {index}")
            print(f"  ID          : {step.step}")
            print(f"  Description : {step.description}")
            print(f"  Target      : {step.target}")
            print(f"  Arguments   : {step.arguments}")

        print("\n" + "-" * 60)
        print("EXECUTION")
        print("-" * 60)

        results = []

        for index, step in enumerate(plan.steps, start=1):

            print(f"\n[{index}] Executing: {step.step}")

            # Intelligence Plan → Runtime Request
            # Validate target
            if not self.registry.has(step.target):
                print(
                    f"    FAILED: target '{step.target}' "
                    "is not registered."
                )
                continue

            request = ToolRequest(
                tool_name=step.target,
                arguments=step.arguments,
            )

            print(f"    Target: {request.tool_name}")
            print(f"    Args  : {request.arguments}")

            # Runtime → Tool Executor
            result = self.executor.execute(request)

            print(f"    Success: {result.success}")

            if result.data is not None:
                print(f"    Result : {result.data}")

            if result.error is not None:
                print(f"    Error  : {result.error}")

            results.append(result)

        print("\n" + "=" * 60)
        print("RUNTIME COMPLETE")
        print("=" * 60)

        return results
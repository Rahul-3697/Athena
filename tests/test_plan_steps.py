from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.plan_step import PlanStep

from athena.runtime.runtime import Runtime
from athena.tools.builtin.calculator import CalculatorTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry


def main():

    # --------------------------------
    # 1. Runtime capabilities
    # --------------------------------

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    executor = ToolExecutor(
        registry=registry
    )

    runtime = Runtime(
        registry=registry,
        executor=executor,
    )

    # --------------------------------
    # 2. Intelligence-produced Plan
    # --------------------------------

    plan = ExecutionPlan(
        steps=[
            PlanStep(
                step="calculate_expression",
                description="Calculate 12 * 8 + 2",
                target="calculator",
                arguments={
                    "expression": "12 * 8 + 2"
                },
            )
        ]
    )

    # --------------------------------
    # 3. Execute Plan
    # --------------------------------

    results = runtime.execute(plan)

    # --------------------------------
    # 4. Final result
    # --------------------------------

    print("\nFinal Results:")
    print("-" * 60)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
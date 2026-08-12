from athena.contracts.tool_request import ToolRequest

from athena.runtime.tool_runner import ToolRunner

from athena.tools.builtin.calculator import CalculatorTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry


def test_calculator_pipeline():

    # 1. Register Tool
    registry = ToolRegistry()

    calculator = CalculatorTool()

    registry.register(calculator)

    # 2. Verify discovery
    assert registry.has("calculator")

    assert "calculator" in (
        registry.list_tools()
    )

    descriptors = registry.descriptors()

    assert len(descriptors) == 1

    assert descriptors[0].name == "calculator"

    # 3. Create Executor
    executor = ToolExecutor(
        registry=registry
    )

    # 4. Create Runtime ToolRunner
    runner = ToolRunner(
        executor=executor
    )

    # 5. Create ToolRequest
    request = ToolRequest(
        tool_name="calculator",
        arguments={
            "expression": "25 * (4 + 2)"
        },
    )

    # 6. Execute through full pipeline
    result = runner.run(request)

    # 7. Validate result
    assert result.success is True

    assert result.data["expression"] == (
        "25 * (4 + 2)"
    )

    assert result.data["result"] == 150

    assert result.error is None

    print(
        "PASS: calculator pipeline"
    )

    print(
        "Registered tools:",
        registry.list_tools()
    )

    print(
        "Tool:",
        descriptors[0].name
    )

    print(
        "Result:",
        result.data
    )


if __name__ == "__main__":

    test_calculator_pipeline()
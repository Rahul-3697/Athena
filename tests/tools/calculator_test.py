from athena.contracts.tool_input import ToolInput
from athena.tools.builtin.calculator import CalculatorTool


def test_calculator():

    tool = CalculatorTool()

    result = tool.execute(
        ToolInput(
            name="calculator",
            arguments={
                "expression": "25 * (4 + 2)"
            },
        )
    )

    assert result.success is True

    assert result.data["expression"] == (
        "25 * (4 + 2)"
    )

    assert result.data["result"] == 150

    print("PASS: calculator")
    print("Expression:", result.data["expression"])
    print("Result:", result.data["result"])


if __name__ == "__main__":
    test_calculator()
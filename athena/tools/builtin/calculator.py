import ast
import operator as op

from athena.contracts.tool_input import ToolInput
from athena.contracts.tool_result import ToolResult
from athena.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return (
            "Perform basic arithmetic calculations "
            "using numbers, +, -, *, /, %, and parentheses."
        )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": (
                        "Arithmetic expression to calculate."
                    ),
                }
            },
            "required": ["expression"],
            "additionalProperties": False,
        }

    def execute(
        self,
        tool_input: ToolInput,
    ) -> ToolResult:

        try:

            expression = tool_input.arguments.get(
                "expression"
            )

            if not isinstance(expression, str):
                return ToolResult(
                    success=False,
                    error=(
                        "'expression' must be a string."
                    ),
                )

            expression = expression.strip()

            if not expression:
                return ToolResult(
                    success=False,
                    error=(
                        "'expression' cannot be empty."
                    ),
                )

            result = self._evaluate(
                expression
            )

            return ToolResult(
                success=True,
                data={
                    "expression": expression,
                    "result": result,
                },
            )

        except Exception as exc:

            return ToolResult(
                success=False,
                error=str(exc),
            )

    @staticmethod
    def _evaluate(expression: str):

        operators = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Mod: op.mod,
            ast.USub: op.neg,
            ast.UAdd: op.pos,
        }

        def evaluate(node):

            if isinstance(
                node,
                ast.Expression,
            ):
                return evaluate(node.body)

            if isinstance(
                node,
                ast.Constant,
            ):
                if isinstance(
                    node.value,
                    (int, float),
                ):
                    return node.value

                raise ValueError(
                    "Only numeric values are allowed."
                )

            if isinstance(
                node,
                ast.BinOp,
            ):
                operator = operators.get(
                    type(node.op)
                )

                if operator is None:
                    raise ValueError(
                        "Unsupported arithmetic operator."
                    )

                return operator(
                    evaluate(node.left),
                    evaluate(node.right),
                )

            if isinstance(
                node,
                ast.UnaryOp,
            ):
                operator = operators.get(
                    type(node.op)
                )

                if operator is None:
                    raise ValueError(
                        "Unsupported unary operator."
                    )

                return operator(
                    evaluate(node.operand)
                )

            raise ValueError(
                "Invalid arithmetic expression."
            )

        tree = ast.parse(
            expression,
            mode="eval",
        )

        return evaluate(tree)
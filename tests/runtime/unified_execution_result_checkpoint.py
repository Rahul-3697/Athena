from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.plan_step import PlanStep
from athena.contracts.execution_state_records.execution_result import (
    ExecutionResult,
)

from athena.capabilities.capability_registry import CapabilityRegistry
from athena.capabilities.capability_resolver import CapabilityResolver

from athena.context.context import Context

from athena.runtime.runtime import Runtime

from athena.tools.base_tool import BaseTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry

from athena.contracts.tool_input import ToolInput
from athena.contracts.tool_result import ToolResult
from athena.tools.builtin.calculator import CalculatorTool


# ============================================================
# TEST TOOL
# ============================================================

# class CalculatorTool(BaseTool):

#     @property
#     def name(self):
#         return "calculator"

#     @property
#     def description(self):
#         return "Performs a simple calculation."

#     def execute(self, tool_input: ToolInput) -> ToolResult:

#         a = tool_input.arguments["a"]
#         b = tool_input.arguments["b"]

#         return ToolResult(
#             success=True,
#             data=a + b,
#         )


# ============================================================
# TEST CAPABILITY
# ============================================================

class DocumentReviewCapability:

    @property
    def name(self):
        return "document_review"

    @property
    def description(self):
        return "Reviews a document."

    @property
    def workflows(self):

        workflow = DocumentReviewWorkflow()

        return {
            "contract_review": workflow
        }

    @property
    def metadata(self):

        return {
            "domain": "legal"
        }


class DocumentReviewWorkflow:

    name = "contract_review"

    def run(self, context: Context):

        context.output = {
            "review_status": "completed",
            "risk_level": "medium",
            "findings": [
                "Missing termination clause"
            ],
        }

        return context


# ============================================================
# CHECKPOINT
# ============================================================

def run_checkpoint():

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 12")
    print("UNIFIED EXECUTION RESULT")
    print("=" * 60)

    # --------------------------------------------------------
    # Tool setup
    # --------------------------------------------------------

    tool_registry = ToolRegistry()

    calculator = CalculatorTool()

    tool_registry.register(calculator)

    tool_executor = ToolExecutor(
        tool_registry
    )

    # --------------------------------------------------------
    # Capability setup
    # --------------------------------------------------------

    capability_registry = CapabilityRegistry()

    capability = DocumentReviewCapability()

    capability_registry.register(capability)

    capability_resolver = CapabilityResolver(
        capability_registry
    )

    # --------------------------------------------------------
    # Runtime
    # --------------------------------------------------------

    runtime = Runtime(
        registry=tool_registry,
        executor=tool_executor,
        capability_registry=capability_registry,
        capability_resolver=capability_resolver,
    )

    # --------------------------------------------------------
    # Execution Plan
    # --------------------------------------------------------

    plan = ExecutionPlan(
        steps=[
            PlanStep(
                step="calculate",
                description="Calculate 10 + 20",
                target="calculator",
                arguments={
                    "expression": "20 + 30 * 2"
                },
            ),
            PlanStep(
                step="review_document",
                description="Review legal contract",
                target="document_review",
                arguments={
                    "workflow": "contract_review",
                },
            ),
        ]
    )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    results = runtime.execute(plan)


    execution_result, execution_record = results

    assert isinstance(
        execution_result,
        ExecutionResult,
    )

    assert execution_result.status == "completed"

    assert len(execution_result.output) == 2

    tool_output = execution_result.output[0]

    capability_output = execution_result.output[1]

    # assert tool_output["expression"] == "20 + 30 * 2"

    # assert tool_output["result"] == 80

    assert capability_output["review_status"] == "completed"

    assert capability_output["risk_level"] == "medium"

    assert len(
        capability_output["findings"]
    ) == 1


    assert execution_record.execution_id == (
    execution_result.execution_id
)

    assert len(execution_record.events) > 0

    event_types = [
    event.event_type
    for event in execution_record.events
]

    assert "ToolResolved" in event_types
    assert "ToolStarted" in event_types

    assert "CapabilityResolved" in event_types
    assert "WorkflowStarted" in event_types
    assert "WorkflowCompleted" in event_types

    print(tool_output)

    # --------------------------------------------------------
    # Basic result verification
    # --------------------------------------------------------

#     print("\n[1] RESULT VERIFICATION")
#     print("-" * 60)

#     print("\nDEBUG RESULTS")
#     print("-" * 60)

#     print(f"Results type : {type(results)}")
#     print(f"Results      : {results[:100]}")

#     for index, item in enumerate(results):
#         print(
#             f"Result {index + 1}: "
#             f"type={type(item)}, "
#             f"value={item}"
#         )

#     assert len(results) == 2

#     tool_result = results[0]
#     capability_result = results[1]

#     assert isinstance(
#         tool_result,
#         ExecutionResult,
#     )

#     assert isinstance(
#         capability_result,
#         ExecutionResult,
#     )

#     print("    Both executions returned ExecutionResult.")

#     # --------------------------------------------------------
#     # Tool result
#     # --------------------------------------------------------

#     print("\n[2] TOOL RESULT")
#     print("-" * 60)

#     assert tool_result.status == "completed"

#     assert tool_result.output == 30

#     assert (
#         tool_result.metadata["execution_type"]
#         == "tool"
#     )

#     assert (
#         tool_result.error is None
#     )

    # print(f"    Status : {tool_output.status}")
    # print(f"    Output : {tool_output.output}")
    # print(f"    Type   : {tool_output.metadata['execution_type']}")

#     # --------------------------------------------------------
#     # Capability result
#     # --------------------------------------------------------

    # print("\n[3] CAPABILITY RESULT")
    # print("-" * 60)

    # print(capability_output)

#     assert capability_result.status == "completed"

#     assert capability_result.output is not None

#     assert (
#         capability_result.output["review_status"]
#         == "completed"
#     )

#     assert (
#         capability_result.output["risk_level"]
#         == "medium"
#     )

#     assert len(
#         capability_result.output["findings"]
#     ) == 1

#     assert (
#         capability_result.metadata["execution_type"]
#         == "capability"
#     )

    # print(
    #     f"    Status : {capability_output.review_status}"
    # )

    # print(
    #     f"    Output : {capability_output.finding}"
    # )

    # print(
    #     "    Type   : "
    #     f"{capability_output.metadata['execution_type']}"
    # )

#     # --------------------------------------------------------
#     # Boundary verification
#     # --------------------------------------------------------

    # print("\n[4] BOUNDARY VERIFICATION")
    # print("-" * 60)

#     assert isinstance(
#         tool_result,
#         ExecutionResult,
#     )

#     assert isinstance(
#         capability_result,
#         ExecutionResult,
#     )

#     assert (
#         tool_result.metadata["execution_type"]
#         != capability_result.metadata["execution_type"]
#     )

#     print(
#         "    ToolResult normalized to ExecutionResult."
#     )

#     print(
#         "    Capability Context normalized to "
#         "ExecutionResult."
#     )

#     print(
#         "    Both execution paths expose the same "
#         "external result contract."
#     )

#     # --------------------------------------------------------
#     # Complete
#     # --------------------------------------------------------

#     print("\n" + "=" * 60)
#     print("CHECKPOINT 12 PASSED")
#     print("=" * 60)


if __name__ == "__main__":
    run_checkpoint()
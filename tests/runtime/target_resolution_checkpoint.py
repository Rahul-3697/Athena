from athena.capabilities import (
    BaseCapability,
    CapabilityRegistry,
    CapabilityResolver,
)

from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.plan_step import PlanStep
from athena.contracts.tool_result import ToolResult

from athena.runtime.runtime import Runtime

from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry
from athena.tools.builtin.calculator import CalculatorTool

from athena.workflow.workflow import Workflow
from athena.skills.base_skill import BaseSkill

from athena.context.context import Context


# ============================================================
# Capability Skill
# ============================================================

class ContractReviewSkill(BaseSkill):

    def invoke(self, context: Context) -> Context:

        context.metadata["review_completed"] = True

        context.metadata["review_result"] = (
            "Contract review workflow executed successfully."
        )

        return context


# ============================================================
# Document Review Capability
# ============================================================

class DocumentReviewCapability(BaseCapability):

    @property
    def name(self) -> str:

        return "document_review"

    @property
    def description(self) -> str:

        return (
            "Review and analyze legal documents."
        )

    @property
    def workflows(self) -> dict[str, Workflow]:

        workflow = Workflow(
            "Contract Review"
        )

        workflow.add(
            ContractReviewSkill()
        )

        return {
            "contract_review": workflow
        }


# ============================================================
# Main Checkpoint
# ============================================================

def run_checkpoint():

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 6")
    print("Runtime Target Resolution")
    print("=" * 60)

    # ========================================================
    # 1. TOOL SETUP
    # ========================================================

    tool_registry = ToolRegistry()

    calculator = CalculatorTool()

    tool_registry.register(
        calculator
    )

    tool_executor = ToolExecutor(
        tool_registry
    )

    print("\n[1] Tool Runtime")

    print(
        f"    Registered : "
        f"{tool_registry.list_tools()}"
    )

    # ========================================================
    # 2. CAPABILITY SETUP
    # ========================================================

    capability_registry = CapabilityRegistry()

    document_review = (
        DocumentReviewCapability()
    )

    capability_registry.register(
        document_review
    )

    capability_resolver = CapabilityResolver(
        capability_registry
    )

    print("\n[2] Capability Runtime")

    print(
        f"    Registered : "
        f"{capability_registry.list_capabilities()}"
    )

    # ========================================================
    # 3. CREATE RUNTIME
    # ========================================================

    runtime = Runtime(
        registry=tool_registry,
        executor=tool_executor,
        capability_registry=capability_registry,
        capability_resolver=capability_resolver,
    )

    # ========================================================
    # 4. TOOL PLAN
    # ========================================================

    tool_step = PlanStep(
        step="calculate_test",
        description="Calculate a test expression.",
        target="calculator",
        arguments={
            "expression": "10 + 20 * 2"
        },
    )

    tool_plan = ExecutionPlan(
        steps=[tool_step]
    )

    print("\n[3] Tool Execution Test")

    # tool_results = runtime.execute(
    #     tool_plan
    # )
    tool_results, execution_record = runtime.execute(
        tool_plan
    )   
    
    print("\nFINAL RESULT")
    print(tool_results.status)
    print(tool_results.execution_id)

    print("\nEXECUTION HISTORY")
    for event in execution_record.events:
        print(event.event_type)

    # ========================================================
    # 5. CAPABILITY PLAN
    # ========================================================

    capability_step = PlanStep(
        step="review_document",
        description=(
            "Review this contract for risky clauses."
        ),
        target="document_review",
        arguments={
            "workflow": "contract_review"
        },
    )

    capability_plan = ExecutionPlan(
        steps=[capability_step]
    )

    print("\n[4] Capability Execution Test")

    # capability_results = runtime.execute(
    #     capability_plan
    # )
    capability_results, execution_record = runtime.execute(
        capability_plan
    )   

    print("\nFINAL RESULT")
    print(capability_results.status)
    print(capability_results.execution_id)

    print("\nEXECUTION HISTORY")
    for event in execution_record.events:
        print(event.event_type)

    # ========================================================
    # 6. VALIDATE TOOL RESULT
    # ========================================================

    tool_success = (
        # len(tool_results) == 1
        # and isinstance(
        #     tool_results[0],
        #     ToolResult
        # )
        tool_results[0].success
        and tool_results[0].data["result"] == 50
    )

    # ========================================================
    # 7. VALIDATE CAPABILITY RESULT
    # ========================================================

    capability_success = (
        len(capability_results) == 1
        and isinstance(
            capability_results[0],
            Context
        )
        and capability_results[0].metadata.get(
            "review_completed"
        )
        is True
        and capability_results[0].metadata.get(
            "capability"
        )
        == "document_review"
        and capability_results[0].metadata.get(
            "workflow"
        )
        == "contract_review"
    )

    # ========================================================
    # 8. CHECKPOINT RESULT
    # ========================================================

    print("\n" + "=" * 60)
    print("CHECKPOINT VALIDATION")
    print("=" * 60)

    print(
        "\n[Tool Path]"
    )

    print(
        f"    Calculator executed : "
        f"{tool_success}"
    )

    if tool_success:

        print(
            "    ✓ Existing Tool → "
            "ToolExecutor path works"
        )

    else:

        print(
            "    ✗ Existing Tool path failed"
        )

    print(
        "\n[Capability Path]"
    )

    print(
        f"    Workflow executed   : "
        f"{capability_success}"
    )

    if capability_success:

        print(
            "    ✓ Capability → "
            "Resolver → Workflow path works"
        )

    else:

        print(
            "    ✗ Capability execution failed"
        )

    success = (
        tool_success
        and capability_success
    )

    print("\n" + "-" * 60)

    if success:

        print(
            "✅ CHECKPOINT 6 PASSED"
        )

        print(
            "Runtime can resolve and execute "
            "Tool and Capability targets."
        )

    else:

        print(
            "❌ CHECKPOINT 6 FAILED"
        )

    print("-" * 60 + "\n")


# ============================================================
# Module Entry Point
# ============================================================

if __name__ == "__main__":
    run_checkpoint()
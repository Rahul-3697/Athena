from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.plan_step import PlanStep

from athena.capabilities.base_capability import BaseCapability
from athena.capabilities.capability_registry import CapabilityRegistry

from athena.context.context import Context
from athena.skills.base_skill import BaseSkill
from athena.workflow.workflow import Workflow

from athena.tools.tool_registry import ToolRegistry
from athena.tools.tool_executor import ToolExecutor

from athena.runtime.runtime import Runtime
from athena.workflow.workflow import Workflow


# ============================================================
# Skill
# ============================================================

class ReviewSkill(BaseSkill):

    def invoke(self, context: Context) -> Context:

        context.metadata["review_status"] = "completed"

        context.metadata["findings"] = [
            "Missing termination clause",
            "Liability clause requires review",
        ]

        context.metadata["risk_level"] = "medium"
        context.metadata["outcome"] = "success"

        return context


# ============================================================
# Capability
# ============================================================

# ============================================================
# Capability
# ============================================================

class DocumentReviewCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "document_review"

    @property
    def description(self) -> str:
        return "Reviews a document and produces structured findings."

    @property
    def workflows(self) -> dict[str, Workflow]:

        return {
            "contract_review": (
                Workflow(name="contract_review")
                .add(ReviewSkill())
            )
        }

    @property
    def metadata(self) -> dict:
        return {
            "domain": "legal",
            "type": "document_review",
        }

# ============================================================
# Main Checkpoint
# ============================================================

def run_checkpoint():

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 9")
    print("CAPABILITY EXECUTION RESULT")
    print("=" * 60)

    # --------------------------------------------------------
    # Registries
    # --------------------------------------------------------

    tool_registry = ToolRegistry()

    capability_registry = CapabilityRegistry()

    capability = DocumentReviewCapability()

    capability_registry.register(capability)

    print("\n[1] Capability Registration")

    print(
        f"    Registered : "
        f"{capability_registry.list_capabilities()}"
    )

    # --------------------------------------------------------
    # Tool Executor
    # --------------------------------------------------------

    executor = ToolExecutor(
        tool_registry
    )

    # --------------------------------------------------------
    # Runtime
    # --------------------------------------------------------

    runtime = Runtime(
        registry=tool_registry,
        executor=executor,
        capability_registry=capability_registry,
    )

    # --------------------------------------------------------
    # Execution Plan
    # --------------------------------------------------------

    plan = ExecutionPlan(
        steps=[
            PlanStep(
                step="review_contract",
                description="Review legal contract",
                target="document_review",
                arguments={
                    "workflow": "contract_review",
                    "document": "sample_contract.pdf",
                },
            )
        ]
    )

    print("\n[2] Execution Plan")

    for step in plan.steps:

        print(
            f"    Step   : {step.step}"
        )

        print(
            f"    Target : {step.target}"
        )

        print(
            f"    Args   : {step.arguments}"
        )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------

    execution_result, execution_record = (
        runtime.execute(plan)
    )

    # --------------------------------------------------------
    # Execution Result
    # --------------------------------------------------------

    print("\n[3] EXECUTION RESULT")
    print("-" * 60)

    print(
        f"    Execution ID : "
        f"{execution_result.execution_id}"
    )

    print(
        f"    Status       : "
        f"{execution_result.status}"
    )

    print(
        f"    Output       : "
        f"{execution_result.output}"
    )

    print(
        f"    Metadata     : "
        f"{execution_result.metadata}"
    )

    # --------------------------------------------------------
    # Execution History
    # --------------------------------------------------------

    print("\n[4] EXECUTION HISTORY")
    print("-" * 60)

    for index, event in enumerate(
        execution_record.events,
        start=1,
    ):

        print(
            f"    {index:02d}. "
            f"{event.event_type}"
            f" | target={event.target}"
            f" | status={event.status}"
        )

    # --------------------------------------------------------
    # Assertions
    # --------------------------------------------------------

    assert execution_result.execution_id == (
        execution_record.execution_id
    )

    assert execution_result.status == "completed"

    assert isinstance(
        execution_result.output,
        list,
    )

    assert len(
        execution_result.output
    ) == 1

    # capability_context = execution_result.output[0]

    # assert capability_context.metadata["review_status"] == (
    # "completed"
    # )

    # assert capability_context.metadata["risk_level"] == (
    # "medium"
    # )

    capability_output = execution_result.output[0]
    print(capability_output)
    # assert capability_output["review_status"] == "completed"

    assert capability_output.metadata["review_status"] == "completed"
    assert capability_output.metadata["risk_level"] == "medium"
    assert len(capability_output.metadata["findings"]) == 2

    # assert len(
    # capability_context.metadata["findings"]
    # ) == 2

    event_types = [
        event.event_type
        for event in execution_record.events
    ]

    assert "ExecutionStarted" in event_types
    assert "CapabilityResolved" in event_types
    assert "WorkflowStarted" in event_types
    assert "WorkflowCompleted" in event_types
    assert "ExecutionCompleted" in event_types

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CHECKPOINT 9 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_checkpoint()
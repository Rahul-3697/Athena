from athena.capabilities import (
    BaseCapability,
    CapabilityRegistry,
    CapabilityResolver,
)
from athena.context.context import Context
from athena.skills.base_skill import BaseSkill
from athena.workflow.workflow import Workflow


class ExampleSkill(BaseSkill):

    def invoke(self, context: Context) -> Context:
        context.metadata["executed"] = True
        context.metadata["message"] = "Capability workflow executed"
        return context


class ExampleCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "example"

    @property
    def description(self) -> str:
        return "Example capability for integration testing."

    @property
    def workflows(self) -> dict[str, Workflow]:
        workflow = Workflow("Example Workflow")
        workflow.add(ExampleSkill())

        return {
            "example_workflow": workflow,
        }


def run_checkpoint() -> None:

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 2")
    print("Capability → Workflow Execution")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create and register capability
    # ---------------------------------------------------------

    registry = CapabilityRegistry()

    capability = ExampleCapability()

    registry.register(capability)

    print("\n[1] Capability Registration")
    print(f"    Capability : {capability.name}")
    print(f"    Registered : {registry.has(capability.name)}")

    # ---------------------------------------------------------
    # 2. Discover capability
    # ---------------------------------------------------------

    print("\n[2] Capability Discovery")
    print(f"    Available  : {registry.list_capabilities()}")

    # ---------------------------------------------------------
    # 3. Resolve workflow
    # ---------------------------------------------------------

    resolver = CapabilityResolver(registry)

    workflow = resolver.resolve(
        capability_name="example",
        workflow_name="example_workflow",
    )

    print("\n[3] Workflow Resolution")
    print(f"    Workflow   : {workflow.name}")

    # ---------------------------------------------------------
    # 4. Execute existing Athena workflow
    # ---------------------------------------------------------

    context = Context()
    context.goal = "Run example capability"

    result = workflow.run(context)

    print("\n[4] Workflow Execution")
    print(f"    Executed   : {result.metadata.get('executed')}")
    print(f"    Message    : {result.metadata.get('message')}")

    # ---------------------------------------------------------
    # 5. Architectural validation
    # ---------------------------------------------------------

    success = (
        registry.has("example")
        and workflow.name == "Example Workflow"
        and result.metadata.get("executed") is True
    )

    print("\n" + "-" * 60)

    if success:
        print("✅ CHECKPOINT 2 PASSED")
        print("Capability successfully resolved and executed")
    else:
        print("❌ CHECKPOINT 2 FAILED")

    print("-" * 60 + "\n")


if __name__ == "__main__":
    run_checkpoint()
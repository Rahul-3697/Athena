from athena.capabilities import (
    BaseCapability,
    CapabilityDiscovery,
    CapabilityRegistry,
)
from athena.workflow.workflow import Workflow


class DocumentReviewCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "document_review"

    @property
    def description(self) -> str:
        return "Review and analyze documents."

    @property
    def workflows(self) -> dict[str, Workflow]:
        return {
            "contract_review": Workflow("Contract Review"),
            "clause_analysis": Workflow("Clause Analysis"),
        }


class ResearchCapability(BaseCapability):

    @property
    def name(self) -> str:
        return "research"

    @property
    def description(self) -> str:
        return "Research information and produce findings."

    @property
    def workflows(self) -> dict[str, Workflow]:
        return {
            "web_research": Workflow("Web Research"),
        }


def run_checkpoint() -> None:

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 3")
    print("Capability Discovery")
    print("=" * 60)

    registry = CapabilityRegistry()

    registry.register(DocumentReviewCapability())
    registry.register(ResearchCapability())

    discovery = CapabilityDiscovery(registry)

    capabilities = discovery.discover()

    print("\nAvailable Capabilities:")

    for capability in capabilities:
        print(f"\n[{capability.name}]")
        print(f"  {capability.description}")
        print("  Workflows:")

        for workflow in capability.workflows:
            print(f"    - {workflow}")

    success = (
        len(capabilities) == 2
        and any(c.name == "document_review" for c in capabilities)
        and any(c.name == "research" for c in capabilities)
    )

    print("\n" + "-" * 60)

    if success:
        print("✅ CHECKPOINT 3 PASSED")
        print("Athena can discover available capabilities")
    else:
        print("❌ CHECKPOINT 3 FAILED")

    print("-" * 60 + "\n")


if __name__ == "__main__":
    run_checkpoint()
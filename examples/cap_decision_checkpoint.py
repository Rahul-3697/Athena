from athena.capabilities import (
    BaseCapability,
    CapabilityDiscovery,
    CapabilityRegistry,
)
from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.decision_type import DecisionType
from athena.decision.base import BaseDecisionMaker
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


class ExampleCapabilityDecisionMaker(BaseDecisionMaker):

    def decide(self, request: AgentRequest) -> AgentDecision:

        capabilities = self.capability_discovery.discover()

        # Deterministic selection for the architectural checkpoint.
        # This is NOT our final intelligence mechanism.
        selected = next(
            capability
            for capability in capabilities
            if capability.name == "research"
        )

        return AgentDecision(
            type=DecisionType.SKILL,
            target=selected.name,
            arguments={
                "workflow": "contract_review",
            },
        )


def run_checkpoint():

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 4")
    print("Agent → Capability Decision")
    print("=" * 60)

    registry = CapabilityRegistry()

    registry.register(DocumentReviewCapability())
    registry.register(ResearchCapability())

    discovery = CapabilityDiscovery(registry)

    decision_maker = ExampleCapabilityDecisionMaker(
        capability_discovery=discovery
    )

    request = AgentRequest(
        goal="Research this contract for risky clauses."
    )

    decision = decision_maker.decide(request)

    print("\n[1] Agent Request")
    print(f"    Goal       : {request.goal}")

    print("\n[2] Available Capabilities")

    for capability in discovery.discover():
        print(f"    - {capability.name}")

    print("\n[3] Agent Decision")
    print(f"    Type       : {decision.type}")
    print(f"    Target     : {decision.target}")
    print(f"    Arguments  : {decision.arguments}")

    success = (
        decision.target == "research" 
        and decision.arguments["workflow"] ==  "contract_review"
    )

    print("\n" + "-" * 60)

    if success:
        print("✅ CHECKPOINT 4 PASSED")
        print("Agent can make a capability-aware decision")
    else:
        print("❌ CHECKPOINT 4 FAILED")

    print("-" * 60 + "\n")


if __name__ == "__main__":
    run_checkpoint()
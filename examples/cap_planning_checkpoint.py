from athena.capabilities import (
    BaseCapability,
    CapabilityDiscovery,
    CapabilityRegistry,
)
from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.decision_type import DecisionType
from athena.planning.default import DefaultPlanner
from athena.workflow.workflow import Workflow
from athena.decision.base import BaseDecisionMaker


# ============================================================
# Example Capabilities
# ============================================================

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


# ============================================================
# Deterministic Capability-Aware Decision Maker
# ============================================================

class ExampleCapabilityDecisionMaker(BaseDecisionMaker):

    def decide(self, request: AgentRequest) -> AgentDecision:

        capabilities = self.capability_discovery.discover()

        # ----------------------------------------------------
        # Deterministic selection for this checkpoint.
        #
        # This is NOT the final intelligence mechanism.
        # The purpose is only to prove that the decision layer
        # can consume discovered capabilities and produce a
        # capability-aware AgentDecision.
        # ----------------------------------------------------

        selected = next(
            capability
            for capability in capabilities
            if capability.name == "document_review"
        )

        return AgentDecision(
            type=DecisionType.SKILL,
            target=selected.name,
            arguments={
                "workflow": "contract_review",
            },
        )


# ============================================================
# Checkpoint 5
# Capability → Planning
# ============================================================

def run_checkpoint() -> None:

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 5")
    print("Capability → Planning")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Create Capability Registry
    # --------------------------------------------------------

    registry = CapabilityRegistry()

    registry.register(
        DocumentReviewCapability()
    )

    registry.register(
        ResearchCapability()
    )

    print("\n[1] Capability Registry")

    print(
        f"    Available  : "
        f"{registry.list_capabilities()}"
    )

    # --------------------------------------------------------
    # 2. Create Capability Discovery
    # --------------------------------------------------------

    discovery = CapabilityDiscovery(
        registry
    )

    print("\n[2] Capability Discovery")

    for capability in discovery.discover():

        print(
            f"    - {capability.name}"
        )

        print(
            f"      {capability.description}"
        )

        print(
            f"      Workflows: "
            f"{capability.workflows}"
        )

    # --------------------------------------------------------
    # 3. Create Capability-Aware Decision Maker
    # --------------------------------------------------------

    decision_maker = ExampleCapabilityDecisionMaker(
        capability_discovery=discovery
    )

    # --------------------------------------------------------
    # 4. Create Agent Request
    # --------------------------------------------------------

    request = AgentRequest(
        goal="Review this contract for risky clauses."
    )

    print("\n[3] Agent Request")

    print(
        f"    Goal       : "
        f"{request.goal}"
    )

    # --------------------------------------------------------
    # 5. Produce Agent Decision
    # --------------------------------------------------------

    decision = decision_maker.decide(
        request
    )

    print("\n[4] Agent Decision")

    print(
        f"    Type       : "
        f"{decision.type}"
    )

    print(
        f"    Target     : "
        f"{decision.target}"
    )

    print(
        f"    Arguments  : "
        f"{decision.arguments}"
    )

    # --------------------------------------------------------
    # 6. Create Execution Plan
    #
    # This uses Athena's EXISTING DefaultPlanner.
    # No capability-specific planner logic is added.
    # --------------------------------------------------------

    planner = DefaultPlanner()

    plan = planner.create_plan(
        decision
    )

    print("\n[5] Execution Plan")

    print(
        f"    Steps      : "
        f"{len(plan.steps)}"
    )

    # --------------------------------------------------------
    # 7. Inspect Generated PlanStep
    # --------------------------------------------------------

    step = plan.steps[0]

    print("\n[6] Plan Step")

    print(
        f"    Step       : "
        f"{step.step}"
    )

    print(
        f"    Description: "
        f"{step.description}"
    )

    print(
        f"    Target     : "
        f"{step.target}"
    )

    print(
        f"    Arguments  : "
        f"{step.arguments}"
    )

    # --------------------------------------------------------
    # 8. Validate Checkpoint
    # --------------------------------------------------------

    success = (
        len(plan.steps) == 1
        and step.target == "document_review"
        and step.arguments.get("workflow")
        == "contract_review"
    )

    print("\n" + "-" * 60)

    if success:

        print(
            "✅ CHECKPOINT 5 PASSED"
        )

        print(
            "Capability-aware decision "
            "successfully became a PlanStep."
        )

    else:

        print(
            "❌ CHECKPOINT 5 FAILED"
        )

        print(
            "Capability information was not "
            "preserved during planning."
        )

    print("-" * 60 + "\n")


# ============================================================
# Module Entry Point
# ============================================================

if __name__ == "__main__":
    run_checkpoint()
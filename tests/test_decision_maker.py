from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.decision_type import DecisionType

from athena.decision.default import DefaultDecisionMaker


def test_default_decision_maker():

    print("\n" + "=" * 60)
    print("ATHENA TEST: AgentRequest → DecisionMaker → AgentDecision")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create Request
    # ---------------------------------------------------------
    request = AgentRequest(
        goal="Investigate payment API failures",
        constraints={
            "environment": "production",
        },
    )

    print("\n[1] Agent Request")
    print(f"    Goal        : {request.goal}")
    print(f"    Constraints : {request.constraints}")

    # ---------------------------------------------------------
    # 2. Create Decision Maker
    # ---------------------------------------------------------
    decision_maker = DefaultDecisionMaker()

    print("\n[2] Decision Maker")
    print(f"    Component   : {decision_maker.__class__.__name__}")

    # ---------------------------------------------------------
    # 3. Generate Decision
    # ---------------------------------------------------------
    decision = decision_maker.decide(request)

    print("\n[3] Agent Decision")
    print(f"    Type        : {decision.type.value}")
    print(f"    Target      : {decision.target}")
    print(f"    Arguments   : {decision.arguments}")

    # ---------------------------------------------------------
    # 4. Validate
    # ---------------------------------------------------------
    assert decision.type == DecisionType.ANSWER
    assert decision.arguments["goal"] == request.goal

    print("\n[4] Validation")
    print("    ✓ Request successfully converted to Decision")

    print("\n" + "=" * 60)
    print("RESULT: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_default_decision_maker()
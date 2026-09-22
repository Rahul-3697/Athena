from athena.agent.agent import Agent

from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.decision_type import DecisionType


def test_agent_creates_decision():

    print("\n" + "=" * 60)
    print("ATHENA TEST: AgentRequest → AgentDecision")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create Agent
    # ---------------------------------------------------------
    agent = Agent(
        name="test-agent",
        workflow=None,
    )

    print("\n[1] Agent")
    print(f"    Name      : {agent.name}")

    # ---------------------------------------------------------
    # 2. Create Agent Request
    # ---------------------------------------------------------
    request = AgentRequest(
        goal="Investigate payment API failures",
        constraints={
            "environment": "production"
        },
    )

    print("\n[2] Agent Request")
    print(f"    Goal      : {request.goal}")
    print(f"    Constraints: {request.constraints}")

    # ---------------------------------------------------------
    # 3. Ask Agent to decide
    # ---------------------------------------------------------
    decision = agent.decide(request)

    print("\n[3] Agent Decision")
    print(f"    Type      : {decision.type.value}")
    print(f"    Target    : {decision.target}")
    print(f"    Arguments : {decision.arguments}")

    # ---------------------------------------------------------
    # 4. Validate
    # ---------------------------------------------------------
    assert decision.type == DecisionType.ANSWER
    assert decision.arguments["goal"] == request.goal

    print("\n[4] Validation")
    print("    ✓ AgentRequest successfully converted to AgentDecision")

    print("\n" + "=" * 60)
    print("RESULT: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_agent_creates_decision()
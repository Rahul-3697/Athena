from athena.agent.agent import Agent

from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.decision_type import DecisionType


def test_agent_request_to_execution_plan():

    print("\n" + "=" * 60)
    print("ATHENA TEST: Agent Lifecycle")
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
    print(f"    Planner   : {agent.planner.__class__.__name__}")

    # ---------------------------------------------------------
    # 2. Create Agent Request
    # ---------------------------------------------------------
    request = AgentRequest(
        goal="Investigate payment API failures",
        constraints={
            "environment": "production",
        },
    )

    print("\n[2] Agent Request")
    print(f"    Goal      : {request.goal}")
    print(f"    Constraints: {request.constraints}")

    # ---------------------------------------------------------
    # 3. Agent decides
    # ---------------------------------------------------------
    decision = agent.decide(request)

    print("\n[3] Agent Decision")
    print(f"    Type      : {decision.type.value}")
    print(f"    Target    : {decision.target}")
    print(f"    Arguments : {decision.arguments}")

    # ---------------------------------------------------------
    # 4. Agent creates plan
    # ---------------------------------------------------------
    plan = agent.plan(decision)

    # print("\n[4] Execution Plan")
    # print(f"    Steps     : {len(plan.steps)}")

    for step in plan.steps:
        # print(f"\n    Step {step.id}")
        print(f"      Description   : {step.description}")
        print(f"      Target  : {step.target}")
        print(f"      Args    : {step.arguments}")

    # ---------------------------------------------------------
    # 5. Validate lifecycle
    # ---------------------------------------------------------
    assert decision.type == DecisionType.ANSWER
    assert decision.arguments["goal"] == request.goal

    # assert len(plan.steps) == 1

    # step = plan.steps[0]

    assert step.arguments["goal"] == request.goal

    print("\n[5] Validation")
    print("    ✓ Request accepted")
    print("    ✓ Decision generated")
    print("    ✓ Plan generated")
    print("    ✓ Decision data preserved in plan")

    print("\n" + "=" * 60)
    print("RESULT: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_agent_request_to_execution_plan()
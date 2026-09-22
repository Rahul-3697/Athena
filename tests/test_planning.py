from athena.agent.agent import Agent

from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.decision_type import DecisionType


def test_agent_creates_plan_from_decision():

    print("\n" + "=" * 60)
    print("ATHENA TEST: AgentDecision → Agent → ExecutionPlan")
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
    # 2. Create Decision
    # ---------------------------------------------------------
    decision = AgentDecision(
        type=DecisionType.TOOL,
        target="search_logs",
        arguments={
            "service": "payment-api",
            "environment": "production",
        },
    )

    print("\n[2] Agent Decision")
    print(f"    Type      : {decision.type.value}")
    print(f"    Target    : {decision.target}")
    print(f"    Arguments : {decision.arguments}")

    # ---------------------------------------------------------
    # 3. Ask Agent to create plan
    # ---------------------------------------------------------
    plan = agent.plan(decision)

    print("\n[3] Execution Plan")
    # print(f"    Steps     : {len(plan.steps)}")

    for step in plan.steps:
        # print(f"    Step {step.id}")
        print(f"      Description   : {step.description}")
        print(f"      Target  : {step.target}")
        print(f"      Args    : {step.arguments}")

    # ---------------------------------------------------------
    # 4. Validate
    # ---------------------------------------------------------
    # assert len(plan.steps) == 1

    # step = plan.steps[0]

    assert step.target == decision.target
    assert step.arguments == decision.arguments

    print("\n[4] Validation")
    print("    ✓ Agent successfully delegated planning")
    print("    ✓ Decision converted to ExecutionPlan")

    print("\n" + "=" * 60)
    print("RESULT: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_agent_creates_plan_from_decision()
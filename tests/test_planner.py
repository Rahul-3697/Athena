from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.decision_type import DecisionType
from athena.planning.default import DefaultPlanner


def test_default_planner_creates_execution_plan():

    print("\n" + "=" * 60)
    print("ATHENA TEST: Decision → Execution Plan")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Create an Agent Decision
    # ---------------------------------------------------------
    decision = AgentDecision(
        type=DecisionType.TOOL,
        target="search_logs",
        arguments={
            "service": "payment-api",
            "environment": "production",
        },
    )

    print("\n[1] Agent Decision")
    print(f"    Type      : {decision.type.value}")
    print(f"    Target    : {decision.target}")
    print(f"    Arguments : {decision.arguments}")

    # ---------------------------------------------------------
    # 2. Create Planner
    # ---------------------------------------------------------
    planner = DefaultPlanner()

    print("\n[2] Planner")
    print(f"    Planner   : {planner.__class__.__name__}")

    # ---------------------------------------------------------
    # 3. Generate Execution Plan
    # ---------------------------------------------------------
    plan = planner.create_plan(decision)

    print("\n[3] Execution Plan")
    print(f"    Steps     : {len(plan.steps)}")

    # ---------------------------------------------------------
    # 4. Inspect generated Plan Step
    # ---------------------------------------------------------
    step = plan.steps[0]

    print("\n[4] Plan Step")
    print(f"    ID        : {step.id}")
    print(f"    Title     : {step.title}")
    print(f"    Target    : {step.target}")
    print(f"    Arguments : {step.arguments}")

    # ---------------------------------------------------------
    # 5. Validate
    # ---------------------------------------------------------
    assert len(plan.steps) == 1
    assert step.id == 1
    assert step.target == decision.target
    assert step.arguments == decision.arguments

    print("\n[5] Validation")
    print("    ✓ Decision successfully converted to ExecutionPlan")

    print("\n" + "=" * 60)
    print("RESULT: PASSED")
    print("=" * 60)


if __name__ == "__main__":
    test_default_planner_creates_execution_plan()
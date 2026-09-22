from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.plan_step import PlanStep

from athena.planning.base import BasePlanner


class DefaultPlanner(BasePlanner):
    """
    Default planner for Athena.

    Converts a single AgentDecision into an initial ExecutionPlan.
    """

    def create_plan(
        self,
        decision: AgentDecision,
    ) -> ExecutionPlan:

        step = PlanStep(
            step="execute_decision",
            description=f"Execute {decision.type.value}",
            target=decision.target,
            arguments=decision.arguments,
        )

        return ExecutionPlan(
            steps=[step]
        )
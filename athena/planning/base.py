from abc import ABC, abstractmethod

from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.execution_plan import ExecutionPlan


class BasePlanner(ABC):
    """
    Base interface for all Athena planners.

    A planner converts an AgentDecision into an ExecutionPlan.
    """

    @abstractmethod
    def create_plan(
        self,
        decision: AgentDecision,
    ) -> ExecutionPlan:
        """
        Create an execution plan from an agent decision.
        """
        pass
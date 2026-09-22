from athena.context.context import Context
from athena.workflow.workflow import Workflow
from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.decision_type import DecisionType
from athena.planning.base import BasePlanner
from athena.planning.default import DefaultPlanner
from athena.contracts.execution_plan import ExecutionPlan
from athena.decision.base import BaseDecisionMaker
from athena.decision.default import DefaultDecisionMaker

class Agent:

    def __init__(
        self,
        name: str,
        workflow: Workflow,
        Planner: BasePlanner | None = None,
        DecisionMaker: BaseDecisionMaker | None = None,
    ):
        self.name = name
        self.workflow = workflow
        self.planner = Planner or DefaultPlanner()
        self.decision_maker = DecisionMaker or DefaultDecisionMaker()

    def decide(
        self,
        request: AgentRequest
    ) -> AgentDecision:
        """
        Produce an AgentDecision from an AgentRequest.
        """
        return self.decision_maker.decide(request)

    def plan(
            self,
            decision: AgentDecision
    ) -> ExecutionPlan:
        """
        Create a plan from an agent decision.
        """
        return self.planner.create_plan(decision)
    

    def invoke(self, goal: str) -> str:

        context = Context()

        context.goal = goal

        context = self.workflow.run(context)

        return context.report.content


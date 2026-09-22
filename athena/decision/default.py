from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.agent_request import AgentRequest
from athena.contracts.agent.decision_type import DecisionType

from athena.decision.base import BaseDecisionMaker


class DefaultDecisionMaker(BaseDecisionMaker):
    """
    Default decision maker used during the foundation phase.

    This implementation does not use an LLM yet.
    """

    def decide(
        self,
        request: AgentRequest,
    ) -> AgentDecision:

        return AgentDecision(
            type=DecisionType.ANSWER,
            arguments={
                "goal": request.goal,
            },
        )
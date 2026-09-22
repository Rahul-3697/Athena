from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.llm_response import LLMResponse


class LLMResponseInterpreter:
    """
    Converts an LLMResponse into an AgentDecision.

    This component is responsible only for interpreting
    the structured response produced by an LLM.
    """

    def interpret(
        self,
        response: LLMResponse,
    ) -> AgentDecision:
        raise NotImplementedError
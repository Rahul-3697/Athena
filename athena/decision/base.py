from abc import ABC, abstractmethod

from athena.contracts.agent.agent_decision import AgentDecision
from athena.contracts.agent.agent_request import AgentRequest

from athena.capabilities.capability_discovery import CapabilityDiscovery

class BaseDecisionMaker(ABC):
    """
    Base interface for components responsible for
    converting an AgentRequest into an AgentDecision.
    """

    def __init__(
        self,
        capability_discovery: CapabilityDiscovery | None = None,
    ):
        self.capability_discovery = capability_discovery


    @abstractmethod
    def decide(
        self,
        request: AgentRequest,
    ) -> AgentDecision:
        """
        Produce an AgentDecision from an AgentRequest.
        """
        pass
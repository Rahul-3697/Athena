from abc import ABC, abstractmethod
from athena.models.state import AgentState


class PipelineComponent(ABC):
    """
    Base class for every pipeline component.
    """

    @abstractmethod
    def execute(self, state: AgentState) -> None:
        """
        Receives the shared state,
        performs its task,
        updates the state.
        """
        pass
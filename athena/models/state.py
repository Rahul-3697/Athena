"""
Shared state for the Research Agent.

Every component receives the same AgentState instance
and updates it during execution.
"""

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    Shared execution state.
    """

    goal: str

    plan: list[str] = Field(default_factory=list)

    search_results: list[str] = Field(default_factory=list)

    report: str = ""

    search_count: int = 0

    is_information_sufficient: bool = False

    
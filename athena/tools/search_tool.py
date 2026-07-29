"""
Mock Search Tool.
"""
from athena.pipeline.component import PipelineComponent
from athena.models.state import AgentState


class SearchTool(PipelineComponent):
    """
    Search Tool Component

    Responsible for performing the search.
    """

    def execute(self, state: AgentState) -> None:

        state.search_results = [
            f"Result 1 about {state.goal}",
            f"Result 2 about {state.goal}",
            f"Result 3 about {state.goal}",
        ]
        state.search_count += 1
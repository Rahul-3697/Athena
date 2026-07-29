"""
Planner Component

Responsible for converting a goal into
a simple execution plan.
"""

from athena.models.state import AgentState


class Planner:

    def execute(self, state: AgentState) -> None:
        """
        Generate a basic execution plan.
        """

        state.plan = [
            "Search for information",
            "Analyze findings",
            "Generate report",
        ]
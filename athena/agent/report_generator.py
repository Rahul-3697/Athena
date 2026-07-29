"""
Report Generator.
"""
from athena.pipeline.component import PipelineComponent
from athena.models.state import AgentState


class ReportGenerator(PipelineComponent):
    """
    Report Generator Component

    Responsible for generating the final report.
    """

    def execute(self, state: AgentState) -> None:

        report = f"""
Research Goal
--------------
{state.goal}

Execution Plan
--------------
"""

        for step in state.plan:
            report += f"- {step}\n"

        report += "\nSearch Results\n--------------\n"

        for result in state.search_results:
            report += f"- {result}\n"

        state.report = report
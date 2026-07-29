"""
Research Agent

Coordinates the workflow.
"""

from athena.agent.planner import Planner
from athena.agent.report_generator import ReportGenerator
from athena.models.state import AgentState
from athena.tools.search_tool import SearchTool


class Pipeline:
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def execute(self, state):
        for component in self.components:
            component.execute(state)

class ResearchAgent:

    def __init__(self):
        self.pipeline = Pipeline()

        self.pipeline.add(Planner())
        self.pipeline.add(SearchTool())
        self.pipeline.add(ReportGenerator())

#     def run(self, goal):
#         state = AgentState(goal=goal)

#         self.pipeline.execute(state)

#         return state.report

    def run(self, goal):

        state = AgentState(goal=goal)

        # Planning Stage
        self.pipeline.execute(state)

        # Research Stage
        # while not state.is_information_sufficient:

        #     self.pipeline.execute(state)

        # Reporting Stage
        self.pipeline.execute(state)

        return state.report

    
from athena.context.context import Context
from athena.workflow.workflow import Workflow


class Agent:

    def __init__(
        self,
        name: str,
        workflow: Workflow
    ):
        self.name = name
        self.workflow = workflow

    def invoke(self, goal: str) -> str:

        context = Context()

        context.goal = goal

        context = self.workflow.run(context)

        return context.report.content


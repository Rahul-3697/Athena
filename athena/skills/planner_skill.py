from athena.context.context import Context
from athena.skills.base_skill import BaseSkill

from athena.prompts import planner
from athena.utils.parser import Parser


class PlannerSkill(BaseSkill):

    def __init__(self, llm):
        self.llm = llm

    def invoke(self, context: Context) -> Context:

        prompt = planner.build(context.goal)

        response = self.llm.invoke(prompt)

        context.plan = Parser.to_execution_plan(response)

        return context
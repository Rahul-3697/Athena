from typing import List

from athena.context.context import Context
from athena.skills.base_skill import BaseSkill


class Workflow:
    """
    A Workflow is an ordered collection of Skills.

    Each Skill receives the shared Context,
    performs its task, and returns the updated Context.
    """

    def __init__(self, name: str = "workflow"):
        self.name = name
        self.skills: List[BaseSkill] = []

    def add(self, skill: BaseSkill) -> "Workflow":
        """
        Add a skill to the workflow.
        """

        self.skills.append(skill)
        return self

    def run(self, context: Context) -> Context:
        """
        Execute all skills sequentially.
        """

        for skill in self.skills:
            context = skill.invoke(context)

        return context
    
    def __iter__(self):
        """
        Return an iterator over the skills in the workflow.
        """
        return iter(self.skills)
    
    @property
    def size(self):
        """
        Return the number of skills in the workflow.
        """
        return len(self.skills)
    
    
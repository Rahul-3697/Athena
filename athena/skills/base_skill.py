from abc import ABC, abstractmethod

from athena.context.context import Context


class BaseSkill(ABC):

    @abstractmethod
    def invoke(self, context: Context) -> Context:
        """
        Execute the skill and return the updated context.
        """
        pass
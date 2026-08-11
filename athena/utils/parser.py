import json

from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.plan_step import PlanStep


class Parser:

    @staticmethod
    def to_execution_plan(response: str) -> ExecutionPlan:

        data = json.loads(response)

        steps = [
            PlanStep(
                id=item["id"],
                title=item["title"]
            )
            for item in data["steps"]
        ]

        return ExecutionPlan(steps=steps)
    

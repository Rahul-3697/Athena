from dataclasses import dataclass, field

from athena.contracts.plan_step import PlanStep


@dataclass
class ExecutionPlan:
    steps: list[PlanStep] = field(default_factory=list)
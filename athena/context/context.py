from dataclasses import dataclass, field
from typing import Any

from athena.contracts.execution_plan import ExecutionPlan
from athena.contracts.report import Report


@dataclass
class Context:

    goal: str = ""

    plan: ExecutionPlan | None = None

    report: Report | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value):

        setattr(self, key, value)

    def get(self, key: str):

        return getattr(self, key)
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class PlanStep:
    """Represents a single step in a plan.
    
    | Field         | Responsibility                          |
    | ------------- | --------------------------------------- |
    | `step`        | Stable identifier for the step          |
    | `description` | What the step is intended to accomplish |
    | `target`      | Capability Runtime should resolve       |
    | `arguments`   | Inputs required by that capability      |

    """
    step: str
    description: str
    target: str
    arguments: dict[str, Any] = field(default_factory=dict)
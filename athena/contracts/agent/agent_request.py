from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentRequest:
    goal: str
    constraints: dict[str, Any] = field(default_factory=dict)
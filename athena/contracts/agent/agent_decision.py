from dataclasses import dataclass, field
from typing import Any
from athena.contracts.agent.decision_type import DecisionType

@dataclass
class AgentDecision:
    type: DecisionType
    target: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
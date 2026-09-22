from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CapabilityDescriptor:
    name: str
    description: str
    workflows: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
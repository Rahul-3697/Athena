from dataclasses import dataclass
from typing import Any
# from athena.runtime.execution_state import ExecutionState


@dataclass
class AgentResult:
    success: bool
    output: Any = None
    execution_state: Any | None = None
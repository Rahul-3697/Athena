from dataclasses import dataclass, field
from typing import Any

from athena.contracts.tool_call import ToolCall
from athena.contracts.tool_result import ToolResult
from athena.runtime.execution_status import ExecutionStatus

@dataclass
class ExecutionState:
    """
    Represents the state of the execution.

    """
    goal: str

    iteration: int = 0

    status: ExecutionStatus = ExecutionStatus.CREATED

    tool_calls: list[ToolCall] = field(
        default_factory=list
    )

    tool_results: list[ToolResult] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

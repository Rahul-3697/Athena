from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionResult:
    """
    Final outcome of an Athena execution.

    ExecutionResult describes what the execution produced.
    ExecutionRecord describes how the execution happened.
    """

    execution_id: str

    status: str

    output: Any = None

    artifacts: list[Any] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    error: str | None = None
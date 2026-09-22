from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ExecutionEvent:
    """
    Immutable fact describing something that happened
    during an Athena execution.
    """

    event_type: str
    execution_id: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    step: str | None = None
    target: str | None = None
    status: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)
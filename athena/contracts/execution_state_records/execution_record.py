from dataclasses import dataclass, field
from datetime import datetime, timezone

from athena.contracts.execution_state_records.execution_event import ExecutionEvent


@dataclass
class ExecutionRecord:
    """
    Represents the lifecycle record of an Athena execution.

    ExecutionRecord owns execution identity and an append-only
    collection of execution events.
    """

    execution_id: str

    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    events: list[ExecutionEvent] = field(default_factory=list)

    completed_at: datetime | None = None

    def add_event(self, event: ExecutionEvent) -> None:
        """
        Append an execution event to the record.
        """

        if event.execution_id != self.execution_id:
            raise ValueError(
                "Execution event belongs to a different execution."
            )

        self.events.append(event)

    def complete(self) -> None:
        """
        Mark the execution record as completed.
        """

        self.completed_at = datetime.now(timezone.utc)
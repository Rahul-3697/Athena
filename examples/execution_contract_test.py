from athena.contracts.execution_state_records.execution_event import ExecutionEvent
from athena.contracts.execution_state_records.execution_record import ExecutionRecord
from athena.contracts.execution_state_records.execution_result import ExecutionResult


def main():

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 7")
    print("EXECUTION CONTRACT FOUNDATION")
    print("=" * 60)

    execution_id = "execution-001"

    # --------------------------------------------------
    # Create execution record
    # --------------------------------------------------

    record = ExecutionRecord(
        execution_id=execution_id
    )

    print("\n[1] Execution Record")
    print(f"    ID      : {record.execution_id}")
    print(f"    Events  : {len(record.events)}")

    # --------------------------------------------------
    # Add events
    # --------------------------------------------------

    record.add_event(
        ExecutionEvent(
            event_type="ExecutionStarted",
            execution_id=execution_id,
            status="running",
        )
    )

    record.add_event(
        ExecutionEvent(
            event_type="WorkflowStarted",
            execution_id=execution_id,
            step="document_review",
            target="document_review",
            status="running",
        )
    )

    record.add_event(
        ExecutionEvent(
            event_type="WorkflowCompleted",
            execution_id=execution_id,
            step="document_review",
            target="document_review",
            status="completed",
        )
    )

    print("\n[2] Execution Events")

    for index, event in enumerate(
        record.events,
        start=1,
    ):
        print(
            f"    {index}. "
            f"{event.event_type}"
            f" | target={event.target}"
            f" | status={event.status}"
        )

    # --------------------------------------------------
    # Complete record
    # --------------------------------------------------

    record.complete()

    print("\n[3] Execution Lifecycle")
    print(f"    Started  : {record.started_at}")
    print(f"    Completed: {record.completed_at}")

    # --------------------------------------------------
    # Create execution result
    # --------------------------------------------------

    result = ExecutionResult(
        execution_id=execution_id,
        status="completed",
        output={
            "message": "Document review completed"
        },
        artifacts=[
            "review_report.docx"
        ],
        metadata={
            "capability": "document_review",
            "workflow": "contract_review",
        },
    )

    print("\n[4] Execution Result")
    print(f"    ID       : {result.execution_id}")
    print(f"    Status   : {result.status}")
    print(f"    Output   : {result.output}")
    print(f"    Artifacts: {result.artifacts}")

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    assert record.execution_id == execution_id
    assert len(record.events) == 3
    assert record.completed_at is not None

    assert result.execution_id == execution_id
    assert result.status == "completed"
    assert result.output is not None
    assert len(result.artifacts) == 1

    print("\n" + "=" * 60)
    print("CHECKPOINT 7 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
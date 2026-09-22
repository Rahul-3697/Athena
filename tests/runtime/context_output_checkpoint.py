from athena.context.context import Context


def run_checkpoint():

    print("\n" + "=" * 60)
    print("ATHENA CHECKPOINT 10")
    print("EXPLICIT WORKFLOW OUTPUT")
    print("=" * 60)

    # --------------------------------------------------------
    # Create execution context
    # --------------------------------------------------------

    context = Context(
        goal="Review legal contract",
        metadata={
            "capability": "document_review",
            "workflow": "contract_review",
        },
    )

    print("\n[1] Context Created")

    print(f"    Goal       : {context.goal}")
    print(f"    Metadata   : {context.metadata}")
    print(f"    Output     : {context.output}")

    # --------------------------------------------------------
    # Simulate workflow producing final output
    # --------------------------------------------------------

    context.output = {
        "summary": "Contract requires further review.",
        "risk_level": "medium",
        "findings": [
            "Missing termination clause",
            "Liability clause requires review",
        ],
    }

    print("\n[2] Workflow Output")

    print(f"    Output     : {context.output}")

    # --------------------------------------------------------
    # Verify separation
    # --------------------------------------------------------

    assert context.output is not None

    assert context.output["risk_level"] == "medium"

    assert len(
        context.output["findings"]
    ) == 2

    assert context.metadata["capability"] == (
        "document_review"
    )

    # --------------------------------------------------------
    # Verify output is separate from metadata
    # --------------------------------------------------------

    assert "risk_level" not in context.metadata

    assert "findings" not in context.metadata

    # --------------------------------------------------------
    # Verify Context helper methods
    # --------------------------------------------------------

    context.set(
        "output",
        {
            "status": "validated",
        },
    )

    result = context.get("output")

    assert result["status"] == "validated"

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print("\n[3] Boundary Verification")

    print("    Internal metadata remains separate.")
    print("    Explicit output is available.")
    print("    Context helpers work correctly.")

    print("\n" + "=" * 60)
    print("CHECKPOINT 10 PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_checkpoint()
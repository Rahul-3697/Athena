from pathlib import Path

from athena.contracts.tool_request import ToolRequest
from athena.tools.builtin.file_search import FileSearchTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry
from athena.runtime.tool_runner import ToolRunner


FIXTURES = (
    Path(__file__).parent
    / "fixtures"
)


def test_file_search_pipeline():

    # 1. Register FileSearchTool
    registry = ToolRegistry()

    file_search = FileSearchTool(
        documents_path=FIXTURES
    )

    registry.register(file_search)

    # 2. Verify registration
    assert registry.has("file_search")

    assert "file_search" in (
        registry.list_tools()
    )

    # 3. Verify LLM-facing descriptor
    descriptors = registry.descriptors()

    assert len(descriptors) == 1

    descriptor = descriptors[0]

    assert descriptor.name == "file_search"

    assert "query" in (
        descriptor.input_schema["properties"]
    )

    # 4. Create executor
    executor = ToolExecutor(
        registry=registry
    )

    # 5. Create runtime runner
    runner = ToolRunner(
        executor=executor
    )

    # 6. Create ToolRequest
    request = ToolRequest(
        tool_name="file_search",
        arguments={
            "query": "refund within 30 days",
            "top_k": 3,
        },
    )

    # 7. Execute through Athena runtime
    result = runner.run(request)

    # 8. Validate result
    assert result.success is True

    assert result.error is None

    assert result.data["query"] == (
        "refund within 30 days"
    )

    assert len(
        result.data["results"]
    ) > 0

    # 9. Verify retrieved evidence
    texts = [
        item["text"]
        for item in result.data["results"]
    ]

    assert any(
        "30 days" in text
        for text in texts
    )

    print(
        "PASS: file search pipeline"
    )

    print(
        "Registered tools:",
        registry.list_tools()
    )

    print(
        "Tool:",
        descriptor.name
    )

    print(
        "Results:",
        len(result.data["results"])
    )

    for item in result.data["results"]:

        print(
            f"\n[{item['chunk_id']}]"
        )

        print(
            item["text"]
        )


if __name__ == "__main__":
    test_file_search_pipeline()
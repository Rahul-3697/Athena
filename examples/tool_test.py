from athena.contracts.tool_request import ToolRequest

from athena.tools.mock_tool import MockTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry


def main():

    registry = ToolRegistry()

    registry.register(MockTool())

    # --------------------------------------------------
    # Tool descriptors
    # --------------------------------------------------

    print("\nTOOL DESCRIPTORS")
    print("-" * 50)

    for descriptor in registry.descriptors():

        print("Name:", descriptor.name)
        print("Description:", descriptor.description)
        print("Schema:", descriptor.input_schema)

    # --------------------------------------------------
    # Tool execution
    # --------------------------------------------------

    executor = ToolExecutor(registry)

    request = ToolRequest(
        tool_name="mock_tool",
        arguments={
            "message": "Hello Athena!"
        }
    )

    result = executor.execute(request)

    print("\nTOOL EXECUTION")
    print("-" * 50)
    print("Success:", result.success)
    print("Data:", result.data)
    print("Error:", result.error)


if __name__ == "__main__":
    main()
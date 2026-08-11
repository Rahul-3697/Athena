from athena.tools.formatters.openai_formatter import OpenAIToolFormatter
from athena.tools.mock_tool import MockTool
from athena.tools.tool_formatter import ToolFormatter
from athena.tools.tool_registry import ToolRegistry


def main():

    registry = ToolRegistry()

    registry.register(MockTool())

    formatter = ToolFormatter(
        OpenAIToolFormatter()
    )

    descriptors = registry.descriptors()

    formatted_tools = formatter.format_many(
        descriptors
    )

    print("=" * 60)
    print("ATHENA TOOL FORMATTER TEST")
    print("=" * 60)

    for tool in formatted_tools:

        print("\nFormatted Tool:")
        print(tool)


if __name__ == "__main__":
    main()
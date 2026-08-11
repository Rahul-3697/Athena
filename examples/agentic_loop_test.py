from athena.contracts.tool_call import ToolCall
from athena.tools.mock_tool import MockTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry
from athena.runtime.tool_loop import ToolLoop


class MockAgenticLLM:

    def generate(self, prompt, tools):

        print("\nLLM received:")
        print(prompt)

        print("\nAvailable tools:")

        for tool in tools:
            print(
                f"- {tool.name}: "
                f"{tool.description}"
            )

        return (
            None,
            [
                ToolCall(
                    tool_name="mock_tool",
                    arguments={
                        "message":
                        "Hello from Athena's first Tool Loop!"
                    }
                )
            ]
        )

    def final_response(
        self,
        prompt,
        tool_result
    ):

        return (
            "The agent executed a Tool successfully.\n"
            f"Tool result: {tool_result.data}"
        )


def main():

    registry = ToolRegistry()

    registry.register(
        MockTool()
    )

    executor = ToolExecutor(
        registry
    )

    llm = MockAgenticLLM()

    tool_loop = ToolLoop(
        llm=llm,
        registry=registry,
        executor=executor,
    )

    result = tool_loop.run(
        "Say hello using an available Tool."
    )

    print("\n")
    print("=" * 60)
    print("ATHENA AGENTIC LOOP")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
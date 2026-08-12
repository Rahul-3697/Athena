from athena.llms.openai_tool_calling import (
    OpenAIToolCallingLLM,
)

from athena.tools.mock_tool import MockTool
from athena.tools.tool_executor import ToolExecutor
from athena.runtime.tool_loop import ToolLoop
from athena.tools.tool_registry import ToolRegistry
from athena.runtime.execution_policy import ExecutionPolicy

def main():

    registry = ToolRegistry()

    registry.register(
        MockTool()
    )

    executor = ToolExecutor(
        registry
    )

    llm = OpenAIToolCallingLLM()

    loop = ToolLoop(
        llm=llm,
        registry=registry,
        executor=executor,
        policy=ExecutionPolicy(
            max_iterations=3,
            max_tool_calls=3,
        )
    )

    result = loop.run(
        """
        Use the available mock tool to say:
        "Athena has completed its first real agentic loop."
        """
    )

    print()
    print("=" * 70)
    print("ATHENA — FIRST REAL AGENTIC LOOP")
    print("=" * 70)
    print()
    print(result)


if __name__ == "__main__":
    main()
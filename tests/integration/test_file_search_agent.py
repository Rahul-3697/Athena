from pathlib import Path
from athena.contracts.tool_request import ToolRequest

from athena.runtime.tool_runner import ToolRunner

from athena.tools.builtin.file_search import FileSearchTool
from athena.tools.tool_executor import ToolExecutor
from athena.tools.tool_registry import ToolRegistry
from athena.llms.openai_tool_calling import OpenAIToolCallingLLM
from athena.runtime.execution_policy import ExecutionPolicy
from athena.runtime.tool_loop import ToolLoop

FIXTURES = (
    Path(__file__).parent
    / "fixtures"
)


registry = ToolRegistry()

registry.register(
    FileSearchTool(
        documents_path=FIXTURES
    )
)

executor = ToolExecutor(
    registry=registry
)

runner = ToolRunner(
    executor=executor
)

llm = OpenAIToolCallingLLM(
    model="gpt-4"
)

loop = ToolLoop(
    llm=llm,
    registry=registry,
    tool_runner=runner,
    policy=ExecutionPolicy(
        max_iterations=3,
        max_tool_calls=5,
    ),
)

answer = loop.run(
    "use file_search to find the refund policy"
)

print(answer)
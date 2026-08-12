from dataclasses import dataclass, field

from athena.contracts.tool_call import ToolCall


@dataclass
class LLMResponse:
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCall:
    """
    Provider-independent representation of an LLM Tool call.
    """

    call_id: str
    tool_name: str
    arguments: dict[str, Any]
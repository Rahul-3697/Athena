from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolDescriptor:
    """
    LLM-facing description of an Athena Tool.

    This contains metadata required to understand and request
    a Tool, but does not expose the Tool implementation itself.
    """

    name: str
    description: str
    input_schema: dict[str, Any]


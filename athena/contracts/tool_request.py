from dataclasses import dataclass
from typing import Any


@dataclass
class ToolRequest:
    """
    Represents a request to execute an Athena Tool.
    """

    tool_name: str
    arguments: dict[str, Any]
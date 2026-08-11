from dataclasses import dataclass
from typing import Any


@dataclass
class ToolResult:
    """
    Standard result returned by an Athena Tool.
    """

    success: bool
    data: Any = None
    error: str | None = None
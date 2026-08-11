from dataclasses import dataclass
from typing import Any


@dataclass
class ToolInput:
    """
    Generic input contract for Athena Tools.
    """

    name: str
    arguments: dict[str, Any]
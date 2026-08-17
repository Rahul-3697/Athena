from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Document:
    """
    Represents a loaded document.
    """

    text: str
    source: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


class BaseDocumentLoader(ABC):
    """
    Base interface for document loaders.
    """

    @abstractmethod
    def load(
        self,
        path: Path,
    ) -> Document:
        raise NotImplementedError
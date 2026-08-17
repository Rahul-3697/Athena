from abc import ABC, abstractmethod

from athena.knowledge.chunking.text_chunker import (
    DocumentChunk,
)


class BaseRetriever(ABC):
    """
    Base interface for knowledge retrieval.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        chunks: list[DocumentChunk],
        top_k: int = 5,
    ) -> list[DocumentChunk]:
        raise NotImplementedError
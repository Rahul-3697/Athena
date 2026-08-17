from dataclasses import dataclass
from typing import Any

from athena.knowledge.loaders.base_loader import Document


@dataclass
class DocumentChunk:
    """
    A searchable section of a Document.
    """

    text: str
    chunk_id: str
    source: str
    metadata: dict[str, Any]


class TextChunker:
    """
    Splits documents into overlapping text chunks.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        overlap: int = 100,
    ):
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if overlap < 0:
            raise ValueError(
                "overlap cannot be negative."
            )

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        document: Document,
    ) -> list[DocumentChunk]:

        text = document.text.strip()

        if not text:
            return []

        chunks = []

        start = 0
        index = 0

        while start < len(text):

            end = start + self.chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        text=chunk_text,
                        chunk_id=(
                            f"{document.source}"
                            f"::{index}"
                        ),
                        source=document.source,
                        metadata={
                            **document.metadata,
                            "chunk_index": index,
                        },
                    )
                )

            index += 1

            if end >= len(text):
                break

            start = end - self.overlap

        return chunks
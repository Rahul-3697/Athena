import re

from athena.knowledge.chunking.text_chunker import (
    DocumentChunk,
)
from athena.knowledge.retrieval.base_retriever import (
    BaseRetriever,
)


class KeywordRetriever(BaseRetriever):
    """
    Simple deterministic keyword-based retriever.
    """

    def retrieve(
        self,
        query: str,
        chunks: list[DocumentChunk],
        top_k: int = 5,
    ) -> list[DocumentChunk]:

        if not query.strip():
            return []

        if top_k <= 0:
            return []

        query_terms = self._tokenize(query)

        scored = []

        for chunk in chunks:

            chunk_terms = self._tokenize(
                chunk.text
            )

            if not chunk_terms:
                continue

            score = sum(
                chunk_terms.count(term)
                for term in query_terms
            )

            if score > 0:
                scored.append(
                    (
                        score,
                        chunk.chunk_id,
                        chunk,
                    )
                )

        scored.sort(
            key=lambda item: (
                -item[0],
                item[1],
            )
        )

        return [
            chunk
            for _, _, chunk in scored[:top_k]
        ]

    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:

        return re.findall(
            r"\b[a-zA-Z0-9]+\b",
            text.lower(),
        )
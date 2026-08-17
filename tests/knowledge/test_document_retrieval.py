from pathlib import Path

from athena.knowledge.chunking.text_chunker import (
    TextChunker,
)
from athena.knowledge.loaders.document_loader import (
    DocumentLoader,
)
from athena.knowledge.retrieval.keyword_retriever import (
    KeywordRetriever,
)


FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "refund_policy.txt"
)


def test_document_retrieval():

    # Load
    loader = DocumentLoader()

    document = loader.load(FIXTURE)

    assert "Refund Policy" in document.text
    assert document.source.endswith(
        "refund_policy.txt"
    )

    # Chunk
    chunker = TextChunker(
        chunk_size=200,
        overlap=20,
    )

    chunks = chunker.chunk(document)

    assert len(chunks) > 0

    # Retrieve
    retriever = KeywordRetriever()

    results = retriever.retrieve(
        query="refund within 30 days",
        chunks=chunks,
        top_k=3,
    )

    assert len(results) > 0

    assert any(
        "30 days" in result.text
        for result in results
    )

    print(
        "PASS: document retrieval"
    )

    print(
        "Document:",
        document.source,
    )

    print(
        "Chunks:",
        len(chunks),
    )

    print(
        "Results:",
        len(results),
    )

    for result in results:

        print(
            f"\n[{result.chunk_id}]"
        )

        print(result.text)


if __name__ == "__main__":
    test_document_retrieval()
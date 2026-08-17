from pathlib import Path

from athena.contracts.tool_input import ToolInput
from athena.contracts.tool_result import ToolResult

from athena.knowledge.chunking.text_chunker import (
    TextChunker,
)
from athena.knowledge.loaders.document_loader import (
    DocumentLoader,
)
from athena.knowledge.retrieval.keyword_retriever import (
    KeywordRetriever,
)

from athena.tools.base_tool import BaseTool


class FileSearchTool(BaseTool):
    """
    Search local documents for relevant passages.
    """

    def __init__(
        self,
        documents_path: str | Path,
    ):
        self.documents_path = Path(
            documents_path
        )

        self.loader = DocumentLoader()

        self.chunker = TextChunker()

        self.retriever = KeywordRetriever()

    @property
    def name(self) -> str:
        return "file_search"

    @property
    def description(self) -> str:
        return (
            "Search local documents and return "
            "relevant passages."
        )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Question or keywords to search for."
                    ),
                },
                "top_k": {
                    "type": "integer",
                    "description": (
                        "Maximum number of relevant "
                        "passages to return."
                    ),
                    "minimum": 1,
                },
            },
            "required": ["query"],
            "additionalProperties": False,
        }

    def execute(
        self,
        tool_input: ToolInput,
    ) -> ToolResult:

        try:

            query = tool_input.arguments.get(
                "query"
            )

            top_k = tool_input.arguments.get(
                "top_k",
                5,
            )

            if not isinstance(query, str):
                return ToolResult(
                    success=False,
                    error="'query' must be a string.",
                )

            if not query.strip():
                return ToolResult(
                    success=False,
                    error="'query' cannot be empty.",
                )

            if not isinstance(top_k, int):
                return ToolResult(
                    success=False,
                    error="'top_k' must be an integer.",
                )

            chunks = self._load_chunks()

            results = self.retriever.retrieve(
                query=query,
                chunks=chunks,
                top_k=top_k,
            )

            return ToolResult(
                success=True,
                data={
                    "query": query,
                    "results": [
                        {
                            "text": chunk.text,
                            "source": chunk.source,
                            "chunk_id": chunk.chunk_id,
                            "metadata": chunk.metadata,
                        }
                        for chunk in results
                    ],
                },
            )

        except Exception as exc:

            return ToolResult(
                success=False,
                error=str(exc),
            )

    def _load_chunks(self):

        if not self.documents_path.exists():
            raise FileNotFoundError(
                "Documents path does not exist: "
                f"{self.documents_path}"
            )

        if not self.documents_path.is_dir():
            raise ValueError(
                "Documents path must be a directory."
            )

        chunks = []

        for path in sorted(
            self.documents_path.rglob("*")
        ):

            if not path.is_file():
                continue

            if path.suffix.lower() not in (
                ".txt",
                ".md",
                ".pdf",
            ):
                continue

            document = self.loader.load(path)

            chunks.extend(
                self.chunker.chunk(document)
            )

        return chunks
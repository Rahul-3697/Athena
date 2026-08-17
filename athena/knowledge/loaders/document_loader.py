from pathlib import Path

from pypdf import PdfReader

from athena.knowledge.loaders.base_loader import (
    BaseDocumentLoader,
    Document,
)


class DocumentLoader(BaseDocumentLoader):
    """
    Loads supported local document formats.
    """

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".pdf",
    }

    def load(
        self,
        path: Path,
    ) -> Document:

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Path is not a file: {path}"
            )

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

        if extension in {".txt", ".md"}:
            text = path.read_text(
                encoding="utf-8"
            )

        elif extension == ".pdf":
            text = self._load_pdf(path)

        else:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

        return Document(
            text=text,
            source=str(path),
            metadata={
                "filename": path.name,
                "extension": extension,
            },
        )

    @staticmethod
    def _load_pdf(
        path: Path,
    ) -> str:

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            text = page.extract_text() or ""

            if text.strip():
                pages.append(text)

        return "\n\n".join(pages)
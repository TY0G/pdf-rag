import fitz

from app.services.embedding_service import EmbeddingService
from app.utils.chunking import chunk_text
from app.utils.text_cleaner import build_summary, clean_text


class ParserService:
    def __init__(self) -> None:
        self.embedding_service = EmbeddingService()

    def parse_pdf(self, file_path: str) -> dict:
        pdf = fitz.open(file_path)
        pages: list[dict] = []
        chunks: list[dict] = []
        chunk_counter = 0

        for index, page in enumerate(pdf, start=1):
            raw_text = page.get_text("text") or ""
            cleaned = clean_text(raw_text)
            pages.append(
                {
                    "page_number": index,
                    "raw_text": raw_text,
                    "cleaned_text": cleaned,
                }
            )
            for piece in chunk_text(cleaned):
                chunks.append(
                    {
                        "page_number": index,
                        "chunk_index": chunk_counter,
                        "content": piece,
                        "meta": {"source": "pdf", "page_number": index},
                        "score": 0.0,
                    }
                )
                chunk_counter += 1

        content_list = [item["content"] for item in chunks]
        embeddings = self.embedding_service.embed_batch(content_list)
        for item, vector in zip(chunks, embeddings):
            item["embedding"] = vector

        summary = build_summary([page["cleaned_text"] for page in pages])
        return {
            "page_count": len(pages),
            "pages": pages,
            "chunks": chunks,
            "summary": summary or "文档已完成解析",
        }

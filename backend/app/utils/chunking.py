from app.core.config import settings


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap or settings.chunk_overlap
    if not text:
        return []

    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        pieces.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return [item.strip() for item in pieces if item.strip()]

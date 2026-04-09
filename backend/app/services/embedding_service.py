import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer


class EmbeddingService:
    def __init__(self) -> None:
        self.vectorizer = HashingVectorizer(
            n_features=384,
            alternate_sign=False,
            analyzer="char",
            ngram_range=(2, 4),
            norm="l2",
        )

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            return [0.0] * 384
        matrix = self.vectorizer.transform([text])
        vector = matrix.toarray()[0].astype(float)
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        matrix = self.vectorizer.transform(texts).toarray().astype(float)
        return [row.tolist() for row in matrix]

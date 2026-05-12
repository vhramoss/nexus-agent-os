from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.texts = []

    def add(self, text: str, metadata: dict | None = None):
        embedding = self.model.encode([text])

        if self.index is None:
            self.index = faiss.IndexFlatL2(len(embedding[0]))

        self.index.add(np.array(embedding))
        self.texts.append({
            "text": text,
            "metadata": metadata or {}
        })

    def search(self, query: str, k: int = 3):
        if self.index is None or not self.texts:
            return []

        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_embedding),
            k
        )

        return [
            self.texts[i]
            for i in indices[0]
            if i < len(self.texts)
        ]
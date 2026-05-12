from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any


class VectorStore:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(384)  # Dimensão do embedding
        self.documents: List[Dict[str, Any]] = []

    def add(self, text: str, metadata: Dict[str, Any]):
        """
        Adiciona um texto ao vetor store, gerando seu embedding e armazenando o documento.
        """
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding))
        self.documents.append({
            "text": text,
            "metadata": metadata,
        })

        def search(self, query: str, k: int = 3):
            if not self.documents:
                return []
            
            embedding = self.model.encode([query])
            distances, indices = self.index.search(np.array(embedding), k)

            return [ 
                self.documents[i]
                for i in indices[0] 
                if i < len(self.documents)
            ]
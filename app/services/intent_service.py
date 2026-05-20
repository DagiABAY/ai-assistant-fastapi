from importlib_metadata import metadata

from app.chroma.chroma_client import get_chroma_client
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

class IntentService:

    def __init__(self):
        self.client = get_chroma_client()
        self.collection = self.client.get_collection("banking_intents")

    def detect(self, message: str):

        query_embedding = model.encode(message).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )

        if not results["documents"][0]:
            return {"intent": "UNKNOWN", "score": 0}

        metadata = results["metadatas"][0][0]
        distance = results["distances"][0][0]

        confidence = 1 - distance
        return {
            "intent": metadata["intent"],
            "confidence": confidence
        }
from app.chroma.chroma_client import get_chroma_client

model = None


class IntentService:

    def __init__(self):
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection("banking_intents")
    def _get_model(self):
        global model
        if model is None:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("all-MiniLM-L6-v2")
        return model

    def detect(self, message: str):

        model = self._get_model()

        query_embedding = model.encode(message).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )

        if not results["documents"][0]:
            return {"intent": "UNKNOWN", "confidence": 0}

        metadata = results["metadatas"][0][0]
        distance = results["distances"][0][0]

        return {
            "intent": metadata["intent"],
            "confidence": 1 - distance
        }
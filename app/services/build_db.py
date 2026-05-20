from sentence_transformers import SentenceTransformer
from app.chroma.chroma_client import get_chroma_client
import os
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = get_chroma_client()
collection = client.get_or_create_collection("banking_intents")

intents = [
    ("CHECK_BALANCE", "what is my balance"),
    ("CHECK_BALANCE", "how much money do I have"),
    ("CHECK_BALANCE", "show my account balance"),

    ("ACCOUNT_INFO", "tell me about my account"),
    ("ACCOUNT_INFO", "show my account details"),

    ("APPLY_ATM_CARD", "apply for debit card"),
    ("LOCK_ATM_CARD", "block my card"),

    ("TRANSFER_MONEY", "send money to someone"),
    ("TRANSFER_MONEY", "transfer money to another account"),
]

for i, (intent, text) in enumerate(intents):
    embedding = model.encode(text).tolist()

    collection.add(
        ids=[f"id_{i}"],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"intent": intent}]
    )

print("✅ Chroma Cloud DB built successfully")
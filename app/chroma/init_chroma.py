from app.chroma.chroma_client import get_chroma_client
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = get_chroma_client()

collection = client.get_or_create_collection("banking_intents")

intents = [
    ("CHECK_BALANCE", "what is my balance"),
    ("CHECK_BALANCE", "how much money do I have"),
    ("CHECK_BALANCE", "show my account balance"),
    
    ("ACCOUNT_INFO", "tell me about my account"),
    ("ACCOUNT_INFO", "show my account details"),
    ("ACCOUNT_INFO", "what account do i have"),
    ("ACCOUNT_INFO", "display my account information"),
    ("ACCOUNT_INFO", "account details"),
    ("ACCOUNT_INFO", "could you tell me about my account"),
    ("ACCOUNT_INFO", "account information"),
    
    
    ("APPLY_ATM_CARD", "I want to apply for ATM card"),
    ("APPLY_ATM_CARD", "apply for debit card"),
    ("APPLY_ATM_CARD", "I need a new ATM card"),
    ("APPLY_ATM_CARD", "replace my card"),
    ("APPLY_ATM_CARD", "lost my ATM card"),
    
    
    ("LOCK_ATM_CARD", "lock my card"),
    ("LOCK_ATM_CARD", "block my card"), 
    ("LOCK_ATM_CARD", "freeze my card"), 
    ("LOCK_ATM_CARD", "suspend my card"), 
    ("LOCK_ATM_CARD", "deactivate my card"), 
    ("LOCK_ATM_CARD", "disable my card"), 
    ("LOCK_ATM_CARD", "hold my card"), 
    ("LOCK_ATM_CARD", "stop my card"), 
    ("LOCK_ATM_CARD", "secure my card"), 
    ("LOCK_ATM_CARD", "protect my card"), 
    
    
    ("SET_ATM_WITHDRAWAL_LIMIT", "set ATM withdrawal limit"),
    ("SET_ATM_WITHDRAWAL_LIMIT", "change ATM limit"),
    ("SET_ATM_WITHDRAWAL_LIMIT", "reduce ATM limit"),
    ("SET_ATM_WITHDRAWAL_LIMIT", "update ATM withdrawal limit"),
    
    
    ("CREATE_BILL_REMINDER", "remind me to pay my electric bill"),
    ("CREATE_BILL_REMINDER", "set a bill reminder"),
    ("CREATE_BILL_REMINDER", "remind me about my water bill"),
    ("CREATE_BILL_REMINDER", "bill payment reminder"),
    ("CREATE_BILL_REMINDER", "remind me to pay electricity"),
    
    
    ("CREATE_TRANSFER_REMINDER", "remind me to send money"),
    ("CREATE_TRANSFER_REMINDER", "create transfer reminder"),
    ("CREATE_TRANSFER_REMINDER", "money transfer reminder"),
    ("CREATE_TRANSFER_REMINDER", "remind me to transfer money"),
    ("CREATE_TRANSFER_REMINDER", "payment reminder"),
    
    
    ("CREATE_BUDGET", "set a budget"),
    ("CREATE_BUDGET", "create a budget"),
    ("CREATE_BUDGET", "I want to set a budget"),
    ("CREATE_BUDGET", "help me create a budget"),
    ("CREATE_BUDGET", "I want to track spending limit"),
    
    ("TRANSFER_MONEY", "I want to transfer money"),
    ("TRANSFER_MONEY", "send money to someone"),   
    ("TRANSFER_MONEY", "transfer money to another account"), 
    ("TRANSFER_MONEY", "I want to send money"),
    ("TRANSFER_MONEY", "help me transfer money"),
    ("TRANSFER_MONEY", "I want to make a money transfer"),
    ("TRANSFER_MONEY", "I want to do a money transfer")
]

for i, (intent, text) in enumerate(intents):

    embedding = model.encode(text).tolist()

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"intent": intent}]
    )

print("✅ Intents stored in Chroma Cloud")
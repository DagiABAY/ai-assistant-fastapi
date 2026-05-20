import os
from groq import Groq

from app.services.banking_service import BankingService

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
from app.session.session_manager import sessions

banking_service = BankingService()


def handle_account_list(chat_id: str, phone_number: str):

    accounts = banking_service.get_account_list_by_phone(phone_number)

    if not accounts:
        return {
            "response": "I couldn't find any account information linked to your phone."
        }

    session = sessions.get(chat_id)

    if not session:
        return {
            "response": "Session expired. Please start again."
        }

    session["transfer_accounts"] = accounts
    session["step"] = 2

    return {
        "response": "Please select the source account for this transfer.",
        "payload": {
            "intent": "TRANSFER_MONEY",
            "type": "SELECTION",
            "field": "source_account",
            "options": [
                {
                    "accountNo": acc["accountNo"],
                    "currency": acc["currency"],
                    "balance": acc["balance"]
                }
                for acc in accounts
            ]
        }
    }

    accounts = banking_service.get_account_list_by_phone(phone_number)
    session = sessions[phone_number]
    if not accounts:
        return {
            "response": "I couldn't find any account information linked to your phone."
        }

    return {
        "response": "Please select the source account for this transfer.",
        "payload": {
            "intent": "ACCOUNT_LIST",
            "type": "SELECTION",
            "field": "source_account",
            "options": [
                {
                    "accountNo": acc["accountNo"],
                    "currency": acc["currency"],
                    "balance": acc["balance"]
                }
                for acc in accounts
            ]
        }
    }
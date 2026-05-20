import os
from groq import Groq

from app.services.banking_service import BankingService

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

banking_service = BankingService()


def handle_account_info(phone_number: str):

    accounts = banking_service.get_account_info_by_phone(phone_number)

    if not accounts:
        return {
            "response": "I couldn't find any account information linked to your profile."
        }

    accounts_text = "\n".join([
        f"""
Account {acc['accountNo']}:
- Type: {acc['accountType']}
- Balance: {acc['balance']} {acc['currency']}
- Branch: {acc['accountBranch']}
"""
        for acc in accounts
    ])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are Abay, a banking assistant.

RULES:
- ONLY use provided account data
- NEVER invent values
- Max 2 sentences
- NO follow-up questions
- Friendly and concise
"""
            },
            {
                "role": "user",
                "content": f"""
Accounts:

{accounts_text}

Respond naturally.
"""
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
from datetime import datetime
from email.mime import message
from app.services.banking_service import BankingService


def handle_transfer_flow(
    sessions,
    chat_id,
    phone_number,
    message
):
    banking_service = BankingService()

    session = sessions[chat_id]

    # =========================================
    # STEP 2 → RECIPIENT
    # =========================================
    print("TRANSFER FLOW", session)
    print("chat_id", chat_id)
    if session["intent"] == "TRANSFER_MONEY" and session["step"] == 2:

        selected_account = message  

        accounts = session.get("transfer_accounts", [])

        valid_accounts = [a["accountNo"] for a in accounts]

        if selected_account not in valid_accounts:
            return {
                "response": "Please select a valid account from the list."
            }

        session["data"]["source_account"] = selected_account
        session["step"] = 3

        return {
            "response": "Enter destination account number."
        }
        
    if session["step"] == 3:

        destination_account = message.strip()

        # 1. Call backend to validate account name
        account_info = banking_service.get_account_name(destination_account)

        if not account_info:
            return {
                "response": "Invalid account number. Please enter a valid destination account."
            }

        session["data"]["destination_account"] = account_info["accountNo"]
        session["data"]["recipient_name"] = account_info["name"]

        session["step"] = 4

        # 3. Ask confirmation
        return {
            "response": f"Is this the correct recipient account?",
            "payload": {
                "intent": "TRANSFER_MONEY",
                "type": "CONFIRMATION",
                "field": "recipient_confirmation",
                "data": {
                    "accountNo": account_info["accountNo"],
                    "name": account_info["name"]
                },
                "options": ["YES", "NO"]
            }
        }
    # =========================================
    # STEP 3 → CONFIRMATION
    # =========================================
    if session["step"] == 4:

        if message == "NO":
            session["step"] = 3
            return {
                "response": "Okay, please enter the correct destination account number."
            }

        if message == "YES":
            session["step"] = 5
            return {
                "response": "How much would you like to transfer?"
            }

        return {
            "response": "Please select YES or NO."
        }
    if session["step"] == 5:

        amount_text = message.strip()
        if not amount_text.isdigit():
                return {
                    "response": "Please enter a valid amount."
                }

        session["data"]["amount"] = int(amount_text)
        session["step"] = 6
        
        return {
            "response": "Please enter the reason for this transfer."
        }
        
    if session["step"] == 6:
        
        session["data"]["reason"] = message
        payload = session["data"]
        del sessions[chat_id]

        return {
            "response": "Your money transfer reminder is ready for confirmation.",
            "payload": {
                "intent": "TRANSFER_MONEY",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }
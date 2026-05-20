from datetime import datetime


def handle_transfer_reminder_flow(
    sessions,
    chat_id,
    message
):

    session = sessions[chat_id]

    # =========================================
    # STEP 2 → RECIPIENT
    # =========================================

    if session["step"] == 2:

        session["data"]["recipient"] = message
        session["step"] = 3

        return {
            "response": "How much would you like to transfer?"
        }

    # =========================================
    # STEP 3 → AMOUNT
    # =========================================

    if session["step"] == 3:

        amount = ''.join(filter(str.isdigit, message))

        if not amount:
            return {
                "response": "Please enter a valid amount."
            }

        session["data"]["amount"] = int(amount)
        session["step"] = 4

        return {
            "response": "When would you like to be reminded?",
            "payload": {
                    "intent": "CREATE_TRANSFER_REMINDER",
                    "type": "DATE_PICKER",
                    "field": "expiry_date",
                    "min_date": "2025-01-01",
                    "max_date": "2026-12-31",
                    "display_format": "DD/MM/YYYY"
            }
           
        }
    # =========================================
    # STEP 4 → DATE
    # =========================================

    if session["step"] == 4:

        try:
            datetime.strptime(message, "%Y-%m-%d")
        except ValueError:
            return {
                "response": "Please enter the date in DD/MM/YYYY format."
            }

        session["data"]["reminder_date"] = message

        payload = session["data"]

        del sessions[chat_id]

        return {
            "response": "Your money transfer reminder is ready for confirmation.",
            "payload": {
                "intent": "CREATE_TRANSFER_REMINDER",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }
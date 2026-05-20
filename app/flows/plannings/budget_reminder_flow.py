from datetime import datetime
from email.mime import message

from requests import session


def handle_budget_reminder_flow(
    sessions,
    chat_id,
    message
):

    session = sessions[chat_id]
    if session["step"] == 2:

            valid_reasons = [ "FOOD",
                    "TRANSPORT",
                    "ENTERTAINMENT",
                    "UTILITIES",
                    "HEALTH",
                    "EDUCATION",
                    "SHOPPING",
                    "TRAVEL",
                    "OTHER"]

            if message not in valid_reasons:
                return {
                    "response": "Please select a valid category."
                }

            session["data"]["category"] = message
            session["step"] = 3

            return {
                "response": "Enter your budget limit amount",
            }
            
    if session["step"] == 3:

            amount_text = message.strip()
            if not amount_text.isdigit():
                return {
                    "response": "Please enter a valid amount."
                }

            session["data"]["amount"] = int(amount_text)
            session["step"] = 4

            return {
                "response": "Please enter the start date for this budget",
                "payload": {
                        "intent": "CREATE_BUDGET",
                        "type": "DATE_PICKER",
                        "field": "start_date",
                        "min_date": "2025-01-01",
                        "max_date": "2026-12-31",
                        "display_format": "YYYY-MM-DD"
                }
            
            }
    if session["step"] == 4:

            try:
                datetime.strptime(message, "%Y-%m-%d")
            except ValueError:
                return {
                    "response": "Please enter the date in YYYY-MM-DD format."
                }
            session["data"]["start_date"] = message
            session["step"] = 5

            return {
                "response": "Please enter the end date for this budget",
                "payload": {
                        "intent": "CREATE_BUDGET",
                        "type": "DATE_PICKER",
                        "field": "end_date",
                        "min_date": "2025-01-01",
                        "max_date": "2026-12-31",
                        "display_format": "YYYY-MM-DD"
                }
            
            }
    if session["step"] == 5:

        try:
                datetime.strptime(message, "%Y-%m-%d")
        except ValueError:
                return {
                    "response": "Please enter the date in YYYY-MM-DD format."
                }
        session["data"]["end_date"] = message

        payload = session["data"]

        del sessions[chat_id]

        return {
            "response": "Your budget reminder is ready for confirmation.",
            "payload": {
                "intent": "CREATE_BUDGET",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }
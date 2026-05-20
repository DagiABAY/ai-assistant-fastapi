from datetime import datetime


def handle_bill_reminder_flow(
    sessions,
    chat_id,
    message
):

    session = sessions[chat_id]

    if session["step"] == 2:

        try:
            datetime.strptime(message, "%Y-%m-%d")
        except ValueError:
            return {
                "response": "Please enter the date in YYYY-MM-DD format."
            }

        session["data"]["valid_until"] = message
        session["step"] = 3

        return {
            "response": "Could you please provide the name of the bill or the company you need to pay?"
        }
    if session["step"] == 3:

   
        session["data"]["bill_name"] = message
        session["step"] = 4

        return {
            "response": "What is the estimated amount for this bill?"
        }
    if session["step"] == 4:

        amount = ''.join(filter(str.isdigit, message))

        if not amount:
            return {
                "response": "Please enter a valid amount."
            }

        session["data"]["amount"] = int(amount)

        payload = session["data"]

        del sessions[chat_id]

        return {
            "response": "Your bill reminder is ready for confirmation.",
            "payload": {
                "intent": "CREATE_BILL_REMINDER",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }
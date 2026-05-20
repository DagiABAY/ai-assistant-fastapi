from datetime import datetime


def handle_atm_limit_flow(
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
            "response": "What would you like the ATM withdrawal limit amount to be?"
        }

    if session["step"] == 3:

        amount = ''.join(filter(str.isdigit, message))

        if not amount:
            return {
                "response": "Please enter a valid amount."
            }

        session["data"]["amount"] = int(amount)

        payload = session["data"]

        del sessions[chat_id]

        return {
            "response": "Your ATM withdrawal limit update is ready for confirmation.",
            "payload": {
                "intent": "SET_ATM_WITHDRAWAL_LIMIT",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }
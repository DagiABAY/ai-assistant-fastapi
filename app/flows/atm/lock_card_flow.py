def handle_lock_card_flow(
    sessions,
    chat_id,
    message
):
    session = sessions[chat_id]

    if session["intent"] != "LOCK_ATM_CARD":
        return None

    if session["step"] == 2:

        valid_reasons = [  "LOST_CARD","STOLEN_CARD","FRAUD_SUSPECTED","OTHER"]

        if message not in valid_reasons:
            return {
                "response": "Please select a valid reason from the options provided."
            }

        session["data"]["reason"] = message
        session["step"] = "DONE"

        payload = session["data"]

        del sessions[chat_id]

        return {
            "response": "Your ATM card request is ready for confirmation.",
            "payload": {
                "intent": "LOCK_ATM_CARD",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }

    return None
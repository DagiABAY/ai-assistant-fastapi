def handle_atm_card_flow(
    sessions,
    chat_id,
    message,
    phone_number
):

    session = sessions[chat_id]

    if session["intent"] != "APPLY_ATM_CARD":
        return None

    # ==============================
    # STEP 2 → SHOW OPTIONS
    # ==============================
    # if session["step"] == 2:

    #     session["data"]["phone_number"] = phone_number
    #     session["step"] = 3   # ✅ FIX: MOVE TO NEXT STEP

    #     return {
    #         "response": "Please select the reason for ATM card request.",
    #         "payload": {
    #             "type": "SELECTION",
    #             "field": "reason",
    #             "options": [
    #                 "NEW_REQUEST",
    #                 "LOST_CARD",
    #                 "DAMAGED_CARD"
    #             ]
    #         }
    #     }

    # ==============================
    # STEP 3 → RECEIVE REASON
    # ==============================
    if session["step"] == 2:

        valid_reasons = ["NEW_REQUEST", "LOST_CARD", "DAMAGED_CARD"]

        if message not in valid_reasons:
            return {
                "response": "Please select a valid reason from the options provided."
            }

        session["data"]["reason"] = message
        session["step"] = 3

        return {
            "response": "Please Select Card Type.",
            "payload": {
                "type": "SELECTION",
                "field": "card_type",
                "options": [
                    "STANDARD",
                    "PREMIUM"
                ]
            }
        }
    # ==============================
    # STEP 4 → FINAL STEP
    # ==============================
    if session["step"] == 3:

        session["data"]["card_type"] = message
        session["step"] = "DONE"

        payload = session["data"]

        del sessions[chat_id]

        return {
            "response": "Your ATM card request is ready for confirmation.",
            "payload": {
                "intent": "APPLY_ATM_CARD",
                "status": "READY_FOR_CONFIRMATION",
                "data": payload
            }
        }

    return None
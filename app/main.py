from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.services.llm_service import LLMService
from app.services.intent_service import IntentService

from app.handlers.balance_handler import handle_balance
from app.handlers.account_info_handler import handle_account_info
from app.handlers.chat_handler import handle_chat
from app.handlers.account_list_handler import handle_account_list

from app.flows.atm.atm_card_flow import handle_atm_card_flow
from app.flows.atm.lock_card_flow import handle_lock_card_flow
from app.flows.atm.atm_limit_flow import handle_atm_limit_flow
from app.flows.plannings.bill_reminder_flow import handle_bill_reminder_flow
from app.flows.plannings.budget_reminder_flow import handle_budget_reminder_flow

from app.session.session_manager import sessions
from app.flows.plannings.transfer_reminder_flow import handle_transfer_reminder_flow
from app.flows.transfer.money_transfer_flow import handle_transfer_flow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()
intent_service = IntentService()


# =====================================================
# ALLOWED BANKING INTENTS
# =====================================================

BANKING_INTENTS = [
    "CHECK_BALANCE",
    "ACCOUNT_INFO",
    "LOCK_ATM_CARD",
    "TRANSFER_MONEY",
    "APPLY_ATM_CARD",
    "SET_ATM_WITHDRAWAL_LIMIT",
    "CREATE_BILL_REMINDER",
    "CREATE_TRANSFER_REMINDER",
    "CREATE_BUDGET",
    "TRANSFER_MONEY"
]


# =====================================================
# REQUEST MODEL
# =====================================================

class ChatRequest(BaseModel):
    chat_id: str
    phone_number: str
    message: str


# =====================================================
# CHAT ENDPOINT
# =====================================================

@app.post("/chat")
def chat(request: ChatRequest):

    chat_id = request.chat_id
    phone_number = request.phone_number
    message = request.message.strip()

    # =====================================================
    # ACTIVE SESSION FLOW HANDLING
    # =====================================================

    if chat_id in sessions:

        session = sessions[chat_id]

        intent = session["intent"]

        if intent == "APPLY_ATM_CARD":
            return handle_atm_card_flow(
                sessions=sessions,
                chat_id=chat_id,
                phone_number=phone_number,  
                message=message
            )

        if intent == "LOCK_ATM_CARD":
            return handle_lock_card_flow(
                sessions=sessions,
                chat_id=chat_id,
                message=message
            )

        if intent == "SET_ATM_WITHDRAWAL_LIMIT":
            return handle_atm_limit_flow(
                sessions=sessions,
                chat_id=chat_id,
                message=message
            )

        if intent == "CREATE_BILL_REMINDER":
            return handle_bill_reminder_flow(
                sessions=sessions,
                chat_id=chat_id,
                message=message
            )

        if intent == "CREATE_BUDGET":
            return handle_budget_reminder_flow(
                sessions=sessions,
                chat_id=chat_id,
                message=message
            )


        if intent == "CREATE_TRANSFER_REMINDER":
            return handle_transfer_reminder_flow(
                sessions=sessions,
                chat_id=chat_id,
                message=message
            )
            
        if intent == "TRANSFER_MONEY":
            return handle_transfer_flow(
                sessions=sessions,
                chat_id=chat_id,
                phone_number=phone_number,  
                message=message
            )
    # =====================================================
    # VECTOR SEARCH
    # =====================================================

    vector_result = intent_service.detect(message)

    vector_intent = vector_result["intent"]
    vector_confidence = vector_result["confidence"]

    print("Vector Intent:", vector_intent)
    print("Vector Confidence:", vector_confidence)

    # =====================================================
    # LLM INTENT EXTRACTION
    # =====================================================

    llm_result = llm_service.extract_intent(message)

    llm_intent = llm_result.get("intent", "CHAT")

    print("LLM Intent:", llm_intent)

    # =====================================================
    # FINAL INTENT DECISION
    # =====================================================

    final_intent = "CHAT"

    if (
        vector_confidence > 0.55
        and vector_intent == llm_intent
    ):
        final_intent = llm_intent

    elif llm_intent in BANKING_INTENTS:
        final_intent = llm_intent

    elif llm_intent == "REJECT":
        final_intent = "REJECT"

    print("Final Intent:", final_intent)

    # =====================================================
    # FLOW STARTERS
    # =====================================================

    if final_intent == "APPLY_ATM_CARD":

        sessions[chat_id] = {
            "intent": "APPLY_ATM_CARD",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }
        return {
            "response": "Please select the reason for ATM card request.",
            "payload": {
                "intent": "APPLY_ATM_CARD",
                "type": "SELECTION",
                "field": "reason",
                "options": [
                    "NEW_REQUEST",
                    "LOST_CARD",
                    "DAMAGED_CARD"
                ]
            }
        }

    if final_intent == "LOCK_ATM_CARD":

        sessions[chat_id] = {
            "intent": "LOCK_ATM_CARD",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }
        
        return {
            "response": "Please select the reason for ATM card lock request.",
            "payload": {
                "intent": "LOCK_ATM_CARD",
                "type": "SELECTION",
                "field": "reason",
                "options": [
                    "LOST_CARD",
                    "STOLEN_CARD",
                    "FRAUD_SUSPECTED",
                    "OTHER"
                ]
            }
        }

    if final_intent == "SET_ATM_WITHDRAWAL_LIMIT":

        sessions[chat_id] = {
            "intent": "SET_ATM_WITHDRAWAL_LIMIT",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }

        return {
            "response": "Until what date should this ATM withdrawal limit apply?",
            "payload": {
                    "intent": "SET_ATM_WITHDRAW_LIMIT",
                    "type": "DATE_PICKER",
                    "field": "expiry_date",
                    "min_date": "2025-01-01",
                    "max_date": "2026-12-31",
                    "display_format": "DD/MM/YYYY"
            }
           
        }

    if final_intent == "CREATE_BILL_REMINDER":

        sessions[chat_id] = {
            "intent": "CREATE_BILL_REMINDER",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }

        return {
            "response": "When would you like to be reminded?",
            "payload": {
                    "intent": "CREATE_BILL_REMINDER",
                    "type": "DATE_PICKER",
                    "field": "expiry_date",
                    "min_date": "2025-01-01",
                    "max_date": "2026-12-31",
                    "display_format": "DD/MM/YYYY"
            }
           
        }


    if final_intent == "CREATE_TRANSFER_REMINDER":

        sessions[chat_id] = {
            "intent": "CREATE_TRANSFER_REMINDER",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }

        return {
            "response": "Sure. Who would you like to send money to?"
        }
    
    if final_intent == "CREATE_BUDGET":

        sessions[chat_id] = {
            "intent": "CREATE_BUDGET",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }
        
        return {
            "response": "Please select the category for your budget.",
            "payload": {
                "intent": "CREATE_BUDGET",
                "type": "SELECTION",
                "field": "category",
                "options": [
                    "FOOD",
                    "TRANSPORT",
                    "ENTERTAINMENT",
                    "UTILITIES",
                    "HEALTH",
                    "EDUCATION",
                    "SHOPPING",
                    "TRAVEL",
                    "OTHER"
                ]
            }
        }
    # =====================================================
    # BANKING HANDLERS
    # =====================================================

    if final_intent == "CHECK_BALANCE":
        return handle_balance(phone_number)

    if final_intent == "ACCOUNT_INFO":
        return handle_account_info(phone_number)
    
    if final_intent == "TRANSFER_MONEY":
         sessions[chat_id] = {
            "intent": "TRANSFER_MONEY",
            "step": 2,
            "phone_number": phone_number,
            "data": {
                "phone_number": phone_number
            }
        }
         return handle_account_list(chat_id,phone_number)

    # =====================================================
    # GENERAL CHAT
    # =====================================================

    if final_intent == "CHAT":
        return handle_chat(message)

    # =====================================================
    # REJECT
    # =====================================================

    if final_intent == "REJECT":

        return {
            "response": (
                "Sorry, I can only help with banking-related requests."
            )
        }

    # =====================================================
    # FALLBACK
    # =====================================================

    return {
        "response": "Sorry, I couldn't process your request."
    }



# from fastapi import FastAPI
# from pydantic import BaseModel
# import os
# from datetime import datetime

# from groq import Groq

# from app.services.llm_service import LLMService
# from app.services.banking_service import BankingService
# from app.services.intent_service import IntentService

# app = FastAPI()

# llm_service = LLMService()
# banking_service = BankingService()
# intent_service = IntentService()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# sessions = {}


# BANKING_INTENTS = [
#     "CHECK_BALANCE",
#     "ACCOUNT_INFO",
#     "LOCK_ATM_CARD",
#     "TRANSFER_MONEY",
#     "APPLY_ATM_CARD",
#     "SET_ATM_WITHDRAWAL_LIMIT",
#     "CREATE_BILL_REMINDER"
# ]


# class ChatRequest(BaseModel):
#     chat_id: str
#     phone_number: str
#     message: str


# @app.post("/chat")
# def chat(request: ChatRequest):

#     chat_id = request.chat_id
#     phone_number = request.phone_number
#     message = request.message.strip()


#     if chat_id in sessions:

#         session = sessions[chat_id]


#         if session["intent"] == "APPLY_ATM_CARD":

#             if session["step"] == 2:

#                 session["data"]["reason"] = message
#                 session["step"] = 3

#                 return {
#                     "response": "Got it. Do you want for all account or for single account?"
#                 }

#             if session["step"] == 3:

#                 session["data"]["card_type"] = message

#                 payload = session["data"]

#                 del sessions[chat_id]

#                 return {
#                     "response": "Your ATM card request is ready for confirmation.",
#                     "payload": {
#                         "intent": "APPLY_ATM_CARD",
#                         "status": "READY_FOR_CONFIRMATION",
#                         "data": payload
#                     }
#                 }

 
#         if session["intent"] == "LOCK_ATM_CARD":

#             if session["step"] == 2:

#                 session["data"]["reason"] = message

#                 payload = session["data"]

#                 del sessions[chat_id]

#                 return {
#                     "response": "Your ATM card lock request is ready for confirmation.",
#                     "payload": {
#                         "intent": "LOCK_ATM_CARD",
#                         "status": "READY_FOR_CONFIRMATION",
#                         "data": payload
#                     }
#                 }

    
#         if session["intent"] == "SET_ATM_WITHDRAWAL_LIMIT":

#             if session["step"] == 2:

#                 try:
#                     datetime.strptime(message, "%d/%m/%Y")
#                 except ValueError:
#                     return {
#                         "response": "Please enter the date in DD/MM/YYYY format."
#                     }

#                 session["data"]["valid_until"] = message
#                 session["step"] = 3

#                 return {
#                     "response": "What would you like the ATM withdrawal limit amount to be?"
#                 }

#             if session["step"] == 3:

#                 amount = ''.join(filter(str.isdigit, message))

#                 if not amount:
#                     return {
#                         "response": "Please enter a valid amount."
#                     }

#                 session["data"]["amount"] = int(amount)

#                 payload = session["data"]

#                 del sessions[chat_id]

#                 return {
#                     "response": "Your ATM withdrawal limit update is ready for confirmation.",
#                     "payload": {
#                         "intent": "SET_ATM_WITHDRAWAL_LIMIT",
#                         "status": "READY_FOR_CONFIRMATION",
#                         "data": payload
#                     }
#                 }


#         if session["intent"] == "CREATE_BILL_REMINDER":

#             if session["step"] == 2:

#                 try:
#                     datetime.strptime(message, "%d/%m/%Y")
#                 except ValueError:
#                     return {
#                         "response": "Please enter the date in DD/MM/YYYY format."
#                     }

#                 session["data"]["valid_until"] = message
#                 session["step"] = 3

#                 return {
#                     "response": "What is the estimated amount for this bill?"
#                 }

#             if session["step"] == 3:

#                 amount = ''.join(filter(str.isdigit, message))

#                 if not amount:
#                     return {
#                         "response": "Please enter a valid amount."
#                     }

#                 session["data"]["amount"] = int(amount)

#                 payload = session["data"]

#                 del sessions[chat_id]

#                 return {
#                     "response": "Your bill reminder is ready for confirmation.",
#                     "payload": {
#                         "intent": "CREATE_BILL_REMINDER",
#                         "status": "READY_FOR_CONFIRMATION",
#                         "data": payload
#                     }
#                 }



#     vector_result = intent_service.detect(message)

#     vector_intent = vector_result["intent"]
#     vector_confidence = vector_result["confidence"]

#     print("Vector Intent:", vector_intent)
#     print("Vector Confidence:", vector_confidence)


#     llm_result = llm_service.extract_intent(message)

#     llm_intent = llm_result.get("intent", "CHAT")

#     print("LLM Intent:", llm_intent)


#     final_intent = "CHAT"

#     if (
#         vector_confidence > 0.55
#         and vector_intent == llm_intent
#     ):
#         final_intent = llm_intent

#     elif llm_intent in BANKING_INTENTS:
#         final_intent = llm_intent

#     elif llm_intent == "REJECT":
#         final_intent = "REJECT"

#     print("Final Intent:", final_intent)


#     if final_intent == "APPLY_ATM_CARD":

#         sessions[chat_id] = {
#             "intent": "APPLY_ATM_CARD",
#             "step": 2,
#             "phone_number": phone_number,
#             "data": {
#                 "phone_number": phone_number
#             }
#         }

#         return {
#             "response": "Sure, I can help you apply for an ATM card. Could you please tell me the reason (lost, damaged, new request)?"
#         }

 
#     if final_intent == "LOCK_ATM_CARD":

#         sessions[chat_id] = {
#             "intent": "LOCK_ATM_CARD",
#             "step": 2,
#             "phone_number": phone_number,
#             "data": {
#                 "phone_number": phone_number
#             }
#         }

#         return {
#             "response": "Sure, I can help you lock your ATM card. Could you please tell me the reason?"
#         }

#     if final_intent == "SET_ATM_WITHDRAWAL_LIMIT":

#         sessions[chat_id] = {
#             "intent": "SET_ATM_WITHDRAWAL_LIMIT",
#             "step": 2,
#             "phone_number": phone_number,
#             "data": {
#                 "phone_number": phone_number
#             }
#         }

#         return {
#             "response": "Sure. Until what date should this ATM withdrawal limit apply? Please use DD/MM/YYYY format."
#         }

#     if final_intent == "CREATE_BILL_REMINDER":

#         sessions[chat_id] = {
#             "intent": "CREATE_BILL_REMINDER",
#             "step": 2,
#             "phone_number": phone_number,
#             "data": {
#                 "phone_number": phone_number
#             }
#         }

#         return {
#             "response": "Sure. When would you like to be reminded?"
#         }



#     if final_intent == "CHECK_BALANCE":

#         accounts = banking_service.get_balances_by_phone(phone_number)

#         if not accounts:
#             return {
#                 "response": "I couldn't find any account information linked to your profile."
#             }

#         # Send ONLY real data to LLM (no summaries, no calculations)
#         accounts_text = "\n".join([
#             f"Account {acc['accountNo']} has balance {acc['balance']} ETB"
#             for acc in accounts
#         ])

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
#                     You are Abay, a banking assistant.

#                     RULES:
#                     - ONLY use the provided account data
#                     - Do NOT guess or add extra information
#                     - Be friendly but concise
#                     - Max 1 sentences
#                     - Do not show JSON or raw formatting
#                     """
#                 },
#                 {
#                     "role": "user",
#                     "content": f"""
#     User account data:

#     {accounts_text}

#     Now respond naturally to the user.
#     """
#                 }
#             ]
#         )

#         return {
#             "response": response.choices[0].message.content
#         }

#     if final_intent == "ACCOUNT_INFO":

#         accounts = banking_service.get_account_info_by_phone(phone_number)

#         if not accounts:
#             return {
#                 "response": "I couldn't find any account information linked to your profile."
#             }

#         # Format raw safe data for LLM (NO summarization, NO guessing)
#         accounts_text = "\n".join([
#             f"""
#     Account {acc['accountNo']}:
#     - Type: {acc['accountType']}
#     - Balance: {acc['balance']} {acc['currency']}
#     - Branch: {acc['accountBranch']}
#     - Holder: {acc['accountHolderName']}
#     """
#             for acc in accounts
#         ])

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
#     You are Abay, a banking assistant.

#     RULES:
#     - ONLY use the provided account information
#     - NEVER guess or invent values
#     - Be concise and friendly
#     - Maximum 2 sentences
#     - Summarize multiple accounts clearly
#     - Do NOT show raw formatting or JSON
#     """
#                 },
#                 {
#                     "role": "user",
#                     "content": f"""
#     User account information:

#     {accounts_text}

#     Respond naturally to the user.
#     """
#                 }
#             ]
#         )

#         return {
#             "response": response.choices[0].message.content
#         }

#     if final_intent == "CHAT":

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": """
#     You are Abay, a banking assistant chatbot.

#     CORE RULES:
#     - You ONLY assist in banking-related context
#     - You are allowed to be friendly, but not a general AI assistant
#     - NEVER discuss or elaborate on non-banking topics
#     - If user asks unrelated topics, gently redirect to banking help

#     RESPONSE STYLE:
#     - Keep responses VERY short (max 1–2 sentences)
#     - Friendly and natural tone
#     - No long greetings
#     - No multiple questions in one response
#     - Do NOT introduce yourself repeatedly
#     - Do NOT say "I am a banking assistant" unless necessary

#     BEHAVIOR EXAMPLES:

#     User: Hi
#     Assistant: Hi 👋 How can I help you with your banking today?

#     User: I'm Dagim
#     Assistant: Nice to meet you, Dagim 👋 How can I help you today?

#     User: How are you?
#     Assistant: I'm here and ready to help you with your banking needs.

#     User: tell me a joke
#     Assistant: I can help you with banking services like accounts, cards, and transfers.

#     STRICT RULE:
#     If message is clearly non-banking → gently redirect to banking services
#     """
#                 },
#                 {
#                     "role": "user",
#                     "content": message
#                 }
#             ]
#         )

#         return {
#             "response": response.choices[0].message.content
#         }

 
#     if final_intent == "REJECT":

#         return {
#             "response": "Sorry, I can only help with banking-related requests."
#         }

#     return {
#         "response": "Sorry, I couldn't process your request."
#     }
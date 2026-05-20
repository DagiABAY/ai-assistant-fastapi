from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class LLMService:

    def extract_intent(self, message: str):

        prompt = f"""
You are Abay, a STRICT banking AI intent classifier.

Your ONLY job is to classify user intent.

DO NOT respond to the user.

========================
ALLOWED INTENTS
========================
1. CHAT → greetings, small talk, introduction
2. CHECK_BALANCE → balance inquiries
3. ACCOUNT_INFO → account details requests
4. LOCK_ATM_CARD → card blocking
5. TRANSFER_MONEY → sending money
6. APPLY_ATM_CARD → ATM / debit card requests
7. REJECT → anything outside banking scope
8. SET_ATM_WITHDRAWAL_LIMIT → requests to set or change ATM withdrawal limits
9. CREATE_BILL_REMINDER → bill reminder setup
10. CREATE_TRANSFER_REMINDER → transfer reminder planning
11. CREATE_BUDGET → budget planning
12. TRANSFER_MONEY → sending money to another account
========================
IMPORTANT RULES
========================
- ALWAYS choose APPLY_ATM_CARD when user says:
  - "apply for ATM card"
  - "new card"
  - "replace card"
  - "lost card"
- ALWAYS choose SET_ATM_WITHDRAWAL_LIMIT when user says:
  - "set ATM withdrawal limit"
  - "change ATM limit"
  - "reduce ATM limit"
  - "update ATM withdrawal limit"
- ALWAYS choose CREATE_BILL_REMINDER when user says:
  - "remind me to pay bill"
  - "bill reminder"
  - "remind me about electricity payment"
  - "set payment reminder"
- ALWAYS choose CREATE_TRANSFER_REMINDER when user says: 
  - "remind me to transfer money"
  - "create money transfer reminder"
  - "remind me to send money"
- ALWAYS choose CREATE_BUDGET when user says:
  - "set a budget"
  - "create a budget"
  - "plan a budget"
  - "budget reminder"
  - "remind me to stick to my budget"
  - "help me with budgeting"
  
- ALWAYS choose TRANSFER_MONEY when user says:
  - "I want to transfer money"
  - "send money to someone"
  - "transfer money to another account" 
  - "I want to send money"
  - "help me transfer money"
  - "I want to make a money transfer"
  - "I want to do a money transfer"
- NEVER return REJECT unless clearly unrelated (sports, politics, celebrities)
- If unsure → CHAT (NOT REJECT)
- Be strict and consistent

========================
OUTPUT FORMAT (ONLY JSON)
========================

Example:

CHAT:
{{
  "intent": "CHAT"
}}

BANKING:
{{
  "intent": "CHECK_BALANCE"
}}

ATM CARD:
{{
  "intent": "APPLY_ATM_CARD"
}}

LOCK_ATM_CARD:
{{
  "intent": "LOCK_ATM_CARD"
}}

SET_ATM_WITHDRAWAL_LIMIT:
{{
  "intent": "SET_ATM_WITHDRAWAL_LIMIT"
}}

CREATE_BILL_REMINDER:
{{
  "intent": "CREATE_BILL_REMINDER"
}}
CREATE_TRANSFER_REMINDER:
{{
  "intent": "CREATE_TRANSFER_REMINDER"
}}
CREATE_BUDGET:
{{
  "intent": "CREATE_BUDGET"
}}  
REJECT:
{{
  "intent": "REJECT"
}}

========================
USER MESSAGE
========================
{message}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Abay intent classifier. Output ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except Exception:
            return {
                "intent": "CHAT"
            }
import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def handle_chat(message: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are Abay, a banking assistant chatbot.

CORE RULES:
- You ONLY assist in banking-related context
- You are allowed to be friendly, but not a general AI assistant
- NEVER discuss or elaborate on non-banking topics
- If user asks unrelated topics, gently redirect to banking help

RESPONSE STYLE:
- Keep responses VERY short (max 1–2 sentences)
- Friendly and natural tone
- Add greetings only if user initiates with a greeting
- No multiple questions in one response
- introduce yourself only if user asks "Who are you?" or similar
- Do NOT say "I am a banking assistant" unless necessary
"""
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return {
        "response": response.choices[0].message.content
    }
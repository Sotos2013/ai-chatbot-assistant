import os
import sys
import io
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# Φόρτωση του .env αρχείου
load_dotenv()

# UTF-8 για τα Ελληνικά στο terminal
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Κρατάμε το ιστορικό παγκόσμια
chat_history = []

class ChatRequest(BaseModel):
    text: str

@app.post("/api/chat")
async def chat_endpoint(data: ChatRequest):
    global chat_history
    
    # 1. Έλεγχος αν υπάρχει το API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("🚨 ΣΦΑΛΜΑ: Το GEMINI_API_KEY δεν βρέθηκε στο .env αρχείο!")
        return {"reply": "Δεν βρήκα το κλειδί API μου. Έλεγξε το αρχείο .env!"}

    client = genai.Client(api_key=api_key)
    for model in client.models.list():
        print(f"Διαθέσιμο μοντέλο: {model.name}")

    try:
        # 2. Προσθήκη του νέου μηνύματος
        chat_history.append({"role": "user", "parts": [{"text": data.text}]})

        # 3. Κλήση του API - Δοκιμάζουμε το 1.5 flash αν το 2.0 έχει θέμα
        response = client.models.generate_content(
            model="models/gemini-2.0-flash", 
            contents=chat_history
        )

        # 4. Αποθήκευση απάντησης
        chat_history.append({"role": "model", "parts": [{"text": response.text}]})

        return {"reply": response.text}

    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        chat_history = [] 
        return {"reply": f"Σφάλμα API: {str(e)}"}

@app.post("/api/clear")
async def clear_chat():
    global chat_history
    chat_history = []
    return {"status": "Memory cleared"}
import os
import sys
import io
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI  # Χρησιμοποιούμε τη βιβλιοθήκη της OpenAI

# 1. Φόρτωση ρυθμίσεων
load_dotenv()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = FastAPI()

# 2. CORS - Επιτρέπει στο Frontend να επικοινωνεί με το Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

# 3. Ρύθμιση του Hugging Face Client
# Βεβαιώσου ότι στο .env έχεις: HF_TOKEN=το_token_σου
hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

# Ιστορικό συνομιλίας (Context)
chat_history = []

class ChatRequest(BaseModel):
    text: str

@app.post("/api/chat")
async def chat_endpoint(data: ChatRequest):
    global chat_history
    
    if not os.getenv("HF_TOKEN"):
        return {"reply": "Λείπει το HF_TOKEN από το αρχείο .env!"}

    try:
        # Προσθήκη μηνύματος χρήστη στο ιστορικό
        chat_history.append({"role": "user", "content": data.text})

        # 4. Κλήση του μοντέλου μέσω Hugging Face
        completion = hf_client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905", # Το μοντέλο που επέλεξες
            messages=chat_history,
            max_tokens=500
        )

        bot_response = completion.choices[0].message.content
        
        # Αποθήκευση απάντησης στο ιστορικό
        chat_history.append({"role": "assistant", "content": bot_response})

        return {"reply": bot_response}

    except Exception as e:
        print(f"🚨 Σφάλμα: {e}")
        chat_history = [] # Reset σε περίπτωση σφάλματος
        return {"reply": f"Σφάλμα API: {str(e)}"}

@app.post("/api/clear")
async def clear_chat():
    global chat_history
    chat_history = []
    return {"status": "Memory cleared"}
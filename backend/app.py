import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from supabase import create_client, Client # <--- Η βιβλιοθήκη της Supabase

app = FastAPI()

# 1. Σύνδεση με Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

class ChatRequest(BaseModel):
    text: str

@app.get("/")
def home():
    # Τραβάμε τα τελευταία 15 μηνύματα από τη Supabase
    response = supabase.table("messages").select("*").order("id", desc=True).limit(15).execute()
    history = response.data
    return {"status": "Running", "history": history[::-1]}

@app.post("/api/chat")
async def chat(data: ChatRequest):
    try:
        # 1. Αποθήκευση μηνύματος χρήστη στη Supabase
        supabase.table("messages").insert({"role": "user", "content": data.text}).execute()

        # 2. Φόρτωση ιστορικού για το AI
        res = supabase.table("messages").select("role", "content").order("id", desc=True).limit(6).execute()
        messages_for_ai = res.data[::-1]

        # 3. Κλήση AI
        completion = hf_client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=messages_for_ai,
            max_tokens=500
        )
        bot_response = completion.choices[0].message.content

        # 4. Αποθήκευση απάντησης bot στη Supabase
        supabase.table("messages").insert({"role": "assistant", "content": bot_response}).execute()

        return {"reply": bot_response}

    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

@app.post("/api/clear")
async def clear_chat():
    # Διαγραφή όλων των εγγραφών (Προσοχή: στην Postgres θέλει φίλτρο, εδώ διαγράφουμε τα πάντα)
    supabase.table("messages").delete().neq("role", "none").execute()
    return {"status": "History Cleared"}
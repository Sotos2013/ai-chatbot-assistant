import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 2. CORS - ΠΟΛΥ ΣΗΜΑΝΤΙΚΟ ΓΙΑ ΤΟ GITHUB PAGES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Ρύθμιση του Hugging Face Client
hf_client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

chat_history = []

class ChatRequest(BaseModel):
    text: str

# Προσθήκη ενός GET endpoint για να ξέρουμε αν είναι "ζωντανό"
@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/api/chat")
async def chat_endpoint(data: ChatRequest):
    global chat_history
    
    token = os.getenv("HF_TOKEN")
    if not token:
        return {"reply": "🚨 Σφάλμα: Το HF_TOKEN δεν έχει οριστεί στα Secrets του Space!"}

    try:
        chat_history.append({"role": "user", "content": data.text})

        completion = hf_client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=chat_history,
            max_tokens=500
        )

        bot_response = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_response})

        return {"reply": bot_response}

    except Exception as e:
        chat_history = [] 
        return {"reply": f"Σφάλμα API: {str(e)}"}

@app.post("/api/clear")
async def clear_chat():
    global chat_history
    chat_history = []
    return {"status": "Memory cleared"}
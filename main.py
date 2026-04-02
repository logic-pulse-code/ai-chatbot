import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# WICHTIG: Erlaubt deiner Website den Zugriff
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisierung des KI-Clients
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/")
def home():
    return {"status": "online", "message": "Backend ist bereit!"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key fehlt in Render Einstellungen!")
    
    try:
        # Hier findet die Magie statt
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher KI-Assistent für mein Portfolio. Antworte kurz und freundlich."},
                {"role": "user", "content": request.message}
            ],
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        print(f"Fehler: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

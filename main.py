import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# CORS erlauben, damit dein Framer-Widget auf das Backend zugreifen darf
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In Produktion hier deine Domain eintragen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq Client initialisieren (Der API Key kommt später in die Render-Einstellungen)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192", # Ein schnelles, kostenloses Modell
            messages=[
                {
                    "role": "system",
                    "content": "Du bist der Assistent von [Dein Name]. Antworte höflich, professionell und auf Deutsch. Branding: [Dein Stil, z.B. locker/seriös]."
                },
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

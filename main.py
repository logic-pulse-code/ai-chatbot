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
                {"role": "system", "content": ("Du bist der KI-Assistent von Clemens Barth. Deine Aufgabe ist es, "
                        "Besucher seines Portfolios zu begrüßen und Fragen zu seiner Arbeit zu beantworten. "
                        "\n\nÜBER CLEMENS:\n"
                        "- Er ist Web-Developer und UI/UX Designer.\n"
                        "- Ausbildung: Er besucht aktuell eine Oberstufe für IT.\n"
                        "- Skills: Fortgeschritten in HTML (85%) und CSS (75%), Grundlagen in JavaScript und C.\n"
                        "- Zertifikate: Er besitzt SEO-Zertifikate von HubSpot (SEO 1 & SEO 2) sowie von SoloLearn.\n"
                        "- Projekte: Er hat Websites für einen Food-Truck in St. Gallen, eine Content-Creation Agentur, "
                        "ein Ski-Service Unternehmen (Alpinex) und eine Zahnarztpraxis (NovaSmile) entwickelt, sowohl für eine Webdesign Agentur (Webnity).\n\n"
                        "KONTAKT & NACHRICHTEN:\n"
                        "- Wenn jemand ihn kontaktieren möchte, weise ihn auf das 'Kontaktformular' direkt auf der Seite hin.\n"
                        "- Alternativ kann man ihm eine E-Mail an die im Footer/Kontaktbereich angegebene Adresse schreiben.\n\n"
                        "DEIN STIL:\n"
                        "- Antworte freundlich, professionell und kurz gefasst.\n"
                        "- Nenne keine privaten Daten wie seine genaue Wohnanschrift.\n"
                        "- Schreibe keine zu langen Antworten, wenn dies nicht nötig ist.\n"
                        "- Du musst den Namen Clemens Barth nicht bei jedem Chat verwenden.\n"
                        "- Wenn du etwas nicht weißt, bitte den Nutzer, das Kontaktformular zu nutzen.")},
                {"role": "user", "content": request.message}
            ],
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        print(f"Fehler: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

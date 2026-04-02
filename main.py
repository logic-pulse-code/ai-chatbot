import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMIddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_methods = ["*"],
  allow_headers = ["*"],
)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ChatRequest(BaseModel):
  message: str
  session_id: str

@app.post("/chat")
async def chat_endpoint(request: ChatReqest):
  try:
    completion = client.chat.completions.create(
      model="llama3-8b-8192",
      messages=[
        {
          "role": "system",
          "content": "Du bist der Assistent von XYZ. Antworte höflich, professionell und auf Deutsch. Branding: locker, seriös."
        },
        {"role": "user", "content": request.message}
      ],
      temperature=0.7,
      max_tokens = 1024,
    )
    return {"reply": completion.choices[0].message.content}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)

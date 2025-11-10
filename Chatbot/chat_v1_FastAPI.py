# openAI API를 활용한 챗봇 서비스

from dotenv import load_dotenv
load_dotenv() # .env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI() # API키 생략

# FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class ChatInput(BaseModel):
  message: str
  model: str = "gpt-4o-mini"
  max_tokens: int = 200
  temperature: float = 0.8

@app.post("/chat")
# 챗함수
def chat(input: ChatInput) -> str:
  response = client.chat.completions.create(
    model=input.model,
    messages=[
      {"role":"system", "content":"You are a helpful assistant."},
      {"role":"user","content": input.message},
    ],
    max_tokens=input.max_tokens,
    temperature=input.temperature,
  )
  return response.choices[0].message.content.strip()
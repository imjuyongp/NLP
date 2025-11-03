# openAI API를 활용한 챗봇 서비스

from dotenv import load_dotenv
load_dotenv() # .env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI() # API키 생략

from pydantic import BaseModel
from typing import List

# 챗 함수
def chat(messages):
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    max_tokens=200
  )
  return response.choices[0].message.content.strip()

class Turn(BaseModel):
  role:str
  content:str

class Messages(BaseModel):
  messages: List[Turn]


# -------- [fast API] --------
from fastapi import FastAPI

app = FastAPI()

@app.post("/chat", response_model=Turn)
def post_chat(messages: Messages):
  assistant_turn = chat(messages.messages)
  return Turn(role="assistant", content=assistant_turn)
import os
from dotenv import load_dotenv
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

from pydantic import BaseModel

from chains import intent_chain, analysis_chain, purchase_chain
from vectordb import get_relevant_documents


class ChatInput(BaseModel):
  message:str

def get_intents() -> str:
  return """
  - purchase
  - inquiry
  - complaint
  """ 

def get_customer_center_guide() -> str:
  return (
    "2025, Customer Center Guide\n"
    "- inquiry about the Notebook is no answered (because of absence of the staff)\n"
    "- inquiry the Printer is available"
  ) 

############################################################
# -- [FastAPI] -- #

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# FastAPI 객체 생성
app = FastAPI(debug=True)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.post("/chat")
def chat(input: ChatInput) -> str:
  req = input.model_dump()
  req["intents"] = get_intents()
  intent = intent_chain.invoke(req)
  print(intent) # 확인용 출력

  if intent == "complaint" :
    COMPLAINT_RESPONSE = "I'm sorry to hear that you're having trouble."
    return COMPLAINT_RESPONSE
  
  if intent == "purchase" :
    req["relevant_documents"] = get_relevant_documents(req["message"])
    purchase_reply = purchase_chain.invoke(req)
    return COMPLAINT_RESPONSE

  if intent == "purchase" :
    PURCHASE_RESPONSE = "I see your order."
    return PURCHASE_RESPONSE
  if intent == "inquiry" :
    req["guide"] = get_customer_center_guide()
    # multi-chain 실행
    result = analysis_reply_chain.invoke(req)
    reply_msg = result # reply_chain에서 최종 reply가 string으로 변환됨
    return reply_msg
  return "I am sorry, I am not able to understand your message"

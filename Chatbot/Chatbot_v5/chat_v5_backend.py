import os
from dotenv import load_dotenv
import openai
from enum import Enum
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class PromptTemplates(str,Enum):
  INTENT_PROMPT = """ choose the one of the following intents for the user message
  [intents] {intents}
  User : i have a problem, your service is aweful
  classifier : complaint
  User: {message}
  classifier :"""

  INQUIRY_ANALYSIS_PROMPT = """analysis the user's message for inquiry
  User: {message}
  Analysis :"""

  INQUIRY_REPLY_PROMPT = """reply to the user's inquiry message with inquiry analysis and Customer Center Guide
  [inquiry analysis] {analysis}
  [Customer Center Guide] {guide}
  User: {message}
  Reply:"""

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

# LLM 모델 초기화
chatOpenAI = ChatOpenAI(
  temperature=0.8,
  max_tokens=200,
  model="gpt-3.5-turbo"
)

def build_llm_chain(llm, template: str):
  prompt = ChatPromptTemplate.from_template(template)
  chain = prompt | llm | StrOutputParser() # Runnable 구문 (파이프라인)
  return chain

# 각 LLM chain runnable 구성
intent_chain = build_llm_chain(chatOpenAI,PromptTemplates.INTENT_PROMPT)
analysis_chain = build_llm_chain(chatOpenAI, PromptTemplates.INQUIRY_ANALYSIS_PROMPT)
reply_chain = build_llm_chain(chatOpenAI, PromptTemplates.INQUIRY_REPLY_PROMPT)

# Multi-chain
analysis_reply_chain = RunnableMap({
  "analysis":analysis_chain,
  "guide": lambda x: x["guide"],
  "message": lambda x: x["message"]
}) | reply_chain

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
    PURCHASE_RESPONSE = "I see your order."
    return PURCHASE_RESPONSE
  if intent == "inquiry" :
    req["guide"] = get_customer_center_guide()
    # muti-chain 실행
    result = analysis_reply_chain.invoke(req)
    reply_msg = result # reply_chain에서 최종 reply가 string으로 변환됨
    return reply_msg
  return "I am sorry, I am not able to understand your message"

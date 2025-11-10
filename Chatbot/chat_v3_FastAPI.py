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

# 챗봇 v2: 고객 의도 파악 (구매, 문의, 불만)
class LlmTemplate(BaseModel):
  message: str
  model: str = "gpt-4o-mini"
  max_tokens: int = 200
  temperature: float = 0.8
  system_message: str = "You are a helpful assistant."

def llm_for_chat(llm: LlmTemplate) -> str:
  response = client.chat.completions.create(
    model=llm.model,
    messages=[
      {"role":"system", "content":llm.system_message},
      {"role":"user", "content": llm.message},
    ],
    max_tokens=llm.max_tokens,
    temperature=llm.temperature,
  )
  return response.choices[0].message.content

ASSISTANT_PERSONA = (
  "You are a helpful assistant, your job is to answer about user`s inquiry"
)
INTENT_CLASSIFIER_PERSONA = "You are a helpful intent classifier, " \
"your job is to classify the intent of the user message"

# 챗봇 v3: "문의"답변에 고객정보 반영 & 고객센터 가이드를 반영한 답변
class User(BaseModel):
  name: str
  email: str
  memo: str
  last_inquiry: str

def get_user_info() -> str:
  user = User(
    name="고소웨",
    email="GoSW@skuniv.ac.kr",
    memo="polite person",
    last_inquiry="불만을 접수한다. 어제 산 노트북이 동작을 안한다.",
  )

  print(user)
  return f"""{user}"""

def get_customer_center_guide() -> str:
  return f"""
  2025, Customer Center Guide
  - 노트북 담당 직원이 없어서, 지금 노트북에 대한 문의는 처리할 수 없음.
  - 데스크탑(PC)에 대한 문의 처리는 가능함.
"""

STAFF_PERSONA = "You are a Customer Center staff , " \
"your job is to answer about customer`s inquiry following the Customer`info " \
"and the guide"

STAFF_SYSTEM_MSG = f"""
{STAFF_PERSONA}

[customer info]
{get_user_info()}

[guide info]
{get_customer_center_guide}

"""

@app.post("/chat")
def chat(input: ChatInput) -> str:
  
  DEFAULT_RESPONSE = f"""
  I am sorry, I am not able to understand your message
  """
  
  INTENT_PROMPT = f"""
  Choose the one of the following intents for the user message
  - purchase
  - complaint
  - inquiry

  User : I have a problem, your service is aweful
  classifier : complaint

  User: {input.message}
  classifier :
  """

  intent_llm = LlmTemplate(
    model=input.model,
    message=INTENT_PROMPT,
    max_tokens=input.max_tokens,
    temperature=input.temperature,
    system_message=INTENT_CLASSIFIER_PERSONA,
  )

  intent = llm_for_chat(intent_llm)
  print(intent) # 작업 확인용 출력

# 고객 의도에 따른 페르소나 설정
# 1) 구매
  if intent == "purchase":
    PURCHASE_RESPONSE = f"""
    I see your order
    """
    return PURCHASE_RESPONSE

# 2) 불만
  if intent == "complaint":
    COMPLAINT_RESPONSE = f"""
    I`m sorry to hear that you`re having trouble.
    """
    return COMPLAINT_RESPONSE
  
# 3) 문의
  if intent == "inquiry":
    # 새 문의 처리하기
    inquiry_llm = LlmTemplate(
      model=input.model,
      message=input.message,
      max_tokens=input.max_tokens,
      temperature=input.max_tokens,
      system_message=ASSISTANT_PERSONA
    )
    return llm_for_chat(inquiry_llm)
  
  return DEFAULT_RESPONSE
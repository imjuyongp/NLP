from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser

from enums import PromptTemplates

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
purchase_chain = build_llm_chain(chatOpenAI, PromptTemplates.PURCHASE_PROMPT)

# Multi-chain
analysis_reply_chain = RunnableMap({
  "analysis":analysis_chain,
  "guide": lambda x: x["guide"],
  "message": lambda x: x["message"]
}) | reply_chain

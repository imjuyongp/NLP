# openAI API를 활용한 챗봇 서비스

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

# 챗 함수
def chat(msgs: str) -> str:
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role":"system", "content":"You are a helpful assistant"},
      {"role":"user", "content":msgs},
    ],
    max_tokens=200,
    temperature=0.8,
  )
  return response.choices[0].message.content.strip()

# 실행 테스트
print(chat("내 나이 24살. 인생이란 뭘까?"))
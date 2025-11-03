# OpenAI API를 활용한 뉴스요약 서비스
from dotenv import load_dotenv
load_dotenv() # .env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI() # API키 생략

# 뉴스 요약 함수
def summarize(text):
  system_instruction = "assistant는 user의 입력을 요약하여 명목형 3개로 요약해준다"

  messages = [{"role":"system", "content":system_instruction},
              {"role":"user", "content":text}
              ]
  
  response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=messages,
          max_tokens=200
      )
  return response.choices[0].message.content.strip()

# # 테스트용 뉴스
# text = """ 연세대학교(총장 윤동섭)와 한국정책학회(KAPS)가 공동 주최하고 Google이 후원한 ‘2025 아시아 임팩트 해커톤’이 지난 5월 9일 연세대 신촌캠퍼스에서 성공적으로 마무리됐다. 이번 해커톤은 AI와 디지털 기술을 활용해 사회문제를 해결하고자 하는 아시아 청년들의 창의적 아이디어를 발굴하고, 청년들이 공공문제에 대해 더 깊이 고민하고, 이를 실천으로 이어갈 수 있도록 돕는 교육적 취지에서 마련됐다.
# 이 행사는 2024년 국내 대학생을 대상으로 한 ‘Yonsei–KAPS Hackathon for Social Good’으로 처음 개최됐으며, 올해는 아시아 12개국에서 300여 개 팀이 참여하는 국제 규모로 확대돼 ‘Asia Impact Hackathon’으로 발전했다. 2개월간의 지역 예선과 본선 과정을 거쳐 한국(2팀), 베트남(2팀), 싱가포르(1팀), 말레이시아(1팀) 등 총 6개 팀이 최종 결선에 진출했으며, 결선은 온라인과 오프라인을 병행한 하이브리드 방식으로 진행됐다. 참가자들은 AI 번역, 사이버 사기 예방, 폐기물 관리, 가짜뉴스 탐지 등 다양한 주제를 바탕으로 기술을 활용한 공공문제 해결 방안을 제시해 주목을 받았다.
# 이번 해커톤은 연세대 행정학과와 계산과학공학과 BK21 교육연구단이 공동 주관했으며, 인문사회와 이공계가 결합된 융합형 심사 체계를 통해 기존 해커톤과 차별화된 경쟁력을 보였다.
# 결선 개회식은 홍순만 연세대 행정학과 BK21 교육연구단장의 사회로 진행됐으며, 박형준 한국정책학회장의 환영사와 이지섭 구글코리아 플랫폼 및 디바이스 부문 대외협력 총괄의 축사로 시작됐다. 심사위원장을 맡은 신원용 연세대 계산과학공학과 교수는 기술을 통해 사회에 기여하는 방향성을 주요 평가 기준으로 삼아 심사를 진행했으며, 이요한 구글 아태지역 플랫폼 및 디바이스 대외협력 상무는 참가자들의 높은 실행력과 창의성에 대해 긍정적인 평가를 전했다.
# 이번 해커톤의 대상은 대한민국 대표로 출전한 서경대학교 팀 ‘글로벌타임즈’가 수상했다. 김온유(컴퓨터공학과), 김주영·박성연(소프트웨어학과), 송수진(글로벌비즈니스어학부·소프트웨어학과) 학생으로 구성된 팀은, 언어 장벽을 넘어 다양한 글로벌 시각의 뉴스와 실시간 트렌드를 누구나 쉽게 접할 수 있도록 돕는 AI 기반 뉴스 요약·이해 플랫폼을 개발해 높은 평가를 받았다. 홍순만 단장은 “다양한 배경을 가진 아시아 학생들이 서로의 사회문제에 대해 고민하고 해법을 공유하는 뜻깊은 자리였다”며, “참가자들의 창의성과 실행력, 그리고 공공문제에 대한 진지한 태도가 매우 인상 깊었다”고 밝혔다.
# """
# print(summarize(text))

# -------- [fast API] --------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputText(BaseModel):
  text:str

@app.post("/summarize")
def sumarize(input_text: InputText):
  summary = summarize(input_text.text)
  return {"summary":summary}
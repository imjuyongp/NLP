# openAI API를 활용한 광고문구 작성 서비스

from dotenv import load_dotenv
load_dotenv() # .env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI() # API키 생략

# 광고 문구 작성 클래스
class SloganGenerator:
  def __init__(self, engine='gpt-4o-mini'):
    self.engine = engine

  def _infer_using_chatgpt(self, prompt):
    system_instruction = (
      "assistant는 마케팅 문구 작성 도우미다. user의 내용을 참고하여 창의적이고 설득력 있는 마케팅 문구를 작성하시오" 
    )
    messages = [
      {"role":"system","content": system_instruction},
      {"role":"user","content": prompt}
    ]
    response = client.chat.completions.create(
      model = self.engine,
      messages=messages,
      max_tokens=200,
      temperature=0.8
    )
    return response.choices[0].message.content.strip()
  
  def generate(self, product_name, details, tone_and_manner):
    prompt = f"제품 이름 : {product_name}\n주요내용: {details}\n광고 문구의 스타일: {tone_and_manner}\n"

    result = self._infer_using_chatgpt(prompt=prompt)
    return result
  
# # 광고문구 작성 실행
# slogan_generator = SloganGenerator(engine="gpt-4o-mini")
# mySlogan = slogan_generator.generate(product_name="서경대 소프트웨어학과",
#                                        details = "4차 산업혁명시대, 지능정보사회를 ON 하는 고급SW개발 인재를 양성합니다.",
#                                        tone_and_manner="과장"
#                                        )
# print(mySlogan)

# -------- [fast API] --------
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
  product_name: str
  details: str
  tone_and_manner: str

@app.post("/create_ad_slogan")
def create_ad_slogan(product:Product):
  slogan_generator = SloganGenerator("gpt-4o-mini")

  ad_slogan = slogan_generator.generate(product_name=product.product_name,
                                        details=product.details,
                                        tone_and_manner=product.tone_and_manner)
  return {"ad_slogan": ad_slogan}
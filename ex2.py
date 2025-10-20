from dotenv import load_dotenv
load_dotenv() #.env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model = "gpt-4o-mini",
  messages=[
    {
      "role":"system",
      "content":"당신은 소프트웨어과 상담사다."
    },
    {
      "role":"user",
      "content":"신입생이 배우기 좋은 언어를 하나만 추천해줘. 언어 이름만 알려줘."
    },
    {
      "role":"assistant",
      "content":"코불(Cobol)"
    },
    {
      "role":"user",
      "content":"활용 분야를 간단히 설명해줘"
    },
  ],
)

print(completion.choices[0].message.content) #응답메세지만 출력
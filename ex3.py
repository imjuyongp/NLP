from dotenv import load_dotenv
load_dotenv() #.env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI()

# ----- 감성 분류 ----- #

completion = client.chat.completions.create(
  model = "gpt-4o-mini",
  messages=[
    {
      "role":"system",
      "content":"입력한 문장을 보고 긍정인지 부정인지 감성을 분류해줘"
    },
    # 원하는 형태의 정확한 답을 위해, 예시 2개 제공 : Two-shot
    {
      "role":"user",
      "content":"지루해서 영화보는 내내 졸았다."
    },
    {
      "role":"assistant",
      "content":"부정 -_- "
    },
    {
      "role":"user",
      "content":"친구랑 다시 보고 싶은 영화다."
    },
    {
      "role":"assistant",
      "content":"긍정 ^o^"
    },
    
    {
      "role":"user",
      "content":"내인생 최고의 영화였다."
    },
  ]
)

print("AI챗봇: " + completion.choices[0].message.content)
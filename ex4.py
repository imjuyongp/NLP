from dotenv import load_dotenv
load_dotenv() #.env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI()

# Multi-turn을 위해 이전 메세지 저장 : 초기 값
messages = [
  {
    "role":"system",
    "content":"너는 친절하고 유능한 비서야."
  }
]

while True:
  user_input = input("사용자 입력 : ")

  if user_input.lower() in ['bye','오늘은여기까지']:
    print("AI챗봇: 다음에 또 만나요!")
    break
  
  # Multi-turn을 위해 이전 메세지에 "user" 메세지 추가
  messages.append(
    {
      "role":"user",
      "content":user_input
    }
  )

  # ----- assistant 응답 생성 처리 ----- #
  
  completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=messages
  )
  response = completion.choices[0].message.content
  print("AI챗봇: ", response)

  # Multi-turn을 위해 이전 메세지에 "assistant" 메세지 추가
  messages.append(
    {
      "role":"assistant",
      "content":response
    }
  )
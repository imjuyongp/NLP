from dotenv import load_dotenv
load_dotenv() #.env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model = "gpt-4o-mini",
  messages=[
    {
      "role":"user",
      "content":"너는 누구니?"
    }
  ]
)

print(completion.choices[0].message.content) #응답메세지만 출력
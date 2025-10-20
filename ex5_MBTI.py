import json
from dotenv import load_dotenv
load_dotenv() #.env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI()

def generate_mbti_questions():
  prompt = """
MBTI 성격 유형을 테스트하기 위한 객관식 질문 4개를 JSON 형식으로 만들어줘.
각 질문을 통해 다음 MBTI 요소를 순서대로 판별한다.
1. 외향형(E) vs. 내향형(I)
2. 감각형(S) vs. 직관형(N)
3. 사고형(T) vs. 감정형(F)
4. 판단형(J) vs. 인식형(P)

##출력 형식 예시:
{ "questions":[
    { "question" : "사람들과 함계 있을 때, 에너지가 어떻게 변하나요?",
      "options" : {
            "a" : "여러 사람과 이야기하며 에너지가 충전된다.",
            "b" : "혼자만의 시간을 보내며 에너지가 회복된다."
            },
            "types" : {
                  "a" : "E",
                  "b" : "I"
                }
              },
              ...
              ]
}

"""
  completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
      {
        "role":"user",
        "content":prompt
      }
    ],
    response_format={
      "type":"json_object"
    }
  )
  return completion.choices[0].message.content

def take_mbti_test(questions):
  questions = json.loads(questions)
  mbti = ""
  for item in questions["questions"]:
    print("="*50)
    print(f"[질문] {item['question']}")
    print(f"  a) {item['options']['a']}")
    print(f"  b) {item['options']['b']}")
    print("-"*50)

    answer = input("답변을 입력하세요 (a또는 b 입력): ")
    if answer in item["types"]:
      mbti += item["types"][answer]

  return mbti 

def mbti_analysis(mbti_type):
  completion = client.chat.completions.create(
      model = "gpt-4o-mini",
      messages=[
        {
          "role":"user",
          "content":f"{mbti_type} 성격 유형의 특징을 3문장 이내로 설명해줘."
        }
      ]
  )
  return completion.choices[0].message.content

# ----- MBTI 테스트 ----- #
print("*** MBTI 테스트 ***")

#(1) MBTI 질문지 생성
questions = generate_mbti_questions()
print(questions)

#(2) 사용자가 질문지에 답변
mbti_type = take_mbti_test(questions)
print("="*50)
print(f" >> 당신의 MBTI 유형은 {mbti_type} 입니다.")

#(3) 답변으로 성격 유형 분석
result = mbti_analysis(mbti_type)

#(4) MBTI 테스트 결과 출력
print(result)
print('\n=== 테스트가 종료되었습니다 ===')
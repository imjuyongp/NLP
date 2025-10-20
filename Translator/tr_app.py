import streamlit as st
from dotenv import load_dotenv
load_dotenv() #.env 파일에서 API키를 불러와서 등록해줌

from openai import OpenAI
client = OpenAI()

# --- 번역 작업 함수 정의 ---
def translate_text_using_chatgpt(text, src_lang, trg_lang):
  completion = client.chat.completions.create(
    model = "gpt-4o-mini",
      messages=[
        {
          "role":"system",
          "content":f"You are a translate assistant that accurately translates {src_lang} text into {trg_lang}."
        },
        {
          "role":"user",
          "content":text
        }
      ],
      temperature=0.7, # 자연스러운 번역을 위해 적당한 온도 설정
      max_tokens=100
  )
  translated_text = completion.choices[0].message.content.strip()
  return translated_text

# ---<< 서비스 웹 페이지 >>---
st.title("변역 서비스")
text = st.text_area("변역할 텍스트를 입력하세요", "")
src_lang = st.selectbox("원본 언어", ["영어", "한국어", "일본어"])
trg_lang = st.selectbox("목표 언어", ["영어", "한국어", "일본어"], index=1)
if st.button("번역"):
  translated_text = translate_text_using_chatgpt(text, src_lang, trg_lang)
  st.success(translated_text)
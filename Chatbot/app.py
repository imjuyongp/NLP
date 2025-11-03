import streamlit as st
from streamlit_chat import message
import requests

chat_url = "http://localhost:8000/chat"

# 이전 메세지 관리
if 'messages' not in st.session_state:
  st.session_state['messages'] = [] # 채팅 기록 리스트 초기화

def chat(text):
  user_turn = {"role":"user","content" : text}
  messages = st.session_state['messages']
  res = requests.post(chat_url, json={"messages":messages + [user_turn]})
  assistant_turn = res.json()

  st.session_state['messages'].append(user_turn)
  st.session_state['messages'].append(assistant_turn)

st.title("챗봇 서비스")

row1 = st.container() # 채팅 메세지 출력 영역(화면 상단)
row2 = st.container() # 새 메세지 입력창 영역(화면 하단)

with row2: # 새 메세지 입력창(화면 하단)
  input_text = st.chat_input("메세지를 입력하세요...")
  if input_text:
    chat(input_text)

with row1:
  for i, msg_obj in enumerate(st.session_state['messages']):
    msg = msg_obj['content']
    is_user = False
    if i%2 == 0: # 현재 턴이 assistant면 
      is_user = True # 다음 턴은 user이다
    
    message(msg, is_user=is_user, key=f"chat_{i}") 

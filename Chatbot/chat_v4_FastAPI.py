import streamlit as st
import requests as req

# 챗봇 서비스 서버 url
chat_url = "http://localhost:8000/chat"

st.title("💬 고객센터 Chain 챗봇")
st.caption("🚀 실습")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def chat_input(message: str = ""):
    res = req.post(
        chat_url,
        json={
            "message":message
        }
    )
    res = res.json()

    return res

if prompt := st.chat_input(): # 사용자가 입력하면 실행
    st.session_state.messages.append({"role":"user", "content":prompt})
    st.chat_message("user").write(prompt)

    msg = chat_input(message=prompt)
    st.session_state.messages.append({"role":"assistant", "content":msg})
    st.chat_message("assistant").write(msg)

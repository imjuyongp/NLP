import streamlit as st
import requests as req

# 챗봇 서비스 서버 url
chat_url = "http://localhost:8080/chat"

st.title("💬 고객센터 챗봇")
st.caption("🚀 실습")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

def chat_input(
  message: str = "",
  model: str = "gpt-4o-mini",
  max_tokens: int = 200,
  temperature: float = 0.8,
):
    res = req.post(
        chat_url,
        json={
            "message":message,
            "model":model,
            "max_tokens":max_tokens,
            "temperature":temperature,
        },
    )

    res = res.json()

    return res


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    msg = chat_input(message=prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
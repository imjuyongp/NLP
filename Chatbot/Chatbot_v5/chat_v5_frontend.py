import streamlit as st
import requests

st.title("ChatGPT-Langchain Chatbot")

API_URL = "http://localhost:8000/chat"

if "messages" not in st.session_state:
  st.session_state["messages"] = []

for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
  st.session_state.messages.append({"role":"user", "content":prompt})
  st.chat_message("user").write(prompt)

  res = requests.post(API_URL, json={"message":prompt})
  reply = res.json()

  st.session_state.messages.append({"role":"assistant","content":reply})
  st.chat_message("assistant").write(reply)
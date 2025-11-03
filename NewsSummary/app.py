import streamlit as st
import requests
# 파일 업로드 기능 추가
import pandas as pd
import io
import os

if 'prev_upload_file' not in st.session_state:
  st.session_state['prev_upload_file'] = None
  st.session_state['prev_df'] = None

summarize_url = "http://localhsot:8000/summarize"

def summarize(text):
  response = requests.post(summarize_url, json={"text":text})
  summary = response.json()["summary"]
  return summary

def summarize_df(df):
  global progress_bar

  total = len(df)
  news_summeries = []
  for i, news_origin in enumerate(df['뉴스원문'], start=1):
    summary = summarize(summary)

    progress_bar.progress(i/total, text="progress")

  df['뉴스요약'] = news_summeries
  return df

# df를 엑셀 파일로 저장하기
def to_excel(df):
  output = io.BytesIO()
  writer = pd.ExcelWriter(output, engine="xlsxwriter")
  df.to_excel(writer, sheet_name="Sheet1", index=False)
  writer.save()
  processed_data = output.getvalue()
  return processed_data

st.title("요약 서비스")

tab1, tab2 = st.tabs(["실시간", "파일 업로드"])

with tab1:
  input_text = st.text_area("여기에 텍스트를 입력하세요", height=300)
  if input_text:
    try:
      summary = summarize(input_text)
      st.success(summary)
    except:
      st.error("요청 오류가 발생했습니다.")
  else:
    st.warning("텍스트를 입력하세요.")

with tab2:
  uploaded_file = st.file_uploader("Choose a file")

  if uploaded_file:
    st.success("업로드 성공!")

    if uploaded_file == st.session_state['prev_upload_file']:
      df = st.session_state['prev_df']
    else:
      progress_bar = st.progress(0, text="progress")

      df = pd.read_excel(uploaded_file)

      df = summarize_df(df)
      st.dataframe(df)

      st.session_state['prev_upload_file'] = uploaded_file
      st.session_state['prev_df'] = df

    file_base_name = os.path.split(os.path.basename(uploaded_file))[0]
    st.download_button(
      label="Download",
      data=to_excel(df),
      file_name=f"{file_base_name}_summarized.xlsx"
    )

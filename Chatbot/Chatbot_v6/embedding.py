import os 
os.environ["USER_AGENT"] = "myDB/1.0"

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import bs4

base_dir = os.path.dirname(os.path.abspath(__file__)) # 현제 파일 디렉토리
file_path = os.path.join(base_dir, "../database/products.txt")

COLLECTION_NAME = "basic_vectordb"
PERSIST_DIRECTORY = os.path.abspath(os.path.join(base_dir,"../database/chroma"))

def chroma_create(docs, collection_name: str, persist_directory: str):
  embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
  vectorstore = Chroma.from_documents(
    documents = docs,
    embedding=embeddings,
    collection_name=collection_name,
    persist_directory=persist_directory,
  )
  return vectorstore

# text docs
def embedding_from_text(file_path:str) -> dict:
  loader = TextLoader(os.path.abspath(file_path), encoding="utf-8")

# web docs : 웹 페이지 데이터 크롤링
def embedding_from_url(url:str)-> dict:
  loader = WebBaseLoader(
    web_path=(url,),
    bs_kwargs=dict(
      parse_only=bs4.SoupStrainer(
        "section",
        attrs={"class":["news_view"]},
      )
    ),
  )

  docs = loader.load()
  # 문장 단위 분할
  splitter = RecursiveCharacterTextSplitter(
    chunk_size=250, # 최대 글자 수
    chunk_overlap=50, # 겹치는 글자 수
    length_function=len,
    separators=[".","!","?"] # 문장 단위로
  )
  split_docs = splitter.split_documents(docs)
  return chroma_create(split_docs, COLLECTION_NAME, PERSIST_DIRECTORY)

### 실행 ###
if __name__ == "__main__":
  print('-'*10, "(1) url 크롤링 -> chromaDB 저장")
  url = "https://www.donga.com/news/Society/article/all/20250515/131614264/1"

  chromaDB = embedding_from_url(url)

  docs1 = chromaDB.similarity_search("서경대학교", k=2) # ChromaDB에서 검색
  print("doc1: ", docs1)
  docs2 = chromaDB.similarity_search("참자가", k=2) # chromaDB에서 검색
  print("doc2: ", docs2)

  # retrieve object
  print('-'*10, "(2) 파일 업로드 -> chromaDB 저장")
  file = os.path.join(base_dir,"../database/products.txt")

  chromaDB = embedding_from_text(file)

  retriever = chromaDB.as_retriever()
  docs3 = retriever.invoke("소웨 밥솥")
  print("docs3: ", docs3)

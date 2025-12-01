from enum import Enum
import os
os.environ["USER_AGENT"] = "myDB/1.0"

class ChromaDB(str, Enum):
  base_dir = os.path.dirname(os.path.abspath(__file__))
  file_path = os.path.join(base_dir, "../database/products.txt")

  COLLECTION_NAME = "basic_vectordb"
  PERSIST_DIRECTORY = os.path.abspath(os.path.join(base_dir,"../database/chroma"))

class PromptTemplates(str,Enum):
  INTENT_PROMPT = """ choose the one of the following intents for the user message
  [intents] {intents}
  User : i have a problem, your service is aweful
  classifier : complaint
  User: {message}
  classifier :"""

  INQUIRY_ANALYSIS_PROMPT = """analysis the user's message for inquiry
  User: {message}
  Analysis :"""

  INQUIRY_REPLY_PROMPT = """reply to the user's inquiry message with inquiry analysis and Customer Center Guide
  [inquiry analysis] {analysis}
  [Customer Center Guide] {guide}
  User: {message}
  Reply:"""

  # Templates 추가
  PURCHASE_PROMPT = """
relay the user's purchase mseeage wuth the following product details
[product details]
User: {message}
Relay:
"""
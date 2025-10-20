from typing import Union

from fastapi import FastAPI

app = FastAPI()

items = {
  0: {"name":"NLP",
      "grade":"A+"},
  1: {"name":"ML",
      "grade":"A"},
  2: { "name":"Capstone",
        "grade":"B+"},
}

@app.get("/")
def read_root():
  return {"Hello":"World"}

@app.get("/items/{item_id}/{key}")
def read_item(item_id: int, key: str = None):
  if key == None: return items[item_id]
  else : return items[item_id][key]
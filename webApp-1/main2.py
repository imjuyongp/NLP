from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

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

@app.get("item-by-name")
def read_item_by_name(name: str):
  for item_id, item in items.items():
    if item['name'] == name:
      return item
  return {"error":"data not found"}

class Item(BaseModel):
  name: str
  grade: str

@app.post("/items/{item_id}")
def create_item(item_id:int, item: Item):
  if item_id in items:
    return {"error": "there is already existing key."}
  items[item_id]= item.dict()
  return {"success":"ok"}

class ItemForUpdate(BaseModel):
  name : Optional[str]
  grade : Optional[str]

@app.put("/items/{item_id}")
def update_item(item_id:int, item: ItemForUpdate):
  if item_id not in items:
    return {"error":f"there is no item id: {item_id}"}
  
  if item.name:
    items[item_id]['name'] = item.name

  if item.grade:
    items[item_id]['grade'] = item.grade

  return {"success":"ok"}

@app.delete("/items/{item_id}")
def delete_item(item_id:int):
  items.pop(item_id)
  return {"success":"ok"}
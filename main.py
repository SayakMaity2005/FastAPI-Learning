from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return {"data": {"Nane": "Sayak"}}

@app.get("/sayak")
def sayak():
    return {"data": ["Sayak"]}

@app.get("/sayak/blogs")
def sayak(limit=10, published: Optional[bool] = True):
    return {"data": f"{limit} blogs {"published" if published else ""}"}


class Item(BaseModel):
    name: str
    description: str | None = None
    


@app.post("/items/")
async def create_item(item: Item):
    return item.name
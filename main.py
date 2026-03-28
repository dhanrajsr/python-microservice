from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple API", version="1.0.0")

# In-memory store
items: dict[int, dict] = {}
next_id = 1


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemResponse(Item):
    id: int


@app.get("/")
def root():
    return {"message": "Welcome to the Simple API"}


@app.get("/items", response_model=list[ItemResponse])
def get_items():
    return [{"id": k, **v} for k, v in items.items()]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items[item_id]}


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    global next_id
    items[next_id] = item.model_dump()
    created = {"id": next_id, **items[next_id]}
    next_id += 1
    return created

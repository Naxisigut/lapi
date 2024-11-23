from fastapi import APIRouter, HTTPException
from app.models.item import Item

router = APIRouter()

items = []

@router.get("/items/", tags=["items"])
async def read_items():
    return items

@router.post("/items/", tags=["items"])
async def create_item(item: Item):
    items.append(item)
    return item

@router.get("/items/{item_id}", tags=["items"])
async def read_item(item_id: int):
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id] 
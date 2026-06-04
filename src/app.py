import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request

from src.schemas import Item

json_file_path = Path(__file__).parent / "product_list.json"
with open(json_file_path, "r") as file:
    data = json.load(file)

product_list = data["product_list"]


app = FastAPI()


# get all items
@app.get("/")
async def root():
    return "Product API is running"


@app.get("/items/")
async def get_all_items():
    return product_list


# request body + path parameters
@app.get("/items/{item_id}")
async def get_items(item_id: int):
    item = product_list.get(str(item_id))
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()

    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    token = params.get("hub.verify_token")  # VERIFY_TOKEN
    challenge = params.get("hub.challenge")  # send this if everything fine
    mode = params.get("hub.mode")  # subscribe

    if mode == "subscribe" and token == VERIFY_TOKEN and challenge is not None:
        return int(challenge)

    raise HTTPException(status_code=403, detail="INVALID VERIFICATION TOKEN")

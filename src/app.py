import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request

from src.whatsapp import extract_message, send_text_message

# loading the product_list json
json_file_path = Path(__file__).parent / "product_list.json"
with open(json_file_path, "r") as file:
    data = json.load(file)

product_list = data["product_list"]

# initializing
app = FastAPI()


@app.get("/")
async def root():
    return "Product API is running"


# get all items
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


# handshake ( 1 time )
load_dotenv()
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


@app.post("/webhook")
async def receive_webhook(request: Request, background_task: BackgroundTasks):
    data = await request.json()

    incoming = extract_message(data)

    if not incoming:
        return {"status": "ignored"}

    sender = incoming["sender"]
    text = incoming["text"]

    background_task.add_task(send_text_message, sender, f"You Said:{text}")

    return {"status": "received"}

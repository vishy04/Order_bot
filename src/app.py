import json
import os

from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request

from src.bot import handle_user_message
from src.security import verify_meta_signature
from src.whatsapp import extract_message, send_text_message

load_dotenv()

app = FastAPI()
VERIFY_TOKEN = os.getenv("META_VERIFICATION_TOKEN")


@app.get("/")
async def root():
    return {"status": "Product API is running"}


@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params

    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    mode = params.get("hub.mode")

    if mode == "subscribe" and token == VERIFY_TOKEN and challenge is not None:
        return int(challenge)

    raise HTTPException(status_code=403, detail="INVALID VERIFICATION TOKEN")


@app.post("/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    raw_body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not signature:
        raise HTTPException(status_code=403, detail="MISSING SIGNATURE")

    if not verify_meta_signature(raw_body=raw_body, signature_header=signature):
        raise HTTPException(status_code=403, detail="INVALID SIGNATURE")

    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="INVALID JSON BODY")

    incoming = extract_message(data)

    if not incoming:
        return {"status": "ignored"}

    sender = incoming["sender"]
    text = incoming["text"]

    if not text:
        reply = "Please send a text message."
    else:
        # turn to async as handle_user is async now after product database search
        reply = await handle_user_message(text)

    background_tasks.add_task(send_text_message, sender, reply)

    return {"status": "received"}

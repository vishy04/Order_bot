import os

import httpx
from dotenv import load_dotenv

load_dotenv()

GRAPH_API_VERSION = "v20.0"


async def send_text_message(user: str, text: str):
    access_token = os.getenv("META_ACCESS_TOKEN")
    phone_id = os.getenv("META_PHONE_ID")

    if not access_token:
        print("WhatsApp send skipped: META_ACCESS_TOKEN is missing")
        return {"status": "failed", "reason": "missing_access_token"}

    if not phone_id:
        print("WhatsApp send skipped: META_PHONE_ID is missing")
        return {"status": "failed", "reason": "missing_phone_id"}

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{phone_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": user,
        "type": "text",
        "text": {
            "body": text,
        },
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, headers=headers, json=payload)

        if response.status_code >= 400:
            print("WhatsApp send failed:", response.status_code, response.text)
            return {
                "status": "failed",
                "status_code": response.status_code,
                "error": response.text,
            }

        return response.json()


# https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started
def extract_message(data: dict):
    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return None

        message = value["messages"][0]
        sender = message["from"]
        message_type = message["type"]

        if message_type == "text":
            return {
                "sender": sender,
                "type": "text",
                "text": message["text"]["body"],
            }

        return {"sender": sender, "type": message_type, "text": None}

    except (KeyError, IndexError, TypeError):
        return None

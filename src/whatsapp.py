import os

import httpx

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_ID = os.getenv("META_PHONE_ID")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
GRAPH_API_VERSION = "v20.0"


async def send_text_message(user: str, text: str):

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
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
        response.raise_for_status()
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
            body = message["text"]["body"]
            return {
                "sender": sender,
                "type": "text",
                "text": body,
            }
        else:
            return {"sender": sender, "type": message_type, "text": None}

    except KeyError:
        return None

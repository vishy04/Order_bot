import os

import httpx

ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_ID = os.getenv("META_PHONE_ID")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
GRAPH_API_VERSION = "v20.0"


async def send_text_message(access_token: str, phone_id: str, graph_api_version: str):

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": PHONE_NUMBER,
        "type": "template",
        "template": {"name": "hello_world", "language": {"code": "en_US"}},
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

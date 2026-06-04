import json
from pathlib import Path

json_file_path = Path(__file__).parent / "product_list.json"

with open(json_file_path, "r") as file:
    data = json.load(file)

product_list = data["product_list"]

welcome_message = """Welcome to our store 👋
Type:
products - View all products
help - Show commands
"""
help_message = "currently only listing of products supported"


def handle_user_message(text: str):

    text = text.lower().strip()

    if text in ["hi", "hello", "start"]:
        return welcome_message

    if text == "help":
        return help_message

    if text == "products":
        return get_product_list(product_list)

    if text.isdigit():
        return product_list[text]

    return "Please Enter a valid command"


def get_product_list(product_list: dict):

    reply = []

    for id, product in product_list.items():
        name = product.get("name", "unknown")
        price = product.get("price", 0)
        tax = product.get("tax", 0)
        reply.append(f"{id}.{name} - ₹{price + tax}")

    return reply

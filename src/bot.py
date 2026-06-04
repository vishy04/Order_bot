# src/bot.py

import json
from pathlib import Path

json_file_path = Path(__file__).parent / "product_list.json"

with open(json_file_path, "r") as file:
    data = json.load(file)

product_list = data["product_list"]


def handle_user_message(text: str) -> str:
    text = text.lower().strip()

    if text in ["hi", "hello", "start"]:
        return get_welcome_message()

    if text == "help":
        return get_help_message()

    if text in ["products", "menu", "items"]:
        return get_product_list_message()

    if text.isdigit():
        return get_product_detail_message(text)

    if text.startswith("order "):
        product_id = text.replace("order ", "").strip()
        return place_order_message(product_id)

    return get_fallback_message()


def get_welcome_message() -> str:
    return (
        "Welcome to our store 👋\n\n"
        "Type:\n"
        "products - View all products\n"
        "help - Show commands"
    )


def get_help_message() -> str:
    return (
        "Available commands:\n\n"
        "hi - Start chat\n"
        "products - View products\n"
        "1 - View product details\n"
        "order 1 - Order product 1"
    )


def get_product_list_message() -> str:
    lines = ["Available products:\n"]

    for product_id, product in product_list.items():
        name = product.get("name", "Unknown")
        price = product.get("price", "N/A")
        lines.append(f"{product_id}. {name} - ₹{price}")

    lines.append("\nReply with product ID to see details.")
    lines.append('Reply "order 1" to order product 1.')

    return "\n".join(lines)


def get_product_detail_message(product_id: str) -> str:
    product = product_list.get(product_id)

    if not product:
        return "Product not found. Type products to see available items."

    name = product.get("name", "Unknown")
    description = product.get("description", "No description available")
    price = product.get("price", "N/A")

    return (
        f"{name}\n\n"
        f"Description: {description}\n"
        f"Price: ₹{price}\n\n"
        f"To order, reply: order {product_id}"
    )


def place_order_message(product_id: str) -> str:
    product = product_list.get(product_id)

    if not product:
        return "Product not found. Type products to see available items."

    name = product.get("name", "Unknown")
    price = product.get("price", "N/A")

    return (
        "Order received ✅\n\n"
        f"Product: {name}\n"
        f"Price: ₹{price}\n\n"
        "Our team will contact you soon."
    )


def get_fallback_message() -> str:
    return (
        "Sorry, I did not understand that.\n\n"
        "Type products to view items.\n"
        "Type help to see commands."
    )

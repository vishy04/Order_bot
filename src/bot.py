import json
from pathlib import Path
from typing import Any

from sqlalchemy import select

from src.models import Product
from src.seed_database import AsyncSessionLocal

PRODUCTS_FILE = Path(__file__).parent / "product_list.json"

with open(PRODUCTS_FILE, "r") as file:
    data = json.load(file)

product_list: dict[str, dict[str, Any]] = data["product_list"]


async def handle_user_message(text: str) -> str:
    command = text.lower().strip()

    if command in ["hi", "hello", "start"]:
        return get_welcome_message()

    if command == "help":
        return get_help_message()

    if command in ["products", "menu", "items", "product"]:
        return get_product_list_message()

    if command.isdigit():
        message = await get_product_detail_message(command)
        return message

    if command.startswith("order "):
        product_id = command.removeprefix("order ").strip()
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
        lines.append(f"{product_id}. {name} - {format_price(product)}")

    lines.append("\nReply with product ID to see details.")
    lines.append('Reply "order 1" to order product 1.')

    return "\n".join(lines)


async def get_product_detail_message(product_id: str) -> str:
    async with AsyncSessionLocal() as session:
        # e1: product_id should be int before passing
        query = select(Product).where(Product.product_id == int(product_id))

        result = await session.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            return "Product not found. Type products to see available items."

        return (
            f"{product.name}\n\n"
            f"Description: {product.description}\n"
            f"Price: {product.price}\n\n"
        )


def place_order_message(product_id: str) -> str:
    if not product_id.isdigit():
        return 'Please send order like this: "order 1".'

    product = product_list.get(product_id)

    if not product:
        return "Product not found. Type products to see available items."

    name = product.get("name", "Unknown")

    return (
        "Order received ✅\n\n"
        f"Product: {name}\n"
        f"Total: {format_price(product)}\n\n"
        "Our team will contact you soon."
    )


def get_fallback_message() -> str:
    return (
        "Sorry, I did not understand that.\n\n"
        "Type products to view items.\n"
        "Type help to see commands."
    )


def format_price(product: dict[str, Any]) -> str:
    price = product.get("price") or 0
    tax = product.get("tax") or 0
    total = price + tax

    if isinstance(total, float) and total.is_integer():
        total = int(total)

    return f"₹{total}"

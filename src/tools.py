from langchain_core.tools import tool
from sqlalchemy import select

from src.models import Customer, Orders, Product
from src.seed_database import AsyncSessionLocal


@tool
async def get_all_products():
    """Returns a list of all available products with their id, name, and price."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        rows = result.scalars().all()

        return [
            {
                "product_id": row.product_id,
                "name": row.name,
                "price": row.price,
                "description": row.description,
                "tax": row.tax,
            }
            for row in rows
        ]


@tool
async def get_product_details(product_id: int):
    """Returns full details for a single product by its ID."""
    async with AsyncSessionLocal() as session:
        query = select(Product).where(Product.product_id == product_id)

        result = await session.execute(query)
        product = result.scalar_one_or_none()

        if not product:
            return {"error": "Product not found"}

        return {
            "product_id": product.product_id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "tax": product.tax,
        }


@tool
async def resolve_customer(customer_contact: str):
    """Get Customer details from there contact"""
    async with AsyncSessionLocal() as session:
        query = select(Customer).where(Customer.customer_contact == customer_contact)
        result = await session.execute(query)
        contact = result.scalar_one_or_none()

        if not contact:
            new_customer = Customer(
                customer_contact=customer_contact, customer_name="Guest"
            )
            session.add(new_customer)
            await session.commit()
            contact = new_customer

        return {
            "customer_id": contact.customer_id,
            "customer_name": contact.customer_name,
            "customer_contact": contact.customer_contact,
        }


@tool
async def place_order(customer_id: int, product_id: int):
    """Create new order with customer id and product id"""
    async with AsyncSessionLocal() as session:
        new_order = Orders(product_id=product_id, customer_id=customer_id)
        session.add(new_order)
        await session.commit()
        await session.refresh(new_order)

        return {
            "order_id": new_order.order_id,
            "customer_id": new_order.customer_id,
            "product_id": new_order.product_id,
            "ordered_date": new_order.ordered_date,
        }

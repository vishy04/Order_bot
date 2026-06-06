import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.models import Base, Product

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def seed_products():
    print("Start")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                "ALTER TABLE products "
                "ALTER COLUMN description TYPE VARCHAR(255) "
                "USING description::text"
            )
        )

    product_list_path = Path(__file__).with_name("product_list.json")
    with product_list_path.open("r") as file:
        data = json.load(file)
        products_list = data["product_list"]
    print("Product list loaded")
    async with AsyncSessionLocal() as session:
        for prod_id, details in products_list.items():
            new_product = Product(
                product_id=int(prod_id),
                name=details["name"],
                description=details["description"],
                price=float(details["price"]),
                tax=float(details["tax"]) if details["tax"] else None,
            )

            # merge inserts new rows or updates existing rows with the same primary key
            await session.merge(new_product)

        await session.commit()
        print("Data Uploaded Sucessfull")


if __name__ == "__main__":
    asyncio.run(seed_products())

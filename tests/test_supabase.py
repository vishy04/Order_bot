import asyncio
import os

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# 1. Load the secret URL from your .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. The Engine: Think of this as the physical cable plugged into Supabase.
# It doesn't send data yet; it just establishes the electrical connection.
engine = create_async_engine(DATABASE_URL, echo=True)

# 3. The Session Factory: Think of this as the worker who actually talks over the cable.
# Every time you need to write or read data, you will ask this factory for a new session.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def test_db():
    print("Attempting to connect to Supabase...")

    # Open a temporary session (like making a phone call)
    async with AsyncSessionLocal() as session:
        try:
            # Send a simple "Hello" query (SELECT 1)
            result = await session.execute(text("SELECT 1"))
            print("✅ CONNECTION SUCCESSFUL! Supabase said:", result.scalar())
        except Exception as e:
            print("❌ Connection failed. Error:", e)


# Run the async function
if __name__ == "__main__":
    asyncio.run(test_db())

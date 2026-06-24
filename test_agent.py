from dotenv import load_dotenv

load_dotenv()

import asyncio

from src.agent_core import graph


async def test():
    result = await graph.ainvoke(
        {
            "messages": [("user", "What products do you have?")],
            "customer_contact": "+911234567890",
            "customer_id": None,
            "customer_name": None,
        }
    )
    print(result["messages"][-1].content)


asyncio.run(test())

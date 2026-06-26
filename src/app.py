import modal

from src.agent_core import graph
from src.cloud_memory import agent_memory
from src.whatsapp import extract_message, send_text_message

app = modal.App("Whatsapp-order-bot")
image = modal.Image.debian_slim().pip_install(
    [
        "asyncpg>=0.31.0",
        "httpx>=0.28.1",
        "langchain-core>=1.4.8",
        "langchain-groq>=1.1.3",
        "langgraph>=1.2.6",
        "pydantic>=2.13.4",
        "python-dotenv>=1.2.2",
        "sqlalchemy>=2.0.50",
    ]
)


@app.function(image=image)
@modal.web_endpoint(method="POST")
async def webhook(data: dict):
    result = extract_message(data)

    if not result:
        return {"status": "ignored"}

    sender = result["sender"]
    text = result["text"]

    history = agent_memory.get(sender, [])

    # using agent and passing everything
    final_state = await graph.ainvoke(
        {
            "messages": history + [("user", text)],
            "customer_contact": sender,
            "customer_id": None,
            "customer_name": None,
        }
    )
    reply = final_state["messages"][-1].content

    agent_memory[sender] = final_state["messages"]
    await send_text_message(sender, reply)

    return {"status": "ok"}

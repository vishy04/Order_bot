import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import SecretStr

from src.tools import (
    get_all_products,
    get_product_details,
    place_order,
    resolve_customer,
)


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    customer_contact: str
    customer_id: int | None
    customer_name: str | None


load_dotenv()

# ChatGroq` uses Pydantic v2 under the hood which requires `SecretStr` for sensitive fields
groq_key = SecretStr(os.getenv("GROQ_API_KEY", ""))

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_key,
)

tools = [get_all_products, get_product_details, resolve_customer, place_order]

llm_with_tools = llm.bind_tools(tools)


graph_builder = StateGraph(AgentState)


# defining nodes
def agent_node(state: AgentState):
    llm_response = llm_with_tools.invoke(state["messages"])
    return {"messages": [llm_response]}


# using ToolNode is imp it takes care if agent returns a tool calls tools_node is called
tools_node = ToolNode(tools)
# adding nodes
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tools_node)

# start from agent_node -> tools_node
graph_builder.set_entry_point("agent")
# this checks if agent returned a tool call
graph_builder.add_conditional_edges("agent", tools_condition)
# links tools -> agent
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()

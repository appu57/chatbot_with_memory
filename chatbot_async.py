from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool, BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
import requests
import asyncio
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages #reducer function to append messages instead of replacing old messages
from langgraph. checkpoint.sqlite import SqliteSaver
from tools import calculator, web_search
from langgraph.prebuilt import ToolNode, tools_condition
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
import threading

load_dotenv()
GROQ_MODEL = "llama-3.3-70b-versatile"
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model=GROQ_MODEL)

# Dedicated async loop for backend tasks
_ASYNC_LOOP = asyncio.new_event_loop()
_ASYNC_THREAD = threading.Thread(target=_ASYNC_LOOP.run_forever, daemon=True)
_ASYNC_THREAD.start()



def _submit_async(coro):
    return asyncio.run_coroutine_threadsafe(coro, _ASYNC_LOOP)


def run_async(coro):
    return _submit_async(coro).result()


def submit_async_task(coro):
    """Schedule a coroutine on the backend event loop."""
    return _submit_async(coro)


class ChatState(TypedDict):
    messages: Annotated[BaseMessage,add_messages ] # such that messages can be classified as human message, system message, AI message
    #if we dont use basemessage then the field value will be simple string, or other datatype and BaseMessage is base class of all three message types
    # annotated and add messages appends new message whereas normal fields replaces old value

client = MultiServerMCPClient(
    {
        "arithmethic":{
            "transport":"stdio", #local server so stdio
            "command":"python3",
            "args":["C:/Users/apoor/Projects/chatbot_with_memory/mcp_tools.py"]
        },
        "expense": {
            "transport": "streamable_http",  # if this fails, try "sse"
            "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
        }
    }
)
@tool
def web_search(query: str) -> str:
    """Searches the live web for recent, real-time, or historical information using DuckDuckGo. 
    Use this whenever you need to find facts or check information.
    """
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

  
def load_mcp_tools() -> list[BaseTool]:
    try:
        return run_async(client.get_tools())
    except Exception:
        return []


mcp_tools = load_mcp_tools()
tools = [web_search, *mcp_tools]
llm_with_tools = llm.bind_tools(tools) if tools else llm

async def build_graph():
    tools = await client.get_tools()
    llm_with_tools = llm.bind_tools(tools)
    async def chat_node(state: ChatState):
        messages = state['messages']
        response = await llm_with_tools.ainvoke(messages)
        return {'messages':[response]} #because messages is a list

    tool_node = ToolNode(tools) #internally async

    graph = StateGraph(ChatState) #state (basically model that holds data)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node"),
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("chat_node",END)
    chatbot = graph.compile()
 
    return chatbot

async def main():
    chatbot = await build_graph()
    initial_state = {
    'messages': [HumanMessage(content="What is the sum of 1000 and 23456789")]
    }
    out =await chatbot.ainvoke(initial_state) #because async use await with invoke when using asyncio
    print(f"output:{out}")


if __name__ == '__main__':
    asyncio.run(main()) 



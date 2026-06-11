from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages #reducer function to append messages instead of replacing old messages

import os
from dotenv import load_dotenv
load_dotenv()
GROQ_MODEL = "llama-3.3-70b-versatile"
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model=GROQ_MODEL)

class ChatState(TypedDict):
    messages: Annotated[BaseMessage,add_messages ] # such that messages can be classified as human message, system message, AI message
    #if we dont use basemessage then the field value will be simple string, or other datatype and BaseMessage is base class of all three message types
    # annotated and add messages appends new message whereas normal fields replaces old value


def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages':[response]} #because messages is a list

graph = StateGraph(ChatState) #state (basically model that holds data)

graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node"),
graph.add_edge("chat_node",END)

from langgraph.checkpoint.memory import MemorySaver, InMemorySaver #stores data in RAM, difference between in-memory and memory saver
checkpointer = InMemorySaver()

chatbot_with_checkpointer = graph.compile(checkpointer=checkpointer)

# for message_chunk, metadata in chatbot_with_checkpointer.stream(
#     {'messages':[HumanMessage(content="Write a blog on langchain")]},
#     config= {'configurable':{'thread_id':'thread-1'}},
#     stream_mode= 'messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content, flush=True)


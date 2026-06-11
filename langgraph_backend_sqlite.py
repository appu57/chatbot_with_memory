from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages #reducer function to append messages instead of replacing old messages
from langgraph. checkpoint.sqlite import SqliteSaver

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


import sqlite3
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False) #works on single thread hence making it false to support multi thread conversation

#A checkpoint is a snapshot of graph state at a particular moment.
checkpointer = SqliteSaver(conn=conn)

chatbot_with_checkpointer = graph.compile(checkpointer=checkpointer)


def get_conversation_threads(): #checkpoint exists in single thread in each conversation , also checkpoint exists in configurable
    #difference is checkpoint in same thread but within messages -> for message history and checkpoint in configurable -> for different window of communication
    #we will pick different conversation threads here.
    configurable_threads = set()
    for checkpoint in checkpointer.list(None): #why None? "Don't filter. Return checkpoints from all threads."
        configurable_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(configurable_threads)

# thread_id identifies a conversation/session. A thread can contain many checkpoints.(each checkpoint is saved snapshot of conversation between each nodes of the graph)
# Each checkpoint is a saved snapshot of the graph state
# after a particular interaction.
#
# checkpointer.list(None) returns checkpoints from all threads.
# We extract unique thread_ids to discover all conversations.
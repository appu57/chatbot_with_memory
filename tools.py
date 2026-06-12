from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import requests


@tool
def web_search(query: str) -> str:
    """Searches the live web for recent, real-time, or historical information using DuckDuckGo. 
    Use this whenever you need to find facts or check information.
    """
    search = DuckDuckGoSearchRun()
    return search.invoke(query)


@tool
def calculator(a: float, b:float, operation:str) -> dict:
    """Performs basic arithmethic operation on two numbers
    Supported operatios: add, sub, mul
    """
    try:
        if operation == 'add':
            result = a+b
        elif operation == 'sub':
            result = a-b
        elif operation == 'mul':
            result = a * b
        else:
            return {"error":f"Unsupported operation: {operation}"}
        
        return {"a":a, "b":b, "operation":operation, "answer": result}

    except Exception as e:
        return {"error": str(e)}

   
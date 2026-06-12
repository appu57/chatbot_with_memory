
In this chatbot we will integrate 
**Chatting + RAG + MCP + tools + UI + langsmith + memory + persistence + HITL + retry + fault tolerance**

Types of messages
1. Human Message: User message
2. AI Message: system response
3. System message : message that contains role and behaviour an LLM has to personate
4. ToolMessage
All of these extends BaseMessage


**Persistence**: Persistence in langgraph refers to the ability to save and restore the state of a workflow over time.
Useful in fault tolerance because if any node crashes the retry starts from same point

**Streaming**: In LLM, streaming means the model starts sending tokens(words) as soon as they are generated, instead of waiting for the entire response to be ready before returning it. 

**Tools and ToolNode**: A toolNode is a prebuilt node type that acts as a bridge between your graph and external tools such as functions, API, utilities
ToolNode is a ready-made node that knows how to handle a list of langchain tools
**tools_condition** is a prebuilt conditional edge function that helps graph decide "Should the flow go to the ToolNode next, or back to the LLM"

**MCP**: When using tools we need to write entire logic, using mcp tool we just need to give server details to connect it.
We need to create MCP client and MCP server (does not provide support to create MCP servers, we have to use FastMCP to create MCP servers)

**ASYNCIO**  VERY IMPORTANT
main is async, Calling it returns a coroutine object, Python needs an event loop to execute coroutines.

When running function outside async of other function
asyncio.run(main())
INTERNALLY 
loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()

Then what is await?
Inside an async function, you can use await.
async def add():
    return 5
async def main():
    x = await add()
    print(x)
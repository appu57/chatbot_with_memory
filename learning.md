
In this chatbot we will integrate 
**Chatting + RAG + MCP + tools + UI + langsmith + memory + persistence + HITL + retry + fault tolerance**

Types of messages
1. Human Message: User message
2. AI Message: system response
3. System message : message that contains role and behaviour an LLM has to personate
All of these extends BaseMessage


Persistence: Persistence in langgraph refers to the ability to save and restore the state of a workflow over time.
Useful in fault tolerance because if any node crashes the retry starts from same point

Streaming: In LLM, streaming means the model starts sending tokens(words) as soon as they are generated, instead of waiting for the entire response to be ready before returning it. 
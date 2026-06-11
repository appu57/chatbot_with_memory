import streamlit as st
from langgraph_backend import chatbot_with_checkpointer
from langchain_core.messages import HumanMessage
# with st.chat_message('User'):
#     st.text('Hi')

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


#message_history = [] #verytime we click on enter after user input the state gets cleared and this also becomes empty so older message dont persist so we use session_state of streamlit
#for messages in message_history: #to show older messages
for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input('Type your message here...')

if user_input:
    st.session_state['message_history'].append({'role':'User', 'content':user_input})
    with st.chat_message('User'): #chat_message and we can set role which displays message as per the role
        st.text(user_input) 


    #stream 
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot_with_checkpointer.stream(
                {'messages':[HumanMessage(content=user_input)]},
                config= {'configurable':{'thread_id':'thread-1'}},
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})

    #Writes entire response at once batch output

    # thread_id = '1'
    # config = {'configurable': {'thread_id':thread_id}}
    # response = chatbot_with_checkpointer.invoke({'messages':[HumanMessage(content=user_input)]}, config=config)
    # ai_message = response['messages'][-1].content
    # st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)
    #with this approach everytime we enter any new input the data gets refreshed so we use dict
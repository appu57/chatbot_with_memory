#Main chatbot streamlit code (ChatGPT-clone with threads)
import streamlit as st
from langgraph_backend_sqlite import chatbot_with_checkpointer, get_conversation_threads
from langchain_core.messages import HumanMessage, AIMessage
import uuid

################### utility function
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def new_thread_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []
    add_new_thread(st.session_state['thread_id'])

def add_new_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    """ Gets the conversation history using .get_state because langgraph stores conversation for each thread"""
    return chatbot_with_checkpointer.get_state(config= get_config(thread_id)).values['messages']

def get_config(thread_id):
    return {'configurable':{'thread_id': thread_id}}



################### INITIALISE SESSION STATE TO PERSIST DATA ACROSS NEW CHAT ENTRY

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state: #if thread_id isnt there only then in initialisation its set, else it gets set in new_thread_chat
    st.session_state['thread_id'] = generate_thread_id() 

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = get_conversation_threads()
    
################### SIDEBAR UI

st.sidebar.title('Langgraph Chatbot')

if st.sidebar.button('New Chat'): #on click of button
    new_thread_chat()

st.sidebar.header('My Conversations')

# st.sidebar.text(st.session_state['thread_id']) shows only current state id in sidebar
#st.sidebar.button(str(thread_id)) means display , if st.sidebar.button(str(thread_id)): means button is clicked
# to display all thread conversation
for thread_id in st.session_state['chat_threads']:
   if st.sidebar.button(str(thread_id)):
    st.session_state['thread_id'] = thread_id 
    messages= load_conversation(thread_id)

    format_message = []
    for message in messages:
        if isinstance(message, HumanMessage):
            role = 'user'
        else:
            role = 'assistant'
        format_message.append({'role':role,'content':message.content})
    
    st.session_state['message_history'] = format_message


################## MAIN PAGE UI

# {'role':'user', 'content':'content'}
# {'role':'assistant', 'content':'content'}
for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.text(messages['content'])

user_input = st.chat_input('Type your message here...')

if user_input:
    st.session_state['message_history'].append({'role':'User', 'content':user_input})
    with st.chat_message('User'): 
        st.text(user_input) 

    with st.chat_message('assistant'):
        #exclude tool message
        def ai_only_stream():
            for message_chunk, metadata in chatbot_with_checkpointer.stream(
                {
                    "messages": [HumanMessage(content=user_input)]   
                },
                 config= get_config(st.session_state['thread_id']),
                 stream_mode= 'messages'
            ):
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        #Shows any message can be toolMessage, AIMessage everythin
        # ai_message = st.write_stream(
        #     message_chunk.content for message_chunk, metadata in chatbot_with_checkpointer.stream(
        #         {'messages':[HumanMessage(content=user_input)]},
        #         config= get_config(st.session_state['thread_id']),
        #         stream_mode= 'messages'
        #     )
        # )
    st.session_state['message_history'].append({'role':'assistant', 'content':ai_message})
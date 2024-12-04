import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Initialization function to load environment variables and set page configuration

def init():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="Your own ChatGPT",
        page_icon="🤖"
    )

# Function for the Streamlit app

def main():
    init()
    # Set up the chat model with gpt-3.5-turbo
    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
    # Display app header
    st.header("Custom ChatGPT 🤖")

    with st.sidebar:
        # Input for user messages
        user_input = st.text_input("Your message", key="user_input")

        # Process user input
        if user_input:
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner("Loading..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            

    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content, is_user=True, key = str(i) + '_user')
        else:
            message(msg.content, is_user=False, key = str(i) + '_ai')

if __name__ == '__main__':
    main()
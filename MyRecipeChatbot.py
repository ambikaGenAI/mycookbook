from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.messages import SystemMessage

import streamlit as st
from streamlit_chat import message

import os
#from dotenv import load_dotenv
#load_dotenv()
#Google_API_KEY=os.getenv("GOOGLE_API_KEY")
#os.environ["GOOGLE_API_KEY"]=Google_API_KEY

os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]

Google_flash_model=ChatGoogleGenerativeAI(model="gemini-1.5-flash-002")

if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys():
    st.session_state.messages=[{"role":"Assistant","content":" What recipe would you like?"}]

system_message=""" You are a Chef and you will help in preparing receipes for the user imput. You will not answer any other questions other than preparing receipes."""

st.set_page_config(page_title="My Cook Book",page_icon="🌭",layout="centered")
st.title("🍲 Ask me a Receipe")
st.header(" Your Cookbook is ready")

conversation=ConversationChain(llm=Google_flash_model,memory=st.session_state.buffer_memory)
conversation.memory.chat_memory.add_message(SystemMessage(content=system_message))

if prompt:= st.chat_input(" Ask a Recipe?"):
    st.session_state.messages.append({"role":"user","content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != 'Assistant':
    with st.chat_message("Assistant"):
        with st.spinner("Preparing............"):
            response=conversation.predict(input=prompt)
            st.write(response)
            message={"role":"Assistant","content":response}
            st.session_state.messages.append(message)



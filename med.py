from dotenv import load_dotenv
load_dotenv() #load enviroment variable
import os
import google.generativeai as genai
import streamlit as st
#input
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])#chat initialization

def get_gemini_response(question):
    #Generates a response to the user's question using Gemini, Google's A
    response=chat.send_message(question,stream=True)#if true ,gives response in chunks
    return response

st.set_page_config(page_title="Health")
st.header("ROBODOC")
#if not in session,to store chat history
if 'chat_history' not in st.session_state:#session state is like cache memory
    st.session_state['chat_history'] = []

input=st.text_input("State your problem: ",key="input")
submit=st.button("Send")


input_prompt="""You are an expert in understanding general diseases as a Homeopathy doctor.We will ask questions regarding our health or symtoms and you will have to answer the question  by generaating the possible treatments one shall take with regards to medication or any other precaution."""



if input and submit:
    response=get_gemini_response(input)
                    #list                   #tuple
    st.session_state['chat_history'].append(("You",input))#to access the session state we use a list
    st.subheader("Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Response",chunk.text))
st.subheader("CHAT HISTORY:")
for role,response in st.session_state['chat_history']:
    st.write(f"{role}: {response}")#printing the response,UNpacking

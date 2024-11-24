from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai



load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to load geminipro model 

model = genai.GenerativeModel("gemini-pro")

chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the streamlit app

st.set_page_config(page_title="Mindsummit Chatbot")
st.header("MindSummit Chatbot")

# Initilize the session state for chat history if it doesn't exist

if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []


input = st.text_input("Input:", key = 'input')
submit = st.button("Ask your question")


if input and submit:
    response = get_gemini_response(input)
    
    # Add user query to session chat history
    st.session_state['chat_history'].append(("You", input))
    
    st.subheader("The response is")
    
    # Iterate over the response chunks and display them
    for chunk in response:
        st.write(chunk.text)
        # Add the response from the bot to the session chat history
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the chat history
st.subheader("The chat history is:")

# Iterate over the stored chat history and display it
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.write(f"**{role}:** {text}")
    else:
        st.write(f"*{role}:* {text}")


    
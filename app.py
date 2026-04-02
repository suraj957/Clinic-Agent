import streamlit as st
import requests

st.set_page_config(page_title="Clinic AI Assistant")

st.title("🏥 AI Clinic Assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        # API call
        response = requests.post(
            "http://127.0.0.1:8001/book",
            json={"message": user_input}
        )

        bot_reply = response.json()["response"]

    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    # Show bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
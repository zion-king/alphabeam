import streamlit as st
import requests

# Function to send user query to the Flask API
def send_query(user_query):
    api_url = "http://localhost:5000/api/query"  # Replace with your actual Flask API URL
    response = requests.post(api_url, json={"userQuery": user_query})
    if response.status_code == 200:
        return response.json().get("result", "Error processing request")
    else:
        return "Error communicating with the Flask API"

# Initialize session_state to store user messages
if 'user_messages' not in st.session_state:
    st.session_state.user_messages = []

# Streamlit app layout
def main():
    st.title("Chat System Interface")

    # User input
    user_input = st.text_input("Type your query:")

    # Send button
    if st.button("Send") and user_input:
        # Store user message in session_state
        st.session_state.user_messages.append(("You", user_input))

        # Display user message
        st.text(f"You: {user_input}")

        # Send user query to the Flask API
        bot_response = send_query(user_input)

        # Store bot response in session_state
        st.session_state.user_messages.append(("Bot", bot_response))

        # Display bot response
        st.text(f"Bot: {bot_response}")

    # Display chat history
    st.text("Chat History:")
    for sender, message in st.session_state.user_messages:
        st.text(f"{sender}: {message}")

if __name__ == "__main__":
    main()

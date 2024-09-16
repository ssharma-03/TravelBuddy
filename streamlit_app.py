import streamlit as st
from groq import Groq

# Retrieve the API key from Streamlit secrets
api_key = st.secrets.get("GROQ_API_KEY")

# Use a fallback method if the API key is missing
def chat(prompt):
    if api_key:
        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content
    else:
        return "API key is missing. Please set up the API key to use this feature."

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client with the API key
api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

def is_travel_related(question):
    """
    Checks if the question is related to travel or hospitality.
    """
    travel_keywords = ['hotel', 'flight', 'travel', 'booking', 'destination', 'trip', 'tour', 'vacation', 'resort', 'restaurant']
    return any(keyword in question.lower() for keyword in travel_keywords)

def chat(prompt):
    """
    Sends a prompt to the Groq API and returns the response.
    """
    try:
        # Make the API call
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )

        # Debugging: Print the type and structure of chat_completion
        print("Chat Completion Response:", chat_completion)
        print("Type of chat_completion:", type(chat_completion))

        # Extract choices from the response
        choices = chat_completion.choices if hasattr(chat_completion, 'choices') else []
        if choices:
            # Access the first choice and its message content
            first_choice = choices[0]
            message = first_choice.message if hasattr(first_choice, 'message') else {}
            message_content = message.content if hasattr(message, 'content') else 'No content available'
            return message_content
        return 'No response available'
    except Exception as e:
        return f"Error: {e}"

def main():
    # Set up the Streamlit page configuration
    st.set_page_config(page_title="TravelBuddy 🌍", layout="wide", initial_sidebar_state="expanded")

    # Apply custom styles to the Streamlit app
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #e0f7fa, #ffffff);  /* Light gradient background */
            color: #2c3e50;  /* Dark text color */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;  /* Modern font */
        }
        .stSidebar {
            background-color: #ffffff;  /* White sidebar background */
            box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);  /* Subtle shadow for sidebar */
        }
        .stButton > button {
            background-color: #3498db;  /* Blue button background */
            color: #ffffff;  /* White text color for buttons */
            border-radius: 12px;  /* Rounded button edges */
            padding: 10px 20px;  /* Padding for buttons */
            transition: background-color 0.3s ease, transform 0.3s ease;  /* Smooth transition for hover effect */
        }
        .stButton > button:hover {
            background-color: #2980b9;  /* Darker blue on hover */
            transform: scale(1.05);  /* Slightly larger button on hover */
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;  /* White background for text input */
            color: #2c3e50;  /* Dark text color for input */
            border-radius: 8px;  /* Rounded input edges */
            padding: 10px;  /* Padding for text input */
            border: 1px solid #dcdde1;  /* Border for input */
        }
        .stMarkdown {
            line-height: 1.6;  /* Improved readability */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("TravelBuddy 🌍")

    st.markdown("""
    ### 🌟 **Welcome to TravelBuddy!**  
    Your AI-powered assistant for travel planning and recommendations!  
    Ask questions about your travel plans, get suggestions, and more.
    """)

    st.sidebar.header("✈️ Travel Assistant")
    st.sidebar.markdown("""
    **How it works:**
    - Enter your travel-related questions or needs.
    - Receive instant suggestions and information.
    """)

    st.subheader("💬 Ask Your Travel Questions")
    question = st.text_input("Enter your question here:", key="question_input")

    if st.button("Get Answer"):
        if question:
            if is_travel_related(question):
                with st.spinner('Generating answer...'):
                    prompt = f"Act as a travel assistant and answer '{question}' based on general travel and hospitality knowledge."
                    response = chat(prompt)
                st.success("Answer Generated!")
                st.subheader("📬 Answer")
                st.write(response)
            else:
                st.error("Sorry, I can only assist with travel and hospitality-related questions.")
        else:
            st.error("Please enter a question")

if __name__ == "__main__":
    main()

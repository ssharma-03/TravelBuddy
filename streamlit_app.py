import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(
    api_key=os.getenv("Groq_API_KEY"),
)

def chat(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content
# Function to check if the question is travel-related
def is_travel_related(question):
    travel_keywords = ['hotel', 'flight', 'travel', 'booking', 'destination', 'trip', 'tour', 'vacation', 'resort', 'restaurant']
    return any(keyword in question.lower() for keyword in travel_keywords)

# Main Streamlit app logic
def main():
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

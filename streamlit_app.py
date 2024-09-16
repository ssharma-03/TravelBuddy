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

def chat(prompt):
    """
    Function to get the response from Groq API based on the user prompt.
    
    Parameters:
    - prompt (str): The question or statement to send to the API.
    
    Returns:
    - str: The response from the API.
    """
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192",
    )
    # Access the message content correctly
    return chat_completion.choices[0].message.content

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from the provided PDF file.
    
    Parameters:
    - pdf_file (BytesIO): PDF file uploaded by the user.
    
    Returns:
    - str: Extracted text content of the PDF.
    """
    import aspose.pdf as pdf
    input_pdf = pdf.Document(pdf_file)
    txt = pdf.text.TextAbsorber()
    txt.visit(input_pdf.pages[1])  # Extracting text from the second page
    return txt.text

def main():
    st.set_page_config(page_title="TravelBuddy 🤖", layout="wide", initial_sidebar_state="expanded")

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

    st.title("TravelBuddy 🤖")

    st.markdown(""" 
    ### 🌍 **Welcome to TravelBuddy**  
    Your AI-powered assistant for all travel and hospitality-related queries!  
    Upload your PDF, ask questions, and get instant answers tailored to your travel needs.
    """)

    st.sidebar.header("📄 Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        try:
            progress_bar = st.progress(0)
            
            for i in range(100):
                progress_bar.progress(i + 1)

            with st.spinner('Extracting text from the PDF...'):
                pdf_text = extract_text_from_pdf(uploaded_file)

            st.sidebar.success("PDF file uploaded successfully!")

            st.sidebar.subheader("📜 Extracted Text Preview")
            st.sidebar.text_area("Extracted Text", pdf_text[:500], height=200, key="extracted_text")

            st.subheader("💬 Ask Questions Based on PDF Content")
            question = st.text_input("Enter your question here:", key="question_input")

            if st.button("Get Answer"):
                if question:
                    with st.spinner('Generating answer...'):
                        prompt = f"Act as a travel assistant and answer the following question based on the data provided. Data: {pdf_text}. Question: {question}"
                        response = chat(prompt)
                    st.success("Answer Generated!")

                    st.subheader("📬 Answer")
                    st.write(response)
                else:
                    st.error("Please enter a question")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a PDF file on the sidebar.")

if __name__ == "__main__":
    main()

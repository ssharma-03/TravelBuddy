import os
from groq import Groq  # Replace with the actual import path if needed
from dotenv import load_dotenv


# Securely retrieve the API key from environment variables
load_dotenv()
totel = ("Enter Your questions:")

api_key = os.getenv('GROQ_API_KEY')  # Set your API key as an environment variable


client = Groq(api_key=api_key)

def chat(prompt):

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-70b-8192"  
    )
 
    return chat_completion.choices[0].message['content']

# Example usage
response = chat("Hi, can you suggest some travel destinations?")
print(response)

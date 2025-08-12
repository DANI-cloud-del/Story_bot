import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment variables from .env
load_dotenv()

# 2. Get the API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ No API key found. Make sure it’s in the .env file as GROQ_API_KEY=your_api_key_here")

# 3. Initialize Groq client
client = Groq(api_key=api_key)

# 4. Make a sample completion request
chat_completion = client.chat.completions.create(
    model="llama3-8b-8192",   # You can change model here
    messages=[
        {"role": "system", "content": "You are a creative storyteller."},
        {"role": "user", "content": "Write a short, peaceful fantasy story about a hero meeting a villain in a forest."}
    ],
    temperature=0.7,
    max_tokens=200
)

# 5. Print the AI's response
print("\n🌿 Generated Story:\n")
print(chat_completion.choices[0].message.content)

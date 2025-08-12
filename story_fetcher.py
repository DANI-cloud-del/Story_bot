# story_fetcher.py
import os
from dotenv import load_dotenv
from groq import Groq

def get_groq_story(prompt: str, max_tokens: int = 500, temperature: float = 0.7):
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ No GROQ_API_KEY in .env file")

    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a creative storyteller. End the story naturally."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )

    story_text = resp.choices[0].message.content
    # Split into non-empty lines
    return [{"narrator": line.strip()} for line in story_text.split('\n') if line.strip()]

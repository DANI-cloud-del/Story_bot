# story_fetcher.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

def get_groq_story(prompt: str, max_tokens: int = 500, temperature: float = 0.7):
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ No GROQ_API_KEY in .env file")

    system_prompt = """You are a creative storyteller and animation director. Generate:
1. A story with dialogue (format: [{"narrator": "text"}] or [{"character": "text"}])
2. Animation instructions (format: {"instructions": [{"character": "hero/villain", "action": "walk/idle/hurt", "duration": seconds}]})

Available actions: idle, walk, hurt
Available characters: hero, villain

Generate both story and instructions in this JSON format:
{
    "story": [{"narrator": "text"}],
    "instructions": [{"character": "hero", "action": "walk", "duration": 2}]
}"""

    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        response_format={"type": "json_object"}
    )

    try:
        response = json.loads(resp.choices[0].message.content)
        return response.get("story", []), response.get("instructions", [])
    except json.JSONDecodeError:
        return [{"narrator": "Story generation failed"}], []
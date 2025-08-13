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
1. A story with dialogue (format: {"speaker": "narrator/hero/villain", "text": "content"})
2. Animation instructions (format: {"character": "hero/villain", "action": "walk/idle/hurt", "duration": seconds})

Generate BOTH in this STRICT JSON format:
{
    "dialogue": [
        {"speaker": "narrator", "text": "The forest was quiet..."},
        {"speaker": "hero", "text": "Hello villain!"}
    ],
    "instructions": [
        {"character": "hero", "action": "walk", "duration": 2}
    ]
}"""

    client = Groq(api_key=api_key)
    try:
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

        response = json.loads(resp.choices[0].message.content)
        
        # Convert to your expected format
        story = []
        for line in response.get("dialogue", []):
            if line["speaker"] == "narrator":
                story.append({"narrator": line["text"]})
            else:
                story.append({line["speaker"]: line["text"]})
                
        return story, response.get("instructions", [])
        
    except Exception as e:
        print(f"Error generating story: {e}")
        # Fallback to simple story
        return [{"narrator": "Once upon a time in the forest..."}], []
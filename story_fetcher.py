# story_fetcher.py
import os
import json
import random
from dotenv import load_dotenv
from groq import Groq
from resource_bank import ResourceBank

def get_groq_story(prompt: str = None, max_tokens: int = 500, temperature: float = 0.7):
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("❌ No GROQ_API_KEY in .env file")

    if not prompt:
        scenarios = [
            "A tense confrontation in an ancient forest",
            "A peaceful meeting between rivals at sunset",
            "A magical duel in the heart of the woods"
        ]
        prompt = f"{random.choice(scenarios)}. Include dramatic dialogue and physical actions."

    system_prompt = """You are a storyteller and animation director. Generate:
1. Dialogue (format: {"speaker": "narrator/hero/villain", "text": "content"})
2. Animation instructions (format: {"character": "hero/villain", "action": "walk/idle/hurt", "direction": "left/right/up/down", "duration": seconds})
3. Music instructions (format: {"action": "play/stop", "track": "adventure/scifi"})

Return STRICT JSON format:
{
    "dialogue": [{"speaker": "narrator", "text": "The forest was quiet..."}],
    "instructions": [{"character": "hero", "action": "walk", "direction": "right", "duration": 2}],
    "music": [{"action": "play", "track": "adventure"}]
}

Rules:
- Actions must match dialogue
- Include approach/retreat movements
- Use 'hurt' during fights
- Each instruction should last 1-3 seconds
- Music tracks should match the scene mood"""
    
    client = Groq(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            response_format={"type": "json_object"}
        )

        response = json.loads(resp.choices[0].message.content)
        
        # Process dialogue
        story = []
        for line in response.get("dialogue", []):
            if line["speaker"] == "narrator":
                story.append({"narrator": line["text"]})
            else:
                story.append({line["speaker"]: line["text"]})
        
        # Process music instructions
        music_instructions = []
        valid_tracks = list(ResourceBank.MUSIC.keys()) if hasattr(ResourceBank, 'MUSIC') else []
        for cmd in response.get("music", []):
            action = cmd.get("action", "play").lower()
            if action not in ["play", "stop"]:
                continue
                
            track = cmd.get("track")
            if action == "play":
                if track not in valid_tracks and valid_tracks:  # Only choose random if we have valid tracks
                    track = random.choice(valid_tracks)
                elif not valid_tracks:
                    continue  # Skip if no valid tracks available
                    
            music_instructions.append({
                "action": action,
                "track": track if action == "play" else None
            })
        
        # Process animation instructions
        instructions = []
        valid_actions = ["walk", "idle", "hurt"]
        for cmd in response.get("instructions", []):
            if cmd.get("character") in ["hero", "villain"]:
                action = cmd.get("action", "idle").lower()
                if action not in valid_actions:
                    action = "idle"
                
                direction = None
                if action == "walk":
                    direction = cmd.get("direction", random.choice(["left", "right"]))
                    if direction not in ["left", "right", "up", "down"]:
                        direction = random.choice(["left", "right"])
                
                duration = max(0.5, min(float(cmd.get("duration", 1.5)), 3.0))
                
                instruction = {
                    "character": cmd["character"],
                    "action": action,
                    "duration": duration
                }
                if direction:
                    instruction["direction"] = direction
                
                instructions.append(instruction)
        
        return story, instructions, music_instructions
        
    except Exception as e:
        print(f"API Error: {e}")
        # Return default story with random music if available
        default_music = []
        try:
            if hasattr(ResourceBank, 'MUSIC') and ResourceBank.MUSIC:
                default_music = [{"action": "play", "track": random.choice(list(ResourceBank.MUSIC.keys()))}]
        except Exception as e:
            print(f"Error getting default music: {e}")
            
        return [
            {"narrator": "The hero stands ready in the mystical forest."},
            {"hero": "I can feel your dark presence!"},
            {"villain": "Then come find me, if you dare!"}
        ], [
            {"character": "hero", "action": "walk", "direction": "right", "duration": 2},
            {"character": "villain", "action": "walk", "direction": "left", "duration": 2}
        ], default_music
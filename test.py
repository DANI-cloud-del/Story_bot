# test_story_api.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

def test_story_api():
    """Test the story generation API with the same model and prompt format"""
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ No GROQ_API_KEY found in .env file")
        print("Please make sure your .env file contains: GROQ_API_KEY=your_actual_key_here")
        return False
    
    print("✅ API Key found")
    print(f"Key: {api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "Key too short!")
    
    # Use the exact same system prompt from your code
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
    
    # Use the same user prompt logic
    import random
    scenarios = [
        "A tense confrontation in an ancient forest",
        "A peaceful meeting between rivals at sunset",
        "A magical duel in the heart of the woods"
    ]
    prompt = f"{random.choice(scenarios)}. Include dramatic dialogue and physical actions."
    
    print(f"\n📝 Using prompt: {prompt}")
    print(f"🤖 Using model: llama3-8b-8192")
    
    try:
        # Initialize client with the same settings
        client = Groq(api_key=api_key)
        
        print("\n🔄 Making API request...")
        
        # Make the exact same API call as in your code
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        print("✅ API request successful!")
        
        # Parse the response exactly like your code does
        response_content = resp.choices[0].message.content
        print(f"\n📄 Raw response (first 200 chars):")
        print(response_content[:200] + "..." if len(response_content) > 200 else response_content)
        
        # Try to parse the JSON
        response = json.loads(response_content)
        
        print(f"\n🎭 Dialogue lines: {len(response.get('dialogue', []))}")
        print(f"🎬 Animation instructions: {len(response.get('instructions', []))}")
        print(f"🎵 Music instructions: {len(response.get('music', []))}")
        
        # Show sample dialogue
        print(f"\n💬 Sample dialogue:")
        for i, line in enumerate(response.get('dialogue', [])[:3]):  # Show first 3 lines
            print(f"  {i+1}. {line.get('speaker', 'unknown')}: {line.get('text', '')}")
        
        # Show animation instructions
        print(f"\n🎬 Animation instructions:")
        for i, cmd in enumerate(response.get('instructions', [])[:3]):  # Show first 3
            print(f"  {i+1}. {cmd}")
        
        # Show music instructions
        print(f"\n🎵 Music instructions:")
        for cmd in response.get('music', []):
            print(f"  - {cmd}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        print("This means the API returned invalid JSON format")
        return False
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        
        # Provide specific error information
        if hasattr(e, 'status_code'):
            print(f"Status code: {e.status_code}")
        if hasattr(e, 'response'):
            print(f"Response: {getattr(e, 'response', 'No response details')}")
        
        return False

def test_tts_api():
    """Test the TTS API functionality"""
    print("\n" + "="*50)
    print("Testing TTS API...")
    
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ No API key for TTS test")
        return False
    
    try:
        client = Groq(api_key=api_key)
        
        print("🔄 Testing TTS...")
        response = client.audio.speech.create(
            model="playai-tts",
            voice="Aaliyah-PlayAI",
            input="Test message for TTS functionality",
            response_format="wav"
        )
        
        print("✅ TTS API working!")
        print(f"Response size: {len(response.read())} bytes")
        return True
        
    except Exception as e:
        print(f"❌ TTS API failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Story Generation API")
    print("=" * 50)
    
    # Test story generation
    story_success = test_story_api()
    
    # Test TTS (optional)
    tts_success = test_tts_api()
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print(f"Story API: {'✅ PASS' if story_success else '❌ FAIL'}")
    print(f"TTS API: {'✅ PASS' if tts_success else '❌ FAIL'}")
    
    if story_success and tts_success:
        print("\n🎉 All tests passed! Your API should work in the main application.")
    else:
        print("\n🔧 Some tests failed. Check your API key and network connection.")
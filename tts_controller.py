# tts_controller.py
import os
import subprocess
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class TTSController:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Updated with valid voice names from the error message
        self.voice_map = {
            "hero": "Aaliyah-PlayAI",      # Female voice
            "villain": "Angelo-PlayAI",    # Male voice
            "narrator": "Atlas-PlayAI"     # Neutral voice
        }

    def speak_line(self, character, text):
        """Convert text to speech and play it immediately"""
        if character not in self.voice_map:
            character = "narrator"
            
        try:
            response = self.client.audio.speech.create(
                model="playai-tts",
                voice=self.voice_map[character],
                input=text,
                response_format="wav"
            )
            
            # Play the audio directly
            proc = subprocess.Popen(
                ["ffplay", "-autoexit", "-", "-nodisp"],
                stdin=subprocess.PIPE
            )
            proc.communicate(response.read())
        except Exception as e:
            print(f"TTS Error for {character}: {e}")
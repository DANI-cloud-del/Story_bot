# tts_controller.py
import os
import subprocess
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class TTSController:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.voice_map = {
            "hero": "Aaliyah-PlayAI",
            "villain": "Angelo-PlayAI",
            "narrator": "Atlas-PlayAI"
        }
        # Try different audio devices in order of likelihood
        self.audio_devices = ["default", "pulse", "alsa", "sdl", "openal"]

    def speak_line(self, character, text):
        if character not in self.voice_map:
            character = "narrator"
            
        try:
            response = self.client.audio.speech.create(
                model="playai-tts",
                voice=self.voice_map[character],
                input=text,
                response_format="wav"
            )
            
            audio_data = response.read()
            
            # First try without specifying audio device
            try:
                proc = subprocess.Popen(
                    ["ffplay", "-autoexit", "-nodisp", "-vn", "-nostats",
                     "-loglevel", "error", "-af", "volume=0.5", "-"],
                    stdin=subprocess.PIPE
                )
                proc.communicate(audio_data)
                return
            except Exception:
                pass
                
            # If that fails, try different audio devices
            for device in self.audio_devices:
                try:
                    proc = subprocess.Popen(
                        ["ffplay", "-autoexit", "-nodisp", "-vn", "-nostats",
                         "-loglevel", "error", "-af", "volume=0.5",
                         "-ao", device, "-"],
                        stdin=subprocess.PIPE
                    )
                    proc.communicate(audio_data)
                    break
                except Exception as e:
                    print(f"Failed to use audio device {device}: {e}")
                    continue
                    
        except Exception as e:
            print(f"TTS Error for {character}: {e}")
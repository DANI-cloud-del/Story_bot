import os
import subprocess
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

model = "playai-tts"
voice = "Fritz-PlayAI"
text = "Hello from Groq TTS, playing directly in the terminal"
response_format = "wav"

response = client.audio.speech.create(
    model=model,
    voice=voice,
    input=text,
    response_format=response_format
)

# Run ffplay with audio data from stdin
proc = subprocess.Popen(
    ["ffplay", "-autoexit", "-", "-nodisp"],
    stdin=subprocess.PIPE
)
proc.communicate(response.read())

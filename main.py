import vosk
import sounddevice as sd
import numpy as np
import json
import requests
from TTS.api import TTS
from api_key import get_api_key  # Import the function from your api_key module

# --- Vosk STT setup ---
model = vosk.Model("./vosk-model-small-en-us-0.15/")  # Replace with your Vosk model path
samplerate = 16000
device = 1  # You might need to change this depending on your audio setup

# --- Coqui TTS setup ---
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", gpu=False)  # Replace with your Coqui TTS model path

# --- Gemini API setup ---
gemini_api_url = "https://api.gemini.google.com/v1/completions"

def transcribe_speech():
  """Captures audio and transcribes it using Vosk."""
  with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16', channels=1) as rec:
    rec.start()
    while True:
      data = rec.read(4000)[0]
      if model.AcceptWaveform(data.tobytes()):
        result = json.loads(model.Result())
        if "text" in result:
          return result["text"]

def get_gemini_response(prompt, api_key): 
  """Sends the prompt to Gemini and returns the response."""
  headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
  }
  data = {
      "prompt": prompt,
      "model": "gemini-pro"  # Or the model you want to use
  }
  response = requests.post(gemini_api_url, headers=headers, json=data)
  response.raise_for_status()
  return response.json()["response"]

def speak_text(text):
  """Speaks the given text using Coqui TTS."""
  tts.tts_to_file(text=text, file_path="output.wav")
  # You may need to adjust the command below based on your setup
  os.system("aplay output.wav")  

if __name__ == "__main__":
    gemini_api_key = get_api_key()
    if gemini_api_key:
        while True:
            print("Listening...")
            text = transcribe_speech()
            print("You said:", text)
            logging.info(f"User: {text}")  # Log user input

            if text:
                gemini_response = get_gemini_response(text, gemini_api_key)
                print("Gemini says:", gemini_response)
                logging.info(f"Gemini: {gemini_response}")  # Log Gemini output
                speak_text(gemini_response)
    else:
        print("Error: Could not retrieve API key.")
        logging.error("Could not retrieve API key.")  # Log the error
import os
import subprocess
import time
from ollama import Client

# --- Start Ollama serve if not already running ---
def start_ollama():
    try:
        subprocess.Popen(['ollama', 'serve'])
        time.sleep(3)  # give it time to start
    except Exception as e:
        print(f"[Warning] Failed to start Ollama serve: {e}")

# --- Initialize model and client ---
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=OLLAMA_URL)

# --- Ensure model is pulled ---
def ensure_model(model_name: str):
    try:
        subprocess.run(['ollama', 'pull', model_name], check=True)
    except Exception as e:
        print(f"[Warning] Failed to pull model {model_name}: {e}")

# Call setup at import
start_ollama()
ensure_model(MODEL_NAME)

# --- Translation functions ---
def get_translation(text: str) -> str:
    """Translate text into English using the selected Ollama model."""
    system_prompt = (
        "You are a translation assistant. Translate any text written in another "
        "language into natural English. If the text is already in English, return "
        "it as is. Only return the translation text, nothing else."
    )

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return response.message.content.strip()

def get_language(text: str) -> str:
    """Detect the language name (in English) of a given text."""
    system_prompt = (
        "You are a language classifier. Detect the language of the input text "
        "and reply only with the English name of that language."
    )
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
    )
    return response.message.content.strip()

def translate_content(post: str) -> tuple[bool, str]:
    """
    Detect and translate text robustly.
    Returns (is_english: bool, translated_text: str)
    """
    try:
        detected_language = get_language(post).strip().lower()
        if not detected_language or "understand" in detected_language:
            raise ValueError("Invalid language detection response")

        if detected_language == "english":
            return True, post

        translation = get_translation(post).strip()
        if not translation or len(translation.split()) < 2:
            raise ValueError("Empty or malformed translation")

        return False, translation

    except Exception as e:
        print(f"[Warning] translate_content failed: {e}")
        return True, post

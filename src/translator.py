import os
import subprocess
import time
from ollama import Client

# --- Initialize model and client ---
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=OLLAMA_URL)

# Call setup at import

# --- Translation functions ---
def get_translation(text: str) -> str:
    """Translate text into English using the selected Ollama model."""

    context = """
    You are a translation assistant.
    Translate any text written in another language into natural English.
    If the text is already in English, return it as is.
    Do not include the original text or explanations,
    just reply with the translated sentence.

    Examples:
    INPUT: "Bonjour"
    OUTPUT: Hello

    INPUT: "Hola amigo!"
    OUTPUT: Hello friend!

    Now, translate the following input:
    """

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": text},
        ],
    )
    return response.message.content.strip()

def get_language(text: str) -> str:
    """Detect the language name (in English) of a given text."""
    context = """
    You are a language classifier.
    Detect the language of the input text and reply only with the English name of that language.

    Example:
    INPUT: Bonjour, je m'appelle Bob
    OUTPUT: French

    INPUT: Können Sie mir bitte helfen?
    OUTPUT: German

    INPUT: Hello, how are you?
    OUTPUT: English
    """
    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": context},
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

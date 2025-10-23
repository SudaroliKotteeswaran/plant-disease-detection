import pyttsx3
import subprocess
import platform
import os
from utils import load_json

_engine = None
_current_lang = 'en'

def _init_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # Optionally set voice properties here; voice selection for languages might need OS voices
        _engine.setProperty('rate', 140)
    return _engine

def set_language(lang_code='en'):
    global _current_lang
    _current_lang = lang_code

def speak(text, lang=None):
    lang = lang or _current_lang
    # Try pyttsx3 offline first
    try:
        engine = _init_engine()
        # for certain languages, voice might not be available in pyttsx3; fallback to espeak
        engine.say(text)
        engine.runAndWait()
        return
    except Exception as e:
        # fallback to espeak or festival if installed
        try:
            if platform.system() == "Linux":
                # mapping: hi -> hi, ta -> ta, mr -> mr (depends on system voices)
                cmd = ['espeak', '-v', lang, text]
                subprocess.run(cmd, check=False)
                return
        except Exception:
            pass
    # final fallback: print
    print("[TTS]", text)

import pdfplumber
from io import BytesIO
import os

def pdf_to_audio(text: list, 
                 out_name: str,
                 backend: str = 'gtts'): 
    
    if backend not in ['gtts', 'ttsx3']:
        raise TypeError("Please provide a valid argument for the backend argument.")
        return None
          
    if backend == 'gtts':
        from gtts import gTTS
        tts = gTTS(text="\n".join(text), lang='en')
        tts.save(out_name)
    elif backend == 'ttsx3':    
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file("\n".join(text) , out_name)
        engine.runAndWait()       
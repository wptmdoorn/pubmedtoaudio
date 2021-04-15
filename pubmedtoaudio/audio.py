import pdfplumber
from io import BytesIO
from gtts import gTTS
import os

def pdf_to_audio(text: list, out_name: str):       
    tts = gTTS(text="\n".join(text), lang='en')
    tts.save(out_name)     
    
    #import pyttsx3
    #engine = pyttsx3.init()
    #engine.save_to_file("\n".join(text) , out_name)
    #engine.runAndWait()       
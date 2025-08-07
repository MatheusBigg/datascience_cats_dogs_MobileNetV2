# Importa a biblioteca gTTS
from gtts import gTTS
import os
import playsound

def speak_text(text, lang, filename):
    print(f"Gerando áudio para: '{text}' no idioma {lang}")
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(filename)
    
    print(f"Reproduzindo áudio do arquivo: {filename}")
    playsound.playsound(filename)
    
    # Remover o arquivo de áudio após a reprodução
    os.remove(filename)

# --- Exemplo 1: Inglês ---
text_to_say_en = "How are you doing?"
language_en = "en"
filename_en = "english_audio.mp3"
speak_text(text_to_say_en, language_en, filename_en)

# --- Exemplo 2: Francês ---
text_to_say_fr = "Je vais au supermarché"
language_fr = "fr"
filename_fr = "french_audio.mp3"
speak_text(text_to_say_fr, language_fr, filename_fr)

# --- Exemplo 3: Português ---
text_to_say_br = "Vamos tomar caipirinha?"
language_br = "pt-br"
filename_br = "br_audio.mp3"
speak_text(text_to_say_br, language_br, filename_br)

# --- Exemplo 4: Chinês ---
text_to_say_chi = "我去超市"
language_chi = "zh"
filename_chi = "chinese_audio.mp3"
speak_text(text_to_say_chi, language_chi, filename_chi)
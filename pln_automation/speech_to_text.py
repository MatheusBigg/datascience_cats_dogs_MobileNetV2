#import section
import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import playsound
import pyaudio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#get mic audio
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone(device_index=4) as source:
        r.pause_threshold = 1
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio, language='pt-BR')
            print(said)
        except sr.UnknownValueError:
            speak("Foi mal, não entendi. Pode repetir?")
        except sr.RequestError:
            speak("Desculpe, serviço não está disponível.")
    return said.lower()

#speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='pt-br')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

def open_browser():
    return webdriver.Firefox()

def search_on_page(driver, url, keyword, search_element_by, search_element_value):
    driver.get(url)
    search_box = driver.find_element(search_element_by, search_element_value)
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

def get_wikipedia_summary(driver):
    try:
        first_paragraph_element = driver.find_element(By.TAG_NAME, "p")
        # Retorna o texto desse elemento
        return first_paragraph_element.text
    except Exception as e:
        print(f"Não foi possível encontrar o parágrafo. Erro: {e}")
        return "Não foi possível obter um resumo da Wikipedia."


#function to respond to commands
def respond(text):
    print("Texto do get_audio " + text)
    if 'youtube' in text:
        speak("O que você quer ver?")
        keyword = get_audio()
        if keyword!= '':
            driver = open_browser()
            url = f"https://www.youtube.com/"
            search_on_page(driver, url, keyword, By.NAME, "search_query")
            speak(f"A pesquisa no youtube por {keyword} esta pronta.")

    elif 'pesquisa' in text or 'procura' in text:
        speak("O que você quer pesquisar?")
        keyword = get_audio()
        if keyword !='':
            driver = open_browser()
            #Wikipedia search
            url_wiki = "https://pt.wikipedia.org/"
            search_on_page(driver, url_wiki, keyword, By.NAME, "search")
            speak(f"Abrindo a pesquisa por {keyword} na wikipedia.")
            summary = get_wikipedia_summary(keyword)
            if summary:
                speak("Eu encontrei um resumo para você.")
                speak(summary)
            else:
                speak("Desculpe, não consegui encontrar um resumo para isso no wikipedia.")
            
    elif 'ativar modo estudo' in text:
        speak("Ativando modo estudo!")
        driver = open_browser()
        os.system('gnome-terminal &')
        os.system('code &')
        speak("Ambiente ativado!")

    elif 'deastivar modo estudo' in text:
        speak("Desativando modo estudo!")
        driver.quit()
        os.system('pkill gnome-terminal')
        os.system('pkill code')
        speak("Ambiente desativado!")

    elif 'que horas são?' in text:
        strTime = datetime.today().strftime("%H:%M %p")
        print(strTime)
        speak(strTime)

    elif 'sair' in text or 'tchau' in text or 'falou' in text:
        speak("Falou mano, até mais!")
        try:
            driver.quit()
        except:
            pass
        exit()

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microfone {index}: {name}")
# breakpoint()

while True:
    print("Pode pá que estou ouvindo...")
    text = get_audio()
    respond(text)
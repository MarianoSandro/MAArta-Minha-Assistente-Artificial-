import speech_recognition as sr # recognise speech
import random
from datetime import datetime # get time details
import pytz 
import webbrowser # open browser
import yfinance as yf # to fetch financial data
import ssl
import certifi
import time
import bs4 as bs
import urllib.request
import os # to remove created audio files
import pyttsx3 #to play audio
import subprocess # to open programs

class pessoa:
    nome = 'Sandro'
    def setNome(self, nome):
        self.nome = nome

def there_exists(termos):
    for termo in termos:
        if termo in textoDito:
            return True

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
def gravarVoz(fala=False):
    with sr.Microphone() as source: # microphone as source
        if fala:
            speak(fala)
        r.adjust_for_ambient_noise(source) #it makes fast recognition, by reducing background nois
        audio = r.listen(source)  # listen for the audio via source
        textoDito = ''
        try:
            textoDito = r.recognize_google(audio, language='pt-BR')  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('Desculpe, não entendi')
        except sr.RequestError:
            speak('Desculpe, o serviço está fora do ar') # error: recognizer is not connected
        print(f">> {textoDito.lower()}") # print what user said
        return textoDito.lower()

# setting up sound engine, for fast response (reply)
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1)
    engine.setProperty('voices', voices[0].id)
except Exception as e:
    print(e)
    quit()

#playing output audio
def speak(audio_string):
    engine.say(audio_string)
    engine.runAndWait()

def respond(textoDito):
    # 1: greeting
    if there_exists(['oi','e aí','olá','fala','salve','saudações']):
        cumprimentos = [f"Olá, {pessoa_obj.nome}, como posso ajudá-lo?", f"E aí, {pessoa_obj.nome}, beleza?", f"Estou ouvindo {pessoa_obj.nome}", f"Posso ajudar, {pessoa_obj.nome}?", f"Oi, {pessoa_obj.nome}!"]
        cumprimento = cumprimentos[random.randint(0,len(cumprimentos)-1)]
        speak(cumprimento)

    # 2: nome
    if there_exists(["nome"]) and (there_exists(["qual"]) or there_exists(["diga"]) or there_exists(["fala", "fale"])):
        if pessoa_obj.nome:
            speak("meu nome é Marta")
        else:
            speak("my nome is Marta. what's your nome?")

    if there_exists(["my nome is"]):
        pessoa_nome = textoDito.split("is",1)[-1].strip()
        speak(f"okay, i will remember that {pessoa_nome}")
        pessoa_obj.setNome(pessoa_nome) # remember nome in pessoa object

    # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        speak(f"I'm very well, thanks for asking {pessoa_obj.nome}")

    # 4: time
    if there_exists(["horas","horário","hora"]):
        fusoBr =  pytz.timezone('Brazil/East')
        horario = datetime.now(fusoBr)
        hora = horario.strftime("%H")
        print(hora)
        if hora == "12":
            hora = 'meio dia'
        elif hora == "00":
            hora = "meia noite"
        minutos = horario.strftime("%M")
        time = f'Agora são {hora} e {minutos}'
        speak(time)

    # 5: pesquisar duckduckgo
    if there_exists(["pesquisar"]) and 'youtube' not in textoDito:
        pesquisar_termo = textoDito.split("for",1)[-1]
        url = f"https://duckduckgo.com/?q={pesquisar_termo}"
        webbrowser.get().open(url)
        speak(f'Here is what we found {pesquisar_termo} on duckduckgo')

    # 6: pesquisar youtube
    if there_exists(["youtube"]):
        pesquisar_termo = textoDito.split("youtube ",1)[-1]
        print(pesquisar_termo)
        url = f"https://www.youtube.com/results?search_query={pesquisar_termo}"
        webbrowser.get().open(url)
        speak(f'Here is what we found for {pesquisar_termo} on youtube')
        
    # 7: pesquisar spotify
    if there_exists(["ouvir", "música", "spotify", "toca"]):
        pesquisar_termo = textoDito.split(" ", 1)[-1]
        pesquisar_termo = ''.join(pesquisar_termo)
        url=f"https://open.spotify.com/search/{pesquisar_termo}"
        webbrowser.get().open(url)
        speak(f'Aqui está o que encontrei no Spotify')

    # 8: definition wikipedia
    if there_exists(["definição"]) or there_exists(["wikipedia"]):
        pesquisar_termo = textoDito.split("de", 1)[-1]
        url=f"https://en.wikipedia.org/wiki/{pesquisar_termo}"
        webbrowser.get().open(url)
        speak(f'Aqui está a página de {pesquisar_termo} na wikipédia')

    # 9: abrir programa
    if there_exists(["abrir", "programa", "aplicativo", "abre", "abra"]):
        pesquisar_termo = textoDito.split(" ")[-1]
        caminho = r"C:\Users\Sandro\Desktop"
        print(caminho + "/" +pesquisar_termo + ".lnk")
        subprocess.run(caminho + "/" +pesquisar_termo + ".lnk")
        speak(f'Abrindo {pesquisar_termo}')
        
    # 10: get stock price
    if there_exists(["preço do"]):
        pesquisar_termo = textoDito.lower().split(" do ")[-1].strip() #strip removes whitespace after/before a termo in string
        stocks = {
            "apple":"AAPL",
            "microsoft":"MSFT",
            "facebook":"FB",
            "tesla":"TSLA",
            "bitcoin":"BTC-USD"
        }
        try:
            stock = stocks[pesquisar_termo]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]

            speak(f'price of {pesquisar_termo} is {price} {stock.info["currency"]} {pessoa_obj.nome}')
        except:
            speak('oops, something went wrong')
    if there_exists(["exit", "quit", "goodbye"]):
        speak("going offline")
        exit()


time.sleep(1)

pessoa_obj = pessoa()
while(1):
    textoDito = gravarVoz() # get the voice input
    respond(textoDito) # respond



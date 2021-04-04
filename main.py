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
    nome = ''
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
            speak('')
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
        cumprimentos = [f"Olá, {pessoa_obj.nome}, como posso ajudá-lo?", f"Estou ouvindo {pessoa_obj.nome}", f"Posso ajudar, {pessoa_obj.nome}?", f"Oi, {pessoa_obj.nome}!"]
        cumprimento = cumprimentos[random.randint(0,len(cumprimentos)-1)]
        if pessoa_obj.nome:
            speak(cumprimento)
        else:
            speak("Olá, qual o seu nome?")

    # 2: nome
    if there_exists(["nome"]) and (there_exists(["qual"]) or there_exists(["diga"]) or there_exists(["fala", "fale"])):
        if pessoa_obj.nome:
            speak("Meu nome é Marta")
        else:
            speak("Meu nome é Marta. Qual o seu?")

    if there_exists(["meu nome é", "me chame de"]):
        pessoaNome = textoDito.split("é",1)[-1].strip()
        speak(f"Prazer em conhecê-lo, {pessoaNome}")
        pessoa_obj.setNome(pessoaNome) # remember nome in pessoa object

    # 3: saudações
    if there_exists(["tudo bem","como vai"]):
        speak(f"Estou funcionando bem, obrigado por perguntar!")

    # 4: agradecimento
    if there_exists(["obrigado", "valeu"]):
        agradecimentos = [f"Estou aqui para ajudar!", f"Por nada, {pessoa_obj.nome}!", f"Me chame se precisar de algo mais."]
        agradecimento = agradecimentos[random.randint(0,len(agradecimentos)-1)]
        speak(agradecimento)

    # 5: horário
    if there_exists(["horas","horário","hora"]):
        fusoBr =  pytz.timezone('Brazil/East')
        horario = datetime.now(fusoBr)
        hora = horario.strftime("%H")
        if hora[:1] == "0":
             hora = hora.replace('0', '', 1)
        if hora == "12":
            hora = 'meio dia'
        elif hora == "0":
            hora = "meia noite"
        elif hora == "1":
            hora = "uma"
        elif hora == "2":
            hora = "duas"
        minutos = horario.strftime("%M")
        minutos.replace('0', '', 1)
        time = f'Agora são {hora} e {minutos}'
        speak(time)
    
    # 6: pesquisar youtube
    if there_exists(["youtube", "vídeo"]):
        pesquisarTermo = textoDito.split("youtube ",1)[-1]
        pesquisarTermo = textoDito.split("vídeo ",1)[-1]
        print(pesquisarTermo)
        url = f"https://www.youtube.com/results?search_query={pesquisarTermo}"
        webbrowser.get().open(url)
        speak(f'Aqui está o que achamos no youtube')
        
    # 7: pesquisar spotify
    if there_exists(["ouvir", "música", "spotify", "toca"]):
        pesquisarTermo = textoDito.split(" ", 1)[-1]
        pesquisarTermo = ''.join(pesquisarTermo)
        url=f"https://open.spotify.com/search/{pesquisarTermo}"
        webbrowser.get().open(url)
        speak(f'Você pode ouvir no Spotify')

    # 8: definição wikipedia
    if there_exists(["definição", "wikipédia", "significado", "significa", "o que é", "o que são"]):
        pesquisarTermo = textoDito.split(" ")[-1]
        url=f"https://pt.wikipedia.org/wiki/{pesquisarTermo}"
        webbrowser.get().open(url)
        speak(f'Aqui está o {pesquisarTermo} na wikipédia')

    # 9: pesquisar duckduckgo
    if there_exists(["pesquisar", "pesquise", "pesquisa", "procure", "procura"]) and 'youtube' not in textoDito:
        pesquisarTermo = textoDito.split("aí ",1)[-1]
        url = f"https://duckduckgo.com/?q={pesquisarTermo}"
        webbrowser.get().open(url)
        speak(f'Pesquisando {pesquisarTermo} no duckduckgo')

    # 10: abrir programa
    if there_exists(["abrir", "programa", "aplicativo", "abre", "abra"]):
        pesquisarTermo = textoDito.split(" ")[-1]
        caminho = r"C:\Users\Sandro\Desktop"
        print(caminho + "/" +pesquisarTermo + ".lnk")
        subprocess.run(caminho + "/" +pesquisarTermo + ".lnk")
        speak(f'Abrindo {pesquisarTermo}')

    # 11: previsão do tempo
    if there_exists(["tempo"]):
        pesquisarTermo = textoDito.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        speak("Aqui estão alguns dados do google")
        
    # 12: preço de ações
    if there_exists(["preço do", "tá quanto o"]):
        pesquisarTermo = textoDito.lower().split(" o ")[-1].strip() #strip removes whitespace after/before a termo in string
        stocks = {
            "apple":"AAPL",
            "microsoft":"MSFT",
            "facebook":"FB",
            "tesla":"TSLA",
            "bitcoin":"BTC-USD"
        }
        try:
            stock = stocks[pesquisarTermo]
            stock = yf.Ticker(stock)
            price = stock.info["regularMarketPrice"]

            speak(f'O preço do {pesquisarTermo} está {price} {stock.info["currency"]} {pessoa_obj.nome}')
        except:
            speak('ops, algo deu errado')
    if there_exists(["fechar", "sair", "tchau"]):
        speak(f'Estou desligando, até mais, {pessoa_obj.nome}')
        exit()

    # 13: distância google maps
    if there_exists(["distância"]):
        pesquisarTermo1 = (textoDito.split("entre ",1)[-1]).split("e ",1)[0]
        pesquisarTermo2 = textoDito.split(" e ",1)[-1]
        url = f"https://www.google.com/maps/dir/{pesquisarTermo1}/{pesquisarTermo2}"
        webbrowser.get().open(url)
        speak(f'Vamos ver o que diz o google maps...')
    
    # mercado livre

    # alarme

    # tradução

    # wolfram alpha

    # noticias

    # tradutor
    

pessoa_obj = pessoa()
while(1):
    textoDito = gravarVoz() # get the voice input
    respond(textoDito) # respond



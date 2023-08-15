import pyttsx3
import speech_recognition as sr
import pyaudio              #to get microphone working in win
import wikipedia
import smtplib
from twilio.rest import Client
import requests
import webbrowser
import winshell
import pyjokes
import subprocess
from datetime import datetime
# VOSK speech recognition could be used to take different language up to 20

engine = pyttsx3.init()


#introduction to user
def intro(vo):
    if vo=="yes":
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)  # to change voice from male[0] to female[1]
    else:
        pass
    rate=engine.getProperty("rate")
    engine.setProperty("rate", 200)   # to change the speed or rate of speech
    speak("my name is Jack, Jack Sparrow")
    speak("I will we your Assistant Today")


# to get users name
def user_name():
    speak("May I know Your name:")
    user = take_command()

    if user=="None":
        speak(f"Its pleasure meeting you")
        return
    else:
        speak(f"Its pleasure meeting you{user}")
        return user


# Greet user
def wish_me():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning ")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon ")
    else:
        speak("Good Evening ")


# For creating a speaking function using Pyttsx3
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


#  Creating a Listening function using SpeechRecognition
def take_command():
    listner = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")     # speak on the listening
        vo = listner.listen(source)
    try:
        print("Recognizing....")        # wait for Google api to recognize
        comand = listner.recognize_google(vo)
        comand=comand.lower()
        print(f"User said :{comand}")

        return comand

    except Exception as e:
        print(e)
        print("Unable to get your voice")
        return " "


wish_me()
intro(vo="no")
u = user_name()  # u is username to be used further / or we could use environmental variable as well
speak(f"How Can i help You {u}")
while True:
    print("#########################################################################################################")
    curious = take_command().lower()
    if "wikipidia" in curious:
         info = curious.replace("wikipedia","")
         search = wikipedia.summary(info, 2)
         print("According to Wikipedia"+ search)
         speak("According to Wikipedia")
         speak(search)

    elif "weather" in curious or "temperature" in curious:
         speak("for what city?")
         lis = take_command().lower()
         city_name = lis
         try:
             api_key = #ur api key adress
             response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}")
             data = response.json()

             weather = data['weather'][0]['description']
             temp =data['main']['temp']

             speak(f"Weather{weather} and temprature {temp}")
             print(f"Your weather is {weather}\nYour Temperature is:{temp}")

         except requests.exceptions.ConnectionError:
             print("connection failure")
             pass

    elif "time" in curious :
         now = datetime.now()
         current_time = now.strftime("%H:%M:%S")
         speak("THe current time is :"+current_time)

    elif "email" in curious:
         new = ""  # password genrated from ur yahoo account
         with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
             connection.starttls()
             connection.login(user="00@yahoo.com", password=new)
             connection.sendmail(
                 from_addr="00@yahoo.com",  #  ur adress
                 to_addrs="00@yahoo.com",    # recivers adress
                 msg="hello nice to hear about ur new program"
             )
             speak("Your email is sent.")

    elif "message" in curious:
         account_sid="" #ur peraonal api key on twillio
         auth_token="" #ur token to access
         client=Client(account_sid,auth_token)
         meassage=client.messages.create\
                 (
                 body=take_command(), #message
                 from_="", #ur number
                 to=""  #reciver number
                )
         print("sent")

    elif "play song" in curious or "play music" in curious:
         webbrowser.open("spotify.com")

    elif "news" in curious:
         speak("opening news")
         webbrowser.open("timesofindia.indiatimes.com")

    elif "open google" in curious:
         speak("Here is google page")
         webbrowser.open("google.com")

    elif "youtube" in curious:
         speak("Here is youtube page")
         webbrowser.open("youtube.com")

    elif "stackoverflow" in curious:
         speak("Here is stackoverflow page")
         webbrowser.open("stackoverflow.com")

    elif "note" in curious or "add to notes" in curious:
        with open("notepad","w") as notepad:
            speak("opening notepad")
            k = input("would u like to add date and time:").lower()
            if "yes " in k or "sure" in k:
                time = datetime.now()
                time = time.strftime("%H:%M:%S")
                date = datetime.today().date()
                notepad.write(f"{time} / {date} :-")
            print("i am writing :")
            speaker = take_command().lower()
            print(speaker)
            notepad.write(speaker)
            speak(speaker)

    elif "remove item in notepad" in curious:
         with open("notepad","w") as notepad:
             speak("opening notepad")
             print(notepad)
             speaker=take_command().lower()
             if speaker in notepad:
                new= notepad.write(speaker.replace(speaker," "))
             else:
                 print("no match found")

    elif" empty recycle" in curious:
         speak("deleting all files in bin")
         all_deleted_files = list(winshell.recycle_bin())   # to delete all files in bin
         print(all_deleted_files)

    elif "sleep" in curious:
         speak("putting device to sleep in ")
         subprocess.call(["shutdown","/h"])

    elif "wish me" in curious:
         wish_me()

    elif "game" in curious:
         speak("I have exctly what u will like")
         webbrowser.open("cometh.io")
         speak("have fun")

    elif "Are you single"in curious or " do you have a gf" in curious or "do you have a bf " in curious:
         speak("I am single but not for u")

    elif "what is" in curious or "who is" in curious:
         info = curious.replace("what is ", " ")
         search = wikipedia.summary(info,2)
         speak(search)

    elif "thank you" in curious:
         speak("My pleasure")

    elif "switch off" in curious:
         speak("switching off")
         break

    elif "change voice" in curious:
         intro("yes")

    elif "joke" in curious:
         speak(pyjokes.get_joke())

    elif "change my name" in curious:
         user_name()

    else:
         print("not found")



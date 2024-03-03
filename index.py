
import os 
import discord
import getpass
import requests
import pyautogui
from gtts import gTTS 
from playsound import playsound
import time
from dotenv import load_dotenv
from threading import Thread

path1 = "C:/users/"
path2 = "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/update.exe"
path=(path1 + getpass.getuser() + path2)
print(str(path))

load_dotenv()
token = os.getenv("Ethan")
timeout = 1
connection = False
def wifi_check():
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        # Connection Success
        print('The internet connection is active')
        connection = True
    except requests.ConnectionError:
        # Connection Retry
        print("The internet connection is down")
        connection = False
        time.sleep(1)
        wifi_check()

wifi_check()

class MyClient(discord.Client):
    async def on_ready(self):
        #announce logon
        print(f'Logged on as {self.user}!') ,
    async def on_message(self, message):

        if f'{message.content}' == 'upd':
            os.startfile(str(path))
            quit()
        else:

            def Minimise():
                pyautogui.hotkey('win', 'd')
            def Playsound():
                #Play the notification and message contents
                message_content = (f'{message.content}')
                player = gTTS(text=message_content, lang='en', slow=False) 
                player.save("msg.mp3") 
                playsound('C:/announcer/incoming.mp3')
                playsound('msg.mp3')
                os.remove("msg.mp3")
            def Dialog_Box():
                message_content = (f'{message.content}')
                pyautogui.alert(message_content, str(message.author.id))
                pyautogui.hotkey('win', 'd')

            
            Minimise()
            t1 = Thread(target=Playsound)
            t2 = Thread(target=Dialog_Box)
            t1.start()
            t2.start()
            t1.join()
            t2.join()

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(str(token))
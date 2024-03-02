
import os 
import discord
import requests
from pyautogui import hotkey
from gtts import gTTS 
from playsound import playsound
import time

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
        def Minimise():
            hotkey('win', 'd')
        def Playsound():
            #Play the notification and message contents
            message_content = (f'{message.content}')
            player = gTTS(text=message_content, lang='en', slow=False) 
            player.save("msg.mp3") 
            playsound('C:/announcer/incoming.mp3')
            playsound('msg.mp3')
            os.remove("msg.mp3")
            hotkey('win', 'd')
        Minimise()
        Playsound()    
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTIxMzA4MDI4NTM2NTgwMTAyMA.GOIiO7.E3dk6vx6xcVwlUUVUjfqxRiLQd8MQODZPBKGQA')
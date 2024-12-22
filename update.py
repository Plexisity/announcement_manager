from urllib.request import urlretrieve
import os
import requests
import time
import discord
import asyncio
import dotenv

dotenv.load_dotenv()

timeout = 1
last_update_time = 0
connection = False
intents = discord.Intents.default()
client = discord.Client(intents=intents)
channel_id = 1319761582145798194  # Replace with your channel ID
token = os.getenv("Ethan")  # Replace with your token

def wifi_check():
    global connection
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        # Connection Success
        print('The internet connection is active')
        connection = True
    except requests.ConnectionError:
        # Connection Retry
        print("The internet connection is down, waiting for connection")
        connection = False
        time.sleep(1)
        wifi_check()

wifi_check()

async def send_message(channel, message):
    await channel.send(message)

def reporthook(block_num, block_size, total_size):
    global last_update_time
    downloaded = block_num * block_size
    progress = downloaded / total_size * 100
    current_time = time.time()
    
    if current_time - last_update_time >= 3:
        asyncio.run_coroutine_threadsafe(send_message(channel, f"Download progress: {progress:.2f}%"), client.loop)
        last_update_time = current_time



async def download_file(url, filename):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, urlretrieve, url, filename, reporthook)

@client.event
async def on_ready():
    global channel
    channel = client.get_channel(channel_id)
    if channel is None:
        print(f"Channel with ID {channel_id} not found.")
        await client.close()
        return

    print(f'Logged in as {client.user}')
    print(f'Found channel: {channel.name}')

    os.system("taskkill /f /im index.exe")
    url = "https://github.com/Plexisity/announcement_manager/raw/main/index.exe"
    filename = "index.exe"

    print("Starting download...")
    await channel.send("Starting download...")
    await download_file(url, filename)
    print("Download complete.")
    await channel.send("Download complete.")

    os.replace("index.exe", "C:/announcer/index.exe")
    os.startfile("C:/announcer/index.exe")
    await client.close()

client.run(token)
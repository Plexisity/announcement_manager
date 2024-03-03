from urllib.request import urlretrieve
import os
import requests
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
        print("The internet connection is down, waiting for connection")
        connection = False
        time.sleep(1)
        wifi_check()

wifi_check()

os.system("taskkill /f /im ethan.exe")
url = "https://github.com/Plexisity/announcement_manager/raw/main/ethan.exe"
filename = "ethan.exe"
file = urlretrieve(url, filename)
os.replace("ethan.exe", "C:/announcer/ethan.exe")
os.startfile("C:/announcer/ethan.exe")
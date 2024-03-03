from urllib.request import urlretrieve
import os
url = "https://github.com/Plexisity/announcement_manager/raw/main/index.exe"
filename = "index.exe"
file = urlretrieve(url, filename)
os.replace("index.exe", "C:/announcer/index.exe")
os.startfile("C:/announcer/index.exe")
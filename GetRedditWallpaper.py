import ctypes
import urllib.request
import json
import datetime 
import logging

SPI_SETDESKWALLPAPER = 20 

wallpapersFolder = "C:\\Users\\zimrh\\Documents\\Wallpapers\\"
loggingFile = wallpapersFolder + "details.log"
wallpapersRedditUrl = "https://www.reddit.com/r/wallpapers.json?limit=1"
redditHeaders = {"User-agent":"zimrhwallpaperbot0.1"}

# Initialize logging to console and file

log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
log.addHandler(handler)

handler = logging.FileHandler(loggingFile)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
log.addHandler(handler)

# Get started

log.info("Getting top wallpaper posts from reddit for last 24 hrs from " + wallpapersRedditUrl)

request = urllib.request.Request(wallpapersRedditUrl,headers=redditHeaders)

with urllib.request.urlopen(request) as response:
    data = json.loads(response.read().decode())

firstWallpaperPost = data["data"]["children"][0]

imageLink = firstWallpaperPost["data"]["url"]
downloadLocation = wallpapersFolder + imageLink.split("/")[-1]

log.info("Downloading " + imageLink + " to " + downloadLocation)

urllib.request.urlretrieve(imageLink, downloadLocation)

log.info("Downloaded to " + downloadLocation + " setting as wallpaper")

ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, downloadLocation, 0)

log.info("Wallpaper set")

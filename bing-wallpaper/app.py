import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path


HOME = Path.home()
FOLDER = ".local/share/bing-wallpaper/bg"
URL = "https://www.bing.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36"
}


if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

def get_wallpaper():
    page = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(page.content, "html.parser")
    url_image = f'{URL}{soup.find(id="preloadBg")["href"]}'

    image = requests.get(url_image, headers=HEADERS)

    if image.status_code == 200:
        today = datetime.today().strftime("%Y-%m-%d")
        wallpaper = f"{FOLDER}/{today}.jpg"
        with open(wallpaper, "wb") as f:
            f.write(image.content)
    return wallpaper


def remove_old_bg():
    files = [os.path.join(FOLDER, nome) for nome in os.listdir(FOLDER)]
    files.sort()
    remove = files[0:-5]
    for item in remove:
        os.remove(item)


def set_wallpaper(wallpaper):
    command = f"gsettings set org.gnome.desktop.background picture-uri file://{HOME}/{wallpaper}"
    os.system(command)


wallpaper = get_wallpaper()
set_wallpaper(wallpaper)
remove_old_bg()

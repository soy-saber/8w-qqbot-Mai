import requests
from bs4 import BeautifulSoup
def anime(message):
    title = message.split(" ")[-1]
    url = "https://www.agefans.net/search?query=" + title + "&page=1"
    response = requests.get(url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html,'html.parser')
    data = soup.select('#container > div:nth-child(3) > div > div:nth-child(1) > div > div:nth-child(1) > a')
    #目标动画的后缀url
    for item in data:
        link = item.get('href')
    dest = "https://www.agefans.net" + link
    return dest
from bs4 import BeautifulSoup as bs
import requests

author = "Wham"
title = "Last Christmas"
base="https://www.youtube.com/results?search_query="

query = ""
for word in author.split():
    query += word + "+"

query += "+".join(title.split())
print(query)

r = requests.get(base+query)
page=r.text
soup=bs(page,'html.parser')

vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})

videourl = 'https://www.youtube.com' + vids[0]['href']

print(videourl)


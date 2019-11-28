from urllib import request
from bs4 import BeautifulSoup

url = "https://www.metrolyrics.com/bohemian-rhapsody-lyrics-queen.html"
html = request.urlopen(url).read().decode('utf8')
parsed = BeautifulSoup(html, 'html.parser')

#content = parsed.find('div', attrs={'class':'js-lyric-text'})
song = parsed.find_all('p', attrs={'class': 'verse'})
song_text = ""
for verse in song:
    song_text += verse.text + "\n"
print(song_text)

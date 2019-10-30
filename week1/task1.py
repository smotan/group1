print("Viikon luetuimmat")

from urllib import request
from bs4 import BeautifulSoup

url = "https://www.hs.fi/uusi/"
html = request.urlopen(url).read().decode('utf8')

parsed = BeautifulSoup(html, 'html.parser')
luetuin_viikko = parsed.find('div', attrs={'class': 'content'})

print(luetuin_viikko)

print("Viikon luetuin")

from urllib import request
from bs4 import BeautifulSoup

url = "https://www.hs.fi/uusi/"
html = request.urlopen(url).read().decode('utf8')

parsed = BeautifulSoup(html, 'html.parser')
luetuimmat_viikko = parsed.find('ol', attrs={'class': 'is-most-read-articles-list tab-content', 'data-period':'week'})
luetuin_viikko = luetuimmat_viikko.find("div", attrs={'class':'content'})
luetuin = luetuin_viikko.text
print(luetuin)


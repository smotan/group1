print("Viikon luetuin")

from urllib import request
from bs4 import BeautifulSoup

url = "https://www.hs.fi/uusi/"
html = request.urlopen(url).read().decode('utf8')

# Try commenting what your code does.
parsed = BeautifulSoup(html, 'html.parser')
# For instance here you could say, that you look for html tag with the weekly most read articles
luetuimmat_viikko = parsed.find('ol', attrs={'class': 'is-most-read-articles-list tab-content', 'data-period':'week'})
luetuin_viikko = luetuimmat_viikko.find('div', attrs={'class':'content'})

luetuin = luetuin_viikko.find('p').text
print(luetuin)


from urllib import request
from bs4 import BeautifulSoup

url = "https://www.maxtv.com.au/top-1000-greatest-songs-of-all-time-3"
html = request.urlopen(url).read().decode('utf8')

data = []
parsed = BeautifulSoup(html, 'html.parser')
content = parsed.find('div', attrs={'class':'entry-content'})
table_body = content.find('tbody')
rows = table_body.find_all('tr')

for row in rows:
    cells = row.find_all('td')
    if len(cells) == 3:    
        song = cells[1].text
        author = cells[2].text
        print(song + " " + author)


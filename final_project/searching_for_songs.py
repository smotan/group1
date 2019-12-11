from urllib import request
from bs4 import BeautifulSoup
import re

def main():
    list_of_songs = []
    url = "https://www.maxtv.com.au/top-1000-greatest-songs-of-all-time-3"
    html = request.urlopen(url).read().decode('utf8')
    parsed = BeautifulSoup(html, 'html.parser')
    content = parsed.find('div', attrs={'class':'entry-content'})
    table_body = content.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 3:
            song = cells[1].text.lower()
            author = cells[0].text.lower()
            song = re.sub(" ", "-", song)
            author = cells[2].text.lower()
            author = re.sub(" ", "-", author)
            url = "https://www.metrolyrics.com/" + song + "-lyrics-" + author + ".html"
            song_text = find_song(url)
            if song_text != "":
                song = re.sub("-", " ", song).title()
                author = re.sub("-", " ", author).title()
                list_of_songs.append((author, song, song_text))
    #print(len(list_of_songs))
    #print(list_of_songs[0])
    write_to_a_file(list_of_songs)

def find_song(url):
    song_text = ""
    not_found = 0
    try:
        html = request.urlopen(url).read().decode('utf8')
        parsed = BeautifulSoup(html, 'html.parser')
        song = parsed.find_all('p', attrs={'class': 'verse'})
        for verse in song:
            song_text += verse.text + "\n"
    except:
        not_found += 1
    return song_text

def write_to_a_file(list_of_songs):
    try:
        my_file = open("songs_with_authors.txt", "w")
        for song in list_of_songs:
            my_file.write("Author: " + song[0] + "\nTitle: " + song[1] + "\nLyrics:\n" + song[2])
        my_file.close()
    except OSError:
        print("error")

main()

import re
from bs4 import BeautifulSoup as bs
import requests

def main():
    text_file = open("../data/songs_with_authors.txt", "r", encoding="utf8")
    file_text = text_file.read()
    list_of_songs = file_text.split("Author: ")
    list_of_songs = list(filter(None, list_of_songs))
    
    my_file = open("songs_with_authors_and_links.txt", "a")
    for song in list_of_songs:
        try:
            title = re.sub('.*Title:.(.*).Lyrics.*', r'\1', song[:100], flags=re.S)
            author = re.sub('(.*).Title.*', r'\1', song[:100], flags=re.S)
            text = re.sub(r'.*Lyrics:.(.*)', r'\1', song, flags=re.S)
            link = get_youtube_link(author, title)
            my_file.write("Author: " + author + "\nTitle: " + title + "\nLyrics:\n" + text + "Youtube: " + link + "\n")
        except TypeError:
            my_file.write("Author: " + author + "\nTitle: " + title + "\nLyrics:\n" + text + "Youtube: no video found\n")
            pass
    my_file.close()

def get_youtube_link(author, title):
    base="https://www.youtube.com/results?search_query="
    query = ""
    
    try:
        for word in author.split():
            query += word + "+"
        query += "+".join(title.split())

        r = requests.get(base+query)
        page=r.text
        soup=bs(page,'html.parser')

        vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})

        videourl = 'https://www.youtube.com' + vids[0]['href']
        return videourl
    except IndexError:
        pass

main()

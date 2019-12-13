from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
import pke
import ast
from string import digits 


def str2tuplelist(s):
    return eval( "[%s]" % s )

#Initialize Flask instance
app = Flask(__name__)

try:
    text_file = open("songs_with_authors.txt", "r", encoding="utf8")
    file_text = text_file.read()
    list_of_songs = file_text.split("Author: ")
    list_of_songs = list(filter(None, list_of_songs))
    theme_file = open("themes1.txt", "r")
    read_themes = theme_file.read()
    themes = read_themes.split("\n")
    list_of_themes = []
    for song_themes in themes:
        list_of_themes.append(str2tuplelist(song_themes))
    #songs_and_themes = dict(zip(list_of_themes, list_of_songs))
    #list_of_songs = list(songs_and_themes.values())
    #list_of_themes = list(songs_and_themes.keys())
except OSError:
    print("File not found")
          
def search_query(query, list_of_songs, list_version, list_of_themes):
    
    #query = re.sub(r'^"', '', query)
    #query = re.sub(r'"$', '', query)
    
    query = query.split()
    dict_of_matches = {}

    for i in range(len(list_of_themes)):
        song_themes_and_scores = list_of_themes[i]
        if song_themes_and_scores:
            for theme in song_themes_and_scores:
                if theme[0] in query:
                    if i in dict_of_matches:
                        #mega boost if second word found
                        dict_of_matches[i] += 3 * theme[1]
                    else:
                        dict_of_matches[i] = theme[1]

    list_of_matches = sorted(dict_of_matches, key=dict_of_matches.get, reverse=True)
    return list_of_matches
    

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []
    list_of_matches = []

    #If query exists (i.e. is not None)
    if query:
        #if not re.search("^\".+\"$", query):
         #   (query, list_version) = parse(query)
        #else:            
        list_version = list_of_songs
        list_of_matches = search_query(query, list_of_songs, list_version, list_of_themes)
        for idx in list_of_matches:
            doc = list_of_songs[idx]
            title = re.sub('.*Title:.(.*).Lyrics.*', r'\1', doc[:100], flags=re.S)
            author = re.sub('(.*).Title.*', r'\1', doc[:100], flags=re.S)
            text = re.sub(r'.*Lyrics:.(.*)', r'\1', doc, flags=re.S)
            text = text.replace('\n', '<br>')
            themes = ""
            for theme in list_of_themes[idx]:
                themes += " "
                themes += str(theme[0])
            matches.append({'author':author, 'title':title,'sisalto':text, 'themes':themes})


    #Render index.html with matches variable
    return render_template('index.html', matches=matches)


from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
import pke
import ast
from string import digits 
import random
from sklearn.feature_extraction.text import CountVectorizer

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
    #WE WANT to have list of songs as list of triples (author, title, song)!!!!!!!!!!!!!!

except OSError:
    print("File not found")


def search_more_words(query):
    list_of_idx = []
    for i in range(len(list_of_themes)):
        song_themes_and_scores = list_of_themes[i]
        if song_themes_and_scores:
            for theme in song_themes_and_scores:
                if theme[0] == query:
                    list_of_idx.append(i)
    return list_of_idx

def literal_search(query):
    list_of_idx = []
    for i in range(len(list_of_songs)):
        if query in list_of_songs[i].lower():
            list_of_idx.append(i)
    return list_of_idx

def search_query(query):

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

#Gets random themes to show on the website
def find_random(list_of_themes):
    list_of_themes = str(list_of_themes)
    remove_digits = str.maketrans('', '', digits)
    res = list_of_themes.translate(remove_digits)
    res = re.sub("\[", "", res)
    res = re.sub("\(\'", "", res)
    res = re.sub("\'\,", ",", res)
    res = re.sub("\.\)", "", res)
    res = re.sub(" ,", "", res)
    res = re.sub("]", "", res)
    list_of_themes = res.split(",")
    num_to_select = 10                           # set the number to select here.
    list_of_random_items = random.sample(list_of_themes, num_to_select)
    return(list_of_random_items)

def rewrite_token(t, td_matrix, t2i):
    d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 


def rewrite_query(themes_query, td_matrix, t2i): # rewrite every token in the query
    return " ".join(rewrite_token(t, td_matrix, t2i) for t in themes_query.split())


def search_themes(themes_query, list_of_themes, list_of_songs):
    list_of_art = []
    remove_digits = str.maketrans('', '', digits)
    res = list_of_themes.translate(remove_digits)
    themes = str(list_of_themes)

    try:
        cv = CountVectorizer(lowercase=True, binary=True)
        sparse_matrix = cv.fit_transform(themes)
        td_matrix = sparse_matrix.todense().T
        t2i = cv.vocabulary_

        hits_matrix = eval(rewrite_query(themes_query, td_matrix, t2i))
        hits_list = list(hits_matrix.nonzero()[1])
        for doc_idx in hits_list:
           #index = list_of_themes.index(list_of_themes[doc_idx])
           list_of_art.append({'sisalto':list_of_songs[doc_idx]})
        return list_of_art
    except ValueError:
        pass

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')
    themes_query = request.args.get('themes_query')
    random_themes = []
    random_themes = find_random(list_of_themes)
    #Initialize list of matches
    boolean_matches = []
    matches = []
    list_of_matches = []

    #If query exists (i.e. is not None) and user searches for words in the text
    if query:
        #if not re.search("^\".+\"$", query):
        #    (query, list_version) = parse(query)
        #else:
        query = query.lower()
        list_of_matches = literal_search(query)
        if len(query.split()) > 1:
            list_idx = search_more_words(query)
            for idx in list_idx:
                if idx not in list_of_matches:
                    list_of_matches.append(idx)
        list_idx = search_query(query)
        for idx in list_idx:
                if idx not in list_of_matches:
                    list_of_matches.append(idx)
     
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

    #If user searches themes
    elif themes_query:
        matches = search_themes(themes_query, list_of_themes, list_of_songs)

    #Render index.html with matches variable
    return render_template('index.html', matches=matches, random_themes=random_themes)


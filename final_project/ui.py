#This is the actual search tool
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
from bs4 import BeautifulSoup as bs
import requests

def str2tuplelist(s):
    return eval( "[%s]" % s )

#Initialize Flask instance
app = Flask(__name__)

try:
    text_file = open("data/songs_with_authors.txt", "r", encoding="utf8")
    file_text = text_file.read()
    list_of_songs = file_text.split("Author: ")
    list_of_songs = list(filter(None, list_of_songs))
    theme_file = open("data/themes1.txt", "r")
    read_themes = theme_file.read()

    # themes is a list of strings in the format (theme, score) - up to ten themes for each song, seperated with ", "
    themes = read_themes.split("\n")
    list_of_themes = []

    # making a list of lists of tuples from a list of strings
    for song_themes in themes:
        list_of_themes.append(str2tuplelist(song_themes))

except OSError:
    print("File not found")

# searching more words as a theme - if a search contains more than one word, 
# firstly we search for them as one theme, then seperately as mor than one theme
def search_more_words_as_a_theme(query):
    list_of_idx = []
    for i in range(len(list_of_themes)):
        song_themes_and_scores = list_of_themes[i]
        if song_themes_and_scores:
            for theme in song_themes_and_scores:
                if theme[0] == query:
                    list_of_idx.append(i)
    return list_of_idx

# literal search
def literal_search(query):
    list_of_idx = []
    for i in range(len(list_of_songs)):
        if query in list_of_songs[i].lower():
            list_of_idx.append(i)
    return list_of_idx


# searching for a query consisting of one or more themes
def search_theme(query):
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

# gets random themes to show on the website
def find_random():
    all_themes = []
    for song_themes_and_scores in list_of_themes:
        for theme in song_themes_and_scores:
            all_themes.append(theme[0])
    num_to_select = 10  # set the number to select here.
    list_of_random_items = random.sample(all_themes, num_to_select)
    
    return(list_of_random_items)

def rewrite_token(t, td_matrix, t2i):
    d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 

# not theme ei toimi
# sen pitää olla and not ni toimii
# mutta pelkkä not love esim.
# aivan 
# nyt ei teemahaku löydä mitää jos hakee christmas, enkä tiiä miks, esim christmas and gravy taas löytyy ja noi boolean operaattorit ei toimi enää ollenkaan
# nyt teemoissa ei ole sitä christmas enää, voi vielä kokeilla toista metodia siihen themes extractioniin
# minne se christmas sit hävis? meijän pitäis varmaa päättää et käytetäänkö tota booleania vai ei. En enää oo varma et miten tää meijän haku toimii ni en oikei tiiä mitä tehä
# se themes.py jotenkin ei enää löytänyt sitä
# lisäsin sen boolean search jos joku niistä sanoista on haussa
# siis miun mielestä kun mie tein tota booleania ni varmasti löyty christmas, koska kokeilin sillä et tuleeko eri tulokset eri hauista
# miusta tuntuu että se christmas teema on vaihtunu christmas day teemaks jostain syystä jossain vaiheessa
# tää ei oo täydellinen mitenkää, mut haluutko sie vielä tehä tälle jotain? mie en enää jaksa keksii mitä tehä mut jos siulla on jotain ehdotuksia ni voin auttaa
# pitää sit päättää et missä vaiheessa jompi kumpi poistaa nää keskustelut täältä :D
# joo, se on nyt christmass day jostain syystä. yritin tehä uudestaan sen themes extractionin mut ei myös tule pelkkä christmas
# ei enää tule mieleen mitä voisi vielä tehdä, ehkä jo riittää?
# nyt sain youtube linkit toimimaan, mut se sitten toimii tosi hitaasti

def rewrite_query(themes_query, td_matrix, t2i): # rewrite every token in the query
    return " ".join(rewrite_token(t, td_matrix, t2i) for t in themes_query.split())

# Searches for matches in the list of themes; boolean search
def boolean_search_themes(themes_query):
    list_of_art = []

    try:
        cv = CountVectorizer(lowercase=True, binary=True)
        sparse_matrix = cv.fit_transform(themes)
        td_matrix = sparse_matrix.todense().T
        t2i = cv.vocabulary_

        hits_matrix = eval(rewrite_query(themes_query, td_matrix, t2i))
        hits_list = list(hits_matrix.nonzero()[1])
        return hits_list

    except ValueError:
        pass

    except KeyError:
        matches = []
        return matches

def get_youtube_link(author, title):
    base="https://www.youtube.com/results?search_query="
    query = ""
    
    for word in author.split():
        query += word + "+"
    query += "+".join(title.split())

    r = requests.get(base+query)
    page=r.text
    soup=bs(page,'html.parser')

    vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})

    videourl = 'https://www.youtube.com' + vids[0]['href']
    return videourl

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')
    themes_query = request.args.get('themes_query')
    random_themes = []
    random_themes = find_random()
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
     
        for idx in list_of_matches:
            doc = list_of_songs[idx]
            title = re.sub('.*Title:.(.*).Lyrics.*', r'\1', doc[:100], flags=re.S)
            author = re.sub('(.*).Title.*', r'\1', doc[:100], flags=re.S)
            text = re.sub(r'.*Lyrics:.(.*)', r'\1', doc, flags=re.S)
            text = text.replace('\n', '<br>')
            themes = ""
            for themes_and_scores in list_of_themes[idx]:
                themes += themes_and_scores[0] + " "
            link = get_youtube_link(author, title)
            matches.append({'author':author, 'title':title,'sisalto':text, 'themes':themes, 'link':link})

    #If user searches for matches in the list of themes
    elif themes_query:
        if (" not " or " NOT " or " or " or " OR " or " and " or "AND ") in themes_query:
            list_of_matches = boolean_search_themes(themes_query)
        else:
            list_of_matches = search_more_words_as_a_theme(themes_query)
            for result in search_theme(themes_query):
                if result not in list_of_matches:
                    list_of_matches.append(result)
        for idx in list_of_matches:
            doc = list_of_songs[idx]
            title = re.sub('.*Title:.(.*).Lyrics.*', r'\1', doc[:100], flags=re.S)
            author = re.sub('(.*).Title.*', r'\1', doc[:100], flags=re.S)
            text = re.sub(r'.*Lyrics:.(.*)', r'\1', doc, flags=re.S)
            text = text.replace('\n', '<br>')
            themes = ""
            for themes_and_scores in list_of_themes[idx]:
                themes += themes_and_scores[0] + " "
            link = get_youtube_link(author, title)
            matches.append({'author':author, 'title':title,'sisalto':text, 'themes':themes, 'link':link})


    #Render index.html with matches variable
    return render_template('index.html', matches=matches, random_themes=random_themes)


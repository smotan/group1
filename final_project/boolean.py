from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, render_template, request
import numpy as np
import re
from nltk.stem import LancasterStemmer
import pke
from string import digits 
import random


#Initialize Flask instance
app = Flask(__name__)
songs = []

try:
    text_file = open("songs.txt", "r")
    file_text = text_file.read()
    list_of_songs = file_text.split("Title: ")
    list_of_songs =list(filter(None, list_of_songs))
    theme_file = open("themes1.txt", "r")
    read_themes = theme_file.read()
    remove_digits = str.maketrans('', '', digits)
    res = read_themes.translate(remove_digits)
    res = re.sub("\[", "", res)
    res = re.sub("\(\'", "", res)
    res = re.sub("\'\,", ",", res)
    res = re.sub("\.\)", "", res)
    res = re.sub(" ,", "", res)
    list_of_themes = res.split("], ")
except OSError:
    print("File not found")

def rewrite_token(t, td_matrix, t2i):
    d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 

def rewrite_query(query, td_matrix, t2i): # rewrite every token in the query
    return " ".join(rewrite_token(t, td_matrix, t2i) for t in query.split())

@app.route('/search')
def search():

    query = request.args.get('query')

    matches = []

    if query:
        matches = search_query(query, list_of_themes, list_of_songs)
    return render_template('index.html', matches=matches)

def search_query(query, list_of_themes, list_of_songs):
    list_of_art = []
    try:
        cv = CountVectorizer(lowercase=True, binary=True)
        sparse_matrix = cv.fit_transform(list_of_themes)
        td_matrix = sparse_matrix.todense().T
        t2i = cv.vocabulary_

        hits_matrix = eval(rewrite_query(query, td_matrix, t2i))
        hits_list = list(hits_matrix.nonzero()[1])
        for doc_idx in hits_list:
           index =list_of_themes.index(list_of_themes[doc_idx])
           list_of_art.append({'sisalto':list_of_songs[index]})
        return list_of_art

    except ValueError:
       print("No results")


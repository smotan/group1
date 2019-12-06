from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
import pke

#Initialize Flask instance
app = Flask(__name__)
songs = []

try:
    text_file = open("songs.txt", "r")
    file_text = text_file.read()
    list_of_songs = file_text.split("Title")
    theme_file = open("themes.txt", "r")
    read_themes = theme_file.read()
    list_of_themes = read_themes.split(", ")
except OSError:
    print("File not found")

def parse(query, list_of_songs):
    porter = LancasterStemmer()
    query = porter.stem(query)
    stem_list_of_songs = []
    results2 = [line.split() for line in list_of_songs]
    results2 = [ x for x in results2 if x != []]
    for i in range(0, len(results2)):
        l1 = results2[i]
        l2 = ' '.join([porter.stem(word) for word in l1])
        stem_list_of_songs.append(l2)    
    return (query, stem_list_of_songs)
          
def search_query(query, list_of_songs, list_version):
    query = re.sub(r'^"', '', query)
    query = re.sub(r'"$', '', query)
    
    list_of_art = []
    try:        
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        sparse_matrix = tfv.fit_transform(list_version).T.tocsr()
        query_vec = tfv.transform([query]).tocsc()        
        hits = np.dot(query_vec, sparse_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        articles = 0
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            article = list_of_songs[doc_idx]
            query = ' ' + query
            doc = article[article.find(query)-100:article.find(query)+100]
            if not doc:
                doc = article[article.find(query):article.find(query)+200]
            articles += 1
            article_name = re.sub(r'\n?<article name="(.*)?">\n.*', r'\1', article[:100])
            list_of_art.append({'name':article_name, 'sisalto':doc})
    except IndexError:
        print("No results")
    return list_of_art


#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        if not re.search("^\".+\"$", query):
            (query, list_version) = parse(query, list_of_songs)
        else:            
            list_version = list_of_songs
        matches = search_query(query, list_of_songs, list_version)


    #Render index.html with matches variable
    return render_template('index.html', matches=matches)

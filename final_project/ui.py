from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
import pke
from string import digits 

#Initialize Flask instance
app = Flask(__name__)
songs = []

try:
    text_file = open("songs_with_authors.txt", "r")
    file_text = text_file.read()
    list_of_songs = file_text.split("Author: ")
    list_of_songs = list(filter(None, list_of_songs))
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
    songs_and_themes = dict(zip(list_of_themes, list_of_songs))
    list_of_songs = list(songs_and_themes.values())
    list_of_themes = list(songs_and_themes.keys())
except OSError:
    print("File not found")

def parse(query, list_of_themes):
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
          
def search_query(query, list_of_songs, list_version, list_of_themes):
    query = re.sub(r'^"', '', query)
    query = re.sub(r'"$', '', query)
    
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=query, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=10)
    list_of_matches = []

    for query in keyphrases:
        try:        
            tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
            sparse_matrix = tfv.fit_transform(list_version).T.tocsr()
            query_vec = tfv.transform([query[0]]).tocsc()       
            hits = np.dot(query_vec, sparse_matrix)
            #Index error if no hits
            ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

            for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
                article = list_of_themes[doc_idx]
                doc = list_of_songs[doc_idx]
                list_of_matches.append(doc)
                #list_of_matches.append({'sisalto':doc})
        except IndexError:
            continue
    return list_of_matches

def sort_matches(list_of_matches):
    sorted_list = []
    final_list = []
    sorted_list = sorted(list_of_matches, key = list_of_matches.count, reverse = True)
    for song in sorted_list:
        if song not in final_list:
            final_list.append(song)
    return final_list

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
        if not re.search("^\".+\"$", query):
            (query, list_version) = parse(query, list_of_songs)
        else:            
            list_version = list_of_themes
        list_of_matches = search_query(query, list_of_songs, list_version, list_of_themes)
        for doc in sort_matches(list_of_matches):
            title = re.sub('.*Title: (.*)(?= Lyrics).*', r'\1', doc[:100])
            author = re.sub('(.*)(?= Title).*', r'\1', doc[:100])
            text = re.sub('.*(?<=Lyrics: )(.*)', r'\1', doc)
            matches.append({'author':author, 'title':title,'sisalto':text})


    #Render index.html with matches variable
    return render_template('index.html', matches=matches)

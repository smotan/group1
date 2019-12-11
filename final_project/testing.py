from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
import pke
from string import digits 

def search_query(query, list_of_songs, list_version, list_of_themes):
    query = re.sub(r'^"', '', query)
    query = re.sub(r'"$', '', query)
    
    query_themes = []
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=query, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    keyphrases = extractor.get_n_best(n=10)

    for query in keyphrases:
        try:        
            tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
            sparse_matrix = tfv.fit_transform(list_version).T.tocsr()
            query_vec = tfv.transform([query[0]]).tocsc()        
            hits = np.dot(query_vec, sparse_matrix)
            #error if no hits
            ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
            articles = 0
            for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
                article = list_of_themes[doc_idx]
                doc = list_of_songs[doc_idx]
                articles += 1
                #print(doc)
        except IndexError:
            print("No results")
            continue


try:
    text_file = open("songs.txt", "r")
    file_text = text_file.read()
    list_of_songs = file_text.split("Title: ")
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
    query = input("Query: ")
    search_query(query, list_of_songs, list_of_songs, list_of_themes)
except IndexError:
    print("index error")

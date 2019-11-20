from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer

#Initialize Flask instance
app = Flask(__name__)

example_data = [{'name':'anna'}]

try:
    text_file = open("enwiki.txt", "r")
    file_text = text_file.read()
    list_of_articles = file_text.split("</article>")
    for article in list_of_articles:
        example_data.append({'name': article})
except OSError:
    print("File not found")


def search_query(query, list_of_articles, list_version):
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
            article = list_of_articles[doc_idx]
            doc = article[article.find(query)-100:article.find(query)+100]
            articles += 1
            article_name = re.sub(r'\n?<article name="(.*)?">\n.*', r'\1', article[:100])
            list_of_art.append({'name':article_name})
    except IndexError:
        print("No results")
    return list_of_art

matches = []
matches = search_query("natural", list_of_articles, list_of_articles)
print(len(matches))

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        #Look at each entry in the example data
        matches = search_query(query, list_of_articles, list_of_articles)


    #Render index.html with matches variable
    return render_template('index.html', matches=matches)


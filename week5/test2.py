from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
import matplotlib.pyplot as plt
import matplotlib as mlp
import re
import nltk
import os
import numpy as np
import re
from pathlib import Path
import pke
from decimal import Decimal

#Initialize Flask instance
app = Flask(__name__)
example_data = []

try:
    text_file = open("enwiki.txt", "r")
    file_text = text_file.read()
    list_of_articles = file_text.split("</article>")
    for article in list_of_articles:
        example_data.append({'name': article})
except OSError:
    print("File not found")

def parse(query, list_of_articles):
    porter = LancasterStemmer()
    query = porter.stem(query)
    stem_list_of_articles = []
    results2 = [line.split() for line in list_of_articles]
    results2 = [ x for x in results2 if x != []]
    for i in range(0, len(results2)):
        l1 = results2[i]
        l2 = ' '.join([porter.stem(word) for word in l1])
        stem_list_of_articles.append(l2)    
    return (query, stem_list_of_articles)    
          
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
            query = ' ' + query
            doc = article[article.find(query)-100:article.find(query)+100]
            if not doc:
                doc = article[article.find(query):article.find(query)+200]
            articles += 1
            article_name = re.sub(r'\n?<article name="(.*)?">\n.*', r'\1', article[:100])
            generate_individual_plots(query, article_name, article)
            list_of_art.append({'name':article_name, 'sisalto':doc, 'pltpath':article_name+'_plt.png'})
    except IndexError:
        print("No results")
    return list_of_art


def generate_individual_plots(query, article_name, article):
    # YOUR code here:
    sisalto = ''.join(article)
    article_name = ''.join(article_name)
    try:
        extractor = pke.unsupervised.TopicRank()
        extractor.load_document(input=sisalto[0:1000], language='en')
        extractor.candidate_selection()
        extractor.candidate_weighting()
        keyphrases = extractor.get_n_best(n=3)
        names = []
        values = []
        for keyphrase in keyphrases:
            names.append(keyphrase[0])
            values.append(str(keyphrase[1]))
        plt.figure()
        values = list(map(float, values))
        plt.bar(names, values)
        plt.title('Themes in the article')
    except ValueError: #Pass if there are no themes in the text
        pass
    plt.savefig('static/'+article_name+'_plt.png')

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():

    #Get query from URL variable
    query = request.args.get('query')
    os.system('rm -f static/*_plt.png')
    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        if not re.search("^\".+\"$", query):
            (query, list_version) = parse(query, list_of_articles)
        else:            
            list_version = list_of_articles
        matches = search_query(query, list_of_articles, list_version)


    #Render index.html with matches variable
    return render_template('index.html', matches=matches)

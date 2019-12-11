from flask import Flask, render_template, request
from bs4 import BeautifulSoup 
import matplotlib.pyplot as plt
import matplotlib as mlp
import re
import nltk
import os
import numpy as np
import re
from nltk.stem import LancasterStemmer
from pathlib import Path
import pke
import time
from decimal import Decimal
from sklearn.feature_extraction.text import TfidfVectorizer

mlp.use('Agg')
# Load the file with the wiki articles
try:
    text_file = "enwiki.txt"
    with open(text_file,'r') as f:
        soup = BeautifulSoup(f,'lxml')
#generate a dictinoary with the entries and the content for each article
    dict_of_articles = {art['name']:art.text for art in soup.find_all('article') }
    list_of_articles = list(dict_of_articles.values())
except OSError:
    print("File not found")

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def extract_pieces(query,content):
    start_indexes = [m.start() for m in re.finditer(query,content.lower())]
    pieces=[]
    for i in start_indexes: 
        index1=content[max(i-15,0):i].find('\n')+1
        index2=content[i:i+100].find('\n')
        pieces.append('...'+content[max(0,i-15+index1):i+100-(100-index2)*(index2>0)]+'...')
        #print(i, content[i-15+index1:i+100-(100-index2)*(index2>0)])
    return pieces[:min(5,len(pieces))]

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
            list_of_art.append({'name':article_name, 'sisalto':doc})
    except IndexError:
        print("No results")
    return list_of_art


@app.route('/search')
def search():
    #Delete previous plots, to avoid having too many of them
    os.system('rm -f static/*_plt.png')
    #Get query from URL variable
    query = request.args.get('query')
    #Initialize list of matches
    keys = []
    matches = []
    plots = 0
    #If query not empty
    if query:
        list_version = list_of_articles
        matches = search_query(query, list_of_articles, list_version)
        for match in matches:
                while plots <= 5:
                    content = dict_of_articles.values()
                    extracted_content = extract_pieces(query.lower(),content)
                    matches.append({'name':art_name, 'palat':extracted_content, 'pltpath':art_name+'_plt.png' })
                    generate_individual_plots(query.lower(),art_name,content,extracted_content)
                    plots += 1
                    if plots < 5:
                        break
        #Render index.html with matches variable
        return render_template('index.html', matches=matches[:5])
    else:
        return render_template('indexempty.html', matches=[])


def generate_individual_plots(query, art_name, content, pieces):
    # YOUR code here:
    sisalto = ''.join(content)
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
    plt.savefig('static/'+art_name+'_plt.png')


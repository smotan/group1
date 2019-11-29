from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup 
import matplotlib.pyplot as plt
import matplotlib as mlp
import re
import nltk
import os
import numpy as np
import re
from nltk.stem import LancasterStemmer
import spacy
from spacy import displacy
from pathlib import Path


mlp.use('Agg')
# Load the file with the wiki articles
try:
    text_file = "enwiki.txt"
    with open(text_file,'r') as f:
        soup = BeautifulSoup(f,'lxml')
#generate a dictinoary with the entries and the content for each article
    list_of_articles = {art['name']:art.text for art in soup.find_all('article') }
except OSError:
    print("File not found")

app = Flask(__name__)

def extract_pieces(query,content):
    start_indexes = [m.start() for m in re.finditer(query,content.lower())]
    pieces=[]
    for i in start_indexes: 
        index1=content[max(i-15,0):i].find('\n')+1
        index2=content[i:i+100].find('\n')
        pieces.append('...'+content[max(0,i-15+index1):i+100-(100-index2)*(index2>0)]+'...')
        #print(i, content[i-15+index1:i+100-(100-index2)*(index2>0)])
    return pieces[:min(5,len(pieces))]

@app.route('/search')
def search():
    #Delete previous plots, to avoid having too many of them
    os.system('rm -f templates/*_plt.html')
    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []
    #If query not empty
    if query:
        #Look at each entry in the example data
        for art_name,content in list_of_articles.items():
            #If an entry name contains the query, add the entry to matches
            if query.lower() in content.lower():
                extracted_content = extract_pieces(query.lower(),content)
                sisalto =''.join(content)
                matches.append({'name':art_name, 'palat':extracted_content })
        #Render index.html with matches variable
        return render_template('index.html', matches=matches)
    else:
        return render_template('indexempty.html', matches=[])

@app.route('/entities')
def entities():
    sisalto =''.join(content)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sisalto)
    html = displacy.render(doc, style='ent', page=True)
    file_name = art_name + "_plt.html"
    output_path = Path("templates/" + file_name)
    output_path.open("w", encoding="utf-8").write(html)
    return render_template('Autism_plt.html', matches=matches)

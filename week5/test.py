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
        #Look at each entry in the example data
        for art_name,content in list_of_articles.items():
            #If an entry name contains the query, add the entry to matches
            if query.lower() in content.lower():
                while plots <= 5:
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


from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
   
def read_from_file():   
    try:
        text_file = open("enwiki.txt", "r")
        list_of_articles = []
        for line in text_file:
            if "<article name=" in line:
                text = ""
                continue
            elif "</article>" in line:
                list_of_articles.append(text)
            else:
                line = line.strip()
                text += " " + line
        return list_of_articles
    except OSError:
        print("File not found")
    
def main():

    while True:
        print("Quit: q & enter")
        query = input("Query: ")
        query = query.lower()
	quotes = re.search("^\".+\"$", query)
	list_of_articles = read_from_file()	

	if(quotes):
	    no_parse(query, list_of_articles)	    

        elif query == "q":
            print("Goodbye!")
            break
        else:
            parse(query, list_of_articles)

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
    try:        
        tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
        sparse_matrix = tfv.fit_transform(stem_list_of_articles).T.tocsr()
        query_vec = tfv.transform([query]).tocsc()        
        hits = np.dot(query_vec, sparse_matrix)
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
        articles = 0
        for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
            article = list_of_articles[doc_idx]
            doc = article[article.find(query)-100:article.find(query)+100]
            if score >= 0.02:
                articles += 1
                print("Score: {:.4f}: {:s}".format(score, doc))
        print("Found", articles, "articles")
    except IndexError:
        print("No results")            

def no_parse(query, list_of_articles):
	query = re.sub("\"", ' ', query)
	try:        
            tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
            sparse_matrix = tfv.fit_transform(list_of_articles).T.tocsr()
            query_vec = tfv.transform([query]).tocsc()        
            hits = np.dot(query_vec, sparse_matrix)
            ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
            articles = 0
            for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
                article = list_of_articles[doc_idx]
                doc = article[article.find(query)-100:article.find(query)+100]
                if score >= 0.02:
                    articles += 1
                    print("Score: {:.4f}: {:s}".format(score, doc))
            print("Found", articles, "articles")
        except IndexError:
	    print("No results")
main()

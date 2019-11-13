from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
   
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

        if query == "q":
            print("Goodbye!")
            break
        list_of_articles = read_from_file()
        
        
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
        
main()

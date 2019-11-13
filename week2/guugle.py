
from sklearn.feature_extraction.text import CountVectorizer

def rewrite_token(t, td_matrix, t2i):
    d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 

def rewrite_query(query, td_matrix, t2i): # rewrite every token in the query
    return " ".join(rewrite_token(t, td_matrix, t2i) for t in query.split())

#def test_query(query):
 #   print("Query: '" + query + "'")
  #  print("Rewritten:", rewrite_query(query))
   # print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
    #print()
        
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
            print("Goodbye")	
            break
        else:
            try:
                list_of_articles = read_from_file()
                if not list_of_articles:
                    break
                cv = CountVectorizer(lowercase=True, binary=True)
                sparse_matrix = cv.fit_transform(list_of_articles)
                td_matrix = sparse_matrix.todense().T
                t2i = cv.vocabulary_

                hits_matrix = eval(rewrite_query(query, td_matrix, t2i))
                hits_list = list(hits_matrix.nonzero()[1])
                for doc_idx in hits_list:
                    print("Matching doc:", list_of_articles[doc_idx])
            except:
                print("No results")	

        
main()

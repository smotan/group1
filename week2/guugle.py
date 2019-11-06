
from sklearn.feature_extraction.text import CountVectorizer

def rewrite_token(t):
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) # Can you figure out what happens here?

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def test_query(query):
    print("Query: '" + query + "'")
    print("Rewritten:", rewrite_query(query))
    print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
    print()
        
def read_from_file(filename):   
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
    except OSError:
        print("File not found")
    
def main():
    d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}

    while True:
        print("Lopeta painamalla q & enter")
        query = input("Query: ")
        query = query.lower()

	
        if query == "q":
            break
        else:
            hits_matrix = eval(rewrite_query(query))
            hits_list = list(hits_matrix.nonzero()[1])
            for doc_idx in hits_list:
                print("Matching doc:", list_of_articles[doc_idx])


        
main()

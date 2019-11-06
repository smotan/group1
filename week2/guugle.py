 #Hakukone
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(lowercase=True, binary=True)
sparse_matrix = cv.fit_transform(texthere)
td_matrix = sparse_matrix.todense().T

t2i = cv.vocabulary_  # shorter notation: t2i = term-to-index
print("Query: example")
print(td_matrix[t2i["example"]])

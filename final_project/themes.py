import pke

def read_from_file():   
    try:
        text_file = open("songs.txt", "r")
        file_text = text_file.read()
        list_of_songs = file_text.split("</article>")
        return list_of_songs
    except OSError:
        print("File not found")

def main():
    songs = read_from_file()
    songs = songs[:10]
    for song in songs:
         extractor = pke.unsupervised.TopicRank()
         extractor.load_document(input=songs, language='en')
         extractor.candidate_selection()
         extractor.candidate_weighting()
         keyphrases = extractor.get_n_best(n=10)
         print(song)
         for keyphrase in keyphrases:
             print(keyphrase[0] + ", score=" + str(keyphrase[1]))

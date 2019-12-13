import pke

def read_from_file():   
    try:
        text_file = open("songs_with_authors.txt", "r")
        file_text = text_file.read()
        list_of_songs = file_text.split("Title: ")
        return list_of_songs
    except OSError:
        print("File not found")

def main():
    songs = read_from_file()
    songs =list(filter(None, songs))
        
    try:
        for song in songs:
            extractor = pke.unsupervised.TopicRank()
            extractor.load_document(input=song, language='en')
            stoplist = ['Lyrics', 'lyrics', 'Author', 'author']
            extractor.candidate_selection(stoplist=stoplist)
            extractor.candidate_weighting()
            keyphrases = extractor.get_n_best(n=10)  
            phrases = ''          
            if keyphrases:
                phrases = ', '.join(str(kp) for kp in keyphrases)
            with open("themes1.txt", "a") as output:
                output.write(phrases + '\n')
    except ValueError:
        with open("themes1.txt", "a") as output:
            output.write('\n')
            pass

main()

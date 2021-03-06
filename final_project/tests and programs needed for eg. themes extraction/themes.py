#A program to perform themes extraction
import pke

def read_from_file():   
    try:
        text_file = open("../data/songs_with_authors.txt", "r")
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
            extractor = pke.unsupervised.KPMiner()
            extractor.load_document(input=song, language='en')
            stoplist = ['Lyrics', 'lyrics', 'Author', 'author']
            pos = {'NOUN', 'PROPN', 'ADJ'}
            extractor.candidate_selection(pos=pos, stoplist=stoplist)
            extractor.candidate_weighting()
            keyphrases = extractor.get_n_best(n=15)  
            phrases = ''          
            if keyphrases:
                phrases = ', '.join(str(kp) for kp in keyphrases)
            with open("../data/themes_KPMiner.txt", "a") as output:
                output.write(phrases + '\n')
    except ValueError:
        with open("themes.txt", "a") as output:
            output.write('\n')
            pass

main()

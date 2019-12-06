import pke

def read_from_file():   
    try:
        text_file = open("songs.txt", "r")
        file_text = text_file.read()
        list_of_songs = file_text.split("Title: ")
        return list_of_songs
    except OSError:
        print("File not found")

def main():
    songs = read_from_file()
    songs =list(filter(None, songs))
    themes = []
    try:
        for song in songs:
            extractor = pke.unsupervised.TopicRank()
            extractor.load_document(input=song, language='en')
            extractor.candidate_selection()
            extractor.candidate_weighting()
            keyphrases = extractor.get_n_best(n=1)
            for keyphrase in keyphrases:
                themes.append(keyphrase[0])
        with open("themes.txt", "w") as output:
            output.write(str(themes))
    except ValueError:
        print("No")
        pass

main()

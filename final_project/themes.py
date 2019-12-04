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
    index = 1
    songs_and_themes = []
    while index <= len(songs):
        try:
            song = songs[index]
            extractor = pke.unsupervised.TopicRank()
            extractor.load_document(input=song, language='en')
            extractor.candidate_selection()
            extractor.candidate_weighting()
            keyphrases = extractor.get_n_best(n=10)
            index += 1
        except ValueError:
            print("No")
            pass

main()

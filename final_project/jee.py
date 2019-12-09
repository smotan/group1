from string import digits 
import re

text_file = open("songs.txt", "r")
file_text = text_file.read()
list_of_songs = file_text.split("Title")
theme_file = open("themes1.txt", "r")
read_themes = theme_file.read()
remove_digits = str.maketrans('', '', digits)
res = read_themes.translate(remove_digits)
res = re.sub("\[", "", res)
res = re.sub("\(\'", "", res)
res = re.sub("\'\,", ",", res)
res = re.sub("\.\)", "", res)
res = re.sub(" ,", "", res)
list_of_themes = res.split("], ")
print(list_of_themes[-1])
print(list_of_songs[-1])
songs_and_themes = dict(zip(list_of_themes, list_of_songs))
list_of_songs = list(songs_and_themes.values())
list_of_themes = list(songs_and_themes.keys())


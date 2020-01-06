#A test to clean the theme file
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer
from string import digits

def main():

    try:
        text_file = open("songs.txt", "r")
        file_text = text_file.read()
        list_of_songs = file_text.split("Title: ")
        list_of_songs =list(filter(None, list_of_songs))
        theme_file = open("themes1.txt", "r")
        file_text = theme_file.read()
        remove_digits = str.maketrans('', '', digits)
        res = file_text.translate(remove_digits)
        res = re.sub("\[", "", res)
        res = re.sub("\(\'", "", res)
        res = re.sub("\'\,", ",", res)
        res = re.sub("\.\)", "", res)
        res = re.sub(" ,", "", res)
        list_of_themes = res.split("], ")
        songs_and_themes = dict(zip(list_of_themes, list_of_songs))

    except OSError:
        print("File not found")

    lista = list(songs_and_themes.values())[0]
    print(lista)

main()

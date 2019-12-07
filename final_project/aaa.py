from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
from nltk.stem import LancasterStemmer

def main():

    try:
        text_file = open("songs.txt", "r")
        file_text = text_file.read()
        list_of_songs = file_text.split("Title")
        list_of_songs =list(filter(None, list_of_songs))
        theme_file = open("themes.txt", "r")
        read_themes = theme_file.read()
        list_of_themes = read_themes.split(", ")
        songs_and_themes = dict(zip(list_of_themes, list_of_songs))
    except OSError:
        print("File not found")
    index = 2
    lista = list(songs_and_themes.keys())[index]
    lista = lista.replace("[","")
    lista = lista.replace("]","")
    lista = lista.replace("'","")
main()

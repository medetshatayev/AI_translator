# models/nltk_resources.py

import nltk

def download_nltk_resources():
    nltk.download('punkt')

def setup_nltk():
    download_nltk_resources()

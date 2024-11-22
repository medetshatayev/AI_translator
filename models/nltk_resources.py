# models/nltk_resources.py

import nltk

def download_nltk_resources():
    nltk.download('punkt_tab', quiet=True)

def setup_nltk():
    download_nltk_resources()

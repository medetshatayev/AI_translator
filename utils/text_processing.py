# utils/text_processing.py

from langdetect import detect, DetectorFactory
import pyphen

# Ensure consistent language detection
DetectorFactory.seed = 0

def detect_language(text):
    try:
        lang = detect(text)
        if lang not in ['ru', 'en', 'kk']:
            return None
        return lang
    except:
        return None

def count_syllables(word, lang):
    if lang == 'kk':
        vowels = "аеёиоуыэюяіүұөө"
        syllables = sum(1 for char in word.lower() if char in vowels)
        return max(1, syllables)
    else:
        dic = pyphen.Pyphen(lang=lang)
        hyphens = dic.inserted(word)
        return max(1, hyphens.count('-') + 1)

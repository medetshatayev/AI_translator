# utils/readability_indices.py

from nltk.tokenize import sent_tokenize, word_tokenize
from .text_processing import count_syllables
import streamlit as st

def flesch_reading_ease(text, lang):
    sentences = sent_tokenize(text, language='russian' if lang == 'ru' else 'english')
    words = [word for word in word_tokenize(text, language='russian' if lang == 'ru' else 'english') if word.isalpha()]
    num_sentences = max(1, len(sentences))
    num_words = max(1, len(words))
    syllable_count = sum([count_syllables(word, lang) for word in words])
    asl = num_words / num_sentences
    asw = syllable_count / num_words
    if lang == 'ru':
        fre = 206.835 - (1.3 * asl) - (60.1 * asw)
    elif lang == 'en':
        fre = 206.835 - (1.015 * asl) - (84.6 * asw)
    elif lang == 'kk':
        fre = 206.835 - (1.2 * asl) - (70 * asw)
    else:
        fre = 0
    return fre

def flesch_kincaid_grade_level(text, lang):
    sentences = sent_tokenize(text, language='russian' if lang == 'ru' else 'english')
    words = [word for word in word_tokenize(text, language='russian' if lang == 'ru' else 'english') if word.isalpha()]
    num_sentences = max(1, len(sentences))
    num_words = max(1, len(words))
    syllable_count = sum([count_syllables(word, lang) for word in words])
    asl = num_words / num_sentences
    asw = syllable_count / num_words
    if lang == 'ru':
        fkgl = (0.5 * asl) + (8.4 * asw) - 15.59
    elif lang == 'en':
        fkgl = (0.39 * asl) + (11.8 * asw) - 15.59
    elif lang == 'kk':
        fkgl = (0.5 * asl) + (9 * asw) - 13
    else:
        fkgl = 0
    return fkgl

def gunning_fog_index(text, lang):
    sentences = sent_tokenize(text, language='russian' if lang == 'ru' else 'english')
    words = [word for word in word_tokenize(text, language='russian' if lang == 'ru' else 'english') if word.isalpha()]
    num_sentences = max(1, len(sentences))
    num_words = max(1, len(words))
    complex_words = [word for word in words if count_syllables(word, lang) >= 3]
    percentage_complex = (len(complex_words) / num_words) * 100
    asl = num_words / num_sentences
    fog_index = 0.4 * (asl + percentage_complex)
    return fog_index

def smog_index(text, lang):
    sentences = sent_tokenize(text, language='russian' if lang == 'ru' else 'english')
    words = [word for word in word_tokenize(text, language='russian' if lang == 'ru' else 'english') if word.isalpha()]
    num_sentences = len(sentences)
    complex_words = [word for word in words if count_syllables(word, lang) >= 3]
    num_complex = len(complex_words)
    if num_sentences >= 3:
        smog = 1.0430 * ((num_complex * (30 / num_sentences)) ** 0.5) + 3.1291
    else:
        smog = 0
    return smog


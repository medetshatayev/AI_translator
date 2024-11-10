# utils/translation.py

import streamlit as st

def translate_text(input_text, src_lang, tgt_lang, translation_pipelines):
    if (src_lang, tgt_lang) not in translation_pipelines or translation_pipelines[(src_lang, tgt_lang)] is None:
        st.error(f"Перевод с {src_lang} на {tgt_lang} не поддерживается.")
        return ""

    try:
        translation_pipeline = translation_pipelines[(src_lang, tgt_lang)]
        translated = translation_pipeline(input_text, max_length=10000)
        translated_text = translated[0]['translation_text']

        # Post-processing: Replace semicolons and capitalize sentences
        translated_text = translated_text.replace(';', '.')
        sentences = translated_text.split('. ')
        translated_text = '. '.join(sentence.capitalize() for sentence in sentences)
    except Exception as e:
        st.error("Ошибка при выполнении перевода.")
        translated_text = ""

    return translated_text

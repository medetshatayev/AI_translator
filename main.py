# main.py

import streamlit as st
import logging
# Set page configuration
st.set_page_config(page_title="Анализ Понятности и Перевод Текста", layout="wide")
logging.basicConfig(level=logging.DEBUG)
import os
import tempfile
import io
from docx import Document

# Import modules after setting page config
from models.nltk_resources import setup_nltk
from models.transformers_models import (
    load_sentiment_analyzer as _load_sentiment_analyzer,
)
from utils.file_readers import read_file
from utils.text_processing import detect_language
from utils.readability_indices import (
    flesch_reading_ease,
    flesch_kincaid_grade_level,
    gunning_fog_index,
    smog_index,
)
from utils.formatting import color_code_index
from utils.argos_translate import translate_text

def main():
    # Setup NLTK resources
    setup_nltk()

    # Load models
    sentiment_analyzer = load_sentiment_analyzer()

    # Define the rest of your main function
    st.title("Анализ Понятности Текста и Перевод")
    st.sidebar.header("Настройки")
    functionality = st.sidebar.radio("Выберите функциональность", ("Анализ удобочитаемости", "Перевод"))

    if functionality == "Перевод":
        # Translation functionality
        st.header("Перевод текста или документов")
        translate_input_method = st.radio(
            "Выберите способ ввода текста для перевода", ("Загрузить файл", "Вставить текст")
        )
        translate_text_input = ""

        if translate_input_method == "Загрузить файл":
            translate_uploaded_file = st.file_uploader(
                "Выберите файл (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"]
            )
            if translate_uploaded_file is not None:
                suffix = os.path.splitext(translate_uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(translate_uploaded_file.getbuffer())
                    temp_file_path = tmp_file.name
                translate_text_input = read_file(temp_file_path)
                os.remove(temp_file_path)
                st.write("**Содержимое файла для перевода:**")
                st.write(translate_text_input)
        else:
            translate_text_input = st.text_area("Вставьте ваш текст для перевода здесь", height=200)

        if translate_text_input:
            auto_detect_translate = st.checkbox("Автоматически определить исходный язык", value=True)

            if auto_detect_translate:
                detected_src_lang = detect_language(translate_text_input)
                if detected_src_lang in ['ru', 'en']:
                    st.info(
                        f"Автоматически определённый исходный язык: **{'Русский' if detected_src_lang == 'ru' else 'Английский'}**"
                    )
                    src_lang = detected_src_lang
                else:
                    st.warning(
                        "Не удалось определить язык или язык не поддерживается. Пожалуйста, выберите исходный язык вручную."
                    )
                    src_lang = st.selectbox("Выберите исходный язык", ("ru", "en"))
            else:
                src_lang = st.selectbox("Выберите исходный язык", ("ru", "en"))

            # Choose target language
            if src_lang == "ru":
                available_tgt_langs = ["en"]
            elif src_lang == "en":
                available_tgt_langs = ["ru"]
            else:
                available_tgt_langs = []

            if available_tgt_langs:
                tgt_lang = st.selectbox("Выберите целевой язык", available_tgt_langs)
                if st.button("Перевести"):
                    with st.spinner('Выполняется перевод...'):
                        translated_text = translate_text(translate_text_input, src_lang, tgt_lang)
                    if translated_text:
                        st.subheader("Переведённый текст:")
                        st.write(translated_text)

                        # Create a Word document
                        doc = Document()
                        doc.add_paragraph(translated_text)

                        # Save the document to a BytesIO object
                        doc_io = io.BytesIO()
                        doc.save(doc_io)
                        doc_io.seek(0)

                        # Provide the download button for the Word document
                        st.download_button(
                            label="Скачать переведённый текст",
                            data=doc_io,
                            file_name=f"translated_text.docx",
                            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        )
                    else:
                        st.warning("Перевод не выполнен. Пожалуйста, проверьте введенный текст и попробуйте снова.")
            else:
                st.warning("Выбранный исходный язык не поддерживается для перевода.")

    elif functionality == "Анализ удобочитаемости":
        # Readability analysis functionality
        st.header("Анализ удобочитаемости текста")
        input_method = st.radio("Выберите способ ввода текста", ("Загрузить файл", "Вставить текст"))
        text = ""

        if input_method == "Загрузить файл":
            uploaded_file = st.file_uploader("Выберите файл (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"])
            if uploaded_file is not None:
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_file_path = tmp_file.name
                text = read_file(temp_file_path)
                os.remove(temp_file_path)
                st.write("**Содержимое файла:**")
                st.write(text)
        else:
            text = st.text_area("Вставьте ваш текст здесь", height=200)

        if text:
            auto_detect = st.checkbox("Автоматически определить язык текста", value=True)

            if auto_detect:
                detected_lang = detect_language(text)
                if detected_lang in ['ru', 'en']:
                    st.info(
                        f"Автоматически определённый язык: **{'Русский' if detected_lang == 'ru' else 'Английский'}**"
                    )
                    lang_code = detected_lang
                else:
                    st.warning(
                        "Не удалось определить язык или язык не поддерживается. Пожалуйста, выберите язык вручную."
                    )
                    lang_code = st.selectbox("Выберите язык текста", ("ru", "en"))
            else:
                lang_code = st.selectbox("Выберите язык текста", ("ru", "en"))

            if st.button("Анализировать"):
                analyze_readability(text, lang_code, sentiment_analyzer)

def analyze_readability(text, lang_code, sentiment_analyzer):
    fre = flesch_reading_ease(text, lang_code)
    fkgl = flesch_kincaid_grade_level(text, lang_code)
    fog = gunning_fog_index(text, lang_code)
    smog = smog_index(text, lang_code)

    if (lang_code == 'ru' or lang_code == 'en') and sentiment_analyzer is not None:
        try:
            sentiment = sentiment_analyzer(text)
            sentiment_label = sentiment[0]['label']
            sentiment_score = sentiment[0]['score']
        except:
            sentiment_label = "Не удалось выполнить анализ тональности."
            sentiment_score = None
    else:
        sentiment_label = "Тональность не поддерживается для данного языка."
        sentiment_score = None

    # Display results in Streamlit
    st.subheader("Результаты анализа")

    # Display indices with color coding
    st.markdown(
        f"**Индекс удобочитаемости Флеша:** {color_code_index('Flesch Reading Ease', fre)}",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**Индекс Флеша-Кинкейда:** {color_code_index('Flesch-Kincaid Grade Level', fkgl)}",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**Индекс тумана Ганнинга:** {color_code_index('Gunning Fog Index', fog)}",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**Индекс SMOG:** {color_code_index('SMOG Index', smog)}",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.subheader("Оценка тональности:")
    if sentiment_score is not None:
        st.write(f"**Тональность:** {sentiment_label}")
        st.write(f"**Уверенность:** {sentiment_score:.2f}")
    else:
        st.write(sentiment_label)

    st.markdown("---")

@st.cache_resource
def load_sentiment_analyzer():
    analyzer = _load_sentiment_analyzer()
    if not analyzer:
        st.error("Ошибка при загрузке модели для анализа тональности.")
    return analyzer

if __name__ == "__main__":
    main()

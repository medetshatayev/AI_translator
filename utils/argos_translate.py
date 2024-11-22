# utils/argos_translate.py

import os
os.environ["ARGOS_DEVICE_TYPE"] = "cuda"  # Set to "cuda" or "auto"
import argostranslate.package
import argostranslate.translate
import streamlit as st
import traceback
import logging
logging.basicConfig(level=logging.DEBUG)

def install_language_package(from_code, to_code):
    # Update package index
    argostranslate.package.update_package_index()

    # Get available packages
    available_packages = argostranslate.package.get_available_packages()

    # Find the desired package
    package_to_install = next(
        (pkg for pkg in available_packages if pkg.from_code == from_code and pkg.to_code == to_code),
        None
    )

    if package_to_install:
        # Install the package
        argostranslate.package.install_from_path(package_to_install.download())
    else:
        st.error(f"No language package found for translation from '{from_code}' to '{to_code}'.")

def ensure_language_package_installed(from_code, to_code):
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((lang for lang in installed_languages if lang.code == from_code), None)
    to_lang = next((lang for lang in installed_languages if lang.code == to_code), None)
    if from_lang and to_lang:
        translation = from_lang.get_translation(to_lang)
        if translation:
            return
    # Install if not present
    install_language_package(from_code, to_code)

# Ensure the language packages are installed
ensure_language_package_installed('en', 'ru')
ensure_language_package_installed('ru', 'en')

def translate_text(input_text, src_lang, tgt_lang):
    try:
        # Load installed languages
        installed_languages = argostranslate.translate.get_installed_languages()

        # Debugging: Print installed languages
        print("Installed languages in Streamlit app:")
        for lang in installed_languages:
            print(f"{lang.name} ({lang.code})")

        # Map language codes to Argos Translate language objects
        from_lang = next((lang for lang in installed_languages if lang.code == src_lang), None)
        to_lang = next((lang for lang in installed_languages if lang.code == tgt_lang), None)

        if from_lang is None:
            st.error(f"Source language '{src_lang}' not found among installed languages.")
            return ""
        if to_lang is None:
            st.error(f"Target language '{tgt_lang}' not found among installed languages.")
            return ""

        translation = from_lang.get_translation(to_lang)

        if translation is None:
            st.error(f"No translation model found for '{src_lang}' to '{tgt_lang}'.")
            return ""

        # Translate the text
        translated_text = translation.translate(input_text)

    except Exception as e:
        st.error(f"Ошибка при выполнении перевода: {e}")
        traceback_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
        st.error(f"Полная информация об ошибке:\n{traceback_str}")
        translated_text = ""

    return translated_text

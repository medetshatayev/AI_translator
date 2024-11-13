# utils/translation.py

import streamlit as st
import re
import torch
from torch.amp import autocast
import traceback


def translate_text(input_text, src_lang, tgt_lang, translation_pipelines):
    if (src_lang, tgt_lang) not in translation_pipelines or translation_pipelines[(src_lang, tgt_lang)] is None:
        st.error(f"Перевод с {src_lang} на {tgt_lang} не поддерживается.")
        return ""

    try:
        translation_pipeline = translation_pipelines[(src_lang, tgt_lang)]
        tokenizer = translation_pipeline.tokenizer
        model = translation_pipeline.model

        # Ensure the device is correctly set
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")

        # Step 1: Remove multiple spaces
        cleaned_text = re.sub(r'\s+', ' ', input_text.strip())

        # Step 2: Split text into sentences using '. ' and new lines as delimiters
        sentences = re.split(r'\.\s|\n+', cleaned_text)

        # Step 3: Trim each sentence to get rid of extra spaces at the beginning and at the end
        sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty strings

        # Set maximum token limit (slightly less than model's max to account for special tokens)
        max_tokens = 460

        # Prepare sentences and check for token length
        sentences_to_translate = []
        for sentence in sentences:
            # Encode the sentence to get the number of tokens
            sentence_tokens = tokenizer.encode(sentence, return_tensors='pt').to(device)
            sentence_token_count = sentence_tokens.shape[1]

            if sentence_token_count > max_tokens:
                # If the sentence exceeds max_tokens, raise an error
                st.error(
                    f"Предложение слишком длинное для перевода (более {max_tokens} токенов). Пожалуйста, упростите это предложение:\n\n{sentence}")
                return ""

            sentences_to_translate.append(sentence)

        # Translate sentences in batches
        batch_size = 256  # Adjust batch size as needed
        translated_sentences = []
        for i in range(0, len(sentences_to_translate), batch_size):
            batch = sentences_to_translate[i:i + batch_size]

            # Tokenize the batch and move inputs to GPU
            inputs = tokenizer(batch, return_tensors='pt', padding=True, truncation=True).to(device)

            # Generate translations using the model with autocast
            with torch.no_grad():
                with autocast(device_type=device.type):
                    translated_tokens = model.generate(
                        **inputs,
                        max_length=512,
                        num_beams=5,
                        early_stopping=True
                    )

            # Decode translations
            batch_translations = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
            translated_sentences.extend(batch_translations)

        # Combine translated sentences
        translated_text = '. '.join(translated_sentences)

        # Post-processing: Capitalize sentences
        translated_text = '. '.join(sentence.capitalize() for sentence in translated_text.split('. '))

    except Exception as e:
        st.error(f"Ошибка при выполнении перевода: {e}")
        # Capture the full traceback
        traceback_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
        st.error(f"Полная информация об ошибке:\n{traceback_str}")
        translated_text = ""

    return translated_text
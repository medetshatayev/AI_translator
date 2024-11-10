# models/transformers_models.py

import torch
from transformers import pipeline

def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

def load_translation_models():
    device = get_device()
    translation_models = {
        ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
        ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
    }
    loaded_models = {}
    for (src, tgt), model_name in translation_models.items():
        try:
            loaded_models[(src, tgt)] = pipeline(
                "translation",
                model=model_name,
                device=0 if device == "cuda" else -1
            )
        except Exception as e:
            # Return None for failed models
            loaded_models[(src, tgt)] = None
    return loaded_models

def load_sentiment_analyzer():
    device = get_device()
    try:
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="yiyanghkust/finbert-tone",
            device=0 if device == "cuda" else -1
        )
        return sentiment_analyzer
    except Exception as e:
        # Return None if loading fails
        return None

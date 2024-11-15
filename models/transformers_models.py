# models/transformers_models.py

import torch
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

def get_device():
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU.")
        return torch.device("cuda:0")  # Use GPU index 0
    else:
        print("CUDA is not available. Using CPU.")
        return torch.device("cpu")

def load_translation_models():
    device = get_device()
    translation_models = {
        ("en", "ru"): "Helsinki-NLP/opus-mt-en-ru",
        ("ru", "en"): "Helsinki-NLP/opus-mt-ru-en",
    }
    loaded_models = {}
    for (src, tgt), model_name in translation_models.items():
        try:
            # Load tokenizer and model separately
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
            # Do not convert the model to FP16 here

            # Create translation pipeline
            translation_pipeline = pipeline(
                "translation",
                model=model,
                tokenizer=tokenizer,
                device=0 if device.type == 'cuda' else -1
                # Do not set torch_dtype here
            )

            # Store the pipeline in the loaded_models dictionary
            loaded_models[(src, tgt)] = translation_pipeline

            print(f"Loaded model {model_name} on device {device}")
        except Exception as e:
            loaded_models[(src, tgt)] = None
            print(f"Failed to load model {model_name}: {e}")
    return loaded_models

def load_sentiment_analyzer():
    device = get_device()
    try:
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="yiyanghkust/finbert-tone",
            device=0 if device.type == "cuda" else -1
        )
        return sentiment_analyzer
    except Exception as e:
        return None

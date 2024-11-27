# models/transformers_models.py

from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import os
import logging

def load_sentiment_analyzer():
    try:
        local_model_dir = 'local_models/finbert-tone'

        # Check if the local model directory exists
        if not os.path.exists(local_model_dir):
            logging.error(f"Local FinBERT model not found at '{local_model_dir}'.")
            return None

        # Load the model and tokenizer from the local directory
        model = AutoModelForSequenceClassification.from_pretrained(local_model_dir)
        tokenizer = AutoTokenizer.from_pretrained(local_model_dir)

        # Initialize the pipeline with the local model and tokenizer
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            device=0  # Set to -1 for CPU or 0 for GPU
        )

        logging.debug("Sentiment analyzer loaded successfully using the local FinBERT model.")

        return sentiment_analyzer

    except Exception as e:
        logging.error(f"Error loading sentiment analyzer: {e}")
        return None

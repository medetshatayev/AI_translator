# download_finbert.py

from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os

model_name = 'yiyanghkust/finbert-tone'
local_model_dir = 'local_models/finbert-tone'

# Create the directory if it doesn't exist
os.makedirs(local_model_dir, exist_ok=True)

# Download and save the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.save_pretrained(local_model_dir)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(local_model_dir)

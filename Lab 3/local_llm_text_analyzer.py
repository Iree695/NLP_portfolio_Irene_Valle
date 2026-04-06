import streamlit as st
import ollama
import json
import re
import nltk
import nltk.corpus import stopwords
import time

# Setup of NLTK
@st.cache_resource # Saving in memory
def download_nltk_data():
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet = True)

download_nltk_data()

def preprocessing_text():
    "For preprocessing: lowercase, remove punctuation and stopwords."
    text = text.lower() # to lowercase
    text = re.sub(r"[^a-z\s]", "", text) # remove punctuation
    stop_words = set(stopwords.words("english"))
    words = text.split()
    cleaned = []
    for w in words:
        if w not in stop_words and len(w) > 2:
            cleaned.append(w)
    return " ".join(cleaned)

def prompt_creation(cleaned_text):
    "Prompt for structured JSON output"
    prompt = f"""You are a smart text analyzer. Analyze this cleaned text:{cleaned_text}
    Return a valid JSON in this format no extra text or explanation:
    {{
    "sentiment" = "positive" or "negative" or "neutral",
    "confidence" = 0.75,
    "keywords" = ["keyword1", "keyword2", "keyword3", "keyword4"]
    "summary" = " One or two sentence summary of the text."
    }}
"""

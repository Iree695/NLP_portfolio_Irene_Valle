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
    return prompt

def analyze_llm(text_model):
    "Preprocessing, with Ollama -> JSON"
    cleaned = preprocessing_text(text)
    prompt = prompt_creation()
    try:
        start_time = time.time()
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        latency = time.time() - start_time
        
        content = response['message']['content'].strip()
        
        # Extract JSON from response
        json_start = content.find('{')
        json_end = content.rfind('}') + 1
        if json_start != -1 and json_end > json_start:
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
        else:
            result = {"error": "No JSON found"}
        
        result['cleaned_text'] = cleaned
        result['latency'] = round(latency, 2)
        return result, None
    except json.JSONDecodeError:
        return {"error": "JSON parse failed", "raw_response": content}, cleaned
    except Exception as e:
        return {"error": str(e)}, cleaned
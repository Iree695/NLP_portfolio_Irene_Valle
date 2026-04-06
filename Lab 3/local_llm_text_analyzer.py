import streamlit as st
import ollama
import json
import re
import nltk
from nltk.corpus import stopwords
import time

# Setup of NLTK
@st.cache_resource # Saving data
def download_nltk_data():
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)

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
    

# Streamlit APP
st.set_page_config(page_title= "Smart Text Analyzer", layout="wide")
st.title("Smart Text Analyzer")
st.markdown("**Local LLM app using Ollama** - Sentiment, Keywords and summary")

    # Sidebar:
with st.sidebar:
    st.header("How it works?")
    st.write("1. Preprocess Texts --> cleaning")
    st.write("2. Promt local LLM --> Structured Analysis")
    st.write("3. Display Results")

text_input = st.text_area(
    "Paste your text here(e.g., product review or article snippet):",
    height= 180,
    placeholder= "Enter text to analyze..."
    )

models_available = ["llama3.2:1b", "tinyllama"]
selected_model = st.selectbox("Choose local model (faster = smaller):", models_available)

if st.button("Analyze with Ollama", type="primary", use_container_width=True):
    if text_input and text_input.strip():
        with st.spinner(f"Processong with{selected_model}...(this may take a few seconds)"):
            result, err = analyze_llm(text_input, selected_model)
        
        if "error" in result:
            st.error(f"Analysis error: {result["error"]}")
            if "raw_response" in result:
                st.code(result["raw_response"], language="text")
        else:
            st.success("Analysis complete!")

            # Original vs cleaned
            col1, col2 = st.colums(2)
            with col1:
                st.subheader("Original Text")
                st.write(
                    text_input[:700] + (
                        "..."
                        if len(text_input) > 700
                        else ""
                    )
                )

            with col2:
                st.subheader("Preprocessed (Cleaned) Text")
                st.write(
                    result.get("cleaned_text", "")[:700] + (
                        "..."
                        if len(result.get("cleaned_text", "")) > 700
                        else ""
                    )
                )
            
            # Results
            st.subheader("Analysis Results")

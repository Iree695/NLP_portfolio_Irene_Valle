import streamlit as st
import ollama
import json
import re
import nltk
from nltk.corpus import stopwords
import time

# Setup of NLTK
@st.cache_resource # Saving data
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    cleaned = [w for w in words if w not in stop_words and len(w) > 2]
    return " ".join(cleaned)

def create_prompt(cleaned_text):
    prompt = f'''You are a smart text analyzer. Analyze this cleaned text: {cleaned_text}
Return ONLY a valid JSON object, no extra text or explanation:
{{
  "sentiment": "positive" or "negative" or "neutral",
  "confidence": 0.75,
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "summary": "One or two sentence summary of the text."
}}'''
    return prompt

def analyze_with_llm(text, model):
    cleaned = preprocess_text(text)
    prompt = create_prompt(cleaned)
    
    try:
        start_time = time.time()
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        latency = time.time() - start_time

        content = response['message']['content'].strip()

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

            # Sentiment
            with st.expander("Sentiment Analysis", expanded=True):
                sent = result.get("sentiment", "neutral").capitalize()
                conf = result.get("confidence", 0.65)

                if sent == "Positive":
                    st.success(f"Sentiment: {sent}")
                elif sent == "Negative":
                    st.error(f"Sentiment: {sent}")
                else:
                    st.warning(f"Sentiment: {sent}")

                st.write(f"Confidence: {conf:.2f}")


            # Keywords
            with st.expander("Keywords", expanded=True):
                keywords = result.get("keywords", ["N/A"])
                st.write("**Extracted Keywords:**")
                st.write(", ".join(keywords))
                st.write("**Top Keywords List:**")
                for i, kw in enumerate(keywords[:5], 1):
                    st.write(f"{i}. {kw}")
            
            # Summary
            with st.expander("Summary", expanded=True):
                st.write(result.get("summary", "No summary generated."))
            
            st.caption(f"Processed in {result.get('latency', 'N/A')} seconds using local {selected_model}")
    else:
        st.warning("Please enter some text to analyze.")

st.caption("Built with Streamlit + Ollama")
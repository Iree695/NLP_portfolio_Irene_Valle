import streamlit as st
import ollama
import json
import re
import nltk
from nltk.corpus import stopwords
import time

# Setup of NLTK
# I cache this so Streamlit does not try to download the same data again and again
@st.cache_resource
def download_nltk_data():
    try:
        # Check if punkt is already installed
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        # If not, download it
        nltk.download('punkt', quiet=True)
    try:
        # Check if stopwords are already installed
        nltk.data.find('corpora/stopwords')
    except LookupError:
        # If not, download them
        nltk.download('stopwords', quiet=True)

# Run this once when the app starts
download_nltk_data()

def preprocess_text(text):
    # Make everything lowercase first
    text = text.lower()

    # Remove punctuation, numbers, and anything that is not a letter
    text = re.sub(r'[^a-z\s]', '', text)

    # Load English stopwords like "the", "and", "is", etc.
    stop_words = set(stopwords.words('english'))

    # Split the text into words
    words = text.split()

    # Keep only useful words:
    # - not stopwords
    # - longer than 2 characters
    cleaned = [w for w in words if w not in stop_words and len(w) > 2]

    # Join everything back into one cleaned string
    return " ".join(cleaned)

def create_prompt(cleaned_text):
    # This prompt tells the model exactly what format I want back
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
    # First clean the text, then build the prompt
    cleaned = preprocess_text(text)
    prompt = create_prompt(cleaned)
    
    try:
        # Start timer to measure how long the model takes
        start_time = time.time()

        # Send the prompt to the selected Ollama model
        response = ollama.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )

        # Calculate total response time
        latency = time.time() - start_time

        # Get the text content returned by the model
        content = response['message']['content'].strip()

        # Sometimes models add extra text, so I extract only the JSON part
        json_start = content.find('{')
        json_end = content.rfind('}') + 1

        if json_start != -1 and json_end > json_start:
            json_str = content[json_start:json_end]
            result = json.loads(json_str)
        else:
            result = {"error": "No JSON found"}

        # Add extra info so I can show it in the interface
        result['cleaned_text'] = cleaned
        result['latency'] = round(latency, 2)

        return result, None

    except Exception as e:
        # If something goes wrong, return the error message
        return {"error": str(e)}, cleaned

# Streamlit APP
st.set_page_config(page_title="Smart Text Analyzer", layout="wide")
st.title("Smart Text Analyzer")
st.markdown("**Local LLM app using Ollama** - Sentiment, Keywords and summary")

# Sidebar:
with st.sidebar:
    st.header("How it works?")
    st.write("1. Preprocess Texts --> cleaning")
    st.write("2. Prompt local LLM --> Structured Analysis")
    st.write("3. Display Results")

text_input = st.text_area(
    "Paste your text here(e.g., product review or article snippet):",
    height=180,
    placeholder="Enter text to analyze..."
)

models_available = ["llama3.2:1b", "tinyllama"]
selected_model = st.selectbox("Choose local model (faster = smaller):", models_available)

if st.button("Analyze with Ollama", type="primary", use_container_width=True):
    if text_input and text_input.strip():
        with st.spinner(f"Processing with {selected_model}...(this may take a few seconds)"):
            result, err = analyze_with_llm(text_input, selected_model)
        
        if "error" in result:
            st.error(f"Analysis error: {result['error']}")
            if "raw_response" in result:
                st.code(result["raw_response"], language="text")
        else:
            st.success("Analysis complete!")

            # Original vs cleaned
            # I show both so it is easier to compare the input and the processed version
            col1, col2 = st.columns(2)

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

                # Different message color depending on the sentiment
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

                # Show the keywords again as a numbered list
                st.write("**Top Keywords List:**")
                for i, kw in enumerate(keywords[:5], 1):
                    st.write(f"{i}. {kw}")
            
            # Summary
            with st.expander("Summary", expanded=True):
                st.write(result.get("summary", "No summary generated."))
            
            # Show model name and how long the analysis took
            st.caption(f"Processed in {result.get('latency', 'N/A')} seconds using local {selected_model}")
    else:
        st.warning("Please enter some text to analyze.")

st.caption("Built with Streamlit + Ollama")
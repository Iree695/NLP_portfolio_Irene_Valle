# Smart Text Analyzer - Local LLM Application

**Subject:** Procesamiento de Lenguaje Natural  
**Student:** Irene Valle  
**Date:** Abril 2026  
**Folder:** Lab 3

## Problem Description
I created a program called **Smart Text Analyzer** for this lab. The program lets the user to type whatever text—product reviews, article extracts, comments, etc.—and automatically get:
- Positive, negative, or neutral sentiment analysis
- Extracting of keywords
- An abbreviated synopsis of the text

Most importantly, it's about asking the LLM about itself as well as asking it queries. Build is a full pipeline from preprocessing through postprocessing and prompt engineering.

### System Design and Workflow
The procedure entails these phases:

1. The user picks the model in the Streamlit interface after input.
2. NLTK cleans the text by lowering, punctuating, and eliminating stopwords.
3. A well designed prompt is developed to compel the LLM to provide the answer in JSON format.
4. **Inference**: The local model is called via Ollama.
5. **Postprocessing**: The JSON is parsed, potential errors are handled, and the results are displayed visually.

**Flowchart of the text**
User Input
↓
Preprocessing (NLTK)
↓
Structured Prompt
↓
Ollama (Local LLM)
↓
JSON Parsing + Postprocessing
↓
Results: Sentiment + Keywords + Summary

## Model Selection and Justification
**Ollama** was used as the tool to run the model locally.

The main model chosen is **`llama3.2:1b`** because:
- It is very lightweight and fast on standard computers
- It consumes few resources
- It is sufficient for basic English text analysis tasks

As an alternate selection in the selector, it was also added under **"tinyllama"**.

All processing is done locally, ensuring privacy and independent of an internet connection (after model download).

## Implementation Details
**Tools used:**
- Python 3
- Streamlit → to create the graphical interface
- Ollama (Python library)
- NLTK → only for stopwords and basic preprocessing
- Standard libraries: `re`, `json`, `time`

**Important decisions:**
- The code was kept simple and readable (less than 120 lines).
- A strict prompt was used to obtain JSON output.
- Basic error handling and response time measurement were added.

### Main code: `local_llm_text_analyzer.py`
(The complete code is in the file within this folder)

## Results and Screenshots
The application works correctly with different types of text. Sentiment is generally accurate, keywords are relevant, and summaries are clear and concise.
Screenshots included:

Main interface (empty)

Text entered and model selected

Complete results with tabs (Sentiment, Keywords, Summary)

## Discussion, Limitations, and Improvements
Starting with a simple Streamlit UI, I progressively integrated NLTK preprocessing, advertisement engineering to get structured JSON, response analysis, and results presentation. 

**Limits observed include:** 
 - Hallucinations sometimes result when using a tiny model (llama3.2:1b); alternatively, the JSON is not properly produced. 
 - Although lower than that of larger models, sentiment and summary precision are adequate. 
 - Response time varies greatly depending on the selected model and the size of the text. 
 
**Possible future enhancements:**
 - Try more robust models like `llama3.2:3b` or `llama3.1:8b`. 
 - Employ the `wordcloud` library to create a word cloud representation for keywords. - Save outcomes or put analysis history into use. 
 - Improve quick engineering to get more steady results. 
 - Include RAG in a more sophisticated course project.

## How to Run the Application
    # 1. Install dependencies
    pip install -r requirements.txt
    # 2. Download the model (only the first time)
    ollama pull llama3.2:1b
    # 3. Run the application
    streamlit run local_llm_text_analyzer.py

## requirements.txt
streamlit
ollama
nltk
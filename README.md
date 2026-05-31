# The Council

The council is a RAG system that has been fed philosophers and various deep thinkers.

# Step1: Ingestion Pipeline

`ingestion_pipeline.py` is the script responsible for ingesting texts into the system. It reads the text files, processes them, and stores them in a format suitable for retrieval.

First I created a virtual environment and installed the necessary dependencies:

```bash
python -m venv venv
venv\Scripts\activate # because Im on windows.
pip install langchain langchain-community langchain_text_splitters langchain-google-genai supabase # Im using genai cuz its free rather than openai which is paid.
```

Next, I wrote a function for reading the text files called

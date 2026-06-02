# The Council

The council is a RAG system that has been fed philosophers and various deep thinkers.

# Step1: Ingestion Pipeline

`ingestion_pipeline.py` is the script responsible for ingesting texts into the system. It reads the text files, processes them, and stores them in a format suitable for retrieval.

First I created a virtual environment and installed the necessary dependencies:

```bash
python -m venv venv
venv\Scripts\activate # because Im on windows. on linux its source venv/bin/activate
pip install langchain langchain-community langchain_text_splitters langchain-google-genai supabase tqdm # Im using genai cuz its free rather than openai which is paid.
```

Next, I wrote scrit for ingestion of the text files.

# Issue#1 : Rate Limiting Problem

Im running into a rate limit problem. The free tier of gemini-embedding-001 only allows 100 requests/minute. I am trying to embed 5816 chunks at once.

So solution for this is to create a batching system and wait in between. I will build this project FREE of cost, even though the whole thing would cost me a few cents if I paid.

So the idea is I import time, create a for loop that creates batches and then runs the vector store function and has a sleep/wait timer.

![ingestion pipeline complete](/screenshots/pipeline_complete_console.png)

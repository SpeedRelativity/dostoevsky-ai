# so this file will have the retrieval pipeline

import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()

# same supabase client
supabase_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# same embedding model as ingestion pipeline
embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        output_dimensionality=768,
        google_api_key=os.getenv("GOOGLE_API_KEY"))

vector_store = SupabaseVectorStore(
    embedding=embedding_model,
    client=supabase_client,
    table_name="documents",
    query_name="match_documents"
)


# feed chunks and query to LLM.

from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

app = FastAPI()

system_message = "You are a philosopher that is an expert in Dostoevsky readings. Always give deep, insightful answers that provoke thought and reflection. Use the context provided in your answers. If the user asks irrelevant question, reply saying that is outside your domain of expertise."

LLM = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"))

@app.post("/chat")
def chat(query):
    # first we get relevant chunks
    relevant_chunks = vector_store.similarity_search(query, k=4)
    # now we setup the LLM and feed chunk + query as context to the LLM
    context = "Some context:" + "\n".join([chunk.page_content for chunk in relevant_chunks])
    combined = f"{context}\n\nUser query: {query}"
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=combined)
    ]
    response = LLM.invoke(messages)
    return response.content




    


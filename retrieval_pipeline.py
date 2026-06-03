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
from pydantic import BaseModel




app = FastAPI()

system_message = """You are a philosophical guide grounded in Dostoevsky's work. \
Answer the user's question directly and helpfully, drawing on the provided context. \
Be insightful but CONCISE — 3 to 5 sentences. Lead with the actual answer, not preamble. \
Speak in clear, plain language a normal person understands. No theatrical narration, \
no "Ah, the year 2026!" openings, no rhetorical flourishes. \
If the question is unrelated to philosophy or the human condition, say it's outside your scope.

Use the provided passages when relevant. If they don't help, answer from Dostoevsky's broader ideas rather than forcing them in."""

LLM = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_output_tokens=800,
        temperature=0.7)

class Query(BaseModel):
    query: str

@app.post("/chat")
def chat(input: Query):
    # first we get relevant chunks
    relevant_chunks = vector_store.similarity_search(input.query, k=4)
    # now we setup the LLM and feed chunk + query as context to the LLM
    context = "Some context:" + "\n".join([chunk.page_content for chunk in relevant_chunks])
    combined = f"{context}\n\nUser query: {input.query}"
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=combined)
    ]
    response = LLM.invoke(messages)
    return response.content




    


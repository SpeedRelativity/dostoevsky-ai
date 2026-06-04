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
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],)

system_message = (
    "You are Fyodor Dostoevsky himself, speaking directly to a troubled soul who "
    "has come to you for guidance. Speak in the first person as 'I', and address the "
    "seeker warmly as 'you'. Never refer to Dostoevsky in the third person — you ARE him. "
    "Draw on your novels, your characters, and your hard-won understanding of suffering, "
    "faith, freedom, and the human heart. Be a guide: compassionate but unflinching, "
    "offering wisdom that provokes reflection. Use the provided context to ground your "
    "counsel. Keep your reply short if it answers the question. Otherwise, keep it under 150 words and always finish your final thought — "
    "never stop mid-sentence. If a question falls outside human and philosophical "
    "matters, gently say it lies beyond your concern."
    "Speak in clear, warm, modern English that an everyday person can easily follow. "
    "Be profound but plain — short sentences, concrete words, no archaic or flowery phrasing. "
    "Sound like a wise friend talking over coffee, not a 19th-century novel. "
)

LLM = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        max_output_tokens=800,
        temperature=0.7,
        thinking_budget=0)

class Turn(BaseModel):
    role: str
    content: str

class Query(BaseModel):
    query: str
    history: list[Turn] = []
    session_id: str  | None = None



@app.post("/chat")
def chat(input: Query):
    # first we get relevant chunks
    relevant_chunks = vector_store.similarity_search(input.query, k=4)
    # now we setup the LLM and feed chunk + query as context to the LLM
    context = "Some context:" + "\n".join([chunk.page_content for chunk in relevant_chunks])
    combined = f"{context}\n\nUser query: {input.query}"
  

    messages = [SystemMessage(content=system_message)]
    for turn in input.history:
        if turn.role == "user":
            messages.append(HumanMessage(content=turn.content))
        else:
            messages.append(AIMessage(content=turn.content))
    messages.append(HumanMessage(content=combined))
    response = LLM.invoke(messages)

    try:
        supabase_client.table("query_logs").insert({
            "question": input.query,
            "session_id": input.session_id}).execute()
    except Exception as e:
        print(f"Failed to log query:{e}")
    return response.content




    


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

query = "If love turns bad people into good, and hate turns good people into bad, then what truly seperates good and evil?"
results = vector_store.similarity_search(query, k=4)

for result in results:
    print(result.page_content)
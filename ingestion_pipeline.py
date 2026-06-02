import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client

from concurrent.futures import ThreadPoolExecutor, as_completed

import time


docs_path = "docs"
# load documents function
def load_documents(docs_path):
    print(f"Loading documents from {docs_path}...")
    loader = DirectoryLoader(docs_path, glob="*.txt", loader_cls=TextLoader,loader_kwargs={"encoding": "utf8", "autodetect_encoding": True}, show_progress=True)
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")
    return documents

def split__documents(documents, chunk_size=1000, chunk_overlap=150):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

def createEmbeddings(chunks, batch_size=250):
    
    # First I'll create the client.
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase_client = create_client(url, key)

    # Then I need the embedding model.
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        output_dimensionality=768,
        google_api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Finally, I can create the vector store, I need to batch though so a for loop with wait timer.
    
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size] 
        vector_store = SupabaseVectorStore.from_documents(
            documents=batch,
            embedding=embedding_model,
            client=supabase_client,
            table_name="documents",
            query_name="match_documents"
            )
        print(f"Processed batch {i//batch_size + 1} of {len(chunks)//batch_size + 1}")
        time.sleep(3)
    

        
    return vector_store


    

def main():
    print("Starting the ingestion pipeline...")
    # load documents
    documents = load_documents(docs_path)

    # chunking the files
    print("Splitting documents into chunks...")
    chunks = split__documents(documents)
    # chunks = chunks[0:50] # for testing, rate limit.

    # embedding
    print("Creating embeddings and storing in vector database...")
    embeddings = createEmbeddings(chunks)
    print("Ingestion pipeline completed.") 



if __name__ == "__main__":
    main()

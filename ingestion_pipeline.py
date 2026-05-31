import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore


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
    return chunks[0:5]

def createEmbeddings(chunks):
    embeddingModel = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", dimensions=768, api_key=os.getenv("GEMINI_API_KEY"))
    vectors = embeddingModel.embed_documents([chunk.page_content for chunk in chunks])
    # next I need to store. 
    vector_store = SupabaseVectorStore.from_vectors(vectors, chunks, table_name="documents")
    return vector_store


    

def main():
    print("Starting the ingestion pipeline...")
    # load documents
    documents = load_documents(docs_path)

    # chunking the files
    print("Splitting documents into chunks...")
    chunks = split__documents(documents)

    # embedding
    print("Creating embeddings and storing in vector database...")
    embeddings = createEmbeddings(chunks)
    print(embeddings)
    print("Ingestion pipeline completed.") 



if __name__ == "__main__":
    main()

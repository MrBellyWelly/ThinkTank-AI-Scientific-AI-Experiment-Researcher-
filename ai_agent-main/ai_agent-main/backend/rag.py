from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import logging
import os

CHROMA_PATH = "./chroma"
api_key = os.getenv('GOOGLE_API_KEY')
def create_rag(documents):
    """Create a RAG using ChromaDB."""
    logging.info(f"🧠 Creating RAG with {len(documents)} documents...")
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001", 
            google_api_key="AIzaSyBmDajvSEvV1jWn7lEke2aovQ-PTJ9-ADk"
        )
        db = Chroma.from_documents(documents, embeddings, persist_directory=CHROMA_PATH)
        db.persist()
        logging.info(f"✅ RAG created successfully at {CHROMA_PATH}")
        return db
    except Exception as e:
        logging.error(f"❌ Error creating RAG: {e}")
        raise e

def query_rag(db, query):
    """Retrieve relevant chunks from the RAG."""
    logging.info(f"🔎 Querying RAG with: {query}")
    
    try:
        results = db.similarity_search(query)
        logging.info(f"✅ Retrieved {len(results)} results from RAG")
        return [result.page_content for result in results]
    except Exception as e:
        logging.error(f"❌ Error querying RAG: {e}")
        return []

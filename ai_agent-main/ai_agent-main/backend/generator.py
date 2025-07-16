from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rag import create_rag, query_rag
from langchain.docstore.document import Document
# from utils import SAVE_DIR
import os
import pdfplumber

# Initialize Gemini model
api_key = os.getenv('GOOGLE_API_KEY')
chat_model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=api_key)

import logging

logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(file_path):
    logging.info(f"📂 Trying to open file: {file_path}")
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            logging.info(f"✅ Successfully extracted text from {file_path}")
            return text
    except Exception as e:
        logging.error(f"❌ Error extracting text from {file_path}: {e}")
        return ""

def generate_scientific_idea(query, memory):
    """Generate scientific idea using RAG and LLM."""
    from scraper import search_and_load_papers
    from langchain.docstore.document import Document
    
    # Scrape and download papers
    documents = search_and_load_papers(query)
    print("################################################################################")
    print(documents)
    print("################################################################################")
    if not documents:
        return "No relevant research papers found."

    # Documents are already text-based, no need to extract from PDFs
    docs = [Document(page_content=doc.page_content) for doc in documents if doc.page_content.strip()]
    if not docs:
        return "No valid data extracted from the papers."

    # Create RAG DB
    db = create_rag(docs)
    
    # Retrieve chunks and generate idea
    retrieved_chunks = query_rag(db, query)
    combined_chunks = "\n".join(retrieved_chunks)

     # --- 🧠 Extract previous conversation lightly ---
    previous_context = ""
    for msg in memory.chat_memory.messages:
        if msg.type == "human":
            previous_context += f"User: {msg.content}\n"
        elif msg.type == "ai":
            previous_context += f"AI: {msg.content}\n"

    # Limit context size if too large (OPTIONAL)
    previous_context = previous_context[-3000:]  # last 3000 characters

    # --- 🧠 Build the final prompt ---
    idea_prompt = f"""You are an expert scientific researcher assistant.

Below is some context from the past conversation (you can use it to better understand user's interests, but prioritize the latest query):

{previous_context}

Now, based on the following research data, generate a highly creative scientific idea and a clear experiment plan:

{combined_chunks}

User's latest request:
{query}

Please give a detailed but actionable scientific idea."""

    # idea_prompt = f"Based on the following research data, generate a scientific idea and an experiment plan:\n\n{combined_chunks}"
    try:
        idea = chat_model.invoke(idea_prompt)
    except Exception as e:
        print(f"❌ Error generating idea: {e}")
        return f"Failed to generate idea: {e}"

    print(idea.content)
    return {idea.content, retrieved_chunks}



def is_valid_scientific_idea(query):
    """Check if the idea is scientifically valid."""
    validation_prompt = f"""
    Consider the following idea for a scientific experiment:
    "{query}"
    
    Does this idea have enough scientific merit and feasibility to justify an experiment?
    Please respond with either "YES" or "NO" and a brief reason.
    """
    
    try:
        response = chat_model.invoke(validation_prompt).content.strip()
        if "YES" in response:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"❌ Error validating scientific idea: {e}")
        return False
    

def generate_general_response(user_message, memory):
    """Generate general response using LLM with chat history awareness."""
    try:
        # Build the history context
        history = ""
        for msg in memory.chat_memory.messages:
            role = "User" if msg.type == "human" else "AI"
            history += f"{role}: {msg.content}\n"

        # Now, create a context-aware prompt
        final_prompt = f"""This is the previous conversation:
        {history}

        User's latest message:
        {user_message}

        Based on the entire conversation so far, generate a helpful and relevant response as an AI assistant.
        """

        response = chat_model.invoke(final_prompt)
        return response.content
    
    except Exception as e:
        import logging
        logging.error(f"❌ Error generating response: {e}")
        return f"Failed to generate response: {e}"


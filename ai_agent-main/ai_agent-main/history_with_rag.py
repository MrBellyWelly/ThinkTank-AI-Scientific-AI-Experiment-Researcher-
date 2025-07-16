# from langchain_community.document_loaders import WebBaseLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from langchain.prompts import ChatPromptTemplate
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Initialize the LLM
# api_key = "YOUR_GOOGLE_API_KEY"
# chat_model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=api_key)

# # Load documents from the web
# loader = WebBaseLoader(
#     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",)
# )
# docs = loader.load()

# # Split documents into chunks
# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# splits = splitter.split_documents(docs)

# # Initialize embeddings and create Chroma vector store
# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
# vectorstore = Chroma.from_documents(splits, embeddings)
# retriever = vectorstore.as_retriever()

# # Define the system prompt
# system_prompt = (
#     "You are an assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer the question. "
#     "If you don't know the answer, say that you don't know. "
#     "Keep your response concise and under three sentences.\n\n{context}"
# )

# # Create a chat prompt
# chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", system_prompt),
#     ("human", "{input}")
# ])

# # Create RAG chain
# rag_chain = RetrievalQA.from_chain_type(
#     llm=chat_model,
#     retriever=retriever,
#     chain_type="stuff",
#     chain_type_kwargs={"prompt": chat_prompt}
# )

# # Invoke the chain
# def ask_question(query):
#     response = rag_chain.invoke({"query": query})
#     return response["result"]

# if __name__ == "__main__":
#     print("Starting RAG system with ChromaDB and Gemini...\n")
    
#     # First question
#     question1 = "What is Task Decomposition?"
#     answer1 = ask_question(question1)
#     print(f"Q: {question1}\nA: {answer1}\n")

#     # Follow-up question
#     question2 = "What are common ways of doing it?"
#     answer2 = ask_question(question2)
#     print(f"Q: {question2}\nA: {answer2}\n")

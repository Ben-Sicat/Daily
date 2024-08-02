import asyncio
import os
from typing import List

from dotenv import load_dotenv
from langchain.schema import Document
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_google_vertexai import (ChatVertexAI, VertexAIEmbeddings)
from src.db.CRUD.document_crud import DocumentCRUD
from langchain.schema.runnable import RunnableMap
from langchain_core.prompts import ChatPromptTemplate
from motor.motor_asyncio import AsyncIOMotorClient  # Import AsyncIOMotorClient
import logging

load_dotenv()

DB_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = "documents"
CONNECTION_STRING = os.getenv('MONGO_URL')
# Initialize Vertex AI Embeddings
embeddings = VertexAIEmbeddings(
    model="text-embedding-004", project="finquest", location="us-central1"
)

async def fetch_all_documents() -> List[Document]:
    """Fetches all documents from the specified MongoDB collection."""
    #use DocumentCRUD to get all documents
    documents = await DocumentCRUD.get_all_documents_content()
    content_list = [doc['content'] for doc in documents]
    logging.info(f"Fetched {len(content_list)} documents.")
    return content_list
async def initialize_db():
    # Fetch documents directly
    docs = await fetch_all_documents()

    # Extract content from documents and embed them
    db = DocArrayInMemorySearch.from_texts(
         docs, embeddings
    )
    return db

# Initialize Vertex AI Chat Model
gemini = ChatVertexAI(
    model="gemini-1.5-flash-001", project="finquest", location="us-central1"
)

# Create retriever (outside the async function as it depends on the awaited db)
async def main():
    db = await initialize_db()
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"score_threshold": 0.8, "k": 2}
    )
    # Define prompt template
    template = """Use the following context to answer the question. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer but mention first if you have context or no, confirm having context or no.
    Act as if you were a financial advisor. and elaborate on your answers why. Your goal is to help them be financially literate.
    
    Context: {context}

    Question: {question}
    """

    # Create Langchain chain
    prompt = ChatPromptTemplate.from_template(template)
    chain = (
        RunnableMap(
            {
                "context": lambda x: retriever.invoke(x["question"]),
                "question": lambda x: x["question"],
            }
        )
        | prompt
        | gemini
        | str  # Convert output to string
    )
    # Run the chain
    response = await chain.ainvoke({"question": "How should you save money for needs? or how should I allocate them"})
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
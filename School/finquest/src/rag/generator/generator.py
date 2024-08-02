import time
import logging
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from src import Database
from src.utils.generator import TextEmbedder
from langchain.vectorstores import DocArrayInMemorySearch
from src.db.CRUD.document_crud import DocumentCRUD
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langchain_google_vertexai import ChatVertexAI
from src.vertexai import initialize_vertex_ai
from typing import List

# Initialize logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Load environment variables
load_dotenv()

# Initialize Vertex AI
client = initialize_vertex_ai()
if not client:
    logging.error("Could not initialize Vertex AI client.")
    exit(1)

# Google VertexAI Gemini Model Initialization
gemini = ChatVertexAI(model="gemini-1.5-flash-001", project="finquest", location="us-central1")

# Database initialization
db = Database().get_database()

# Embedded data generator
embedder = TextEmbedder()

class AtlasClient:
    def __init__(self, mongo_uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(mongo_uri)
        self.database = self.client[db_name]
        self.collection_name = collection_name

    def vector_search(self, query: str, limit: int = 10) -> List[dict]:
        query = query.lower().strip()

        # Embed the query text
        t1a = time.perf_counter()
        embedded_query = embedder(query)
        t1b = time.perf_counter()
        logging.info(f"Embedding time: {t1b - t1a:.4f} seconds")

        collection = self.database[self.collection_name]

        # Placeholder for vector search
        # Replace "$vectorSearch" with your actual vector search logic or integration
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "embedding",  # Assuming the index name is "embedding"
                    "path": "embedding",  # Assuming the embedding field name is "embedding"
                    "queryVector": embedded_query,
                    "numCandidates": 50,
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "content": 1,
                    "search_score": {"$meta": "vectorSearchScore"},
                }
            },
        ])

        return list(results)

    def do_vector_search(self, query: str) -> List[dict]:
        query = query.lower().strip()

        # Embed the query text
        t1a = time.perf_counter()
        embedded_query = embedder(query)  # Get the first (and only) result
        t1b = time.perf_counter()
        logging.info(f"Embedding time: {t1b - t1a:.4f} seconds")

        # Perform the vector search
        t2a = time.perf_counter()
        collection = self.database[self.collection_name]
        results = collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "embedding", 
                    "path": "embedding",
                    "queryVector": embedded_query,
                    "numCandidates": 50,
                    "limit": 10,
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "content": 1,
                    "search_score": {"$meta": "vectorSearchScore"},
                }
            },
        ])
        t2b = time.perf_counter()
        #also add a log for the result
        logging.info(f"Vector search result: {results}")
        logging.info(f"Vector search time: {t2b - t2a:.4f} seconds")

        for result in results:
            logging.info(f"Result: {result}")
        return list(results)


if __name__ == "__main__":
    # Retrieve MongoDB URI from environment variable
    mongo_uri = os.getenv("MONGO_URL")
    if not mongo_uri:
        logging.error("MongoDB URI not found. Please set MONGO_URL in your environment variables.")
        exit(1)

    # Initialize Atlas Client
    atlas_client = AtlasClient(mongo_uri, "finquest", collection_name="documents")

    # Example query
    query = "How much should you save of your income?"

    # Perform vector search
    results = atlas_client.do_vector_search(query)


    # logging.info(f"Top Result: {results[0]}")
    # Output resultslogging.info(f"Number of results: {len(results)}")
    if len(results) > 0:
        logging.info(f"Top Result: {results[0]}")
    else:   
        logging.info("No documents found for the query.")

        
    for result in results:
        logging.info(f"Document ID: {result['_id']}, Title: {result['title']}, Score: {result['search_score']}")

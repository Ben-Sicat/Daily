from typing import Optional
from src.db.CRUD.document_crud import DocumentCRUD
from src.vertexai import initialize_vertex_ai  # Assuming this initializes Vertex AI client
from src.utils.generator import TextEmbedder as embed_text
import pymongo
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import MongoDBAtlasVectorSearch

from google.cloud import aiplatform
import asyncio
import logging
from dotenv import load_dotenv
import os
import numpy as np  # Import numpy for array operations

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def main():
    client = initialize_vertex_ai()
    if not client:
        logging.error("Could not initialize Vertex AI client.")
        exit(1)
    indexer = Indexer()
    await indexer.index_documents()

    logging.info("Indexing complete.")


class Indexer:
    def __init__(self, project: str = "finquest", location: str = "us-central1",
                 GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
        self.embedder = embed_text()
        self.project_ID = project
        self.GOOGLE_APPLICATION_CREDENTIALS = GOOGLE_APPLICATION_CREDENTIALS
        self.location = location
        aiplatform.init(project=self.project_ID, location=self.location)  # Initialize AI Platform once

    async def index_documents(self):
        """
        Retrieves documents from the database, splits them, embeds them if needed, and updates the database.
        """
        try:
            documents = await DocumentCRUD.get_all_documents()

            if not documents:
                logging.info("No documents found for indexing.")
                return

            for document in documents:
                # Check if embedding is valid (optional if document already has embedding field)
                if not document.embedding or not isinstance(document.embedding, list) or len(document.embedding) != 256 or not all(isinstance(x, (int, float)) for x in np.array(document.embedding).flatten()):
                    # Split document content using text splitter
                    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
                    docs = text_splitter.split_documents(document.content)

                    # Embed each document segment
                    embeddings = [self.embedder(doc) for doc in docs]

                    # Assuming document model dump combines content and embeddings
                    document.embedding = embeddings  # Update document embedding with list of embeddings
                    await DocumentCRUD.update_document(document.id, document.model_dump(by_alias=True))
                else:
                    logging.info(f"Document already indexed: {document.id}")

        except Exception as e:
            logging.error(f"Error indexing documents: {e}")


if __name__ == "__main__":
    asyncio.run(main())

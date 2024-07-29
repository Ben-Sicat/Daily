from pymongo import ReturnDocument
from typing import List, Dict
from src.db.models.document import Document
from src.db import Database
from bson import ObjectId
import logging

from langchain.embeddings.utils import cosine_similarity

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db = Database().get_database()

class DocumentCRUD:
    @staticmethod
    async def create_document(document_data: dict) -> Document:
        document = Document(**document_data)
        try:
            results = await db.document.insert_one(document.model_dump(by_alias=True))
            logging.info(f"Inserted document ID: {results.inserted_id}")
            return document
        except Exception as e:
            logging.error(f"Error inserting document: {e}")
            return None
    @staticmethod
    async def get_document(document_id: str) -> Document:
        try:
            document = await db.document.find_one({"_id": ObjectId(document_id)})
            if document:
                return Document(**document)
        except Exception as e:
            logging.error(f"Error getting document: {e}")
            return None
    @staticmethod
    async def update_document(document_id: str, document_data: dict) -> Document:
        try:
            document = await db.document.find_one_and_update(
                {"_id": ObjectId(document_id)},
                {"$set": document_data},
                return_document=ReturnDocument.AFTER
            )
            if document:
                return Document(**document)
            else:
                logging.info(f"Document with ID {document_id} not found")
                return None
        except Exception as e:
            logging.error(f"Error updating document: {e}")
            return None
    @ staticmethod
    async def delete_document(document_id: str) -> bool:
        try:
            result = await db.document.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count:
                logging.info(f"Document with ID {document_id} deleted")
                return True
            else:
                logging.info(f"Document with ID {document_id} not found")
                return False
        except Exception as e:
            logging.error(f"Error deleting document: {e}")
            raise e
    @staticmethod
    async def retrieve_similar_embeddings(query_embedding: List[float], k: int = 5) -> List[Dict[str, any]]:
        """Retrieve similar embeddings from the database."""
        try:
            cursor = db.document.find({}, {"_id": 1, "embedding": 1, "text": 1})
            result = []
            
            async for doc in cursor:
                #cosine similarity
                stored_embedding = doc["embedding"]
                similarity = cosine_similarity(query_embedding, stored_embedding)
                
                result.append({
                    "document_id": str(doc["_id"]),
                    "text": doc["text"],
                    "similarity": similarity
        
                })
                
            result.sort(key=lambda x: x["similarity"], reverse=True)
            return result[:k]
        
        except Exception as e:
            logging.error(f"Error retrieving similar embeddings: {e}")
            return []
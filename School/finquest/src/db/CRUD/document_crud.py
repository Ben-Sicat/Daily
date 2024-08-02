from pymongo import ReturnDocument
from src.db.models.document import Document
from src.database import Database
from src.utils.generator  import TextEmbedder
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db = Database().get_database()

class DocumentCRUD:
    @staticmethod
    async def create_document(document_data: dict) -> Document:
        document = Document(**document_data)
        try:
            embedding = TextEmbedder().embed_text(document.content)
            logging.info(f"Embedding: {embedding}") 
            print(embedding)
            #now add the embedding to the document in field embedding
            document.embedding = embedding
            results = await db.documents.insert_one(document.model_dump(by_alias=True))
            logging.info(f"Inserted document ID: {results.inserted_id}")
            return document
        except Exception as e:
            logging.error(f"Error inserting document: {e}")
            return None
    @staticmethod
    async def get_document(document_id: ObjectId) -> Document:
        try:
            document = await db.documents.find_one({"_id": ObjectId(document_id)})
            if document:
                return Document(**document)
        except Exception as e:
            logging.error(f"Error getting document: {e}")
            return None
    @staticmethod
    async def get_all_documents() -> list:
        try:
            documents = await db.documents.find().to_list(length=None)
            processed_documents = []
            for doc in documents:
                # Convert embedding to a list of lists if necessary
                embedding = doc.get('embedding', [])  # Get embedding, default to empty list
                if not isinstance(embedding, list):
                    # Handle cases where embedding is not a list
                    embedding = [embedding] if isinstance(embedding, list) else [embedding]  # Convert to list
                doc['embedding'] = embedding  # Update the document with the converted embedding
                processed_documents.append(Document(**doc))
            return processed_documents
        except Exception as e:
            logging.error(f"Error getting documents: {e}")
            return []

    @staticmethod
    async def update_document(document_id: ObjectId, document_data: dict) -> Document:
        update_data = {key: value for key, value in document_data.items() if key != "_id"}
        print(document_id)
        logging.info(f"document_id: {document_id}")
        #now we need to parse document_id to string
        # document_id = str(document_id)
        try:
            document = await db.documents.find_one_and_update(
                {"_id": document_id},
                {"$set": update_data},
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
            result = await db.documents.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count:
                logging.info(f"Document with ID {document_id} deleted")
                return True
            else:
                logging.info(f"Document with ID {document_id} not found")
                return False
        except Exception as e:
            logging.error(f"Error deleting document: {e}")
            raise e
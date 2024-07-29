from pymongo import ReturnDocument
from src.db.models.document import Document
from src.db import Database
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

db = Database().get_database()
class UsersCRUD:
    @staticmethod
    async def create_user(user_data: dict) -> Document:
        user = Document(**user_data)
        try:
            results = await db.users.insert_one(user.model_dump(by_alias=True))
            logging.info(f"Inserted user ID: {results.inserted_id}")
            return user
        except Exception as e:
            logging.error(f"Error inserting user: {e}")
            return None
    @staticmethod
    async def get_user(user_id: str) -> Document:
        try:
            user = await db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                return Document(**user)
        except Exception as e:
            logging.error(f"Error getting user: {e}")
            return None
    @staticmethod
    async def update_user(user_id: str, user_data: dict) -> Document:
        try:
            user = await db.users.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": user_data},
                return_document=ReturnDocument.AFTER
            )
            if user:
                return Document(**user)
            else:
                logging.info(f"User with ID {user_id} not found")
                return None
        except Exception as e:
            logging.error(f"Error updating user: {e}")
            return None
    @ staticmethod
    async def delete_user(user_id: str) -> bool:
        try:
            result = await db.users.delete_one({"_id": ObjectId(user_id)})
            if result.deleted_count:
                logging.info(f"User with ID {user_id} deleted")
                return True
            else:
                logging.info(f"User with ID {user_id} not found")
                return False
        except Exception as e:
            logging.error(f"Error deleting user: {e}")
            raise e
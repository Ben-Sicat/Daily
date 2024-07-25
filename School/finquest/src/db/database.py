# database connection goes here

from pymongo import MongoClient
import motor.motor_asyncio
import os

class Database:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("MONGO_URI"))
        self.db = self.client["rag_database"]
        
    def get_database(self):
        return self.db
    
    
    
db_instance = Database()
database = db_instance.get_database()
        
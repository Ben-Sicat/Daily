# src/db/test_insert.py

from src.database import Database
from src.db.models import Literature, Document, Users, Interaction

import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def insert_test_data():
    # Create database connection
    db = Database()
    database = db.get_database()

    # Test data for Literature collection
    literature_data = {
        "title": "A Study on Artificial Intelligence",
        "content": "Artificial Intelligence is rapidly evolving...",
        "url": "http://example.com/ai-study",
        "created_at": "2024-07-25",
        "updated_at": "2024-07-25"
    }

    # Convert to Pydantic model
    literature = Literature(**literature_data)

    try:
        # Insert literature data into MongoDB
        result = await database.literature.insert_one(literature.model_dump(by_alias=True))
        logging.info(f"Inserted literature document ID: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error inserting literature: {e}")

    # Test data for Document collection
    document_data = {
        "title": "Understanding Deep Learning",
        "content": "Deep Learning techniques have transformed AI...",
        "author": "John Doe",
        "created_at": "2024-07-25",
        "updated_at": "2024-07-25"
    }

    # Convert to Pydantic model
    document = Document(**document_data)

    try:
        # Insert document data into MongoDB
        result = await database.documents.insert_one(document.model_dump(by_alias=True))
        logging.info(f"Inserted document ID: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error inserting document: {e}")

    # Test data for User collection
    user_data = {
        "name": "janedoe",
        "email": "janedoe@example.com",
        "full_name": "Jane Doe",
        "password": "hashed_password_here",
    }

    # Convert to Pydantic model
    user = Users(**user_data)

    try:
        # Insert user data into MongoDB
        result = await database.users.insert_one(user.model_dump(by_alias=True))
        logging.info(f"Inserted user ID: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error inserting user: {e}")

    # Test data for Interaction collection
    interaction_data = {
        "user_id": str(user.id),
        "query": "What is AI?",
        "response": "AI stands for Artificial Intelligence...",
        "timestamp": "2024-07-25T12:00:00"
    }

    # Convert to Pydantic model
    interaction = Interaction(**interaction_data)

    try:
        # Insert interaction data into MongoDB
        result = await database.interactions.insert_one(interaction.model_dump(by_alias=True))
        logging.info(f"Inserted interaction ID: {result.inserted_id}")
    except Exception as e:
        logging.error(f"Error inserting interaction: {e}")

# Run the asynchronous test_insert function
if __name__ == "__main__":
    asyncio.run(insert_test_data())

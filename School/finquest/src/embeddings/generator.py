from google.cloud import aiplatform
from langchain_google_vertexai import VertexAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
import os
from typing import List

"""
This file will be responsible for generating embeddings for the given text data, and storing them into the database.

The generator will be responsible for the following tasks:
1. Accepting a list of text data
2. Generating embeddings for each text data
3. Storing the embeddings into the database

"""
embeddings = VertexAIEmbeddings(model="text-embedding-004", project=os.environ.get["GOOGLE_PROJECT"])
class EmbeddingGenerator:
    def __init__(self, embeddings: VertexAIEmbeddings):
        self.embeddings = embeddings
        
    def generate_embeddings(self, text_data: List[str]) -> List[float]:
        retriever = text_data.as_retriever(search_type="similarity", search_kwargs={"score_threshold": 0.8, "k":2})
        
        
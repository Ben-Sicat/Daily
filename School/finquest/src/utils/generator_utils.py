from typing import List, Optional
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextEmbedder:
    """
    A class to handle text embedding using a pre-trained Vertex AI model.
    """

    def __init__(
        self,
        model_name: str = "text-embedding-004",
        dimensionality: Optional[int] = 256,
        task: str = "RETRIEVAL_DOCUMENT"
    ):
        """
        Initialize the TextEmbedder with model configurations.

        args:
            model_name (str): The name of the embedding model to use.
            dimensionality (Optional[int]): Desired output dimensionality of embeddings.
            task (str): The task type for embeddings, default is 'RETRIEVAL_DOCUMENT'.
        """
        self.model_name = model_name
        self.dimensionality = dimensionality
        self.task = task
        self.model = TextEmbeddingModel.from_pretrained(self.model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of texts using the Vertex AI embedding model.

        args:
            texts (List[str]): A list of strings to be embedded.

        Returns:
            List[List[float]]: A list of embedding vectors.
        """
        try:
            # Prepare inputs for embedding
            inputs = [TextEmbeddingInput(text, self.task) for text in texts]
            
            # Define additional arguments based on dimensionality
            kwargs = {'output_dimensionality': self.dimensionality} if self.dimensionality else {}

            # Get embeddings from the model
            embeddings = self.model.get_embeddings(inputs, **kwargs)
            
            # Log the successful generation of embeddings
            logging.info(f"Generated embeddings for {len(texts)} texts.")
            
            return [embedding.values for embedding in embeddings]
        
        except Exception as e:
            logging.error(f"An error occurred while generating embeddings: {e}")
            raise RuntimeError(f"Failed to embed texts: {e}")

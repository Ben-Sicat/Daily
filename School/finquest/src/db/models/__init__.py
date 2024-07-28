# src/db/models/__init__.py

# This file makes 'models' a package.

# Importing individual classes for direct access
from .document import Document, PyObjectId
from .literature import Literature
from .users import Users
from .interaction import Interaction
from .embeddings import Embeddings

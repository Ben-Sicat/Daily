from beanie import Document, init_beanie, Optional, PydanticObjectId

class User_vectorized(Document):
    user_id: PydanticObjectId
    vector: listd
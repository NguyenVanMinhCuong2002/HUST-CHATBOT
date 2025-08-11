from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import os
import dotenv
dotenv.load_dotenv()


def connection_vector_db(
                endpoint: str, 
                collection_name: str = os.getenv("COLLECTION"), 
                vector_size: int = 1024):
    
    collection_name = collection_name
    client = QdrantClient(endpoint)

    # Tạo collection nếu chưa tồn tại
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created.")
    else:
        print(f"Collection '{collection_name}' already exists.")

    return client


import json
from src.connection.connect_qdrand import connection_vector_db
from qdrant_client.models import PointStruct, VectorParams, Distance
from src.connection.embedding import get_embedding_from_ollama  # Thay bằng module thật
import dotenv
import os

dotenv.load_dotenv()

class VectorDBClient:
    def __init__(self):
        self.client = connection_vector_db(endpoint=os.getenv("VECTORDB_ENDPOINT"))

    def import_data(self, documents, collection_name="general"):
        points = []
        for doc in documents:
            vector = get_embedding_from_ollama(doc["question"])
            # if not vector or len(vector) != self.client.get_collection(self.collection_name).vectors.size:
            #     print(f"Skipping doc id={doc['id']}, invalid vector size.")
            #     continue
            
            point = PointStruct(
                id=doc["id"],
                vector=vector,
                payload={
                    "question": doc["question"],
                    "solution": doc["solution"],
                    "topic": doc["topic"]
                }
            )
            points.append(point)
        
        if points:
            self.client.upsert(collection_name=collection_name, points=points)
            print(f"Upserted {len(points)} points into '{collection_name}'.")
        else:
            print("No valid points to upsert.")
    

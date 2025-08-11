import json
from src.qdrantdb.connection import connection_vector_db
from qdrant_client.models import PointStruct, VectorParams, Distance
from src.qdrantdb.embedding import get_embedding_from_ollama  # Thay bằng module thật
import dotenv
import os

dotenv.load_dotenv()

class VectorDBClient:
    def __init__(self):
        self.client = connection_vector_db(endpoint=os.getenv("VECTORDB_ENDPOINT"))

    def import_data(self, documents):
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
            self.client.upsert(collection_name=self.collection_name, points=points)
            print(f"Upserted {len(points)} points into '{self.collection_name}'.")
        else:
            print("No valid points to upsert.")

    def search(self, query ,limit=3, collection_name="general"):
        query_vector = get_embedding_from_ollama(query)


        results = self.client.search(
        collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
        )

        return str(results)


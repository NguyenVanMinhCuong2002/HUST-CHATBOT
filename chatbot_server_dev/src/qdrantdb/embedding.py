import requests
import dotenv
import os

dotenv.load_dotenv()

def get_embedding_from_ollama(text: str, model="mxbai-embed-large"):
    response = requests.post(
        os.getenv("EMBEDDING_ENDPOINT"),
        json={
            "model": model,
            "prompt": text
        }
    )

    return response.json()["embedding"]


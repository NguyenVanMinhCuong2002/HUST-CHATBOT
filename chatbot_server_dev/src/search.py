from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from src.qdrantdb.embedding import get_embedding_from_ollama
from src.qdrantdb.vector_db_client import VectorDBClient
import dotenv 
import os 
import requests

dotenv.load_dotenv()

endpoint = os.getenv("LLM_ENDPOINT")
model = os.getenv("MODEL_NAME")
headers = {
            "Content-Type": "application/json"
        }

vector_db_client = VectorDBClient()

def import_data(file):
    return

def classify_topic_with_llm(question: str) -> str:
    topics = [
        "toán Học",
        "english ",
        "vật lý",
        "hóa học"
    ]
    system_prompt = f"""
    Bạn là một trợ lý toán học. Hãy phân loại bài toán sau thành một trong các chủ đề nằm trong topic:
    {str(topics)}
    Các câu hỏi liên quan đến đạo hàm, logarit, hình học sẽ là toán học 
    Các câu hỏi chứa những từ tiếng anh sẽ là liên quan đến môn tiếng anh 
    Trả lời **chỉ tên chủ đề**, không thêm gì khác.
    """

    payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "stream": False
        }


    response = requests.post(endpoint, json=payload, headers=headers)
    print(response.json())
    return response.json()["message"]["content"].strip().lower()


def reasoning_and_search(query: str, collection_name):
    topic = classify_topic_with_llm(query)
    topics = [
        "toán học",
        "english ",
        "vật lý",
        "hóa học"
    ]
    det = f"[🔍 Topic Detected]: {topic}"

    if topic not in topics:
        # print("❌ Câu hỏi không liên quan đến toán học. Không thực hiện tìm kiếm.")
        return "không phải một câu hỏi liên quan đến các môn học" + "\t" + det

    results = vector_db_client.search(
        query=query,
        collection_name=collection_name
    )

    return results + "\t" + det


# def test_classify_topic_and_reasoning_search():
#     test_cases = [
#         ("Tính đạo hàm của hàm số y = x^2 + 3x + 2", "giải tích"),
#         ("Giải phương trình bậc hai x^2 - 4x + 4 = 0", "giải tích"),
#         ("Chào bạn, hôm nay thế nào?", "none"),  # Câu hỏi không liên quan
#     ]

#     for query, expected_topic in test_cases:
#         print(f"Testing query: {query}")
#         topic = classify_topic_with_llm(query)
#         print(f"Detected topic: {topic}")
#         assert topic == expected_topic, f"Expected topic '{expected_topic}', got '{topic}'"

#         if topic == "none":
#             results = reasoning_and_search(query)
#             assert results == [], "Expected no search results for unrelated query"
#             print("Passed: No search for unrelated query.\n")
#         else:
#             results = reasoning_and_search(query)
#             print(f"Search returned {len(results)} results.")
#             assert isinstance(results, list), "Search results should be a list"
#             print("Passed: Search executed for related topic.\n")

# if __name__ == "__main__":
#     # Khởi tạo instance vector_db của bạn ở đây
#     test_classify_topic_and_reasoning_search()

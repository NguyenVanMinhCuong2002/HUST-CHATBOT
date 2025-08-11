import streamlit as st
from qdrant_client import QdrantClient
from src.chatbot_model import llm_model
from src.search import reasoning_and_search
from src.qdrantdb.vector_db_client import VectorDBClient
import time
import random


client = QdrantClient(host="qdrant", port=6333)

collections_response = client.get_collections()
collections = [c.name for c in collections_response.collections]

if not collections:
    st.warning("⚠️ Không có collection nào trong Qdrant.")
    st.stop()

# --- Tạo selectbox để chọn ---
selected_collection = st.selectbox("📦 Chọn collection:", collections)

vector_db_client = VectorDBClient()

def response_generator(response):
    response = random.choice(
        [response]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("LamMath Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Gửi toàn bộ lịch sử (user và assistant) vào LLM
    resioning_response = reasoning_and_search(prompt, collection_name=selected_collection)
    # st.session_state.messages.append({"role": "context", "content": resioning_response})
    
    with st.chat_message("resioning"):
        st.write_stream(response_generator(resioning_response))

    st.session_state.messages.append({"role": "user", "content": prompt, "context":resioning_response})
    response = llm_model.send_messages(st.session_state.messages)
    # print(st.session_state.messages)

    # Hiển thị phản hồi từ assistant
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(response))

    # # Lưu lại tin nhắn assistant
    st.session_state.messages.append({"role": "assistant", "content": response})

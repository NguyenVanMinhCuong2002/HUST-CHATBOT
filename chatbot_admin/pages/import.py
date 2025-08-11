import streamlit as st
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid
from src.crud.crud import VectorDBClient

vector_db_client = VectorDBClient()

client = QdrantClient(host="qdrant", port=6333)

collections_response = client.get_collections()
collections = [c.name for c in collections_response.collections]

if not collections:
    st.warning("⚠️ Không có collection nào trong Qdrant.")
    st.stop()

# --- Tạo selectbox để chọn ---
selected_collection = st.selectbox("📦 Chọn collection:", collections)


uploaded_file = st.file_uploader("Chọn file dữ liệu (CSV)", type=["csv", "xlsx"])


if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("📄 Dữ liệu đã tải lên. Bạn có thể chỉnh sửa bên dưới:")

    # Cho phép chỉnh sửa dữ liệu
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    # Hiển thị nút import
    if st.button("🚀 Import vào Qdrant"):
        if edited_df.shape[1] < 2:
            st.error("❌ Dữ liệu cần có ít nhất 2 cột (1 cột ID/text, các cột vector).")
        else:
            st.success("✅ Dữ liệu đã sẵn sàng để đẩy vào Qdrant.")
            # Thêm xử lý đẩy vào Qdrant tại đây
            dict_list = edited_df.to_dict(orient="records")
            vector_db_client.import_data(dict_list, collection_name=selected_collection)

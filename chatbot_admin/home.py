import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Kết nối tới Qdrant
client = QdrantClient(host="qdrant", port=6333)

st.set_page_config(page_title="Trang chủ", page_icon="🏠")
st.title("🏠 Qdrant Collection Manager")

# --- Lấy danh sách collection ---
collections_response = client.get_collections()
collections = [c.name for c in collections_response.collections]

st.subheader("📋 Danh sách các collection hiện có:")
if collections:
    st.table(collections)
else:
    st.info("Không có collection nào hiện tại.")

# --- Tạo collection mới ---
st.subheader("➕ Thêm Collection Mới")

with st.form("create_collection_form"):
    new_collection_name = st.text_input("Tên collection mới", placeholder="vd: my_collection")
    distance_metric = st.selectbox("Khoảng cách", ["Cosine", "Euclid", "Dot"])

    submitted = st.form_submit_button("Tạo collection")
    if submitted:
        if new_collection_name.strip() == "":
            st.warning("⚠️ Vui lòng nhập tên collection.")
        elif new_collection_name in collections:
            st.warning("⚠️ Collection đã tồn tại.")
        else:
            client.create_collection(
                collection_name=new_collection_name,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance[distance_metric.upper()]
                )
            )
            st.success(f"✅ Collection `{new_collection_name}` đã được tạo.")
            st.rerun()

# --- Xoá collection ---
st.subheader("🗑️ Xoá Collection")

collection_to_delete = st.selectbox("Chọn collection cần xoá", collections, key="delete_selector")

if st.button("❌ Xoá collection"):
    try:
        client.delete_collection(collection_to_delete)
        st.success(f"✅ Đã xoá collection `{collection_to_delete}`")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Lỗi khi xoá: {e}")

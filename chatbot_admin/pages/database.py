import streamlit as st
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import PointIdsList

# Kết nối Qdrant
client = QdrantClient(host="qdrant", port=6333)

collections_response = client.get_collections()
collections = [c.name for c in collections_response.collections]

if not collections:
    st.warning("⚠️ Không có collection nào trong Qdrant.")
    st.stop()

# --- Tạo selectbox để chọn ---
selected_collection = st.selectbox("📦 Chọn collection:", collections)


st.title("📊 Xem và Chỉnh sửa điểm trong Qdrant")

# Hàm lấy dữ liệu
def fetch_all_points(collection_name, batch_size=500):
    all_data = []
    offset = None

    while True:
        points, offset = client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            with_payload=True,
            with_vectors=True,
            offset=offset
        )
        for point in points:
            data = {
                "id": point.id,
                "vector": point.vector,
                **point.payload
            }
            all_data.append(data)

        if offset is None:
            break

    return pd.DataFrame(all_data)

# Lấy dữ liệu
df = fetch_all_points(selected_collection)

# Hiển thị bảng có thể chỉnh sửa
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# Nút lưu thay đổi
if st.button("💾 Lưu thay đổi vào Qdrant"):
    # Chuyển các dòng trong dataframe thành list of PointStruct
    try:
        points = []
        for _, row in edited_df.iterrows():
            # Đảm bảo "vector" là list float (trường hợp bị đọc sai thành chuỗi)
            vector = row["vector"]
            if isinstance(vector, str):
                import ast
                vector = ast.literal_eval(vector)

            # Bỏ các trường không phải payload (id, vector)
            payload = row.drop(["id", "vector"]).to_dict()

            points.append(
                PointStruct(
                    id=row["id"],
                    vector=vector,
                    payload=payload
                )
            )

        # Upsert lại vào Qdrant
        client.upsert(collection_name=selected_collection, points=points)
        st.success("✅ Dữ liệu đã được cập nhật vào Qdrant!")

    except Exception as e:
        st.error(f"❌ Lỗi khi lưu dữ liệu: {e}")



st.subheader("🗑️ Xoá point theo ID")

delete_id = st.text_input("Nhập ID của point cần xoá")

if st.button("❌ Xoá point"):
    if delete_id:

        # Tự động chuyển sang int nếu có thể
        point_id = int(delete_id) if delete_id.isdigit() else delete_id

        client.delete(
            collection_name=selected_collection,
            points_selector=PointIdsList(points=[point_id])
        )
        st.success(f"✅ Đã xoá point có ID = {point_id}")
        st.rerun()

    else:
        st.warning("⚠️ Vui lòng nhập ID trước khi xoá.")
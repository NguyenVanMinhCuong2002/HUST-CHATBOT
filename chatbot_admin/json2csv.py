import json 
import pandas as pd

file_path="/home/luke/PythonProjects/chatbot_admin/data.json"

with open(file=file_path) as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Xuất ra file CSV
df.to_csv("cau_hoi_toan.csv", index=False, encoding="utf-8-sig")

print("✅ Đã lưu dữ liệu thành 'cau_hoi_toan.csv'")
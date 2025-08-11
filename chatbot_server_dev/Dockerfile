FROM python:3.10

# Cài gói hệ thống cần thiết (ví dụ curl hoặc bash nếu cần)
RUN apt-get update && apt-get install -y bash && rm -rf /var/lib/apt/lists/*

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép requirements và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn và script khởi chạy
COPY . .

EXPOSE 8502

# Chạy script khởi động
CMD ["sh","run.sh"]

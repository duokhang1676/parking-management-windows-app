# Bước 1: Sử dụng image cơ bản từ Docker Hub (Python 3.9)
FROM python:3.9-slim

# Bước 2: Đặt thư mục làm việc trong container
WORKDIR /app

# Bước 3: Sao chép tệp requirements.txt vào container
COPY requirements.txt /app/

# Bước 4: Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Bước 5: Sao chép toàn bộ mã nguồn của ứng dụng vào container
COPY . /app/

# Bước 6: Xác định lệnh chạy khi container khởi động
CMD ["python", "main.py"]

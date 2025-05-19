smart_parking_management_system/
├── main.py                     # File chính khởi chạy ứng dụng
├── resources/
│   ├── icons/
│   ├── coordinates/            # Hàm generage tọa độ 
│   ├── license_plate_recognition/  # Nhận dạng biển số xe
│   ├── mp3/                    
│   ├── models/                 # Model yolo
│   └── print_bill/             # Hàm in hóa đơn
├── modules/
│   ├── page1_thread_classes.py # Các luồng xử lý của page1
│   ├── page1.py                # Trang chính
│   ├── page2.py                # Module quản lý hóa đơn 
│   ├── page3.py                # Module quản lý xe trong bãi
│   ├── page4.py                # Module quản lý khách hàng
│   ├── page5.py                # Modele setup tọa độ
│   └── utils.py                # Các hàm tiện ích
├── database/
├── test.py
├── dockerfile
├── requirements.txt            # Thư viện python
└── README.md                   # Tài liệu hướng dẫn sử dụng và triển khai

tạo file requirements
pip freeze > requirements.txt

Xây dựng Docker Image
docker build -t my-python-app .

Chạy Docker Container
docker run -it -p 5000:5000 my-python-app



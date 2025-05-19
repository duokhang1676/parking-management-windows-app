from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDateEdit, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont
from pymongo import MongoClient
from PyQt5.QtCore import Qt, QDate
from datetime import datetime, timedelta

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)

        # Kết nối tới MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["server_local"]
        self.collection = self.db["History"]

        # Top layout
        main_layout = QVBoxLayout()

        # Search and Date Selector
        search_date_layout = QHBoxLayout()

        # Date picker
        self.date_picker = QDateEdit()
        self.date_picker.setDisplayFormat("yyyy-MM-dd")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setStyleSheet("padding: 5px; font-size: 14px;")
        self.date_picker.setDate(QDate.currentDate())
        search_date_layout.addWidget(self.date_picker)

        # Search bar
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search by License...")
        self.search_field.setStyleSheet("padding: 5px; font-size: 14px;")
        search_date_layout.addWidget(self.search_field)

        main_layout.addLayout(search_date_layout)

        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["License Plate", "Time In", "Time Out", "Parking Time", "Customer Type"])

        # Adjust font
        font = QFont()
        font.setPointSize(14)  # Tăng kích thước font
        self.table_widget.setFont(font)

        # Adjust header font
        header_font = QFont()
        header_font.setPointSize(16)  # Font chữ lớn hơn cho header
        self.table_widget.horizontalHeader().setFont(header_font)

        # Adjust table layout
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Cột tự động giãn
        self.table_widget.horizontalHeader().setStretchLastSection(True)  # Cột cuối chiếm hết phần dư
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setRowCount(0)  # Ban đầu không có dữ liệu

        # Ensure the table expands to fill available space and scrollbars appear
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set size policy
        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show vertical scrollbar
        self.table_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Always show horizontal scrollbar

        # Prevent editing
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing

        # Add table to the main layout
        main_layout.addWidget(self.table_widget)

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setStyleSheet("font-size: 14px; padding: 5px;")
        self.refresh_button.clicked.connect(self.refresh_table)  # Connect refresh button to function
        main_layout.addWidget(self.refresh_button)

        layout.addLayout(main_layout)
        self.setLayout(layout)

        # Bind F5 key to refresh the table
        self.setFocusPolicy(Qt.StrongFocus)
        self.keyPressEvent = self.handle_key_press

        # Connect search field and date picker to search function
        self.search_field.returnPressed.connect(self.search_data)
  
        self.refresh_table()

    def refresh_table(self):
        """Refresh the data from MongoDB and update the table."""
        # Clear existing data in the table
        self.table_widget.setRowCount(0)

        # Retrieve data from MongoDB collection
        data = self.collection.find().sort("time_out", -1)

        # Populate the table with data from MongoDB
        for row, record in enumerate(data):
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(record.get("license", "")))
            time_in_str = record.get("time_in","").strftime('%Y-%m-%d %H:%M:%S')
            self.table_widget.setItem(row, 1, QTableWidgetItem(time_in_str))
            time_out_str = record.get("time_out","").strftime('%Y-%m-%d %H:%M:%S')
            self.table_widget.setItem(row, 2, QTableWidgetItem(time_out_str))
            self.table_widget.setItem(row, 3, QTableWidgetItem(record.get("parking_time", "")))
            self.table_widget.setItem(row, 4, QTableWidgetItem(record.get("customer_type", "")))

    def search_data(self):
        """Search the data based on the selected date and license."""
        # Clear existing data in the table
        self.table_widget.setRowCount(0)

        # Get the selected date from date picker
        selected_date = self.date_picker.date().toString("yyyy-MM-dd")
        
        # Get the search query from search field
        search_query = self.search_field.text().strip()

       # Chuyển đổi selected_date thành một đối tượng datetime
        date_object = datetime.strptime(selected_date, "%Y-%m-%d")

        # Tạo ISODate cho MongoDB (đặt giờ là 00:00:00)
        start_of_day = datetime(date_object.year, date_object.month, date_object.day)

        # Tạo đối tượng end_of_day (23:59:59) của ngày đã chọn
        end_of_day = start_of_day + timedelta(days=1)  # Cộng thêm 1 ngày để lấy ngày hôm sau

        # Thực hiện truy vấn
        data = self.collection.find({
            "license": search_query,
            "time_out": {
                "$gte": start_of_day,  # Tìm tài liệu có time_out lớn hơn hoặc bằng 00:00:00 của ngày đã chọn
                "$lt": end_of_day  # Tìm tài liệu có time_out nhỏ hơn 00:00:00 của ngày hôm sau
            }
        }).sort("time_out", -1)
        # Populate the table with filtered data
        for row, record in enumerate(data):
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(record.get("license", "")))
            time_in_str = record.get("time_in","").strftime('%Y-%m-%d %H:%M:%S')
            self.table_widget.setItem(row, 1, QTableWidgetItem(time_in_str))
            time_out_str = record.get("time_out","").strftime('%Y-%m-%d %H:%M:%S')
            self.table_widget.setItem(row, 2, QTableWidgetItem(time_out_str))
            self.table_widget.setItem(row, 3, QTableWidgetItem(record.get("parking_time", "")))
            self.table_widget.setItem(row, 4, QTableWidgetItem(record.get("customer_type", "")))

    def handle_key_press(self, event):
        """Handle key press events, specifically F5 for refresh."""
        if event.key() == Qt.Key_F5:
            self.refresh_table()  # Refresh table when F5 is pressed

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
from modules.page1 import ParkingSlotPage 
from modules.page2 import HistoryPage
from modules.page3 import CarsInParkingPage
from modules.page4 import CustomersPage
from modules.page5 import CoordinatesSetup
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart parking management system")
        self.setGeometry(100, 100, 900, 600)

        # Root container
        root_widget = QWidget()
        root_layout = QVBoxLayout(root_widget)

        # Header
        header = QLabel("✨ Hệ thống quản lý đỗ xe thông minh ✨")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            background-color: #4CAF50;
            color: white;
            padding: 15px;
            font-size: 24px;
            font-weight: bold;
        """)
        root_layout.addWidget(header)

        # Horizontal Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        root_layout.addWidget(divider)

        def create_menu_button(text, icon_path):
            btn = QPushButton(text)
            btn.setIcon(QIcon(icon_path))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f0f0f0;
                    font-size: 16px;
                    padding: 10px;
                    border: none;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #c8e6c9;
                }
            """)
            # self.menu_buttons.append(btn)
            return btn

        # Menu
        menu_bar = QHBoxLayout()
          # Buttons with Icons
        btn_page1 = create_menu_button("Home", "resources/icons/page1.png")
        btn_page2 = create_menu_button("History", "resources/icons/page2.png")
        btn_page3 = create_menu_button("Car In Parking", "resources/icons/page3.png")
        btn_page4 = create_menu_button("Customer", "resources/icons/page4.png")
        btn_page5 = create_menu_button("Setup", "resources/icons/page5.png")

        menu_bar.addWidget(btn_page1)
        menu_bar.addWidget(btn_page2)
        menu_bar.addWidget(btn_page3)
        menu_bar.addWidget(btn_page4)
        menu_bar.addWidget(btn_page5)
        menu_bar.addStretch()
        root_layout.addLayout(menu_bar)

        # Content Area
        self.content_area = QStackedWidget()
        root_layout.addWidget(self.content_area)

        # Footer
        footer = QLabel("© 2024 - My Cool App. All rights reserved.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("background-color: #333; color: white; padding: 10px; font-size: 14px;")
        root_layout.addWidget(footer)

        # Adding Pages
        self.page1 = ParkingSlotPage()

        self.page2 = HistoryPage()

        self.page3 = CarsInParkingPage()

        self.page4 = CustomersPage()

        self.page5 = CoordinatesSetup()

        self.content_area.addWidget(self.page1)
        self.content_area.addWidget(self.page2)
        self.content_area.addWidget(self.page3)
        self.content_area.addWidget(self.page4)
        self.content_area.addWidget(self.page5)

        # Connect buttons to change pages
        btn_page1.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page1))
        btn_page2.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page2))
        btn_page3.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page3))
        btn_page4.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page4))
        btn_page5.clicked.connect(lambda: self.content_area.setCurrentWidget(self.page5))

        self.setCentralWidget(root_widget)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

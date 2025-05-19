from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QListWidget, QLabel, QStackedWidget, QFrame
from PyQt5.QtCore import Qt
import sys
import cv2
import os
import glob
from PyQt5.QtGui import QImage, QPixmap, QFont
from resources.coordinates.coordinates_generator import CoordinatesGenerator
from resources.coordinates.coordinates_generator_auto import CoordinatesGeneratorAuto
from resources.coordinates.coordinates_generator_forFirst import CoordinatesGeneratorForFirst
from modules.utils import *
import re

class CoordinatesSetup(QWidget):
    def __init__(self):
        super().__init__()
        self.ClOUD_SERVER_URL = 'https://parking-cloud-server.onrender.com/api/'
        self.PARKING_ID = 'parking_001'
        self.image = None
        self.camera_id = None
        self.curentCam = None
        self.setWindowTitle("Cài đặt tọa độ các ô đỗ")
        self.setGeometry(100, 100, 900, 600)

        # Main Layout
        main_layout = QVBoxLayout(self)

        # Top Layout with Left and Right sections
        top_layout = QHBoxLayout()

        # Left side: List of cameras (QListWidget)
        self.camera_list = QListWidget()
        self.camera_list.addItem("Camera 0")
        self.camera_list.addItem("Camera 1")
        self.camera_list.addItem("Camera 2")
        self.camera_list.addItem("Camera 3")
        self.camera_list.addItem("Camera 4")
        self.camera_list.addItem("Camera 5")
        self.camera_list.addItem("Camera 6")
        

        # Set font for QListWidget items (increase font size)
        font = QFont()
        font.setPointSize(12)  # Increase font size here (14 is an example)
        self.camera_list.setFont(font)
        
        # Add the list widget to the left side
        top_layout.addWidget(self.camera_list)

        # Right side: Display camera content (QLabel)
        self.camera_display = QLabel("Select a camera from the list")
        self.camera_display.setAlignment(Qt.AlignCenter)
        self.camera_display.setFixedSize(1500, 750)  # Fixed size for displaying camera feed

        # Add the QLabel for camera feed to the right side
        top_layout.addWidget(self.camera_display)

        # Add top layout to the main layout
        main_layout.addLayout(top_layout)

        # Bottom: Control buttons (1, 2, 3, etc.)
        self.bottom_buttons_layout = QHBoxLayout()
        btn_Reload = QPushButton("Tải lại danh sách camera")
        btn_Reload.setFixedHeight(40)
        font.setPointSize(10)
        btn_Reload.setFont(font)

        btn_Update = QPushButton("Cập nhật vị trí ô đỗ")
        btn_Update.setFixedHeight(40)
        btn_Update.setFont(font)

        btn_AutoCoordinate = QPushButton("Tự động gán vị trí ô đỗ")
        btn_AutoCoordinate.setFixedHeight(40)
        btn_AutoCoordinate.setFont(font)

        self.bottom_buttons_layout.addWidget(btn_Reload)
        self.bottom_buttons_layout.addWidget(btn_Update)
        self.bottom_buttons_layout.addWidget(btn_AutoCoordinate)

        # Add bottom buttons layout to main layout
        main_layout.addLayout(self.bottom_buttons_layout)

        # Connect the camera list selection to show the camera feed
        self.camera_list.currentItemChanged.connect(self.display_camera)
        self.camera_list.itemClicked.connect(self.display_camera2)
        btn_Reload.clicked.connect(lambda: self.on_btnReload_click())
        btn_Update.clicked.connect(lambda: self.on_btnUpdate_click(self.image))
        btn_AutoCoordinate.clicked.connect(lambda: self.on_btnAutoCoordinate_click(self.image))

    def on_btnAutoCoordinate_click(self,image):
        if image is None:
            show_message(self,"Hãy chọn 1 camera để cập nhật vị trí!")
            return
        numbers = re.findall(r'\d+', self.curentCam)
        data_file = "resources/coordinates/data/"+self.camera_id+".yml"
            # Mở tệp để ghi tọa độ vào
        with open(data_file, "w+") as points:
            # Khởi tạo đối tượng CoordinatesGenerator với hình ảnh và màu sắc
            try:
                generator = CoordinatesGeneratorAuto(image, points)
            # Gọi phương thức generate để tạo tọa độ
                generator.generate()
                points.flush()
                os.fsync(points.fileno())
                show_message(self,"Hãy nhập các vị trí ô đỗ đầu tiên của hàng!")
                # cập nhật lại camerafeed
                self.update_video_feed(self.curentCam)
            except Exception as e:
                return 
        coordinates_data = read_yaml(data_file)
        with open(data_file, "a+") as points:
            # Khởi tạo đối tượng CoordinatesGenerator với hình ảnh và màu sắc
            try:
                generator = CoordinatesGeneratorForFirst(image, points, (0, 0, 255),numbers[0], coordinates_data)
            # Gọi phương thức generate để tạo tọa độ
                generator.generate()

                points.flush()
                os.fsync(points.fileno())

                show_message(self,"Cập nhật thành công")
                # Gửi tọa độ lên server
                coordinates_data = read_yaml(data_file)
                if self.send_coordinates(self.camera_id, coordinates_data):
                    print("Coordinates sent successfully")
                # cập nhật lại camerafeed
                self.update_video_feed(self.curentCam)

            except Exception as e:
                return 
            
    def on_btnReload_click(self):
        url = f'{self.ClOUD_SERVER_URL+"coordinates/"+self.PARKING_ID}'
        response = requests.get(url)
        if response.status_code == 200:
            for file_path in glob.glob(os.path.join("resources/coordinates/data/frame", "*")):
                os.remove(file_path)
            print("Tải lại danh sách camera thành công")
            for i in response.json():
                img_url = i['image_url']
                response = requests.get(img_url)
                if response.status_code == 200:
                    with open("resources/coordinates/data/frame/"+str(i['camera_id'])+".jpg", 'wb') as file:
                        file.write(response.content)
                else:
                    print(f'Error downloading image: {response.status_code} - {response.text}')
            
            

    def on_btnUpdate_click(self,image):
        if image is None:
            show_message(self,"Hãy chọn 1 camera để cập nhật vị trí!")
            return
        numbers = re.findall(r'\d+', self.curentCam)
        data_file = "resources/coordinates/data/"+self.camera_id+".yml"
            # Mở tệp để ghi tọa độ vào
        coordinates_data = read_yaml(data_file)
        with open(data_file, "a+") as points:
            # Khởi tạo đối tượng CoordinatesGenerator với hình ảnh và màu sắc
            try:
                generator = CoordinatesGenerator(image, points, (0, 0, 255),numbers[0], coordinates_data)
            # Gọi phương thức generate để tạo tọa độ
                generator.generate()

                points.flush()
                os.fsync(points.fileno())

                show_message(self,"Cập nhật thành công")
                # Gửi tọa độ lên server
                coordinates_data = read_yaml(data_file)
                if self.send_coordinates(self.camera_id, coordinates_data):
                    print("Coordinates sent successfully")
                # cập nhật lại camerafeed
                self.update_video_feed(self.curentCam)

            except Exception as e:
                return 
            
    def send_coordinates(self, camera_id, coordinates_data):
        print("Sending coordinates to server...")
        url = f'{self.ClOUD_SERVER_URL+"coordinates/"+self.PARKING_ID+"/"+camera_id}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data[0]['coordinates_list'] = coordinates_data
            url = f'{self.ClOUD_SERVER_URL+"coordinates/"}update/{self.PARKING_ID}/{camera_id}'
            response = requests.put(url, json=data[0])
            return response.status_code == 200

    def display_camera(self, current, previous):
        """ Simulate showing camera feed. In real app, replace with code that connects to actual cameras. """
        camera_name = current.text()  # Get the selected camera name from the list
        self.curentCam = camera_name
        self.update_video_feed(camera_name)

    def display_camera2(self, current):
        """ Simulate showing camera feed. In real app, replace with code that connects to actual cameras. """
        camera_name = current.text()  # Get the selected camera name from the list
        self.curentCam = camera_name
        self.update_video_feed(camera_name)

    def update_video_feed(self, camera_name):
        path = 'resources/coordinates/data/frame/'
        files = os.listdir(path)
        cam_id = int(re.search(r'\d+', camera_name).group(0))
        if cam_id < len(files):
            self.camera_id = os.path.splitext(files[cam_id])[0]
            frame = cv2.imread(path+files[cam_id])
            if frame is None:
                show_message(self,"Không đọc được ảnh")
                return
            self.image = frame.copy()
            # Resize the frame to fit the QLabel
            # frame = cv2.resize(frame, (1200, 700))

            frame = self.drawCoordinates(frame)
            height, width, channels = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(q_img)
            self.camera_display.setPixmap(pixmap)
            
        else:   
                self.image = None
                self.camera_id = None
                self.camera_display.setText("No camera feed available")

    def drawCoordinates(self,frame):
        data_file = "resources/coordinates/data/"+self.camera_id+".yml"
        coordinates_data = read_yaml(data_file)
        
        if coordinates_data is None or (isinstance(coordinates_data, (dict, list)) and len(coordinates_data) == 0):
            return frame
        
        for item in coordinates_data:
            coord = item['coordinate']
            x, y = coord
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Dấu chấm màu xanh lá
            # Vẽ ID gần dấu chấm
            cv2.putText(frame, str(item['id']), (x - 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)  # ID màu đỏ
        return frame
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoordinatesSetup()
    window.show()
    sys.exit(app.exec_())

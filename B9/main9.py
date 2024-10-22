import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QComboBox, QSlider
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class EdgeDetectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng Tách Biên Ảnh")
        self.resize(1200, 600)  # Điều chỉnh kích thước cửa sổ lớn hơn
        self.image = None  # Ảnh gốc
        self.threshold1 = 100  # Giá trị ngưỡng 1 mặc định cho bộ lọc Canny
        self.threshold2 = 200  # Giá trị ngưỡng 2 mặc định cho bộ lọc Canny

        # Layout chính
        self.main_layout = QVBoxLayout()

        # Tạo layout ngang cho ảnh gốc và ảnh đã qua xử lý
        self.image_layout = QHBoxLayout()

        # Nhãn hiển thị ảnh gốc
        self.original_label = QLabel("Ảnh gốc")
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setFixedSize(600, 400)  # Điều chỉnh kích thước nhãn lớn hơn
        self.image_layout.addWidget(self.original_label)
        
        # Nhãn hiển thị ảnh sau khi tách biên
        self.edge_label = QLabel("Ảnh đã tách biên")
        self.edge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edge_label.setFixedSize(600, 400)  # Điều chỉnh kích thước nhãn lớn hơn
        self.image_layout.addWidget(self.edge_label)

        # Thêm layout ảnh vào layout chính
        self.main_layout.addLayout(self.image_layout)
        
        # Nút chọn ảnh
        self.btn_select_image = QPushButton("Chọn ảnh")
        self.btn_select_image.clicked.connect(self.load_image)
        self.main_layout.addWidget(self.btn_select_image)
        
        # Thêm thanh trượt để điều chỉnh threshold1 cho Canny
        self.threshold1_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold1_slider.setMinimum(1)
        self.threshold1_slider.setMaximum(255)
        self.threshold1_slider.setValue(self.threshold1)
        self.threshold1_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.threshold1_slider.setTickInterval(25)
        self.threshold1_slider.valueChanged.connect(self.update_threshold1)
        self.main_layout.addWidget(self.threshold1_slider)

        # Thêm thanh trượt để điều chỉnh threshold2 cho Canny
        self.threshold2_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold2_slider.setMinimum(1)
        self.threshold2_slider.setMaximum(255)
        self.threshold2_slider.setValue(self.threshold2)
        self.threshold2_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.threshold2_slider.setTickInterval(25)
        self.threshold2_slider.valueChanged.connect(self.update_threshold2)
        self.main_layout.addWidget(self.threshold2_slider)

        # Đặt layout chính cho cửa sổ
        self.setLayout(self.main_layout)
    
    def load_image(self):
        # Chọn file ảnh từ máy tính
        image_path, _ = QFileDialog.getOpenFileName(self, "Chọn hình ảnh", "", "Image Files (*.png *.jpg *.bmp)")
        if image_path:
            self.image = cv2.imread("z5931215272978_e5bb5d81a84dd1e3cafa734491193219.jpg", cv2.IMREAD_GRAYSCALE)  # Đọc ảnh dưới dạng grayscale
            self.display_image(self.image, self.original_label)
            self.apply_edge_detection()  # Áp dụng tách biên ngay khi chọn ảnh
    
    def display_image(self, img, label):
        # Chuyển đổi ảnh từ OpenCV (Grayscale) sang QImage
        height, width = img.shape
        bytes_per_line = width
        qimg = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio))  # Điều chỉnh kích thước ảnh để vừa với nhãn

    def update_threshold1(self):
        # Cập nhật giá trị threshold1 khi thanh trượt thay đổi
        self.threshold1 = self.threshold1_slider.value()
        self.apply_edge_detection()

    def update_threshold2(self):
        # Cập nhật giá trị threshold2 khi thanh trượt thay đổi
        self.threshold2 = self.threshold2_slider.value()
        self.apply_edge_detection()

    def apply_edge_detection(self):
        if self.image is None:
            return
        
        # Áp dụng thuật toán Canny với hai ngưỡng threshold1 và threshold2
        edges = cv2.Canny(self.image, self.threshold1, self.threshold2)
        
        # Hiển thị ảnh đã tách biên
        self.display_image(edges, self.edge_label)

# Khởi chạy ứng dụng
app = QApplication(sys.argv)
window = EdgeDetectionApp()
window.show()
sys.exit(app.exec())

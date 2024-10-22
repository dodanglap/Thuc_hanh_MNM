import sys
import math
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import numpy as np

class GeometryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Học Hình Học")

        # Combo box to choose shape
        self.shape_select = QComboBox()
        self.shape_select.addItems(["Tam giác", "Tròn", "Vuông", "Hình hộp chữ nhật", "Hình trụ", "Hình cầu"])
        self.shape_select.currentIndexChanged.connect(self.update_input_fields)

        # Input fields
        self.input_fields_layout = QVBoxLayout()
        self.inputs = {}

        self.init_input_fields()  # Khởi tạo ô nhập cho tất cả các hình

        # Result label
        self.result_label = QLabel("Kết quả: ")

        # Buttons
        self.calculate_button = QPushButton("Tính diện tích")
        self.draw_button = QPushButton("Vẽ")
        self.calculate_button.clicked.connect(self.calculate_area)
        self.draw_button.clicked.connect(self.draw_shape)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.shape_select)
        layout.addLayout(self.input_fields_layout)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.draw_button)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 300)
        self.show()

    def init_input_fields(self):
        # Ô nhập cho hình tam giác
        self.inputs["Tam giác"] = {
            "Đáy": QLineEdit(),
            "Chiều cao": QLineEdit(),
        }
        
        # Ô nhập cho hình tròn
        self.inputs["Tròn"] = {
            "Bán kính": QLineEdit(),
        }
        
        # Ô nhập cho hình vuông
        self.inputs["Vuông"] = {
            "Cạnh": QLineEdit(),
        }
        
        # Ô nhập cho hình hộp chữ nhật
        self.inputs["Hình hộp chữ nhật"] = {
            "Chiều dài": QLineEdit(),
            "Chiều rộng": QLineEdit(),
            "Chiều cao": QLineEdit(),
        }
        
        # Ô nhập cho hình trụ
        self.inputs["Hình trụ"] = {
            "Bán kính": QLineEdit(),
            "Chiều cao": QLineEdit(),
        }
        
        # Ô nhập cho hình cầu
        self.inputs["Hình cầu"] = {
            "Bán kính": QLineEdit(),
        }

        # Thêm các ô nhập vào layout
        for shape in self.inputs:
            for key, input_field in self.inputs[shape].items():
                self.input_fields_layout.addWidget(QLabel(key))
                self.input_fields_layout.addWidget(input_field)
        
        self.update_input_fields()  # Ẩn ô nhập không cần thiết ban đầu

    def update_input_fields(self):
        # Ẩn tất cả ô nhập và chỉ hiển thị ô nhập tương ứng với hình đã chọn
        for shape, fields in self.inputs.items():
            for input_field in fields.values():
                input_field.setVisible(shape == self.shape_select.currentText())

    def calculate_area(self):
        shape = self.shape_select.currentText()
        try:
            if shape == "Tam giác":
                base = float(self.inputs["Tam giác"]["Đáy"].text())
                height = float(self.inputs["Tam giác"]["Chiều cao"].text())
                area = 0.5 * base * height
            elif shape == "Tròn":
                radius = float(self.inputs["Tròn"]["Bán kính"].text())
                area = math.pi * (radius ** 2)
            elif shape == "Vuông":
                side = float(self.inputs["Vuông"]["Cạnh"].text())
                area = side ** 2
            elif shape == "Hình hộp chữ nhật":
                length = float(self.inputs["Hình hộp chữ nhật"]["Chiều dài"].text())
                width = float(self.inputs["Hình hộp chữ nhật"]["Chiều rộng"].text())
                height = float(self.inputs["Hình hộp chữ nhật"]["Chiều cao"].text())
                area = 2 * (length * width + length * height + width * height)
            elif shape == "Hình trụ":
                radius = float(self.inputs["Hình trụ"]["Bán kính"].text())
                height = float(self.inputs["Hình trụ"]["Chiều cao"].text())
                area = 2 * math.pi * radius * (radius + height)
            elif shape == "Hình cầu":
                radius = float(self.inputs["Hình cầu"]["Bán kính"].text())
                area = 4 * math.pi * (radius ** 2)
            else:
                area = 0
            
            self.result_label.setText(f"Kết quả: {area:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập giá trị hợp lệ!")

    def draw_shape(self):
        shape = self.shape_select.currentText()
        if shape == "Tam giác":
            self.draw_triangle()
        elif shape == "Tròn":
            self.draw_circle()
        elif shape == "Vuông":
            self.draw_square()
        elif shape == "Hình hộp chữ nhật":
            self.draw_rectangular_prism()
        elif shape == "Hình trụ":
            self.draw_cylinder()
        elif shape == "Hình cầu":
            self.draw_sphere()

    def draw_triangle(self):
        base = float(self.inputs["Tam giác"]["Đáy"].text())
        height = float(self.inputs["Tam giác"]["Chiều cao"].text())
        points = np.array([[0, 0], [base, 0], [base / 2, height]])
        
        plt.figure()
        plt.fill(points[:, 0], points[:, 1], 'b', alpha=0.5)
        plt.xlim(-1, base + 1)
        plt.ylim(-1, height + 1)
        plt.title("Tam giác")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()

    def draw_circle(self):
        radius = float(self.inputs["Tròn"]["Bán kính"].text())
        theta = np.linspace(0, 2 * np.pi, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        plt.figure()
        plt.fill(x, y, 'r', alpha=0.5)
        plt.xlim(-radius - 1, radius + 1)
        plt.ylim(-radius - 1, radius + 1)
        plt.title("Hình tròn")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()

    def draw_square(self):
        side = float(self.inputs["Vuông"]["Cạnh"].text())
        points = np.array([[0, 0], [side, 0], [side, side], [0, side]])
        
        plt.figure()
        plt.fill(points[:, 0], points[:, 1], 'g', alpha=0.5)
        plt.xlim(-1, side + 1)
        plt.ylim(-1, side + 1)
        plt.title("Hình vuông")
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid()
        plt.show()

    def draw_rectangular_prism(self):
        length = float(self.inputs["Hình hộp chữ nhật"]["Chiều dài"].text())
        width = float(self.inputs["Hình hộp chữ nhật"]["Chiều rộng"].text())
        height = float(self.inputs["Hình hộp chữ nhật"]["Chiều cao"].text())

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        # Tạo các đỉnh của hình hộp
        x = [0, length, length, 0, 0, length, length, 0]
        y = [0, 0, width, width, 0, 0, width, width]
        z = [0, 0, 0, 0, height, height, height, height]
        
        # Vẽ các cạnh
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # Mặt đáy
            [4, 5], [5, 6], [6, 7], [7, 4],  # Mặt trên
            [0, 4], [1, 5], [2, 6], [3, 7]   # Các cạnh bên
        ]
        
        for edge in edges:
            ax.plot3D(*zip(*[(x[edge[0]], y[edge[0]], z[edge[0]]), (x[edge[1]], y[edge[1]], z[edge[1]])]), color='b')

        ax.set_title("Hình hộp chữ nhật")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()


    def draw_cylinder(self):
        radius = float(self.inputs["Hình trụ"]["Bán kính"].text())
        height = float(self.inputs["Hình trụ"]["Chiều cao"].text())
        z = np.linspace(0, height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(np.array([x]*100), np.array([y]*100), z[:, None], color='r', alpha=0.5)
        ax.set_title("Hình trụ")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    def draw_sphere(self):
        radius = float(self.inputs["Hình cầu"]["Bán kính"].text())
        phi = np.linspace(0, np.pi, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        x = radius * np.outer(np.sin(phi), np.cos(theta))
        y = radius * np.outer(np.sin(phi), np.sin(theta))
        z = radius * np.outer(np.cos(phi), np.ones(np.size(theta)))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, color='b', alpha=0.5)
        ax.set_title("Hình cầu")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GeometryApp()
    sys.exit(app.exec())

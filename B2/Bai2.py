import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QComboBox, QDialog, QFileDialog, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QSpinBox)
from sympy import symbols, diff, integrate, sympify

class GiaiTichApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phần mềm hỗ trợ học tập môn Giải tích")
        
        # Khởi tạo các biến lưu trữ hệ số và kết quả
        self.coefficients = []
        self.result = None

        # ComboBox để lựa chọn bài toán: Đạo hàm, Nguyên hàm, Tích phân
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Chọn bài toán", "Đạo hàm", "Nguyên hàm", "Tích phân"])

        # SpinBox để người dùng chọn số bậc của phương trình
        self.degree_input = QSpinBox()
        self.degree_input.setRange(1, 10)  # Giới hạn bậc từ 1 đến 10
        self.degree_input.setValue(4)  # Mặc định là bậc 4
        self.degree_input.valueChanged.connect(self.update_table)  # Cập nhật bảng khi thay đổi bậc

        # Bảng nhập hệ số đa thức
        self.table_widget = QTableWidget(1, 5)  # Mặc định 5 cột cho đa thức bậc 4
        self.table_widget.setHorizontalHeaderLabels(['Hệ số a', 'Hệ số b', 'Hệ số c', 'Hệ số d', 'Hằng số'])

        # Thêm ô nhập cho cận trên và cận dưới
        self.lower_limit_input = QLineEdit()  # Cận dưới
        self.lower_limit_input.setPlaceholderText("Cận dưới")
        self.upper_limit_input = QLineEdit()  # Cận trên
        self.upper_limit_input.setPlaceholderText("Cận trên")
        
        # Nút tính toán
        self.calc_button = QPushButton("Tính toán")
        self.calc_button.clicked.connect(self.calculate)

        # Nút tải CSV
        self.load_csv_button = QPushButton("Tải file CSV")
        self.load_csv_button.clicked.connect(self.load_csv)

        # Nút lưu CSV
        self.save_csv_button = QPushButton("Lưu kết quả ra CSV")
        self.save_csv_button.clicked.connect(self.save_csv)

        # Hiển thị kết quả
        self.result_label = QLabel("Kết quả: ")

        # Layout tổng thể
        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        
        # Layout cho nhập số bậc
        degree_layout = QHBoxLayout()
        degree_layout.addWidget(QLabel("Nhập số bậc:"))
        degree_layout.addWidget(self.degree_input)
        layout.addLayout(degree_layout)

        layout.addWidget(self.table_widget)

        # Layout cho cận trên và cận dưới
        limit_layout = QHBoxLayout()
        limit_layout.addWidget(self.lower_limit_input)
        limit_layout.addWidget(self.upper_limit_input)
        layout.addLayout(limit_layout)

        layout.addWidget(self.calc_button)
        layout.addWidget(self.result_label)
        
        # Layout cho các nút thao tác
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_csv_button)
        button_layout.addWidget(self.save_csv_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def update_table(self):
        """Cập nhật bảng hệ số dựa trên số bậc được chọn."""
        degree = self.degree_input.value()
        self.table_widget.setColumnCount(degree + 1)  # Số cột = số bậc + 1 cho hằng số
        header_labels = [f"Hệ số {chr(97 + i)}" for i in range(degree)] + ["Hằng số"]
        self.table_widget.setHorizontalHeaderLabels(header_labels)

    def load_csv(self):
        """Load hệ số từ file CSV."""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load CSV', '', 'CSV Files (*.csv)')
        if file_path:
            try:
                data = pd.read_csv(file_path)
                self.degree_input.setValue(data.shape[1] - 1)  # Cập nhật số bậc dựa trên số cột
                self.table_widget.setRowCount(data.shape[0])
                self.table_widget.setColumnCount(data.shape[1])
                for i in range(data.shape[0]):
                    for j in range(data.shape[1]):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(data.iloc[i, j])))
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Không thể tải file CSV: {e}")

    def save_csv(self):
        """Lưu kết quả và tham số ra file CSV."""
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save CSV', '', 'CSV Files (*.csv)')
        if file_path:
            try:
                row_count = self.table_widget.rowCount()
                col_count = self.table_widget.columnCount()
                data = []
                for i in range(row_count):
                    row_data = []
                    for j in range(col_count):
                        item = self.table_widget.item(i, j)
                        row_data.append(item.text() if item else "")
                    data.append(row_data)
                
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False, header=False)
                
                QMessageBox.information(self, "Thành công", "Lưu file CSV thành công!")
            except Exception as e:
                QMessageBox.warning(self, "Lỗi", f"Không thể lưu file CSV: {e}")

    def calculate(self):
        """Tính toán đạo hàm, nguyên hàm hoặc tích phân."""
        x = symbols('x')
        try:
            # Lấy hệ số từ bảng nhập
            degree = self.degree_input.value()
            row_data = []
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(0, col)
                row_data.append(float(item.text()) if item else 0)

            # Tạo đa thức theo bậc: ax^n + bx^(n-1) + ... + hằng số
            poly_expr = " + ".join([f"{row_data[i]}*x**{degree-i}" for i in range(degree)] + [str(row_data[-1])])
            poly = sympify(poly_expr)

            # Tùy chọn bài toán
            choice = self.combo_box.currentText()
            if choice == "Đạo hàm":
                self.result = diff(poly, x)
            elif choice == "Nguyên hàm":
                self.result = integrate(poly, x)
            elif choice == "Tích phân":
                lower_limit = float(self.lower_limit_input.text())
                upper_limit = float(self.upper_limit_input.text())
                self.result = integrate(poly, (x, lower_limit, upper_limit))

            self.result_label.setText(f"Kết quả: {self.result}")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể tính toán: {e}")


# Khởi tạo ứng dụng
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GiaiTichApp()
    window.show()
    sys.exit(app.exec())

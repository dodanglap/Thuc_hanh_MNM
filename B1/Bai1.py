import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QGridLayout, QHBoxLayout, QSpinBox, QFileDialog, QMessageBox
)
import numpy as np
import pandas as pd

class LinearSystemSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.layout = QVBoxLayout()

        # Nhập số phương trình (n)
        self.num_equations_label = QLabel('Enter number of equations (n):', self)
        self.layout.addWidget(self.num_equations_label)
        
        self.num_equations_input = QSpinBox(self)
        self.num_equations_input.setMinimum(2)  # Ít nhất 2 phương trình
        self.layout.addWidget(self.num_equations_input)
        
        # Nút để tạo các ô nhập hệ số
        self.generate_btn = QPushButton('Generate Coefficients Input', self)
        self.generate_btn.clicked.connect(self.generate_inputs)
        self.layout.addWidget(self.generate_btn)

        # Nút để tải file CSV
        self.load_csv_btn = QPushButton('Load CSV', self)
        self.load_csv_btn.clicked.connect(self.load_from_csv)
        self.layout.addWidget(self.load_csv_btn)

        # Khu vực để chứa các ô nhập hệ số và giá trị vế phải
        self.coefficients_layout = QGridLayout()
        self.layout.addLayout(self.coefficients_layout)
        
        # Nút giải hệ phương trình
        self.solve_btn = QPushButton('Solve System', self)
        self.solve_btn.clicked.connect(self.solve_system)
        self.layout.addWidget(self.solve_btn)
        
        # Hiển thị kết quả
        self.result_label = QLabel('Result:', self)
        self.layout.addWidget(self.result_label)
        
        # Nút để lưu kết quả ra CSV
        self.save_btn = QPushButton('Save Result to CSV', self)
        self.save_btn.clicked.connect(self.save_to_csv)
        self.layout.addWidget(self.save_btn)
        
        self.setLayout(self.layout)
        self.setWindowTitle('Linear System Solver')

    def generate_inputs(self):
        """Tạo các ô nhập hệ số dựa trên số phương trình n."""
        # Xóa các ô nhập liệu trước đó
        for i in reversed(range(self.coefficients_layout.count())): 
            widget = self.coefficients_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Lấy số phương trình
        num_equations = self.num_equations_input.value()

        # Tạo các ô nhập liệu cho hệ số và giá trị vế phải
        self.coefficient_inputs = []
        for i in range(num_equations):
            row_inputs = []
            for j in range(num_equations):
                coef_input = QLineEdit(self)
                self.coefficients_layout.addWidget(coef_input, i, j)
                row_inputs.append(coef_input)
            # Ô nhập cho vế phải (hằng số)
            constant_input = QLineEdit(self)
            self.coefficients_layout.addWidget(constant_input, i, num_equations)
            row_inputs.append(constant_input)
            self.coefficient_inputs.append(row_inputs)

    def solve_system(self):
        """Giải hệ phương trình và hiển thị kết quả."""
        try:
            coefficients, constants = self.get_coefficients_and_constants()
            result = self.solve_linear_system(coefficients, constants)
            if result is not None:
                self.result_label.setText(f'Result: {result}')
            else:
                self.result_label.setText('No solution or infinite solutions.')
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")
    
    def get_coefficients_and_constants(self):
        """Lấy các hệ số và hằng số từ các ô nhập."""
        num_equations = self.num_equations_input.value()
        coefficients = []
        constants = []
        for i in range(num_equations):
            row = []
            for j in range(num_equations):
                value = float(self.coefficient_inputs[i][j].text())
                row.append(value)
            coefficients.append(row)
            constants.append(float(self.coefficient_inputs[i][-1].text()))
        return np.array(coefficients), np.array(constants)
    
    def solve_linear_system(self, coefficients, constants):
        """Giải hệ phương trình tuyến tính."""
        try:
            result = np.linalg.solve(coefficients, constants)
            return result
        except np.linalg.LinAlgError:
            return None
    
    def save_to_csv(self):
        """Lưu hệ phương trình và kết quả ra file CSV."""
        try:
            coefficients, constants = self.get_coefficients_and_constants()
            result = self.solve_linear_system(coefficients, constants)
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save CSV', '', 'CSV Files (*.csv)')
            if file_path:
                data = pd.DataFrame(coefficients)
                data['Constants'] = constants
                if result is not None:
                    data['Solution'] = result
                else:
                    data['Solution'] = "No solution"
                data.to_csv(file_path, index=False)
                QMessageBox.information(self, "Success", "Data saved successfully.")
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")

    def load_from_csv(self):
        """Tải hệ phương trình từ file CSV và điền vào giao diện."""
        file_path, _ = QFileDialog.getOpenFileName(self, 'Load CSV', '', 'CSV Files (*.csv)')
        if file_path:
            try:
                data = pd.read_csv(file_path)
                print(data)
                num_equations = len(data)  # Số phương trình = số hàng
                self.num_equations_input.setValue(num_equations)
                self.generate_inputs()

                # Điền các hệ số vào ô nhập
                for i in range(0, num_equations):
                    for j in range(num_equations+1):
                        self.coefficient_inputs[i][j].setText(str(data.iloc[i, j]))
                        print(str(data.iloc[i, j]))
            except Exception as e:
                QMessageBox.warning(self, "File Error", f"Error loading file: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    solver = LinearSystemSolver()
    solver.show()
    sys.exit(app.exec())

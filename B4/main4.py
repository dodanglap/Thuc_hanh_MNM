import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QLineEdit, QDialog, QLabel, QMessageBox
import matplotlib.pyplot as plt
class CourseReportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chương trình Báo cáo Học phần")
        self.setGeometry(200, 100, 1000, 600)

        # Khởi tạo các thành phần
        self.table_widget = QTableWidget()
        self.import_button = QPushButton("Nhập CSV")
        self.export_button = QPushButton("Xuất CSV")
        self.add_class_button = QPushButton("Thêm Lớp")
        self.delete_class_button = QPushButton("Xóa Lớp")
        self.analyze_button = QPushButton("Phân tích Điểm")

        # Thiết lập layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.add_class_button)
        button_layout.addWidget(self.delete_class_button)
        button_layout.addWidget(self.analyze_button)

        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Kết nối các sự kiện nút
        self.import_button.clicked.connect(self.import_csv)
        self.export_button.clicked.connect(self.export_csv)
        self.add_class_button.clicked.connect(self.add_class)
        self.delete_class_button.clicked.connect(self.delete_class)
        self.analyze_button.clicked.connect(self.analyze_grades)
    def import_csv(self):
        # Xóa biến options và gọi getOpenFileName trực tiếp
        file_path, _ = QFileDialog.getOpenFileName(self, "Nhập CSV", "", "CSV Files (*.csv)")
        if file_path:
            df = pd.read_csv(file_path)
            self.load_data(df)

    def export_csv(self):
        # Xóa biến options và gọi getSaveFileName trực tiếp
        file_path, _ = QFileDialog.getSaveFileName(self, "Xuất CSV", "", "CSV Files (*.csv)")
        if file_path:
            df = self.get_data()
            df.to_csv(file_path, index=False)

    def add_class(self):
        dialog = AddClassDialog(self)
        if dialog.exec():
            new_class_data = dialog.get_class_data()
            current_row_count = self.table_widget.rowCount()
            
            # Thêm lớp mới và cập nhật STT
            self.table_widget.insertRow(current_row_count)
            for col, value in enumerate(new_class_data[1:], start=1):  # Bỏ qua STT ở đây
                self.table_widget.setItem(current_row_count, col, QTableWidgetItem(value))
            
            self.update_stt()  # Cập nhật lại cột STT

    def delete_class(self):
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            self.table_widget.removeRow(selected_row)
            self.update_stt()  # Cập nhật lại cột STT
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn lớp để xóa")

    def update_stt(self):
        # Cập nhật STT cho tất cả các hàng
        row_count = self.table_widget.rowCount()
        for row in range(row_count):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(row + 1)))

    def load_data(self, df):
        self.table_widget.setRowCount(df.shape[0])
        self.table_widget.setColumnCount(df.shape[1])
        self.table_widget.setHorizontalHeaderLabels(df.columns)
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iat[row, col]))
                self.table_widget.setItem(row, col, item)

    def get_data(self):
        row_count = self.table_widget.rowCount()
        col_count = self.table_widget.columnCount()
        data = []
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.table_widget.item(row, col)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        df = pd.DataFrame(data, columns=[self.table_widget.horizontalHeaderItem(i).text() for i in range(col_count)])
        return df
    
    def analyze_grades(self):
        selected_row = self.table_widget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một lớp để phân tích")
            return

        # Lấy dữ liệu điểm cho lớp được chọn
        grade_labels = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]
        grade_counts = [
            int(self.table_widget.item(selected_row, 3).text()),
            int(self.table_widget.item(selected_row, 4).text()),
            int(self.table_widget.item(selected_row, 5).text()),
            int(self.table_widget.item(selected_row, 6).text()),
            int(self.table_widget.item(selected_row, 7).text()),
            int(self.table_widget.item(selected_row, 8).text()),
            int(self.table_widget.item(selected_row, 9).text()),
            int(self.table_widget.item(selected_row, 10).text()),
            int(self.table_widget.item(selected_row, 11).text())
        ]

        # Kiểm tra dữ liệu có hợp lệ không
        if sum(grade_counts) == 0:
            QMessageBox.warning(self, "Lỗi", "Không có dữ liệu điểm để phân tích")
            return

        # Tạo biểu đồ hình tròn
        plt.figure(figsize=(8, 6))
        plt.pie(grade_counts, labels=grade_labels, autopct='%1.1f%%', startangle=140)
        plt.title("Phân tích Điểm Lớp " + self.table_widget.item(selected_row, 1).text())
        plt.axis('equal')  # Đảm bảo biểu đồ tròn hoàn chỉnh
        plt.show()


class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Lớp Học")
        self.layout = QVBoxLayout(self)

        self.fields = [
            "STT", "Mã lớp", "Số SV", "Loại A+", "Loại A", "Loại B+", "Loại B", "Loại C+", "Loại C",
            "Loại D+", "Loại D", "Loại F", "L1", "L2", "TX1", "TX2", "Cuối kỳ"
        ]
        self.inputs = {}

        for field in self.fields:
            label = QLabel(field)
            line_edit = QLineEdit()
            self.inputs[field] = line_edit
            self.layout.addWidget(label)
            self.layout.addWidget(line_edit)

        self.add_button = QPushButton("Thêm")
        self.add_button.clicked.connect(self.accept)
        self.layout.addWidget(self.add_button)

    def get_class_data(self):
        return [self.inputs[field].text() for field in self.fields]

# Khởi chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CourseReportApp()
    window.show()
    sys.exit(app.exec())

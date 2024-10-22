import csv

def create_csv(filename):
    # Dữ liệu hệ số (các phương trình tuyến tính)
    data = [
        [2, 3, 5],   # Phương trình: 2x + 3y = 5
        [4, -6, 10], # Phương trình: 4x - 6y = 10
        # Có thể thêm nhiều phương trình hơn
    ]

    # Ghi dữ liệu vào file CSV
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Ghi từng hàng hệ số vào file CSV
        writer.writerows(data)

    print(f'File CSV "{filename}" đã được tạo thành công.')

# Tạo file CSV với tên "he_phuong_trinh.csv"
create_csv('he_phuong_trinh.csv')

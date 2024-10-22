import cv2
import numpy as np

# Hàm cập nhật ảnh khi thanh trượt thay đổi
def update_filter(val):
    # Lấy giá trị từ thanh trượt
    kernel_value = val / 100.0  # Chuyển đổi giá trị từ 0-100 thành 0.0-1.0
    # Tạo kernel cho bộ lọc identity
    kernel_identity = np.array([[0, 0, 0], [0, kernel_value, 0], [0, 0, 0]])

    # Tạo kernel sắc nét
    kernel_sharpen = np.array([[0, -1, 0],
                                [-1, 5, -1],
                                [0, -1, 0]])

    # Áp dụng bộ lọc identity
    output_identity = cv2.filter2D(img, -1, kernel_identity)
    
    # Áp dụng bộ lọc sắc nét
    output_sharpened = cv2.filter2D(output_identity, -1, kernel_sharpen)

    # Hiển thị ảnh đã được lọc
    cv2.imshow('Filtered Image', output_sharpened)

# Đọc ảnh
img = cv2.imread('B9/z5931215272978_e5bb5d81a84dd1e3cafa734491193219.jpg')
cv2.imshow('Original', img)

# Tạo cửa sổ hiển thị
cv2.namedWindow('Filtered Image')

# Thiết lập thanh trượt để điều chỉnh giá trị kernel
cv2.createTrackbar('Kernel Value', 'Filtered Image', 100, 100, update_filter)

# Gọi hàm update_filter ban đầu để hiển thị ảnh với giá trị mặc định
update_filter(100)

# Chờ người dùng nhấn phím
cv2.waitKey(0)
cv2.destroyAllWindows()

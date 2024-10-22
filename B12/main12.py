import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu từ file CSV
data = pd.read_csv('B12/Student_Performance.csv')

# Xem trước dữ liệu
print("Dữ liệu đầu vào:")
print(data.head())

# Tìm max, min, trung bình cho từng cột
print("\nGiá trị lớn nhất (Max):")
print(data.max())

print("\nGiá trị nhỏ nhất (Min):")
print(data.min())

print("\nGiá trị trung bình (Mean):")
print(data.mean())

# Vẽ biểu đồ phân bố cho từng biến
plt.figure(figsize=(15, 10))

# Biểu đồ phân bố số giờ học
plt.subplot(2, 3, 1)
sns.histplot(data['Hours Studied'], kde=True, color='blue')
plt.title('Phân bố số giờ học')

# Biểu đồ phân bố điểm số trước đó
plt.subplot(2, 3, 2)
sns.histplot(data['Previous Scores'], kde=True, color='green')
plt.title('Phân bố điểm số trước đó')

# Biểu đồ phân bố hoạt động ngoại khóa
plt.subplot(2, 3, 3)
sns.histplot(data['Extracurricular Activities'], kde=True, color='orange')
plt.title('Phân bố hoạt động ngoại khóa')

# Biểu đồ phân bố giờ ngủ
plt.subplot(2, 3, 4)
sns.histplot(data['Sleep Hours'], kde=True, color='purple')
plt.title('Phân bố số giờ ngủ')

# Biểu đồ phân bố số bài kiểm tra mẫu đã làm
plt.subplot(2, 3, 5)
sns.histplot(data['Sample Question Papers Practiced'], kde=True, color='red')
plt.title('Phân bố số bài kiểm tra mẫu')

# Biểu đồ phân bố chỉ số hiệu suất
plt.subplot(2, 3, 6)
sns.histplot(data['Performance Index'], kde=True, color='brown')
plt.title('Phân bố chỉ số hiệu suất')

plt.tight_layout()
plt.show()

# Vẽ biểu đồ tương quan giữa các biến
plt.figure(figsize=(10, 6))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Ma trận tương quan giữa các biến')
plt.show()

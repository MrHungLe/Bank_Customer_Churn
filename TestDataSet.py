import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 1. Đọc file và xóa các cột rác
df = pd.read_csv(r"C:\AI project\demo\AI project\Customer-Churn-Records.csv")
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# 2. FIX LỖI Ở ĐÂY: Tự động tìm tất cả các cột chứa CHỮ (object)
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
print(f"Các cột chứa chữ đã được tìm thấy và tự động mã hóa: {categorical_cols}")

# Dùng One-Hot Encoding cho toàn bộ các cột chữ đó
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# 3. Tách Features (X) và Target (y)
X = df.drop('Exited', axis=1) 
y = df['Exited']              

# 4. Chia tập Train/Test (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Chuẩn hóa dữ liệu (Scaling)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 6. Huấn luyện mô hình Random Forest
model = RandomForestClassifier(random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

# 7. Làm bài thi và in Báo cáo
y_pred = model.predict(X_test_scaled)
print("\n--- BÁO CÁO KẾT QUẢ MÔ HÌNH ---")
print(classification_report(y_test, y_pred))



# 8. Lưu "bộ não" mô hình và "thước đo" chuẩn hóa
joblib.dump(model, 'rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Cực kỳ quan trọng: Lưu lại danh sách các cột để API biết đường xếp đúng thứ tự
joblib.dump(X.columns.tolist(), 'model_columns.pkl')

print("Đã xuất thành công 3 file .pkl ra thư mục dự án!")
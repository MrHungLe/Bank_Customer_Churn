import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv(r"C:\AI project\demo\AI project\Customer-Churn-Records.csv")
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
print(f"Các cột chứa chữ đã được tìm thấy và tự động mã hóa: {categorical_cols}")
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

X = df.drop('Exited', axis=1) 
y = df['Exited']              
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = RandomForestClassifier(random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print("\n--- BÁO CÁO KẾT QUẢ MÔ HÌNH ---")
print(classification_report(y_test, y_pred))

joblib.dump(model, 'rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(X.columns.tolist(), 'model_columns.pkl')

print("Đã xuất thành công 3 file .pkl ra thư mục dự án!")

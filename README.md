# 🏦 Bank Customer Churn Prediction System

Dự án xây dựng hệ thống dự đoán khả năng rời bỏ dịch vụ của khách hàng ngân hàng. Hệ thống sử dụng mô hình Machine Learning kết hợp với API (FastAPI) để dự đoán thời gian thực và lưu trữ lịch sử vào cơ sở dữ liệu MySQL.

## 🚀 Tính năng chính
- **Machine Learning**: Sử dụng thuật toán Random Forest Classifier để dự đoán tỉ lệ rời bỏ.
- **Data Pipeline**: Quy trình tiền xử lý dữ liệu tự động (Encoding & Scaling) đảm bảo tính nhất quán giữa lúc huấn luyện và dự đoán.
- **RESTful API**: Cung cấp Endpoint `/predict` để nhận dữ liệu khách hàng và trả về kết quả ngay lập tức.
- **Database Integration**: Tự động lưu trữ mọi yêu cầu dự đoán và kết quả của AI vào MySQL để phục vụ mục đích hậu kiểm và phân tích.

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ**: Python 3.13
- **Framework API**: FastAPI, Uvicorn
- **AI/ML Library**: Scikit-learn, Pandas, Joblib
- **Database**: MySQL (Sử dụng `mysql-connector-python`)
- **Quản lý môi trường**: Pip & Requirements.txt

## 📂 Cấu trúc thư mục
- `main.py`: File thực thi chính chứa API logic và kết nối Database.
- `rf_model.pkl`: Mô hình Random Forest đã được huấn luyện.
- `scaler.pkl`: Bộ chuẩn hóa dữ liệu để đảm bảo các con số (Balance, Salary) về đúng định dạng.
- `model_columns.pkl`: Danh sách các đặc trưng (features) để đảm bảo đầu vào luôn khớp với mô hình.
- `requirements.txt`: Danh sách các thư viện cần thiết.

## ⚙️ Hướng dẫn cài đặt và chạy

1. **Clone dự án**:
   ```bash
   git clone <link-github-cua-ban>
   cd "AI project"
2. Cài đặt thư viện:
    pip install -r requirements.txt
3. Database:
    Tạo database churn_prediction_db trong MySQL.
    Chạy lệnh SQL trong file (hoặc tạo bảng prediction_history theo cấu trúc tương ứng).
    Cập nhật mật khẩu MySQL của bạn trong file main.py.
4. Khởi chạy Server:
    uvicorn main:app --reload
5. Sử dụng:
    Truy cập http://127.0.0.1:8000/docs để thử nghiệm trực tiếp trên giao diện Swagger UI.
6. Kết quả mẫu:
    {
  "churn_prediction": "Yes",
  "probability": "99.0%"
    }
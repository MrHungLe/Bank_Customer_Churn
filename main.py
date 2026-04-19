import pandas as pd
import joblib
import mysql.connector
from fastapi import FastAPI
from pydantic import BaseModel
import os

# 1. Load các file bảo bối
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "rf_model.pkl"))
model_columns = joblib.load(os.path.join(BASE_DIR, "model_columns.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

app = FastAPI(title="Bank Churn Prediction API")

# 2. ĐỊNH NGHĨA LẠI CHURNINPUT (Sửa lỗi NameError)
class ChurnInput(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float
    Complain: int
    Satisfaction_Score: int 
    Card_Type: str
    Point_Earned: int

# 3. Hàm lưu Database (Giữ nguyên logic của bạn)
def save_to_mysql(data_dict, prediction, probability):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mật khẩu của bạn(không phải của tôi)", # Thay mật khẩu của bạn vào đây
            database="churn_prediction_db"
        )
        cursor = conn.cursor()
        sql = """INSERT INTO prediction_history 
                 (credit_score, geography, gender, age, tenure, balance, num_of_products, 
                  has_cr_card, is_active_member, estimated_salary, complain, 
                  satisfaction_score, card_type, point_earned, churn_prediction, probability) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        values = (
            data_dict['CreditScore'], data_dict['Geography'], data_dict['Gender'], data_dict['Age'],
            data_dict['Tenure'], data_dict['Balance'], data_dict['NumOfProducts'],
            data_dict['HasCrCard'], data_dict['IsActiveMember'], data_dict['EstimatedSalary'],
            data_dict['Complain'], data_dict['Satisfaction_Score'], data_dict['Card_Type'],
            data_dict['Point_Earned'], prediction, probability
        )
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database Error: {e}")

@app.post("/predict")
def predict(data: ChurnInput):
    # A. CHUYỂN DỮ LIỆU THÀNH DATAFRAME
    # Lưu lại bản gốc để lưu vào DB sau này
    original_data = data.dict()
    input_df = pd.DataFrame([original_data])
    
    # B. XỬ LÝ DỮ LIỆU CHỮ
    # 1. Đổi tên cột Satisfaction_Score -> Satisfaction Score (cho giống lúc train)
    input_df = input_df.rename(columns={
        "Satisfaction_Score": "Satisfaction Score",
        "Card_Type": "Card Type",
        "Point_Earned": "Point Earned"
    })
    
    # 2. One-Hot Encoding tự động
    input_df_encoded = pd.get_dummies(input_df)
    
    # 3. Reindex để khớp với 100% các cột AI đã học (Dùng model_columns.pkl)
    final_df = input_df_encoded.reindex(columns=model_columns, fill_value=0)
    
    # 4. Chuẩn hóa số liệu (Dùng scaler.pkl)
    final_df_scaled = scaler.transform(final_df)
    
    # C. DỰ ĐOÁN
    prediction = model.predict(final_df_scaled)[0]
    probability = model.predict_proba(final_df_scaled)[0][1]
    
    res_text = "Yes" if prediction == 1 else "No"
    prob_text = f"{probability*100:.1f}%"
    
    # D. LƯU VÀO MYSQL
    save_to_mysql(original_data, res_text, prob_text)
    
    return {
        "churn_prediction": res_text,
        "probability": prob_text
    }

import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()  # Tải biến môi trường từ file .env

app = Flask(__name__)

# --- CẤU HÌNH API GROQ (MIỄN PHÍ) ---
# Đăng ký tại: https://console.groq.com để lấy API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"  

def get_ai_response(prompt):
    """
    Gửi prompt đến Groq API và trả về câu trả lời.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi Groq API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Chi tiết lỗi: {e.response.text}")
        return "Xin lỗi, tôi không thể kết nối với dịch vụ AI ngay lúc này. Vui lòng kiểm tra API key tại https://console.groq.com"


# --- ROUTE XỬ LÝ GIAO DIỆN CHÍNH ---
@app.route('/')
def home():
    """Render trang HTML chính của chatbot."""
    return render_template('index.html')


# --- ROUTE XỬ LÝ YÊU CẦU CHAT ---
@app.route('/chat', methods=['POST'])
def chat():
    """Nhận câu hỏi từ người dùng và trả về câu trả lời của AI."""
    # Lấy dữ liệu JSON được gửi từ frontend
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"answer": "Vui lòng nhập câu hỏi của bạn."})

    # Lấy câu trả lời từ AI
    ai_response = get_ai_response(user_message)

    # Trả về câu trả lời dưới dạng JSON
    return jsonify({"answer": ai_response})


if __name__ == '__main__':
    # Chạy ứng dụng Flask
    # Đặt debug=True để tự động tải lại khi bạn thay đổi mã
    app.run(debug=True)
# 🍔 Chatbot tư vấn ẩm thực khi du lịch Đà Nẵng

Dự án chatbot AI được xây dựng bằng framework Rasa, hỗ trợ người dùng đặt câu hỏi và nhận câu trả lời tự động về ẩm thực Đà Nẵng (ví dụ: món ăn, địa chỉ món ăn,...).

## Dưới đây là toàn bộ hướng dẫn để set up project trên localhost
## Cấu trúc project (localhost)
Đây là cấu trúc thư mục cơ bản của Rasa project trên localhost, các file khác của mình trong github chỉ là mình add vào để phục vụ việc deploy lên VPS thôi. Mọi người có thể xóa các file đó và giữ nguyên structure như bên dưới cũng được 😊 

```bash
chatbot_rasa_n8n/
├── data/                 # Dữ liệu huấn luyện chatbot (intents, stories, rules)
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
│
├── actions/              # Tập tin custom actions
│   └── actions.py
│
├── models/               # Mô hình được train
│
├── domain.yml            # Định nghĩa intents, entities, responses,...
├── config.yml            # Cấu hình pipeline, policies
├── credentials.yml       # Cấu hình kênh tích hợp
├── endpoints.yml         # Địa chỉ server actions
```

## Yêu cầu hệ thống
- Python 3.8+
- pip
- Rasa CLI (`pip install rasa`)

## Run chatbot trên localhost

### Clone project

```bash
git clone https://github.com/quochuy43/chatbot_rasa_n8n.git
cd chatbot_rasa_n8n
```

### Cấu hình
- Tạo và active môi trường ảo venv: <br>
```bash
python -m venv venv
venv/bin/activate
```
- Cài đặt thư viện Rasa:
```bash
pip install rasa
```
- Sửa action_endpoint trong endpoints.yml lại thành
```bash
action_endpoint:
  url: "http://localhost:5055/webhook"
```

### Hướng dẫn sử dụng
- Train chatbot
```bash
rasa train
```
- Chạy chatbot thử trong terminal
```bash
rasa shell
```
- Chạy API server + actions
```bash
# Terminal 1
rasa run actions

# Terminal 2
rasa run --enable-api
```

### Tích hợp Postman (Test API)
- Endpoint: POST http://localhost:5005/webhooks/rest/webhook
- Body:
```bash
{
  "sender": "test_user",
  "message": "Đà Nẵng có món gì ngon"
}
```
- Expected Output:
```bash
[
    {
        "recipient_id": "test_user",
        "text": "Bánh Canh Ruộng - Đặc Sản Đà Nẵng Bình Dân; Mì Quảng - Món Ăn Đà Nẵng Nổi Tiếng Bốn Phương; Bánh Tráng Cuốn Thịt Heo - Đậm Đà Hương Vị Đà Nẵng; Bánh Tráng Kẹp - Món Ăn Vặt Nổi tiếng Đà Nẵng; Bánh Bèo - Món Ăn Xế Thơm Ngon Ở Đà Nẵng; Bánh Nậm Đà Nẵng - Món Ăn Sáng Thơm Ngon Ở Đà Nẵng; Bánh Bột Lọc Đà Nẵng; \nBạn muốn biết thêm thông tin chi tiết về món nào? Hãy nhắn tên món ăn để mình giới thiệu nhé!"
    }
]
```

---
## Vậy là đã xong 1 endpoint. 
### Ta có thể tích hợp vào web, app cá nhân hoặc build 1 workflow automation, sử dụng endpoint rasa làm HTTP Request Node như mình vậy nè: 
![Screenshot 2025-05-11 110444](https://github.com/user-attachments/assets/e2622893-a4ed-4ee1-bdcb-8585568c75e6)


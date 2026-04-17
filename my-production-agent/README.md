# my-production-agent

AI Agent được containerize dựa trên các nguyên tắc ứng dụng 12-factor cho Production hoàn chỉnh.

## Tính năng (Features)
- **FastAPI Core**: Nền tảng framework nhanh gọn, tối giản.
- **Docker Multi-stage Builds**: Tối ưu hóa dung lượng image ở mức siêu nhẹ.
- **Security Check**: Tích hợp lớp xác thực người dùng bằng API Key.
- **Redis Load Balance**: Triển khai Rate Limit (10req/min) và Cost Guarding chặn chi phi vượt quá ngân sách.
- **Graceful Shutdown Integration**: Có sẵn các endpoint Liveness và readiness phục vụ Health Check báo cáo tình trạng lên Cloud.

## Cài đặt từ đầu
Môi trường yêu cầu: **Docker** & **Docker Compose**

Chạy Docker-compose:
```bash
docker compose up --scale agent=3 -d
```
> Việc này sẽ khởi chạy 3 backend của FastApi AI Agent, 1 Nginx HTTP proxy reverse, cùng Redis phục vụ Load Balancing.

## Cài đặt môi trường Production trên Cloud
Dự án được cấu hình sẵn để triển khai dễ dàng lên **Render** (như trong bài lab).

1. Push toàn bộ source code này lên một repository GitHub (Public).
2. Tạo tài khoản trên [Render.com](https://render.com) và chọn **New > Web Service**.
3. Liên kết với kho GitHub của bạn. Render sẽ tự động nhận diện `Dockerfile` nếu cấu hình đúng `Root Directory` là `my-production-agent` (nếu bạn deploy toàn kho).
4. Thiết lập 2 biến môi trường bắt buộc trong Dashboard của Render:
   - `REDIS_URL`: URL tới máy chủ chứa Redis (VD: Internal/External Redis URL).
   - `AGENT_API_KEY`: Chuỗi mật khẩu bảo mật của riêng bạn.
5. Save & Deploy. Render sẽ tự động build image đa lớp và tiến hành Graceful run.

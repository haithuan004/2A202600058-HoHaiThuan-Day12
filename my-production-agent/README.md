# my-production-agent

AI Agent được containerize dựa trên các nguyên tắc ứng dụng 12-factor cho Production hoàn chỉnh.

## Features
- **FastAPI Core**: Minimal and fast base framework
- **Docker Multi-stage Builds**: Minimal production image
- **Security Check**: API Key authentication layer
- **Redis Load Balance**: 10req/min Rate Limit and Cost Guarding
- **Graceful Shutdown Integration**: Liveness and readiness endpoints

## Cài đặt từ đầu
Môi trường yêu cầu: **Docker** & **Docker Compose**

Chạy Docker-compose:
```bash
docker compose up --scale agent=3 -d
```
> Việc này sẽ khởi chạy 3 backend của FastApi AI Agent, 1 Nginx HTTP proxy reverse, cùng Redis phục vụ Load Balancing.

## Cài đặt môi trường Production trên Cloud
Hãy trỏ Cloud Deployment provider (Render, Railway, v.v) vào thư mục này để thực thi Image. Yêu cầu có `REDIS_URL` trên Platform đã public.

```bash
railway init
railway up
```

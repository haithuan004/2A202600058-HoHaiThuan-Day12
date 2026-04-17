# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Hardcoded API secrets.
2. Sử dụng port cố định.
3. Kích hoạt Debug mode (`debug=True`) ở môi trường chạy.
4. Không có endpoint health check.
5. Không có cơ chế xử lý Graceful shutdown khi container bị dừng.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Why Important? |
|---------|---------|------------|----------------|
| Config | Hardcode | Env vars | Tránh lộ thông tin nhạy cảm và giúp ứng dụng có thể chạy ở bất kỳ môi trường nào mà không cần sửa đổi mã nguồn. |
| Health check | Không có | Có | Giúp Cloud Platform tự động phát hiện lỗi và khởi động lại ứng dụng nếu nó bị treo (Self-healing). |
| Logging | print() | JSON Log | Giúp các công cụ giám sát (như ELK, Datadog) tự động phân tích và tìm lỗi nhanh chóng khi traffic lớn. |
| Shutdown | Đột ngột | Graceful | Tăng trải nghiệm người dùng, đảm bảo hệ thống luôn ổn định ngay cả khi đang bảo trì hoặc cập nhật phiên bản mới. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim`
2. Working directory: `/app`
3. Tại sao COPY requirements.txt trước?: Docker chạy caching theo từng lớp (layers). Việc copy file requirements.txt và cài requirements trước sẽ giúp tận dụng cache layer cho các lần build sau nếu file này không thay đổi, tiết kiệm thời gian chờ tải và cài lại thư viện.
4. CMD vs ENTRYPOINT khác nhau thế nào?: `ENTRYPOINT` định nghĩa executable command cố định mà container luôn chạy, khó bị lướt/ghi đè. `CMD` chứa arguments mặc định để có thể bị lệnh từ dòng run của docker ghi đè dễ dàng.

### Exercise 2.3: Image size comparison
*(Với cấu trúc Multi-stage build và Slim image)*
- Develop: ~1.02 GB
- Production: ~165 MB
- Difference: ~84% (Giảm 84% dung lượng)

## Part 3: Cloud Deployment

### Exercise 3.1: Railway / Render deployment
*(Khi bạn kết nối repository với Railway hoặc Render, hãy dán URL được cung cấp vào đây)*
- URL: `https://twoa202600058-hohaithuan-day12.onrender.com`
- Screenshot: `[Đã lưu ảnh dashboard.png, running.png và test.png đính kèm]` 

## Part 4: API Security

### Exercise 4.1-4.3: Test results
**Test 1: Lỗi xác thực (Không Authentication)**
`{"detail":"Invalid API Key"}`  (Mã lỗi: 401)

**Test 2: Request bình thường (Có Auth)**
`{"reply":"I am a mock response to 'test'","history":["Q: test","A: I am a mock response to 'test'"]}` (Mã lỗi: 200)

**Test 3: Rate Limiting (Spam 15 lần trong 1 phút)**
Lần 11 sẽ bị chặn chặn đứng với lỗi: `{"detail":"Rate limit exceeded"}` (Mã lỗi: 429)

### Exercise 4.4: Cost guard implementation
Logic được triển khai: Ta sử dụng Redis làm in-memory database để lưu giữ ngân sách. Tên Key (khóa lưu giữ giá trị) quy định mức spending mỗi tháng có chứa User ID (ví dụ: `budget:user_id:2026-04`).
- Trước mỗi request, lấy giá trị hiện tại ra, nếu cộng thêm chi phí ước lượng của lượt Request mới (VD $0.05) mà vượt $10, sẽ báo lỗi HTTP 402 Payment Required.
- Nếu không vượt, update lại khoản này trong Redis, gia hạn Expire để sang tháng sau nó tự reset.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Health checks: Setup endpoint GET `/health` (return "ok" cho biết app có thể chạy) và GET `/ready` (Ping thử Redis connection để xem sẵn sàng truy vấn chưa).
- Graceful shutdown: Bắt sự kiện hệ thống `SIGTERM` và `SIGINT` với Python `signal`, đặt cờ `is_shutting_down = True`, chờ 1 khoảng trước khi thoát hoàn toàn; Server Fastapi middleware sẽ trả về HTTP 503 khi server đang shutdown để báo với Cloud điều hướng Request sang node khác.
- Phân tán Stateful: Tránh lưu hội thoại trên RAM ứng dụng, mọi dữ liệu chat giữa Agent và User được đẩy vào Redis qua key History, qua đó Nginx chia lượng tải tới Agent nào thì Agent đó vẫn có thông tin context cũ.

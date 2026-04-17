# Deployment Information

## Public URL
Chưa cấu hình Server

## Platform
Railway / Render *(Chọn sau)*

## Test Commands

### Health Check
```bash
curl https://[YOUR_URL]/health
# Expected: {"status": "ok"}
```

### API Test (with authentication)
```bash
curl -X POST https://[YOUR_URL]/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user1", "question": "Hello"}'
```

## Environment Variables Set
- PORT=8000
- REDIS_URL=redis://redis:6379/0
- AGENT_API_KEY=my-secret-key
- LOG_LEVEL=INFO
- RATE_LIMIT_PER_MINUTE=10
- MONTHLY_BUDGET_USD=10.0

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)

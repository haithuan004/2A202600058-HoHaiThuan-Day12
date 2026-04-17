from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import signal
import sys
import redis
import time

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit, r as redis_rate_client
from .cost_guard import check_budget, r as redis_budget_client
from .logger import logger
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.mock_llm import generate_response

is_shutting_down = False
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class AskRequest(BaseModel):
    question: str
    user_id: str = "default_user"

def rate_limiter_dep(req: AskRequest):
    check_rate_limit(req.user_id)

def budget_dep(req: AskRequest):
    check_budget(req.user_id)

def shutdown_handler(signum, frame):
    global is_shutting_down
    logger.info("Received termination signal, shutting down gracefully...")
    is_shutting_down = True
    time.sleep(1)
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    yield
    logger.info("Application shutting down...")
    redis_client.close()

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def graceful_shutdown_middleware(request, call_next):
    if is_shutting_down:
        return JSONResponse(status_code=503, content={"detail": "Service is shutting down"})
    response = await call_next(request)
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        redis_client.ping()
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        return JSONResponse(status_code=503, content={"status": "not ready"})

@app.post("/ask")
async def ask(
    req: AskRequest,
    api_key_valid: str = Depends(verify_api_key),
    _rate_limit: None = Depends(rate_limiter_dep),
    _budget: None = Depends(budget_dep)
):
    logger.info(f"Processing request for user {req.user_id}")
    
    history_key = f"history:{req.user_id}"
    history = redis_client.lrange(history_key, 0, -1)
    
    response = await generate_response(req.question)
    
    redis_client.rpush(history_key, f"Q: {req.question}")
    redis_client.rpush(history_key, f"A: {response}")
    redis_client.ltrim(history_key, -20, -1) 

    return {
        "reply": response,
        "history": history
    }

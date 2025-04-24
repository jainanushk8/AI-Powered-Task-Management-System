# ai-service/main.py

import time
import logging
import logging.config

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from routes import sentiment, optimization, schedule_predict, chat, tasks
from logging_config import LOGGING_CONFIG

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth import create_access_token
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse




# ─── Configure structured logging ───────────────────────────────────────────
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# ─── Create FastAPI app ─────────────────────────────────────────────────────
app = FastAPI(title="AI Microservice for App")

# ─── CORS Middleware ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Prometheus Metrics ─────────────────────────────────────────────────────
REQUEST_COUNT = Counter(
    "app_request_count", "Total HTTP requests",
    ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "HTTP request latency in seconds",
    ["method", "endpoint"]
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace with your user authentication logic
    user_dict = {"username": "testuser", "password": "testpass"}
    if form_data.username != user_dict["username"] or form_data.password != user_dict["password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user_dict["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start

    method = request.method
    path = request.url.path
    status = response.status_code

    REQUEST_COUNT.labels(method=method, endpoint=path, http_status=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=path).observe(elapsed)

    return response

@app.get("/metrics")
async def metrics():
    """
    Expose Prometheus metrics.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

# ─── Static files & favicon ─────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# ─── Mount your API routers ─────────────────────────────────────────────────
app.include_router(tasks.router)
app.include_router(chat.router)
app.include_router(sentiment.router, prefix="/api/sentiment", tags=["Sentiment"])
app.include_router(optimization.router, prefix="/api/optimize-task", tags=["Optimization"])
app.include_router(schedule_predict.router, prefix="/api/schedule-predict", tags=["Scheduling"])

# ─── Health check ───────────────────────────────────────────────────────────
@app.get("/")
def read_root():
    logger.info("Health check OK")
    return {"message": "AI microservice is live!"}

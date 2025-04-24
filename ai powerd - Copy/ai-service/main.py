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

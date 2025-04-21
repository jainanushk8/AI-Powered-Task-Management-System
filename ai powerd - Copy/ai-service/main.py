from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import sentiment, optimization, schedule_predict

app = FastAPI(title="AI Microservice for Jira App")

# ✅ Add this CORS middleware setup here:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔌 Connect the routes
app.include_router(sentiment.router, prefix="/api/sentiment")
app.include_router(optimization.router, prefix="/api/optimize-task")
app.include_router(schedule_predict.router, prefix="/api/schedule-predict")

@app.get("/")
def read_root():
    return {"message": "AI microservice is live!"}

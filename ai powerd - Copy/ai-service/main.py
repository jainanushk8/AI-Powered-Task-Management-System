from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import sentiment, optimization, schedule_predict, chat, tasks  # Combined imports for better structure

# Create the FastAPI app instance
app = FastAPI(title="AI Microservice for Jira App")

# Middleware setup for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from the different modules
app.include_router(tasks.router)  # Tasks route
app.include_router(chat.router)   # Chat route
app.include_router(sentiment.router, prefix="/api/sentiment")  # Sentiment analysis route
app.include_router(optimization.router, prefix="/api/optimize-task")  # Task optimization route
app.include_router(schedule_predict.router, prefix="/api/schedule-predict")  # Schedule prediction route

# Test route to check if the service is live
@app.get("/")
def read_root():
    return {"message": "AI microservice is live!"}

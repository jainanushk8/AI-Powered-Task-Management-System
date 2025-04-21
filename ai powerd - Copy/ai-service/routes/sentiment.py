from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.sentiment_model import SentimentModel

router = APIRouter()
sentiment_model = SentimentModel()

class SentimentRequest(BaseModel):
    text: str

@router.post("/")
async def get_sentiment(request: SentimentRequest):
    try:
        result = sentiment_model.analyze_sentiment(request.text)
        return {"label": result["label"], "confidence": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

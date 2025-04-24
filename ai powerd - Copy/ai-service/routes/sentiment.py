# ai-service/routes/sentiment.py

from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.sentiment_model import SentimentModel

router = APIRouter()
sentiment_model = SentimentModel()

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    label: str
    confidence: float

@router.post(
    "/", 
    response_model=SentimentResponse,
    summary="Run sentiment analysis on input text"
)
async def get_sentiment(request: SentimentRequest) -> SentimentResponse:
    try:
        # Call the sentiment model's predict_sentiment method
        raw_output = sentiment_model.predict_sentiment(request.text)
        
        # Log the raw output to see its structure
        print(f"Raw model output: {raw_output}")

        # Ensure the output is a dict and it has the correct keys
        if "label" not in raw_output or "confidence" not in raw_output:
            raise HTTPException(status_code=500, detail="Invalid model output format")

        # Ensure `label` is a string and `confidence` is a float
        label = str(raw_output["label"])  # Force label to be a string
        confidence = float(raw_output["confidence"])  # Force confidence to be a float

        return SentimentResponse(label=label, confidence=round(confidence, 4))

    except Exception as e:
        # Catch any error and raise an HTTP exception
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# A simple GET route to verify the router is live
@router.get("/test", summary="Test that sentiment router is live")
async def test_route():
    return {"message": "Sentiment route is working"}

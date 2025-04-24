# ai-service/routes/sentiment.py

from typing import Dict, Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from models.sentiment_model import SentimentModel
import logging

router = APIRouter()
model = SentimentModel()
logger = logging.getLogger(__name__)

class SentimentRequest(BaseModel):
    # Use Field() instead of a direct constr() call in the annotation
    text: str = Field(..., min_length=1, max_length=500)

    @validator("text")
    def no_only_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must contain non-whitespace characters")
        return v

class SentimentResponse(BaseModel):
    label: str
    confidence: float

@router.post(
    "/",
    response_model=SentimentResponse,
    summary="Run sentiment analysis on input text",
    tags=["Sentiment"]
)
async def get_sentiment(request: SentimentRequest) -> SentimentResponse:
    """
    Analyze sentiment of the provided text.
    """
    logger.info("Received sentiment request: %r", request.text[:30] + ("…" if len(request.text)>30 else ""))
    raw_output: Dict[str, Union[str, float]] = model.predict_sentiment(request.text)

    if "error" in raw_output:
        logger.error("Model returned error: %s", raw_output["error"])
        raise HTTPException(
            status_code=500,
            detail=f"Sentiment model error: {raw_output['error']}"
        )

    try:
        label = str(raw_output["label"])
        confidence = round(float(raw_output["confidence"]), 4)
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Invalid model output format: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Invalid format from sentiment model"
        )

    logger.info("Returning sentiment: %s (%.4f)", label, confidence)
    return SentimentResponse(label=label, confidence=confidence)

@router.get("/test", summary="Test that sentiment router is live", tags=["Sentiment"])
async def test_route():
    """Simple GET to verify router is up."""
    return {"message": "Sentiment route is working"}

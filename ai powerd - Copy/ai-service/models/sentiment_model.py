from transformers.pipelines import pipeline
from typing import Dict, Union
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class SentimentModel:
    def __init__(self):
        """
        Initializes a sentiment-analysis pipeline with a specific pretrained model and revision.
        """
        self._pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            revision="714eb0f"
        )

    @lru_cache(maxsize=256)
    def predict_sentiment(self, text: str) -> Dict[str, Union[str, float]]:
        """
        Predicts sentiment for a given text using a pretrained transformer model.

        Results for identical texts will be cached (up to 256 unique inputs).
        """
        logger.debug("Running pipeline for text: %r", text[:50] + ("…" if len(text) > 50 else ""))
        try:
            raw = self._pipeline(text)
        except Exception as e:
            logger.error("Pipeline error: %s", e, exc_info=True)
            return {"label": "ERROR", "confidence": 0.0, "error": str(e)}

        if (not raw or not isinstance(raw, list) 
                or not isinstance(raw[0], dict) 
                or "label" not in raw[0] or "score" not in raw[0]):
            logger.warning("Unexpected pipeline output: %r", raw)
            return {"label": "UNKNOWN", "confidence": 0.0}

        label = raw[0]["label"]
        score = raw[0]["score"]
        logger.debug("Pipeline output: %s (%.4f)", label, score)
        return {"label": label, "confidence": round(float(score), 4)}

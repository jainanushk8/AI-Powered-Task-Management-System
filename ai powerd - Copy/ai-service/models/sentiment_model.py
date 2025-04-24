from transformers.pipelines import pipeline
from typing import Dict, Union

class SentimentModel:
    def __init__(self):
        self.pipeline = pipeline("sentiment-analysis")

    def predict_sentiment(self, text: str) -> Dict[str, Union[float, str]]:
        result = self.pipeline(text)
        if not result or not isinstance(result, list) or not isinstance(result[0], dict):
            return {"label": "UNKNOWN", "confidence": 0.0}

        label = result[0].get("label", "UNKNOWN")
        score = result[0].get("score", 0.0)

        return {
            "label": label,
            "confidence": round(float(score), 4)
        }

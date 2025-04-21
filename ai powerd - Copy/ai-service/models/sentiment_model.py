from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self.model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def analyze_sentiment(self, text: str):
        result = self.model(text)
        return result[0]  # {'label': 'POSITIVE', 'score': 0.98}

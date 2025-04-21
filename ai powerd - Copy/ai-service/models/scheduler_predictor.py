from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class SchedulerPredictor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("nreimers/MiniLMv2-L6-H384-distilled")
        self.model = AutoModelForSequenceClassification.from_pretrained("nreimers/MiniLMv2-L6-H384-distilled")

    def predict(self, text_input: str):
        inputs = self.tokenizer(text_input, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).numpy()[0]

        # Hypothetical interpretation:
        # Index 0 = On time
        # Index 1 = Slight delay
        # Index 2 = Major delay
        # Index 3 = Urgent/Immediate
        predicted_class = np.argmax(probabilities)

        return {
            "predicted_label": int(predicted_class),
            "confidence_scores": probabilities.tolist()
        }

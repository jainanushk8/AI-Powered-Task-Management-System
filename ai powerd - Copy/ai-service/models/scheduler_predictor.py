from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

class SchedulerPredictor:
    def __init__(self):
        # ✅ Use a public & lightweight transformer
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
        self.model.eval()

    def predict(self, text_input: str):
        inputs = self.tokenizer(text_input, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).numpy()[0]

        # Hypothetical interpretation remains (you can train/fine-tune for better labels later)
        predicted_class = np.argmax(probabilities)

        return {
            "predicted_label": int(predicted_class),
            "confidence_scores": probabilities.tolist()
        }

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class TaskOptimizer:
    def __init__(self):
        model_path = "models/task_priority_model.pkl"
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.model = RandomForestRegressor()
            # In prod, you would train the model and save
            # For now, use a dummy model until training is done

    def predict_priority(self, features: list):
        prediction = self.model.predict([features])
        return float(prediction[0])

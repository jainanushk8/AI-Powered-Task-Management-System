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
            # If the model doesn't exist, train a dummy model and save it
            self.model = RandomForestRegressor()
            # Dummy data for training (replace with your actual training data)
            X_train = np.array([[5, 3, 10], [3, 2, 5], [6, 4, 12]])  # Example features
            y_train = np.array([1, 2, 3])  # Example labels (priority score)
            self.model.fit(X_train, y_train)
            joblib.dump(self.model, model_path)  # Save the trained model

    def predict_priority(self, features: list):
        prediction = self.model.predict([features])
        return float(prediction[0])

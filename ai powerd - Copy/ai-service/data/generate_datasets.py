import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples, output_file):
    """
    Generate synthetic data for training or testing.
    Each row contains features and a target value.
    """
    # Generate random features (e.g., 5 features per sample)
    X = np.random.rand(num_samples, 5) * 100  # Features scaled between 0 and 100
    # Generate target values as a linear combination of features with some noise
    coefficients = [2.5, -1.2, 3.0, 0.8, -0.5]  # Coefficients for the linear relationship
    noise = np.random.randn(num_samples) * 5  # Add some noise
    y = np.dot(X, coefficients) + noise  # Linear relationship with noise

    # Combine features and target into a DataFrame
    data = pd.DataFrame(X, columns=[f"Feature_{i+1}" for i in range(X.shape[1])])
    data["Target"] = y

    # Save to CSV
    data.to_csv(output_file, index=False)
    print(f"Dataset with {num_samples} samples saved to {output_file}")

# Generate training dataset
generate_synthetic_data(100, "f:\\CHat with PDF and Audio\\ai-task-management-system\\ai\\data\\training_data.csv")

# Generate testing dataset
generate_synthetic_data(100, "f:\\CHat with PDF and Audio\\ai-task-management-system\\ai\\data\\testing_data.csv")
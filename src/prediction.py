"""
Copyright 2021-2022 Leonardo Furnielis.
Licensed under MIT License
"""

from tensorflow import keras
import numpy as np

model = keras.models.load_model('models/neural_network.h5')

def model_predict(X):
    """Execute the model to predict sentiment of text
    Args:
        X (lilst): The text to predict (post text feature engineering)
    
    Returns:
        dict: The result of predictin and it's confidence
    """   
    predicted = model.predict(X)
    predicted = predicted[0]
    if predicted[0] > predicted[1]:
        result = {
            'sentiment': 'negative',
            'confidence': np.float64(predicted[0])
        }
    else:
        result = {
            'sentiment': 'positive',
            'confidence': np.float64(predicted[1])
        }
    return result
